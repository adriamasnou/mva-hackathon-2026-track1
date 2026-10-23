# Thermal stability of the *BUB1B* pseudokinase domain carrying the MVA variant p.(Asn1002Lys)

**A protocol for a collaborating laboratory**

| | |
|---|---|
| **Version** | 1.3 — 2026-10-23; published methods, control scope and instrument adaptation corrected |
| **Author** | adriamasnou · *Rare Disease, Real Kid: The MVA Hackathon 2026* |
| **Licence** | CC BY 4.0 |
| **Companion document** | [`n1002k-reagent-specification.md`](n1002k-reagent-specification.md) — construct design, all four orderable sequences, costings |
| **Biosafety** | **BSL-1.** *E. coli* K-12/B-derivative expression host; synthetic dsDNA; no human material, no pathogen, no controlled-access data |
| **Estimated reagent cost** | **≈ $630** — four constructs including two controls (list prices, §Materials) |
| **Estimated timeline** | **~3 weeks** elapsed; ~4 days hands-on (§Timing) |

---

## Scope and scientific premise

This is a **proposed fragment biophysics sub-study**, not a validated assay or an executed experiment. Its decisions were drafted before data collection but have not been registered as a final statistical protocol. The [full-length functional and exposure plan](functional-rescue-plan.md) governs candidate advancement.

The retained literature supports instability for some MVA-associated BubR1 variants, but does not establish N1002K function. Phase and nonsense-mediated decay for the identified pair are unmeasured. The protocol therefore makes no claim that all protein in the child is N1002K. PMID 20516114. **[OUR INFERENCE]**

The experiment compares HIS₆-BubR1(721–1,044) WT and N1002K with K795A and Q921H comparators. Published WT-fragment unfolding curves exist (PMID 22698286, Fig S3G–H), but the reported WT–K795A thermal separation concerns **full-length GST-BUBR1** (Fig 3G/S3D). Isolated full-length Q921H was WT-like in the cited cellular abundance, segregation, alignment and checkpoint assays (PMID 20516114, Fig 4D and S2A–B); this does not establish neutral fragment thermostability or clinical benignity. All fragment comparators need qualification before interpretation.

The C-terminal domain contributes structural and non-catalytic functions; the proposal does not require a universal claim that BubR1 has no catalytic activity. A fragment stability measurement cannot establish checkpoint function, HSP90 dependence or a treatment indication. PMID 22698286; PMID 33207204.

**Potential deliverable:** a reproducible fragment stability measurement with explicit assay limits. A null result cannot exclude a full-length or cellular-context defect. **Not delivered by this experiment alone:** clinical classification, drug rescue or a calibrated PS3/BS3 evidence strength.

---

## Materials

### Biological materials

| Item | Source | Notes |
|---|---|---|
| *E. coli* expression host | **BL21(DE3) T1R** | Reported in ref 1, Supplemental Experimental Procedures, p.10. A substitute host is a laboratory adaptation requiring qualification. |
| Cloning host | DH5α or equivalent | For plasmid propagation |

### DNA constructs

**Four proposed constructs, with controls qualified before interpretation.**

| Construct | Proposed role | Residue in 721–1,044? | Dated materials estimate |
|---|---|---|---|
| WT | baseline | — | ≈$87 + vector $35–55 |
| N1002K | variant under test | 1002 | as above |
| K795A | candidate destabilising comparator | 795 | as above |
| Q921H | candidate WT-like fragment comparator, unqualified; WT-like in the reported full-length cellular assays | 921 | as above |

Brnich et al. require assay controls, a demonstrated dynamic range and justified thresholds before interpreting functional evidence (PMID 31892348). Merely adding two constructs does not meet those requirements or establish an ACMG evidence strength. A WT–variant comparison alone cannot establish calibration.

K795A has published thermal measurements on **full-length GST-BUBR1**: WT 39.1 °C and K795A 34.7 °C (PMID 22698286, Figures 3G/S3D). These values do not establish the behaviour of the isolated 721–1,044 fragment. Qualify the comparator in the actual assay before using it to interpret a negative result.

Isolated full-length Q921H was WT-like in cellular abundance and chromosome segregation (PMID 20516114, Fig 4D, middle panel), and in the reported alignment and checkpoint assays (Fig S2A–B). Those direct functional results do not validate neutral fragment thermostability, every possible BubR1 function or clinical benignity. Q921H also occurs in cis with L844F in an affected family (PMID 15475955). Qualify its proposed WT-like role in the fragment assay before using it as a negative folding comparator. If either comparator fails its prespecified qualification criteria, redesign the control set and classify the assay as indeterminate.

