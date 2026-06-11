---
wiki_id: "WIKI-OUT-001"
title: "Opt-Out Mechanism for Secondary Use"
regulation: "Reg. (EU) 2025/327"
article: "71, 58, 10, 65"
category: "secondary_use"
keywords: ["opt-out", "Article 71", "data subject rights", "HDAB", "secondary use", "GDPR right to object", "opt-out registry", "granular opt-out", "citizen engagement", "Article 71(4) exceptions", "EHDS", "TEHDAS2", "D8.1", "sui generis right"]
index_refs: ["EHDS-2025-327-A71", "EHDS-2025-327-A58", "EHDS-2025-327-A65"]
anchors: ["A71-P1", "A71-P2", "A71-P3", "A71-P4", "A71-P8"]
created: "2026-05-12"
updated: "2026-06-11"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/d8.1-guideline-for-health-data-access-bodies-on-implementing-opt-out-from-the-secondary-use-of-health-data.pdf"]
---

# Opt_Out_Mechanism

**TEHDAS2 — D8.1 Guideline for Health Data Access Bodies on implementing opt-out from the secondary use of health data, 24 March 2026 (final version)**

The EHDS Regulation establishes a Union-wide right for natural persons to opt out from secondary use of their personal electronic health data under Article 71. Member States implement the mechanism nationally. This guideline provides implementation guidance for HDABs, covering the scope, procedures, granularity, citizen engagement, and enforcement of the opt-out right.

## Definition and Legal Framework

Article 71(1) EHDS: Natural persons have the right to opt out at any time, without providing any reason, from the processing of their personal electronic health data for secondary use. The right is **reversible**. Key characteristics: unconditional (no justification required), reversible at any time (affects future permits only, Article 71(6)), and time-unlimited.

The EHDS opt-out is a **sui generis right** — a new, standalone right created by the EHDS Regulation, independent of GDPR legal bases. It is distinct from the GDPR right to object (Article 21 GDPR), which requires justification and can be overridden. The EHDS opt-out cannot be overridden by the controller, except under the narrow exceptions of Article 71(4).

### Distinction from Primary Use Opt-Out (Article 10)

Primary use opt-out (Article 10) is **optional** for Member States. Secondary use opt-out (Article 71) is **mandatory**. The two are independent: exercising one does not affect the other. There is no automatic link between opting out in primary or secondary use. The right to restrict access under Article 8 also does not block secondary use — a separate opt-out under Article 71 is needed.

### Relationship with GDPR

The GDPR continues to apply fully. The EHDS opt-out complements, not replaces, GDPR rights. The GDPR right to object (Article 21) and the EHDS opt-out are cumulative and independent — exercising one does not trigger the other. Under Article 65 EHDS, GDPR supervisory authorities monitor and enforce the opt-out right, including handling complaints and imposing administrative fines.

## Data and Identifiability

The opt-out applies to personal electronic health data categories listed in Article 51: EHR data, administrative health data, disease registries, genomic data, medical device data, person-generated data, etc. **Anonymised data** falls outside scope (Article 71(8)). The opt-out applies to pseudonymised data only when the entity responsible for implementing the opt-out can identify or re-identify the natural person.

Crucially, the opt-out applies to **the entire chain of processing** for secondary use, including anonymisation and pseudonymisation steps that process personal data. Data holders are not obliged to maintain, acquire, or process additional information solely to identify data subjects for opt-out compliance (Article 71(8), mirroring Article 11 GDPR).

## Exceptions — Article 71(4)

Member States may adopt national laws allowing access to opted-out data if **three cumulative conditions** are met:
1. Request by a public sector body or Union institution (Article 53(1)(a)-(c)) or for important public interest scientific research.
2. Data cannot be obtained by alternative means in a timely and effective manner.
3. Sufficient justification provided by the applicant.

Safeguards include prohibition of re-identification (Article 61(3)), use of SPEs (Chapter IV), and necessity/proportionality (Article 71(5)-(6)). Member States must notify the European Commission of any national override provisions.

## Granularity

Member States may implement granular opt-out mechanisms (by data type, purpose, or data holder), but are not obliged to. Recommended levels: full opt-out, per data type (genomic, imaging), per data holder (cohorts, biobanks, EHR), or per purpose (research, innovation, policy). The guideline warns against excessive granularity causing administrative burden and decision fatigue. A balanced citizen-centred approach is recommended. Opt-outs do not propagate automatically across borders — citizens may need to submit opt-outs in each relevant Member State.

## Implementation Architecture

### Declaration Channels (5.4.1)
- Online portal (co-located with national EHR or hosted by HDAB).
- Via healthcare providers or data holders.
- Government office one-stop shops.
- Non-digital alternatives for limited digital literacy.
- Must comply with accessibility standards (WCAG 2.1+).

### Opt-Out Registries and Enforcement (5.4.2)
Member States may implement centralised or decentralised systems. The guideline does not prescribe a single centralised register. Key requirements: data minimisation, immediate confirmation to the individual, timestamped logging, access strictly limited to authorised entities with logging and oversight. Two lines of defence: **data holder level** (prevent transfer of opted-out data) and **dataset level** (filtering during HDAB dataset preparation).

## Actor Responsibilities (Table 3)

| Actor | Key Responsibilities |
|-------|---------------------|
| **Natural Person** | Exercises/reverses opt-out without reasons. |
| **Data Holder** | Applies data minimisation, respects opt-out granularity, excludes opted-out individuals from new permits (Articles 57, 61). |
| **HDAB** | Publishes clear information, logs data access, screens datasets to filter opted-out individuals, evaluates exceptions, cooperates with supervisory authorities (Articles 58, 65). |
| **Data User** | Complies with data permits, respects opt-out restrictions, cannot re-identify. |
| **Member State** | Establishes accessible, understandable, reversible opt-out mechanism; defines national exceptions (Article 71(4)). |
| **Supervisory Authority** | Monitors and enforces opt-out compliance (Article 65). |

## Citizen Engagement

HDABs should provide clear, balanced information about the societal benefits of secondary use while maintaining value-neutrality. Communication should avoid implying that better understanding should lead to fewer opt-outs. Key elements: plain-language explanations, multiple communication channels, accessibility for vulnerable groups (older adults, persons with disabilities, low literacy). Member States should invest in digital health literacy, co-design materials with patient/citizen representatives, and establish stakeholder cooperation under Articles 57 and 93 (EHDS Stakeholder Forum). HDABs must publish information on data uses, permits, and outcomes (Article 58(1)).

## Pitfalls

- Centralised opt-out registries create sensitive datasets requiring strong data protection.
- Granular opt-out can inadvertently resemble consent-based logic, undermining the EHDS framework.
- National fragmentation undermines cross-border data access and creates citizen confusion.
- EHR-level access restrictions (Article 8) do NOT block secondary use.
- The guideline is **not legally binding** — it is an expert opinion document developed within the TEHDAS2 framework.

## Related

[[On_How_To_Use_Data_In_A_Secure_Processin]] [[HDAB_Approval]] [[Data_Holder_Obligations]] [[Pseudonymisation_Anonymisation]] [[Significant_Findings_Notification]]
