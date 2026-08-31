# Thermal stability of the *BUB1B* pseudokinase domain carrying the MVA variant p.(Asn1002Lys)

**A protocol for a collaborating laboratory**

| | |
|---|---|
| **Version** | 1.0 — 2026-08-31 |
| **Author** | adriamasnou · *Rare Disease, Real Kid: The MVA Hackathon 2026* |
| **Licence** | CC BY 4.0 |
| **Companion document** | [`n1002k-reagent-specification.md`](n1002k-reagent-specification.md) — construct design, orderable sequences, costings |
| **Biosafety** | **BSL-1.** *E. coli* K-12/B-derivative expression host; synthetic dsDNA; no human material, no pathogen, no controlled-access data |
| **Estimated reagent cost** | **≈ $290–330** (list, §Materials) |
| **Estimated timeline** | **~3 weeks** elapsed; ~4 days hands-on (§Timing) |

---

## Abstract

Mosaic variegated aneuploidy syndrome 1 (MVA1, MIM 257300) is caused by biallelic loss of function
in *BUB1B*, encoding the spindle-assembly-checkpoint protein BubR1. Five missense variants in the
BubR1 pseudokinase domain (aa 721–1,044) are published to act by destabilising the fold and lowering
cellular protein abundance; one in-domain variant is published not to. **The variant
p.(Asn1002Lys) has never been assayed by any method.** It matters because it occurs in a patient
in whom the second allele, `p.(Leu737*)`, is a nonsense-mediated-decay substrate — so **essentially
all BubR1 protein in that individual is N1002K**, and whether it is destabilised or merely
functionally impaired at normal abundance determines whether protein-stabilising approaches are
mechanistically coherent for this genotype at all.

This protocol measures the melting temperature (Tm) of recombinant HIS₆-BubR1(721–1,044) wild-type
and N1002K, purified from the same expression batch and denatured side by side, using the buffer and
readout conditions of the published series so the result is comparable to it. **The interpretation of
each possible outcome is pre-registered in §Anticipated results and is not to be revised after
unblinding.**

**Keywords:** BUB1B · BubR1 · pseudokinase · protein thermostability · nanoDSF · mosaic variegated
aneuploidy · variant functional characterisation · ACMG PS3

---

## Introduction

### Background

BubR1 is a core component of the mitotic checkpoint complex. Its C-terminal domain (aa 721–1,044) is
a **pseudokinase** — catalytically inactive in vertebrates — whose role appears to be structural and
scaffolding rather than enzymatic (**PMID 22698286**, ref 1). Suijkerbuijk *et al.* established that
several MVA-associated missense variants in this domain reduce BubR1 abundance by destabilising the
fold, and demonstrated the effect directly by thermal denaturation of the recombinant domain
(**PMID 22698286**) and by chaperone-dependence in cells (**PMID 20516114**, ref 2).

### The gap

`p.(Asn1002Lys)` (`NM_001211.6:c.3006T>G`) lies within the pseudokinase domain. It is **absent from
every functional dataset**: it is not among the variants characterised in refs 1–2, it is not
represented in any public reagent repository (Coriell and Addgene searched record by record), and two
independent pre-registered computational attempts by this project terminated at their own decision
rules without returning a usable score.

### What this protocol does and does not deliver

**Delivers:** the first functional measurement of any kind for this allele; an absolute Tm anchor for
the HIS₆-BubR1(721–1,044) fragment, for which none is published; and a data point toward the
control set a future expert panel would require.

**Does not deliver:** ACMG PS3-level evidence. §Limitations sets out why, with the measurement that
establishes it. **This is stated at the front rather than buried, because a protocol that oversells
its evidentiary reach wastes the time of whoever runs it.**

---

## Materials

### Biological materials

| Item | Source | Notes |
|---|---|---|
| *E. coli* expression host | BL21(DE3) or equivalent | **Not specified in ref 1**, which states only *"expressed in E. coli"*. BL21(DE3) is our recommendation for a T7-driven His-tagged construct, not a source parameter. |
| Cloning host | DH5α or equivalent | For plasmid propagation |

### DNA constructs

| Construct | Source | Cost |
|---|---|---|
| **HIS₆-BubR1(721–1,044) WT**, 972 bp CDS | **Synthesise.** Sequence in companion document §3 | Twist Clonal Gene, 9¢/bp ≈ **$87** + vector $35–55 |
| **HIS₆-BubR1(721–1,044) N1002K**, 972 bp | **Synthesise.** Sequence in companion document §3 | as above |