> **CRITICAL** — Order all four constructs as **cloned, sequence-verified genes** (e.g. Twist *Clonal
> Genes*, specified *"100% sequence perfect, NGS verified"*), **not** as linear gene fragments. Order
> them **in the same run**. The measurement is a ΔTm between constructs that must differ from WT only
> at the intended codon; two synthesis batches introduce differences the experiment cannot separate from
> the variant. See companion document §3 for the full rationale and a documented trap involving
> silent siRNA-resistance edits present in the deposited pLAP-BUBR1 plasmids.
>
> **CRITICAL** — The fragment is **internal to the ORF**: no start codon, no stop codon. Ensure the
> destination vector supplies an N-terminal HIS₆ tag **in frame**, and that a stop codon is present —
> append `TAA` if the vector does not provide one. **Do not codon-optimise.** Optimisation would break
> the requirement that the constructs be identical outside their intended edits.

### Reagents

| Reagent | Supplier in ref 1 | Current equivalent | Notes |
|---|---|---|---|
| HEPES, NaOH | — | any | Buffer base |
| NaCl | — | any | |
| TCEP | — | any | Reducing agent |
| Protease inhibitor cocktail | Roche | Roche cOmplete or equivalent | EDTA-free recommended (Ni-NTA downstream) |
| DNase I | — | any | |
| Chelating Sepharose | GE Healthcare | **Cytiva** (GE Healthcare Life Sciences is now Cytiva) | Charge with NiCl₂ |
| NiCl₂ | — | any | |
| Imidazole | — | any | Elution, 400 mM |
| Superdex S75 column | GE Healthcare | **Cytiva** | Size-exclusion |
| **AMP-PNP** | **Sigma** | Sigma-Aldrich / Merck | Non-hydrolysable ATP analogue |
| MgCl₂, EDTA | — | any | Nucleotide-condition panel |

⚠️ **Catalogue numbers are deliberately not given** for items where we could not verify a current
part number. Supplier and product identity are given instead; source locally. The two figures we did
verify against live vendor pricing on 2026-08-31 are Twist Clonal Genes (9¢/bp, +$35–55 cloning) and
Plasmidsaurus whole-plasmid sequencing ($15/sample, 1-day turnaround).

### Equipment

| Item | As used in ref 1 | Proposed alternative / qualification |
|---|---|---|
| Cell disruption | **Emulsiflex** homogeniser | French press, microfluidiser, or sonication |
| Centrifuge | 4,000 g and 20,000 g capable | any |
| FPLC | Akta Explorer | any FPLC |
| **Thermal denaturation** | **Perkin Elmer LS55 fluorimeter** + Neslab RTE circulator + in-cuvette thermometer (Edale), software Fluope | **NanoDSF is a proposed adaptation requiring qualification**, not an established equivalent — see note below |
| Circular dichroism | Jasco-32 spectropolarimeter | any far-UV CD instrument with Peltier control |

> **CRITICAL — qualify the instrument adaptation.** Ref 1 follows intrinsic fluorescence of the
> fragment at **290 nm excitation / 340 nm emission**, using **1 °C steps with 5 min equilibration**
> and a transition estimated by linear extrapolation. A continuous-ramp 350/330 nm ratio is a
> different readout and analysis, not automatically a numerically equivalent measurement.
> For nanoDSF, document the actual instrument's excitation and emission channels, compatibility with
> nucleotide-containing samples, ramp, aggregation behaviour and transition-fitting method. Do not
> assume it can select 290 nm excitation or collect a 340 nm trace. Bridge against source-like
> conditions where practicable; retain raw signals and report method-specific transition estimates.
> **[Proposed adaptation and qualification requirements; not validation reported in ref 1.]**

### Reagent setup

**Lysis / purification buffer** — 20 mM HEPES/NaOH pH 7.4, 300 mM NaCl, 1 mM TCEP.
Supplement with protease inhibitors and DNase I immediately before use.

**Elution buffer** — lysis buffer + 400 mM imidazole.

**SEC buffer** — 20 mM HEPES/NaOH pH 7.4, 300 mM NaCl, 1 mM TCEP.

**Thermal denaturation conditions** — 20 mM HEPES/NaOH pH 7.4, 300 mM NaCl, 1 mM TCEP, run as a
four-condition panel exactly as in ref 1:

1. **+ 10 mM EDTA** (apo / metal-free)
2. **+ 10 mM MgCl₂**
3. **+ 250 µM AMP-PNP**
4. **+ 10 mM MgCl₂ + 250 µM AMP-PNP**

