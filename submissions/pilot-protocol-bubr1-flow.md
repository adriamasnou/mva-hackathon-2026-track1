# Pilot: can BubR1 abundance be measured by intracellular flow cytometry?

**Proposed assay qualification; clinical-source corrections integrated 23 October 2026.** Historical protein measurements are contextual examples, not an expected N1002K range or a therapeutic threshold. This pilot has not been performed.

**The gate that comes before the screen — and it is now a much cheaper gate than this protocol
originally assumed.** Neither antibody this protocol first shortlisted is vendor-validated for flow
cytometry. **But other anti-BubR1 clones are, and we were wrong to say otherwise.**

> 🔴 **THE ORIGINAL CLAIM IS FALSIFIED — corrected 2026-08-30, and the correction is good news.**
> This section used to open: *"**No** anti-BUBR1 antibody is validated for this application **by
> any vendor**, and no published precedent exists."* **That rested on checking exactly two
> products** — `A300-386A` and `BD 612502` — and a two-catalogue check cannot license a market-wide
> negative. Adrià pulled the Novus/Bio-Techne catalogue. **Eight anti-BubR1 products across four
> clones list Flow Cytometry as a validated application, and several publish an intracellular flow
> histogram on the datasheet.**
>
> | catalogue | clone | host / isotype | flow, as listed | vendor flow figure |
> |---|---|---|---|---|
> | **MA1-16577** *(Invitrogen/Thermo — a **second, independent supplier of the same clone**)* | **8G1** | mouse IgG1κ | **1 µg per 10⁶ cells** | — WB/ICC figures; positive control **HeLa**; RRID **AB_568472** |
| **NB100-353** · **NBP2-80606** | **8G1** | mouse IgG1κ | **1 µg per 10⁶ cells** · *CyTOF-ready* | ✅ **intracellular stain, HeLa, 4% PFA / 0.1% saponin, 5 µg/mL 30 min RT, vs a matched isotype control**, DyLight 650 direct conjugate |
> | **NB100-353AF350** | 8G1 | mouse IgG1κ | listed; dilution to be determined | — **directly conjugated (Alexa Fluor 350)** |
> | NB100-353CL1 | 8G1 | mouse IgG1κ | listed | — (CoraFluor 1 conjugate) |
> | **NBP1-47680** · **NBP2-70314** | OTI6E5 | mouse IgG1 | **1:100** · *CyTOF-ready* | ✅ **HEK293T transfected with BubR1 vs empty vector** — a specificity control by overexpression |
> | **NBP3-15207** | 7H4 | **rabbit** IgG | listed | ✅ overlay histogram, HeLa, 70% EtOH fix, **1 µg/10⁶ cells**, FITC goat-anti-rabbit |
> | **NBP3-51987** | 23GB1640 | rabbit IgG | listed | — **"Knockdown Validated"** |
>
> **What survives of the original claim, stated precisely:** the two antibodies this protocol
> shortlisted are still not flow-validated, and **a peer-reviewed precedent for quantifying BubR1
> abundance by flow is still not established** — a vendor datasheet figure is the manufacturer's
> own data, not an independent publication, and this protocol does not treat the two as equal.
> **What does not survive is the word "any vendor".**
> [Novus datasheets v.20.1, retrieved 2026-08-30, held at `papers-local/datasheets/`; catalogue
> numbers resolve at `novusbio.com/<cat>`. **Thermo `MA1-16577` and BD `612502` read directly from
> the vendor product pages on 2026-08-30** — both had returned HTTP 403 to an automated fetch the
> same day, so this is the check that was recorded as deferred, now done.]

- **Neither originally shortlisted antibody is vendor-validated for flow cytometry.** `A300-386A`
  is validated for western blot and immunoprecipitation only. **`BD 612502` is listed by BD for
  *"Western blot (Routinely Tested), Immunofluorescence (Tested During Development)"* — and
  nothing else.**
  🔻 **CORRECTED 2026-08-30.** This line used to say 612502 was validated *"for WB, IF, ELISA, ICC
  and IP"* — **five applications where BD lists two**, one of which BD qualifies as only *tested
  during development*. We overstated a reagent's validation, in the document whose entire subject
  is that validation matters. **[VERIFIED — BD Biosciences product page for 612502, read
  2026-08-30: clone 9/BUBR1, mouse **IgG2a**, immunogen human BUBR1 aa 276–388, 250 µg/mL,
  RRID **AB_2066085**, RUO.]**
- **No *published* precedent for the readout.** Of 39 papers citing `A300-386A`, six also mention
  flow — and in every case the antibody sits in a *western-blot* list while the flow is doing
  something unrelated. Co-occurrence, not usage. **This still holds**, and it is about
  `A300-386A`; it says nothing about 8G1, OTI6E5 or 7H4, which no longer need it.

### 1.1 ★ What this changes in the protocol

**[OUR INFERENCE]** — the four items below are our reading of the datasheet evidence above,
not claims made by any vendor. The underlying facts (applications, hosts, clones, dilutions,
figure legends) are `[VERIFIED]` from the datasheets at `papers-local/datasheets/`, retrieved
2026-08-30 from `novusbio.com`; what to *do* about them is ours.

1. **★ Start with `NB100-353` (clone 8G1). [OUR INFERENCE from the datasheet facts above; the datasheets themselves are held at `papers-local/datasheets/`, retrieved 2026-08-30 from `novusbio.com`.]** It is the only option with a **published intracellular
   flow protocol on the HeLa reference line used in Matsuura's fibroblast immunoblot comparison** — including
   fixation, permeabilisation, concentration, incubation and an isotype control. That replaces
   §5.1's blind `1:50–1:800` titration with a **published starting point: 4% PFA, 0.1% saponin,
   5 µg/mL, 30 min RT**, and the titration becomes a confirmation rather than a search.
2. **★ The two-colour species clash dissolves.** `screen-protocol-runnable.md` §10 pairs BubR1 with
   α-tubulin `sc-32293` (clone DM1A, **mouse**), which collides with a mouse BubR1 primary. Two
   clean exits now exist: **(a)** use the **rabbit** clone **7H4 (`NBP3-15207`)** for BubR1 and keep
   mouse DM1A — two hosts, two secondaries, no isotype gymnastics; or **(b)** use a **directly
   conjugated** 8G1 (`NB100-353AF350`, Alexa Fluor 350) and skip the BubR1 secondary entirely.
3. **`NBP3-51987` is "Knockdown Validated"** by the vendor — the same specificity evidence §5.6's
   dsiRNA arm exists to generate. Worth ordering as the confirmatory reagent even if 8G1 is the
   primary workhorse.
4. **`CyTOF-ready` on 8G1 and OTI6E5** is independent evidence that these clones survive fixation
   and permeabilisation in single-cell suspension, which is the property the whole readout depends
   on.

**A screen built on an unvalidated readout is not a screen.**

## 2. Historical protein measurements and their limits

Matsuura *et al.* 2006 (PMID 16411201) studied PCS/MVA families. The title's use of
"monoallelic" and "PCS" does not make the patients irrelevant to MVA. The important limits
are the genotypes, cell preparations, assay and reference used.

**Figure 3A:** BubR1 immunoblot intensities in fibroblast lines from patients 1, 2 and 5 were
**22%, 25% and 29% of the HeLa reference**, normalised to α-tubulin. The Methods (pp.359–360)
describe **SV40 transformation followed, after crisis, by phTERT transfection**. These are
transformed-fibroblast immunoblot measurements, not intracellular-flow measurements in LCLs.

