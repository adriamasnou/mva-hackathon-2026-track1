# Thermal stability of the *BUB1B* pseudokinase domain carrying the MVA variant p.(Asn1002Lys)

**A protocol for a collaborating laboratory**

| | |
|---|---|
| **Version** | 1.2 — 2026-10-23; interpretation and evidence limits corrected |
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

The experiment compares HIS₆-BubR1(721–1,044) WT and N1002K with K795A and Q921H comparators. Published K795A thermal values concern **full-length GST-BUBR1**, not this fragment. Q921H is a normal-abundance comparator in the cited cellular work; it is not a proven neutral fragment-thermostability or clinical control. All fragment comparators need qualification before interpretation. PMID 22698286; PMID 20516114.

The C-terminal domain contributes structural and non-catalytic functions; the proposal does not require a universal claim that BubR1 has no catalytic activity. A fragment stability measurement cannot establish checkpoint function, HSP90 dependence or a treatment indication. PMID 22698286; PMID 33207204.

**Potential deliverable:** a reproducible fragment stability measurement with explicit assay limits. A null result cannot exclude a full-length or cellular-context defect. **Not delivered by this experiment alone:** clinical classification, drug rescue or a calibrated PS3/BS3 evidence strength.

---

## Materials

### Biological materials

| Item | Source | Notes |
|---|---|---|
| *E. coli* expression host | BL21(DE3) or equivalent | **Not specified in ref 1**, which states only *"expressed in E. coli"*. BL21(DE3) is our recommendation for a T7-driven His-tagged construct, not a source parameter. |
| Cloning host | DH5α or equivalent | For plasmid propagation |

### DNA constructs

**Four proposed constructs, with controls qualified before interpretation.**

| Construct | Proposed role | Residue in 721–1,044? | Dated materials estimate |
|---|---|---|---|
| WT | baseline | — | ≈$87 + vector $35–55 |
| N1002K | variant under test | 1002 | as above |
| K795A | candidate destabilising comparator | 795 | as above |
| Q921H | normal-abundance cellular comparator; fragment behaviour unknown | 921 | as above |

Brnich et al. require assay controls, a demonstrated dynamic range and justified thresholds before interpreting functional evidence (PMID 31892348). Merely adding two constructs does not meet those requirements or establish an ACMG evidence strength. A WT–variant comparison alone cannot establish calibration.

K795A has published thermal measurements on **full-length GST-BUBR1**: WT 39.1 °C and K795A 34.7 °C (PMID 22698286, Figures 3G/S3D). These values do not establish the behaviour of the isolated 721–1,044 fragment. Qualify the comparator in the actual assay before using it to interpret a negative result.

Q921H retained approximately normal abundance in the cited cellular experiment (PMID 20516114). That does not validate neutral fragment thermostability or normal chromosome-segregation function. It also occurs in cis with L844F in an affected family (PMID 15475955). It is neither a clinically benign calibration variant nor an established negative folding control. If either comparator fails qualification, redesign the control set and classify the assay as indeterminate.

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

| Item | As used in ref 1 | Accepted modern equivalent |
|---|---|---|
| Cell disruption | **Emulsiflex** homogeniser | French press, microfluidiser, or sonication |
| Centrifuge | 4,000 g and 20,000 g capable | any |
| FPLC | Akta Explorer | any FPLC |
| **Thermal denaturation** | **Perkin Elmer LS55 fluorimeter** + Neslab RTE circulator + in-cuvette thermometer (Edale), software Fluope | 🔑 **nanoDSF (e.g. NanoTemper Prometheus) is the direct modern equivalent and we recommend it** — see CRITICAL note below |
| Circular dichroism | Jasco-32 spectropolarimeter | any far-UV CD instrument with Peltier control |

> 🔑 **CRITICAL — instrument substitution, and why this one is not a compromise.** Ref 1 measures
> **intrinsic tryptophan fluorescence** (excitation 290 nm, emission followed at 340 nm) in 1 °C
> steps. **That is precisely the physical observable nanoDSF measures natively**, as the 350/330 nm
> emission ratio, with far better temperature control, continuous ramping, and ~10 µL sample volumes.
> A modern nanoDSF instrument is therefore **the same measurement, better executed** — not a
> substitution that breaks comparability. **Report both the raw 340 nm curve and the 350/330 ratio**
> if the instrument provides them, so the value can be compared to the published series either way.
> **[Our recommendation. Ref 1 used the LS55; the equivalence argument is ours.]**

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

