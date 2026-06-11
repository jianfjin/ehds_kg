---
wiki_id: "WIKI-SFN-001"
title: "Significant Findings Notification"
regulation: "Reg. (EU) 2025/327"
article: "58, 61, 94"
category: "secondary_use"
keywords: ["significant findings", "incidental findings", "notification obligation", "HDAB", "data user", "data holder", "Article 58(3)", "Article 61(5)", "Recital 67", "right not to be informed", "clinical significance", "re-identification", "EHDS", "TEHDAS2", "D8.2"]
index_refs: ["EHDS-2025-327-A58", "EHDS-2025-327-A61"]
anchors: ["A58-P3", "A58-P4", "A61-P5"]
created: "2026-05-12"
updated: "2026-06-11"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/d8.2-guideline-for-health-data-access-bodies-on-implementing-the-obligation-of-notifying-the-natural-person-on-a-significant-finding-from-the-secondary-use-of-health-data.pdf"]
---

# Significant_Findings_Notification

**TEHDAS2 — D8.2 Guideline for Health Data Access Bodies on implementing the obligation of notifying the natural person on a significant finding from the secondary use of health data, 24 March 2026 (final version)**

The EHDS Regulation establishes an obligation to notify natural persons when significant health-related findings are discovered during secondary use of identifiable electronic health data. The HDAB serves solely as a procedural intermediary — not a clinical decision-maker.

## Definition and Terminology

The EHDS Regulation does not provide a formal legal definition of "significant findings." The guideline offers a working interpretation: **new information relevant to an identifiable individual that may carry potential clinical importance** — typically novel, potentially actionable, and capable of informing diagnosis, treatment, preventive strategies, or follow-up care.

### Key Distinctions
- **Incidental findings**: Unexpected observations unrelated to the original research purpose. May or may not be clinically relevant.
- **Clinically significant findings**: Observations with direct impact on patient care, diagnosis, treatment, or prognosis. These influence patient management, treatment options, or health outcomes.

If a dataset is selected based on predefined conditions (e.g., BRCA1/BRCA2 mutation), mere reconfirmation does NOT constitute a significant finding. New, previously unknown clinically relevant information may qualify. The EHDS does **not** impose an obligation to actively search for findings beyond the authorised analytical scope (Article 61(5)).

## Legal Framework

- **Article 61(5)**: Data users shall inform the HDAB of any significant finding related to the health of a natural person whose data are included in the dataset.
- **Article 58(3)**: The HDAB must transmit the finding securely to the relevant health data holder. The HDAB is NOT authorised to interpret, validate, or assess clinical relevance, nor to inform the individual directly.
- **Article 58(4)**: The responsibility to decide whether, how, and when to inform the individual rests with the health data holder, following national law.
- **Recital 67**: Natural persons should be informed by health data holders about significant findings. They have the right to request NOT to be informed. Member States may delay communication until a health professional can explain.
- **Article 94(2)(c)**: The EHDS Board may develop guidelines to help data users determine clinical significance.

### Identifiability Requirement
The rules apply only if individuals can be identified — directly (personal identifiers) or indirectly (via pseudonymisation key). If re-identification is not possible (truly anonymised data), obligations cannot be operationalised.

## Notification Chain (4-Step Process)

```
Data User → HDAB → Data Holder → Natural Person / Treating Health Professional
```

**Step 1 — Data User Identification**: Data users identify potentially significant findings during authorised secondary use. Assessment is based on national legal/ethical rules, medical guidelines, and future EHDS Board guidance (Article 94(2)(c)). The obligation applies only when findings emerge within the permitted analytical context — not from systematic screening for unrelated conditions.

**Step 2 — HDAB Transmission**: HDAB's role is strictly procedural: receive notification, transmit securely and without delay to the appropriate health data holder. The HDAB does NOT clinically validate or interpret findings. Member States may define additional procedural tasks (e.g., verifying formal criteria). For multi-holder datasets, the HDAB sorts and communicates transparently with data holders.