**Figure 1 and mutation results (PMID 16411201):** these three patients had a detected truncating BUB1B alteration
and no second mutation explaining disease identified by the methods used. Patients 1 and 2
carried the **6G3** second haplotype; patient 5 carried **6G8**. The study's failure to detect a
second mutation does not establish its absence, and the haplotype label is not itself a proven
causal sequence variant. These models differ from the present unphased nonsense-plus-missense
pair. **The child's phase, NMD, protein abundance and N1002K function remain unmeasured.**

**Figure 3B:** the separate EBV-transformed LCL experiments include family 2 values of **57%**
for the father, **71%** for the mother and **22%** for the patient, relative to a normal reference
at 100%. Other normal-individual lanes include **63%, 112% and 158%**. Truncating-allele carrier
lanes include **13%, 21%, 29% and 57%**; the paper's prose summary of 21–57% omits the 13% lane.
Values vary widely and overlap between groups. The affected R36Q case has approximately normal
abundance (**102% in Figure 3B, 104% in the prose**). Neither these individual values nor the
three fibroblast measurements define a diagnostic reference interval or an expected N1002K signal.

**Qualify specificity, linearity, normalisation and precision independently of the patient value.**
A measured level outside these examples may reflect biology, cell model or measurement. Use
qualified depletion controls, dilution/linearity and orthogonal protein measurement to distinguish
these. Do not tune the assay to force a patient into a historical abundance band. Criterion 3
tests measurement performance; the observed patient abundance remains a result. **[OUR INFERENCE]**

## 3. 🔴 The precision the assay must reach — derived, not asserted

This is the calculation the screen protocol could not do, and it produces a trap worth naming.

For assay design, consider a **hypothetical two-fold abundance increase from 25% to 50%** of a reference control. Neither 25% nor a clinically meaningful two-fold rescue has been measured for this child or N1002K. The following is an engineering precision calculation under an equal-CV assumption, not a therapeutic threshold. Using
the Assay Guidance Manual's own Z′ definition, with CV equal in both populations:

```
Z' = 1 - 3·CV·(hi + lo) / (hi - lo)
```

| what is being resolved | Z′ target | **maximum assay CV** |
|---|---|---|
| illustrative low vs reference — **25% vs 100%** *(the easy comparison)* | ≥ 0.4 | **≤ 12.0%** |
| **a 2-fold hit — 25% vs 50%** *(chosen engineering target)* | ≥ 0.4 | **≤ 6.7%** |
| the same, comfortably | ≥ 0.5 | ≤ 5.6% |
| the same, bare 3σ separation | 0.0 | ≤ 11.1% |

> ### 🔴 The trap: the easy comparison is **~1.8×** more forgiving than the one that matters.
> Separation of a patient and control does not establish precision for a smaller change. In this
> **hypothetical contrast**, separating 25% from 100% permits CV ≤ 12%, while separating 25% from
> 50% requires **CV ≤ 6.7%** at the chosen Z′ target.
> **CV ≤ 6.7% is therefore the proposed engineering target for this contrast**, not a measured
> N1002K baseline or a guarantee of detecting a clinically meaningful rescue. Qualify the model
> in the actual assay before confirmation; "clear separation" alone is insufficient.
> 🔻 **"~3×" corrected to "~1.8×" on 2026-08-31.** **12.0 / 6.7 = 1.79.** The figure 3 is the value
> of `(hi+lo)/(hi-lo)` for the hard comparison (50 vs 25 → exactly 3.000), not the ratio between
> the two CV allowances — it was read off the wrong quantity in the same derivation. Both limits
> re-derived from this file's own formula and both are correct: at Z′ = 0.4,
> `CV = 0.6 / (3 × (hi+lo)/(hi−lo))` gives **12.00%** for 100 vs 25 and **6.67%** for 50 vs 25.
> **The allowance ratio is 1.8×, conditional on these chosen contrasts and equal-CV assumptions.**
> [OUR MEASUREMENT — arithmetic, 2026-08-31.]

## 4. Materials — catalogue numbers

| item | source | identifier |
|---|---|---|
| **anti-BUBR1, clone 9** (primary) | BD Transduction | **612502** (50 µg) / **612503** (150 µg) — mouse monoclonal IgG2a, aa 276–388, **knockout-validated** |
| isotype control | BioLegend **400287** (purified) | **mouse IgG2a κ, clone MOPC-173** — matched **µg/mL**, not matched dilution. ⚠️ *For an isotype control the CLONE and ISOTYPE are what matter; vendors are interchangeable, and BioLegend lists more than one purified format (standard and Go-ChIP-Grade) — confirm the format at ordering.* |
| **Fc receptor block** | BioLegend **422302** (TruStain FcX, RRID AB_2818986) *or* BD **564220** / **564219** (Human BD Fc Block) | 🔴 **mandatory — these are EBV-transformed B cells.** BD's own guidance specifies **10 min before staining**, matching §5.3 |
| **fixable viability dye** | Thermo **L34976** (LIVE/DEAD Fixable **Near-IR**, 633/775) | must be **fixable** (PI/7-AAD do not survive fix), **and spectrally clear of Alexa 488** |
| knockdown host line | ATCC | **HeLa CCL-2** (RRID **CVCL_0030**) or **U2OS HTB-96** (RRID **CVCL_0042**) — both verified via Cellosaurus |
| secondary | Jackson ImmunoResearch **715-545-150** | **Alexa Fluor 488 AffiniPure Donkey Anti-Mouse IgG (H+L), *min X*** — flow-validated. 🔴 ***min X* is not optional here: see below** |
| **patient cells** | NIGMS/Coriell | **GM21284** (LCL, *BUB1B* `753X`/`R814H`) |
| **normal-abundance reference** | NIGMS/Coriell | **GM12878** (CEPH/HapMap LCL) **plus ≥1 further unrelated apparently-healthy LCL** — see the 🔴 box below |
| positive control (raises BubR1) | Calbiochem | **MG132**, CAS **133407-82-6** |
| **specificity control** | **Gama Braga 2020**, *Cell Rep* 33:108397 (PMID 33207204) — see the citation note in §5.6 | **dsiBUBR1 5'-GUCUCACAGAUUGCUGCCUCAGAGC-3'**, published at **20–50 nM** |
| mitotic arrest (optional arm) | Sigma | nocodazole **M1404-10MG** |