> **CRITICAL** — Run all four conditions for **all four** constructs. Nucleotide and metal binding shift
> Tm, and a ΔTm measured under only one condition can miss a difference that appears under another —
> or manufacture one. The panel is the control.

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
   > ⚠️ **Induction temperature, IPTG concentration and duration are NOT specified in ref 1** and are
   > left to the laboratory. Whatever is chosen must be **identical for all four constructs**, and should
   > be recorded, since a future laboratory reproducing this will need it — one of the reasons this
   > measurement is worth publishing is that it establishes parameters the source did not report.
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
15. **Melt all four constructs side by side in the same run.** **CRITICAL STEP** — The measurement is
    the ΔTm of N1002K from WT, read against the K795A and Q921H arms melted in the same run. Absolute
    Tm compared across runs is not the endpoint.
16. Ramp temperature in **1 °C steps**, equilibrating **5 min** at each step (or the equivalent
    continuous slow ramp on a nanoDSF instrument).
17. Record emission **300–400 nm** with excitation at **290 nm**; plot the melting curve at
    **340 nm**. On nanoDSF, additionally record the **350/330 ratio**.
    > **CRITICAL** — Excitation at 290 nm rather than 280 nm is deliberate in ref 1, *"due to
    > interference of the nucleotide by excitation at 280 nm"*. Conditions 3 and 4 contain AMP-PNP.
    > **Do not default the instrument to 280 nm.**
18. Determine the denaturation temperature by **linear extrapolation** (ref 1's stated method), or by
    first-derivative maximum if using nanoDSF — **report which, and use one method throughout.**
19. **Repeat Stages 2–4 with ≥3 independent protein preparations.** **CRITICAL STEP** — There is no
    published Tm for this fragment, so reproducibility across independent preparations *is* the
    anchor. ? **TROUBLESHOOTING**

### Stage 5 · Orthogonal confirmation (recommended) ● TIMING 0.5 day

20. Acquire far-UV CD spectra for WT and N1002K (and the controls, if material allows) ± 10 mM MgCl₂ / 250 µM AMP-PNP, temperature ramped
    in 1 °C steps. This tests whether any Tm difference is accompanied by a change in secondary
    structure content, and distinguishes a destabilised-but-folded protein from a misfolded one.

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
| 17 | Flat signal in AMP-PNP conditions | Excitation set to 280 nm; nucleotide interference | Set excitation to **290 nm** (Step 17) |
| 19 | ΔTm inconsistent across preparations | Batch effect; asymmetric purification | Confirm all four constructs were purified identically (Step 12) and travelled together from Step 4 |

---

## Anticipated results and interpretation limits

**Draft before data collection; not a completed preregistration.** A laboratory must freeze sample size, analysis and technical exclusion rules after assay qualification and before confirmatory unblinding. The exploratory minimum of three preparations is not a power calculation or permission for optional stopping.

Published WT 39.1 °C and K795A 34.7 °C values were measured on full-length GST-BUBR1 (PMID 22698286). They are not acceptance thresholds for the 721–1,044 fragment. A comparator that does not separate from WT in this system may indicate limited assay sensitivity, different construct biology or a failed assay; do not reinterpret that as a positive result for N1002K.

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
   *(Thermal denaturation method, buffer and instrument conditions; the 39.1/34.7 °C full-length
   pair; the 721–1,044 construct definition. Method parameters in §3 are verbatim from this paper's
   Supplemental Experimental Procedures.)*
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

Every experimental parameter in §Procedure Stages 3–5 is quoted from ref 1 and its Supplemental
Experimental Procedures. Where a parameter is **not** in the source — expression strain, induction
conditions, the nanoDSF equivalence argument, the recommendation to purify all constructs
symmetrically — it is marked as ours at the point of use. The ClinVar tabulation is our measurement,
dated. Construct sequences, primer design and costings are in the companion document, each carrying
its own source and date.

**No competing interests.** This work was produced for a public rare-disease hackathon and is
released CC BY 4.0. **No funding or laboratory commitment is attached to it.**
