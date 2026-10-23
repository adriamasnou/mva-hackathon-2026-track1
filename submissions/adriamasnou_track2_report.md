# Arimoclomol for BUB1B-MVA: test exposure, protein function and rescue before treatment

**Track 2 · adriamasnou · 23 October 2026**<br/>
**Research proposal. No drug rescue experiment or treatment in this child has been performed.**

## The proposed candidate and the decision it must earn

We propose **arimoclomol as a conditional preclinical repurposing candidate** for an abundance-limited, functionally rescuable *BUB1B* phenotype. The hypothesis is that augmenting a cellular stress response could increase the pool of functional BubR1. Three links remain unproven: the effect of **p.Asn1002Lys (N1002K)**, the drug's effect on this protein, and rescue at relevant exposure. Our proposed experiment tests those links separately. **[OUR INFERENCE]**

The candidate has a defined human regulatory and pharmacokinetic record, but no established MVA indication. Its US indication is neurological manifestations of Niemann–Pick type C, **with miglustat**, from age two; its clinical mechanism in NPC remains unknown. This is a reason to examine translation carefully, not evidence of efficacy or safety in this child. [MIPLYFFA label, revised March 2026, §§1, 12](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc).

The deliverable combines a falsifiable drug proposal with two working public tools: an offline **gene-to-condition navigator** and a **fail-closed interpretation canary**. It is supported by variant analysis, literature adjudication, a proposed laboratory protocol and a public-genome computational smoke test. The tools can be used now; therapeutic rescue remains to be demonstrated.

## 1. Genotype and mechanism: distinguish evidence from inference

Our analysis identified heterozygous *BUB1B* **c.2210T>G, p.Leu737*** and **c.3006T>G, p.Asn1002Lys**. Their location on opposite parental alleles is **inferred, not established** by parental genotyping or read-based phase. The nonsense allele is predicted to undergo nonsense-mediated decay by analogy to nearby truncations; decay and residual protein have not been measured for this allele. We therefore do not assert that every BubR1 molecule in this child is N1002K. [Track 1 analysis](adriamasnou_track1_report.md); PMID 20516114. **[OUR MEASUREMENT; OUR INFERENCE]**

Published work separates protein amount from function. Some MVA-associated BubR1 substitutions reduce abundance and remain chaperone-dependent; increased expression can restore checkpoint activity for particular tested alleles. Q921H retained approximately normal abundance, so a domain location alone cannot establish instability. Neither observation classifies N1002K. PMID 20516114.

Human BubR1's C-terminal domain has structural functions beyond any catalytic interpretation. Stability and chromosome alignment can be disrupted through different mechanisms; the domain contributes to PP2A-B56 recruitment and checkpoint silencing. We do not base treatment selection on a prediction of lost kinase activity. PMID 22698286; PMID 33207204.

**Working categories are abundance-limited, function-limited, mixed and indeterminate.** They are experimental outcomes, not diagnoses assigned from a structure prediction. A normal melting temperature of an isolated fragment cannot exclude a full-length stability, degradation, localisation or interaction defect. A rise in total protein does not by itself establish rescue. **[OUR INFERENCE]**

Local annotation retained all 313,417 input variants as distinct annotated variants. A prespecified phenotype-blind scan returned *BUB1B* within a severity-tied block spanning ranks 53–61 among 230 genes (nominal rank 55); this is supporting analysis with limited discrimination, not a blinded clinical validation. Local SpliceAI produced low scores for the two findings, with positive controls, which does not exclude splice effects experimentally. [Annotation methods](annotation-toolchain-vep.md); [splice assessment](splice-prediction.md). **[OUR MEASUREMENT]**

## 2. Why arimoclomol merits a bounded test—and what could disqualify it

The primary pharmacology is context-dependent. Kuta and colleagues observed arimoclomol-associated Hsp70 induction in stressed murine neuronal cultures using low-micromolar exposures; mutant-FUS neurons did not show the same induction. These are neuronal stress models, not dividing N1002K cells. The result supports testing a conditional mechanism and argues against assuming a uniform response. PMID 31900865, Figures 5–7 and Results; full article body read, supplementary dose-response data not used for a quantitative claim.