> 🔴 **CORRECTED 2026-08-30 — the previous control lines were wrong, and wrong in the direction
> that would have broken the assay.** This table used to name **GM21657** and **GM22004** as
> "unaffected parent LCLs". Coriell's own records, fetched to check, say otherwise:
>
> | line | what Coriell actually says | why it cannot be the 100% denominator |
> |---|---|---|
> | **GM21657** | *"MOSAIC VARIEGATED ANEUPLOIDY SYNDROME 2; MVA2 · CENTROSOMAL PROTEIN, 57-KD; CEP57"*, father of GM21654/GM21655 | A *CEP57*-family comparator; the quoted relationship alone does not verify a molecular carrier genotype or a normal BubR1 reference value |
> | **GM22004** | *"MOSAIC VARIEGATED ANEUPLOIDY SYNDROME 1; MVA1"*, *"father of an affected child (GM22006)"* | A family comparator **pending molecular genotype verification**; fatherhood and an MVA1 catalogue label alone do not establish a heterozygous *BUB1B* genotype |
> | **GM21284** | *"parental cell lines not in the repository"* | Neither of the two quoted family relationships identifies a parent of GM21284; its held catalogue record does not list available parental lines |
>
> **Comparator selection matters.** A carrier must not silently become an unaffected reference.
> Matsuura's LCL examples show wide variation and overlapping values, including the normal and
> carrier lanes listed in §2; they do not supply reference limits for this flow assay. A carrier
> with lower BubR1 could compress a patient/control contrast, but the direction and size must be
> measured in the actual lines. No patient/control abundance band is an acceptance criterion.
>
> **The replacement, and why it is defensible.** The reference must be **unrelated to any MVA
> family**, apparently healthy, and an LCL so that cell type matches. **GM12878** is a
> CEPH/HapMap pedigree-1463 B-lymphocyte line. *Full disclosure from its Coriell record: it carries* `CYP2C19*2`,
> *a pharmacogenetic splice variant with no relationship to BubR1 abundance.* **Use at least two
> unrelated controls** to characterise between-line variation; neither is required to reproduce
> a historical percentage. Criterion 3 concerns linearity and orthogonal agreement in the chosen cells.
> The *CEP57* lines **GM21654 · GM21655 are disease comparators**. A different causal MVA gene
> does not make them BubR1-negative or establish antibody specificity. Reserve specificity
> assessment for **qualified BubR1 depletion and orthogonal validation in §5.6**.
> **GM21657 and GM22004 may be run as family comparators**, with the molecular genotype recorded
> as unverified unless a source explicitly establishes it. Use a carrier label only after that
> verification; neither family relationship alone defines a normal-abundance denominator.

Cell lines ~**$262 US-academic / $448 international** each, MTA required.

## 5. Method — bench level

### 5.0 Culture

LCLs are EBV-transformed suspension B-cell lines. **The repository publishes the conditions per
line, and these are GM21284's own, taken from its catalogue record rather than assumed:**

| | |
|---|---|
| medium | **RPMI-1640 with 2 mM L-glutamine** (or equivalent) |
| serum | **15% fetal bovine serum — NOT heat-inactivated** |
| temperature / atmosphere | **37 °C, 5% CO₂** |
| subcultivation | **split ratio 1:4**, by dilution — add fresh medium |

🔻 **An earlier version of this section specified a density window of "3 × 10⁵ to 1 × 10⁶ cells/mL".
That was invented.** The repository specifies a **split ratio, not a density**, and the
"not heat-inactivated" instruction is a real one that a lab defaulting to heat-inactivated FBS would
silently violate. **[VERIFIED — Coriell/NIGMS catalogue record for GM21284.]**

Expand for **≥ 2 passages after thaw** before any measurement; freshly thawed LCLs are not in steady
state. **[OUR CONVENTION — not specified by the repository.]**

### 5.1 🔴 STEP ONE: antibody titration. This is not optional.

The antibody is **not validated for flow**, so **no dilution can be assumed** — the IF and WB
dilutions on the datasheet are for other applications and other fixation chemistries.

**Titrate before anything else:** 1:50 · 1:100 · 1:200 · 1:400 · 1:800, on control LCLs, stained
alongside a matched isotype at each concentration.
**Compare dilutions using an adapted stain index.** Maecker *et al.* (*Cytometry A* 2004,
PMID 15536642, p.173) support assessing separation relative to the spread of the negative
population and permit medians as an alternative to means. The following median/MAD implementation
and control choice are **our proposed adaptation**, not a published BubR1-flow validation:

```
MAD_negative = median(|x_negative − median(x_negative)|)
robust_SD_negative = 1.4826 × MAD_negative
adapted_stain_index = (median_stained − median_negative) / (2 × robust_SD_negative)
```

Calculate this on **linear compensated fluorescence values**, retaining negative compensated
values without clipping or adding an offset; log/biexponential plots are for display and do not
change the calculation. Use the same qualified live-singlet gate for the matched samples. If the
negative dispersion is zero or non-finite, mark the index undefined and investigate rather than
assigning infinite separation. Freeze the estimator, scale and control definition before
confirmation. **[OUR ANALYSIS CHOICE]**

The proposed negative population is a **same-line, same-preparation, concentration-matched
isotype control**, intended to assess background under the chosen staining conditions. Check it
against unstained and secondary-only controls and appropriate single-stain/FMO controls for
multicolour interpretation. An isotype control alone cannot establish target specificity or
eliminate spreading error. The biological depletion and orthogonal checks in §5.6 remain required.
Select a concentration with useful separation and acceptable background, then confirm it in the
actual assay; neither maximal brightness nor a high adapted index alone proves BubR1 specificity.
**[OUR INFERENCE; PROPOSED ANALYSIS]**

### 5.2 Fix and permeabilise

Two conditions, **run in parallel on the first plate**, because BubR1 is nuclear/kinetochore-
associated and detergent versus alcohol permeabilisation are not interchangeable for such epitopes:

| | **Condition A** (published for BUBR1 staining) | **Condition B** (alcohol) |
|---|---|---|
| fix | **4% formaldehyde + 1% Triton X-100 in PBS, 20 min, RT, in the dark** | 4% formaldehyde in PBS, **10 min, RT** |
| permeabilise | (simultaneous, above) | **ice-cold 90% methanol** — vendor protocols specify **90%, minimum 10 min ON ICE**; 30 min is within convention but the published minimum is 10 |
| wash | 2 × 200 µL PBS + 0.1% Triton | 2 × 200 µL PBS |

**Testing both once costs one day. Discovering the wrong one after the screen costs the screen.**

> ### 🔴 A fluorophore constraint on Condition B that a substitution would walk straight into
> **Methanol damages PE and APC and causes loss of signal.** The reagents specified here are safe —
> Alexa Fluor 488 (secondary) and an amine-reactive fixable viability dye, both covalently bound or
> small-molecule — **but a PE-conjugated secondary is one of the most common substitutions a lab
> would make, and in Condition B it would silently lose signal.** ⚠️ **Any substitution into the
> methanol arm must be checked for alcohol compatibility first**, and the fixable viability dye's
> methanol tolerance should be confirmed on the first plate rather than assumed.

### 5.3 Staining — per well, 96-well V-bottom

1. **5 × 10⁵ cells** per well **[OUR CONVENTION]**. Pellet **350 × g, 5 min** — the vendor's own
   published intracellular-staining protocol, not the 300 × g an earlier version specified.
2. 🔴 **FIXABLE viability dye, on LIVE cells, BEFORE fixation.** Amine-reactive fixable stain
   **LIVE/DEAD Fixable Near-IR, Thermo **L34976** (~633 nm ex / ~775 nm em)**, 15 min RT in PBS
   **without protein**, then wash.
   ⚠️ **Not the Aqua variant (L34957).** Aqua emits at **~525 nm** against Alexa 488's **~519 nm** —
   resolvable only by separate lasers, with heavy spillover **into the very channel this assay
   reads**. Near-IR sits **250 nm away on a different laser**, so spillover into the BubR1 channel
   is negligible. **The dye choice is part of the CV budget, not a detail.** **Conventional PI or 7-AAD do NOT survive fixation and permeabilisation** — using one
   here would put dead cells back into the analysis gate, and dead cells bind antibody
   non-specifically. **This step must precede fixing; it cannot be added later.**
3. 🔴 **Fc RECEPTOR BLOCK — mandatory, and specific to this cell type.**
   **These are EBV-transformed B-lymphoblastoid lines, and EBV transformation *increases* Fcγ
   receptor number per cell.** A mouse IgG2a monoclonal will bind FcγR non-specifically on every
   line in this pilot. Block with **human Fc receptor blocking reagent** (BioLegend TruStain FcX
   **422302**, or BD Human Fc Block **564220**), **10 min RT before the primary antibody**, per
   the manufacturer's volume.
   > **This is not a refinement.** Unblocked FcγR binding raises background in *all* arms, **adds
   > variance to the very CV that §3 requires to be ≤ 6.7%**, and can blunt the knockdown response
   > that criterion 2 depends on. An isotype control measures this artefact; it does not remove it.
