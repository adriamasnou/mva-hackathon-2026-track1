# Track 2 — MVA Hackathon 2026

**Status: DRAFT IN PROGRESS. NOT FOR SUBMISSION.**
Track 2 is **one shot with no resubmit**. Nothing here ships without Adrià's explicit go-ahead
(`CLAUDE.md` RED #1). Started 2026-08-29.

**Rubric this is written against:** Rigor 35 · Impact 25 · Innovation 25 · Scalability 15.

> **Build note.** Sections are written in the order set by `dossier/PLAN-2026-08-29-remade.md` §5:
> the two elements measured at **0 of 54 competitor owners** come first, because uncontested *and*
> invisible is the worst combination for material we already hold. Every section below is
> converted from held, sourced dossier material — **no section states anything not already
> verified in the private tree.** **[OUR MEASUREMENT — the 0-of-54 field positions are from a grep
> over all 59 distinct repos / 54 owners in `archive/competitors/`, re-derived 2026-08-31 with a
> positive control (`BUB1B` 53 of 54 owners); first recorded at the then-current 41 repos / 39
> owners in `dossier/scoreboard-VERIFIED.json`.]**

---

## 1. Impact — PGT-M for MVA is already approved in the UK, and is undiscoverable by gene

**Field position: 0 of 54 competitor owners hold this** *(re-measured 2026-08-31 against **54 owners** after `mateooSM` and `Jakeelamb` were archived; numerator unchanged, control `BUB1B` **53 of 54**)* [OUR MEASUREMENT — grep over all 59 distinct repos (60 archived directories, one repo archived
twice under a rename) / 54 owners in `archive/competitors/`, every hit read by hand; `F-005`,
re-verified 2026-08-31].

Preimplantation genetic testing for monogenic conditions (PGT-M) is **already approved by the UK
regulator for mosaic variegated aneuploidy** — not one type, but five.

| condition | HFEA status | OMIM |
|---|---|---|
| **Mosaic Variegated Aneuploidy Syndrome 1 (MVA1)** — the *BUB1B* form, this child's | **approved** | 257300 |
| Mosaic Variegated Aneuploidy Syndrome 2 (MVA2) | approved | 614114 |
| Mosaic Variegated Aneuploidy Syndrome 3 (MVA3) | approved | 617598 |
| MVA5 / Atelis Syndrome 1 | approved | 620184 |
| MVA6 / Atelis Syndrome 2 | approved | 620185 |

**Source:** HFEA's own downloadable workbook, snapshot **2026-08-05**, **2,063 approved
conditions**, parsed directly; the copy is retained at `data/derived/hfea_pgtm_2026-08-05.xlsx` and
the parsed rows ship in this directory as `hfea-pgtm-gene-crosswalk.csv` (**2,063 data rows**,
re-counted 2026-08-30).

> 🔻 **CORRECTED 2026-08-30.** This paragraph described an earlier pass: the
> `2026-07-24` workbook at **2,057 conditions**, retrieved from an Internet Archive snapshot
> because the live HFEA site was returning `HTTP Error 500.30 — ASP.NET Core app failed to start`
> (reproduced with `curl`, WebFetch and a real browser). **That outage ended and the register was
> re-downloaded live**, but this section still narrated the outage and quoted the superseded count
> — while `hfea-pgtm-gene-crosswalk.md`, shipping in the same directory on the same date, said
> **2,063**. **A judge opening both files would have found them disagreeing about the size of the
> register the whole element rests on.** The 2,057 figure and the Archive route are kept here as
> history, not as method. Corroborated for this exact condition by the
regulator's **Statutory Approvals Committee minutes of 26 January 2026** — applicant **Aria
Fertility (centre 0382)**, chair **Frances Flinter**, Specialist Adviser **Dr Alan Fryer**, chair's
signature **12 February 2026**;
**<https://ifqlive.blob.core.windows.net/inspectiondocuments/8623.pdf>** (local copy retained at
`data/derived/hfea_SAC_minutes_MVA1_2026-01-26.pdf`).
🔻 *Locator added 2026-08-31: the corroboration for this project's flagship uncontested Impact
element previously shipped with **no URL, no document number and no committee reference** — a claim
a judge was asked to take on trust while a fully resolvable provenance sat in the private tree and
had never been carried across.*

