---
document_id: "PAPERCLIP-ARCH-001"
title: "EHDS Neuro-Symbolic Storage Fabric — Three-Layer Knowledge Stack"
version: "1.0.0"
author: "CTO-FengGe"
date: "2026-05-11"
regulation: "Reg. (EU) 2025/327"
---

# EHDS Neuro-Symbolic Storage Fabric
## Three-Layer Knowledge Stack Architecture

> "From black-box rejection to forensically-citable compliance auditing."
> — CTO 峰哥 (He Mi Si), Paperclip Project

---

## 1. Executive Summary

This document defines the **Three-Layer Knowledge Stack** for the Paperclip project's EHDS (European Health Data Space) compliance auditing system. The architecture transforms opaque regulatory text into a **neuro-symbolic storage fabric** that enables:

- **Forensic traceability**: Every audit finding cites exact legal coordinates (Regulation + Article + Paragraph)
- **Machine-actionable rules**: Structured YAML frontmatter and anchor IDs enable automated rule engines
- **Cross-agent interoperability**: MCP (Model Context Protocol) exposes the entire stack to Claude, Cursor, Codex, LangChain, and Agno

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                 AUDIT CLIENT (Claude / Cursor / Agno)                  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▵  MCP (stdio)
                                    │
┌─────────────────────────────────────────────────────────────────┐
│          EHDS MCP SERVER (ehds_mcp_server.py)                           │
│  ─────────────────────────────────────────────────────────  │
│   Tools: list_documents │ read_document │ search_kb │ resolve_citation │ audit_document │
└─────────────────────────────────────────────────────────────────┘
                                    │
              ┌───────────┬───────────┬───────────┐
              │  INDEX   │   WIKI    │    KB     │
              │  LAYER   │   LAYER   │   LAYER   │
              └───────────┴───────────┴───────────┘
```

### 2.1 Layer Definitions

| Layer | Directory | Purpose | Human vs Machine |
|-------|-----------|---------|------------------|
| **Index** | `ehds_index/` | Authoritative legal text with **stable IDs** and **Markdown anchors** per paragraph | Human-readable primary source |
| **Wiki** | `ehds_wiki/` | Semantic associations, context, and cross-references with **YAML Frontmatter** | Human-readable + machine-parseable |
| **KB** | `ehds_kb/` | Machine-actionable rules, heuristics, and prompt templates | Machine-optimized |

---

## 3. Layer 1: Index (Authoritative Legal Text)

### 3.1 Design Principles

- **One file per Article**: Each EHDS Article gets its own markdown file
- **Stable IDs never change**: `EHDS-2025-327-A54` is immutable, even if the file moves
- **Paragraph anchors**: Every paragraph gets an anchor ID like `A54-P2` for precise citation
- **No interpretation**: Index layer contains **only** the regulation text, no commentary

### 3.2 File Naming Convention

```
EHDS-{YYYY}-{NNN}_Art-{AAA}.md

Example: EHDS-2025-327_Art-054.md
```

### 3.3 Frontmatter Schema (Index)

```yaml
---
regulation: "Reg. (EU) 2025/327"
article: 54
title: "Permitted purposes for secondary use — scientific research"
chapter: "V"
stable_id: "EHDS-2025-327-A54"
category: "secondary_use"
date_enacted: "2025-03-11"
---
```

### 3.4 Body Structure

```markdown
# Art. 54 — Permitted purposes for secondary use: scientific research

## Para 1
Electronic health data may be processed for the purpose of scientific research...

## Para 2
The processing ... shall be subject to prior authorisation by the health data access body...