4. Fix/permeabilise per §5.2. Pellet, wash twice.
5. **Block: 50 µL TBS + 0.1% Triton X-100 + 2% BSA, 30 min, RT.**
6. **Primary: 50 µL at the titrated concentration in block buffer, 20 min at room temperature,
   IN THE DARK** — the vendor's published intracellular-staining protocol, which specifies *"a
   predetermined optimum concentration … for 20 minutes in the dark at room temperature"*.
   🔻 **An earlier version of this protocol said 1 h RT. That was convention; 20 min in the dark is
   the published condition.** Whichever is used, **hold it constant across every plate and day.**
   🔑 **Note that the vendor protocol itself says "predetermined optimum concentration" — the
   titration in §5.1 is the vendor's own requirement, not an extra step invented here.**
7. Wash **2 × 200 µL** block buffer.
8. **Secondary: 50 µL anti-mouse Alexa 488 (**715-545-150**) in block buffer, 30 min RT, protected
   from light.** Dilution **1:500 [OUR CONVENTION — a starting point]**; the vendor does not publish
   a flow-specific dilution, and §5.1's titration applies to the secondary too.
   > 🔴 **Why the *min X* secondary is mandatory rather than preferred.** **LCLs are B cells — they
   > PRODUCE immunoglobulin.** A donkey anti-mouse secondary without minimal cross-reactivity
   > screening can bind human Ig, and on an immunoglobulin-producing cell that is not a small
   > background — it is background proportional to the very cells being measured. **715-545-150 is
   > the *min X* product; a non-min-X anti-mouse secondary is the wrong reagent for this cell type.**
9. Wash 2 × 200 µL. **Resuspend in 200 µL PBS + 1% BSA.** Acquire same day.

**Compensation.** This is a **two-colour** experiment (Alexa 488 + viability dye). Acquire
**single-stain controls on the same cells, same day**: unstained · viability-only · Alexa-488-only.
Compensation set from beads alone is not adequate when one dye is amine-reactive on cells.

### 5.4 🔴 Gating strategy — stated explicitly, because a flow assay without one is not defined

1. **FSC-A vs SSC-A** → the intact lymphoblast population, excluding debris at low FSC. Qualify
   this gate in representative pilot samples from each chosen line before freezing it; a
   control-only boundary must not silently exclude an altered patient-cell population (§5.10).
2. **FSC-H vs FSC-A** → **singlets.** Doublets carry double the signal and will otherwise widen the
   CV — which is the exact quantity this pilot must minimise.
3. **Viability dye vs FSC-A** → live cells only. Dead cells bind antibody non-specifically and
   inflate both signal and variance.
4. **BubR1 (Alexa 488) histogram** on the live-singlet gate.
5. **Report the MEDIAN fluorescence intensity of that gate**, not the mean — flow distributions are
   right-skewed and the mean is unstable to outliers.

**Events per well — derived from the CV budget, not chosen.** The per-well statistic is a median,
whose sampling error must be negligible against the **6.7%** between-well budget, or the assay's
measured precision is limited by counting rather than by biology. Using
`SE(median) ≈ 1.2533·σ/√n`, and targeting **SE ≤ 0.67%** (one tenth of the budget):

| within-well population CV | events needed |
|---|---|
| 30% (tight stain) | ≥ 3,150 |
| **50% (typical protein stain)** | **≥ 8,748** |
| **80% (broad stain)** | **≥ 22,395** |

> **Collect ≥ 25,000 live singlet events per well**, and **set the final count from the spread
> actually observed during titration.** 🔻 An earlier version said "≥10,000" — adequate only if the
> stain is tight, and **insufficient at a broad 80% spread**, where counting error alone would eat
> 15% of the CV budget. Keep voltages, gates and compensation **identical
across all wells, plates and days**; changing them between conditions invalidates every CV computed.

> 🔻 **RAISED FROM 20,000 TO 25,000 ON 2026-08-31 — because 20,000 failed the same test that
> retired 10,000.** The table three lines above requires **≥ 22,395 events at an 80% (broad) stain
> spread**. I re-derived it: `SE(median) = 1.2533 × CV / √n`, so at CV = 80%,
> **n = 20,000 gives SE = 0.709%**, above the 0.67% target — the section recommended a number
> insufficient for exactly the case it had just declared 10,000 insufficient for.
> **n = 22,395 is the exact break-even; 25,000 is the round number above it.**
> **AND §5.10'S EXCLUSION FLOOR WAS STILL SET AT THE RETRACTED VALUE.** Its pre-declared rule read
> *"fewer than 10,000 live singlet events"*, so a well acquired at 12,000 was below §5.4's spec and
> yet **required to be kept and analysed**. That floor is raised to **20,000** — deliberately below
> the 25,000 target, because an exclusion rule should catch acquisition failures, not marginal
> wells. **[OUR MEASUREMENT — arithmetic re-derived 2026-08-31.]**

### 5.5 🔴 How many replicate wells — derived, and it is NOT six

An earlier version of this protocol said "n ≥ 6". **That is wrong, and the error is instructive:
a CV estimated from n wells is itself uncertain, so "observed CV ≤ 6.7%" is not the same claim as
"CV ≤ 6.7%".** With few wells the estimate is so loose that a passing observation demonstrates
nothing.

**Upper 95% confidence bound on the true CV** (χ² sampling distribution of the sample variance).
Reproduce: `python3 pipeline/pilot_n.py`.

| n | observed 3% | observed 4% | observed 5% | observed 6% |
|---|---|---|---|---|
| 3 | 13.2% | 17.7% | 22.1% | 26.5% |
| **6** | **6.3% ✅** | 8.4% ❌ | 10.4% ❌ | 12.5% ❌ |
| 8 | 5.4% ✅ | 7.2% ❌ | 9.0% ❌ | 10.8% ❌ |
| **12** | 4.7% ✅ | **6.2% ✅** | 7.8% ❌ | 9.3% ❌ |
| 24 | 4.0% ✅ | 5.3% ✅ | **6.6% ✅** | 8.0% ❌ |

**Smallest n that actually demonstrates CV ≤ 6.7%:**

| if the assay turns out to be | you need |
|---|---|
| excellent (CV 3%) | n ≥ 6 |
| good (CV 4%) | **n ≥ 10** |
| adequate (CV 5%) | **n ≥ 23** |
| marginal (CV 6%) | **n ≥ 127** — i.e. not demonstrable at any sane plate count |

> ### The rule this produces: **run n = 12.**
> At n = 12 an observed CV up to **4%** demonstrates the criterion. If the observed CV comes back at
> **5–6%, the table tells you immediately that no realistic number of wells will rescue it** — the
> answer is assay optimisation or the reporter-line fallback, **not more replicates.** That is a
> decision you want on day one rather than after three months of adding wells.

**Seven arms (arm 7 added 2026-08-31), n = 12 each = 84 wells — which does NOT fit one 96-well plate under this protocol's own
edge rule**, and the layout below is corrected accordingly. 

