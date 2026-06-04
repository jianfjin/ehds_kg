#!/usr/bin/env python3
"""
EHDS HTTP API Gateway
======================
Lightweight HTTP server that wraps the three-layer knowledge stack in REST
endpoints plus an HTML dashboard. Runs on port 8080.

Usage:
    python3 ehds_api_server.py
    # Then open http://localhost:8080/

Dependencies: Python 3.11+, no extra packages beyond stdlib.
"""

import json
import os
import time
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

from ehds_common import (
    PROJECT_ROOT, INDEX_ROOT, WIKI_ROOT, KB_ROOT, DOCS_ROOT,
    _parse_frontmatter, _load_index_entries, _resolve_citation,
    _resolve_kb_path, _walk_kb, _search_in_file, _read_text_file,
    _read_pdf_file, audit_document,
)

# Lazy-import embedding engine (avoids loading TF-IDF cache at import time)
_embedding_engine = None

# /api/retrieve query result cache: TTL 120s, max 500 entries
_retrieve_cache: dict = {}
_RETRIEVE_CACHE_TTL = 120_000  # 120 seconds
_RETRIEVE_CACHE_MAX = 500


def _get_embedding_engine():
    global _embedding_engine
    if _embedding_engine is None:
        from ehds_embedding import get_engine
        _embedding_engine = get_engine()
    return _embedding_engine

PORT = 8080

