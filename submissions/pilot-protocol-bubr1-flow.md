# Pilot: can BubR1 abundance be measured by intracellular flow cytometry?

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
   flow protocol on the exact reference cell line our calibration anchor uses — HeLa** — including
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

## 2. ★ The calibration anchor — a published expected value

The screen protocol had **no published expected value for its primary readout**, which was its main
weakness against the companion stability protocol. **This pilot has one.**

> **Matsuura *et al.* 2006 (PMID 16411201) measured BubR1 in three MVA patients at
> 22%, 25% and 29%** of the reference level.

> ✅ **AN AUDIT CANDIDATE CHECKED HERE AND REFUTED, 2026-08-31 — recorded so the correction is not
> made later by someone who reads only the paper's title.** A coverage sweep flagged *"they are not
> MVA patients"*, on the ground that PMID 16411201 is titled *"**Monoallelic** BUB1B mutations …
> in seven families with **premature chromatid separation (PCS) syndrome**"*. **The paper's own
> first sentence settles it the other way:** *"Cancer-prone syndrome of premature chromatid
> separation (PCS syndrome) with mosaic variegated aneuploidy (MVA) is a rare autosomal recessive
> disorder …"*, and it calls MVA syndrome *"probably identical to the PCS syndrome"*. **They are
> MVA patients**, and the anchor stands.
>
> ⚠️ **What IS a real difference, and it is not the one the sweep found.** Matsuura's patients 1, 2
> and 5 carry **one truncating allele plus the low-expression `6G3` haplotype** — a second allele
> *"without detectable mutation"*. **This child carries two identified variants**, a nonsense and a
> missense. The genetic architectures differ even though the consequence — a large reduction in
> BubR1 with no wild-type pool — is the same shape. **The anchor is an expected range from an
> analogous architecture, not a matched genotype**, which is the third limit stated below.
> [`papers-local/matsuura2006_ajmg_monoallelic_bub1b.txt`, re-read 2026-08-31; title confirmed by
> `esummary` for PMID 16411201.]

**A working assay must reproduce roughly that.** If patient cells read at 80% of control, the assay
is not measuring BubR1 specifically. If they read at 3%, something else is wrong. **The pilot has a
number to hit, not merely a signal to observe.**

⚠️ **Three honest limits on the anchor, and the third was rewritten on 2026-08-30 because it was
wrong in both halves.** Matsuura's figures are **% of HeLa**; **those patients are not this
repository's donor**; and **the 22 / 25 / 29% trio was measured on hTERT-immortalised *fibroblast*
lines from patients 1, 2 and 5 — not on lymphoblastoid cells.** Proliferation rate, and therefore
cell-cycle distribution, differs between fibroblasts and LCLs, and §5.13 shows that distribution is
coupled to BubR1 abundance. **Treat 22–29% as an expected range and direction, not a target to be
matched to the digit** — which is why criterion 3 is written as a broad 20–35% band.