> **CRITICAL [OUR DESIGN]** — Apply the published four-condition panel to **all four** constructs.
> Report condition-dependent differences without assuming that nucleotide or metal addition must
> stabilise the fragment. The panel does not replace qualification of the construct comparators.

---

## Procedure

### Stage 1 · Construct preparation ● TIMING 1–2 weeks, mostly waiting

1. Order all four constructs — WT, N1002K, K795A, Q921H; sequences in the companion document §3 — as
   cloned, sequence-verified genes per §Materials. **TIMING** 4–7 business
   days express, 10 standard.
2. Transform into the cloning host; prepare plasmid DNA.
3. **Verify by whole-plasmid sequencing** (e.g. Plasmidsaurus, $15/sample, overnight).
   **CRITICAL STEP** — The acceptance criterion is **each construct differs from WT only at its
   intended codon — one base for N1002K and Q921H, two adjacent bases for K795A — and nothing else
   differs anywhere in any of the four plasmids.** Not
   "the edit is present" — *only* the edit is present. Whole-plasmid rather than Sanger sequencing,
   because polymerase-based steps introduce second-site mutations that a targeted amplicon cannot see.
   ■ **PAUSE POINT** — plasmid stocks are stable indefinitely at −20 °C.

### Stage 2 · Expression ● TIMING 2 days

4. Transform all four plasmids into the expression host **in parallel, on the same day, from the same
   competent-cell batch.**
5. Express all four constructs **in the same experiment**, under identical induction conditions.
   **CRITICAL STEP** — Batch is a confounder for every downstream comparison. All four constructs must
   travel together from this step onward.
   > **Published conditions:** BL21(DE3) T1R cultures grown at **30 °C to OD₆₀₀ 0.6** in **LB with
   > 30 µg/mL kanamycin**, then induced with **0.25 mM IPTG for 18 h at 16 °C** (ref 1,
   > Supplemental Experimental Procedures, p.10, Protein purification). These are source parameters,
   > not guarantees of N1002K expression. Record any adaptation for the selected vector/host and
   > apply matched conditions across all four constructs.
6. Harvest by centrifugation, **15 min at 4,000 g**.
   ■ **PAUSE POINT** — pellets may be frozen at −80 °C.

### Stage 3 · Purification ● TIMING 1–2 days

7. Resuspend pellets in **lysis buffer** (20 mM HEPES/NaOH pH 7.4, 300 mM NaCl, 1 mM TCEP) with
   protease inhibitors and DNase I.
8. Lyse by **Emulsiflex** or equivalent.
9. Clarify the homogenate by centrifugation, **30 min at 20,000 g**.
10. Affinity-purify on **chelating Sepharose charged with NiCl₂**.
11. Elute in lysis buffer + **400 mM imidazole**.
12. **Polish all four constructs identically.**
    > 🔴 **CRITICAL STEP — a methodological asymmetry in the source, which we flag so that
    > reproducing it is a decision rather than an inheritance.** Ref 1 applied **size-exclusion
    > chromatography (Superdex S75) to WT only**, while *"the point mutants … were dialyzed"*. SEC
    > removes aggregate and misfolded species. Applying it to WT alone could flatter WT's apparent
    > stability relative to the mutant, in the same direction as the hypothesis under test. **We
    > recommend treating all constructs identically — SEC all, or dialyse all.** If you reproduce
    > the published asymmetry for comparability with ref 1, we suggest running the symmetric version
    > alongside it. The source does not comment on this. **[Our observation on reading the method.]**
13. Assess purity and integrity by SDS-PAGE.
    **CRITICAL STEP** — Confirm expression **before** any melting run. A construct that does not
    express cannot produce a melting curve, and a flat curve would otherwise be interpreted as a
    result. ? **TROUBLESHOOTING**

### Stage 4 · Thermal denaturation ● TIMING 1 day

14. Prepare all four constructs at matched concentration in each of the four conditions in §Reagent setup.
    The published WT-fragment fluorescence curves used **1 µM protein** (ref 1, Fig S3G).
    Qualify signal quality at the chosen concentration and record any adaptation.
15. **Melt all four constructs side by side in the same run.** **CRITICAL STEP** — The measurement is
    the within-run ΔTm of N1002K from WT. Interpret it only after qualifying the K795A and Q921H
    comparators for their intended roles. Retain absolute unfolding curves and transition estimates
    as well as within-run differences.
16. **Source-like fluorescence method:** increase temperature in **1 °C steps**, equilibrating
    **5 min** at each step. **Proposed nanoDSF adaptation:** qualify and report its ramp and
    equilibration settings; do not call a continuous ramp equivalent without a method comparison.
