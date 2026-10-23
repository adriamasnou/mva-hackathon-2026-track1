# The repurposing screen, made runnable

**Turning a design sketch into something a screening facility can quote. Validation criteria are
the NIH/NCATS Assay Guidance Manual's, not ours.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## 0. What was missing, and what this closes

The screen design existed and **called itself a design sketch, not a protocol.** Its own readiness
audit listed **13 components: 4 done, 7 desk-closable, 1 blocked on a laboratory, 1 caveat** — and
the binding constraint was named honestly: **we held zero high-throughput-screening methods
papers.** This closes the seven.

**This is a proposed abundance-screen design, not an executed screen.** No reliable probability of a hit or treatment follows from the protocol. Candidate advancement is governed by the [full-length functional and exposure plan](functional-rescue-plan.md).

## 1. The question the screen asks

Does any approved drug **raise the amount of BubR1** in patient cells? An abundance-limited defect is a hypothesis to test. This screen measures amount; function, exposure, proliferation and selection must be assessed separately before advancing a candidate.

## 2. ★ The design decision everything else follows from

The published **MPM-2⁺ fraction of the 4N population after 16 h nocodazole, by flow cytometry**
is a checkpoint-arrest readout (Suijkerbuijk SJE et al., *Cancer Res* 2010; PMID 20516114, Fig 4D, upper panel).
The same paper measures chromosome segregation by live imaging (PMID 20516114, Fig 4D, middle panel).
Y155C retains kinetochore localisation and chromosome-alignment activity but fails to restore
nocodazole-induced MPM-2 positivity, illustrating separation of these functions (PMID 20516114, Fig 5A–D).

Gama Braga measures BUBR1 KARD phosphorylation and PP2A-B56 recruitment separately from
checkpoint silencing and kinetochore–microtubule attachment; the tested constructs can retain
kinetochore-localised protein yet have impaired functional readouts (PMID 33207204, Figs 3–4 and S5).

Foley shows restoration of cold-stable fibres after short Aurora B or Plk1 inhibitor treatment
in B56-depleted cells (PMID 21874008, Fig 4D–E and Fig 5A–B); that attachment result
does not itself demonstrate correct subsequent chromosome segregation.

Nocodazole arrest maintenance alone cannot establish attachment, checkpoint-silencing or
segregation rescue. These distinct experimental endpoints motivate following abundance hits
through the [full-length functional and exposure plan](functional-rescue-plan.md).
**[OUR INFERENCE — proposed confirmation design.]**

> **Primary screen: BubR1 ABUNDANCE, by intracellular antibody stain, read on a
> high-throughput flow cytometer in 384-well format.
> Hit confirmation: repeat abundance dose–response and counter-screens, followed by functional
> testing with segregation errors per completed division as the primary functional outcome.**

Measure chromosome alignment, checkpoint activation/maintenance, checkpoint silencing/exit timing,
full-length BubR1 abundance/localisation, and division and cell fates separately. Track failed,
arrested and dying cells so that restricting the primary denominator to completed divisions does
not conceal harm or selection. Phospho-KARD/B56 and cold-stable-fibre assays may help identify a
failed attachment-regulation step; they do not replace the division-level outcome. PMID 23079597;
PMID 21874008. **[PROPOSED FOLLOW-UP; governed by the full-length plan]**

Use controls qualified for each endpoint. The published forced-expression rescue of the
nocodazole checkpoint response by I909T/L1012P does not calibrate every BubR1 function, and
fragment thermal comparators do not serve as interchangeable cellular rescue controls.
PMID 20516114. **[OUR INFERENCE]**

**The screen line is a lymphoblastoid line, i.e. suspension cells.** This motivates flow for the
abundance primary; it does not establish that the proposed division-imaging and functional assays
are qualified in that line. Model and readout qualification remain laboratory work.

## 3. Cells — real catalogue numbers

| line | type | genotype | role |
|---|---|---|---|
| **GM21284** | LCL | *BUB1B* `4-bp ins 2211GTTA` / `R814H` | **the screen line** |
| **GM12878** + ≥1 further unrelated apparently-healthy LCL | LCL | CEPH/HapMap pedigree 1463; no MVA-gene family history | **normal-abundance reference** |
| GM21657 · GM22004 | LCL | 🔴 **obligate carriers, NOT normals — corrected 2026-08-30.** GM21657 is *CEP57*/MVA2 (father of GM21654·GM21655, the row below); GM22004 is *MVA1* (father of an affected child). MVA is recessive, so both are heterozygous carriers | **carrier comparators** — informative, but they cannot be the 100% denominator |
| GM21654 · GM21655 | LCL | *CEP57* patients | specificity control — a different MVA gene |

