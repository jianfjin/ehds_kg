---
wiki_id: "WIKI-On_How_To_Use_Data_In_A_Secure_Processin"
title: "On How To Use Data In A Secure Processing Environment"
regulation: "Reg. (EU) 2025/327"
category: "hdab"
priority: 0.15
tags: ["category:hdab", "priority:new"]
keywords: ["EHDS", "SPE", "secure processing environment", "data user", "HDAB", "pseudonymisation", "anonymisation", "data permit", "data controller", "Article 73", "Article 74", "Article 62", "data export", "data analysis", "fees", "rule violation", "TEHDAS2", "D7.1"]
version: "1.0"
created: "2026-06-09"
updated: "2026-06-11"
priority: 0.15
sources: ["data/source_pdfs/d7.1-guideline-on-how-to-use-data-in-a-secure-processing-environment.pdf"]
---

# On How To Use Data In A Secure Processing Environment

**TEHDAS2 — D7.1 Guideline on how to use data in a secure processing environment, 27 May 2025 (final deliverable after public consultation)**

This guideline supports data users who plan to access personal electronic health data for secondary use through the HealthData@EU infrastructure. It covers activities from gaining access to a Secure Processing Environment (SPE) through to completion of analysis and export of results.

## What is an SPE?

An SPE is a secure digital workspace where authorised users process electronic health data in a highly controlled manner. SPEs are a core component of the EHDS infrastructure enabling secondary use of personal electronic health data. The legal basis is in Article 2(1)(c) and Article 73 of the EHDS Regulation, building on the definition in Article 2(20) of the Data Governance Act (DGA).

SPEs must meet at least three core criteria:
- **Data security**: Prevent unauthorised access, maintain confidentiality, ensure data integrity.
- **Restricted access**: Users may process only data covered by a valid data permit, within the permitted scope.
- **Controlled outputs**: Only non-personal data — aggregated and anonymised results — may be exported, after HDAB authorisation.

SPEs may be used in two contexts: (1) by data users under a data permit (Articles 68–74), and (2) by HDABs when preparing data for data requests (Article 69).

## Data Format in SPE

No directly identifiable personal data (names, addresses, SSNs) are provided to data users. Data in an SPE is either **pseudonymised** or **anonymised** as defined in the data permit. Pseudonymised data still refers to individual persons, enabling individual-level analysis while preventing direct identification by the data user. Pseudonymisation must be justified in the access application and approved in the data permit (Articles 67(2)(e) and 68(1)(c)). Users cannot download personal data — only anonymised, aggregate outputs may leave the SPE after HDAB validation (Article 73(2)).

## Suggesting the Appropriate SPE

HDABs are responsible for granting access and attributing the SPE. Data applicants may suggest an SPE, providing reasons (cost, prior experience, technical requirements). The final decision lies with the HDAB. The selected SPE is specified in the data permit (Article 68). Each Member State must ensure at least one functional SPE is available.

When suggesting an SPE, applicants should specify required computational power, data volume/storage, required software tools, and specific data types (genomics, imaging, etc.). Different SPEs vary in software availability, data types supported, computing power (including GPU/HPC), cost models, and access modalities (web interface, virtual desktop).

## Fees

Under Article 62, HDABs may charge fees for: evaluating data access applications, preparing datasets (pseudonymisation, anonymisation, linkage), and using the SPE (provision, training, software licences, processing, storage, output verification). Fees must be transparent, proportionate, and non-discriminatory. The single invoice principle (Article 62(6)) applies: HDAB issues one invoice covering all fees including third-party providers.

## Communication with SPE Provider

If the SPE is managed directly by the HDAB, all communication goes through the HDAB. If operated by a third-party provider: data governance/supervision communication goes through the HDAB; technical/access communication may be direct with the provider. The single invoice principle applies regardless.

## Getting Access

Access is granted only to individuals named in the data permit. The process includes: enrolment and identification, login credentials with strong password policies (NIST-based), **multifactor authentication (MFA)**, and continuous monitoring/logging. Any change to authorised users requires a formal permit amendment (Article 68(13)). Access is denied to persons not named in the permit, whose identity cannot be verified, or whose credentials have expired.

## Analysing Data Within the SPE

SPEs offer pre-approved analytical tools (R, Python, STATA). Users may request additional software installations (no admin rights). Users may only conduct analyses authorised in the data permit. Federated analysis is possible subject to HDAB oversight. Only anonymised, aggregate results may be exported after HDAB validation (Article 74(2)). Users must not circumvent security features; all activities are logged and audited. Collaboration platforms (Slack, Teams) may not be allowed.

## Data Controller Accountability

Under Article 74(1), the **data user is the data controller** for analysis conducted within the SPE, but only within the scope of the data permit. The regulation determines many purposes and means of processing, limiting the user-controller's discretion. The user is responsible for GDPR/EHDS compliance, purpose limitation, and data minimisation. SPE operators may act as processors (Article 28(3) GDPR). Joint controllership requires a joint controllership agreement (Article 26 GDPR).

## Rule Violations

Prohibited actions (Articles 54, 61): using data for detrimental decisions (insurance, employment, banking), advertising/marketing, developing harmful products, re-identification attempts, providing access to unauthorised third parties. Non-compliance may result in: revocation of the data permit, administrative sanctions under EHDS, GDPR penalties, and legal/criminal action under national law. Data users must immediately report breaches to the HDAB. HDAB must inform supervisory authorities of possible GDPR breaches.

## After Completing Data Analysis

Only anonymised, non-personal results in statistical format may be exported after HDAB verification (Article 74(2)). Reduced-capacity archiving within the SPE may be available for reproducibility during the permit period. Data permits are granted for up to 10 years, extendable once for up to an additional 10 years (Article 68(12)). Data must be deleted within six months of permit expiry; processing scripts may be retained by the HDAB. HDABs must publish information on access applications and permits (Article 72). Data users must publish results and inform the HDAB of significant findings (D8.4).

## Related

[[HDAB_Approval]] [[Pseudonymisation_Anonymisation]] [[Opt_Out_Mechanism]] [[Significant_Findings_Notification]] [[Data_Holder_Obligations]]
