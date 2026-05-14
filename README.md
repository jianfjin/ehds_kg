# EHDS Knowledge Graph (EHDS-KG)

Neuro-Symbolic Compliance Knowledge Base for the European Health Data Space (EHDS) Regulation.

Migrated from Hermes Agent's Paperclip project to standalone project.

## Directory Structure

```
ehds_kg/
├── README.md
├── THREE_LAYER_ARCHITECTURE.md   # Architecture documentation
├── ehds_index/                   # Layer 1: Authoritative legal text (36 Articles)
├── ehds_wiki/                    # Layer 2: Semantic associations (7 entries)
├── ehds_kb/                      # Layer 3: Machine-actionable rules (2 rules)
├── src/                          # Python toolchain
│   ├── ehds_common.py            # Shared utilities (parsers, resolvers, audit engine)
│   ├── ehds_embedding.py         # TF-IDF semantic search engine
│   ├── ehds_api_server.py        # HTTP REST API gateway (port 8080)
│   ├── batch_import.py           # Bulk Article importer
│   ├── ehds_tfidf.py            # Lightweight TF-IDF (standalone)
│   └── __init__.py
├── scripts/
│   ├── test_e2e.py               # End-to-end validation suite
│   └── verify-semantic-search.py # Pipeline health check
├── data/source_pdfs/             # Source regulation PDFs
├── cache/                        # TF-IDF index and embeddings DB
├── dashboard/                    # HTML dashboards
└── docs/                         # Compliance prompts, architecture docs, logs
```

## Quick Start

```bash
cd ~/projects/ehds_kg

# Validate the stack
python3 scripts/test_e2e.py

# Build TF-IDF index
python3 src/ehds_embedding.py --build

# Search
python3 src/ehds_embedding.py --search "HDAB approval requirements"

# Start API server
python3 src/ehds_api_server.py
# Then open http://localhost:8080/
```

## Three Layers

| Layer | Directory | Purpose | Files |
|-------|-----------|---------|-------|
| Index | `ehds_index/` | Raw regulation text, one file per Article | 36 |
| Wiki  | `ehds_wiki/` | Semantic context, cross-references, MOCs | 7 |
| KB    | `ehds_kb/` | Machine-actionable audit rules | 2 |

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | HTML dashboard |
| `GET /api/health` | Service health |
| `GET /api/stack` | Layer counts |
| `GET /api/index` | List Index documents |
| `GET /api/wiki` | List Wiki documents |
| `GET /api/kb` | List KB documents |
| `GET /api/resolve?citation=Art.54(2)` | Citation resolver |
| `GET /api/audit?path=...` | Compliance audit |
| `GET /api/search?q=...` | Full-text search |

## Citation Formats Supported

| Format | Example | Resolves To |
|--------|---------|-------------|
| Stable ID | `EHDS-2025-327-A54` | Full Article 54 |
| Stable ID + Anchor | `EHDS-2025-327-A54-P2` | Paragraph 2 of Art. 54 |
| Article ref | `Art. 54` | Article 54 |
| Article + Paragraph | `Art. 54(2)` | Paragraph 2 of Art. 54 |
| Full legal cite | `Reg. (EU) 2025/327, Art. 54(2)` | Paragraph 2 of Art. 54 |
