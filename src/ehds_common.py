#!/usr/bin/env python3
"""
EHDS Knowledge Graph — Shared Utilities
========================================
Extracted from ehds_mcp_server.py dependencies.
Import this from all EHDS tools instead of the Hermes MCP server.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Project root: two levels up from src/ehds_common.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Layer directories
INDEX_ROOT = PROJECT_ROOT / "ehds_index"
WIKI_ROOT = PROJECT_ROOT / "ehds_wiki"
KB_ROOT = PROJECT_ROOT / "ehds_kb"
CACHE_ROOT = PROJECT_ROOT / "cache"
DATA_ROOT = PROJECT_ROOT / "data"
SCRIPTS_ROOT = PROJECT_ROOT / "scripts"
DOCS_ROOT = PROJECT_ROOT / "docs"

# Index entry cache
_index_cache: Optional[Dict[str, Dict[str, Any]]] = None
_index_cache_time: float = 0.0


# ---------------------------------------------------------------------------
# Frontmatter Parser (using yaml if available, else simple parser)
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """Split YAML frontmatter from body. Returns (meta, body)."""
    meta: Dict[str, Any] = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2]
            try:
                import yaml
                meta = yaml.safe_load(fm_text) or {}
            except ImportError:
                # Fallback: simple line parser
                for line in fm_text.split("\n"):
                    line = line.strip()
                    if ":" in line:
                        key, _, val = line.partition(":")
                        key = key.strip()
                        val = val.strip().strip('"').strip("'")
                        # Try numeric conversion
                        try:
                            val = int(val)
                        except ValueError:
                            try:
                                val = float(val)
                            except ValueError:
                                pass
                        meta[key] = val
    return meta, body


# ---------------------------------------------------------------------------
# Index Layer — Article Loading
# ---------------------------------------------------------------------------

def _load_index_entries() -> Dict[str, Dict[str, Any]]:
    """Load all Index articles keyed by stable_id. Cached for 300s."""
    global _index_cache, _index_cache_time
    import time
    now = time.time()
    if _index_cache is not None and (now - _index_cache_time) < 300:
        return _index_cache

    entries: Dict[str, Dict[str, Any]] = {}
    if not INDEX_ROOT.exists():
        return entries

    for f in sorted(INDEX_ROOT.glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        meta, body = _parse_frontmatter(text)
        sid = meta.get("stable_id", "")
        if not sid:
            continue

        # Parse anchors from ## Para N sections. Store both legacy ParaN
        # keys and canonical A###-PN keys when explicit [[A###-PN]] anchors
        # are present, so old citation calls and regenerated zero-padded
        # Article files resolve through the same public API.
        anchors: Dict[str, str] = {}
        para_pattern = re.compile(r"^## (Para \d+)$", re.MULTILINE)
        paras = re.split(r"^## Para \d+$", body, flags=re.MULTILINE)
        para_names = para_pattern.findall(body)
        for i, name in enumerate(para_names):
            if i + 1 < len(paras):
                snippet = paras[i + 1].strip()[:500]
                legacy_key = name.replace(" ", "")
                anchors[legacy_key] = snippet
                explicit = re.search(r"\[\[([^\]]+)\]\]", snippet)
                if explicit:
                    anchors[explicit.group(1)] = snippet

        entries[sid] = {
            "stable_id": sid,
            "article": meta.get("article", 0),
            "title": meta.get("title", ""),
            "chapter": meta.get("chapter", ""),
            "category": meta.get("category", ""),
            "filename": f.name,
            "anchors": anchors,
            "body": body,
        }

    _index_cache = entries
    _index_cache_time = now
    return entries


# ---------------------------------------------------------------------------
# Citation Resolution
# ---------------------------------------------------------------------------

def _resolve_citation(
    citation: str, index: Optional[Dict[str, Dict[str, Any]]] = None
) -> Optional[Dict[str, Any]]:
    """Resolve citation string to an Index article entry."""
    if index is None:
        index = _load_index_entries()
    if not index:
        return None

    c = citation.strip()

    # 1. Exact stable_id match. Accept both canonical zero-padded
    # EHDS-2025-327-A054 and legacy non-padded EHDS-2025-327-A54.
    stable_match = re.fullmatch(r"(EHDS-2025-327-A)(\d{1,3})(?:-(.+))?", c, re.IGNORECASE)
    if stable_match:
        canonical = f"{stable_match.group(1).upper()}{int(stable_match.group(2)):03d}"
        entry = index.get(canonical)
        if entry:
            anchor_key = stable_match.group(3)
            if anchor_key:
                for ak in entry.get("anchors", {}):
                    if anchor_key.lower() in ak.lower() or ak.lower().endswith(anchor_key.lower()):
                        return {"entry": entry, "anchor": ak, "anchor_text": entry["anchors"][ak]}
            return {"entry": entry}
    if c in index:
        return {"entry": index[c]}

    # 2. Stable ID + anchor fallback for any custom stable IDs.
    for sid in index:
        if c.startswith(sid) and len(c) > len(sid):
            anchor_key = c[len(sid) + 1:] if c[len(sid)] == "-" else c[len(sid):]
            entry = index[sid]
            for ak in entry.get("anchors", {}):
                if anchor_key.lower() in ak.lower():
                    return {"entry": entry, "anchor": ak, "anchor_text": entry["anchors"][ak]}
            return {"entry": entry}

    # 3. Article ref (e.g. "Art. 54" or "Art.54")
    art_match = re.match(r"Art\.?\s*(\d+)", c, re.IGNORECASE)
    if art_match:
        art_num = int(art_match.group(1))
        para_match = re.search(r"\((\d+)\)", c)
        para_num = int(para_match.group(1)) if para_match else None
        for sid, entry in index.items():
            if entry.get("article") == art_num:
                result: Dict[str, Any] = {"entry": entry}
                if para_num:
                    anchor_key = f"Para{para_num}"
                    if anchor_key in entry.get("anchors", {}):
                        result["anchor"] = anchor_key
                        result["anchor_text"] = entry["anchors"][anchor_key]
                return result

    # 4. Full legal cite
    reg_match = re.match(r"Reg\.\s*\(EU\)\s*(\d+)/(\d+).*Art\.\s*(\d+)", c, re.IGNORECASE)
    if reg_match:
        art_num = int(reg_match.group(3))
        for sid, entry in index.items():
            if entry.get("article") == art_num:
                return {"entry": entry}

    return None


# ---------------------------------------------------------------------------
# KB Path Resolution & Walking
# ---------------------------------------------------------------------------

KB_ROOTS = [INDEX_ROOT, WIKI_ROOT, KB_ROOT]


def _resolve_kb_path(user_path: str) -> Optional[Path]:
    """Resolve a user-provided path against KB roots. Returns None if unsafe."""
    p = Path(user_path)

    # 1. Try relative to project root
    candidate = PROJECT_ROOT / p
    if candidate.exists() and _is_inside_roots(candidate):
        return candidate.resolve()

    # 2. Try relative to each KB root
    for root in KB_ROOTS:
        candidate = root / p.name
        if candidate.exists() and _is_inside_roots(candidate):
            return candidate.resolve()

    return None


def _is_inside_roots(path: Path) -> bool:
    """Check if resolved path is within any KB root."""
    resolved = path.resolve()
    for root in KB_ROOTS:
        try:
            resolved.relative_to(root.resolve())
            return True
        except ValueError:
            continue
    return False


def _walk_kb() -> List[Dict[str, str]]:
    """Walk all KB roots and return file metadata."""
    results: List[Dict[str, str]] = []
    layer_map = {
        "ehds_index": "index",
        "ehds_wiki": "wiki",
        "ehds_kb": "kb",
    }
    for root in KB_ROOTS:
        if not root.exists():
            continue
        layer = layer_map.get(root.name, root.name)
        for f in sorted(root.glob("*.md")):
            results.append({
                "path": str(f.relative_to(PROJECT_ROOT)),
                "absolute": str(f),
                "layer": layer,
                "size": f.stat().st_size,
            })
    return results


# ---------------------------------------------------------------------------
# File Readers
# ---------------------------------------------------------------------------

def _read_text_file(path: Path) -> str:
    """Read a text/markdown file."""
    return path.read_text(encoding="utf-8", errors="replace")


def _read_pdf_file(path: Path) -> str:
    """Read a PDF file with PyMuPDF if available, else return empty."""
    try:
        import fitz
        doc = fitz.open(str(path))
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except ImportError:
        return ""


def _read_pdf_file_structured(path: Path) -> List[Dict[str, Any]]:
    """Read PDF with page/bbox coordinates."""
    try:
        import fitz
        doc = fitz.open(str(path))
        blocks: List[Dict[str, Any]] = []
        line_estimate = 1
        for page in doc:
            for block in page.get_text("blocks"):
                x0, y0, x1, y1, text, *_ = block
                blocks.append({
                    "page": page.number + 1,
                    "bbox": [x0, y0, x1, y1],
                    "text": text.strip(),
                    "line_estimate": line_estimate,
                })
                line_estimate += text.count("\n") + 1
        return blocks
    except ImportError:
        return []


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def _search_in_file(path: Path, keywords: List[str]) -> Optional[str]:
    """Search for all keywords in a file. Return snippet or None."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace").lower()
    except Exception:
        return None
    lowered_keywords = [k.lower() for k in keywords]
    if not all(k in text for k in lowered_keywords):
        return None
    # Return first 300 chars as snippet
    lines = text.split("\n")
    for i, line in enumerate(lines):
        for kw in lowered_keywords:
            if kw in line:
                start = max(0, i - 1)
                end = min(len(lines), i + 3)
                snippet = "\n".join(lines[start:end])
                return snippet[:300]
    return text[:300]