> 🔴 **PLATE LAYOUT CORRECTED 2026-08-31 — the design did not fit, by this protocol's own §5.9
> rule.** §5.9 rule 1 says *"**Do not use the outer wells for samples.** Fill row A/H and column
> 1/12 with buffer."* A 96-well plate minus rows A/H and columns 1/12 leaves **6 × 10 = 60 usable
> wells**. The design needs **72** before anything else, and the true requirement is larger still:
> §5.3 mandates single-stain compensation controls (unstained · viability-only · Alexa-488-only,
> plus a DNA-dye single stain once §5.13 makes it three-colour), and **arm 6 is a 2 / 4 / 6 h MG132
> time course — three conditions, not one**. **★ Run the LCL arms across two 96-well plates**, with
> the compensation controls on a third partial plate, and treat "one plate per condition-set" as
> retired. *(Arm 5 is not an LCL arm at all — §5.6 moves the knockdown to reverse-transfected
> adherent HeLa/U2OS at three DsiRNA concentrations, so it never belonged in this count.)*

This is also why
§5.2's two fix/perm conditions fit on two plates run side by side.

### 5.5b The arms

| # | arm | condition |
|---|---|---|
| 1 | patient + **isotype** control | mouse IgG2a at the same µg/mL as the titrated primary |
| 2 | patient + **secondary only** | no primary |
| 3 | **patient + anti-BUBR1** | baseline |
| 4 | **control LCL + anti-BUBR1** | comparison with unrelated LCLs; no required patient/control ratio |
| 5 | **+ BUBR1 knockdown** | specificity — see §5.6 |
| 6 | **patient + MG132** | **10 µM**, with a **2 / 4 / 6 h** time course |
| **7** | **patient + VEHICLE (DMSO alone)** | **matched to arm 6's DMSO concentration, same 2 / 4 / 6 h time course** — 🔻 **ADDED 2026-08-31** |

> 🔴 **WHY ARM 7 HAD TO BE ADDED, AND IT FIXES TWO THINGS AT ONCE.** §5.13b(a) introduces a
> falsifiable cell-cycle rule — *flag a well when any compartment shifts by more than 3 SD of the
> DMSO-control wells on the same plate* — **and there were no DMSO-control wells.** Arms 1–6 are
> isotype, secondary-only, patient + anti-BUBR1, control LCL + anti-BUBR1, knockdown, and
> patient + MG132. **None is a vehicle arm**, so the threshold written specifically to cure an
> unfalsifiable rule was itself unrunnable — its reference population did not exist.
> **The second gap is worse and independent: MG132 is dissolved in DMSO.** Without a vehicle
> comparator, **any BubR1 change produced by the pilot's own positive control cannot be separated
> from the solvent.** Arm 7 is the control that makes arm 6 interpretable, and it should have been
> there from the first draft.

**MG132 at 10 µM is well supported** across the literature held here. ⚠️ **The duration needed for
BubR1 accumulation is NOT** — the published uses are 15 min to 1 h for mitotic arrest, a different
purpose. **Hence the time course rather than a single invented number.**

### 5.6 ⚠️ The knockdown control has a practical problem, and it changes where it is run

`dsiBUBR1 5'-GUCUCACAGAUUGCUGCCUCAGAGC-3'` is directly reported by **Gama Braga 2020**
(PMID 33207204). Delivery and depletion must be demonstrated in the chosen cells; the published
reagent does not establish effective transfection in this LCL model.

**Proposed development arm:** start the knockdown comparison in HeLa or U2OS. A response there
supports reagent qualification but **does not establish specificity in LCLs under this fixation
and flow protocol**. Before screening, demonstrate depletion in the chosen LCL preparation with
a qualified delivery method and an orthogonal protein measurement. Nucleofection is a candidate
delivery approach to qualify, not an assumed successful method. Failed delivery is an
indeterminate specificity test, not proof that the antibody fails. Arms 3–4 remain an LCL
comparison with no prescribed abundance ratio. **[OUR INFERENCE; PROPOSED EXPERIMENT]**

**Knockdown conditions for the adherent arm:** **HeLa (ATCC CCL-2, CVCL_0030)** or **U2OS
(ATCC HTB-96, CVCL_0042)**, reverse-transfected with a standard lipid reagent (e.g. Lipofectamine
RNAiMAX).

🔻🔻 **CONCENTRATION CORRECTED TWICE — read this, because the first correction made it worse.**
An early version specified "10–20 nM". A correction on 2026-08-30 replaced that with a
**0.1 / 1 / 10 nM** dose–response, reasoning from the *manufacturer's* generic DsiRNA guidance
(27mer Dicer-substrate, more potent than a 21mer, often effective at ≤1 nM). **That reasoning was
sound and the answer was wrong**, because generic vendor guidance was preferred over the
verified published protocol for *this exact duplex*.

**Gama Braga et al. 2020 (*Cell Rep* 33:108397, PMID 33207204) — the paper that published this
sequence — states in its Methods, verbatim: `dsiBUBR1 (20-50 nM)`.** The same paragraph runs
`dsiCENP-E` at 50 nM and `dsiBUB1` at 20 nM. **That paragraph does not establish a 1 nM working dose for dsiBUBR1.**
The 0.1 nM floor was **200–500× below** the published working concentration and even the 10 nM
ceiling was 2–5× below it — a titration that could have returned no knockdown and been read as
antibody failure.

**★ USE: a dose–response of `5 / 20 / 50 nM`**, which brackets the published 20–50 nM rather than
sitting under it. Report the knockdown at each dose. If ≥70% knockdown is reached at 5 nM, use the
lowest effective dose for the specificity arm — the manufacturer's off-target argument below is
still correct, it just cannot justify a range that has never been shown to work.

> **Reagent provenance, updated 23 October 2026:** Gama Braga 2020 directly prints this
> dsiBUBR1 sequence in its Key Resources Table and the **20–50 nM** range in its Cell culture
> methods (PMID 33207204). Its table credits Foley 2011 (PMID 21874008), but the exact duplex
> was not identified in the fully read Foley main text or its **now-held, fully read seven-page
> publisher supplement, Figures S1–S6**. The earlier attribution remains unresolved. Cite Gama
> Braga for the verified sequence and reported working range; this is not a claim about unpublished
> material. The proposed **5 / 20 / 50 nM** titration adds a lower dose by design; 5 nM is not a
> reported working dose in the cited paragraph. Different dose labels within Gama Braga's
> Figure S3B also preclude assigning every panel a single exact dose from that figure alone.
> 🔴 **The off-target argument is still real — it just cannot set the dose on its own.** The
> manufacturer's stated reason for low DsiRNA concentrations is **minimising off-target effects**,
> and this arm exists **solely to demonstrate SPECIFICITY**, so an unnecessary excess is a genuine
> hazard inside the one experiment whose purpose is showing the signal is on-target. That is why
> the recommended series **brackets** the published 20–50 nM from below (5 / 20 / 50 nM) and why
> the lowest dose reaching ≥70% knockdown is the one to carry forward. **A concentration that has
> never been shown to work is not the safe choice; it is an uninterpretable one.**

🔴 **Add a POSITIVE transfection control** (e.g. an HPRT DsiRNA), which the manufacturer recommends
in every experiment to assess transfection efficiency. **This protocol had a non-targeting control
but no positive one, and they answer different questions.** Non-targeting says *transfection
perturbs the cells*; a positive control says *the transfection worked at all*.
> **Without it, a failed criterion 2 is uninterpretable** — the antibody may be fine and the
> transfection may simply have failed — **and §7's decision tree would send the project to the
> reporter-line fallback for the wrong reason.** That is the most expensive wrong turn available
> in this document.

**Harvest at 48 and 72 h.** ⚠️ The manufacturer's standard 24 h assay measures **gene expression**;
this measures **protein**, and **BubR1 is stable, so protein depletion lags mRNA depletion.** The
deviation from 24 h is deliberate and reasoned, not an oversight. **[OUR INFERENCE.]**