# Minimal HTML dashboard
DASHBOARD_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>EHDS Stack</title></head>
<body style="font-family:sans-serif;background:#0d1117;color:#c9d1d9;padding:20px;">
<h1>EHDS Three-Layer Knowledge Stack</h1>
<div id="stats">Loading...</div>
<script>
async function load() {
  const [stack, idx, wiki, kb] = await Promise.all([
    fetch('/api/stack').then(r=>r.json()),
    fetch('/api/index').then(r=>r.json()),
    fetch('/api/wiki').then(r=>r.json()),
    fetch('/api/kb').then(r=>r.json())
  ]);
  document.getElementById('stats').innerHTML = `
    <p>Index: ${idx.count} | Wiki: ${wiki.count} | KB: ${kb.count}</p>
    <pre>${JSON.stringify(stack, null, 2)}</pre>
  `;
}
load();
</script>
</body></html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode())

    def _html(self, html, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def do_GET(self):
        p = urllib.parse.urlparse(self.path)
        path, q = p.path, urllib.parse.parse_qs(p.query)

        if path in ("/", "/index.html"):
            return self._html(DASHBOARD_HTML)

        if path == "/api/health":
            return self._json({"status": "healthy", "layers": ["index", "wiki", "kb"]})

        if path == "/api/stack":
            def count(layer_dir):
                d = PROJECT_ROOT / layer_dir
                return len(list(d.glob("*.md"))) if d.exists() else 0
            return self._json({
                "index": count("ehds_index"),
                "wiki": count("ehds_wiki"),
                "kb": count("ehds_kb"),
            })

        if path == "/api/index":
            docs = []
            for f in sorted(INDEX_ROOT.glob("*.md")) if INDEX_ROOT.exists() else []:
                meta, _ = _parse_frontmatter(f.read_text(errors="replace"))
                docs.append({"name": f.name, "stable_id": meta.get("stable_id"), "article": meta.get("article")})
            return self._json({"count": len(docs), "documents": docs})

        if path == "/api/wiki":
            docs = []
            for f in sorted(WIKI_ROOT.glob("*.md")) if WIKI_ROOT.exists() else []:
                meta, _ = _parse_frontmatter(f.read_text(errors="replace"))
                docs.append({"name": f.name, "wiki_id": meta.get("wiki_id"), "article": meta.get("article")})
            return self._json({"count": len(docs), "documents": docs})

        if path == "/api/kb":
            docs = []
            for f in sorted(KB_ROOT.glob("*.md")) if KB_ROOT.exists() else []:
                docs.append({"name": f.name, "size": f.stat().st_size})
            return self._json({"count": len(docs), "documents": docs})

        if path == "/api/resolve":
            citation = q.get("citation", [""])[0]
            if not citation:
                return self._json({"error": "Missing citation"}, 400)
            index = _load_index_entries()
            r = _resolve_citation(citation, index)
            if not r:
                return self._json({"citation": citation, "found": False})
            e = r["entry"]
            return self._json({
                "citation": citation, "found": True,
                "stable_id": e.get("stable_id"), "article": e.get("article"),
                "title": e.get("title"), "body_preview": e.get("body", "")[:600]
            })

        if path == "/api/audit":
            doc_path = q.get("path", [""])[0]
            if not doc_path:
                return self._json({"error": "Missing path"}, 400)
            result = audit_document(doc_path)
            return self._json(result)

        if path == "/api/search":
            query = q.get("q", [""])[0]
            if not query:
                return self._json({"error": "Missing q"}, 400)
            keywords = [k for k in query.strip().split() if k]
            docs = _walk_kb()
            matches = []
            for doc in docs:
                if len(matches) >= 20:
                    break
                snippet = _search_in_file(Path(doc["absolute"]), keywords)
                if snippet:
                    matches.append({"path": doc["path"], "layer": doc["layer"], "snippet": snippet})
            return self._json({"query": query, "match_count": len(matches), "matches": matches})

        if path == "/api/retrieve":
            query = q.get("q", [""])[0]
            if not query:
                return self._json({"error": "Missing q"}, 400)
            try:
                depth = int(q.get("depth", ["1"])[0])
            except ValueError:
                depth = 1
            try:
                max_results = min(int(q.get("max_results", ["5"])[0]), 20)
            except ValueError:
                max_results = 5

            # Query result cache lookup (TTL 120s, max 500)
            cache_key = f"{query}|{depth}|{max_results}"
            cached = _retrieve_cache.get(cache_key)
            if cached and (time.time() * 1000) < cached["expires_at"]:
                return self._json(cached["data"])

            results: list = []
            seen_paths: set = set()

            # --- depth=0: citation / keyword lookup in Index ---
            if depth >= 0:
                index = _load_index_entries()
                query_lower = query.lower()
                import re as _re
                tokens = set(_re.findall(r"[a-z0-9]+", query_lower)) or {query_lower}
                for sid, entry in index.items():
                    text_all = (entry.get("title", "") + " " + entry.get("body", "")).lower()
                    if query_lower in sid.lower() or all(t in text_all for t in tokens):
                        results.append({
                            "layer": "index",
                            "document": f"EHDS-Index-{entry.get('article', '?')}",
                            "section": entry.get("title", ""),
                            "stable_id": sid,
                            "text": entry.get("body", "")[:800],
                            "source_path": entry.get("filename", ""),
                        })

            # --- depth>=1: TF-IDF semantic search ---
            if depth >= 1:
                try:
                    engine = _get_embedding_engine()
                    semantic = engine.semantic_search(query, top_k=max_results)
                    kg_path = PROJECT_ROOT
                    for sr in semantic:
                        sp = sr.get("source_path", "")
                        if sp in seen_paths:
                            continue
                        seen_paths.add(sp)
                        # Read full file body for rich context
                        try:
                            full_path = kg_path / sp
                            full_text = full_path.read_text(encoding="utf-8", errors="replace")
                            _, body = _parse_frontmatter(full_text)
                        except Exception:
                            body = sr.get("text", "")
                        meta = sr.get("metadata", {})
                        results.append({
                            "layer": sr.get("layer", ""),
                            "document": f"EHDS-{sr.get('layer', 'kg').title()}",
                            "section": meta.get("title", sp),
                            "similarity": sr.get("similarity"),
                            "text": body.strip()[:800],
                            "source_path": sp,
                            "article": meta.get("article", ""),
                        })
                except Exception as e:
                    pass  # TF-IDF unavailable — omit gracefully

            # --- depth>=2: audit rules check ---
            if depth >= 2:
                try:
                    audit_result = audit_document(query)
                    for v in audit_result.get("violations", [])[:max_results]:
                        results.append({
                            "layer": "audit",
                            "document": "EHDS-Audit",
                            "section": f"[{v.get('severity', '?').upper()}] {v.get('rule_id', '')}",
                            "rule_id": v.get("rule_id"),
                            "severity": v.get("severity"),
                            "text": f"{v.get('description', '')}\n{v.get('remediation', '')}",
                            "source_path": audit_result.get("document", ""),
                        })
                except Exception:
                    pass

            data = {
                "query": query,
                "depth": depth,
                "result_count": len(results[:max_results]),
                "results": results[:max_results],
            }
            # Cache the result (TTL 120s, LRU max 500)
            _retrieve_cache[cache_key] = {"data": data, "expires_at": time.time() * 1000 + _RETRIEVE_CACHE_TTL}
            if len(_retrieve_cache) > _RETRIEVE_CACHE_MAX:
                oldest_k = next(iter(_retrieve_cache))
                del _retrieve_cache[oldest_k]
            return self._json(data)

        return self._json({"error": "Not found"}, 404)


if __name__ == "__main__":
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"[+] EHDS API Gateway on http://localhost:{PORT}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutdown")
        srv.shutdown()