> **CRITICAL** — Order both constructs as **cloned, sequence-verified genes** (e.g. Twist *Clonal
> Genes*, specified *"100% sequence perfect, NGS verified"*), **not** as linear gene fragments. Order
> them **in the same run**. The measurement is a ΔTm between two constructs that must differ at
> exactly one base; two synthesis batches introduce differences the experiment cannot separate from
> the variant. See companion document §3 for the full rationale and a documented trap involving
> silent siRNA-resistance edits present in the deposited pLAP-BUBR1 plasmids.
>
> **CRITICAL** — The fragment is **internal to the ORF**: no start codon, no stop codon. Ensure the
> destination vector supplies an N-terminal HIS₆ tag **in frame**, and that a stop codon is present —
> append `TAA` if the vector does not provide one. **Do not codon-optimise.** Optimisation would break
> the requirement that the two constructs be identical outside the edit.

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

> **CRITICAL** — Run all four conditions for **both** constructs. Nucleotide and metal binding shift
> Tm, and a ΔTm measured under only one condition can miss a difference that appears under another —
> or manufacture one. The panel is the control.

---

## Procedure

### Stage 1 · Construct preparation ● TIMING 1–2 weeks, mostly waiting

1. Order both constructs as cloned, sequence-verified genes per §Materials. **TIMING** 4–7 business
   days express, 10 standard.
2. Transform into the cloning host; prepare plasmid DNA.
3. **Verify by whole-plasmid sequencing** (e.g. Plasmidsaurus, $15/sample, overnight).
   **CRITICAL STEP** — The acceptance criterion is **exactly one difference between the two
   constructs, at the intended position, and no other difference anywhere in either plasmid.** Not
   "the edit is present" — *only* the edit is present. Whole-plasmid rather than Sanger sequencing,
   because polymerase-based steps introduce second-site mutations that a targeted amplicon cannot see.
   ■ **PAUSE POINT** — plasmid stocks are stable indefinitely at −20 °C.

### Stage 2 · Expression ● TIMING 2 days

4. Transform both plasmids into the expression host **in parallel, on the same day, from the same
   competent-cell batch.**
5. Express both constructs **in the same experiment**, under identical induction conditions.
   **CRITICAL STEP** — Batch is a confounder for every downstream comparison. WT and N1002K must
   travel together from this step onward.
   > ⚠️ **Induction temperature, IPTG concentration and duration are NOT specified in ref 1** and are
   > left to the laboratory. Whatever is chosen must be **identical for both constructs**, and should
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
12. **Polish both constructs identically.**
    > 🔴 **CRITICAL STEP — a methodological asymmetry in the source, which we flag so that
    > reproducing it is a decision rather than an inheritance.** Ref 1 applied **size-exclusion
    > chromatography (Superdex S75) to WT only**, while *"the point mutants … were dialyzed"*. SEC
    > removes aggregate and misfolded species. Applying it to WT alone could flatter WT's apparent
    > stability relative to the mutant, in the same direction as the hypothesis under test. **We
    > recommend treating both constructs identically — SEC both, or dialyse both.** If you reproduce
    > the published asymmetry for comparability with ref 1, we suggest running the symmetric version
    > alongside it. The source does not comment on this. **[Our observation on reading the method.]**
13. Assess purity and integrity by SDS-PAGE.
    **CRITICAL STEP** — Confirm expression **before** any melting run. A construct that does not
    express cannot produce a melting curve, and a flat curve would otherwise be interpreted as a
    result. ? **TROUBLESHOOTING**

### Stage 4 · Thermal denaturation ● TIMING 1 day

14. Prepare WT and N1002K at matched concentration in each of the four conditions in §Reagent setup.
15. **Melt WT and N1002K side by side in the same run.** **CRITICAL STEP** — The measurement is the
    ΔTm between them. Absolute Tm compared across runs is not the endpoint.
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

20. Acquire far-UV CD spectra for both constructs ± 10 mM MgCl₂ / 250 µM AMP-PNP, temperature ramped
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
| 19 | ΔTm inconsistent across preparations | Batch effect; asymmetric purification | Confirm WT and mutant were purified identically (Step 12) and travelled together from Step 4 |

---

## Anticipated results

**Pre-registered. This section is written before any data exist and is not to be revised once a
result is known.**

The published orientation for the size of a destabilising shift in this protein is **WT 39.1 °C vs
K795A 34.7 °C**<sup>1</sup> (Fig 3G/S3D). ⚠️ **That pair was measured on full-length GST-BUBR1, not
on the 721–1,044 fragment, and there is no published Tm for this fragment at all.** It is an
expectation of magnitude, **not a control for this construct**, and must not be used as an
acceptance gate.

### Outcome A — N1002K is destabilised (ΔTm negative, beyond preparation-to-preparation variance)