⚠️ **Confirm depletion by western blot in parallel.** If the flow signal falls but the blot shows no
depletion, the flow readout is measuring something else — a result worth having before the screen,
not after.

### 5.7 How the CV is computed, so criterion 4 is unambiguous

**CV = SD / mean of the per-well MEDIAN fluorescence intensities**, across the **n = 12 replicate
wells of one arm on one plate** 🔻 *(this read "n ≥ 6" until 2026-08-31 — the exact value §5.5
exists to retract. The correction had landed everywhere except the one section that DEFINES the
criterion.)* — *not* the CV of events within a well, which is a different and
much larger number that would fail the criterion for the wrong reason.
Report it **separately for each arm**, and **for arm 3 (patient baseline) it must meet §3's ≤ 6.7%**,
because that is the population the screen actually measures against.

## 5.13 🔴 THE CONFOUND THAT FIVE EARLIER PASSES MISSED — BubR1 abundance is cell-cycle dependent

**BubR1 protein is not constitutively expressed.** It is degraded after mitotic exit via **APC/C-Cdh1**
(it carries a destruction box and KEN boxes) and is **held low through interphase**. Abundance
therefore tracks **what fraction of the population is in mitosis.**

> ### Consequence: anything that increases the mitotic fraction raises measured BubR1 without
> ### touching BubR1 stability at all.
> **This is a large false-positive class for an abundance screen, and none of the screen's three
> counter-screens catches it** — such a compound is not necessarily toxic, it *does* raise BubR1
> specifically, and it would behave similarly across genotypes. **A repurposing library of approved
> drugs contains multiple antimitotics** (taxanes, vinca alkaloids) **and many more compounds that
> perturb the cycle.** It is not an edge case; it is one of the most probable ways this screen
> produces confident nonsense.

**And it confounds this pilot's own positive control**, since MG132 is standardly used to hold cells
in mitosis.

### The fix, and it costs one channel rather than one experiment

**Measure DNA content in the same wells.** The readout is already flow, so this needs no extra plate
and no extra sample:

- Add a **DNA dye on the violet laser** (e.g. DAPI or an equivalent fixable DNA stain) — the violet
  channel is otherwise unused, since the viability dye was moved to Near-IR (§5.2) and the readout is
  Alexa 488. ⚠️ **This makes it a three-colour experiment: single-stain compensation controls are
  required for all three (§5.3).**
- **Report DNA content alongside the primary whole-live-singlet abundance result.** Any secondary
  DNA-content stratification requires qualification in the actual lines; do not select a normal
  diploid peak solely because it makes the abundance comparison easier (§5.13a).
- **Report the cycle distribution alongside every measurement**, and treat any compound that shifts
  it as confounded until shown otherwise.

### 5.13a Characterise the actual population before interpreting a DNA-content gate

**MVA does not establish a universal >25% aneuploid-cell threshold.** Matsuura 2006 Table I
reports **9–32%** aneuploidy in affected patients, including several below 25% (PMID 16411201).
These chromosome-count proportions are not measurements of DNA-content peaks in the proposed
cultures. A descriptive literature phrase such as "usually >25%" cannot define this line's
aneuploid fraction, the cells excluded by a flow gate, or their BubR1 abundance.

A gate based solely on a normal diploid DNA-content distribution **may** distort an aneuploid
culture. The direction and magnitude of that bias depend on the actual cell states, chromosome
changes and assay resolution. Do not assume that excluded cells have less BubR1 or that every
aneuploid cell lies outside a nominal G1 peak. **[OUR INFERENCE]**

For the primary abundance analysis, retain the qualified whole-live-singlet population and report
its BubR1 histogram, median and DNA-content distribution. Qualify any secondary cell-state
stratification in the actual lines, specify it before confirmation and report the number and
fraction of events included and excluded. A shift in DNA content flags a potential cell-state
confound; an unchanged distribution does **not** exclude other confounding or establish functional
rescue. The [functional plan](functional-rescue-plan.md) governs candidate advancement.
**[OUR INFERENCE; PROPOSED ANALYSIS]**

### 5.13b Qualify distribution, staining and precision assumptions

**(a) Prespecify a distribution-shift flag.** Report the fraction of events in each qualified
DNA-content compartment. The proposed rule is to flag a shift greater than **3 SD of the vehicle
(DMSO) control wells on the same plate** (§5.5b, arm 7). Qualify the compartment definitions and
their variability in the pilot before confirmation. This is an analysis choice, not a validated
disease or safety threshold. If compartments cannot be assigned reliably, report the unresolved
distribution rather than force cells into normal diploid categories.

**(b) Qualify the DNA readout under both fixation/permeabilisation conditions.** Acquire DNA
histograms in both §5.2 conditions and assess resolution in each chosen line. Do not assume that
a methanol-compatible fluorophore alone establishes a reliable DNA-content assay. Select and
document a condition that supports the intended analysis before confirmation.

**(c) Inspect the BubR1 distribution before choosing its summary and precision model.** A median
and the CV across per-well medians can be calculated for a multimodal population, but a median
alone may conceal changing subgroup proportions or responses. Multiple modes can also reflect
staining, doublets or cell-state differences; they do not by themselves establish distinct disease
subpopulations. Report histogram shape, investigate the cause and qualify the analysis for the
observed distribution. Do not discard a mode to obtain a desired patient value or CV.

The **CV ≤6.7%** value remains the conditional engineering target for the hypothetical contrast
in §3. Its suitability and the event-sampling approximation in §5.4 require qualification in the
actual assay. No historical patient-abundance band or universal aneuploid fraction supplies that
qualification. A flow cytometrist should review the population definitions, staining and analysis
before confirmation. **[OUR INFERENCE; PROPOSED ANALYSIS throughout §5.13b]**

## 5.8 🔴 PROVENANCE OF EVERY DETAIL — and the honest answer is that not all of it is primary

Asked directly whether every detail here comes from a validated primary source: **no.** This table
says which is which, because a protocol that hides the difference is worse than one that admits it.

**[A] PRIMARY — verified against a paper, vendor datasheet or registry**

