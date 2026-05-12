---
wiki_id: "WIKI-MC-001"
title: "HDAB Minimum Categories and Limitations on Reuse"
regulation: "Reg. (EU) 2025/327"
article: "52, 53, 54"
category: "secondary_use"
keywords: ["minimum categories", "allowed purposes", "prohibited use", "Article 53", "Article 54", "secondary use assessment", "HDAB"]
index_refs: ["EHDS-2025-327-A53", "EHDS-2025-327-A54", "EHDS-2025-327-A52"]
anchors: ["A53-P1", "A54-P1"]
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-guideline-for-health-data-access-bodies-on-minimum-categories-and-limitations-on-the-reuse-of-health-data.pdf"]
---

# HDAB_Minimum_Categories

## Definition

The TEHDAS2 M5.2 Draft Guideline defines the framework for HDABs to assess whether a secondary use application falls within the six **allowed purposes** under Article 53 or breaches the five **prohibited uses** under Article 54 of the EHDS Regulation. It also addresses Article 52(3) limitations on data availability due to intellectual property rights (IPR) and trade secrets.

Articles 53 and 54 must be **read together**: an HDAB must conclude not only that the purpose matches Article 53(1)(a)–(f) but also that nothing in the application indicates an infringement of Article 54 prohibitions.

## Six Allowed Purposes — Article 53(1)

### (a) Public Interest in Public/Occupational Health (public sector only)
Restricted to public sector bodies (Article 53(2)). Covers activities such as health surveillance, disease monitoring, and evaluating public health interventions. *Recital 58*: "public interest" should be interpreted broadly — not limited to emergency responses.

**Key checks:**
- Verify legal status/mandate of applicant as public sector body (EU Data Governance Act, Art. 2(17))
- Confirm mandate scope explicitly covers public health tasks
- International organisations are NOT eligible by default; must act through a public authority mandate

### (b) Policymaking and Regulatory Activities (public sector only)
Covers activities of public sector bodies and Union institutions in health/care sectors carrying out tasks defined in their mandates. Examples: regulatory authorities monitoring drug safety, health technology assessment (HTA) bodies, health inspectorates.

**Key checks:**
- Applicant must show explicit legal basis (relevant legislation assigning the task)
- The mandate must cover the specific regulatory activity, not just general affiliation

### (c) Statistics (public sector only)
Limited to national, multi-national and EU-level official statistics under the European Statistical System (ESS). Definition: "quantitative and qualitative, aggregated and representative information characterising a collective phenomenon in a given population" (Reg. 223/2009, Art. 3(1)).

**Key checks:**
- Only entities legally mandated to produce official statistics can invoke this purpose
- Other public bodies doing analytical work should apply under (b) or (e)
- Data must be health- or care-related

### (d) Education or Teaching Activities
Applies to vocational or higher education in health or care sectors. Covers formal educational activities (medicine, nursing, pharmacy, biomedical informatics, public health, social care).

**Key checks:**
- Distinguish from scientific research — a thesis may fall under (e) rather than (d)
- Digital health tool training only qualifies if part of a formal curriculum
- Focus is on purpose of activity, not status of applicant

### (e) Scientific Research
Broad interpretation (Recital 61), including both publicly and privately funded projects. Must contribute to public health or HTA, or ensure high levels of quality/safety of healthcare, medicinal products, or medical devices.

**Key checks:**
- Require research plan, funding evidence, ethics approval (if needed)
- Assess scope, methodology and aims against stated purpose
- HDABs should have access to scientific expertise/advisory boards
- Studies on non-medical products fall under (e) if intended to benefit patients

### (f) Improvement of Healthcare Delivery
Covers personalised medicine (treatments tailored from population-level insights) and system-level improvements (workflow optimisation, resource planning, evaluating care models). Any applicant may apply, but must show targeted care improvement, not general innovation.

**Key checks:**
- Verify direct link to healthcare provider or public health authority
- Proof that project outputs will be integrated into care pathways
- Clinical staff involvement in study or implementation phase

## Five Prohibited Uses — Article 54

### (a) Decisions Detrimental to Individuals or Groups
Prohibits taking decisions producing legal, social or economic effects based on health data. Broader than GDPR Art. 22 — covers automated, semi-automated, AND manual decisions.

**Red flags:** Risk-scoring tools with individual consequences, automated profiling for insurance/service eligibility, AI systems producing binding clinical decisions without human oversight.

### (b) Discriminatory Decisions
Prohibits decisions on job offers, insurance/credit terms, or any discrimination based on health data. Linked to EU Charter of Fundamental Rights Art. 21.

