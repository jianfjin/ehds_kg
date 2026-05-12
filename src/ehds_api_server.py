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
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

from ehds_common import (
    PROJECT_ROOT, INDEX_ROOT, WIKI_ROOT, KB_ROOT, DOCS_ROOT,
    _parse_frontmatter, _load_index_entries, _resolve_citation,
    _resolve_kb_path, _walk_kb, _search_in_file, _read_text_file,
    _read_pdf_file, audit_document,
)

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

        return self._json({"error": "Not found"}, 404)


if __name__ == "__main__":
    srv = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"[+] EHDS API Gateway on http://localhost:{PORT}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutdown")
        srv.shutdown()