**Step 3 — Data Holder Assessment**: The data holder assesses clinical significance on the individual's future care, decides whether communication is warranted, involves the treating healthcare professional if needed, and applies appropriate method/timing (under national law).

**Step 4 — Notification to Individual**: Where permitted/required under national law, the individual is informed clearly and understandably — unless they have exercised the right not to be informed. The EHDS process ends with the data holder's obligation; further care provision falls outside EHDS scope.

## Typical Examples (Section 5.2, non-exhaustive)

- **Genetic/Genomic**: BRCA1/BRCA2 mutations (hereditary cancer risk), clinically relevant variants for cardiovascular conditions or inherited metabolic disorders.
- **Laboratory**: Pathological parameters newly recognised as clinically relevant (e.g., markers linked to preeclampsia progression).
- **Radiological**: Lung nodules on chest X-ray/CT suggesting early-stage lung cancer (may include false positives/negatives).

Examples are illustrative and non-binding. Classification depends on analytical context, dataset characteristics, and applicable national frameworks.

## Right Not to Be Informed (Section 5.3, 8.3, 8.4)

Every natural person has the right to request not to be informed of significant findings (Recital 67, Article 58(3)). Procedures are determined exclusively at Member State level. HDABs may maintain a register of such requests, or this may be handled by data holders. National rules should clarify whether a general opt-out from secondary use (Article 71) implies refusal to receive significant findings, or whether these preferences are registered separately.

## HDAB Responsibilities (Chapter 8)

| Area | HDAB Obligations |
|------|------------------|
| **Notification from data users (8.1)** | Receive and transmit to the relevant data holder in line with Article 58(3). |
| **Measures towards data holders (8.2)** | Collaborate with original data holders to facilitate appropriate transmission. The obligation is fulfilled once securely transmitted. |
| **Preference management (8.3, 8.4)** | Maintain or coordinate register of requests not to be informed. |
| **Track record (8.5)** | Maintain comprehensive records of notifications to support transparency and traceability. |
| **Privacy aspects (8.6)** | Ensure GDPR compliance — purpose limitation, data minimisation, confidentiality (Article 5(1)(b),(c),(f)). HDABs must not access/interpret medical information beyond what is necessary for transmission. |
| **Re-identification** | HDABs do NOT re-identify individuals. Any re-identification occurs within secure, legally established frameworks, under the responsibility of the data holder or a Trusted Third Party (TTP). |

## Cross-Border Considerations

When a data user operates under a multi-country data permit and identifies a significant finding concerning a data subject from another Member State, coordination between involved HDABs is needed. Guiding principles: privacy protection, accountability of each actor, interoperability, and transparency. The cross-border notification scheme (Figure 2 in the guideline) shows a representative scenario involving a data user in EU MS1, a data subject in EU MS2, and a data holder in EU MS2.

## National-Level Policy Decisions (Section 8.7 — Checklist)

The guideline provides a comprehensive non-binding checklist of issues Member States should address:
- Governance frameworks and SOPs for handling significant findings.
- National criteria/categories for identifying significant findings.
- Clear allocation of responsibilities between HDABs, data users, data holders, and treating clinicians.
- Communication pathways, especially where the data holder lacks a therapeutic relationship.
- Management of the right not to be informed.
- Rules for re-identification, including TTP involvement.
- Data quality and provenance considerations.
- Cross-border coordination mechanisms.
- Equity and capacity-building across different organisations.

## Pitfalls

- HDABs must not overstep into clinical validation — their role is strictly procedural (Article 58(3)).
- Over-notification of non-actionable findings can cause distress.
- Pseudonymised data still triggers obligations if re-identification is possible.
- National fragmentation in defining "significant findings" may lead to inconsistent protection.
- Data holders without a therapeutic relationship (e.g., population registries) face unique challenges in communicating findings.
- The guideline is **not legally binding** — it is an expert opinion document reflecting TEHDAS2 project partner input.

## Related

[[Opt_Out_Mechanism]] [[HDAB_Approval]] [[Data_Holder_Obligations]] [[Pseudonymisation_Anonymisation]] [[On_How_To_Use_Data_In_A_Secure_Processin]]
