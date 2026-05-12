---
wiki_id: "WIKI-PA-001"
title: "Pseudonymisation, Anonymisation and Synthetic Data"
regulation: "Reg. (EU) 2025/327"
article: "66, 67, 68, 73"
category: "secondary_use"
keywords: ["pseudonymisation", "anonymisation", "synthetic data", "data minimisation", "re-identification risk", "quasi-identifiers", "differential privacy", "Article 67", "SPE", "GDPR Recital 26"]
index_refs: ["EHDS-2025-327-A66", "EHDS-2025-327-A67", "EHDS-2025-327-A68"]
anchors: ["A66-P3", "A67-P1", "A67-P2", "A67-P3", "A68-P1c"]
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-guideline-on-data-minimisation-pseudonymisation-anonymisation-and-synthetic-data.pdf"]
---

# Pseudonymisation_Anonymisation

The EHDS Regulation and GDPR require health data to be processed with appropriate minimisation, pseudonymisation, or anonymisation measures depending on purpose and context. All categories of data processed must be subject to these measures (Art. 66(3) EHDS).

## Data Minimisation Foundation

Data minimisation (GDPR Art. 5(1)(c)) requires that personal data be "adequate, relevant and limited to what is necessary." In the EHDS context, it applies throughout the entire data lifecycle:
- During data collection and preparation by the data holder.
- When assessing the data request/access application (by HDAB).
- During use and processing by the data user, including export of results from the SPE.

### Five Dimensions of Data Minimisation

The guideline introduces a practical framework of five dimensions for scoping data provision:

1. **Who** — Study population. Inclusion/exclusion criteria define which individuals' data is needed. Avoid strong quasi-identifiers like date of birth; use age groups/year of birth instead. Combinations like "date of birth + sex + postcode" must be avoided.

2. **What** — Research variables. Only request variables necessary for study objectives. Distinguish between study-specific variables and control/confounding variables. Genetic data, rare disease codes, and medical images require special attention as they may act as quasi-identifiers.

3. **When** — Timeframe. Specify calendar periods or relative timeframes aligned with study purposes. Date-level granularity dramatically increases privacy risk — prefer year or month when possible. Hospital admission/discharge dates are particularly sensitive quasi-identifiers.

4. **Where** — Geographical perimeter. Limit to locations relevant for study purposes. Geographical data combined with other variables significantly increases re-identification risk.

5. **How** — Extraction methods. Define sampling strategies, data transformation approaches, and any pre-defined granularity levels offered by data holders.

### Risk Mitigation Techniques for Quasi-Identifiers

- **Generalisation**: Reduce detail level (e.g., age brackets instead of exact age; income ranges instead of exact values).
- **Suppression**: Remove or hide specific cell values (e.g., extreme lab test values; small cell counts for rare diseases).
- **Randomisation**: Add calibrated noise (more common in anonymisation than pseudonymisation under EHDS, which prioritises data fidelity).

## Pseudonymisation

### Concept
Pseudonymisation replaces direct identifying information (names, social security numbers) with pseudonyms. The "additional information" needed to link pseudonyms back to individuals is kept **entirely separate and secure**.

### When to Apply
Pseudonymisation should be performed **as early as possible** in the data journey. Re-pseudonymisation must occur before data provision into the SPE. The HDAB defines and oversees the pseudonymisation process.

### Key Requirements
- Pseudonymised data must not contain direct identifiers (stored separately as "additional information").
- Quasi-identifiers may remain but must be risk-mitigated through generalisation, suppression, or randomisation.
- HDABs decide whether anonymised or pseudonymised data format is appropriate (Art. 68(1)(c)) — pseudonymised format is permitted only if re-identification risk is justified and appropriately mitigated (Art. 66(3)).
- The HDAB and data user share responsibility for preventing re-identification (Recital 72 EHDS: data users shall refrain from any re-identification attempt).

### Value of Pseudonymisation
- Enables **record linkage** across datasets from different sources or countries without revealing direct identity — vital for comprehensive research.
- Supports data subject rights: opt-out from future projects, notification of significant findings.

## Anonymisation