> 🔴 **WHAT THE PREVIOUS WORDING GOT WRONG, and it was flagged "— checked directly —".** It read:
> *"the patient material was lymphocytes and fibroblasts, **not** EBV-transformed lymphoblastoid
> lines."* **Both halves are false, and the paper we hold says so on the same page.** The trio is
> fibroblast-only (*"fibroblast cell lines from patients 1, 2, and 5 … BubR1 bands of normal size
> but reduced intensities (22%, 25%, and 29% of HeLa cells)"*), and **Matsuura DOES report
> EBV-transformed lymphoblastoid lines, at length** — family 2 at mother **71%**, father **57%**,
> **patient 2 at 22%**; family 6 with carriers at **38%** and **31%** against normal individuals at
> **112%** and **158%**. **An asserted verification is the most dangerous kind of unverified
> claim**: "checked directly" told every later reader not to check.
>
> 🔑 **AND IT IS GOOD NEWS FOR THIS PROTOCOL.** The lymphoblastoid data are the closest published
> match to what this pilot actually measures — **patient 2's LCL reads 22%**, inside the 20–35%
> band criterion 3 already specifies, and the normal range of **112–158%** is what a proper
> unrelated control should look like. The anchor is *stronger* than the previous caveat allowed.
> [OUR MEASUREMENT — `papers-local/matsuura2006_ajmg_monoallelic_bub1b.txt` re-read 2026-08-30;
> control `grep -ci bubr1` → 44.]

## 3. 🔴 The precision the assay must reach — derived, not asserted

This is the calculation the screen protocol could not do, and it produces a trap worth naming.

The screen must detect a **2-fold rise from the patient baseline**: **25% → 50%** of control. Using
the Assay Guidance Manual's own Z′ definition, with CV equal in both populations:

```
Z' = 1 - 3·CV·(hi + lo) / (hi - lo)
```

| what is being resolved | Z′ target | **maximum assay CV** |
|---|---|---|
| patient vs control — **25% vs 100%** *(the easy comparison)* | ≥ 0.4 | **≤ 12.0%** |
| **a 2-fold hit — 25% vs 50%** *(what the screen needs)* | ≥ 0.4 | **≤ 6.7%** |
| the same, comfortably | ≥ 0.5 | ≤ 5.6% |
| the same, bare 3σ separation | 0.0 | ≤ 11.1% |

> ### 🔴 The trap: the easy comparison is ~3× more forgiving than the one that matters.
> A pilot that shows "we can clearly separate patient from control cells" would look like a
> success, be declared one, **and the screen would then fail** — because separating 25% from 100%
> needs CV ≤ 12% while separating 25% from 50% needs **CV ≤ 6.7%.**
> **Therefore the pilot's acceptance criterion is CV ≤ 6.7%, not "clear separation".**

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
> | **GM21657** | *"MOSAIC VARIEGATED ANEUPLOIDY SYNDROME 2; MVA2 · CENTROSOMAL PROTEIN, 57-KD; CEP57"*, father of GM21654/GM21655 | **A different gene.** He is in the *CEP57* family this protocol already lists one row below as its *specificity* control |
> | **GM22004** | *"MOSAIC VARIEGATED ANEUPLOIDY SYNDROME 1; MVA1"*, *"father of an affected child (GM22006)"* | MVA is **autosomal recessive**, so he is an **obligate heterozygous carrier** at the *BUB1B* locus |
> | **GM21284** | *"parental cell lines not in the repository"* | **Neither line is a parent of the patient line.** No parent of GM21284 exists at Coriell |
>
> **Why this mattered more than a wrong catalogue number.** These two lines were the **100%
> denominator** for acceptance criterion 3 (*patient ≈ 20–35% of control*) and the cells §5.1
> titrates the antibody on. Using a carrier as "normal" compresses the very ratio the assay
> exists to measure — and the protocol's **own anchor paper says so**: Matsuura 2006 reports
> lymphoblastoid BubR1 at **63–158% in normal individuals** against **21–57%** in truncating-
> mutation carriers and **31–71%** in 6G3-haplotype carriers. A carrier denominator would have
> made a real reduction look smaller than it is, in the conservative direction — which is worse,
> not better, because it costs sensitivity silently.
>
> **The replacement, and why it is defensible.** The reference must be **unrelated to any MVA
> family**, apparently healthy, and an LCL so that cell type matches. **GM12878** is a
> CEPH/HapMap pedigree-1463 B-lymphocyte line, the most deeply characterised LCL in existence
> (1000 Genomes / ENCODE tier 1). *Full disclosure from its Coriell record: it carries* `CYP2C19*2`,
> *a pharmacogenetic splice variant with no relationship to BubR1 abundance.* **Use at least two
> unrelated controls**, because criterion 3 is a ratio and a single denominator has no spread.
> The *CEP57* lines **GM21654 · GM21655 remain the specificity control** — a different MVA gene is
> exactly what that arm needs — and **GM21657 and GM22004 may still be run as carrier comparators,
> labelled as carriers**, which is informative. They are simply not "normal".

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
**Choose the dilution maximising the *stain index*** — the published metric for exactly this
purpose (**Maecker *et al.*, *Cytometry A* 2004, PMID 15536642**), which weights the separation
between populations by **the spread of the negative**, and therefore penalises a bright reagent
sitting on a broad background:

```
stain index = (median_stained − median_isotype) / (2 × robust SD_isotype)
```

**Not the dilution giving the brightest signal** — the brightest is usually not the most separated,
and picking on raw brightness is the standard way to enter a screen with a poor window.

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

1. **FSC-A vs SSC-A** → the intact lymphoblast population, excluding debris at low FSC.
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

> **Collect ≥ 20,000 live singlet events per well**, and **set the final count from the spread
> actually observed during titration.** 🔻 An earlier version said "≥10,000" — adequate only if the
> stain is tight, and **insufficient at a broad 80% spread**, where counting error alone would eat
> 15% of the CV budget. Keep voltages, gates and compensation **identical
across all wells, plates and days**; changing them between conditions invalidates every CV computed.

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

**Six arms, n = 12 each = 72 wells = one 96-well plate per condition-set**, which is also why
§5.2's two fix/perm conditions fit on two plates run side by side.

### 5.5b The arms

| # | arm | condition |
|---|---|---|
| 1 | patient + **isotype** control | mouse IgG2a at the same µg/mL as the titrated primary |
| 2 | patient + **secondary only** | no primary |
| 3 | **patient + anti-BUBR1** | baseline |
| 4 | **control LCL + anti-BUBR1** | the anchor comparison |
| 5 | **+ BUBR1 knockdown** | specificity — see §5.6 |
| 6 | **patient + MG132** | **10 µM**, with a **2 / 4 / 6 h** time course |

**MG132 at 10 µM is well supported** across the literature held here. ⚠️ **The duration needed for
BubR1 accumulation is NOT** — the published uses are 15 min to 1 h for mitotic arrest, a different
purpose. **Hence the time course rather than a single invented number.**

### 5.6 ⚠️ The knockdown control has a practical problem, and it changes where it is run

`dsiBUBR1 5'-GUCUCACAGAUUGCUGCCUCAGAGC-3'` (**Gama Braga 2020**, PMID 33207204; see §5.6) is the right reagent, **but LCLs are
EBV-transformed B cells and are notoriously refractory to lipid transfection.** Assuming a
lipofection will work here is the kind of assumption that costs a month.

> **Therefore: run the knockdown specificity arm in an easily transfected adherent line
> (HeLa or U2OS), not in the LCLs.** Specificity is a property of the *antibody*, not of the cell
> line, so it transfers. **The anchor comparison (§ arms 3–4) stays in the LCL pair, where the
> published 22–29% expectation applies.**
> If a knockdown in LCLs is wanted regardless, it requires **nucleofection**, not lipofection, and
> the efficiency must be measured rather than assumed.

**Knockdown conditions for the adherent arm:** **HeLa (ATCC CCL-2, CVCL_0030)** or **U2OS
(ATCC HTB-96, CVCL_0042)**, reverse-transfected with a standard lipid reagent (e.g. Lipofectamine
RNAiMAX).

🔻🔻 **CONCENTRATION CORRECTED TWICE — read this, because the first correction made it worse.**
An early version specified "10–20 nM". A correction on 2026-08-30 replaced that with a
**0.1 / 1 / 10 nM** dose–response, reasoning from the *manufacturer's* generic DsiRNA guidance
(27mer Dicer-substrate, more potent than a 21mer, often effective at ≤1 nM). **That reasoning was
sound and the answer was wrong**, because generic vendor guidance was preferred over the only
published use of *this exact duplex*.

**Gama Braga et al. 2020 (*Cell Rep* 33:108397, PMID 33207204) — the paper that published this
sequence — states in its Methods, verbatim: `dsiBUBR1 (20-50 nM)`.** The same paragraph runs
`dsiCENP-E` at 50 nM and `dsiBUB1` at 20 nM. **That laboratory does not run DsiRNAs at 1 nM.**
The 0.1 nM floor was **200–500× below** the published working concentration and even the 10 nM
ceiling was 2–5× below it — a titration that could have returned no knockdown and been read as
antibody failure.

**★ USE: a dose–response of `5 / 20 / 50 nM`**, which brackets the published 20–50 nM rather than
sitting under it. Report the knockdown at each dose. If ≥70% knockdown is reached at 5 nM, use the
lowest effective dose for the specificity arm — the manufacturer's off-target argument below is
still correct, it just cannot justify a range that has never been shown to work.

> 🔴 **CITATION NOTE, and it does not resolve cleanly.** This protocol previously attributed the
> duplex to **Foley 2011**. **Gama Braga's own Key Resources Table credits it the same way** —
> `dsiBUBR1 … (Foley et al., 2011)` — so the attribution was inherited from a peer-reviewed
> source, not invented here. **But we hold Foley et al. 2011 (*Nat Cell Biol* 13:1265,
> PMID 21874008) in full text, and the duplex sequence does not appear in it**
> (`grep -c GUCUCACAGAUUGCU foley2011.txt` → 0; that paper's siRNAs target the B56 subunits, and
> "BubR1" appears 6 times in the whole text). We cannot exclude a supplementary file we do not
> hold, so we do not assert that Gama Braga is wrong. **What we assert is what we verified:
> Gama Braga 2020 publishes the sequence and the working concentration, so Gama Braga is the
> citation a reader needs — and the concentration is the reason it matters.**
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

**CV = SD / mean of the per-well MEDIAN fluorescence intensities**, across the **n ≥ 6 replicate
wells of one arm on one plate** — *not* the CV of events within a well, which is a different and
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
- **Use DNA content as a REPORTED COVARIATE, not as a filter** — see the correction below, which
  matters specifically because of this disease.
- **Report the cycle distribution alongside every measurement**, and treat any compound that shifts
  it as confounded until shown otherwise.

### 🔴 5.13a A CORRECTION TO THE FIX ABOVE — and it is specific to MVA

The obvious implementation is to **gate on G1 and report BubR1 within it.** **In this disease that
is wrong**, and the reason is the disease's own definition:

> **MVA is diagnosed by aneuploidy in — verbatim — *"usually >25%"* of cells.**
> **More than a quarter of the patient population has abnormal DNA content by definition.**

Three consequences:
1. **A G1 gate drawn on normal diploid cells does not map onto the patient line.** Aneuploid cells
   with gains or losses sit off the 2N peak, so the gate silently excludes them.
2. 🔴 **Worse, the exclusion is not random — it selects AGAINST the cells carrying the phenotype.**
   Gating "normal G1 DNA content" in an MVA line preferentially retains its most euploid
   subpopulation. **If BubR1 level and mis-segregation are related at all — which is the entire
   thesis — then those are exactly the cells with the most BubR1, and the gate biases the measured
   value upward.**
3. **It breaks the patient-vs-control comparison**, since a near-diploid control and a >25%-aneuploid
   patient line are not comparable populations inside "the same" gate.

> ### Resolution: measure DNA content, report it, and do not filter on it.
> The confound being addressed is *"the compound redistributed the cell cycle"*, and that is visible
> in the **BubR1-versus-DNA-content relationship** without excluding any cell. **Report the median
> BubR1 of the whole live-singlet population AND the cycle distribution, and flag any well whose
> distribution has moved.** A hit that raises BubR1 *and* shifts the cycle is confounded; a hit that
> raises BubR1 with the distribution unchanged is not.
> **This keeps the aneuploid cells in the analysis, where they belong — they are the disease.**

### 🔻 5.13b THREE GAPS IN §5.13a ITSELF, found by auditing the fix as a new claim

**Written one pass after §5.13a, because a fix is a claim and gets the same scrutiny as what it
fixed.**

**(a) "Flag any well whose distribution has moved" had NO THRESHOLD.** Having criticised an
asserted hit criterion, the fix introduced a rule with no criterion at all — which is worse, because
it is unfalsifiable. **Definition now required: report the percentage of events in each cycle
compartment, and flag a well when any compartment shifts by more than 3 SD of the DMSO-control wells
on the same plate.** Same logic as the hit criterion; the plate's own controls set the scale.

**(b) 🔴 The DNA dye's compatibility with METHANOL was never checked** — and Condition B is a
methanol arm. Methanol permeabilisation changes DNA-dye access and histogram resolution, and this
protocol asks for a DNA dye and a methanol condition **without ever asking whether they work
together.** **Add to the §5.2 comparison: acquire the DNA histogram in both fix/perm conditions and
confirm resolvable G1/G2 peaks before either is chosen.** If the methanol arm cannot give a clean
DNA histogram, that is a reason to prefer Condition A — a criterion this protocol did not have.

**(c) 🔴 The whole statistical framework assumes a UNIMODAL population, and this disease may not
provide one.** §3's CV ≤ 6.7% derivation and every use of "median MFI" assume a single well-behaved
distribution. **But the patient line is >25% aneuploid, and whether BubR1 is distributed unimodally
across euploid and aneuploid subpopulations is unknown** — and it is not a safe assumption, since
the thesis itself proposes that BubR1 level and mis-segregation are linked.
> **Therefore: unimodality is now a PRECONDITION, checked before the CV criterion is applied.**
> **Report the BubR1 histogram shape for every arm.** If the patient distribution is bimodal, **a
> median is the wrong statistic and the CV criterion does not hold** — the analysis must move to
> reporting the subpopulations, and the hit definition changes with it.
> ⚠️ **A bimodal patient distribution would not be a nuisance. It would be a finding** — it would
> say the patient's cells are not uniformly BubR1-low, which no published measurement of these
> lines addresses.

**[OUR INFERENCE throughout §5.13b. (c) rests on the published >25% aneuploidy figure; the
statistical consequence is our reasoning.]**

⚠️ **Acceptance criteria are therefore unchanged in both value and population:** the 20–35% anchor
and CV ≤ 6.7% apply to the whole live-singlet gate, as originally written. **[OUR INFERENCE from a
sourced fact — the >25% aneuploidy figure is published; that it makes cycle-gating inappropriate
here is our reasoning.]**

**[OUR INFERENCE from sourced facts — that BubR1 is an APC/C-Cdh1 substrate degraded after mitotic
exit is published; that this makes cell-cycle gating necessary for an abundance screen is our
reasoning, and it is the kind of reasoning that should be checked by a flow cytometrist.]**

## 5.8 🔴 PROVENANCE OF EVERY DETAIL — and the honest answer is that not all of it is primary

Asked directly whether every detail here comes from a validated primary source: **no.** This table
says which is which, because a protocol that hides the difference is worse than one that admits it.

**[A] PRIMARY — verified against a paper, vendor datasheet or registry**

| detail | source |
|---|---|
| patient BubR1 at 22 / 25 / 29% | **PMID 16411201** |
| Z′ formula · ≥0.4 · SW ≥2 · CV ≤20% | **NIH/NCATS Assay Guidance Manual** |
| BD 612502: clone 9, IgG2a, aa 276–388, KO-validated, applications | vendor |
| A300-386A: **WB + IP only**, epitope aa 350–400 | vendor |
| A300-386A = **NCBI Gene 701 (*BUB1B*)**, RRID AB_386097 · A300-373A = *BUB1*, RRID AB_2065943 | Antibody Registry + NCBI |
| fix/perm 4% formaldehyde + 1% Triton, 20 min RT | published, used for BUBR1 staining |
| MG132 **10 µM** | literature held here |
| `dsiBUBR1` sequence and its **20–50 nM** working concentration | **Gama Braga 2020**, *Cell Rep* 33:108397, PMID 33207204 (its own resource table credits Foley 2011; we could not find the duplex there — see §5.6) |
| GM21284 / GM21657 / GM22004, type, genotype, price | NIGMS repository |
| Jackson **715-545-150** | published Key Resources Table |
| TruStain FcX **422302**, RRID AB_2818986, FACS + ICS | vendor |
| **MOPC-173 → BioLegend 400287** · **BD Fc Block 564220/564219** + its 10-min protocol | vendor |
| **HeLa = CCL-2 = CVCL_0030** · **U2OS = HTB-96 = CVCL_0042** | Cellosaurus |
| **MIFlowCyt** reporting standard | **PMID 18752282**, ISAC |
| **L34976** Near-IR, 633/775, fixable, pre-fixation use | vendor |
| **GM21284 culture: RPMI-1640 + 2 mM L-gln, 15% FBS not heat-inactivated, 37 °C/5% CO₂, split 1:4** | **Coriell/NIGMS catalogue record** |
| **stain index** as the titration metric | **PMID 15536642** (Maecker 2004) |
| **350 × g, 5 min**; fix 20 min RT **in the dark**; **primary 20 min RT in the dark**; **"predetermined optimum concentration"**, i.e. titration is the vendor's own requirement | vendor intracellular-staining protocol (protocols.io, DOI-versioned) |
| **≥20,000 events/well** | **DERIVED** — `SE(median) ≈ 1.2533·σ/√n` against the 6.7% budget |
| **90% methanol, minimum 10 min on ice**; **methanol damages PE and APC** | vendor alcohol-permeabilisation protocols |
| **715-545-150 = Alexa 488 donkey anti-mouse IgG (H+L) *min X***, flow-validated | Jackson ImmunoResearch |
| **DsiRNA at 5 / 20 / 50 nM**, bracketing the published 20–50 nM; **a positive transfection control in every experiment** | **Gama Braga 2020 Methods** for the concentration; manufacturer guidance for the off-target rationale and the transfection control |
| EBV transformation **increases** FcR per cell | literature |

**[B] DERIVED — computed by us from sourced inputs, reproducible**

| detail | how |
|---|---|
| **CV ≤ 6.7%** | AGM Z′ formula + the Matsuura baseline |
| **n = 12** | χ² bound on the sample variance — `pipeline/pilot_n.py` |
| the 3× forgiveness trap in §3 | same derivation |

**[C] 🔴 CONVENTION OR OUR CHOICE — NOT from a primary source for this assay**

**5 × 10⁵ cells per well · 50 µL staining volumes · 30 min RT secondary · secondary at 1:500 · the
1:50–1:800 titration range · the dsiRNA **timepoints** 48/72 h (the *concentration* is now sourced — §5.6) · MG132 duration (already flagged) ·
≥2 passages after thaw.**

🔻 **A FIFTH pass corrected the knockdown arm, and a SIXTH pass corrected the FIFTH.** The fifth
replaced "10–20 nM" with the manufacturer's generic **0.1 / 1 / 10 nM**. The sixth (2026-08-30)
found that this preferred vendor boilerplate over the **only published use of this exact duplex**:
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
   interleaved pattern, and **use the same map on every plate and every day.**
3. **Record the well position with every measurement.** If the median MFI correlates with row or
   column, the CV is reporting plate geometry, not assay precision — **and that must be checked
   before the CV is believed**, not after.

**Without this, a plate gradient can produce either a false pass on criterion 3 (patient ≈ 20–35%
of control, manufactured by position) or a false fail on criterion 4.**

## 5.10 Analysis plan, fixed in advance

- **Gates are set once**, on the control-LCL + full-stain sample, and **applied unchanged to every
  well.** Per-well gate adjustment is how subjective flow analysis becomes unfalsifiable.
- **Gating is performed blind to arm assignment** — the well map is unblinded only after the median
  MFIs are exported. Cheap, and it removes the largest source of unconscious bias in flow analysis.
- **No well is excluded** except for a pre-declared technical reason (fewer than 10,000 live singlet
  events; visible clog). **Outlier removal on the basis of the value itself is not permitted** — it
  would directly manufacture the CV this protocol is testing.
- Analysis software and version recorded; `.fcs` files retained.

## 5.11 MIFlowCyt conformance

Flow cytometry has a published minimum-reporting standard — **MIFlowCyt** (Lee *et al.*,
*Cytometry A* 2008, **PMID 18752282**), an ISAC standard required by *Nature* and PLOS. Its four
domains, and where this protocol addresses them:

| MIFlowCyt domain | here |
|---|---|
| experiment overview, purpose, keywords | §1–§3 |
| **specimens and reagents** | §4 (catalogue numbers, RRIDs), §5.0 |
| **instrument configuration** | 🟡 **PARTIAL** — lasers implied by the dye choices; **voltages, filter sets and cytometer model must be recorded at run time and cannot be pre-specified here** |
| **data processing** — gates, transformations, software | §5.4, §5.10 |

**⚠️ The instrument row cannot be closed by us**, because it is a property of the facility's machine.
**It is named so that it is recorded rather than forgotten**, which is the whole purpose of a
minimum-reporting standard.

## 5.12 Adversarial review of THIS pilot

The screen protocol carries one; this document did not, which was an inconsistency rather than a
judgement. Three attacks:

**P1 — "You are measuring total BubR1, but the patient's defect may be functional."** Does not land
*for the pilot*, which is an assay-qualification experiment and makes no biological claim. **It lands
hard on the screen**, and is already recorded there as attack A1.

**P2 — "The 22–29% anchor is from a different cell type and different patients, so criterion 3 is
not really a criterion."** **Partly lands.** It is why the acceptance range is written as a broad
**20–35%** rather than a point estimate, and why §2 states the limits explicitly. **If the observed
value is 40–50%, the honest response is uncertainty about the anchor, not automatic rejection of
the assay** — and that ambiguity is a real weakness with no clean resolution available to us.

**P3 — "Criterion 2 (knockdown) is run in a different cell type from criteria 3–4."** **Lands, and
it is the sharpest.** Specificity is demonstrated in HeLa/U2OS while the anchor is measured in LCLs,
so **strictly, specificity is not demonstrated in the cells the screen will actually use.** The
justification — that antibody specificity is a property of the antibody — is reasonable but is an
**assumption, not a measurement.** ⚠️ **Mitigation, now required: if the pilot passes, confirm
BubR1 depletion in LCLs by nucleofection at least once before the screen begins.** Deferred, not
dismissed.

## 6. Acceptance criteria — all four, fixed before any data exist

| # | criterion | why |
|---|---|---|
| **1** | **Specific signal**: arm 3 ≫ arms 1 and 2 | otherwise it is background |
| **2** | **Specificity by knockdown**: dsiBUBR1 reduces signal **≥ 50%** | 🔴 **the decisive one.** An antibody signal that does not fall when the target is knocked down is not measuring the target, whatever else it does |
| **3** | **Anchor**: patient ≈ **20–35%** of control | reproduces the published expectation; well outside that range means the assay is measuring something else |
| **4** | 🔴 **Precision**: **CV ≤ 6.7%** across replicate wells | §3 — and **not** merely "patient and control separate" |
| **5** | **Reproducibility across ≥ 2 antibody lots** and 2 independent days | a screen runs for months |

## 7. Decision, written before the result

- **All five met** → proceed to Z′ validation and the screen.
- **1–3 met, 4 failed** *(specific but imprecise)* → the assay measures BubR1 but cannot see a
  2-fold change. **Optimise before proceeding — do not start the screen.** This is the most likely
  partial outcome and the one most likely to be waved through.
- **2 failed** *(no knockdown response)* → **stop.** The reagent is not measuring BubR1 in this
  format. Try the other antibody once; if it also fails, go to the fallback.
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
