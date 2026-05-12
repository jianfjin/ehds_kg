---
wiki_id: "WIKI-SFN-001"
title: "Significant Findings Notification"
regulation: "Reg. (EU) 2025/327"
article: "58, 61, 94"
category: "secondary_use"
keywords: ["significant findings", "incidental findings", "notification obligation", "HDAB", "data user", "data holder", "Article 58(3)", "Article 61(5)", "Recital 67", "right not to be informed", "clinical significance"]
index_refs: ["EHDS-2025-327-A58", "EHDS-2025-327-A61"]
anchors: ["A58-P3", "A58-P4", "A61-P5"]
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-guideline-to-health-data-access-bodies-on-implementing-the-obligation-of-notifying-the-natural-person-on-a-significant-finding-from-the-secondary-use-of-health-data.pdf"]
---

# Significant_Findings_Notification

The EHDS Regulation establishes an obligation to notify natural persons when significant health-related findings are discovered during secondary use of identifiable electronic health data. The HDAB serves as a procedural intermediary, not a clinical decision-maker.

## Definition

The EHDS Regulation does not provide a formal legal definition of "significant findings." The TEHDAS2 guideline offers a working interpretation: **new information that is relevant to an identifiable individual and may carry potential clinical importance** — typically novel, potentially actionable, and capable of informing diagnosis, treatment decisions, preventive strategies, or follow-up care.

### Distinction from Incidental Findings
- **Incidental Findings**: Unexpected observations during a diagnostic test or research study, unrelated to the primary reason for the test. May or may not be clinically relevant.
- **Clinically Significant Findings**: Observations that have a **direct impact** on patient care, diagnosis, treatment, or prognosis. Must influence patient management, treatment options, or health outcomes.

Important: A new result from secondary use does not automatically imply clinical significance. If a dataset is selected based on predefined conditions (e.g., BRCA1/BRCA2 mutation), the mere reconfirmation of those conditions does NOT constitute a significant finding. The emergence of new, previously unknown clinically relevant information may qualify.

## Legal Framework

### Core Provisions
- **Art. 61(5)**: Data users shall inform the HDAB of any significant finding related to the health of a natural person whose data are included in the dataset.
- **Art. 58(3)**: Upon receiving notification, the HDAB must transmit the finding securely to the relevant health data holder. The HDAB is NOT authorised to interpret, validate, or assess clinical relevance, nor to directly inform the individual.
- **Art. 58(4)**: The responsibility to decide whether, how, and when to inform the individual or their treating health professional rests with the health data holder, following national laws.
- **Recital 67**: Natural persons should be informed by health data holders about significant findings. They have the right to request NOT to be informed. Member States may delay communication until a health professional can explain.

### Key Principle: Identifiability Required
The rules on significant findings only apply if individuals can be identified — either directly (personal identifiers) or indirectly (via pseudonymisation with a key). If re-identification is not possible (truly anonymised data), the obligations concerning significant findings cannot be applied (consistent with Art. 11 GDPR).

## Notification Chain (4-Step Process)

```
Data User → HDAB → Data Holder → Natural Person / Treating Health Professional
```

### Step 1: Identification by Data User
Data users (researchers) identify potentially significant findings during secondary use. Assessment of impact is based on national legal/ethical rules, medical guidelines, and future EHDS Board guidance (Art. 94(2)(c)). The data user reports to the relevant HDAB.

### Step 2: HDAB Transmission
HDAB's role is strictly procedural:
- Receive notification from data user.
- Transmit securely and without delay to the appropriate data holder.
- HDAB does NOT clinically validate or interpret findings.
- Member States may assign additional procedural tasks (e.g., verifying notification meets formal criteria).

### Step 3: Data Holder Assessment
The data holder:
- Assesses clinical significance on the individual patient's future care.
- Decides whether communication to the natural person is warranted.
- Involves treating healthcare professional if needed.
- Applies appropriate method and timing for communication (under national law).
- May delay communication until a health professional can explain (Recital 67).

### Step 4: Notification to Individual
Where permitted/required under national legislation, the individual is informed in a clear and understandable manner — unless they have exercised the right not to be informed. The EHDS process ends here; further care provision falls outside EHDS scope.

## Typical Examples of Significant Findings

- **Genetic/Genomic**: BRCA1/BRCA2 mutations indicating hereditary cancer risk; clinically relevant variants from exome/genome sequencing related to cardiovascular conditions or inherited metabolic disorders.
- **Laboratory**: Pathological parameters newly recognised as clinically relevant (e.g., markers linked to preeclampsia progression).
- **Radiological**: Lung nodules on routine chest X-ray/CT suggesting early-stage lung cancer. Note: preliminary findings may include false positives/negatives.

All examples are illustrative. Decisions to act must follow national law and medical judgment.

## Right Not to Be Informed

Every natural person has the right to request not to be informed of significant findings. Procedures for exercising this right are determined exclusively at Member State level. HDABs should maintain a register of natural persons' requests not to be informed.

## Cross-Border Transmission

When a data user operates under a multi-country data permit and identifies a significant finding concerning a data subject from a different Member State, coordination mechanisms between the involved HDABs are needed. The guideline recommends:
- Privacy protection through strict data protection and confidentiality compliance.
- Accountability by each actor in the chain.
- Interoperability of systems and procedures across Member States.
- Transparency so natural persons can obtain information on how their data is used.

## HDAB Specific Responsibilities

- Collaborate with original data holders to facilitate appropriate transmission.
- Maintain a track record of notifications from/to data users/data holders.
- Ensure privacy aspects are respected throughout the process.
- Do NOT communicate directly with patients — this is the data holder's domain.

## Issues Left to Member States

- Criteria, categories, and procedures for identifying significant findings at national level.
- How and when individuals are informed.
- Regulation of the right not to be informed.
- Secure data-sharing pathways and clinical follow-up procedures.
- Cross-border coordination mechanisms.

## Pitfalls

- Over-notification of non-actionable or uncertain findings can cause distress and burden individuals.
- HDABs must not overstep into clinical validation — their role is strictly procedural.
- Pseudonymised data still triggers significant findings obligations if re-identification is possible.
- National fragmentation in defining "significant findings" may lead to inconsistent protection across Member States.

## Related

[[Opt_Out_Mechanism]] [[HDAB_Approval]] [[Data_Holder_Obligations]] [[Pseudonymisation_Anonymisation]]