The EMA's earlier NPC assessment describes HSP70/NPC1 expression effects at much higher concentrations, including 400 µM, and questions the concentration-response relationship. That is a substantial warning about extrapolating a chaperone mechanism between cells; it is not a universal threshold or a refutation of the later US approval. [CHMP withdrawal assessment, adopted 16 December 2021, pp.21–22](https://www.ema.europa.eu/en/documents/withdrawal-report/withdrawal-assessment-report-miplyffa_en.pdf).

The current label estimates paediatric NPC steady-state mean serum trough and peak concentrations of **206 and 523 ng/mL**. Using arimoclomol free-base molecular weight approximately 313.78 g/mol gives **0.66 and 1.67 µM**, respectively. This arithmetic is a first exposure anchor: serum concentration is not intracellular free concentration, and a peak is not sustained exposure. [Label §§11–12](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc); [reproducible calculation](../analysis/exposure_check.py). **[OUR MEASUREMENT]**

**Advance only if a validated cellular assay demonstrates functional benefit in the clinically anchored range.** A proposed initial series spans vehicle, 0.2, 0.6, 1 and 2 µM; 4 and 10 µM are exploratory arms clearly separated from the translational claim. These are laboratory design values, not doses for a person. Measure medium and intracellular exposure where feasible and account for protein binding and time course. An effect confined to a high exploratory concentration does not pass the translational gate. **[PROPOSED EXPERIMENT]**

## 3. The experiment: four gates with explicit failure outcomes

**Gate A — establish what the variant does.** Compare sequence-verified full-length WT and N1002K in a controlled replacement system, with endogenous BubR1 addressed consistently. Include an empty/depleted control and a published destabilising allele. Measure transcript, protein abundance, turnover and localisation. Titrate WT to match N1002K abundance before comparing function: otherwise a functional deficit could simply reflect unequal amounts. Confirm any result in an independent preparation and ultimately a patient-relevant system. **[PROPOSED EXPERIMENT; design informed by PMID 20516114]**

**Gate B — validate measurement and engagement.** Qualify linear protein measurement, dynamic range and repeatability before testing efficacy. Use HSPA1A and other justified pathway readouts alongside BubR1. Validate normalisers under each condition; total-protein normalisation is a candidate, not an automatic guarantee. Include a separate positive control for the stress-response assay. Biological variation in a clinical PBMC study is not analytical CV for a cell assay: the former cannot size the latter. PMID 34418116. **[PROPOSED EXPERIMENT]**

**Gate C — require function, not a protein-only hit.** Quantify chromosome alignment and segregation errors per completed division, checkpoint response, division timing, viability and proliferation. Track cell fate so cytostasis, apoptosis or selection against abnormal cells cannot masquerade as corrected segregation. Use blinded scoring and randomized plate positions. Plan biological replicates from pilot variance and a prespecified effect size; report confidence intervals, independent replicates and all tested concentrations. **[PROPOSED EXPERIMENT]**

**Gate D — interpret each outcome correctly.**

- **Abundance rises and function improves at relevant exposure:** advance to independent replication and a patient-relevant model; this still does not justify prescribing.
- **Abundance rises without functional benefit:** reject protein abundance as an adequate surrogate and stop this candidate in that system.
- **The assay works, but arimoclomol has no engagement or benefit at relevant exposure:** reject the tested drug–exposure–system combination. Do not declare all proteostasis strategies impossible.
- **Controls or exposure measurements fail:** label the experiment indeterminate and repair it; do not count it as a biological negative.
- **Only a fragment assay is negative:** retain the full-length functional question. Fragment thermal measurements are supporting evidence, not the decisive gate. **[OUR INFERENCE; PROPOSED EXPERIMENT]**

The existing sequence and reagent specifications support an initial fragment study. Their approximately $630 materials estimate is **not** a quote for the full cellular programme, laboratory labour, exposure measurement or patient-derived validation. No laboratory has committed to execute this proposal. [Reagent specification](n1002k-reagent-specification.md); [functional protocol](functional-rescue-plan.md). **[ESTIMATE; PROPOSED EXPERIMENT]**

