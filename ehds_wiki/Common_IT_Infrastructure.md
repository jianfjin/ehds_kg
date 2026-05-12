---
wiki_id: "WIKI-ITI-001"
title: "Common IT Infrastructure (HealthData@EU)"
regulation: "Reg. (EU) 2025/327"
article: "75, 76, 50-54"
category: "secondary_use"
keywords: ["HealthData@EU", "common IT infrastructure", "NCP", "National Contact Point", "eDelivery", "interoperability", "cross-border", "data exchange", "TEHDAS2"]
index_refs: ["EHDS-2025-327-A75", "EHDS-2025-327-A76", "EHDS-2025-327-A54", "EHDS-2025-327-A51"]
anchors: []
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-technical-specifications-for-health-data-access-bodies-on-the-implementation-of-the-common-it-infrastructure.pdf"]
---

# Common IT Infrastructure (HealthData@EU)

## Overview

The HealthData@EU infrastructure is the common EU infrastructure established under Chapter IV of the EHDS Regulation (Article 75) to enable secure and interoperable cross-border secondary use of electronic health data. It connects national contact points (NCPs) with the HealthData@EU Central Platform, operated by the European Commission.

## Key Definitions

- **HealthData@EU infrastructure**: The infrastructure connecting national contact points for secondary use with the HealthData@EU Central Platform.
- **HealthData@EU Central Platform**: The interoperability platform established by the European Commission to support and facilitate the exchange of information between national contact points for secondary use.

## Two-Layer Architecture

The infrastructure is built on two layers:

1. **Business Layer** — Managing message content and format. Implemented via HealthData@EU Dispatchers (national and central) that validate message conformance and ensure compliance with business and technical requirements.
2. **Messaging (Transport) Layer** — Responsible for secure exchange of messages. Implemented via eDelivery Access Points using the AS4 Conformance Profile (ebMS3 standard of OASIS).

## Key Infrastructure Components

### National Level (per Member State)
- **National Contact Point (NCP)**: The national gateway designated by each Member State. Acts as the interface between national services and the cross-border HealthData@EU infrastructure.
- **HealthData@EU National Dispatcher**: Business-layer component that validates message conformance and prepares messages for transmission.
- **National eDelivery Access Point**: Messaging-layer component ensuring secure message transport using the AS4 protocol.

### Central Level (EU Commission)
- **HealthData@EU Central Platform**: Platform operated by the Commission offering features required by the EHDS regulation.
- **HealthData@EU Central Dispatcher**: Business-layer component at central level.
- **Central eDelivery Access Point**: Messaging-layer component at central level.

## Communication Model

All communication is **point-to-point** between NCPs and the Central Platform:
- National Dispatchers and Access Points communicate ONLY with the Central Platform.
- There is NO peer-to-peer exchange between NCPs or national systems from different Member States.
- The European Commission's eDelivery building block (Domibus reference implementation) is used for messaging.

## Message Exchange Flow (NCP-initiated)

1. NCP sends message content to the National Dispatcher.
2. National Dispatcher validates conformance using the HealthData@EU Interoperability Test Bed Validator.
3. If valid, the message is forwarded to the National eDelivery Access Point.
4. National eDelivery Access Point encrypts and signs the message with national certificate and sends to Central eDelivery Access Point.
5. Central eDelivery Access Point forwards to Central Dispatcher for processing.

## HealthData@EU Use Cases

### Dataset Management
- Create/Update/Delete Dataset Request

### Application Lifecycle
- Data Access Application Form Exchange
- Data Request Application Form Exchange
- Communication between applicant and assessors
- Update of submitted applications

### Decision Outcomes
- Positive/Negative decision for data access application (Data Permit)
- Positive/Negative decision for data request application

### Appeals and Reporting
- Create appeal from negative decision
- Create Biennial Report of HDAB
- Create Analysis Study Record
- Create Sanctions and Penalties Record

## Regulatory Provisions Mapped to Infrastructure

| Regulation | Infrastructure Implementation |
|---|---|
| Secure communication (Art. 75) | eDelivery Access Points (Messaging layer) |
| Interoperability and standardisation | HealthData@EU Dispatchers (Business layer) |
| EU Dataset Catalogue Synchronisation | Central Platform receives dataset metadata from Member States via NCPs |
| Cross-border data access mechanisms | Central Platform distributes requests to relevant NCPs |

## Scope

**In-Scope**: NCPs, National and Central Dispatchers, eDelivery (Domibus), HealthData@EU Central Platform.

**Out of Scope**: Detailed UI designs, Member State-specific modules or extensions, detailed Central Platform architecture, low-level technical implementation details (deployment configs, source code, runtime specs).

## Key EHDS Articles

- **Art. 75** — Common infrastructure for secondary use: Commission develops central services; Member States establish NCPs; common technical and organisational requirements
- **Art. 76** — EU-level dataset catalogue synchronisation
- **Art. 50-54** — General secondary use framework and permitted purposes
- **Art. 51(3)** — Member States may designate multiple HDABs

## Related Wiki Entries

[[Secure_Processing_Environment]] [[DAAMS_Application_System]] [[HDAB_Approval]] [[Data_Linkage]]
