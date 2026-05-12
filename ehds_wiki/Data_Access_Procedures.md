---
wiki_id: "WIKI-DAP-001"
title: "Data Access Procedures and Formats for HDABs"
regulation: "Reg. (EU) 2025/327"
article: "67, 68, 69, 72, 73"
category: "secondary_use"
keywords: ["data access application", "data request", "completeness check", "data permit", "assessment process", "HDAB workflow", "time frames", "application formats"]
index_refs: ["EHDS-2025-327-A67", "EHDS-2025-327-A68", "EHDS-2025-327-A69", "EHDS-2025-327-A72", "EHDS-2025-327-A73"]
anchors: ["A67-P1", "A68-P4", "A69-P2", "A72-P1"]
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-guideline-for-health-data-access-bodies-on-the-procedures-and-formats-for-data-access.pdf"]
---

# Data_Access_Procedures

## Definition

The TEHDAS2 D6.3 Guideline provides operational guidance for HDABs on the end-to-end procedures for managing health data access applications (Article 67) and health data requests (Article 69). It covers three distinct workflow stages: (1) the **application completeness check**, (2) the **assessment and evaluation process**, and (3) **post-decision actions**. The guideline also addresses simplified procedures with Trusted Health Data Holders (TDHs) under Article 72.

## Workflow Stages

### Stage 1: Application Completeness Check (Articles 68(4), 69(3))

The completeness check is a **pre-screening validation step**, not a substantive review. It verifies that all mandatory information is submitted with plausible content. A 'complete application' is one where all required information is provided, contextually relevant, and semantically meaningful.

**Three types of checks:**

1. **Technical Completeness:** All mandatory fields filled, attachments openable and non-empty. The DAAMs (Data Access Application Management systems) ensure mandatory fields are filled before submission.

2. **Semantic Validity (does the input make sense?):** Text fields contain real words (not random characters), numerical fields contain valid values, address fields resemble real address formats.

3. **Contextual Consistency (is the input relevant?):** Cross-field consistency checks to identify illogical or contradictory entries (e.g. project title unrelated to described purpose). This is a sanity check — not an assessment of scientific soundness.

**Key procedural requirements:**
- Applications must be made public through electronic means **without undue delay after initial reception** (Article 57(1)(j)(ii)), even before completeness check
- If incomplete, applicant has **up to four weeks** to provide missing information
- A similar four-week window can be applied operationally to data requests for consistency
- The completeness check should not cause undue delays — HDABs may set internal targets (e.g. 5–10 working days)

**Application form templates** are provided in Annexes 5 (data access application) and 6 (data request) of the guideline, with completeness checklists in Annexes 7 and 8. Data permit and data request approval templates are in Annexes 9 and 10. Key recommendations for electronic contractual arrangements are in Annex 11.

**Completeness check by application type:**

For **data access applications** (Annex 7 checklist), the HDAB verifies:
- Applicant identification and contact details, legal status, mandate documentation (for public sector purposes a–c)
- Research plan, ethics approval, funding evidence
- Description of intended use and expected benefits, data minimisation justification
- Data specification: variables, population, time period, format requirements
- IPR and trade secrets risk mitigation measures

For **data requests** (Annex 8 checklist), a lighter verification applies since only anonymised statistical output is provided:
- Simplified applicant information
- Statistical question formulation and expected output description
- Justification that anonymised aggregated data is sufficient for the stated purpose

### Stage 2: Application Assessment Process

Once the application is deemed complete, the HDAB proceeds to assess whether a data permit should be issued or a data request approved. The assessment evaluates all requirements under the EHDS Regulation:

**Assessment criteria include:**
- Whether the described purpose corresponds to one or more of Article 53(1)(a)–(f) purposes
- That nothing indicates infringement of Article 54 prohibited uses
- Data minimisation check (adequate, relevant, limited to what is necessary)
- Ethical evaluation where required (Article 68(1)(f))
- Risk mitigation for IP and trade secrets (Article 52)
- Risk analysis for national defence, security, public security (Articles 63, 68)
- Whether data holders can provide the requested data

**Key actions during assessment:**
- HDAB must contact health data holders to establish data extractability
- Provide a consolidated fee estimate to the applicant (Article 62(5))
- The applicant may review the application to reduce costs or withdraw (only charged for costs incurred so far)
- All decisions (approval or refusal) must be published with reasoning for refusals (Article 58(1)(f))