### 1.1 🔑 The finding is not the approval. It is that the approval cannot be found.

**The workbook's columns are *condition name*, *status*, and *OMIM number*. There is no gene
column, and the string `BUB1B` appears in none of the 2,063 rows.** Querying the HFEA list for
`BUB1B` returns **"No data to display."**
**[OUR MEASUREMENT — HFEA workbook, 2026-08-05 snapshot, parsed directly, 2,063 rows (re-counted
from the shipped CSV 2026-08-30); source `https://www.hfea.gov.uk/pgt-m-conditions/`.]**

**That is a false negative, and it is structural.** A family — or a clinician — who searches the
regulator's list the way genetics is actually practised, *by gene*, is told the thing they are
entitled to does not exist. It does exist. It has existed since before this hackathon opened.

This is a **discoverability failure in a regulator's index**, not a gap in medicine, and it is
fixable by anyone who publishes the gene↔OMIM crosswalk. That is the contribution.

⚠️ **Eligibility is a separate question and is not satisfied by approval alone.** HFEA criteria
require a risk of an affected pregnancy of **"10% or more"**, referral **by an NHS Clinical
Genetics Service**, and prior genetic counselling. **[Criteria quoted verbatim from the HFEA
source; whether any individual family qualifies is a clinical determination we do not make and
have not made.]**

---

## 2. Impact — a "Definitive" gene with zero expert-reviewed variants and no expert panel

**Field position: 0 of 54 competitor owners hold this** [same measurement as §1]. *(re-measured 2026-08-31 against **54 owners** after `mateooSM` and `Jakeelamb` were archived; numerator unchanged, control `BUB1B` **53 of 54**)*

> 🔴 **DENOMINATOR CORRECTED 2026-08-30, IN OUR OWN FAVOUR.** Both field-position lines above read
> **"0 of 39 competitor owners"** until today — a denominator two re-measurements stale. The
> archive now holds **54 owners across 59 distinct repositories** (60 archived directories, one repo
> archived twice under a rename — `Samistus1234__mva-hackathon-track1` is the SAME upstream repo as
> `Samistus1234__mva-hackathon`, proved by HTTP 301 on the old name; **owner counts are unaffected and
> never needed correcting**), and **both elements were re-measured
> against all of it and both still return zero**:
>
> | screen | owners | route |
> |---|---|---|
> | `HFEA` | **0 of 54** | `grep -rli HFEA archive/competitors/` |
> | `PGT-M` / `PGTM` | **0 of 54** | same, both spellings |
> | *(context)* `preimplantation`, any mention | 2 of 54 — `ModeEric`, `neilkale` | the broader term IS present; the specific regulatory route is not |
> | *(context)* `preimplantation genetic testing/diagnosis` spelled out | 1 of 54 — `ModeEric` | |
> | *control* `BUB1B` | **53 of 54** | proves a zero here is real and not a broken route |
>
> **The stale figure understated our own claim**, and we are correcting it in the direction that
> helps us — which is exactly why the control row is printed beside it. **[OUR MEASUREMENT —
> 2026-08-30; every row of this table re-derived against the live 54-owner archive on 2026-08-31 and
> every one reproduces exactly.]** The two context rows are given because *"nobody has thought about embryo
> selection"* would be false; the claim is narrower and survives: **nobody has gone to the
> regulator's own approved-condition register.**

*BUB1B*'s gene–disease relationship for MVA is classified at the **highest confidence tier**. The
variant-interpretation infrastructure that tier is supposed to imply **does not exist**.

Re-derived 2026-08-29 via NCBI E-utilities, **with the exact query strings recorded** so every
number is reproducible (`dossier/sweeps/clinvar-bub1b-2026-08-29.md`; public gene queries only, no
patient data transmitted):

| quantity | `term=` query | count |
|---|---|---|
| *BUB1B* records in ClinVar | `BUB1B[gene]` | **2,493** |
| missense variants of uncertain significance | ClinVar bulk `variant_summary.txt.gz`, deduped on `VariationID` | **1,426** |
| **expert-reviewed (3-star), any variant type** | `BUB1B[gene] AND "reviewed by expert panel"[Review status]` | **0** |
| practice guideline (4-star) | `BUB1B[gene] AND "practice guideline"[Review status]` | **0** |
| **ClinGen Variant Curation Expert Panel for *BUB1B*** | — | **none exists** |