- Converts an **inference by class into a measurement on this patient's actual protein.** The
  destabilisation mechanism was established for I909T, L1012P, R727C, R814H and L844F
  (**PMID 20516114**) — **not** for N1002K. **[OUR INFERENCE — that the class reading does not
  transfer to an unassayed in-domain variant; the variant series is the source's.]**
- **Sharpens an HSP90 contraindication from a class prediction to an allele-specific one.**
  Geldanamycin severely depletes destabilised BubR1 mutants while barely affecting
  WT<sup>2</sup>. If N1002K is destabilised, that caution — currently the single most clinically
  actionable output of this project — stops being an extrapolation.
- Makes temperature-rescue and chaperone-modulation arms testable for this genotype
  (27/33 °C, ref 1 Fig 3H/S3E–F).
- 🔴 **It does not establish that any drug helps.** It establishes that the lesion is of a *kind* that
  stabilisation could in principle address. The distance from there to a paediatric therapy is large
  and is not shortened by this result.

### Outcome B — N1002K behaves like wild-type (no ΔTm)

**This is the outcome with the larger consequences, and it is negative for the hypothesis that
motivated the experiment.**

- The standing alternative — that the pseudokinase domain can be functionally impaired **at normal
  protein level**, via PP2A-B56 recruitment rather than folding — becomes the leading reading of this
  genotype.
- **A protein-abundance-raising strategy would be misdirected for this patient**, and several
  independent groups are currently pursuing exactly that direction with different molecules.
- 🔑 **This is arguably the more valuable result, and it is the reason the experiment is worth running
  regardless of direction.** A negative redirects effort currently being spent on an untested premise.

### Outcome C — Ambiguous (ΔTm within preparation variance)

Report as indeterminate with the measured variance. **Do not resolve an ambiguous result by adding
preparations until it reaches significance.** The pre-registered n is ≥3; any extension beyond it is
a separate, declared analysis.

---

## Limitations

**This experiment, executed perfectly, does not reach ACMG PS3-level evidence, and we would rather
say so than have it discovered downstream.**

The governing standard is ClinGen's Sequence Variant Interpretation recommendation for the PS3/BS3
codes (**PMID 31892348**, ref 3): *"a minimum of 11 total pathogenic and benign variant controls are
required to reach moderate-level evidence in the absence of rigorous statistical analysis."*

**Those controls do not exist for this domain.** All **449** in-domain (aa 721–1,044) missense records
in ClinVar, by **aggregate** germline classification:

| Aggregate germline classification | Records |
|---|---|
| **Uncertain significance** | **430 (96%)** |
| Conflicting classifications | 9 |
| Likely benign | 8 |
| Benign / Benign–Likely benign | 2 |
| 🔴 **Pathogenic or Likely pathogenic** | 🔴 **0** |
| **provenance** | **[OUR MEASUREMENT — all 449 in-domain (aa 721–1,044) missense ClinVar records, by aggregate germline classification, 2026-08-30.]** |

The BubR1 pseudokinase domain is a **variant-of-uncertain-significance desert**: 96% uncertain, and
**not one pathogenic or likely-pathogenic in-domain missense record** available to serve as a
positive control against the 11 that **PMID 31892348** requires. There is additionally **no ClinGen
Variant Curation Expert Panel for *BUB1B***, so no body currently exists to make the assay-scoping
decision that would set the achievable ceiling. **[OUR MEASUREMENT and OUR INFERENCE — the ClinVar
tabulation is ours (2026-08-30); the control-count requirement is ClinGen's; the conclusion that the
two cannot currently be reconciled for this domain is ours.]**

Further limitations, stated plainly:

- **A single-domain thermostability measurement is not a measurement of checkpoint function.** It
  addresses folding, not activity.
- **Recombinant fragment behaviour need not predict full-length behaviour in cells.**
- **n = 1 variant against WT** is a two-point comparison, not a calibrated assay.

---

## What is being asked, and what is not

- **No clinical recommendation is made or intended.** Nothing here constitutes advice about the care
  of any patient, and no contact with the family is sought or permitted.
- **This project has no wet laboratory.** Everything here is specification; we cannot run it.
- **No controlled-access data or material is involved.** The only patient-derived information
  required is the variant string `BUB1B NM_001211.6:c.3006T>G, p.(Asn1002Lys)`, which is already
  public two independent ways — via a CC-BY hackathon submission, and via an existing ClinVar VUS for
  the identical protein change through `c.3006T>A`.
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
conditions, the nanoDSF equivalence argument, the recommendation to purify both constructs
symmetrically — it is marked as ours at the point of use. The ClinVar tabulation is our measurement,
dated. Construct sequences, primer design and costings are in the companion document, each carrying
its own source and date.

**No competing interests.** This work was produced for a public rare-disease hackathon and is
released CC BY 4.0. **No funding is attached to it and none is sought.**