### Legal Basis
Art. 67 EHDS: Where data are made available in anonymous format, the requirements of Arts. 54(2) and 59(1)(b) do not apply (simplified access pathway). Anonymisation must be carried out in accordance with implementing acts adopted pursuant to Art. 68. The HDAB must verify anonymisation techniques meet standards before making data available (Art. 67(3)).

### Definition (GDPR Recital 26)
Data are anonymised only if the data subject is **not identifiable by any means reasonably likely to be used**, taking into account objective factors: cost, time, and available technologies. Anonymisation is NOT a binary or permanent status — previously anonymised data may cease to meet conditions due to technological advances or the ability to combine multiple datasets.

### Key Principles
- HDABs must apply **tested state-of-the-art techniques** ensuring data processing preserves privacy (Recital 65 EHDS): generalisation, suppression, randomisation.
- Anonymisation transforms original personal data so it no longer relates to an identified or identifiable person.
- The HDAB must conduct privacy risk assessments (re-identification risk, attribute inference, membership inference, linkage attacks) before export.
- All anonymisation activities must be thoroughly documented for transparency and accountability.

### Use Cases
- Data intended for export from SPE (analysis results).
- Data to be made publicly available (open data).
- Data request responses (non-personal aggregated statistical format).

## Synthetic Data Generation

### Definition
Synthetic data generation creates **entirely new, artificial datasets** that mimic the statistical properties and relationships of original data without containing actual personal information. Distinct from anonymisation (which transforms real data).

### Regulatory Status
- The EHDS does **not impose legal obligations** regarding synthetic data generation.
- HDABs may support its use via evaluation frameworks as part of enabling responsible data access.
- EDPB (Opinion 28/2024): synthetic data may still fall under GDPR if individuals can be re-identified with reasonable effort — documentation must demonstrate theoretical resistance to re-identification techniques.
- Synthetic data generation must meet purpose and data minimisation principles.

### Techniques
- Generative Adversarial Networks (GANs)
- Variational Autoencoders (VAEs)
- Differential Privacy (DP) integration

### Use in EHDS
- May be used during processing of data requests to create data in anonymised statistical format.
- Can serve as basis for aggregated result exports.

## Data Types and Special Considerations

| Data Type | Special Risks |
|-----------|---------------|
| Structured (tabular) | Cross-classification of variables creates uniqueness; quasi-identifier combinations increase singling-out risk |
| Medical Imaging (DICOM) | May reveal unique body features acting as direct/quasi-identifiers; DICOM headers may contain patient IDs |
| Bio-signals (ECG, EEG) | Potential for re-identification through signal patterns |
| Genetic Data | Can act as direct/quasi-identifiers; classified as sensitive under Art. 9(1) GDPR; special safeguards apply |
| Textual/Unstructured | Difficult to manage attribute selection; may contain more background information than necessary; NER-based de-identification is less deterministic |
| Multimodal | Combines multiple media types, multiplying re-identification vectors |

## Controllership in the EHDS Data Flow

- **Data Holders**: Controllers for initial processing and provision to HDAB.
- **HDABs**: Controllers for processing within their tasks (data linkage, additional pseudonymisation, risk reduction, anonymisation, SPE upload).
- **Data Users**: Controllers for data made available in SPE, limited to permitted purposes.

## HDAB Verification and Documentation Requirements

- Verify anonymisation techniques meet Art. 67 standards before release (Art. 67(3)).
- Conduct privacy risk assessments covering re-identification, attribute inference, membership inference, and linkage attacks.
- Document anonymisation or synthetic data generation processes thoroughly.
- Approve result exports from SPE only after risk assessment.

## Pitfalls

- Anonymisation is not permanent — technological advances or dataset combinations may break anonymity over time.
- "Anonymised" data with residual quasi-identifiers may still allow singling-out or linkage attacks — continuous risk assessment is required.
- Non-deterministic techniques (randomisation, noise injection) can significantly reduce data utility — calibration is critical.
- Synthetic data that overfits the training data may inadvertently reproduce real individual records.
- Unstructured text data is particularly challenging to de-identify reliably compared to structured data.

## Related

[[Data_Minimization]] [[Data_Linkage]] [[Article_SecondaryUse]] [[Data_Holder_Obligations]] [[Opt_Out_Mechanism]]
