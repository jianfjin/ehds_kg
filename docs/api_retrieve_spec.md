# /api/retrieve — API Contract

**Version:** 1.0
**Server:** ehds_kg API (Python `http.server`, port 8080)
**Consumer:** edm_home LLM prompt injector

## Design Philosophy

One endpoint. Three depths. The response has exactly two things the consumer needs:
a `context_text` string ready to inject into any LLM prompt, and a `sources`
array so the LLM can cite its answers. Nothing else.

---

## Request

```
GET /api/retrieve?q=<query>&depth=<0|1|2>&max_results=<int>
```

### Parameters

| Param        | Required | Type    | Default | Description                                           |
|-------------|----------|---------|---------|-------------------------------------------------------|
| `q`         | yes      | string  | —       | Natural-language query (URL-encoded).                 |
| `depth`     | no       | int     | 1       | Retrieval depth: 0=index, 1=+wiki TF-IDF, 2=+KB audit.|
| `max_results`| no      | int     | 5       | Max sources returned. Clamped to 1–20.                |

### Depth Behavior

| Depth | Layers Searched                               | Method                              |
|-------|-----------------------------------------------|-------------------------------------|
| 0     | Index only (legal articles)                   | Citation resolution + title/body substring match. |
| 1     | Index + Wiki (semantic)                       | TF-IDF cosine similarity across all chunks.       |
| 2     | Index + Wiki + KB audit                       | Depth 1 results + per-document compliance audit.  |

### Examples

```
GET /api/retrieve?q=HDAB+approval+requirements
GET /api/retrieve?q=data+linkage&depth=2&max_results=3
GET /api/retrieve?q=Art.+54+penalties&depth=0
```

---

## Response

### Success (200)

```json
{
  "query": "data linkage approval",
  "depth": 1,
  "max_results": 5,
  "result_count": 3,
  "context_text": "## EHDS Knowledge Graph Results\n\n### [wiki] Data Linkage in EHDS\nData linkage is the process of combining datasets from multiple sources...\n\n### [index] EHDS-2025-327-A68 — Art. 68\n1. Health data access bodies shall provide access to electronic health data...\n\n### [wiki] DAAMS Application System\nThe Data Access Application Management System (DAAMS) is...",
  "sources": [
    {
      "rank": 1,
      "similarity": 0.8456,
      "document": "Data_Linkage.md",
      "section": "Data Linkage in EHDS",
      "parent_id": null,
      "child_id": null,
      "text": "Data linkage is the process of combining datasets from multiple sources to create a richer, linked dataset. Under EHDS, data linkage is a pre-access, centralized process managed by HDAB...",
      "source_path": "ehds_wiki/Data_Linkage.md",
      "layer": "wiki"
    },
    {
      "rank": 2,
      "similarity": 0.7201,
      "document": "EHDS-2025-327_Art-68.md",
      "section": "Art. 68 — Data linkage governance",
      "parent_id": "EHDS-2025-327-A68",
      "child_id": "EHDS-2025-327-A68-P2",
      "text": "1. Health data access bodies shall provide access to electronic health data only where the requested processing is necessary for one of the following purposes...",
      "source_path": "ehds_index/EHDS-2025-327_Art-68.md",
      "layer": "index"
    }
  ],
  "audit": null
}
```

### Source Object Fields

| Field        | Type         | Description                                                |
|-------------|-------------|------------------------------------------------------------|
| `rank`       | int         | 1-based result rank.                                       |
| `similarity` | float|null | TF-IDF cosine similarity (0–1). Null for depth=0.          |
| `document`   | string      | Human-readable filename.                                   |
| `section`    | string      | Heading or title of the matched section.                   |
| `parent_id`  | string|null| Index stable_id (e.g. `EHDS-2025-327-A68`). Null for wiki. |
| `child_id`   | string|null| Index paragraph anchor (e.g. `EHDS-2025-327-A68-P2`).      |
| `text`       | string      | Full matched paragraph/chunk text (not truncated).         |
| `source_path`| string      | Relative path from project root.                           |
| `layer`      | string      | `index`, `wiki`, or `kb`.                                  |

### Audit Object (depth=2 only)

When `depth=2`, each source that maps to a KB-root document gets audited.
The `audit` field is an object keyed by `source_path`:

```json
"audit": {
  "ehds_wiki/Data_Linkage.md": {
    "severity_summary": {"critical": 0, "high": 1, "medium": 1, "low": 0},
    "violations": [
      {
        "rule_id": "EHDS-SEC-LINK-001",
        "severity": "critical",
        "violation_type": "missing",
        "description": "Missing data linkage governance: no HDAB pre-access approval reference (Art.68)",
        "remediation": "Add explicit reference to: data linkage, record linkage"
      }
    ]
  }
}
```

If no KB-auditable documents matched, `audit` is `null`.

---

## Error Responses

### Missing Query (400)

```json
{
  "error": "Missing required parameter: q",
  "hint": "GET /api/retrieve?q=your+query"
}
```

### Empty Results (200 — not an error)

```json
{
  "query": "xyzzy foobar blarg",
  "depth": 1,
  "max_results": 5,
  "result_count": 0,
  "context_text": "No relevant documents found for: xyzzy foobar blarg",
  "sources": [],
  "audit": null
}
```

### Engine Unavailable (503)

When the TF-IDF index hasn't been built yet (no `ehds_tfidf.pkl`):

```json
{
  "error": "Search engine not initialized",
  "hint": "POST to /api/rebuild to build the TF-IDF index, then retry."
}
```

### Invalid Depth (200 — forgiven)

Out-of-range depth values are silently clamped:
- `<0` → `0`
- `>2` → `2`

### Max Results Clamping

- `<1` → `1`
- `>20` → `20`

---

## Consumer Integration (edm_home)

edm_home calls this endpoint and injects `context_text` directly into its
LLM system prompt or as a RAG context block. The `sources` array drives
citations in the LLM response.

```
# edm_home pseudocode
resp = fetch(f"http://localhost:8080/api/retrieve?q={encode(user_query)}&depth=1")
data = resp.json()

system_prompt = f"""You are an EHDS compliance assistant.
Use the following retrieved knowledge to answer the user's question.
Cite sources using [source_path].

{data['context_text']}
"""
```

The LLM can reference `source_path` values (e.g., `ehds_wiki/Data_Linkage.md`)
which edm_home resolves to URLs or MCP citations as needed.

---

## What This Endpoint Does NOT Do

- No streaming. The response fits in memory (max 20 sources × ~2KB = 40KB).
- No pagination. If you need more, increase `max_results`.
- No filters beyond depth. `layer` filtering is implicit in depth.
- No authentication. This is a localhost service.
- No caching headers. The consumer is expected to call it fresh per query.