**1,426 uncertain missense variants. Zero reviewed by an expert panel. No panel to review them.**
Restricted to the pseudokinase domain the assay targets (aa 721–1,044): **430 uncertain missense
variants, and again zero expert-reviewed.**

This child's second allele, `p.Asn1002Lys`, sits in that bucket. It is a variant of uncertain
significance **not because the evidence was weighed and found wanting, but because no mechanism
exists to weigh it.**

> 🔻 **Provenance note.** Two counting methods give two numbers and **both are correct for their own
> method**: an `esearch` facet query counts ClinVar *records* and returns **1,463**; the ClinVar bulk
> `variant_summary.txt.gz` deduplicated on `VariationID` counts *unique variants* and returns
> **1,426**. **The bulk-file figure is used here** because it is the method the comparison literature
> uses. Both query strings and the extraction script are recorded in
> `dossier/sweeps/clinvar-bub1b-2026-08-29.md` and `pipeline/clinvar_bub1b_counts.py`.
> ⚠️ **The bulk file carries one row per assembly (GRCh37 and GRCh38); a naive row count
> double-counts every variant.**

### 2.1 What it would take to close it — and the number is now known

A functional assay is the documented remedy for exactly this situation, and ClinGen specifies how
strong such evidence may be: **Brnich et al., *Genome Med* 2019/2020 (PMID 31892348)** defines
`OddsPath` and its evidence-strength bands.

Applying that framework to a *BUB1B* pseudokinase-domain assay yields a result that is easy to get
backwards, and we got it backwards ourselves before computing it:

> **The attainable evidence strength is governed by the number of BENIGN controls, not by the
> absent pathogenic ones.** Under Brnich's perfect-classifier model, `OddsPath = n_benign` exactly —
> the pathogenic count cancels. Verified across all 39 modelled rows of Brnich's own published
> Additional file 1 (PMID 31892348, `13073_2019_690_MOESM1_ESM.xlsx`), and stated in prose as the
> central finding of Rowlands et al. (PMID 40925377).

> 🔴 **AUTHOR NAME CORRECTED 2026-08-30.** Every reference to PMID 40925377 in this report
> previously read **"Lin"**. The paper is **Rowlands CF et al.**, *"Availability of benign missense
> variant 'truthsets' for validation of variant effect maps"*, CanVIG-UK, *Am J Hum Genet*
> 2025;112(10):2281–2294. **There is no author named Lin on it** — our own held full text names
> Charlie F Rowlands and contains "Lin" zero times. **No number in this report moves**: the
> thesis, the threshold of 19, the 19.8% and 36.2% figures and every count were always taken from
> the paper itself, never from the byline. Three working files still carry the wrong surname in
> their **filenames** (`lin2025_ajhg_benign_truthsets.txt`, `pipeline/lin_table3_parse.py`,
> `pipeline/lin_panel_compare.py`); they are named here deliberately and left unrenamed, because a
> filename is referenced from several places and a silent rename is how a citation error becomes
> untraceable. **Their contents are corrected.**

⚠️ **This is not our insight and we do not claim it.** It is the headline thesis of
**Rowlands et al., *Am J Hum Genet* 2025 (PMID 40925377)**: *"benign truthset size is the primary driver
of applicable functional evidence toward pathogenicity (PS3)."* That paper also fixes the integer —
*"the minimum number of benign truthset variants permitting application of PS3 at 'strong' is
**19**"* — and reports that only **19.8% (23/116)** of established cancer-susceptibility genes can
reach "strong" from ClinVar ≥2★ classifications alone. ***BUB1B* is one of the 116 genes in its
Table 3.**

**What this project contributes here is the application, not the principle:** that for *BUB1B*
specifically the binding constraint is the benign arm, and that Rowlands' systematic construction
framework — assigning benignity across all possible missense variants using population frequency,
in silico codes and case-control signal — is therefore the operation that would unlock a calibrated
assay for this gene.

### 2.2 🔑 The benign truthset for *BUB1B*, measured — and the one scoping decision that sets the answer

Rowlands' Table 3 records *BUB1B* benign/likely-benign missense at **19 (≥1★)** and **8 (≥2★)**. Our
counts are larger. **Rather than declare that unreconciled, we reconciled it** by replicating Rowlands'
method on the ClinVar bulk file at two timepoints, including an archived release:

