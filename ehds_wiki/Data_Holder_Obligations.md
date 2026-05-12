---
wiki_id: "WIKI-DHO-001"
title: "Data Holder Obligations for Secondary Use"
regulation: "Reg. (EU) 2025/327"
article: "60, 63, 51, 72, 77, 50"
category: "secondary_use"
keywords: ["data holder", "Article 60", "personal data", "non-personal data", "trusted data holder", "data provision", "SPE", "dataset catalogue", "HealthDCAT-AP", "intermediation entity", "HDIE"]
index_refs: ["EHDS-2025-327-A60", "EHDS-2025-327-A63", "EHDS-2025-327-A51", "EHDS-2025-327-A72", "EHDS-2025-327-A77"]
anchors: ["A60-P1", "A60-P3", "A60-P5", "A63-P3"]
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-guideline-for-health-data-holders-on-making-personal-and-non-personal-electronic-health-data-available-for-reuse.pdf"]
---

# Data_Holder_Obligations

The EHDS Regulation imposes mandatory duties on health data holders to make personal and non-personal electronic health data available for secondary use. These obligations apply across a heterogeneous landscape of entities and are enforceable by HDABs.

## Definition of a Health Data Holder

Under Art. 2(2)(t) EHDS, a health data holder is any natural or legal person, public authority, agency or other body in the healthcare or care sectors that processes electronic health data and has either:
- (i) The right or obligation to process personal electronic health data as a controller or joint controller for healthcare, public health, reimbursement, research, innovation, policymaking, official statistics, patient safety, or regulatory purposes; OR
- (ii) The ability to make available non-personal electronic health data through control of technical design of a product and related services.

### Who Qualifies
- Healthcare providers (hospitals, clinics, GPs, physiotherapists)
- Public authorities/agencies (monitoring, statistics, epidemiological surveillance)
- Health insurers and reimbursement organisations
- Developers of health-related products, services, and wellness applications
- Research institutions and registries (health registries, mortality registries)
- EU institutions, bodies, and agencies managing health data

### Exemptions (Art. 50)
- Natural persons (individual researchers)
- Microenterprises (< 10 employees AND < €2M turnover or balance sheet)
- Member States may extend obligations to microenterprises via national law.

## Core Mandatory Duties (Art. 60)

### 1. Personal Data Provision (Art. 60(1))
Upon receipt of a data permit or approved data request, provide the required personal electronic health data to the HDAB **no later than 3 months**, extendable once by another 3 months in justified cases. The timeline begins when the HDAB notifies the data holder (Art. 63(3)).

### 2. Non-Personal Data Provision (Art. 60(5))
Make non-personal electronic health data available via **open public databases** that comply with standards for transparency, governance, and long-term accessibility. Non-personal data includes:
- Personal data rendered anonymous (data subject not identifiable)
- Synthetic datasets (not containing actual personal information)
- Data that does not relate to individuals

### 3. Dataset Description and Metadata (Art. 60(3), 77)
- Submit metadata describing datasets to the national dataset catalogue.
- Review and update at least **once per year** (Art. 77(2)).
- Use HealthDCAT-AP common metadata model for discoverability and semantic interoperability.

## Three Data Provision Pathways

| Data Type | Access Mechanism | Processing Location |
|-----------|-----------------|---------------------|
| Personal electronic health data | Data permit or data request via HDAB | SPE (Secure Processing Environment) |
| Non-personal — Open Data | Public platform (Art. 60(5)) | Freely accessible |
| Non-personal — Restricted Access | HDAB approval of permit/request | May involve additional safeguards |

## Recommended (Non-Mandatory) Tasks

TEHDAS2 experts recommend data holders also:
- Organise internal systems for accurate dataset descriptions and quality labels.
- Set up workflows for data extraction, preparation, and secure transfer to SPE.
- Communicate with HDABs for clarifications, quality checks, or complaint handling.
- Coordinate with other EHDS stakeholders (SPEs, intermediation entities, pseudonymisation services).
- Correct errors in provided datasets when notified.
- Handle enriched datasets returned by data users (per national law).
- Respond to significant findings forwarded by HDAB (Art. 58(3), 61(5)) — inform the natural person or treating health professional under national law.

## Trusted Data Holder (Art. 72)

Member States may optionally designate certain data holders as Trusted Data Holders (TDHs) if they meet conditions:
- Ability to provide access via SPE with adequate technical/organisational measures.
- Necessary expertise to assess data access applications and requests.
- Ability to guarantee compliance with EHDS Chapter IV.

### TDH Duties (delegated by HDAB)
- Preliminary assessment of data access applications.
- Processing and preparation of datasets (including pseudonymisation/anonymisation).
- Provision of access through compliant SPE.

### Important Legal Points
- HDAB remains the **sole decision-maker** — TDH provides assessment and proposal.
- TDH acts as **controller** when preparing data/anonymising; as **processor** on behalf of the user when granting SPE access.
- TDH must submit assessment within 2 months; HDAB issues final decision within another 2 months.
- TDH must store and process personal health data within the EU (unless GDPR adequacy decision applies, Art. 87).

## Health Data Intermediation Entities (HDIE) — Art. 50(3)

Member States may establish HDIEs to reduce administrative burden on smaller/less-resourced data holders. HDIEs may:
- Prepare and process data for provision to HDABs.
- Facilitate metadata submission to catalogues.
- Manage technical operations for data sharing.
- Provide access via SPEs.

**Legal responsibility remains with the data holder** unless explicitly transferred by national law. HDIEs differ from DGA data intermediation services (business-to-business) — they operate under a public-task framework.

## Data Preparation Workflow

1. **Interpret data permit/request**: Understand which data is needed.
2. **Create data subset**: Apply inclusion/exclusion criteria, filter by the 5 dimensions (Who, What, When, Where, How — see [[Data_Minimization]]).
3. **Apply preparation measures**: Pseudonymisation, anonymisation, or other de-identification.
4. **Provide data**: Transfer to SPE (personal data) or public platform (non-personal open data).

## Timeliness Requirements

- **3 months** from HDAB notification (for personal data provision under Art. 60(1)).
- Extendable by **+3 months** in justified cases.
- Dataset descriptions reviewed/updated **at least annually** (Art. 77(2)).

## Interaction Points with HDABs

Data holders may interact with HDABs during:
- Data discovery: responding to feasibility queries.
- Data access: receiving notification of permits/requests.
- Data preparation: clarifying requirements, negotiating subset scope.
- Finalisation: receiving significant findings, handling complaints.

## Pitfalls

- No distinction in duties between public and private data holders, or between different healthcare system models — all face the same Art. 60 obligations.
- Entities that grow beyond microenterprise status become subject to full obligations; transitional planning is recommended.
- Inaccurate or outdated metadata may result in non-compliance with Art. 60(3) and Art. 77(2).
- Non-personal data provision via open databases requires robust governance and sustainability — not a one-time upload.

## Related

[[Data_Minimization]] [[Pseudonymisation_Anonymisation]] [[HDAB_Approval]] [[Opt_Out_Mechanism]] [[Significant_Findings_Notification]] [[Data_Linkage]]