## Audit Anchors
- [[A54-P1]] :: scientific-research-definition / Annex-II-areas
- [[A54-P2]] :: HDAB-authorisation-required / anonymous-exemption
```

### 3.5 Citation Resolution

The MCP server supports multiple citation formats:

| Format | Example | Resolves To |
|--------|---------|-------------|
| Stable ID | `EHDS-2025-327-A54` | Full Article 54 text |
| Stable ID + Anchor | `EHDS-2025-327-A54-P2` | Paragraph 2 of Article 54 |
| Article reference | `Art. 54` | Article 54 |
| Article + Paragraph | `Art. 54(2)` | Paragraph 2 of Article 54 |
| Full legal citation | `Reg. (EU) 2025/327, Art. 54(2)` | Paragraph 2 of Article 54 |

---

## 4. Layer 2: Wiki (Semantic Associations)

### 4.1 Design Principles

- **Frontmatter-enriched**: Every wiki file carries YAML metadata for machine parsing
- **Bi-directional linking**: `[[WikiLink]]` syntax maintains semantic graph
- **Index citations**: Every claim references the authoritative Index layer
- **Audit context**: Human-readable explanations of *why* an article matters

### 4.2 Frontmatter Schema (Wiki)

```yaml
---
wiki_id: "WIKI-SEC-001"
title: "Secondary Use of Health Data"
regulation: "Reg. (EU) 2025/327"
article: 54
category: "secondary_use"
keywords: ["scientific research", "HDAB approval", "public health", "data reuse", "Annex II"]
index_refs: ["EHDS-2025-327-A54", "EHDS-2025-327-A55", "EHDS-2025-327-A33"]
anchors: ["A54-P1", "A54-P2", "A54-P3", "A54-P4", "A33-P4"]
created: "2026-05-08"
updated: "2026-05-11"
author: "CTO-FengGe"
---
```

### 4.3 Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `wiki_id` | string | Unique wiki identifier (e.g. `WIKI-SEC-001`) |
| `title` | string | Human-readable title |
| `regulation` | string | Source regulation citation |
| `article` | integer | Primary article number |
| `category` | string | Taxonomic category |
| `keywords` | list | Searchable tags |
| `index_refs` | list | Stable IDs of referenced Index entries |
| `anchors` | list | Specific paragraph anchors referenced |
| `created` | date | Creation date |
| `updated` | date | Last modification date |
| `author` | string | Responsible party |

---

## 5. Layer 3: KB (Machine-Actionable Rules)

### 5.1 Design Principles

- **Prompt templates**: LLM-optimized prompts for compliance checking
- **Heuristic rules**: Regex-based and keyword-based violation detectors
- **Output schemas**: JSON-LD templates for structured audit reports

### 5.2 Example KB File

See existing files:
- `ehds_kb/secondary_use_rules.md`
- `ehds_kb/buzzword_optimizer.md`

---

## 6. MCP Tool Reference

### 6.1 `audit_document`

Performs a structured compliance audit on any document (PDF or Markdown) in the KB roots.

**Input:**
```json
{
  "document_path": "drive_ehds_docs_r2/draft-guideline.pdf",
  "purpose_tags": ["scientific_research", "cross_border"]
}
```

**Output (JSON-LD):**
```json
{
  "@context": "https://schema.org",
  "@type": "AuditReport",
  "audit_status": "completed",
  "document": "drive_ehds_docs_r2/draft-guideline.pdf",
  "extraction_method": "pymupdf",
  "purpose_tags": ["scientific_research", "cross_border"],
  "severity_summary": {"critical": 1, "high": 2, "medium": 1, "low": 0},
  "violation_count": 4,
  "violations": [
    {
      "rule_id": "EHDS-SEC-AUTH-001",
      "ehds_citation": "EHDS Reg. (EU) 2025/327, Art. 54(2)",
      "violation_type": "missing",
      "severity": "critical",
      "description": "Document fails to mention Health Data Access Body (HDAB) authorisation...",
      "location": {
        "page": null,
        "bbox": null,
        "line_estimate": 0,
        "extraction_method": "pymupdf"
      },
      "remediation": "Add explicit HDAB authorisation requirement and reference the responsible national HDAB entity."
    }
  ],
  "recommendation": "CRITICAL: Document is non-compliant and likely to be rejected by HDAB."
}
```

### 6.2 `resolve_citation`

Resolves any EHDS citation to authoritative text from the Index layer.

**Supported formats:**
- `EHDS-2025-327-A54`
- `EHDS-2025-327-A54-P2`
- `Art. 54`
- `Art. 54(2)`
- `Reg. (EU) 2025/327, Art. 54(2)`

### 6.3 `search_kb`

Full-text AND search across all three layers.

### 6.4 `list_documents` / `read_document`

Browse and read any file in the KB roots.

---

## 7. Migration & Deployment

### 7.1 Backup (Old Machine)

```bash
cd ~/migration_tools
./pack.sh
```

Includes:
- `ehds_index/` — Authoritative legal text
- `ehds_wiki/` — Semantic associations
- `ehds_kb/` — Machine rules
- `ehds_audit/` — Architecture documentation
- MCP server script

### 7.2 Restore (New Machine)

```bash
cd ~/migration_backup
./awakening.sh
```

Auto-generates MCP client configuration at `~/.hermes/mcp_ehds_config.json`.

### 7.3 MCP Client Setup

**Claude Desktop:**
```bash
cat ~/.hermes/mcp_ehds_config.json >> ~/.config/Claude/claude_desktop_config.json
```

**Cursor:**
```bash
cat ~/.hermes/mcp_ehds_config.json >> ~/.cursor/mcp.json
```

---

## 8. Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-10 | **Do NOT rebuild Wiki** | `[[WikiLink]]` semantic graph has irreplaceable associative value |
| 2026-05-10 | **Add `ehds_index/` layer** | Need authoritative text with stable IDs for forensic citation |
| 2026-05-10 | **Frontmatter + Anchors** | Enables both human readability and machine parsing |
| 2026-05-10 | **Three-layer stack** | Separation of concerns: Authority → Semantics → Action |
| 2026-05-10 | **MCP exposure** | Cross-agent interoperability (Claude, Cursor, Codex, Agno) |
| 2026-05-11 | **LLM Reasoning Layer** | Added neuro-symbolic audit engine: keyword pre-filter → semantic search (TF-IDF) → LLM cross-layer reasoning (Index→Wiki→KB). Falls back to keyword-only when LLM unavailable. |

---

## 9. Glossary

| Term | Definition |
|------|------------|
| **EHDS** | European Health Data Space (Reg. (EU) 2025/327) |
| **HDAB** | Health Data Access Body (national authority per Art. 59) |
| **MCP** | Model Context Protocol (stdio-based tool exposure) |
| **Stable ID** | Immutable identifier (e.g. `EHDS-2025-327-A54`) |
| **Anchor** | Paragraph-level reference (e.g. `A54-P2`) |
| **Frontmatter** | YAML metadata block at top of Markdown files |

---

*Document version 1.0.0 — Paperclip Project — CTO 峰哥*
