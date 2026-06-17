#!/usr/bin/env python3
"""Collect a retrieval baseline for the EHDS KG BM25 pipeline.

Usage:
    uv run python3 scripts/retrieval_baseline.py --label before --out baseline.json
    uv run python3 scripts/retrieval_baseline.py --label after  --out baseline.json

The script appends a labeled snapshot to the output JSON file so before/after
comparisons can be made from the same artifact.
"""

import argparse
import json
import time
from collections import Counter
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ehds_embedding import get_engine


BENCHMARK_QUERIES = [
    "ethical governance recommendations",
    "collaboration challenges in EHDS",
    "Art.68 data permit",
    "secure processing environment requirements",
    "data holder responsibilities secondary use",
    "opt-out secondary use health data",
    "fees and penalties HDAB",
    "data minimisation pseudonymisation",
]


def _doc_id(result: dict) -> str:
    meta = result.get("metadata", {})
    return meta.get("document_id") or Path(result["source_path"]).stem[:4].upper()


def _section_id(result: dict) -> str:
    return result.get("metadata", {}).get("section_id", "")


def evaluate(engine, query: str, top_k: int = 10) -> dict:
    start = time.perf_counter()
    results = engine.semantic_search(query, top_k=top_k)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    doc_counts = Counter(_doc_id(r) for r in results)
    section_ids = [_section_id(r) for r in results if _section_id(r)]
    text_lengths = [len(r["text"]) for r in results]

    return {
        "query": query,
        "result_count": len(results),
        "unique_documents": len(doc_counts),
        "top_document_count": doc_counts.most_common(1)[0][1] if doc_counts else 0,
        "documents": sorted(doc_counts.keys()),
        "section_ids_present": len(section_ids),
        "avg_chunk_chars": round(sum(text_lengths) / len(text_lengths), 1) if text_lengths else 0,
        "latency_ms": elapsed_ms,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect retrieval baseline metrics")
    parser.add_argument("--label", required=True, help="Snapshot label, e.g. before or after")
    parser.add_argument("--out", default="cache/retrieval_baseline.json", help="Output JSON path")
    parser.add_argument("--top-k", type=int, default=10, help="Number of results per query")
    args = parser.parse_args()

    engine = get_engine()
    snapshot = {
        "label": args.label,
        "top_k": args.top_k,
        "queries": [evaluate(engine, q, top_k=args.top_k) for q in BENCHMARK_QUERIES],
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        data = json.loads(out_path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            data = [data]
    else:
        data = []

    # Replace any existing snapshot with the same label.
    data = [s for s in data if s.get("label") != args.label]
    data.append(snapshot)

    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[+] Baseline '{args.label}' written to {out_path}")
    print(f"    Queries: {len(snapshot['queries'])}")
    avg_latency = sum(q["latency_ms"] for q in snapshot["queries"]) / len(snapshot["queries"])
    avg_docs = sum(q["unique_documents"] for q in snapshot["queries"]) / len(snapshot["queries"])
    print(f"    Avg latency: {avg_latency:.1f} ms")
    print(f"    Avg unique documents per query: {avg_docs:.1f}")


if __name__ == "__main__":
    main()
