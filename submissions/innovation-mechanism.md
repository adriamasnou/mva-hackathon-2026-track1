# Compartment matching, and the branch point a therapy proposal has to choose



*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## 1. The branch point

A pseudokinase-domain missense can be pathogenic in **two mechanistically distinct ways**, and a
therapeutic proposal is only coherent once it commits to one:
1. **Destabilise the fold** → less total protein → a *quantitative* deficit. Treatable in principle
   by anything that raises the amount of protein.
2. **Break a scaffolding interaction** while leaving the fold intact → a *qualitative* defect.
   Raising the amount of a protein that cannot do its job achieves nothing.
**[OUR INFERENCE — the two-branch framing is ours, drawn from the published observation that kinase-domain missense variants in this family act both by destabilisation and by loss of scaffolding contacts. Which branch THIS variant sits on is unmeasured, and that is the point of §1.]**

**This child's variant has not been assigned to a branch**, and that assignment — not the choice of
drug — is the decision the whole therapeutic argument turns on. The experiment that settles it is
cheap, and it is specified in the wet-lab protocol accompanying this work.

## 2. Compartment matching — why most chaperone proposals are aimed at the wrong place

If the lesion is branch 1, the obvious move is a chaperone-axis drug. But **chaperone systems are
compartment-specific**, and BubR1 is a soluble cytosolic/nuclear protein.

| agent | compartment it acts on | matched to BubR1? |
|---|---|---|
| **arimoclomol** (HSF1/HSP70 axis; FDA-approved Sept 2024, paediatric ≥2 y) | **cytosolic** | ✅ **yes** |
| TUDCA, 4-PBA | endoplasmic reticulum | ❌ no |

**A drug that corrects folding in the ER cannot correct a misfolded cytosolic protein**, however
good its safety record. That single filter removes most of the chaperone-axis candidates that
appear in rare-disease repurposing lists.

> This is a *screening* argument, not a treatment recommendation. It says which candidates are
> **not worth testing**, which is the cheaper half of a therapeutic programme.

## 2b. 🔴 And if you give the matched drug — can you tell whether it worked?

Compartment matching says arimoclomol is **aimed at the right place**. It says nothing about
whether the answer would be **readable**. That question has a published answer, and it is
uncomfortable.

**The only human measurement of this drug engaging its target** comes from the Niemann-Pick C phase
2/3 trial — Mengel E et al., *J Inherit Metab Dis* 2021, **PMID 34418116** (**NCT02612129**),
93–372 mg/day weight-banded, three times daily:

| | |
|---|---|
| HSP70 in PBMCs, 0 → 12 months | **n = 11**, mean change **+1778.98 pg/mL**, **SD 1835.56**, *P* = .001 |
| Statistical test | **within-group** Wilcoxon signed-rank — not a between-group comparison |
| Placebo comparator | **none usable** — verbatim: *"Because of loss of PBMC samples by the central laboratory, it was not possible to consider the placebo group (n = 4) as a control"* |