| detail | source |
|---|---|
| historical fibroblast immunoblot examples: 22 / 25 / 29% of HeLa, after SV40/phTERT transformation; not an expected LCL or N1002K range | **PMID 16411201**, Figure 3A and cell-culture Methods |
| Z′ formula · ≥0.4 · SW ≥2 · CV ≤20% | **NIH/NCATS Assay Guidance Manual** |
| BD 612502: clone 9, IgG2a, aa 276–388, KO-validated, applications | vendor |
| A300-386A: **WB + IP only**, epitope aa 350–400 | vendor |
| A300-386A = **NCBI Gene 701 (*BUB1B*)**, RRID AB_386097 · A300-373A = *BUB1*, RRID AB_2065943 | Antibody Registry + NCBI |
| fix/perm 4% formaldehyde + 1% Triton, 20 min RT | published, used for BUBR1 staining |
| MG132 **10 µM** | literature held here |
| `dsiBUBR1` sequence and its reported **20–50 nM** working range | **Gama Braga 2020**, *Cell Rep* 33:108397, PMID 33207204, Key Resources Table / Cell culture; earlier Foley attribution unresolved after reading its main text and publisher supplement — see §5.6 |
| GM21284 / GM21657 / GM22004, type, genotype, price | NIGMS repository |
| Jackson **715-545-150** | published Key Resources Table |
| TruStain FcX **422302**, RRID AB_2818986, FACS + ICS | vendor |
| **MOPC-173 → BioLegend 400287** · **BD Fc Block 564220/564219** + its 10-min protocol | vendor |
| **HeLa = CCL-2 = CVCL_0030** · **U2OS = HTB-96 = CVCL_0042** | Cellosaurus |
| **MIFlowCyt** reporting standard | **PMID 18752282**, ISAC |
| **L34976** Near-IR, 633/775, fixable, pre-fixation use | vendor |
| **GM21284 culture: RPMI-1640 + 2 mM L-gln, 15% FBS not heat-inactivated, 37 °C/5% CO₂, split 1:4** | **Coriell/NIGMS catalogue record** |
| separation relative to negative-population spread as a titration principle | **PMID 15536642** (Maecker 2004), p.173; our median/MAD estimator, scale and negative-control choice are specified as adaptations in §5.1 |
| **350 × g, 5 min**; fix 20 min RT **in the dark**; **primary 20 min RT in the dark**; **"predetermined optimum concentration"**, i.e. titration is the vendor's own requirement | vendor intracellular-staining protocol (protocols.io, DOI-versioned) |
| **≥25,000 events/well** | **DERIVED** — `SE(median) ≈ 1.2533·σ/√n` against the 6.7% budget |
| **90% methanol, minimum 10 min on ice**; **methanol damages PE and APC** | vendor alcohol-permeabilisation protocols |
| **715-545-150 = Alexa 488 donkey anti-mouse IgG (H+L) *min X***, flow-validated | Jackson ImmunoResearch |
| **DsiRNA reported at 20–50 nM**; **a positive transfection control in every experiment** | **Gama Braga 2020 Methods** for the reported range; manufacturer guidance for the transfection control. The added 5 nM arm is our design choice, not a published working dose. |
| EBV transformation **increases** FcR per cell | literature |

**[B] DERIVED — computed by us from sourced inputs, reproducible**

| detail | how |
|---|---|
| **CV ≤ 6.7%**, conditional engineering target | AGM Z′ formula with the hypothetical 25%-to-50% contrast and equal-CV assumption in §3; not a measured Matsuura or N1002K baseline |
| **n = 12** | χ² bound on the sample variance — `pipeline/pilot_n.py` |
| the approximately 1.8× ratio of CV allowances in §3 | same derivation for the two hypothetical contrasts |

**[C] 🔴 CONVENTION OR OUR CHOICE — NOT from a primary source for this assay**

5 × 10⁵ cells per well · 50 µL staining volumes · 30 min RT secondary · secondary at 1:500 · the
1:50–1:800 titration range · the added **5 nM dsiRNA arm** and **timepoints** 48/72 h (20–50 nM is the reported range — §5.6) · MG132 duration (already flagged) ·
≥2 passages after thaw · the **median/MAD stain-index implementation and matched negative-control choice in §5.1**.

🔻 **A FIFTH pass corrected the knockdown arm, and a SIXTH pass corrected the FIFTH.** The fifth
replaced "10–20 nM" with the manufacturer's generic **0.1 / 1 / 10 nM**. The sixth (2026-08-30)
found that this preferred vendor boilerplate over the **verified published protocol for this exact duplex**:
Gama Braga 2020 runs `dsiBUBR1` at **20–50 nM**, so the "corrected" floor was 200–500× below a
working dose. **★ Now 5 / 20 / 50 nM.** The fifth pass's other finding stands: a **positive
transfection control was missing**, without which a failed criterion 2 is uninterpretable.
**A fix is a new claim and earns the same scrutiny as what it fixed.**

🔻 **A FOURTH pass moved two more out, and both carried a constraint I did not have:** the methanol
conditions (**90%, minimum 10 min on ice — and PE/APC are damaged by methanol**, which is a trap for
anyone substituting a secondary), and the secondary's identity (**715-545-150 is the *min X*
product, and *min X* is mandatory on immunoglobulin-producing B cells, not merely preferable**).

⚠️ **On volumes specifically: the vendor protocol is written for 12 × 75 mm TUBES (0.5 mL fixation,
2 mL washes). This protocol is 96-well V-bottom.** **Times, speeds and "in the dark" transfer
directly; VOLUMES DO NOT** and are scaled here by format. That distinction is stated rather than
letting a tube protocol's numbers be silently reused at plate scale.

🔻 **A THIRD sourcing pass moved three more out of this class — two of them corrections:**
**primary incubation 1 h → 20 min RT in the dark** (vendor); **titration is the vendor's OWN
requirement** ("predetermined optimum concentration"), not an addition here; and **events/well
≥10,000 → ≥20,000, now DERIVED** from the CV budget rather than chosen.