**Decision types:**
- **Data Permit** (Article 68): Grants access to individual-level pseudonymised/anonymised data within an SPE
- **Data Request Approval** (Article 69): Grants access only to anonymised, aggregated statistical results
- **Refusal:** Must include justification and be published

### Stage 3: Post-Decision Actions

After a data permit is granted or data request approved:

1. **Data Extraction:** HDAB requests extraction from data holders (Article 68(7))
2. **Data Preparation:** Data holders prepare data (selection, extraction, pseudonymisation/anonymisation, consolidation)
3. **SPE Access:** Data is made available in Secure Processing Environment; users receive credentials
4. **Invoicing:** HDABs invoice according to fee guidelines (see [[EHDS_Fees]])
5. **Monitoring:** Continuous compliance monitoring (Article 57(1)(a)(ii)), regular audits, security assessments
6. **Process Documentation:** Activity report every two years (Article 59(1)), records of applications, processing, security
7. **Revocation:** HDABs can revoke permits for non-compliance, must notify SPE provider and other HDABs via HealthData@EU IT tool
8. **Appeal Process:** All final decisions subject to appeal under national administrative law; EU Court of Justice for UHDAS decisions
9. **Amendments:** Users can apply for permit extensions or updates to access lists; data/scope changes require new application
10. **Results Publication:** Publication of outputs from secondary use required
11. **Data Deletion:** Data must be deleted from SPE within **six months** of permit expiry (Article 68(12))

## Time Frames

| Phase | Time Frame | Legal Basis |
|-------|-----------|-------------|
| Completeness check | No statutory limit (HDAB internal target: 5–10 working days) | — |
| Applicant completion window | Up to **4 weeks** | Art. 68(4) |
| Data permit decision (standard) | **3 months** from complete application; extendable by **3 more months** | Art. 68(4) |
| Data permit decision (accelerated — public sector) | **2 months** from complete application; extendable by **1 more month** | Art. 68(4) |
| Data request decision | **3 months** from receipt (no separate completeness phase mandated) | — |
| TDH assessment submission | **2 months** from receiving forwarded application | Art. 72 |
| HDAB decision after TDH assessment | **2 months** from receiving TDH assessment | Art. 72 |
| Data deletion from SPE | Within **6 months** of permit expiry | Art. 68(12) |

**Prioritisation:** HDABs are NOT required to follow a strict first-in-first-out approach (Recital 74). They may prioritise based on urgency (public health emergencies), public interest value, and available capacity — provided criteria are objective and transparent.

## Simplified Procedure with TDH (Article 72)

When an application concerns only electronic health data held by a TDH:
- Application is forwarded to the TDH
- TDH assesses against the same criteria as the HDAB
- TDH submits assessment and proposal within **2 months**
- HDAB makes the final decision within **2 months** of receiving the assessment (not bound by TDH proposal)
- TDH prepares data and provides access via SPE

## Cross-Border and Multi-Country Cases

For multi-country applications, the HealthData@EU Central Platform manages submissions. National DAAMs interface with the central platform. HDABs must coordinate across Member States for consistent handling.

## Practical Examples

- **Example 1:** An application is submitted with an empty research plan attachment → completeness check flags as incomplete → applicant given 4 weeks to provide the attachment → if not provided, application rejected without prejudice.
- **Example 2:** A public health authority submits an urgent pandemic-related application → recognised as accelerated procedure → decision within **2 months** (extendable by 1 month).
- **Example 3:** A data user submits amendment to add a colleague to SPE access list → simple administrative update; but requesting new data variables → requires a new application.

## Pitfalls

1. **Confusing completeness with assessment:** The completeness check must NOT include judgements on content quality or scientific validity — this belongs to the assessment phase.
2. **Missing the accelerated timeline:** Public sector applications under Art. 53(1)(a–c) must be identified early to meet the 2-month deadline.
3. **Not publishing applications promptly:** Applications must be made public immediately upon receipt — before the completeness check.
4. **Over-reliance on post-hoc amendments:** The guideline emphasises that users should provide comprehensive information at application time rather than relying on amendment requests.

## Related
[[HDAB_Minimum_Categories]] [[EHDS_Fees]] [[EHDS_Penalties]] [[HDAB_Approval]] [[Data_Linkage]]
