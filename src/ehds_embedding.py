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
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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

# Layer-level boost applied to BM25 scores in semantic_search.
LAYER_BOOST = {"data": 0.15, "wiki": 0.0, "index": 0.0}

# PDF conversion tools (e.g. markitdown) sometimes inject page markers.
_PAGE_MARKER_RE = re.compile(r"^---\s*Page\s+\d+\s*---\s*$", re.MULTILINE)

# Heading-aware chunking constants.
_CHUNK_MIN_CHARS = 256
_CHUNK_MAX_CHARS = 2000

# Split-on-newline-before-numbered-heading pattern.
# Lookahead preserves the heading text (unlike re.split on the heading itself
# which would consume the matched prefix).
_NUMBERED_HEADING_SPLIT_RE = re.compile(r"\n(?=^\d+(?:\.\d+)*\s+[A-Za-z])", re.MULTILINE)

# Markdown H2 heading pattern.
_MD_H2_RE = re.compile(r"\n## ")


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
        self.bm25 = BM25Okapi(tokenized, b=0.4)
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

    @staticmethod
    def _derive_document_id(path: Path, meta: Dict[str, Any]) -> str:
        """Derive a short document identifier like ``D8.2`` from filename/title."""
        # Filename stem first: d8.2-... or D8.2-...
        m = re.search(r"(?i)\b(d\d+\.\d+)\b", path.stem)
        if m:
            return m.group(1).upper()
        # Fall back to frontmatter title.
        title = meta.get("title", "")
        m = re.search(r"(?i)\b(d\d+\.\d+)\b", title)
        if m:
            return m.group(1).upper()
        # Final fallback.
        return path.stem[:4].upper()

    @staticmethod
    def _extract_section_id(heading: str) -> str:
        """Extract ``3.2`` from a heading like ``3.2 Governance Model``."""
        m = re.match(r"^(\d+(?:\.\d+)*)\b", heading.strip())
        return m.group(1) if m else ""

    @staticmethod
    def _section_sort_key(section_id: str) -> Tuple[int, ...]:
        """Convert ``3.2`` to (3, 2) so ``3.10`` sorts after ``3.2``."""
        try:
            return tuple(int(p) for p in section_id.split(".") if p)
        except (ValueError, AttributeError):
            return (999,)

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
        elif layer == "data":
            document_id = self._derive_document_id(path, meta)

            # Prefer Markdown H2 headings; fall back to numbered section headings.
            if _MD_H2_RE.search(body):
                parts = _MD_H2_RE.split(body)
            else:
                parts = _NUMBERED_HEADING_SPLIT_RE.split(body)

            chunks: List[Dict[str, Any]] = []
            for raw in parts:
                raw = raw.strip()
                if not raw:
                    continue
                lines = raw.split("\n", 1)
                heading = lines[0].strip()
                content = lines[1].strip() if len(lines) > 1 else ""

                # Merge tiny heading-only fragments into the previous chunk.
                if len(raw) < _CHUNK_MIN_CHARS and chunks:
                    chunks[-1]["text"] += "\n\n" + raw
                    continue

                section_id = self._extract_section_id(heading)
                chunk_text = f"{meta.get('title', path.stem)}\n{heading}\n{content}"
                if len(chunk_text) > _CHUNK_MAX_CHARS:
                    chunk_text = chunk_text[:_CHUNK_MAX_CHARS] + "..."

                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        "document_id": document_id,
                        "section_id": section_id,
                        "section": heading,
                        "source": meta.get("source", ""),
                        "document": meta.get("document", path.name),
                    },
                    "priority": 0.0,
                })

            # Second pass: merge any trailing tiny chunks backwards.
            merged: List[Dict[str, Any]] = []
            for c in chunks:
                if len(c["text"]) < _CHUNK_MIN_CHARS and merged:
                    merged[-1]["text"] += "\n\n" + c["text"]
                    # Keep the lowest section_id of the merged pair.
                    if c["metadata"]["section_id"]:
                        current = merged[-1]["metadata"]["section_id"]
                        if (not current or
                                self._section_sort_key(c["metadata"]["section_id"]) <
                                self._section_sort_key(current)):
                            merged[-1]["metadata"]["section_id"] = c["metadata"]["section_id"]
                            merged[-1]["metadata"]["section"] = c["metadata"]["section"]
                else:
                    merged.append(c)
            return merged
        else:
            # Paragraph chunking for wiki.
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
                    chunks.append({
                        "text": f"{meta.get('title', '')}\n{para}",
                        "metadata": metadata,
                        "priority": priority,
                    })
        return chunks

    def semantic_search(
        self, query: str, top_k: int = 10, layer_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        if self.bm25 is None:
            return []
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        chunks = self._load_chunks()
        candidates = []
        for i, chunk in enumerate(chunks):
            if layer_filter and chunk["layer"] != layer_filter:
                continue
            score = float(scores[i])
            if score <= 0:
                continue
            # Priority boost: newer / highlighted documents rank higher.
            priority = chunk.get("priority", 0.0)
            layer = chunk.get("layer", "")
            boosted = score * (1.0 + float(priority) + LAYER_BOOST.get(layer, 0.0))
            candidates.append({
                "similarity": round(boosted, 4),
                "source_path": chunk["source_path"],
                "layer": chunk["layer"],
                "text": chunk["text"][:2000] + "..." if len(chunk["text"]) > 2000 else chunk["text"],
                "metadata": chunk.get("metadata", {}),
            })
        candidates.sort(key=lambda x: x["similarity"], reverse=True)

        # Use a generous candidate pool so diversity rerank has options.
        candidate_pool = candidates[:max(top_k * 3, 20)]

        # Diversity rerank: top-2 per document_id, then fill remaining by score.
        by_doc = defaultdict(list)
        for r in candidate_pool:
            doc_id = self._extract_doc_id_from_result(r)
            by_doc[doc_id].append(r)

        diverse = []
        for items in by_doc.values():
            diverse.extend(items[:2])

        # Re-sort diverse set by similarity to preserve approximate ranking.
        diverse.sort(key=lambda x: x["similarity"], reverse=True)

        # Fill remaining slots if needed.
        if len(diverse) < top_k:
            used = {id(r) for r in diverse}
            remaining = [r for r in candidate_pool if id(r) not in used]
            # Score-gap tie-breaker: avoid fillers far below the best score.
            if diverse:
                best_score = diverse[0]["similarity"]
                gap_threshold = best_score * 0.5
                for r in remaining:
                    if len(diverse) >= top_k:
                        break
                    if r["similarity"] >= gap_threshold:
                        diverse.append(r)
                        used.add(id(r))
            # If still short, take the rest regardless of gap.
            if len(diverse) < top_k:
                needed = top_k - len(diverse)
                for r in remaining:
                    if needed <= 0:
                        break
                    if id(r) not in used:
                        diverse.append(r)
                        used.add(id(r))
                        needed -= 1

        results = diverse[:top_k]

        # Final ordering: group by document_id, then section_id.
        results.sort(key=lambda x: (
            self._extract_doc_id_from_result(x),
            self._section_sort_key(x.get("metadata", {}).get("section_id", "")),
        ))
        return results

    @staticmethod
    def _extract_doc_id_from_result(result: Dict[str, Any]) -> str:
        """Pull document_id from metadata or fall back to filename stem."""
        meta = result.get("metadata", {})
        doc_id = meta.get("document_id")
        if doc_id:
            return str(doc_id)
        m = re.search(r"(?i)\b(d\d+\.\d+)\b", Path(result["source_path"]).stem)
        if m:
            return m.group(1).upper()
        return Path(result["source_path"]).stem[:4].upper()


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
    parser.add_argument("--top-k", type=int, default=10)
    args = parser.parse_args()

    engine = EHDSEmbeddingEngine()
    if args.build:
        engine.build_index()
    elif args.search:
        for r in engine.semantic_search(args.search, top_k=args.top_k):
            print(f"sim={r['similarity']} | {r['layer']} | {r['source_path']}")
    else:
        parser.print_help()