**Red flags:** Segmenting individuals by health status in pricing models, service offers, or recruitment filters.

### (c) Advertising or Marketing Activities
Prohibits all advertising/marketing directed at any audience (shift from original proposal which only covered health professionals). "Marketing" = overall strategy; "Advertising" = promotional subset (Directive 2006/114/EC).

**Red flags:** Pharmaceutical companies using data for targeted marketing campaigns. Distinguish from legitimate research that may eventually yield commercial products — the key is whether the data use itself is promotional.

### (d) Developing Harmful Products or Services
Prohibits developing products/services that may cause harm to individuals, public health, or societies at large.

### (e) Ethical Provisions Under National Law
Prohibits uses that violate ethical provisions established by national law, even if they would otherwise fall under an allowed purpose.

## IPR and Trade Secrets — Article 52(3)

HDABs must ensure adequate safeguards to preserve confidentiality of IPR. If safeguards are insufficient to protect IPR or trade secrets, the HDAB may reject the permit application (Article 52(5)). This is relevant when a lawful purpose cannot be implemented due to unresolved IPR concerns.

## Concepts Defined in EU Legal Acts

Several core concepts in Article 53 are already defined in EU legislation, providing a common legal baseline for HDAB assessments:

| Concept | Legal Source |
|----------|-------------|
| **Healthcare** | Directive 2011/24/EU, Art. 3(a) |
| **Medicinal Product** | Directive 2001/83/EC, Art. 1(2) |
| **Medical Device** | Regulations (EU) 2017/745 and 2017/746, Art. 2(1) |
| **AI Systems** | AI Act — Regulation (EU) 2024/1689, Art. 3(1) |
| **Health Technology Assessment** | Regulation (EU) 2021/2282, Art. 2(5) |
| **Public Sector Body** | Data Governance Act — Regulation (EU) 2022/868, Art. 2(17) |
| **Statistics** | Regulation (EU) 223/2009, Art. 3(1) |
| **Serious Cross-Border Threats** | Regulation (EU) 2022/2371, Art. 2(1) |

**Development Activities:** The concept is partially defined in Directive 2009/81/EC, Art. 1(27): "all activities comprising fundamental research, applied research and experimental development, where the latter may include the realisation of technological demonstrators."

## Public Interest — Cross-Recital Analysis

The concept of "public interest" permeates the EHDS Regulation. Key references include:

| Recital/Article | Scope |
|-----------------|-------|
| **Recital 52** | Assigns public interest tasks to HDABs per GDPR Art. 6(1)(e) and 9(2)(g–j) |
| **Recital 54** | Specifies public interest includes: protection against serious cross-border health threats, scientific research for important reasons of public interest (unmet medical needs, rare diseases, emerging health threats) |
| **Recital 58** | Public interest should be interpreted broadly — not limited to emergency responses |
| **Recital 61** | Secondary use should benefit society through new medicines, devices, healthcare products at affordable prices, enhancing access across all Member States |
| **Article 71(4)** | Opt-out override possible for public sector bodies where data cannot be obtained by alternative means and serves public interest purposes under Art. 53(1)(a–c) |
| **Article 55(5)** | HDABs must remain free of conflicts of interest, act independently, and serve the public interest |

These cross-references establish that "public interest" is not an open-ended justification — it must be grounded in specific tasks contributing to public health, healthcare quality/safety, or scientific advancement benefiting society.

## Practical Examples

- **Example 1:** A national health research institute applies for public health surveillance → must provide national law establishing its role in public health monitoring
- **Example 2:** A clinician wants data from across Europe to improve treatment of a rare disease → falls under (f) improvement of healthcare
- **Example 3:** A pharmaceutical company requests ATC code data per hospital to identify where prescriptions are low → HDAB should scrutinise for marketing intent under (c)
- **Example 4:** A clinic head compares treatment outcomes with other clinics to improve care delivery, no research protocol → (f), not (e)

## Pitfalls

1. **Blurring research and marketing:** Commercial actors may have mixed motives. Focus on immediate purpose of data use, not eventual profit.
2. **Overly broad public interest:** Not every public body activity qualifies — the mandate must explicitly cover the stated purpose.
3. **Statistics confusion:** Only bodies with a formal statistical mandate can use purpose (c); others must use (b) or (e).
4. **Education vs research overlap:** A PhD project may qualify under (e) even if conducted in an educational setting.

## Related
[[Data_Access_Procedures]] [[EHDS_Penalties]] [[HDAB_Approval]] [[Purpose_Scientific]]
