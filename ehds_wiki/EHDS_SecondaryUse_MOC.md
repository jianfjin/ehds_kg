---
wiki_id: "WIKI-MOC-001"
title: "EHDS Secondary Use Map of Content"
regulation: "Reg. (EU) 2025/327"
article: "33-68"
category: "moc"
keywords: ["secondary use", "map of content", "knowledge graph", "audit trail", "data linkage"]
index_refs: ["EHDS-2025-327-A33", "EHDS-2025-327-A54", "EHDS-2025-327-A55", "EHDS-2025-327-A59", "EHDS-2025-327-A60", "EHDS-2025-327-A66", "EHDS-2025-327-A67", "EHDS-2025-327-A68", "EHDS-2025-327-A71"]
anchors: ["A33-P2", "A33-P3", "A33-P4", "A33-P5", "A33-P6", "A54-P1", "A54-P2", "A54-P3", "A54-P4", "A59-P1", "A59-P2", "A59-P3", "A60-P1", "A66-P4", "A67-P1", "A68-P1b", "A71-P1", "A71-P2", "A71-P4"]
created: "2026-05-08"
updated: "2026-05-12"
author: "CTO-FengGe"
---

# EHDS_SecondaryUse_MOC

Map of Content for EHDS Secondary Use compliance auditing.

## Core Principles
- [[Data_Minimization]] → Art. 33(2)(a)(e), Art. 66(3) :: proportionality & minimisation, five-dimension framework
- [[Pseudonymisation_Anonymisation]] → Art. 66(3), Art. 67, Art. 68(1)(c) :: pseudonymisation, anonymisation, synthetic data, re-identification risk
- [[Data_Linkage]] → Art. 68(1)(b) :: record-level dataset combination, HDAB-managed

## Data Subject Rights
- [[Opt_Out_Mechanism]] → Art. 71 :: unconditional, reversible, no justification, opt-out registry, granularity, Art. 71(4) exceptions
- [[Significant_Findings_Notification]] → Art. 58(3)(4), Art. 61(5) :: 4-step notification chain, clinical significance, right not to be informed

## Data Holder Obligations
- [[Data_Holder_Obligations]] → Art. 60, Art. 63 :: personal vs non-personal data provision, 3-month timeline, trusted data holders, intermediation entities

## Governance
- [[HDAB_Approval]] → Art. 59 :: independent body, authorisation, refusal grounds
- [[Data_Linkage]] → Art. 68 :: data access application, linkage request workflow

## Permitted Purposes
- [[Purpose_Scientific]] → Art. 54 :: research ethics, Annex II, HDAB auth
- [[Article_SecondaryUse]] → Art. 54-55 :: general secondary use framework

## Cross-Border
- [[International_Transfer]] → Chapter V safeguards, anonymous exemption

## Enforcement
- [[Violation_Fine]] → Art. 66 :: penalties, fines, bans

## Knowledge Stack
| Layer | Path | Purpose |
|-------|------|---------|
| Index | `ehds_index/` | Authoritative legal text with stable IDs |
| Wiki | `ehds_wiki/` | Semantic associations & audit context |
| KB | `ehds_kb/` | Machine-actionable rules & heuristics |
