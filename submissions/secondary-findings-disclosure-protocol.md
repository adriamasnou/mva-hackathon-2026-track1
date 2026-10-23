# Secondary findings in an open single-patient challenge

**Proposed governance template, with a dated account of this project's work. Updated 23 October 2026. CC BY 4.0.**

An openly accessible research report can make unrelated health information persistent and identifiable. This template separates research discovery, clinical interpretation, return of results and public disclosure. It has not been evaluated with participants, clinicians or organisers and does not itself establish consent, legal authority or a return-of-results pathway. **[OUR INFERENCE]**

## Proposed process

Before analysis, record the challenge's permitted scope, consent terms, publication restrictions, deletion obligations and any authorised private review route. Do not infer consent for public disclosure of every result from access to a genome. If the rules leave a gap, document it and seek an authorised governance decision before disclosure. A team must not invent a private return channel or contact a family contrary to the rules. **[PROPOSED GOVERNANCE]**

Classify potential results for review:

- **Primary-condition findings:** report only within the authorised scope, with the evidence and uncertainty needed to interpret them. A research candidate is not automatically a confirmed molecular diagnosis.
- **Potential modifiers or other relevant findings:** retain for evidence review; an annotation or raw panel extraction is not a curated finding.
- **Potentially actionable unrelated findings:** avoid public variant-level disclosure. A qualified reviewer must determine technical validity, gene–disease relevance, reportability and consent before any authorised return route is used.
- **Uncertain or weakly supported findings:** document their review status in the protected research record. Do not present them as clinically actionable.

These are proposed workflow categories, not a validated clinical classification system. Even aggregate counts can convey sensitive information in a single-person challenge; publish them only when justified by consent and the applicable rules. “Not screened”, “screened but not curated” and “no result met this filter” are different states. None implies that no health risk exists. **[OUR INFERENCE]**

For any return pathway, establish who is clinically responsible, what confirmation is required and what the participant has agreed to receive. Stenton and colleagues describe a Rare Genomes Project setting involving clinical return of findings; that example does not grant this project a similar channel. PMID 38685113.

Record the decision and its evidence, restrict access appropriately, and apply the challenge's deletion obligations to raw and derived patient data, including backups. An open licence for authored prose does not override data restrictions or authorise distribution of patient files.

## Application in this project

**Primary findings:** two BUB1B variants are reported with inferred phase and unresolved allele-specific functional evidence. They are consistent with the disease model. The report does not claim a new clinical classification.

**Relevant-feature panel:** a 30-gene extraction was performed for a clinical feature. It was a raw pre-filter extraction, not a curated findings list. No clinical findings count is claimed from it, and its variant-level output is not distributed here. **[OUR MEASUREMENT — historical project record]**

**Secondary-finding filter:** the August 29 analysis used a retained 81-gene ACMG-labelled list and dated NHS PanelApp-derived lists. It looked for exact variant matches to ClinVar Pathogenic/Likely pathogenic records with at least one review star. This was a research filter, **not** a complete implementation of clinical secondary-findings guidance: gene-specific reporting restrictions, clinical confirmation, coverage, structural variation, conflicts and newer evidence require separate consideration. **[OUR MEASUREMENT; OUR INFERENCE]**

The historical screen reported zero qualifying matches in each category: the 28 cancer, 39 cardiovascular and 14 metabolic/other genes in its ACMG-labelled list, and the 7 child, 6 adult-specific and 14 full-health-related genes in its NHS-derived lists. These lists overlap and must not be added as independent people or findings. The recorded input included 10,895 PASS variants in the ACMG-labelled genes. The join had positive controls, but this does not make the negative result a clinical clearance. **[OUR MEASUREMENT — `pipeline/acmg_sf_screen.py`, dated August 29 record]**

The panel names and counts describe that historical input. They are not a statement of current NHS policy or of what a particular child is entitled to receive. No finding has been sent to the family or to a clinician by this project, and no authorised clinical return pathway or review is claimed. “No qualifying match” does not establish that there is nothing clinically relevant to disclose.

## Adoption questions

1. What analysis and disclosure did the participant actually authorise?
2. Who reviews technical validity and clinical relevance, and who is accountable for return?
3. Is there an authorised private channel, and what may be retained or published?
4. How are non-execution, incomplete curation and negative filter results distinguished?
5. How are retention, deletion and copies audited?

This template is reusable under CC BY 4.0 with attribution. It proposes a process and exposes unresolved decisions; it does not demonstrate better family outcomes or compliance in every setting.
