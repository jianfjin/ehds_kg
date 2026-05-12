---
wiki_id: "WIKI-DL-001"
title: "Data Linkage in EHDS"
regulation: "Reg. (EU) 2025/327"
article: "66, 68"
category: "secondary_use"
keywords: ["data linkage", "record linkage", "dataset combination", "HDAB pre-access", "data permit", "SPE", "Article 68", "TEHDAS2"]
index_refs: ["EHDS-2025-327-A66", "EHDS-2025-327-A68", "EHDS-2025-327-A54", "EHDS-2025-327-A44", "EHDS-2025-327-A39"]
anchors: ["A66-P1", "A68-P1b"]
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-guideline-for-data-enrichment.pdf"]
---

# Data Linkage in EHDS

## Definition (ISO 5127:2017)

> Data linkage is the process of combining datasets "from several sources on one topic or data subject" using unique identifiers, probabilistic methods, or a combination of techniques.

Source: TEHDAS2 M5.4 Draft Guideline for Data Enrichment, Glossary (p.47)

## Data Linkage vs. Data Enrichment

This is a critical distinction within the EHDS secondary use workflow:

| Aspect | Data Linkage | Data Enrichment |
|--------|-------------|-----------------|
| **Timing** | Pre-access (before user gets data) | Post-access (after data permit issued) |
| **Who performs** | HDAB or data holder | Authorised data user within SPE |
| **Nature** | Centralised, regulated, formal | User-driven, analytical, optional |
| **Legal basis** | Article 68(1)(b) — must be explicitly requested in data access application | No mandatory obligation; Member State discretion |
| **Scope** | Record-level matching across datasets | Adding derived variables or contextual attributes |
| **Governance** | Subject to regulatory assessment, data minimisation checks | Governed by data permit terms |

## EHDS Workflow

```
APPLICATION (Art.68)
  └─ User requests datasets + data linkage (Art.68(1)(b))
       │
       ▼
HDAB ASSESSMENT
  └─ Legal/ethical/technical review
  └─ Data minimisation check (Art.66(1): "adequate, relevant and limited")
       │
       ▼
DATA PERMIT ISSUED
  └─ Specifies datasets, operations, restrictions
       │
       ▼
DATA LINKAGE (pre-access, HDAB-managed)
  └─ Person-level matching across datasets
  └─ Only the final linked dataset is provided to user
       │
       ▼
SPE ACCESS (post-access, user-driven)
  └─ Data preparation, analysis, enrichment
  └─ Results export (aggregated/anonymised)
```

## Example of Data Linkage

A research team applies to an HDAB requesting to link:
- **Electronic health records** (category a) with
- **National mortality register** (category l)

The HDAB or data holder performs the record-level linkage and provides the researcher with the resulting combined dataset. The user never sees the unlinked raw records.

## Example of Data Enrichment (NOT linkage)

A researcher with an approved dataset:
- Appends **area-level deprivation scores** from publicly available data
- Calculates **risk scores** from existing clinical measurements within the same dataset
- These are user-driven operations within the SPE, under existing data permit

## Key EHDS Articles

- **Art. 68(1)(b)** — Data access application must specify any intended data linkage
- **Art. 66(1)** — Only "adequate, relevant and limited" data may be provided (data minimisation)
- **Art. 54** — Secondary use for scientific research (where linkage is most common)
- **Art. 44** — Security of processing, including pseudonymisation (precondition for safe linkage)
- **Art. 39** — Cross-border data exchange (linkage across Member States)

## Forthcoming Guidance

The TEHDAS2 consortium is developing a dedicated **"Guideline for Health Data Access Bodies on Linkage of Health Datasets"** (consultation wave 3, May 2026). This will provide operational and governance details beyond the enrichment guideline.

## Pitfall: Enrichment That Becomes Linkage

> "Where external enrichment involves record-level matching or joining across datasets to create person-level connections, it should be treated as **data linkage** for governance purposes unless national rules explicitly provide otherwise."

Source: TEHDAS2 M5.4, Section 4.2.1 (p.19)

Bottom line: if you're joining person-level records from two different data permit sources, you're doing linkage — not enrichment — and need explicit HDAB approval under Article 68(1)(b).