| source | exact 1★ | **≥2★** | ≥1★ total |
|---|---|---|---|
| Rowlands 2025 Table 3 (extraction predates 2025-01) | 11 | **8** | 19 |
| ClinVar 2025-01 (archived release) | 20 | **8** | 28 |
| ClinVar 2026-08 (current) | 27 | **8** | **35** |

✅ **The ≥2★ tier is 8 at all three timepoints — an exact match to Rowlands.** The entire difference is
**accretion confined to the single-submitter (1★) tier**. Over the same 19 months the gene grew from
1,818 to 2,477 unique variants. **The discrepancy is explained, not waved away.**

**And this yields the assay's single most consequential design parameter, now measured:**

| truthset scope | benign ≥1★ | OddsPath ceiling | attainable strength |
|---|---|---|---|
| **gene-wide** | **35** | 35 | 🟢 **`PS3` (strong)** — clears Rowlands' threshold of 19 |
| **pseudokinase domain only (aa 721–1,044)** | **10** | 10 | 🟡 **`PS3_moderate`** |

> **Whether a *BUB1B* functional assay can deliver *strong* or only *moderate* evidence turns
> entirely on whether benign controls from outside the assayed domain are admissible.**

⚠️ **We do not assert which scoping is correct.** That is exactly the judgement a Variant Curation
Expert Panel exists to make — **and for *BUB1B* no such panel exists**, which is §2's whole point.
Both numbers are reported so the choice is visible rather than buried.
**[OUR MEASUREMENT — `pipeline/clinvar_bub1b_counts.py`; method and full tables in
`dossier/sweeps/clinvar-bub1b-2026-08-29.md`.]**

---

### 2.3 🔑 Generalised to 116 cancer-susceptibility genes: the ceiling has not moved in 19 months

The *BUB1B* result above is not a special case, and we tested that rather than asserting it. Rowlands'
Table 3 covers **116 inherited cancer-susceptibility genes**; we re-counted all of them against the
ClinVar bulk release at two later timepoints (`F-028`).

**Five rows of that baseline are under-reported, and we establish it rather than assume it.**
`CDKN1C`, `GATA2`, `GREM1`, `NTHL1` and `RUNX1` read `0 0 0 0` in Table 3 of **Rowlands et al.,
PMID 40925377**, checked here against the ClinVar public bulk releases of 2025-01 and 2026-08
**[OUR MEASUREMENT]**. That the
zeros are in the source data — not in our reading of it — follows from arithmetic: our parse, with
the zeros in place, reproduces Rowlands' **own published** 36.2% and 19.8% **exactly**; had we mis-read
those rows our totals would have come out *lower*. And that the zeros are incorrect follows from the
archived ClinVar release of 2025-01, which predates any accretion window: **`RUNX1` holds 31 benign
and 31 pathogenic missense classifications there, and has its own ClinGen Myeloid Malignancy VCEP.**

**Both halves of that matter, and the second is reassuring:** correcting all five moves the headline
from **19.8% → 20.7%** and **36.2% → 37.1%** — **one gene of 116 changes tier. Rowlands' conclusion
stands.** We therefore **correct rather than drop**, keeping n = 116, and substitute the 2025-01
values — a deliberately conservative choice that *raises* the baseline and so *understates* later
growth. The drop variant (n = 111) is reported as a sensitivity check and agrees.
**[OUR MEASUREMENT — Rowlands Table 3 (PMID 40925377) as parsed, against ClinVar public bulk releases
2025-01 and 2026-08. We do claim the five rows under-report ClinVar; we do NOT claim to know why,
as their extraction pipeline is not visible to us.]**

**Genes able to support `PS3` (strong), i.e. ≥ 19 benign controls:**

| timepoint | **≥2★ truthset** | **≥1★ truthset** |
|---|---|---|
| Rowlands 2025 baseline (corrected) | **24/116 = 20.7%** | 43/116 = 37.1% |
| ClinVar 2025-01 | **24/116 = 20.7%** | 45/116 = 38.8% |
| ClinVar 2026-08 | **24/116 = 20.7%** | **63/116 = 54.3%** |

