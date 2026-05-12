#!/usr/bin/env python3
"""
EHDS Three-Layer Stack — End-to-End Test
=========================================
Validates the neuro-symbolic compliance KB.

Usage:
    cd ~/projects/ehds_kg
    python3 scripts/test_e2e.py
"""

import sys
import os
from pathlib import Path

# Add project src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ehds_common import (
    PROJECT_ROOT, INDEX_ROOT, WIKI_ROOT, KB_ROOT,
    _load_index_entries, _resolve_citation, _parse_frontmatter,
    _resolve_kb_path, _read_text_file,
)

PASS, FAIL = "✓", "✗"
passed = failed = 0

def check(cond, msg):
    global passed, failed
    (passed, failed) = (passed + 1, failed) if cond else (passed, failed + 1)
    print(f"  {PASS if cond else FAIL} {msg}")

print("=" * 60)
print("EHDS Knowledge Stack — E2E Validation")
print(f"Project: {PROJECT_ROOT}")
print("=" * 60)

# 1. INDEX LAYER
print("\n[1/5] INDEX LAYER")
index = _load_index_entries()
check(len(index) >= 7, f"Loaded {len(index)} entries (>= 7)")
check("EHDS-2025-327-A54" in index, "Art. 54 exists")
check("EHDS-2025-327-A59" in index, "Art. 59 (HDAB) exists")
entry = index.get("EHDS-2025-327-A54", {})
check(entry.get("article") == 54, "Art. 54 number correct")
check(len(entry.get("anchors", {})) >= 4, f">=4 anchors on Art. 54")

# 2. CITATION RESOLUTION
print("\n[2/5] CITATION RESOLUTION")
cases = [
    ("EHDS-2025-327-A54", "EHDS-2025-327-A54", None),
    ("EHDS-2025-327-A54-P2", "EHDS-2025-327-A54", "P2"),
    ("Art. 54", "EHDS-2025-327-A54", None),
    ("Art. 54(2)", "EHDS-2025-327-A54", "A054-P2"),
]
for cite, sid, anchor in cases:
    r = _resolve_citation(cite, index)
    ok = r and r["entry"]["stable_id"] == sid and (not anchor or r.get("anchor") == anchor)
    check(ok, f"'{cite}' -> {sid}")
check(_resolve_citation("Art. 999", index) is None, "Missing cite returns None")

# 3. WIKI LAYER
print("\n[3/5] WIKI LAYER (Frontmatter)")
files = list(WIKI_ROOT.glob("*.md")) if WIKI_ROOT.exists() else []
check(len(files) >= 7, f"{len(files)} wiki files (>= 7)")
for f in files:
    text = f.read_text(encoding="utf-8", errors="replace")
    meta, _ = _parse_frontmatter(text)
    check("wiki_id" in meta, f"{f.name} has wiki_id")
    check("index_refs" in meta, f"{f.name} has index_refs")

# 4. PATH SECURITY + AUDIT ENGINE
print("\n[4/5] PATH SECURITY & AUDIT")
check(_resolve_kb_path("../../../etc/passwd") is None, "Traversal blocked")
kb_path = KB_ROOT / "buzzword_optimizer.md"
if kb_path.exists():
    text = _read_text_file(kb_path).lower()
    has_hdab = "hdab" in text or "health data access body" in text
    check(not has_hdab, "Non-compliant doc lacks HDAB (audit should catch)")

# 5. ARCHITECTURE DOC
print("\n[5/5] ARCHITECTURE DOCUMENTATION")
arch = PROJECT_ROOT / "THREE_LAYER_ARCHITECTURE.md"
check(arch.exists(), "THREE_LAYER_ARCHITECTURE.md exists")
if arch.exists():
    body = _read_text_file(arch)
    check("ehds_index" in body and "ehds_wiki" in body and "ehds_kb" in body,
          "Doc references all three layers")

print("\n" + "=" * 60)
print(f"RESULTS: {passed} passed, {failed} failed")
print("=" * 60)
sys.exit(0 if failed == 0 else 1)
