---
wiki_id: "WIKI-OUT-001"
title: "Opt-Out Mechanism for Secondary Use"
regulation: "Reg. (EU) 2025/327"
article: "71, 58, 10, 65"
category: "secondary_use"
keywords: ["opt-out", "Article 71", "data subject rights", "HDAB", "secondary use", "GDPR right to object", "opt-out registry", "granular opt-out", "citizen engagement", "Article 71(4) exceptions"]
index_refs: ["EHDS-2025-327-A71", "EHDS-2025-327-A58", "EHDS-2025-327-A65"]
anchors: ["A71-P1", "A71-P2", "A71-P3", "A71-P4", "A71-P8"]
created: "2026-05-12"
updated: "2026-05-12"
author: "CTO-FengGe"
confidence: "high"
sources: ["data/source_pdfs/draft-guideline-to-health-data-access-bodies-how-to-implement-opt-out-from-secondary-use-of-electronic-health-data.pdf"]
---

# Opt_Out_Mechanism

The EHDS Regulation establishes a Union-wide right for natural persons to opt out from the secondary use of their personal electronic health data, while delegating the practical implementation of the mechanism to Member States.

## Definition

Article 71(1) EHDS: "Natural persons shall have the right to opt out at any time, and without providing any reason, from the processing of personal electronic health data relating to them for secondary use under this Regulation. The exercise of that right shall be reversible."

Key characteristics:
- **Unconditional**: No justification required — the mere declaration is sufficient.
- **Reversible**: Can be revoked at any time; reversal applies only to data permits/requests authorised after the revocation (Art. 71(3)).
- **Time-unlimited**: No deadline to meet; exercisable at any moment.
- **Applies to personal electronic health data**: Both directly and indirectly identifiable data. Once data is fully anonymised before opt-out is exercised, it falls outside scope.

## Distinction from Other Rights

### vs. Primary Use Opt-Out (Art. 10)
- Art. 10 allows Member States the *option* to provide opt-out from primary use (healthcare) via national EHR systems.
- Secondary use opt-out under Art. 71 is *mandatory* for all Member States.
- The two mechanisms are distinct and independent — a natural person may exercise one without the other.

### vs. GDPR Right to Object (Art. 21 GDPR)
- GDPR Art. 21 requires the data subject to provide reasons relating to their "particular situation" and can be overridden by "compelling legitimate grounds" of the controller.
- EHDS opt-out requires **no justification** and **cannot be overridden** by the controller.
- The two rights are cumulative and independent — exercising one does not trigger the other.

### vs. Informed Consent
- EHDS uses an opt-out model (data available by default, individuals can withdraw), not consent-based (opt-in).
- The EHDS opt-out is a *safeguard* and *protective overlay*, not a form of presumed consent or a prerequisite for processing.

## Opt-Out Granularity

Member States may implement granular opt-out mechanisms (e.g., by data type, purpose, or data holder), but **are not obliged to do so**. The guideline recommends balancing usability with control:

Recommended meaningful granularity levels:
- **Full opt-out** — all secondary uses blocked.
- **Per data type** — e.g., genomic data, medical images.
- **Per data holder** — e.g., cohorts, biobanks, EHR systems.
- **Per purpose** — e.g., research, innovation, policy development.

Excessive granularity risks administrative burden, decision fatigue, and cross-border interoperability issues. A 2-3 layer approach is recommended.

## Does Opt-Out Block Anonymisation?

**Yes.** Under Art. 71(1) and (3), the opt-out applies to the entire chain of processing for secondary use, including anonymisation and pseudonymisation steps that process personal data. However, datasets already anonymised *before* the opt-out was exercised are not affected.

Art. 71(8): Data holders are not obliged to maintain, acquire, or process additional information to identify data subjects solely for complying with opt-out rights.

## Exceptions — Article 71(4)

Member States may adopt national laws allowing access to opted-out data if **all three** cumulative conditions are met:
1. Application is made by a public sector body or Union institution carrying out public health tasks (Art. 53(1)(a)-(c)) or for scientific research with important public interest reasons.
2. Data cannot be obtained by alternative means in a timely and effective manner under equivalent conditions.
3. Applicant provides sufficient justification.

Such exceptions must include specific safeguards: prohibition of re-identification (Art. 61(3)), secure processing environments (Chapter IV), necessity and proportionality (Art. 71(5)-(6)).

## Implementation Architecture

### Opt-Out Registry
Member States or designated HDABs should maintain a secure opt-out registry that:
- Records only data necessary to confirm opt-out status (GDPR data minimisation).
- Uses pseudonymised/encrypted identifiers.
- Provides immediate confirmation to the individual.
- Logs timestamp and source of declaration.
- Is accessible for viewing, updating, or revoking decisions.
- Has access strictly limited to authorised entities with logging and oversight.

### Data Filtering Points
Two lines of defence:
1. **Data holder level** (primary): Healthcare data controllers must be immediately notified and ensure opted-out data is not transferred.
2. **Dataset level** (secondary): Technical barriers at the HDAB/release system prevent release of opted-out data from aggregated datasets.

### Declaration Channels
- Online portal (co-located with national EHR or hosted by HDAB).
- Via healthcare providers or data holders.
- Government office one-stop shops.
- Must include non-digital alternatives for those with limited digital literacy.
- Must comply with accessibility standards (WCAG 2.0+).

## HDAB Responsibilities

If a Member State assigns opt-out implementation to HDABs (Art. 58(2)):
- Provide public information about the opt-out procedure.
- Facilitate the exercise of the right.
- Maintain publicly searchable registers of data permits and access decisions.
- Publish biennial activity reports including statistics on opt-out, exceptions under Art. 71(4), and categories of data used.
- Cooperate with stakeholders including patient organisations, health professionals, researchers, and ethics committees (Art. 57).

## Citizen Engagement

HDABs should:
- Clearly communicate societal benefits of secondary use.
- Inform that opt-out may limit research utility and create dataset bias.
- Provide balanced information acknowledging risks and drawbacks.
- Adapt communication to varying levels of digital health literacy (Art. 84(2)).
- Use diverse channels: online portals, point-of-care materials, mass media, stakeholder networks.
- Engage citizens in co-design of opt-out systems.

## Cross-Border Considerations

Opt-outs do not propagate automatically across borders. Citizens may need to submit opt-outs in each relevant Member State. Alignment of opt-out frameworks across the EU is recommended for interoperability.

## Pitfalls

- Centralised opt-out registries create sensitive datasets that themselves require strong data protection — they reveal individual choices about health data sharing.
- Granular opt-out can inadvertently resemble consent-based logic, undermining the EHDS framework.
- National fragmentation of opt-out mechanisms can undermine cross-border data access.
- EHR-level access restrictions (Art. 8) do NOT block secondary use — citizens must separately opt out under Art. 71.

## Related

[[HDAB_Approval]] [[Data_Holder_Obligations]] [[Pseudonymisation_Anonymisation]] [[Significant_Findings_Notification]]
