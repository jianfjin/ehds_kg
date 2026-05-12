---
wiki_id: "WIKI-FEE-001"
title: "EHDS Fees for Health Data Access"
regulation: "Reg. (EU) 2025/327"
article: "62"
category: "secondary_use"
keywords: ["fees", "cost recovery", "invoicing", "compensation", "data access fees", "Article 62", "marginal costs", "fixed costs", "transparency", "non-discrimination"]
index_refs: ["EHDS-2025-327-A62"]
anchors: ["A62-P1", "A62-P2", "A62-P5"]
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-guideline-on-fees-related-to-the-ehds-regulation.pdf"]
---

# EHDS_Fees

## Definition

The TEHDAS2 M4.1.1 Draft Guideline on fees provides recommendations on the fee structure for accessing health data for secondary use under Article 62 of the EHDS Regulation. It addresses three core questions: **which costs can be included in fees (and which are excluded)**, **to whom fees should be paid**, and **when fees should be paid** by the data user (DU).

The fee framework aims to promote **transparency, fairness, and operational efficiency** in line with principles of non-discrimination, proportionality, and competition neutrality (Article 62).

## Legal Basis — Article 62

- HDABs (including the Union health data access service) and TDHs **may** charge fees for making electronic health data available for secondary use (Article 62.1)
- Fees may include **compensation for costs incurred** by the data holder for compiling and preparing the electronic health data (Article 62.2)
- The EHDS does NOT mandate charging fees — compensation may range from partial to full, depending on national approach and funding context
- Reduced fees may be offered to: public sector bodies, Union institutions with public health mandates, university researchers, or microenterprises (Article 62.1)

## Guiding Principles (Article 62)

1. **Transparency:** Fees are related to eligible costs incurred. Before issuing a data permit, the HDAB must inform the applicant of estimated fees (Article 62.5). When fees are claimed, an invoice is provided describing the amount and what it covers.

2. **Non-discrimination:** DUs of the same category are treated equally regardless of nationality, charged equivalent fees proportional to actual costs. Specific categories (e.g. academics, small enterprises, public sector) may benefit from reduced fees at the discretion of each Member State.

3. **Proportionality:** Fees must be proportionate to the cost of making data available. They must not restrict competition or create undue barriers for any eligible DU category.

4. **Competition Neutrality:** Fee structures must not be used to distort or restrict competition. No double compensation — any eligible costs already covered by public or private funding cannot be used to justify fees.

5. **No double compensation:** Expenses already financed through other sources must be excluded from fee calculation.

## Excluded Costs (Cannot Be Charged)

1. **Primary use data collection and processing:** All costs associated with data collection for medical purposes (primary use). However, specific "by design" efforts to support future secondary use may be eligible if necessary for a specific secondary use request.

2. **Data discovery phase:** Costs for creating, updating, and maintaining metadata records and catalogues (Article 77), including quality labelling (Article 78). These are regulatory obligations, not user-specific services.

3. **Information on significant findings:** Costs related to informing natural persons about significant health findings identified by DUs (Recital 67, Article 58.3).

## Included Costs (Eligible for Fee Recovery)

### Phase 1 — Receipt of Data Access Application / Data Request

**HDAB may charge for:**
- Application management (completeness check process)
- Running and updating the public information system
- Regulatory feasibility assessment
- Assessment of datasets to be requested from DHs
- Preparation of the consolidated fee estimate (quote)
- Related administrative overheads

**DHs may charge for:**
- Examination of protocol and feasibility study
- Preparation of the quote
- Related administrative overheads

### Phase 2 — Data Permit / Data Request Approval

**HDAB may charge for:**
- Assessment against EHDS criteria (Article 68(1))
- Ethical evaluation where required (Article 68(1)(f))
- Risk mitigation analysis for IP and trade secrets (Article 52)
- Risk analysis for national defence, security, public order
- Permit/request decision with justification
- Updating public information system
- Project contracting and monitoring
- Related administrative overheads

### Phase 3 — Data Preparation

**DHs may charge for:**
- Data selection, extraction, including data minimisation and pseudonymisation/anonymisation
- Data consolidation
- Data export to HDAB
- Project monitoring
- Patient information for the use of their data

**Depending on data holder strategy:**

*Database/Warehouse Model (fixed costs):*
- Data extraction from initial information system
- Data quality improvement related to compiling and preparation
- Data linkage between different data systems
- Data storage and infrastructure costs (running, maintaining, updating)
- Regulatory obligation to inform natural persons

*Per-Request Model (marginal costs):*
- Data quality improvement (per-request specific)
- Data linkage for the specific request

### Phase 4 — Provision of Data

**HDAB may charge for:**
- Data quality, linkage, and consolidation
- Pseudonymisation or anonymisation
- Data treatment to protect IP and trade secrets
- Dataset validation
- SPE project space preparation
- Data export to project space
- Tool adaptation and development, licences
- SPE access, additional services, environment updates
- User training and support
- Technical resources (CPU time, disk space allocation)
- Related administrative overheads

**For data requests specifically:**
- Preparation of analysis plan for data aggregation
- Generation of aggregated data