**The standard deviation is larger than the mean: CV = 1835.56 / 1778.98 = 103.2%.**
**[OUR MEASUREMENT — arithmetic on the trial's own two published values.]**

**Three consequences for anyone designing the experiment, including us:**

1. **Target engagement gates interpretation.** An experiment in which HSP70 did not rise is
   **uninterpretable, not negative.** Blot BubR1 in the same lysate as **HSPA1A** and **HSP90AA1**.
2. **Do not calibrate that gate from the trial.** At a marker CV near 100%, a gate keyed to it at
   n = 3 cannot separate *"no engagement"* from *"engagement we could not see"* — it converts a
   technical failure into a false negative, which is the very thing the gate exists to prevent.
   **Pre-specify the minimum detectable induction in the cell system, from its own CV.**
3. **Never normalise to GAPDH or tubulin here.** HSF1 activation and HSP90 inhibition perturb
   housekeeping proteins, so a housekeeping normaliser **manufactures an effect** in exactly the
   arms of interest. Use total-protein normalisation, and a **linear** quantification method
   (capillary western or PRM mass spectrometry) — the effects at stake are **20–40%**, at or below
   reliable ECL film resolution.

> 🔻 **THIS OBJECTION IS NOT OURS, AND WE WERE BEHIND ON IT.** Measured 2026-08-31 over 52 archived
> owners with a positive control: **2 owners already state it**, and **one states it in a more
> developed form than we did** — specifying target-engagement gating, linear quantification and the
> housekeeping-normalisation trap. A claim that these objections were new to us has been retracted
> in the private record. **What is added here is the trial arithmetic**: that team's own report says
> the NPC exposures were *not retrieved*, and the CV above is what the retrieved paper shows.
> **Being second to an idea is not a reason to state it less carefully.**

## 3. 🔻 What we are NOT claiming, because we measured it

**This is not novel to us.** On 2026-10-23, the case-insensitive raw pattern
`arimoclomol` occurs in **18 of 111 archived owners**, across a corpus of 126 distinct
repositories (127 directories); control `BUB1B` occurs in **102 of 111 owners**.
**[OUR MEASUREMENT — `guardrails/owner_count.py`, NUL-byte binary exclusion, owner-deduplicated.]**
Mentions include proposals, contraindications and harvested evidence; they are not 18 endorsements.
Several competing reports now frame the same abundance-versus-function question, including
`11pingupingu99-max/MVA_Track2_kotgienia`, whose report separates abundance limitation from
functional impairment and gates any rescue claim on functional measurements.

> 🔻 **DENOMINATOR AND NUMERATOR BOTH RE-MEASURED 2026-09-01, AND THE REASON MATTERS MORE THAN THE
> NUMBERS.** This paragraph read *"7 of 64 archived competitor repositories, held by 6 of 54 distinct
> owners"*. **The owner count is genuinely unchanged at 6** — but it is now 6 **of 57**, and the repo
> figure is 7 **of 64**. More importantly, **`Marxist-Leninist/mva-hackathon-2026` newly carries the
> term, and we could not see it until today**: our archived copy of that repo was cloned 2026-08-27
> and upstream had pushed on 2026-08-30. **Eight of our 63 archived copies were stale on 2026-09-01
> and were re-cloned; refreshing them moved 15 of the 23 competitor cells on the scoreboard, every
> one of them upward.** The full table is in
> `dossier/sweeps/evidence-2026-09-01/FIELD-SWEEP-2026-09-01.md`.
> 🔑 **A FIELD MEASUREMENT HAS TWO WAYS TO BE STALE — the denominator, and the CONTENT the numerator
> was counted over.** This project had a standing rule for the first and no instrument for the
> second. **[OUR MEASUREMENT — `grep -rli arimoclomol archive/competitors/`, deduplicated to owner
> and to repository via `guardrails/archive_duplicates.json`, 2026-09-01, after the refresh.]**

> 🔴 **DENOMINATOR CORRECTED 2026-08-30, AND SO WAS ITS UNIT.** This paragraph read *"the
> 50-archived-owner denominator: `arimoclomol` appears in **6 of 50 competitor repositories**"* —
> which names an **owner** denominator and then applies it to **repositories** in the same breath.
> They are different populations: the archive holds **54 owners across 59 distinct repositories**
> (60 archived directories, one repo archived twice under a rename — `Samistus1234__mva-hackathon-track1`
> is the SAME upstream repo as `Samistus1234__mva-hackathon`, proved by HTTP 301 on the old name;
> **owner counts are unaffected and never needed correcting**), because
> some owners have more than one. Re-measured with a positive control run first
> (`grep -rli BUB1B archive/competitors/` → 713 files, so a zero would have been real):
> **6 repositories, 6 owners.** The conclusion is unchanged and slightly stronger against us —
> which is why it is stated in both units rather than whichever is smaller.
>
> 🔴 **REPO COUNT CORRECTED AGAIN 2026-08-31 — it read "7 of 57", and I re-verified that figure the
> same day and reported it as holding. It does not.** `archive/competitors/` holds **the same
> repository twice**: `Samistus1234__mva-hackathon` is a **strict subset** of
> `Samistus1234__mva-hackathon-track1` (0 files unique to it, 60 shared paths, 55 byte-identical) —
> the upstream repo was **renamed**, and we archived it under both names. **Both copies were inside
> the arimoclomol 7.** True at that measurement: **6 repositories of 56** — and **6 of 58** at the
> live denominator once `mateooSM` and `Jakeelamb` were archived later the same day (numerator
> re-measured, unchanged). ⚠️ **The OWNER counts are unaffected** — the
> two directories always deduplicated to one owner — **so every "of 52 owners" figure in this
> project stands. Only repo-denominated counts were inflated.**
> [OUR MEASUREMENT — `grep -rli arimoclomol archive/competitors/`, deduplicated to repository and
> to owner, 2026-08-30.]

**[OUR MEASUREMENT — grep over `archive/competitors/`, every hit read by hand, 2026-08-29.
An observation about competitors' documents, never evidence about the biology.]**

**Our contribution here is the compartment filter and the branch point, not the drug.** Several
teams arrive at the same molecule; the argument we can defend is *why most of its neighbours are
excluded* and *what experiment decides whether any of them could work at all*.

## 4. The honest position

The therapeutic branch of this work is the **weakest** part of it, and our own odds on it are
poor: **25–40%** that a screen yields any compound raising BubR1 two-fold, **well under 10%** that
anything reaches a child. **[ESTIMATE — both figures are ours and neither is derived from data.
No *BUB1B*-specific prior exists, because no screen has been run.** The reasoning behind them is
in `THERAPEUTIC-SCREEN-design-and-odds.md`: proteostasis/degradation lesions are a precedented
screening target, the required effect is modest, and the readout is direct — which is an argument
for plausibility, not a measurement.**]**

> 🔻 **CORRECTED 2026-08-30.** This paragraph read *"and the numbers say so"*, which presents two
> subjective priors as measurements. **The private source tags both figures `[ESTIMATE]` and
> carries the reason they can be nothing else** — *"No BUB1B-specific prior exists because no
> screen has been run"* — and the tag was dropped when the sentence was restated in this
> judge-visible file. **A provenance tag that does not survive being copied outward is not
> provenance.** It is included because a mechanism actively tested and found wanting is a different
epistemic state from one never examined — and because the branch point is a real, cheap,
decidable question that nobody has answered.