## 4. Alternatives and mechanistic cautions

**HSP90 inhibition:** tested destabilising BubR1 mutants lost protein under HSP90 inhibition. This supports a mechanistic caution when considering that axis, conditional on an untested allele's behaviour; it is not an established clinical contraindication for N1002K. PMID 20516114.

**Fisetin:** Salmela and colleagues observed substantial loss of kinetochore BubR1 and premature mitotic exit in dividing cells at 30 µM. We retain this as a **mechanistic caution against assuming an OTC senolytic is beneficial**. Human exposure at supplement doses and clinical harm in MVA were not established by that experiment. It does not establish the same effect for quercetin or dasatinib. PMID 19395653. A clinician or pharmacist should assess supplement use; the report does not advise a family to change treatment independently.

**Rapamycin and NAD precursors:** model-specific findings and unresolved translation prevent a treatment recommendation. Preliminary rapamycin observations reported in a paper are not a controlled published negative trial. SIRT2 transgene effects are not evidence that NR rescues BubR1, and an NR tumour-model signal warrants scrutiny without being treated as a measured risk in this child. PMID 23602569; PMID 24825348; PMID 36371959. **[OUR INFERENCE]**

**4-PBA and TUDCA:** the earlier blanket exclusion based on an “ER-only” compartment argument is withdrawn. Compartment labels alone do not establish a drug's complete pharmacology or rule out indirect effects. We have not demonstrated BubR1 rescue by either compound. Lack of supporting evidence is not a universal refutation. **[OUR INFERENCE]**

## 5. Innovation that another team can use

**Gene-to-condition navigator.** The offline [interactive lookup](pgtm-navigator.html) joins a dated HFEA register to candidate gene mappings from ClinVar, HPO and gene-MIM records. The rebuilt August 5 workbook contains **2,063 rows: 2,028 mapped and 35 unmapped**, with **1,782 gene symbols**. Each gene retains source/OMIM evidence; nine ClinVar/HPO disagreements remain visible. No match is not ineligibility, and a matched condition does not establish a particular variant or family's eligibility. [Data and provenance](hfea-pgtm-provenance.json); [builder](../tools/pgtm/build.py). **[OUR MEASUREMENT]**

The tool addresses a practical information gap while preserving uncertainty. It runs without a server, sends no queries and links back to the regulator. Its extension to other genes is demonstrated by the full crosswalk and public controls, not inferred from the single MVA case. It has not been evaluated with families or clinicians and does not claim a measured improvement in access or outcomes.

**Interpretation canary.** The [portable panel](../canary/README.md) refuses to turn missing, malformed or nonfinite model outputs into reassuring negatives. Real SpliceAI inference passes six controls; a separate harness self-test rejects nine injected failures. These are regression checks, not a clinical accuracy benchmark. No patient-scale data or reference genome is distributed. **[OUR MEASUREMENT — measured output and dependency snapshot included]**

**Public computational smoke test.** A prior Exomiser run processed 4,096,123 normalized variants in a public HG002 genome with an *FGFR2* spike and ranked *FGFR2* first of 649 scored genes. This demonstrates that run at genome scale. It does not estimate diagnostic sensitivity, establish all background genes as true negatives or exclude knowledge leakage from ClinVar. [Public-case report](generalisation-public-case.md). **[OUR MEASUREMENT]**

## 6. What is delivered, and what remains unknown

Delivered: the analysis and source trail, a conditional named candidate, explicit functional and exposure gates, portable code, public-data lookup, family-oriented explanation and a proposed laboratory plan. The molecular diagnosis remains consistent with *BUB1B*-MVA, with unresolved phase and allele-specific functional evidence. No clinical reclassification or treatment claim follows from the computational work alone.

The next result worth obtaining is **whether full-length N1002K retains rescuable function, and whether arimoclomol improves that function at relevant exposure**. If it fails, the decision criteria make that failure useful. If it succeeds, replication and clinical review—not this competition—determine what happens next.