### Phase 5 — Use of Data

**HDAB may charge for:**
- Project closure activities (final reporting, data archiving, controlled data destruction)
- Long-term storage of metadata or audit logs
- Continued allocation of computing resources and storage
- Permit extension and related SPE updates

### Simplified Procedure with TDH (Article 72)

TDHs may obtain compensation for performing HDAB-equivalent responsibilities: data preparation, SPE configuration, and other assessment duties normally borne by the HDAB.

## How Fees Are Computed

**Marginal Costs (per-request):**
- Based on specific resources used to process the application
- Human resources: time required × hourly rate derived from staff salaries
- Technological resources: consumption of infrastructure (disk space, CPU, GPU)

**Fixed/Structuring Costs (shared across users):**
- Expenses to build/maintain secondary-use infrastructure (database development, data modelling, data quality, standardisation, licences)
- Annually compensated through proportional allocation using transparent methodology

### Simplified Calculation Example (Fixed Costs)

For a secondary-use database:
```
WAC_DBk = Cost_DBk / NbPatients_DBk
F_REQ = Σ_DBk [(NbPatients_REQ × WAC_DBk) / NbProjects_DBk]
```
Where DBk = data block, WAC = weighted average cost, REQ = request.

Requires annual recalibration based on 3-year retrospective costs.

## To Whom Fees Are Paid — Three Invoicing Scenarios

| Scenario | Model | Description | Recommendation |
|----------|-------|-------------|----------------|
| **Scenario 1** | Centralised | HDAB consolidates all fees into a single invoice to DU, collects payment, redistributes to stakeholders | **Recommended baseline** (aligned with Recital 70) |
| **Scenario 2** | Decentralised | HDAB, TDHs, and DHs each issue their own invoice directly to DU | Increases DU burden; challenges for smaller DHs |
| **Scenario 3** | Hybrid | HDAB offers centralised invoicing but allows DHs to invoice directly if they have operational maturity | Provides flexibility while preserving coherence |

**Recommendation:** The **centralised model (Scenario 1)** is preferred as it reflects Recital 70 and ensures simplicity and transparency for DUs. However, Member States may adopt models adapted to their national contexts, provided the principles of transparency, consistency, and proportionality are respected.

## When Fees Are Paid

Key payment concepts:
- **Invoice:** Legally binding commercial document with complete cost breakdown by services and DHs
- **Request for Payment:** Formal request for payment of actual costs for work completed in a specific period
- **Payment Instalment:** Scheduled payment aligned with procedure progress or service delivery

**Payment timing:**
- Fee estimate provided before data permit decision; applicant may withdraw if costs are unacceptable
- If withdrawn, applicant only charged for costs incurred so far
- Actual invoicing follows data permit issuance, structured as instalments aligned with delivery milestones

## Current Situation Across Member States

- 46% of surveyed Member States reported **no formalised pricing practices** for data provision
- 63% reported **no regulatory framework** governing fee application
- Some offer free access (e.g. Slovakia), others full break-even (e.g. Sweden)
- Fees generally based on hourly rates for data preparation effort
- Reduced fees common for academics, students, patient organisations, and small enterprises
- Main challenge: aligning fees and practices within countries and across Member States

### Cross-Border Fee Disparity Risks

The TEHDAS2 survey identified a critical systemic risk: **economic disparities among Member States** directly affect fees because cost recovery is based on local salaries and technological provision costs. This may:

- **Create imbalance in HDAB burden distribution** across Europe when data are substitutable among countries
- **Undermine cross-border access** to health data for users from certain Member States
- **Reduce representativeness** of some countries in European studies
- **Exacerbate differences** between Member States, counteracting the intended harmonisation effects of the EHDS

Maintaining **preferential pricing schemes** for academics and small companies is perceived as essential to ensure a level playing field for research and innovation in the EU. Several Member States highlighted the importance of cultural and organisational change, as well as the need for further guidance, capacity-building, and coordination mechanisms.

## Practical Examples

- **Example 1:** A university researcher applies for pseudonymised hospital data. HDAB collects fee estimates from 3 DHs, consolidates into a single invoice → researcher pays HDAB → HDAB redistributes to DHs.
- **Example 2:** A pharmaceutical company applies under purpose (e) for scientific research. The project requires data preparation from a warehouse → fixed costs shared proportionally across all projects using that data block.
- **Example 3:** An applicant receives the fee estimate and realises the costs exceed their budget → withdraws application → only charged for the completeness check and quote preparation already performed.

## Pitfalls

1. **Double compensation:** Charging for costs already covered by public funding violates the fee principles.
2. **Charging for data discovery:** Metadata catalogue and dataset descriptions are regulatory obligations and cannot be charged to DUs.
3. **Lack of transparency:** Not publishing the fee calculation methodology undermines trust and may violate non-discrimination principles.
4. **Underestimating fixed cost allocation:** Without proper annual recalibration, fixed costs may be unfairly distributed among too few projects.

## Related
[[Data_Access_Procedures]] [[HDAB_Approval]] [[Data_Minimization]]
