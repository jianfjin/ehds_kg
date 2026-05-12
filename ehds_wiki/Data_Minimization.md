---
wiki_id: "WIKI-DM-001"
title: "Data Minimisation Principle"
regulation: "Reg. (EU) 2025/327"
article: "33, 66, 68"
category: "principles"
keywords: ["data minimisation", "proportionality", "necessary data", "GDPR Article 5", "five dimensions", "quasi-identifiers", "generalisation", "suppression", "randomisation", "Who What When Where How"]
index_refs: ["EHDS-2025-327-A33", "EHDS-2025-327-A5", "EHDS-2025-327-A66", "EHDS-2025-327-A68"]
anchors: ["A33-P2", "A33-P6", "A66-P3", "A68-P1c"]
created: "2026-05-08"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-guideline-on-data-minimisation-pseudonymisation-anonymisation-and-synthetic-data.pdf"]
---

# Data_Minimization

Data minimisation is a fundamental GDPR principle requiring that only data necessary for the specific purpose are processed. Under the EHDS, it applies throughout the entire data lifecycle — from collection to export of results from the SPE.

## Index Citations
- Art. 33(2)(a): "the principle of proportionality, ensuring that only data necessary for the specific purpose are processed"
- Art. 33(2)(e): "the principle of data minimisation, limiting the processing to what is adequate, relevant and necessary"
- Art. 66(3): all categories of data processed must be subject to appropriate minimisation, pseudonymisation or anonymisation measures

## Five Dimensions of Data Minimisation (TEHDAS2 M7.2 Framework)

The TEHDAS2 guideline introduces a practical framework for scoping data provision across five dimensions:

1. **Who** — Study Population
   - Define inclusion/exclusion criteria explicitly.
   - Avoid strong quasi-identifiers: date of birth, date of death.
   - Replace with year of birth, age groups, age at death where possible.
   - Group extreme age values (e.g., 0-5 and 85+).
   - Sensitive demographics (ethnicity, health status) require additional legal/ethical assessment under Art. 9(1) GDPR.
   - Avoid combinations like "date of birth + sex + postcode" — these dramatically increase re-identification risk.

2. **What** — Research Variables
   - Distinguish between study-specific variables (answer research questions) and control/confounding variables (enhance validity).
   - Genetic data and rare disease codes act as quasi-identifiers — require special safeguards.
   - Medical images may reveal unique body features and can act as direct/quasi-identifiers.
   - Unstructured text data is particularly hard to de-identify — may contain excess background information.

3. **When** — Timeframe
   - Specify calendar periods or relative timeframes aligned with study objectives.
   - Prefer year/month granularity over exact dates when sufficient.
   - Hospital admission/discharge dates are sensitive quasi-identifiers.

4. **Where** — Geographical Perimeter
   - Limit to locations relevant for study purposes.
   - Geographical data combined with other variables increases re-identification risk.

5. **How** — Extraction Methods
   - Define sampling strategies and data transformation approaches.
   - Consider pre-defined granularity levels offered by data holders.

## Risk Mitigation Techniques

- **Generalisation**: Reduce detail level (age brackets instead of exact age; income ranges; grouped location codes).
- **Suppression**: Remove/hide specific values (extreme lab values; small cell counts in aggregated data).
- **Randomisation**: Add calibrated noise (primarily for anonymisation; may significantly reduce data utility).

## Lifecycle Application

Data minimisation applies to all actors and phases:
- **Data Holder**: During initial collection and preparation.
- **HDAB**: When assessing data access applications/data requests (pre-permit) and during data preparation before SPE upload.
- **Data User**: During analysis in SPE and when requesting result exports.
- **HDAB (finalisation)**: Risk assessment before approving SPE result export.

## Role in Risk Mitigation

Data minimisation indirectly supports the GDPR triad:
- Confidentiality (reducing exposure to unauthorised access)
- Integrity (reducing surface for unauthorised alterations)
- Availability (limiting scope of data not accessible to authorised parties)

It also forms part of the broader risk mitigation strategy alongside pseudonymisation, anonymisation, and organisational safeguards, and supports protection of intellectual property and trade secrets (Art. 52 EHDS).

## Related
[[Pseudonymisation_Anonymisation]] [[Article_SecondaryUse]] [[Purpose_Scientific]] [[Data_Holder_Obligations]]