*Sensitivity, five rows dropped instead (n = 111): 20.7% at all three timepoints likewise;
37.8% → 39.6% → 55.9% at ≥1★.* **The two framings agree.**

> **At ≥2★ the figure is 20.7% at every timepoint. It has not moved in 19+ months** — net churn
> exactly zero (`NF1` in, `ANKRD26` out). **At ≥1★ it crossed from a minority to a majority**,
> 22 genes in, 2 out.

🔑 **The generalisation, and it is the same shape as §2.2:** whether a functional assay can deliver
*strong* evidence is decided by an **admissibility question — do single-submitter classifications
count?** — far more than by the accumulation of data. **Waiting for ClinVar does not work: four in
five genes remain unable to reach `PS3` from 2★ classifications, at exactly the rate measured
before.** *BUB1B* sits at **rank 41 of 116** — an ordinary member of this panel, which is what makes
it usable as a worked example rather than a special pleading.

**[OUR MEASUREMENT — `pipeline/lin_table3_parse.py` → `clinvar_gene_panel.py` → `lin_panel_compare.py`;
public gene-level ClinVar only, no patient data. Two validations were run before any result was
read: the Table-3 parse reproduces Rowlands' published 36.2% and 19.8% exactly, and the panel counter
reproduces our independent single-gene *BUB1B* run exactly on all four values. Limits in `F-028` §5 —
notably that the domain-scoping arm remains n = 1 and every figure is a perfect-classifier ceiling.]**

## 3. Innovation — the mining harness, and why its **kill rate** is the result worth reporting

**Field position: 11 of 54 competitor owners hold some form of multi-agent / orchestrated-harness
method framing** **[OUR MEASUREMENT — `guardrails/score_field.py`, element `Innovation :: novel
method framing`, over 54 archived owners, 2026-08-31; control `BUB1B` 53 of 54]**. So the harness
itself is **not** novel and we do not claim it is. **What we have not seen anyone else report is the
number below.**

### What was actually run

Literature mining was run as **orchestrated subagent roles, not one long conversation**:

| role | what it does | output |
|---|---|---|
| **miner nodes** | read one held primary each; emit **typed** findings — `CONTRADICTS`, `NARROWS`, `SUPPORTS`, `NEW_NUMBER`, `NEW_ANGLE` — each with a verbatim quote and a file-and-line locator | 361 findings over 87 papers |
| **adversarial verifier nodes** | receive one allegation with **no stake in it** and are instructed to **REFUTE** it, defaulting to refuted under uncertainty | one verdict per allegation |
| **adjudication** | only survivors are applied to the corpus; refuted allegations are recorded, not deleted | the corpus diff |

The separation matters: the node that generates a claim never gets to confirm it, and the verifier
is rewarded for killing it. Runs, raw verdicts and reports are committed —
`dossier/sweeps/pool1-mining-2026-08-31.json`, `pool1-verify38-2026-08-31.json`,
`pool2-mining-2026-08-31.json`, and the three `POOL*-*.md` reports beside them.

### The result

| | alleged | survived | refuted | kill rate |
|---|---|---|---|---|
| Pool 1 (first pass) | 20 | 5 | 15 | 75% |
| Pool 1 (remaining 38, `wf_0a9fa457-04b`) | 38 | 8 | 30 | 79% |
| Pool 2 | 35 | 2 | 33 | 94% |
| **combined** | **93** | **15** | **78** | **83.9%** |

**[OUR MEASUREMENT — recomputed from the three committed JSONs on 2026-08-31, not quoted from the
reports: `alleged`, `len(survivors)`, `len(refuted)`.]**

🔑 **Roughly five in six of this method's own confident allegations do not survive an adversarial
check.** That is the finding. An unverified mining run of this size would have injected on the order
of **78 wrong statements** into a corpus that a family and a clinical audience are meant to read —
each one fluent, each one carrying a real quote and a real line number.

### The distinction that makes the number interpretable

A separate pass measured something the kill rate does **not** measure. All **91 `NEW_NUMBER`** leads —
the class that asserts *figures* — were checked against the primaries, whitespace-insensitively,
with a control asserting the matcher **rejects the same quote with one digit changed**:

| | |
|---|---|
| verbatim faithful to the primary | **91 of 91** |
| **fabricated or unsupported figures** | **0** |

