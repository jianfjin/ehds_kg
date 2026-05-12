# EHDS Secondary Use Rules (Symbolic KB)
## Core Constraints
- RULE_01: [Data Access Body (HDAB)] -> MUST_APPROVE -> [All Secondary Use Requests]
- RULE_02: [Purpose] -> MUST_BE -> [Public Interest / Scientific Research / Public Health]
- RULE_03: [Purpose] -> MUST_NOT_BE -> [Commercial Marketing / Insurance Underwriting]
- RULE_04: [Data Minimization] -> REQUIRE -> [Anonymization/Pseudonymization] -> [Prior to Release]
- RULE_05: [Cross-Border] -> REQUIRE -> [Adequacy Decision] OR [Standard Contractual Clauses]
- RULE_06: [Data Linkage] -> MUST_REQUEST -> [Explicit HDAB Approval Art.68(1)(b)] AND [Pre-Access Management]
- RULE_07: [External Enrichment w/ Record-Level Match] -> TREAT_AS -> [Data Linkage] -> REQUIRES -> [Separate Approval]

## Data Linkage Specifics
- Data linkage is a **pre-access, centralized process** managed by HDAB or data holder (Art.68)
- Record-level matching across datasets requires **explicit request** in data access application
- Only the **final linked dataset** is provided to user (never raw unlinked records)
- Distinguish from **data enrichment**: enrichment is post-access, user-driven, analytical
- If enrichment involves person-level joins → it's treated as **linkage** for governance

## High-Risk Keywords (Lure for the Auditor)
- "Broadly defined research": HIGH_RISK -> Violation of Rule_02
- "Marketing optimization": CRITICAL_RISK -> Violation of Rule_03
- "Full dataset access": HIGH_RISK -> Violation of Rule_04
- "Cross-referencing patient records without HDAB approval": CRITICAL_RISK -> Violation of Rule_06
- "Record-level join across data permits": CRITICAL_RISK -> Violation of Rule_07