**~$262 US-academic / $448 international each, MTA required** (NIGMS Human Genetic Cell Repository).

🔴 **Limitation, stated up front: `GM21284` has no matched parent in the repository.** The
unaffected LCLs above are from *other families and a different gene*, so they are population
references, not matched controls. **[VERIFIED from the repository's own records; the trio structure
of families 2680 and 2741 does not extend to the *BUB1B* donor.]**
⚠️ And `GM21284` is **not this child's genotype** — no N1002K line is catalogued in Coriell or Addgene *(the repositories searched; ECACC unresolved)*, which is what the
accompanying reagent specification addresses.

## 4. Assay validation — to the Assay Guidance Manual, with its numbers

**[NIH/NCATS Assay Guidance Manual — these thresholds are the AGM's, quoted, not invented here.
Eli Lilly & Company and the National Center for Advancing Translational Sciences, eds.
*Assay Guidance Manual*, Bethesda (MD): NCBI Bookshelf **NBK53196**,
`https://www.ncbi.nlm.nih.gov/books/NBK53196/` — the Z′-factor, signal window and CV criteria are
in its assay-validation chapters. 🔻 *Locator added 2026-08-31: this document's subtitle stakes it
on this source and §4 reproduces five numeric thresholds from it, and until today it gave no
Bookshelf ID, no chapter and no URL — so no reader could check whether the numbers were quoted
correctly. The project's own standard requires a PMID, DOI or URL on every load-bearing claim,
and the document's headline authority was the one claim without one.*]**

```
Z' = 1 - ( 3·(SD_max + SD_min) / |AVG_max - AVG_min| )
```

| criterion | AGM requirement |
|---|---|
| **Z′-factor** | **≥ 0.4** |
| signal window | **SW ≥ 2** (alternative to Z′) |
| coefficient of variation | **CV_max and CV_mid ≤ 20%** |
| minimum-signal CV | CV_min ≤ 20%, or SD_min ≤ min(SD_mid, SD_max) |
| plate format | ≥ 96-well; 384 and 1536 templates provided |

**The Z′ controls, which the design previously lacked:**

- **Minimum signal** = patient cells + DMSO.
- **Candidate maximum-signal control** = patient cells + a **proteasome inhibitor** (e.g. MG132).
  The MG132 immunoblot result in PMID 20516114, Fig 3C motivates testing this control, but
  does not validate its effect in this LCL flow assay. Qualify the signal window and record viability and cell-cycle effects before use.
- **The positive control is an abundance-assay control, not a functional-rescue control.** A
  proteasome-inhibitor response does not establish BubR1-specific function or treatment potential;
  candidates still require the counter-screens and functional advancement tests. **[OUR DESIGN]**

**Gate: no compound plate is read until Z′ ≥ 0.4 on validation plates.** Cited in advance so it
cannot be relaxed after seeing data.

## 5. Library — named, and filtered for a reason

| library | size | note |
|---|---|---|
| **Prestwick Chemical Library** | **~1,520** | ~all off-patent approved drugs — **recommended primary** |
| NCATS Pharmaceutical Collection | ~2,750 | approved/investigational, NIH |
| Broad Drug Repurposing Hub | ~6,800 | broadest, richly annotated |

**1,520 compounds in 384-well = 5 assay plates**, once every plate carries its own controls. That
is still the reason to start with Prestwick: the whole primary screen is a handful of plates, not a
campaign.

> 🔻 **CORRECTED 2026-08-31 — the old figure of 4 left no room for the controls this same document
> makes mandatory.** 1,520 / 384 = **3.96**, so four plates hold the library only if **every** well
> takes a compound, leaving **16 wells in total — four per plate** for both control populations.
> But §4 requires a **minimum-signal (DMSO)** and a **maximum-signal (MG132)** population large
> enough to compute a Z′-factor on each plate, and §6 calls hits at **"≥ 3 SD above the plate mean
> of DMSO wells"** — which needs a DMSO population big enough to estimate a mean *and* an SD, **per
> plate**. Four wells cannot do either. Reserving the outer two columns per plate (a standard
> screening layout that also avoids edge effects) gives **320 compound wells**, so
> **1,520 / 320 = 4.75 → 5 plates**. §8's budget already said **"~6 plates + validation"**, which
> contradicted §5's four without explanation; at five plus validation the two now agree.
> **[OUR MEASUREMENT — arithmetic, 2026-08-31.]**

> ### ★ Apply a paediatric-exposure filter to the library BEFORE screening, not after.
> The patient is a child with a cancer-predisposition syndrome. A hit with no paediatric safety data
> — or one contraindicated by his condition — is not a lead, it is a distraction that will absorb
> months of follow-up. **Most repurposing screens filter at the hit stage. Filtering the library
> first costs nothing and removes that failure mode before it happens.** ⚠️ Declare the filter in
> advance and report how many compounds it removed, so the denominator stays honest.
> **[OUR INFERENCE — that most repurposing screens filter at the hit stage rather than the
> library stage is our reading of how such screens are reported, not a surveyed finding. The
> argument for filtering first stands on its own logic and should be judged on that.]**

## 6. Concentrations and hit calling

| stage | design |
|---|---|
| primary | **single concentration, 10 µM**, single well per compound |
| hit threshold | **≥ 3 SD above the plate mean** of DMSO wells, plate-normalised (B-score if plate effects appear) |
| abundance confirmation | **10-point dose–response, 3-fold dilutions from 30 µM, in triplicate** |
| provisional abundance-hit criterion, not functional rescue | **≥ 2-fold increase in BubR1 abundance**, dose-dependent, reproduced on a separate day; functional advancement follows §2 and the full-length plan |

Single-well primary screening is standard **when Z′ ≥ 0.4** — which is what §4's gate exists to
establish. Below that threshold, replicates are needed and the design changes.

## 7. 🔴 Counter-screens — the part that decides whether a hit is real

Our own odds table already prices the biggest risk: **~50% that any hit is a general stress or
proteostasis response rather than anything specific.** These three counter-screens exist to catch
exactly that, and each must be run on every confirmed hit:

1. **Cytotoxicity / viability**, same plates. A compound that kills cells changes every measurement.
   **Non-negotiable, and its absence is the single most common way a screen fools itself.**
2. **An unrelated abundance control protein.** If a compound raises BubR1 *and* an unrelated
   protein, it is affecting global translation or degradation, not BubR1. **This is the counter-screen
   that directly tests our own thesis rather than flattering it.**
3. **Specificity across genotype.** A real BubR1-abundance effect should behave differently in the
   *CEP57* lines, which have a different lesion. A compound that does the same thing everywhere is
   a general effect.
4. 🔴 **CELL-CYCLE DISTRIBUTION — added 2026-08-29, and it may be the most important of the four.**
   **BubR1 is degraded after mitotic exit by APC/C-Cdh1 and is held low in interphase**, so its
   abundance tracks the mitotic fraction. **Any compound that arrests or slows cells in mitosis
   raises measured BubR1 without affecting BubR1 stability at all** — and **counter-screens 1–3 do
   not catch it**: such a compound need not be toxic, it *does* raise BubR1 specifically, and it
   behaves similarly across genotypes. **An approved-drug library contains multiple antimitotics.**
   **Measure DNA content in the same wells and report the distribution and any inclusion/exclusion
   rules.** A gate based solely on a normal diploid DNA-content distribution may distort an
   aneuploid culture; characterise the actual line's chromosome and DNA-content distributions before
   defining such a gate. **MVA has no universal >25% aneuploid-cell minimum:** Matsuura reports
   affected cases with **9–32%** aneuploidy (PMID 16411201, Table I), and Yost reports a case with
   **10%** and culture-dependent changes in another (PMID 28553959, Fig S1). Those chromosome-count
   fractions do not determine the fraction excluded by a DNA-content gate in this assay.
   Flag hits that shift the cycle distribution and assess possible selection explicitly.
   **[Source findings as cited; gating recommendation is OUR DESIGN.]** See also pilot protocol
   §5.13 and §5.13a.

## 8. Cost and duration

| item | estimate |
|---|---|
| cell lines — **5 minimum** (GM21284 + 2 unrelated normals + 2 *CEP57* specificity), **7 with the carrier comparators** — at $262 US-academic / $448 international each | **$1,310–2,240** minimum · **$1,834–3,136** full |
| Prestwick library access (facility-dependent) | **[VARIES — often already held by the facility]** |
| 384-well plates, antibodies, staining reagents, ~6 plates + validation | **$2,000–5,000** |
| high-throughput flow time | **[NOT ESTIMATED — facility rate]** |
| **elapsed time, validation → confirmed hits** | **[ESTIMATE] 3–5 months** |

**[OUR ESTIMATE. Cell-line prices are `[VERIFIED]` from the repository — GM12878 was checked on 2026-08-30 and sits in the same $262/$448 tier. The line COUNT was corrected the same day: the table said 4 while §3 specified 5, and §3 now specifies 7 including the carrier comparators. Everything else is a range
for scoping, not a quote — and labour is not included, not because it is small but because
inventing it would be worse than admitting it.]**

## 9. Adversarial review — of THIS document

The previous adversarial pass in this project reviewed the *stability protocol*, not the screen.
Three attacks on this one:

**A1 — "The primary readout does not measure what you care about."** Partly lands. Abundance is a
proxy for function; a compound could raise a non-functional pool. **MPM-2 arrest alone does not
resolve this:** §2 requires division-level segregation outcomes and distinct attachment,
checkpoint and cell-fate assessments under the full-length plan. **A hit that raises abundance
without restoring function remains possible and does not pass the advancement gate.**

**A2 — "GM21284 is the wrong genotype."** Lands fully. It is `753X/R814H`, not N1002K, so a hit
found here **may not transfer to this child** — the odds table already scores that transfer as
`unknown`. The screen is a **class** experiment, not a personal one, and should be described that
way.

**A3 — "A proteasome inhibitor positive control guarantees a Z′ you cannot achieve with a real
hit."** A qualified proteasome-inhibitor control may provide a much larger signal than candidate
compounds. **Z′ ≥ 0.4 against that control does not
guarantee power to detect a 2-fold change.** ⚠️ **Therefore: a secondary Z′ must also be computed
against a low-effect reference before believing the screen can see what it is looking for.**
*This attack changed the protocol rather than being noted and dismissed.*

## 10. 🔴 THE CRITICAL REAGENT, and an honest risk that could sink the primary readout

**In an intracellular BubR1 flow stain, the antibody IS the assay.** The first version of this
protocol said "intracellular antibody stain" and named nothing — which is the single fastest way to
stall a facility. Closing it surfaced a real problem.

| reagent | identifier | status |
|---|---|---|
| **anti-BUBR1** | **Bethyl A300-386A** | ⚠️ documented in our holdings **at 1:100 for immunofluorescence** — **NOT for flow** |
| MG132 (Z′ maximum control) | Calbiochem, CAS **133407-82-6** | ✅ catalogued |
| **anti-α-tubulin, clone DM1A** — the "unrelated abundance control protein" of §7.2, now named | Santa Cruz **sc-32293**, RRID:**AB_628412** | ✅ catalogued |
| Alexa-conjugated secondary — **anti-MOUSE** | Jackson ImmunoResearch **715-545-150** (Alexa Fluor 488 AffiniPure Donkey Anti-**Mouse** IgG (H+L), *min X*) | ✅ catalogued · 🔴 **corrected 2026-08-30, see below** |

> 🔴 **THE §10.3 RECOMMENDATION CHANGE HAD NOT REACHED THIS TABLE, AND THE PANEL AS LISTED COULD
> NOT HAVE PRODUCED A SIGNAL.** §10.3 ends *"★ RECOMMENDATION CHANGED: use BD 612502 (clone 9),
> not A300-386A"* — swapping a **rabbit polyclonal** for a **mouse monoclonal, IgG2a**. This table
> still listed **Jackson 711-545-152** as the only secondary. Checked against the vendor on
> 2026-08-30, with a positive control run first: **715-545-150 → "Alexa Fluor 488-Donkey
> Anti-Mouse IgG"**, **711-545-152 → "Alexa Fluor 488-Donkey Anti-*Rabbit* IgG"**. An anti-rabbit
> secondary is blind to a mouse primary: the stain would have come back empty and read as
> "the antibody does not work in flow".
>
> **A SECOND PROBLEM THE SWAP CREATES, which was not in the original finding's scope but follows
> from it.** The §7.2 abundance control in this same table, **Santa Cruz sc-32293 (clone DM1A,
> RRID AB_628412)**, is *also* a **mouse monoclonal** — confirmed via the Antibody Registry API on
> 2026-08-30 (`sourceOrganism: mouse, clonality: monoclonal`). Once the BubR1 primary is mouse,
> **two-colour discrimination by host species is gone.** Resolve it before the bench, by one of:
> **(a)** an **isotype-specific** secondary pair — BD 612502 is **IgG2a** and DM1A is **IgG1**, so
> anti-mouse-IgG2a and anti-mouse-IgG1 secondaries separate them cleanly; **(b)** a **directly
> conjugated** α-tubulin reagent; or **(c)** a **rabbit** α-tubulin clone.
>
> ✅ **RESOLVED 2026-08-30 — a better exit than any of the three, and it comes from falsifying a
> different claim.** The pilot protocol's founding negative (*"no anti-BubR1 antibody is
> flow-validated by any vendor"*) turned out to be false: **four Novus clones list flow, and two
> of them dissolve this clash outright.** Either **swap the BubR1 primary to the RABBIT clone
> `NBP3-15207` (7H4)** — two hosts, two secondaries, DM1A stays exactly as it is — **or use a
> directly conjugated 8G1 (`NB100-353AF350`, Alexa Fluor 350)** and drop the BubR1 secondary
> entirely. **Both are cheaper than isotype-specific secondaries and neither requires giving up a
> validated clone.** See `pilot-protocol-bubr1-flow.md` §1 and §1.1 for the datasheet evidence and
> the recommendation. **[OUR INFERENCE from vendor datasheets held at `papers-local/datasheets/`,
> retrieved 2026-08-30.]**
>
> **This document warned about exactly this class of error one section earlier** — §10.2(a):
> *"do not carry this reagent between the two documents"* — and then carried a reagent across its
> own section boundary. The warning was right; the propagation was not done.

> ### The risk, stated plainly
> Janssen A, Kops GJPL, Medema RH, *PNAS* 2009 (**PMID 19855003**) reports **BubR1 immunoblotting**
> and includes a research BubR1 antibody in a combined list covering immunoblotting,
> immunofluorescence and FACS (Materials and Methods, Antibodies; Figs 1–4). The list does not
> establish which application used that antibody. **We have not verified a BubR1 flow-cytometry
> protocol from this paper**; its supporting information was inaccessible in this review.
>
> The separately retained **vendor-flow evidence in §10.3** remains relevant, but does not establish
> quantitative performance in this LCL preparation. It is not strengthened by the Janssen antibody
> list. Application-specific qualification of the selected reagent is still necessary.
>
> **The pilot must establish a specific, quantitative intracellular BubR1 signal in LCLs using the
> selected reagent**, with suitable controls, an orthogonal protein measurement and a qualified
> signal window. The current vendor-listed candidates are in §10.3 and the pilot protocol;
> A300-386A's historical consideration is not validation of the present assay. **Reagent
> qualification comes before the Z′ gate.**

### 10.1 ✅ The catalogue-number discrepancy — investigated to resolution

An earlier version flagged that our holdings disagreed about which antibody detects which protein,
and said "confirm before ordering". **That was not good enough, and it is now resolved definitively
at the gene-identifier level.**

| catalogue | RRID | registry name | **NCBI Gene** |
|---|---|---|---|
| **A300-386A** | **AB_386097** | Rabbit anti-BubR1, affinity purified | **701 = *BUB1B*** ✅ |
| A300-373A | AB_2065943 | Bub1 Antibody | *BUB1* |

**`A300-386A` targets *BUB1B*. This protocol is correct.** Resolved by gene identifier, not by name
matching — a name can be mistyped in a registry; a gene ID cannot mean two things.

**Where the confusion came from: two papers we hold each contradict *themselves*.**
1. One paper's methods correctly state `Bub1 = A300-373A, BubR1 = A300-386A` **and its own RRID
   table agrees** — then a later sentence calls **`A300-373A` "anti-BubR1"**. Wrong once in three
   mentions, inside one paper.
2. 🔴 **More serious: a paper *about biallelic* BUB1 *mutations* has two figure legends stating that
   BUB1 protein was detected "using A300-386A"** — the anti-**BUBR1** antibody — while **its own
   methods section correctly assigns `BUB1 = A300-373A`.** Its western blot of BUB1 levels and its
   BUB1 immunofluorescence panel are both legended with the wrong antibody. The methods section is
   almost certainly right and the legends are typos, but **a reader taking reagents from the figure
   legends of a BUB1 paper would order an anti-BUBR1 antibody.**

**[OUR MEASUREMENT — every occurrence of both catalogue numbers across `papers-local/` was
enumerated; RRIDs resolved via the Antibody Registry; NCBI Gene 701 confirmed as *BUB1B* via
E-utilities. The contradictions are in the published texts, not introduced here.]**

### 10.2 🔴 Two risks the investigation surfaced that nobody had asked about

**(a) The epitope is outside the stability protocol's construct.** A300-386A's epitope is
**aa 350–400**. The companion stability protocol's route A2 expresses **BubR1 (721–1,044)** — the
pseudokinase domain. **The epitope is not in that fragment, so this antibody cannot detect that
construct.** Irrelevant to the screen, which measures full-length endogenous protein, but a
genuine cross-protocol trap: **do not carry this reagent between the two documents.**

**(b) It is an unconjugated rabbit POLYCLONAL, and that is a poor fit for a screen.** Polyclonal
lot-to-lot variability across a campaign running for months is a reproducibility risk that a Z′
computed on one plate on one day will not reveal, and "unconjugated" means a secondary-antibody
step adding background and another source of variation.
> **Therefore the §10 pilot must test more than "does it work once": it must check signal
> reproducibility across at least two lots, and a monoclonal or directly-conjugated alternative
> should be sought in parallel.** A screen whose primary reagent drifts between lots produces hit
> lists that cannot be compared across plates.

### 10.3 ✅ Is any anti-BUBR1 antibody validated for flow? — asked and answered. No.

An earlier version left this "for a human to confirm with the vendor". It is now settled from the
vendors and the literature, and **the answer changes which antibody this protocol recommends.**

| | **A300-386A** (Bethyl/Thermo) | **612502 / 612503** (BD, clone 9) |
|---|---|---|
| format | **rabbit POLYclonal** | ✅ **mouse MONOclonal, IgG2a** |
| vendor-validated | Western blot (1:2,000–1:15,000), **IP only** | WB, **immunofluorescence**, ELISA, ICC, IP |
| **knockout-validated** | not stated | ✅ **yes** |
| **flow cytometry** | ❌ **not listed** | ❌ **not listed** |
| epitope | aa **350–400** | aa **276–388** |

> ### 🔴 **Neither of these two** antibodies is vendor-validated for flow cytometry.
> **Earlier headings exceeded the evidence.** A two-product check and one product's citing
> literature could not support either a field-wide absence of vendor-listed flow reagents or a
> field-wide absence of published BubR1 flow methods. The retained evidence supports these
> separate conclusions:
> **(i)** four Novus/Thermo clones (**8G1, OTI6E5, 7H4, 23GB1640**) *are* vendor-listed for flow at
> 1 µg/10⁶ cells, several with an intracellular histogram on HeLa — see
> `pilot-protocol-bubr1-flow.md` §1.
> **(ii)** The earlier appeal to Janssen's combined antibody list (**PMID 19855003**) as a BubR1
> FACS precedent was unsupported. The paper reports BubR1 immunoblotting; we have not verified a
> BubR1 flow protocol from it (§10). That limitation does not negate the separately documented
> vendor-flow listings above, which still require qualification in the proposed LCL assay. The
> `A300-386A` measurement below concerns **one product's
> citing literature, not the field as a whole**, and that is exactly the narrowing that was lost when it
> was promoted to a heading.
>
> **What remains true:** 39 papers cite `A300-386A`; six also mention flow
> cytometry; **in every case the antibody sits in a WESTERN-BLOT list at 1:1,000–1:2,000 while the
> flow in that paper is doing something unrelated** — sorting YFP⁺ cells, BODIPY lipid staining,
> BrdU incorporation. **The six hits were co-occurrence, not usage.**
> **[OUR MEASUREMENT — Europe PMC full-text search, each hit's full text retrieved and the usage
> context read. A hit count is not a usage count.]**

**★ RECOMMENDATION CHANGED AGAIN, 2026-08-30: use clone 8G1 or 7H4, not BD 612502 and not
A300-386A.** BD's own product page lists 612502 for *"Western blot (Routinely Tested),
Immunofluorescence (Tested During Development)"* **only** — this document previously credited it
with WB, IF, ELISA, ICC and IP, which overstated it. Meanwhile **8G1 and 7H4 ARE vendor-listed for
flow at 1 µg/10⁶ cells**, with intracellular-stain figures on HeLa; see
`pilot-protocol-bubr1-flow.md` §1. The reasoning below is kept because it is still the right
reasoning — it was simply applied to too small a candidate set.

**★ SUPERSEDED RECOMMENDATION (2026-08-29): use BD 612502 (clone 9), not A300-386A.** Neither is flow-validated, so
the pilot is mandatory either way — but clone 9 is the better bet on every axis that matters here:

1. **Monoclonal** — removes the lot-to-lot variability that makes a polyclonal a poor reagent for a
   campaign running months. §10.2(b)'s risk is designed out rather than tested around.
2. **Knockout-validated** — the strongest available specificity evidence.
3. **Immunofluorescence-validated** — and **IF is a far better predictor of intracellular flow than
   western blot is**, because both require the epitope to survive fixation and permeabilisation in
   situ. A300-386A is not even IF-validated by its vendor, though papers use it that way.

⚠️ **The epitope (aa 276–388) is likewise outside the stability protocol's 721–1,044 construct**, so
§10.2(a)'s cross-protocol warning stands unchanged for this antibody too.

### 10.4 The contingency, named now rather than discovered later

Because **no antibody is validated for this application**, there is a real chance the pilot fails —
not because the biology is wrong but because no reagent detects BubR1 well enough in flow.

**If it fails, the fallback is a tagged reporter line** — endogenous BubR1 tagged with a fluorescent
protein, read directly with no antibody at all. That removes the reagent risk entirely and gives a
cleaner quantitative signal. **It is also a substantially larger and slower project**, requiring
genome editing in a patient-derived line.
**Naming it now means the pilot has a decision attached to its failure**, rather than becoming the
point at which the screen quietly stalls.

## 11. What the published experiments calibrate

**Neither protocol is already calibrated for N1002K.** The fragment protocol includes WT and
candidate comparators whose roles need qualification in the chosen construct and assay.
N1002K is the unknown. Published WT-fragment unfolding curves and the full-length WT/K795A thermal
pair inform development, but do not establish K795A separation or Q921H neutrality in the fragment
assay (PMID 22698286, Fig 3G/S3D and S3G–H). Q921H's WT-like cellular abundance, segregation,
alignment and checkpoint results do not supply fragment thermal calibration (PMID 20516114,
Fig 4D and S2A–B). Counting catalogue numbers or numerical observations does not establish a
validated control set.

Drug-induced BubR1-abundance measurements do exist: Suijkerbuijk 2010 **Fig 3C** tests WT, I909T
and L1012P with cycloheximide, geldanamycin and MG132 (**PMID 20516114**). It reports loss of the
mutant proteins under HSP90 inhibition and prevention of enhanced turnover under proteasome
inhibition. These are **immunoblot measurements in transfected cells**, not validation of this
intracellular-flow screen, its signal window or its hit threshold. They motivate testing MG132
as an abundance-assay control; they do not guarantee its performance here or establish rescue.

**The ≥2-fold abundance criterion in §6 is a provisional design choice, not a threshold derived
from those papers.** A pilot must establish the actual assay's signal window and precision, then
justify and freeze hit criteria before confirmatory screening. The fragment study likewise needs
control and method qualification; neither a calculated detection limit nor a proposed comparator
substitutes for those measurements.

Both documents can support laboratory design review and qualification work. Functional advancement
requires the separate full-length plan, not a fragment melting result or an abundance hit alone.

## 12. What still needs a person

- 🔴 **A screening facility.** Nothing here can be ordered by us.
- MTAs for the cell lines; library access is facility-dependent.
- **The paediatric filter list** should be reviewed by someone with paediatric pharmacology
  expertise before it is applied — filtering wrongly is as harmful as not filtering.
- **A2 above is a scoping decision**, not a technical one: is this a screen for *this child*, or for
  *BUB1B*-MVA as a class? **The honest answer is the class, and the document should not be allowed
  to drift into implying otherwise.**