17. **Source-like method:** record emission **300–400 nm** with excitation at **290 nm**, and plot
    the melting curve at **340 nm**. Ref 1 selected 290 nm because nucleotide interfered at 280 nm.
    **NanoDSF adaptation:** report the available raw emission channels and ratio, if used, and
    qualify interference in AMP-PNP conditions. If the instrument has fixed excitation, it cannot
    simply reproduce the source's 290 nm setting; unresolved interference prevents interpretation.
18. **Source-like method:** estimate the transition by **linear extrapolation** (ref 1).
    **NanoDSF adaptation:** prespecify a qualified fitting method, such as a first-derivative maximum,
    and report it explicitly. Use one analysis consistently within a comparison; do not pool
    method-specific transition estimates as though they were interchangeable.
19. **Repeat Stages 2–4 with ≥3 independent protein preparations [OUR EXPLORATORY DESIGN].**
    Published WT-fragment unfolding curves exist (ref 1, Fig S3G–H), but do not establish fragment
    WT–K795A separation, Q921H neutrality or an N1002K threshold. Reproducibility complements
    control qualification; it does not replace calibration or a confirmatory power calculation.
    ? **TROUBLESHOOTING**

### Stage 5 · Orthogonal confirmation (recommended) ● TIMING 0.5 day

20. Acquire far-UV CD spectra for WT and N1002K (and the comparators, if material allows), with and
    without **10 mM MgCl₂ plus 250 µM AMP-PNP**. The published WT-fragment experiment used **2.5 µM
    protein** (ref 1, Fig S3H), **1 °C steps**, **3 min equilibration** and an unfolding trace at
    **222 nm** (Supplemental Experimental Procedures, p.12). Applying this to N1002K is our proposed
    orthogonal measurement of secondary structure and unfolding, not a cellular functional assay.

---

## Timing

| Stage | Hands-on | Elapsed |
|---|---|---|
| 1 · Construct preparation | ~0.5 day | **1–2 weeks** (synthesis + sequencing turnaround) |
| 2 · Expression | ~0.5 day | 2 days |
| 3 · Purification | ~1.5 days | 1–2 days |
| 4 · Thermal denaturation | ~1 day | 1 day |
| 5 · CD (optional) | ~0.5 day | 0.5 day |
| **× 3 independent preparations** | | add ~1 week |
| **Total** | **~4 days** | **~3 weeks** |

---

## Troubleshooting

| Step | Problem | Possible reason | Solution |
|---|---|---|---|
| 3 | Sequencing shows differences beyond the intended edit | Second-site mutation from a polymerase step; or comparator is an Addgene-derived plasmid carrying silent siRNA-resistance edits (`c.2823C>A`, `c.2826G>A` — **both inside this fragment**) | Re-order; or if comparing against a deposited plasmid, expect and account for those two synonymous differences. See companion §4a.1 |
| 13 | No expression, or insoluble product | Internal fragment, no native start/stop; frame error at the tag junction | Re-check frame across the cloning junction; confirm a stop codon is present; try lower induction temperature |
| 13 | One construct expresses, the other does not | A genuinely destabilising variant can reduce soluble yield | **This is itself informative — record it.** Do not discard; note yield for both and proceed with whatever is obtainable |
| 15 | Noisy or non-sigmoidal melting curve | Protein concentration too low; aggregation; buffer mismatch | Confirm concentration; centrifuge before loading; verify buffer identity between constructs |
| 17 | Flat signal in AMP-PNP conditions | Possible nucleotide interference or inadequate signal | For a source-like assay, check **290 nm** excitation. For fixed-excitation instruments, qualify interference and signal quality; redesign the measurement if unresolved (Step 17) |
| 19 | ΔTm inconsistent across preparations | Batch effect; asymmetric purification | Confirm all four constructs were purified identically (Step 12) and travelled together from Step 4 |

---

## Anticipated results and interpretation limits

**Draft before data collection; not a completed preregistration.** A laboratory must freeze sample size, analysis and technical exclusion rules after assay qualification and before confirmatory unblinding. The exploratory minimum of three preparations is not a power calculation or permission for optional stopping.

Published WT 39.1 °C and K795A 34.7 °C values were measured on full-length GST-BUBR1 (PMID 22698286, Fig 3G/S3D). They are not acceptance thresholds for the 721–1,044 fragment, whose WT unfolding curves are in Fig S3G–H. Qualification must establish whether K795A provides reproducible destabilising separation and whether Q921H is WT-like in the actual fragment assay. Q921H is not expected to supply the destabilising separation merely because it is called a comparator. Failure to establish either proposed role requires control redesign and an indeterminate assay classification; it is not a positive result for N1002K.

### Reproducible lower thermal stability

