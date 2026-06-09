#!/usr/bin/env python3
"""
EHDS Semantic Embedding Engine
===============================
Production-ready TF-IDF semantic search with optional neural fallback.
Designed for resource-constrained VMs (2-core / 1-2GB RAM).

Usage:
    python3 ehds_embedding.py --build          # rebuild TF-IDF index
    python3 ehds_embedding.py --search "query" # semantic search
"""

from __future__ import annotations

import argparse
import json
import pickle
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from ehds_common import PROJECT_ROOT, INDEX_ROOT, WIKI_ROOT, KB_ROOT, CACHE_ROOT, _parse_frontmatter

DB_PATH = CACHE_ROOT / "ehds_embeddings.db"
TFIDF_PATH = CACHE_ROOT / "ehds_tfidf.pkl"


# ---------------------------------------------------------------------------
# Embedding Engine
# ---------------------------------------------------------------------------

class EHDSEmbeddingEngine:
    """TF-IDF based semantic search engine with sklearn."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self.tfidf_path = TFIDF_PATH
        self.vectorizer: Any = None
        self.chunk_matrix: Any = None
        self._chunks_cache: Optional[List[Dict[str, Any]]] = None
        self._init_db()
        self._load_or_build_tfidf()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_path TEXT NOT NULL,
                    layer TEXT NOT NULL,
                    text TEXT NOT NULL,
                    tfidf TEXT,
                    metadata TEXT,
                    priority REAL NOT NULL DEFAULT 0.0
                )
            """)
            conn.commit()

    def _load_chunks(self) -> List[Dict[str, Any]]:
        if self._chunks_cache is not None:
            return self._chunks_cache
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(
                "SELECT id, source_path, layer, text, tfidf, metadata, priority FROM chunks ORDER BY id"
            )
            rows = []
            for row in cur.fetchall():
                rows.append({
                    "id": row[0], "source_path": row[1], "layer": row[2],
                    "text": row[3],
                    "tfidf": json.loads(row[4]) if row[4] else None,
                    "metadata": json.loads(row[5]) if row[5] else None,
                    "priority": row[6] if len(row) > 6 else 0.0,
                })
            self._chunks_cache = rows
            return rows

    def _load_or_build_tfidf(self):
        if self.tfidf_path.exists():
            with open(self.tfidf_path, "rb") as f:
                cache = pickle.load(f)
            self.vectorizer = cache["vectorizer"]
            self.chunk_matrix = cache["chunk_matrix"]
            return
        self.build_index()

    def build_index(self):
        all_chunks: List[Dict[str, Any]] = []
        for layer, root in [("index", INDEX_ROOT),
                              ("wiki", WIKI_ROOT),
                              ("kb", KB_ROOT)]:
            if not root.exists():
                continue
            for f in sorted(root.glob("*.md")):
                chunks = self._extract_chunks(f, layer)
                for c in chunks:
                    c["layer"] = layer
                    c["source_path"] = str(f.relative_to(PROJECT_ROOT))
                all_chunks.extend(chunks)

        if not all_chunks:
            print("[!] No chunks found - nothing to index.")
            return

        from sklearn.feature_extraction.text import TfidfVectorizer
        texts = [c["text"] for c in all_chunks]
        self.vectorizer = TfidfVectorizer(
            stop_words="english", lowercase=True,
            ngram_range=(1, 2), max_features=5000,
            min_df=1, max_df=1.0,
        )
        self.chunk_matrix = self.vectorizer.fit_transform(texts)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM chunks")
            for i, c in enumerate(all_chunks):
                dense = self.chunk_matrix[i].toarray().tolist()[0]
                conn.execute(
                    "INSERT INTO chunks (source_path, layer, text, tfidf, metadata, priority) VALUES (?, ?, ?, ?, ?, ?)",
                    (c["source_path"], c["layer"], c["text"],
                     json.dumps(dense), json.dumps(c.get("metadata", {})), c.get("priority", 0.0)),
                )
            conn.commit()

        with open(self.tfidf_path, "wb") as f:
            pickle.dump({"vectorizer": self.vectorizer, "chunk_matrix": self.chunk_matrix}, f)

        print(f"[+] Indexed {len(all_chunks)} chunks, vocab={len(self.vectorizer.vocabulary_)}")

    def _extract_chunks(self, path: Path, layer: str) -> List[Dict[str, Any]]:
        text = path.read_text(encoding="utf-8", errors="replace")
        meta, body = _parse_frontmatter(text)
        chunks: List[Dict[str, Any]] = []

        if layer == "index":
            import re
            paragraphs = re.split(r"\n## Para \d+\n", body)
            para_headers = re.findall(r"\n## (Para \d+)\n", body)
            for idx, para in enumerate(paragraphs):
                para = para.strip()
                if not para:
                    continue
                header = para_headers[idx - 1] if idx > 0 and (idx - 1) < len(para_headers) else "Preamble"
                chunks.append({
                    "text": f"{meta.get('title', '')}\n{header}\n{para}",
                    "metadata": {
                        "stable_id": meta.get("stable_id"),
                        "article": meta.get("article"),
                        "header": header,
                    },
                    "priority": 0.0,
                })
        else:
            for para in body.split("\n\n"):
                para = para.strip()
                if para and not para.startswith("[["):
                    priority = float(meta.get("priority", 0)) if meta.get("priority") else 0.0
                    chunks.append({
                        "text": f"{meta.get('title', '')}\n{para}",
                        "metadata": {
                            "wiki_id": meta.get("wiki_id"),
                            "article": meta.get("article"),
                        },
                        "priority": priority,
                    })
        return chunks

    def semantic_search(
        self, query: str, top_k: int = 5, layer_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        if self.vectorizer is None or self.chunk_matrix is None:
            return []
        q_vec = self.vectorizer.transform([query])
        scores = (self.chunk_matrix * q_vec.T).toarray().ravel()
        chunks = self._load_chunks()
        results = []
        for i, chunk in enumerate(chunks):
            if layer_filter and chunk["layer"] != layer_filter:
                continue
            score = float(scores[i])
            if score <= 0:
                continue
            # Priority boost: new documents rank higher
            priority = chunk.get("priority", 0.0)
            boosted = score * (1.0 + float(priority))
            results.append({
                "similarity": round(boosted, 4),
                "source_path": chunk["source_path"],
                "layer": chunk["layer"],
                "text": chunk["text"][:280] + "..." if len(chunk["text"]) > 280 else chunk["text"],
                "metadata": chunk.get("metadata", {}),
            })
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]


# Global singleton
_engine_instance: Optional[EHDSEmbeddingEngine] = None


def get_engine() -> EHDSEmbeddingEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = EHDSEmbeddingEngine()
    return _engine_instance


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--search", type=str)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    engine = EHDSEmbeddingEngine()
    if args.build:
        engine.build_index()
    elif args.search:
        for r in engine.semantic_search(args.search, top_k=args.top_k):
            print(f"sim={r['similarity']} | {r['layer']} | {r['source_path']}")
    else:
        parser.print_help()
