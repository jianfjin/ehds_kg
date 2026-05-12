#!/usr/bin/env python3
"""
verify-semantic-search.py
=========================
Quick end-to-end probe for the EHDS semantic search pipeline.
Run after `python3 src/ehds_embedding.py --build` and after starting the API server.

Usage:
    cd ~/projects/ehds_kg
    python3 scripts/verify-semantic-search.py

Exit code 0 = all probes passed.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_ROOT = PROJECT_ROOT / "cache"
API_BASE = "http://127.0.0.1:8080"
PROBES: list[dict] = []


def record(name: str, passed: bool, detail: str = ""):
    PROBES.append({"name": name, "passed": passed, "detail": detail})
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))


def main():
    print("[*] Probing EHDS Semantic Search Pipeline...")
    failed = False

    # 1. TF-IDF artifacts exist
    db_exists = (CACHE_ROOT / "ehds_embeddings.db").exists()
    pkl_exists = (CACHE_ROOT / "ehds_tfidf.pkl").exists()
    record(
        "TF-IDF artifacts exist",
        db_exists and pkl_exists,
        f"db={db_exists}, pkl={pkl_exists}",
    )
    if not (db_exists and pkl_exists):
        print("[!] Run: cd ~/projects/ehds_kg && python3 src/ehds_embedding.py --build")
        failed = True

    # 2. API health
    try:
        with urllib.request.urlopen(f"{API_BASE}/api/health", timeout=5) as resp:
            data = json.loads(resp.read())
            healthy = data.get("status") == "healthy"
            record("API health check", healthy)
            if not healthy:
                failed = True
    except Exception as exc:
        record("API health check", False, str(exc))
        failed = True

    # 3. Stack counts
    try:
        with urllib.request.urlopen(f"{API_BASE}/api/stack", timeout=5) as resp:
            data = json.loads(resp.read())
            index_count = data.get("index", 0)
            record("Index layer count > 0", index_count > 0, f"count={index_count}")
    except Exception as exc:
        record("Index layer count", False, str(exc))
        failed = True

    # 4. Semantic search returns results
    try:
        url = f"{API_BASE}/api/search?q=HDAB+approval"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
            match_count = data.get("match_count", 0)
            record("Search returns matches", match_count > 0, f"matches={match_count}")
            if match_count == 0:
                failed = True
    except Exception as exc:
        record("Search returns matches", False, str(exc))
        failed = True

    # 5. Citation resolution
    try:
        url = f"{API_BASE}/api/resolve?citation=Art.54(2)"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            found = data.get("found", False)
            record("Citation resolution", found, f"stable_id={data.get('stable_id')}")
            if not found:
                failed = True
    except Exception as exc:
        record("Citation resolution", False, str(exc))
        failed = True

    # Summary
    print("\n" + "=" * 50)
    total = len(PROBES)
    passed = sum(1 for p in PROBES if p["passed"])
    print(f"RESULTS: {passed}/{total} probes passed")
    if failed:
        print("[!] Semantic search pipeline is NOT ready.")
        sys.exit(1)
    else:
        print("[+] Semantic search pipeline is ready.")
        sys.exit(0)


if __name__ == "__main__":
    main()