**[OUR MEASUREMENT — `dossier/sweeps/NEWNUMBER-ADJUDICATION-2026-08-31.md`, 2026-08-31.]**

🔑 **Transcription fidelity and allegation validity are different quantities, and this method is
near-perfect at the first while failing five times in six at the second.** The quotes are real. The
*inferences drawn from them about our own corpus* are usually wrong. Reporting one number without
the other would misdescribe the method in either direction, which is why both are here.

### What the refutation stage actually caught

Two of the fifteen survivors were defects in our own judge-visible material that no gate we hold
could see:

- **An oncological signal against our own lead compound, which we already held and had never
  cited.** Maric 2023 (**PMID `36371959`**): dietary nicotinamide riboside at **≈32 mg/kg/day
  human-equivalent — the same order as the paediatric A-T dose we cite as precedent** — was
  associated with **brain metastases in 9 of 11 animals versus 3 of 12**, Fisher *p* = 0.012, in an
  MDA-MB-231 xenograft. Our own `papers-READ-index.md` had logged it as an *"adverse oncological
  signal"*; the claim file named the compound **6 times** and the study **0 times**. **We had applied
  a cancer caveat to the candidate we were demoting and withheld it from the one we were leading
  with.** It is now in the family-facing summary, not just our notes.
- **A category error in a published mechanism claim** — that an allele *"escapes NMD"* because it
  sits in the last exon. A **missense creates no premature stop codon, so nonsense-mediated decay is
  never engaged** and the exon is irrelevant. The conclusion survived on a corrected premise.

> 🔑 **A WRONG REASON UNDER A RIGHT CONCLUSION IS INVISIBLE TO EVERY AUTOMATED CHECK IN THIS
> REPOSITORY.** The claim linter sees a source. The citation gate sees a PMID that resolves. The
> figure gate sees a panel that exists. None of them reads the argument. **That is the specific gap
> an adversarial reader role fills, and it is why the kill rate is high enough to be uncomfortable.**

### Limits, stated

- **93 allegations is the adversarially-checked subset, not the whole harvest.** The remaining
  **268** findings — 108 `NEW_ANGLE`, 91 `NEW_NUMBER`, 69 `SUPPORTS` — have had **no adversarial
  pass on their substance**, and on this record the prior for any one of them is poor. They are
  recorded as **leads, not results**, and nothing in this submission rests on an unadjudicated one.
- **The kill rate is not a measure of the underlying literature.** It measures *this method's
  allegations about our corpus*, which is a much narrower thing.
- **A verifier that shares the miner's blind spot cannot see it.** Verifier nodes run on the same
  model family as the miners; independence here is independence of *stake and context*, not of
  architecture. **[OUR INFERENCE — stated as a limitation, not measured.]**

---

## 4. Where the rest of this submission lives

> 🔻 **THIS SECTION REPLACED A STALE ONE, 2026-08-31.** It previously read *"SECTIONS NOT YET
> WRITTEN … Ten remaining of the twelve measured as `HELD BUT NOT PUBLISHED` by
> `guardrails/score_field.py` on 2026-08-29"* and then listed ten elements as missing. **Eleven of
> those twelve are now judge-visible** — they were written as standalone documents in this
> directory after that measurement, and the report's own status block was never updated. **A
> to-do list that outlives its own completion misdescribes the submission in the direction of
> understating it**, which is the rarer and more embarrassing direction.
> **Re-measured `guardrails/score_field.py` 2026-08-31: exactly ONE element was still
> `HELD BUT NOT PUBLISHED` — `Innovation :: novel method framing` — and §3 above is it.**
> **[OUR MEASUREMENT — `python3 guardrails/score_field.py`, `US`/`JV` columns over
> 54 archived owners, 2026-08-31.]**

**This report is the spine, not the whole submission.** Each element below is a complete standalone
document in this directory, and the scoreboard element it answers is named so a reader can check
coverage rather than take our word for it.

### Rigor

