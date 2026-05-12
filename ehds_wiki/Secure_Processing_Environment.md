---
wiki_id: "WIKI-SPE-001"
title: "Secure Processing Environment"
regulation: "Reg. (EU) 2025/327"
article: "73, 68, 44"
category: "secondary_use"
keywords: ["SPE", "Secure Processing Environment", "Article 73", "federation", "data security", "access control", "sensitive data", "output control", "TEHDAS2"]
index_refs: ["EHDS-2025-327-A73", "EHDS-2025-327-A68", "EHDS-2025-327-A44", "EHDS-2025-327-A54"]
anchors: []
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-technical-functional-and-security-specifications-of-secure-processing-environments.pdf"]
---

# Secure Processing Environment (SPE)

## Overview

A Secure Processing Environment (SPE) is the central technical component of the European Health Data Space (EHDS) for secondary use of electronic health data, as required under Article 73 of Regulation (EU) 2025/327. SPEs enable safe secondary use of health data while ensuring compliance with data protection, confidentiality, and information security obligations.

As defined by the EU Data Governance Act (DGA, EU 2022/868), an SPE is:

> "the physical or virtual environment and organisational means to ensure compliance with Union law, such as Regulation (EU) 2016/679, in particular with regard to data subjects' rights, intellectual property rights, and commercial and statistical confidentiality, integrity and accessibility, as well as with applicable national law, and to allow the entity providing the secure processing environment to determine and supervise all data processing actions, including the display, storage, download and export of data and the calculation of derivative data through computational algorithms." (DGA, Article 2)

## EHDS Article 73 Requirements

An EHDS-compliant SPE must satisfy:

- **Data security**: Prevent unauthorised access, ensure data confidentiality, and maintain integrity.
- **Restricted access**: Allow data users to process data only within the scope defined by their data access permit (Art. 73(1)(a)).
- **Controlled outputs**: Ensure that only aggregated or anonymised results are exported, subject to HDAB approval (Art. 73(1)).
- **Individual user identities**: Use of unique, persistent, auditable, and non-transferable user identities with confidential access modes (Art. 73(1)(d)).
- **Limited privileged access**: Restrict access to a limited number of authorised, identifiable individuals (Art. 73(1)(c)).

## SPE Lifecycle

1. **Environment Creation**: Once a data permit is issued, the SPE operator sets up an isolated environment instance tailored to the permit conditions. Typically deployed as a virtual machine in a dedicated cluster or cloud environment.
2. **Data Reception**: Data is transferred from the data holder to the SPE via secure interfaces.
3. **Data Processing**: Authorised users carry out analysis within the SPE, with no ability to export personal data.
4. **Output Review**: Results are reviewed for anonymity/aggregation before export.
5. **Data Deletion**: All electronic health data MUST be deleted within six months of data permit expiry (Art. 68(12)), including backups and redundant copies.

## Core Roles

- **HDAB (Health Data Access Body)**: National authority overseeing access to sensitive health data. Ensures data corresponds to permit conditions, oversees SPE compliance, conducts audits, and provides guidance/training.
- **SPE Operator**: Manages technical, operational, and security measures. May be the HDAB itself or a separate entity acting as a processor under a data processing agreement.
- **Data Holder**: Organisation possessing original health datasets (hospitals, registries, research institutions). Provides requested data to HDAB under legal/technical safeguards.
- **Health Data User**: Authorised individual/organisation accessing data within the SPE for approved secondary use.

## Two Use Cases (Trust Models)

1. **Distrusting Use Case**: Health data user processes health data under a data permit. The user cannot export anything except anonymous results. The HDAB oversees the entire process.
2. **Trusting Use Case**: HDAB employees process the permitted data that will be handed over to the health data user's SPE. This use case protects data from non-users only, matching general scientific research requirements.

## Core SPE Requirements (Sensitive Data)

Derived from the TEHDAS2 M7.4 specification:

- **SDR-1**: Unauthorised users MUST NOT be able to access sensitive data.
- **SDR-2**: Service administrators SHOULD NOT have access to sensitive data (except for authorised technical maintenance).
- **SDR-3**: Sensitive data MUST be in a protected format at rest and in transit (encryption).
- **SDR-4**: Sensitive data protection MUST use widely accepted, secure algorithms combined with effective isolation measures.

## Operational Requirements

SPE operational requirements are organised into six categories:

1. **Main SPE roles** — Clear role definitions and responsibilities
2. **SPE setup and access management** — OPR-1: Enforce user authentication and access restrictions based on data permit; OPR-2: Limit number of authorised staff with privileged access
3. **SPE auditing, compliance and reporting** — Log all access and operations; maintain audit trails
4. **Monitoring and incident management** — Detect and respond to security incidents
5. **Risk management and mitigation** — Regular risk assessments aligned with NIS2 and ISO 27001/27002
6. **Maintenance and support** — Service portfolio management, configuration management (CMDB), termination upon permit expiry

## SPE Federation

EHDS secondary use is inherently a federation of interconnected services. Key federation requirements (FSPER):

- **FSPER-1**: Legal or contractual agreement MUST cover the SPE federation across organisations.
- **FSPER-2**: Federation user identities MUST match over services.
- **FSPER-3**: An SPE federation MUST fulfil sensitive data processing requirements defined for stand-alone SPEs.
- **FSPER-4**: All interactive user actions on sensitive data in the federation MUST be through SPE.
- **FSPER-5**: Federation governance MUST cover secure, shared data access and export.
- **FSPER-7**: Federation MUST have technical and semantic interoperability for shared processing.
- **FSPER-8**: Federation MUST use shared secure communication and data transfer protocols (e.g., EU eDelivery, GA4GH crypt4GH).

## FitSM Framework

TEHDAS2 recommends FitSM as a lightweight, open-source IT Service Management standard for coordinating SPE operations. FitSM was developed through an EC-funded project (FedSM, 2012-2015) and supports federated service provision. It is proposed as a practical framework for connecting security and operational requirements across EHDS SPEs.

## Key EHDS Articles

- **Art. 73** — SPE requirements: access restriction, user identities, limited administrators, output controls, audit logs
- **Art. 68** — Data access application, data permit, 6-month deletion requirement (68(12))
- **Art. 44** — Security of processing including pseudonymisation
- **Art. 54** — Secondary use for scientific research (where SPEs are most used)

## Related Wiki Entries

[[Data_Linkage]] [[HDAB_Approval]] [[DAAMS_Application_System]] [[Common_IT_Infrastructure]] [[Data_Enrichment]]
