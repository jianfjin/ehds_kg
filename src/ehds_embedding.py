#!/usr/bin/env python3
"""
EHDS Semantic Embedding Engine
===============================
Production-ready BM25 semantic search with optional neural fallback.
Designed for resource-constrained VMs (2-core / 1-2GB RAM).

Usage:
    python3 ehds_embedding.py --build          # rebuild BM25 index
    python3 ehds_embedding.py --search "query" # semantic search
"""

from __future__ import annotations

import argparse
import json
import os
import pickle
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure src/ is on sys.path for sibling imports
import sys
_src = Path(__file__).resolve().parent
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from ehds_common import (
    PROJECT_ROOT, INDEX_ROOT, WIKI_ROOT, KB_ROOT, DATA_ROOT,
    CACHE_ROOT, _parse_frontmatter,
)

DB_PATH = CACHE_ROOT / "ehds_embeddings.db"
BM25_PATH = CACHE_ROOT / "ehds_bm25.pkl"

# PDF conversion tools (e.g. markitdown) sometimes inject page markers.
_PAGE_MARKER_RE = re.compile(r"^---\s*Page\s+\d+\s*---\s*$", re.MULTILINE)


# ---------------------------------------------------------------------------
# Embedding Engine
# ---------------------------------------------------------------------------

class EHDSEmbeddingEngine:
    """BM25Okapi based semantic search engine."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self.bm25_path = BM25_PATH
        self.bm25: Any = None
        self._chunks_cache: Optional[List[Dict[str, Any]]] = None
        self._init_db()
        self._load_or_build_bm25()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_path TEXT NOT NULL,
                    layer TEXT NOT NULL,
                    text TEXT NOT NULL,
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
                "SELECT id, source_path, layer, text, metadata, priority FROM chunks ORDER BY id"
            )
            rows = []
            for row in cur.fetchall():
                rows.append({
                    "id": row[0],
                    "source_path": row[1],
                    "layer": row[2],
                    "text": row[3],
                    "metadata": json.loads(row[4]) if row[4] else None,
                    "priority": row[5] if len(row) > 5 else 0.0,
                })
            self._chunks_cache = rows
            return rows

    def _load_or_build_bm25(self):
        if self.bm25_path.exists():
            with open(self.bm25_path, "rb") as f:
                cache = pickle.load(f)
            self.bm25 = cache["bm25"]
            self._chunks_cache = cache.get("chunks")
            return
        self.build_index()

    def build_index(self):
        all_chunks: List[Dict[str, Any]] = []
        roots = [
            ("index", INDEX_ROOT),
            ("wiki", WIKI_ROOT),
            ("kb", KB_ROOT),
        ]
        if DATA_ROOT.exists():
            roots.append(("data", DATA_ROOT))

        for layer, root in roots:
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

        from rank_bm25 import BM25Okapi

        tokenized = [self._tokenize(c["text"]) for c in all_chunks]
        self.bm25 = BM25Okapi(tokenized)
        self._chunks_cache = all_chunks

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM chunks")
            for c in all_chunks:
                conn.execute(
                    "INSERT INTO chunks (source_path, layer, text, metadata, priority) VALUES (?, ?, ?, ?, ?)",
                    (
                        c["source_path"],
                        c["layer"],
                        c["text"],
                        json.dumps(c.get("metadata", {})),
                        c.get("priority", 0.0),
                    ),
                )
            conn.commit()

        with open(self.bm25_path, "wb") as f:
            pickle.dump({"bm25": self.bm25, "chunks": all_chunks}, f)

        print(f"[+] Built BM25 index: {len(all_chunks)} chunks")

    @staticmethod
    def _tokenize(text: str) -> List[Any]:
        """Tokenize for BM25.

        Keeps dots and dashes intact so identifiers like ``Art.68`` and
        ``D8.2`` survive as single tokens.  Adds adjacent bigrams so that
        phrases such as ``health data`` also match as a unit.
        """
        unigrams = re.findall(r"[a-z0-9.+-]+", text.lower())
        bigrams = [
            (unigrams[i], unigrams[i + 1])
            for i in range(len(unigrams) - 1)
        ]
        return unigrams + bigrams

    def _extract_chunks(self, path: Path, layer: str) -> List[Dict[str, Any]]:
        text = path.read_text(encoding="utf-8", errors="replace")
        meta, body = _parse_frontmatter(text)

        # Title fallback for documents without frontmatter.
        if not meta.get("title"):
            meta["title"] = path.stem

        # Strip PDF conversion page markers from the body.
        body = _PAGE_MARKER_RE.sub("\n\n", body)

        chunks: List[Dict[str, Any]] = []

        if layer == "index":
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
            # Paragraph chunking for both wiki and data layers.
            for para in body.split("\n\n"):
                para = para.strip()
                if para and not para.startswith("[["):
                    priority_raw = meta.get("priority", 0)
                    try:
                        priority = float(priority_raw) if priority_raw else 0.0
                    except (TypeError, ValueError):
                        priority = 0.0
                    metadata: Dict[str, Any] = {
                        "article": meta.get("article"),
                    }
                    if layer == "wiki":
                        metadata["wiki_id"] = meta.get("wiki_id")
                    elif layer == "data":
                        metadata["source"] = meta.get("source", "")
                        metadata["document"] = meta.get("document", path.name)
                    chunks.append({
                        "text": f"{meta.get('title', '')}\n{para}",
                        "metadata": metadata,
                        "priority": priority,
                    })
        return chunks

    def semantic_search(
        self, query: str, top_k: int = 5, layer_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        if self.bm25 is None:
            return []
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        chunks = self._load_chunks()
        results = []
        for i, chunk in enumerate(chunks):
            if layer_filter and chunk["layer"] != layer_filter:
                continue
            score = float(scores[i])
            if score <= 0:
                continue
            # Priority boost: newer / highlighted documents rank higher.
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