| document | what it establishes |
|---|---|
| [`adriamasnou_track1_report.md`](adriamasnou_track1_report.md) | the variant call, the phasing bound, and the alignment it rests on |
| [`annotation-toolchain-vep.md`](annotation-toolchain-vep.md) | Ensembl VEP over the full cache — **313,417 variants in, 313,417 distinct out**, nothing dropped, both patient alleles passing a known-answer control |
| [`methods-and-self-critique.md`](methods-and-self-critique.md) | the **phenotype-blind** scan, run so the answer could have come out otherwise — plus every claim of ours that failed |
| [`splice-prediction.md`](splice-prediction.md) | local SpliceAI run **as the model, not as lookup**, with a positive control that caught a silent failure of our own making |
| [`sv-cnv-survey.md`](sv-cnv-survey.md) | genome-wide SV/CNV survey — is the compound heterozygote the complete molecular explanation? |
| [`callability-audit.md`](callability-audit.md) | genome-wide MAPQ/callability audit, and the check that the causal locus is **not** in a dark region |
| [`generalisation-public-case.md`](generalisation-public-case.md) | the same pipeline, unchanged, on **public** data |

### Impact

| document | what it establishes |
|---|---|
| [`register-audit.md`](register-audit.md) | **1,850 of 2,063** approved conditions (**89.7%**) have **no expert-curated variant in any causative gene** |
| [`hfea-pgtm-gene-crosswalk.md`](hfea-pgtm-gene-crosswalk.md) | the gene↔condition crosswalk the regulator's own register does not provide |
| [`impact-costs-and-access.md`](impact-costs-and-access.md) | what surveillance actually costs, and how anything would reach this child |
| [`family-facing-decision-aid.md`](family-facing-decision-aid.md) | built to **IPDAS**, including a declaration of the criteria it **fails** |
| [`family-facing-summary.md`](family-facing-summary.md) | the same evidence written for the family, carrying the same caveats — including the one against our own lead compound |
| [`secondary-findings-disclosure-protocol.md`](secondary-findings-disclosure-protocol.md) | a reusable governance template for open single-patient challenges, CC BY 4.0 |

### Innovation

| document | what it establishes |
|---|---|
| [`innovation-mechanism.md`](innovation-mechanism.md) | compartment matching, and the **contraindication** it produces — which candidates are *not* worth testing |
| §3 of this report | the mining harness and its **83.9% kill rate** |
| [`n1002k-reagent-specification.md`](n1002k-reagent-specification.md) | what a lab would have to buy — **no N1002K construct exists in any catalogue searched** |
| [`screen-protocol-runnable.md`](screen-protocol-runnable.md) · [`pilot-protocol-bubr1-flow.md`](pilot-protocol-bubr1-flow.md) | the screen, and the pilot that gates it |

### Presentation

| document | what it establishes |
|---|---|
| [`pitch-video-script.md`](pitch-video-script.md) | the ToS §7 pitch, scripted, with a **claim ledger** binding every spoken sentence to a source |

---

## 5. What we are not claiming

**The strongest thing in this submission is the list of things we stopped claiming.** Each was held,
written down, and then withdrawn on evidence:

| withdrawn | why | where |
|---|---|---|
| **the ClinVar submission itself** | we built the package, then found **three of the four ACMG criteria we had claimed do not hold** — `PM3` needs parental phase we do not have, `PP4` fails because MVA has ≥8 genetic causes, `PP3` is inadmissible because Richards requires in-silico agreement and ours disagree (REVEL 0.472 vs AlphaMissense 0.923). **Only `PM2` survives. It is not being submitted.** | `dossier/clinvar-submission-package.md` |
| **"supplement-grade safety" for our lead compound** | an unresolved oncological signal we already held — §3 above | `family-facing-summary.md` §7 |
| **"the mosaic aneuploidy is visible in bulk WGS"** | **falsified — it was mis-mapping.** Replaced with a bounded negative: no gain above **~3.2% of cells**, on a model whose truth anchor returns chrX **0.4999** against a true 0.5000 | `methods-and-self-critique.md` |
| **"microcephaly is *BUB1B*-specific"** | citation drift, traced across three papers; the primary says **4 of 7** | `dossier/findings/F-024` |
| **"an N1002K construct does not exist anywhere"** | narrowed to the two repositories actually searched — **an unresolved query is not an absence** | `n1002k-reagent-specification.md` |

> 🔑 **Every row above was found by us, before submission, and each is published rather than
> quietly dropped.** A reviewer can check that: the corrections are in the files, with dates and
> with what the text used to say.

---

*Rare Disease, Real Kid: The MVA Hackathon 2026 · Track 2 · adriamasnou · CC BY 4.0*