🔻 **Four items left this class after the second pass and are now [A]:** the culture
conditions (**Coriell's own record — and it corrected an invented density window**), the stain-index
metric (**PMID 15536642**), the centrifugation speed (**350 × g, not the 300 × g asserted here
first**), and fixation in the dark. **Asserting that class [C] was unsourceable was itself wrong;
it was under-searched.**

**✅ Every catalogue number in this document has now been verified against its vendor or a public
registry.** The three that were previously flagged are closed: **MOPC-173 → BioLegend 400287**
(purified mouse IgG2a κ); **BD 564220 / 564219 → Human BD Fc Block**, whose own guidance confirms
the 10-minute pre-stain incubation this protocol specifies; and **ATCC CCL-2 → HeLa (CVCL_0030)**,
**HTB-96 → U2OS (CVCL_0042)** via Cellosaurus.

⚠️ **Two residual cautions, which are not the same as being unverified.** BioLegend lists more than
one *purified* MOPC-173 format (standard and Go-ChIP-Grade), so the **format** — not the clone —
should be confirmed at ordering. And for an isotype control the **clone and isotype are the
specification**; the vendor is interchangeable. Every other catalogue number in this document has been checked against its vendor or a
registry today.

> ### What class [C] means in practice
> These are **standard, defensible laboratory conventions** — a flow cytometrist would recognise all
> of them — but **they are not evidence, and none is optimised for this assay.** They are starting
> points the pilot exists to refine. **Class [C] is roughly half the bench detail in this document.**
>
> **The one thing that must not happen is class [C] being read as class [A].** That is what the
> earlier `[NOT FOUND]` error in the family document did, in the other direction, and it is why this
> table exists.

## 5.9 🔴 PLATE LAYOUT — the omission that most directly attacked this protocol's own criterion

Everything here is built on achieving **CV ≤ 6.7%**, and the protocol had **no plate layout at
all.** Plate-position artefacts are among the largest and best-documented sources of well-to-well
variance in plate-based assays, and they are systematic rather than random — so they do not average
out and they inflate exactly the quantity being measured.

**Rules:**
1. **Do not use the outer wells for samples.** Fill row A/H and column 1/12 with buffer. Evaporation
   and thermal gradients are worst at the edge.
2. 🔴 **Interleave the arms; never block them.** If patient wells occupy columns 2–7 and control
   wells 8–11, **any plate gradient becomes indistinguishable from the biological difference the
   assay exists to measure.** Assign the six arms across the plate in a randomised or systematically
   interleaved pattern, and **use a recorded balanced randomisation across plates and days.**
3. **Record the well position with every measurement.** If the median MFI correlates with row or
   column, the CV is reporting plate geometry, not assay precision — **and that must be checked
   before the CV is believed**, not after.

**Without this, a plate gradient can manufacture a patient–control difference or distort the precision estimate.**

## 5.10 Analysis plan, fixed in advance

- **Qualify gates in representative pilot samples from each chosen line, then freeze the rules
  before confirmation.** Apply the same rules to every well; any justified model-specific
  boundaries must be prespecified. Report included/excluded events and verify that a control-only
  boundary does not silently remove a patient-cell population. Do not retune gates to obtain a
  preferred abundance result (§5.13a).
- **Gating is performed blind to arm assignment** — the well map is unblinded only after the median
  MFIs are exported. Cheap, and it removes the largest source of unconscious bias in flow analysis.
- **No well is excluded** except for a pre-declared technical reason (fewer than **20,000** live singlet 🔻 *raised from 10,000 on 2026-08-31 with §5.4 — the floor had been left at a value §5.4 retracted, so a well at 12,000 events was below spec and yet required to be kept*
  events; visible clog). **Outlier removal on the basis of the value itself is not permitted** — it
  would directly manufacture the CV this protocol is testing.
- Analysis software and version recorded; `.fcs` files retained.

## 5.11 Prospective MIFlowCyt reporting plan

Flow cytometry has a published minimum-reporting standard — **MIFlowCyt** (Lee *et al.*,
*Cytometry A* 2008, **PMID 18752282**), an **ISAC minimum-information standard**. This prospective
protocol addresses its four domains; it does not yet supply a completed experimental record:

| MIFlowCyt domain | here |
|---|---|
| experiment overview, purpose, keywords | §1–§3 |
| **specimens and reagents** | §4 (catalogue numbers, RRIDs), §5.0 |
| **instrument configuration** | 🟡 **PARTIAL** — lasers implied by the dye choices; **voltages, filter sets and cytometer model must be recorded at run time and cannot be pre-specified here** |
| **data processing** — gates, transformations, software | §5.4, §5.10 |

At execution, complete the run-specific specimen/reagent record, instrument configuration and
settings, controls and compensation, transformations, gate hierarchy with denominators, analysis
versions and appropriate raw-FCS access information. A uniquely specified stock instrument model
can identify fixed components; modifications and unresolved settings require explicit description.
The standard supports interpretable reporting, not certification of assay specificity, precision
or clinical validity. No blanket journal-policy requirement is asserted here.

## 5.12 Adversarial review of THIS pilot

The screen protocol carries one; this document did not, which was an inconsistency rather than a
judgement. Three attacks:

**P1 — "You are measuring total BubR1, but the patient's defect may be functional."** Does not land
*for the pilot*, which is an assay-qualification experiment and makes no biological claim. **It lands
hard on the screen**, and is already recorded there as attack A1.

**P2 — a historical protein-abundance range cannot validate a different cell line.** This criticism stands. The Matsuura series is informative context, but does not establish the expected signal in GM21284 or an N1002K system. Even a value inside the published range is insufficient evidence of specificity. Validate the assay independently, then report the observed biology. PMID 16411201. **[OUR INFERENCE]**

**P3 — a knockdown result in HeLa/U2OS does not establish LCL-flow specificity.** This criticism
stands. The adherent arm is a proposed development step, not permission to transfer validation
between cell models and preparations. Before the LCL assay qualifies for screening, demonstrate
depletion in the chosen LCL preparation using a qualified delivery method, confirm protein loss
orthogonally and assess the flow response. Delivery failure leaves the test indeterminate (§5.6).

## 6. Proposed assay-qualification criteria

These are design targets for laboratory review, not a completed preregistration. The observed patient abundance is a result, never a pass/fail target. The [functional plan](functional-rescue-plan.md) requires additional cellular validation before a drug claim.

| # | criterion | why |
|---|---|---|
| **1** | **Specific signal**: arm 3 ≫ arms 1 and 2 | otherwise it is background |
| **2** | **Specificity by confirmed depletion in the chosen LCL preparation**: proposed flow-signal reduction **≥ 50%**, with orthogonal protein confirmation and passing delivery controls | an adherent-line result alone does not qualify LCL flow; failed depletion makes the specificity test indeterminate |
| **3** | **Linearity and orthogonal agreement** in the chosen cells, with tolerance fixed from pilot precision before confirmation | validates measurement without forcing a patient value into a historical range |
| **4** | **Precision**: proposed **CV ≤ 6.7%** across replicate wells, with the summary and model qualified in the actual assay | conditional on §3's hypothetical contrast and equal-CV assumption; patient/control separation alone is insufficient |
| **5** | **Reproducibility across ≥ 2 antibody lots** and 2 independent days | a screen runs for months |

## 7. Decision, written before the result

- **All five met in the intended LCL assay**, with population/analysis assumptions qualified → proceed to Z′ validation for the proposed abundance screen. This does not qualify N1002K function or a therapeutic effect.
- **1–3 met, 4 failed** *(specific but imprecise)* → the assay has not met the precision target
  for the chosen hypothetical 2-fold contrast under §3's assumptions. **Optimise and requalify
  before proceeding.** A failed design target does not establish the size of a biological response.
- **2 indeterminate** *(delivery/depletion controls fail)* → qualify those controls and repeat;
  do not infer antibody failure from ineffective depletion.
- **2 failed despite confirmed depletion** → **stop.** Resolve the mismatch between protein loss
  and flow signal, including assay linearity and background. Qualify an alternative antibody or
  readout before proceeding; do not declare the assay specific from the adherent arm alone.
- **3 failed** → measurement is indeterminate. Resolve dilution/linearity or orthogonal disagreement before screening. A patient value outside the published examples is not itself a failure. Do not infer a carrier state from an abundance band. **[OUR INFERENCE]**
- **5 failed** *(not reproducible)* → **decompose it before deciding, because the two halves have
  different fixes.**
  - **Fails across ANTIBODY LOTS, holds across days** → a reagent problem, not an assay problem.
    **Qualify each lot against the same control LCL before use** and record the lot in every result;
    this is ordinary practice for a polyclonal-sensitive readout and does not invalidate the assay.
  - **Fails across DAYS, holds across lots** → a run-to-run problem: instrument setup, compensation,
    or culture state. **Add a bead-based daily standardisation and fix passage number after thaw
    (§5.10 already requires ≥2 passages), then re-run.**
  - **Fails both** → **stop and go to the fallback.** A readout that is neither lot-stable nor
    day-stable cannot support a 1,520-compound screen where plates are acquired over days.
- **Distribution or analysis assumptions unresolved** (§5.13b(c)) → report the data and investigate
  the cause before interpreting criterion 4. A multimodal histogram does not make a per-well
  median or its CV undefined, but it can make that summary inadequate. Qualify any subgroup
  analysis without removing a population merely to meet an abundance or precision target.
- **Fallback** → an **endogenously tagged fluorescent BubR1 reporter line**: no antibody, cleaner
  quantitation, but genome editing in a patient-derived line and a substantially larger project.
  **Named here so that failure has a route rather than becoming a stall.**

## 8. Cost and duration

| | |
|---|---|
| cell lines (3) | **~$790–1,350** |
| antibodies, isotype, secondary, 2 lots | **$600–1,200** |
| MG132, dsiRNA, transfection reagent, plasticware | **$400–800** |
| flow time | **[NOT ESTIMATED — facility rate]** |
| **elapsed** | **[ESTIMATE] 3–6 weeks**, dominated by cell-line delivery and LCL expansion |

**[OUR ESTIMATE. Cell-line prices `[VERIFIED]` from the repository; antibody and reagent figures are
current market ranges to be re-quoted. Labour and instrument time are not invented.]**

## 9. What this pilot cannot tell you

- Nothing about whether any drug raises BubR1. **It is an assay-qualification experiment.**
- Nothing about **N1002K** — `GM21284` is `753X`/`R814H`. See the accompanying reagent specification.
- Whether the assay holds at 384-well density: **that is the Z′ validation step, which comes after
  this and is a separate gate.**
