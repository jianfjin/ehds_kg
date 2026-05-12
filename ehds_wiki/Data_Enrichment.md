---
wiki_id: "WIKI-DE-001"
title: "Data Enrichment in EHDS"
regulation: "Reg. (EU) 2025/327"
article: "51, 73"
category: "secondary_use"
keywords: ["data enrichment", "internal enrichment", "external enrichment", "data quality feedback loop", "SPE", "user-driven", "Recital 57", "TEHDAS2"]
index_refs: ["EHDS-2025-327-A51", "EHDS-2025-327-A54"]
anchors: []
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-guideline-for-data-enrichment.pdf"]
---

# Data Enrichment in EHDS

## Overview

Data enrichment is an **optional, user-driven, and value-based activity** that may occur during secondary use of health data within a Secure Processing Environment (SPE). The EHDS Regulation does not establish data enrichment as a mandatory compliance requirement, nor does it prescribe uniform governance models. Instead, it leaves Member States discretion to decide whether and how such activities are addressed in national frameworks (Article 51(3)).

The concept is introduced in **Recital 57** of Regulation (EU) 2025/327, which envisions the possibility for health data users to enhance the datasets they access through corrections, annotations, or other improvements — for instance by supplementing missing or incomplete data to increase accuracy, completeness, or quality.

> **Important**: Data enrichment is NOT data linkage. For the distinction, see [[Data_Linkage]].

## What Data Enrichment Is

Data enrichment refers to the process of enhancing an existing dataset by adding new information, context, or derived value to increase its analytical usefulness. It goes beyond preparing data for analysis (cleaning, structuring) and instead aims to expand the informational content of the dataset.

### Key Distinctions

| Aspect | Data Enrichment | Data Linkage |
|--------|----------------|--------------|
| **Timing** | Post-access (after data permit issued) | Pre-access (before user gets data) |
| **Who performs** | Authorised data user within SPE | HDAB or data holder |
| **Nature** | User-driven, analytical, optional | Centralised, regulated, formal |
| **Legal basis** | No mandatory obligation; Member State discretion | Article 68(1)(b) — must be explicitly requested |
| **Governance** | Governed by data permit terms | Subject to regulatory assessment and data minimisation checks |

## Internal vs. External Enrichment

### Internal Enrichment
Deriving new information exclusively from the dataset itself, without incorporating external sources:

- **Feature derivation**: Calculating risk scores from clinical measurements
- **Temporal aggregation**: Summarizing time-series data into episode-level summaries
- **Semantic tagging**: Applying standardised clinical codes or ontologies
- **Longitudinal transformations**: Time from diagnosis to treatment, follow-up periods, sequence of interventions
- **Image segmentation**: Annotating tumour regions in CT scans

### External Enrichment
Adding authorised information from other datasets available to the user in the SPE:

- **Contextual augmentation**: Adding epidemiological, environmental, or socio-economic variables
- **Supplementing missing information**: Appending approved variables from other sources
- **Aggregated data appending**: Population-level statistics matched by geographic or demographic identifiers
- **Annotation**: Adding descriptive information, coding references, or clinical annotations

> **Pitfall**: Where external enrichment involves record-level matching or joining across datasets to create person-level connections, it should be treated as **data linkage** for governance purposes unless national rules explicitly provide otherwise. (TEHDAS2 M5.4, Section 4.2.1)

## Data Quality Feedback Loop

The enrichment process can create a feedback loop to continuously improve data quality for secondary use, involving three actors:

### Data User
Performs enrichment within the SPE. If the enrichment is deemed valuable, they may return a description of the enrichment, or the enriched dataset where permitted and appropriate, to the HDAB or data holder. Sharing should occur under agreed conditions (free of charge, cost-recovery, or licensing arrangements).

### HDAB
Acts as the intermediary. Where foreseen by national frameworks, the HDAB may facilitate or coordinate the assessment of data enrichment activities. The Regulation does not assign HDABs formal responsibilities in this area.

### Data Holder
The original custodian of the data. They may engage with the HDAB or data user to make the enhanced dataset available for future use. Integration into operational systems may be constrained by legacy architectures or resource limitations.

## The EHDS User Journey and Enrichment

1. **Application for Data Access**: Applicant submits application specifying datasets, purpose, and any planned operations including enrichment intentions.
2. **Issuance of Data Permit**: HDAB issues a data permit defining scope, conditions, and limitations.
3. **Data Access and Processing in the SPE**: Data user gains access to requested datasets. Enrichment occurs within this phase.
4. **Exporting and Reporting Results**: Outputs are typically aggregated or anonymised. Documentation of enrichment methods and outputs may be communicated to the HDAB and data holder (in line with Recital 57).

## Data Preparation vs. Enrichment

Activities that are NOT enrichment (they are data preparation):
- **Data cleaning**: Addressing missing values, outliers, inconsistencies
- **Data formatting**: Standardising variable structures
- **Data harmonisation**: Aligning coding schemes or units across sources
- **Data validation**: Checking data integrity before analysis
- **Data correction**: Identifying and rectifying errors (e.g., standardising date formats, removing outliers)
- **Data deduplication**: Eliminating duplicate records

All of these are preparatory steps that make data fit for analysis, whereas enrichment adds new value.

## Practical Considerations for Sharing Enrichment

Data users should consider three questions before communicating enrichment results:

1. **Relevance beyond the current project**: Is the enrichment specific to one research question, or does it have broader applicability?
2. **Significance of effort and outcome**: Does the enrichment represent substantial analytical effort generating valuable new information?
3. **Regulatory and ethical considerations**: Can enrichment be shared without compromising the data permit, ethical approvals, or data minimisation principles?

Importantly, sharing methods, documentation, code, and executable procedures is often preferred over sharing enriched datasets themselves, reflecting practical constraints of data holder infrastructures.

## What Is Out of Scope

- **Data Linkage**: Covered in a separate TEHDAS2 guideline (see [[Data_Linkage]])
- **Critical errors in datasets**: Foundational integrity issues requiring HDAB/data holder resolution
- **Reporting of significant findings**: Covered in TEHDAS2 Milestone 8.2 guideline on notifying natural persons

## Key EHDS Articles

- **Art. 51(3)** — Member State discretion on enrichment governance
- **Recital 57** — Recognition of enrichment value; improved datasets made available free of charge to original data holder
- **Art. 73** — SPE as the environment where enrichment occurs
- **Art. 68** — Data access application (enrichment intent should be declared)

## Related Wiki Entries

[[Data_Linkage]] [[Secure_Processing_Environment]] [[HDAB_Approval]] [[Data_Minimization]]