This supports destabilisation of the purified fragment under the tested conditions. It does not measure full-length abundance, prove HSP90 dependence or establish a clinical contraindication. Test those separately in cells. The finding motivates, but does not validate, a stabilisation hypothesis. **[OUR INFERENCE]**

### No detectable difference

Report the estimate, confidence interval and resolution of the assay. A null result is consistent with similar fragment stability, insufficient sensitivity, a full-length-context defect or altered cellular degradation/localisation. It does not establish a specific PP2A mechanism or exclude an abundance-limited state in cells. **[OUR INFERENCE]**

### Ambiguous or failed measurement

If the curves, controls or independent preparations fail prespecified quality rules, report the result as indeterminate. Any additional work after unblinding must be identified as follow-up rather than silently extending a fixed analysis.

## Clinical evidence and future scale

The ClinGen functional-evidence framework requires assessment of assay relevance, validation and suitable controls (PMID 31892348). Its control-count guidance is conditional, not an automatic ceiling determined solely by the existence of a VCEP. A BUB1B-specific panel is not the only mechanism for clinical interpretation. This fragment experiment has not been validated for PS3 or BS3 and must not be used to upgrade N1002K by itself.

A domain-wide multiplexed assay could measure many variants and help reveal functional patterns. PMID 31892348. **[OUR INFERENCE]** **It cannot generate its own independent clinical truth labels merely by measuring more variants.** Calibration still requires external pathogenic/benign evidence, suitable validation and an appropriate disease-relevant readout. A large set of VUS measurements is not automatically a clinically classified domain. **[PROPOSED FUTURE WORK; OUR INFERENCE]**

## What is being asked, and what is not

- **No clinical recommendation is made or intended.** Nothing here constitutes advice about the care
  of any patient, and no contact with the family is sought or permitted.
- **This project has no wet laboratory.** Everything here is specification; we cannot run it.
- **The proposed recombinant fragment experiment needs a variant sequence, not patient sequencing files or tissue.** Do not treat a ClinVar record for c.3006T>A as public provenance for c.3006T>G: they encode the same protein substitution but are different nucleotide alleles. Patient-derived extensions would require separate access, consent and governance.
- **Whatever the result, it should be published** — including, and especially, Outcome B.

---

## References

1. Suijkerbuijk SJ, van Dam TJP, Karagöz GE, von Castelmur E, Hübner NC, Duarte AMS, Vleugel M,
   Perrakis A, Rüdiger SGD, Snel B, Kops GJPL. **The vertebrate mitotic checkpoint protein BUBR1 is
   an unusual pseudokinase.** *Dev Cell* 2012;22(6):1321–1329. PMID **22698286**.
   *(Full-length WT/K795A thermal pair, Fig 3G/S3D; WT-fragment fluorescence and CD curves,
   Fig S3G–H. Expression, purification and thermal methods: Supplemental Experimental Procedures,
   pp.9–12. Proposed adaptations and qualification steps are identified separately above.)*
2. Suijkerbuijk SJ, van Osch MHJ, Bos FL, Hanks S, Rahman N, Kops GJPL. **Molecular causes for BUBR1
   dysfunction in the human cancer predisposition syndrome mosaic variegated aneuploidy.**
   *Cancer Res* 2010;70(12):4891–4900. PMID **20516114**. *(Destabilisation mechanism for the
   in-domain missense series; geldanamycin/HSP90 dependence, Fig 3C.)*
3. Brnich SE, Abou Tayoun AN, Couch FJ, Cutting GR, Greenblatt MS, Heinen CD, Kanavy DM, Luo X,
   McNulty SM, Starita LM, Tavtigian SV, Wright MW, Harrison SM, Biesecker LG, Berg JS; ClinGen
   Sequence Variant Interpretation Working Group. **Recommendations for application of the functional
   evidence PS3/BS3 criterion using the ACMG/AMP sequence variant interpretation framework.**
   *Genome Med* 2020;12(1):3. PMID **31892348**. *(Control-count requirement; OddsPath conversion.)*

---

## Provenance and competing interests

The expression strain, induction conditions, buffers and source-like fluorescence/CD methods are
reported in ref 1 and its Supplemental Experimental Procedures. The matched purification design,
four-construct comparisons, exploratory preparation count, control-qualification rules and nanoDSF
adaptation are our proposals, not methods validated for N1002K by that paper. Published curves and
full-length thermal values are distinguished above from proposed fragment acceptance criteria.
Construct sequences, primer design and costings are in the companion document, each carrying its
own source and date.

**No competing interests.** This work was produced for a public rare-disease hackathon and is
released CC BY 4.0. **No funding or laboratory commitment is attached to it.**
