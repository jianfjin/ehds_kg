---
wiki_id: "WIKI-DAAMS-001"
title: "DAAMS Application System"
regulation: "Reg. (EU) 2025/327"
article: "70, 68, 53"
category: "secondary_use"
keywords: ["DAAMS", "Data Access Application Management System", "HDAB", "data permit", "application workflow", "front office", "back office", "TEHDAS2"]
index_refs: ["EHDS-2025-327-A68", "EHDS-2025-327-A54", "EHDS-2025-327-A51"]
anchors: []
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/technical-specifications-for-data-access-application-management-system-daams-for-health-data-access-bodies-hdabs.pdf"]
---

# DAAMS (Data Access Application Management System)

## Overview

The Data Access Application Management System (DAAMS) is a national platform designed to enable secure and compliant access to electronic health data for secondary usage across the European Union, in alignment with the EHDS Regulation. Operated by Health Data Access Bodies (HDABs) at national level, DAAMS manages the full application lifecycle and interacts with both national applicants and the cross-border EHDS infrastructure via the National Contact Point (NCP).

DAAMS serves as a core component of the national EHDS portal, supporting two main functions:

1. **Submission and management of national data access applications and data requests** originating within the Member State.
2. **Reception and processing of data access applications and data requests** submitted via the HealthData@EU Central Platform.

## Architecture

DAAMS operates within a modular national EHDS infrastructure, interoperating with other national systems via APIs. Key integration points:

- **National Health Dataset Catalogue**: DAAMS connects to the dataset catalogue for browsing and selecting datasets.
- **NCP (National Contact Point)**: DAAMS receives cross-border applications through the NCP, never communicating directly with HealthData@EU Central Platform.
- **SPE**: After permit issuance, the SPE is configured according to DAAMS-managed permit conditions.

Member States may designate multiple HDABs, each potentially operating its own DAAMS instance. A coordinating HDAB (or the NCP) distributes incoming applications to the appropriate DAAMS.

## DAAMS Front Office (Applicant Interface)

DAAMS MUST provide a GUI web interface supporting at least one official EU language (English SHOULD also be supported). Key front-office capabilities:

- **Draft application forms**: Applicants can create, save, modify, and clone draft forms.
- **Form templates**: Respective templates for data access applications and data requests, matching the EU Common Data Access Application form (to be specified by implementing acts under Art. 70(2)).
- **Dataset selection**: "Shopping cart" metaphor for selecting multiple datasets from the National Health Dataset Catalogue.
- **Form validation**: Mandatory field highlighting, field guidance text, validation errors as messages.
- **Submission**: Forms cannot be submitted with missing required fields or validation errors.
- **Status tracking**: Applicants can track application status including at minimum the states defined in the specification (e.g., DRAFT, SUBMITTED, PROCESSING, AWAITING_ADDITIONAL_INFORMATION, APPROVED, REJECTED).
- **Additional information**: Applicants can provide additional information when HDAB considers an application incomplete.
- **Messaging interface**: Structured exchanges between applicant and HDAB assessor with audit trail.
- **Withdrawal**: Applicants can withdraw submitted applications.
- **Export/Import**: Submitted forms exportable in machine-actionable format; draft forms may be importable.
- **Accessibility**: SHOULD comply with WCAG 2.0 or above.
- **Fee notification**: Applicants must be notified about applicable fees upon submission.

## DAAMS Back Office (HDAB Processing)

DAAMS is primarily responsible for processing national and incoming cross-border applications. Key back-office capabilities:

### Pre-Screening
- **Data Access Applications**: MAY support completeness check; applications deemed incomplete can be returned for completion or rejected with structured justification.
- **Health Data Requests**: MUST support completeness check with documented outcomes.

### Application Assessment
- HDAB personnel access and review applications.
- Request additional information from applicants with field-level flagging.
- Track application status updates through the workflow.

### Message Structure
Applications received via NCP from HealthData@EU CP contain:
- **Application attributes**: ID, type (Data Access / Data Request), title, user name
- **Dataset information**: Central dataset ID, title, country of origin, HDAB, provenance, catalogue ID
- **Form data**: Original language and translated sections/fields/values
- **Attachments**: Compressed zip file of submitted attachments

DAAMS acknowledges receipt via an ACK message with application ID, status, and timestamp.

## Application Lifecycle States

Key states managed by DAAMS:
- **DRAFT**: Form saved but not yet submitted
- **SUBMITTED**: Application submitted to HDAB
- **PROCESSING**: Under HDAB review
- **AWAITING_ADDITIONAL_INFORMATION**: HDAB requests more input from applicant (does not constitute a formal re-submission)
- **APPROVED**: Positive decision — data permit issued
- **REJECTED**: Negative decision with justification
- **WITHDRAWN**: Applicant withdrew application

Draft forms may expire (e.g., after 6 months of inactivity).

## Interoperability

DAAMS MUST NOT communicate directly with the HealthData@EU Central Platform. All cross-border communication flows through:

```
HealthData@EU CP → NCP → National Dispatcher API → DAAMS
DAAMS → NCP → National Dispatcher API → HealthData@EU CP
```

The HealthData@EU National Dispatcher provides an OpenAPI specification for all application processing methods.

## Scope

**In Scope**: Functional and non-functional requirements, data models, process flows/business logic, integration patterns, standardised components for cross-border interoperability.

**Out of Scope**: National-level implementation details, internal HDAB decision-making processes, SPE operation, opt-out management, helpdesk, fees and invoicing management.

## Key EHDS Articles

- **Art. 70(2)** — EU Common Data Access Application form (implementing acts)
- **Art. 68** — Data access application content and process
- **Art. 53** — Permitted secondary use purposes
- **Art. 51(3)** — Member States may designate multiple HDABs

## Related Wiki Entries

[[Secure_Processing_Environment]] [[Common_IT_Infrastructure]] [[HDAB_Approval]] [[Data_Linkage]]