# ---------------------------------------------------------------------------
# Audit Rule Engine
# ---------------------------------------------------------------------------

def audit_document(path_str: str) -> Dict[str, Any]:
    """Run compliance audit on a document. Returns JSON-LD audit report."""
    resolved = _resolve_kb_path(path_str)
    if not resolved:
        return {"error": "Not found or outside KB roots", "path": path_str}

    if resolved.suffix == ".md":
        text = _read_text_file(resolved)
    elif resolved.suffix == ".pdf":
        text = _read_pdf_file(resolved)
    else:
        text = ""

    lowered = text.lower()
    violations: List[Dict[str, Any]] = []

    # Built-in audit rules
    rules = [
        ("EHDS-SEC-AUTH-001", "critical", "Missing HDAB authorisation reference",
         ["hdab", "health data access body"]),
        ("EHDS-SEC-MIN-001", "high", "Missing data minimisation principle",
         ["minimisation", "minimization", "data minim"]),
        ("EHDS-SEC-PURPOSE-001", "high", "Missing scientific research purpose limitation",
         ["scientific research", "purpose limit"]),
        ("EHDS-SEC-XFER-001", "medium", "Missing international transfer safeguards",
         ["adequacy decision", "standard contractual clauses", "scc", "international transfer"]),
        ("EHDS-SEC-CONSENT-001", "medium", "Missing consent or opt-out mechanism",
         ["consent", "opt-out", "opt out", "right to object"]),
        ("EHDS-SEC-PENALTY-001", "high", "Missing penalty/fine reference",
         ["penalty", "fine", "infringement", "administrative fine"]),
        ("EHDS-SEC-LINK-001", "critical", "Missing data linkage governance: no HDAB pre-access approval reference (Art.68)",
         ["data linkage", "record linkage", "dataset combination", "linkage approval"]),
        ("EHDS-SEC-LINK-002", "high", "Record-level matching without explicit Art.68(1)(b) data permit request",
         ["article 68", "art.68", "data permit", "pre-access", "hdab managed linkage"]),
    ]

    for rule_id, severity, description, keywords in rules:
        if not any(kw in lowered for kw in keywords):
            violations.append({
                "rule_id": rule_id,
                "severity": severity,
                "violation_type": "missing",
                "description": description,
                "location": {"page": None, "bbox": None, "line_estimate": 0, "extraction_method": "text"},
                "remediation": f"Add explicit reference to: {', '.join(keywords[:2])}",
            })

    return {
        "@context": "https://schema.org",
        "@type": "AuditReport",
        "audit_status": "completed",
        "document": path_str,
        "severity_summary": {
            "critical": sum(1 for v in violations if v["severity"] == "critical"),
            "high": sum(1 for v in violations if v["severity"] == "high"),
            "medium": sum(1 for v in violations if v["severity"] == "medium"),
            "low": sum(1 for v in violations if v["severity"] == "low"),
        },
        "violations": violations,
    }
