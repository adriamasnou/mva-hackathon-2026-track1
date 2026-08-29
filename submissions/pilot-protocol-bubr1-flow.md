# Pilot: can BubR1 abundance be measured by intracellular flow cytometry?

**The gate that comes before the screen. No anti-BUBR1 antibody is validated for this application
by any vendor, and no published precedent exists — so this is not a formality, and it has a
pre-declared failure condition with an action attached.**

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · 2026-08-29 · CC BY 4.0*

---

## 1. The question, and why it cannot be assumed

The repurposing screen's primary readout is **BubR1 protein abundance, by intracellular antibody
stain, read on a flow cytometer.** Establishing that this works is a prerequisite, because:

- **Neither candidate antibody is vendor-validated for flow cytometry.** `A300-386A` is validated
  for western blot and immunoprecipitation only; `BD 612502` for WB, IF, ELISA, ICC and IP.
- **No published precedent exists.** Of 39 papers citing `A300-386A`, six also mention flow — and
  in every case the antibody is in a *western-blot* list while the flow is doing something
  unrelated. Co-occurrence, not usage.

**A screen built on an unvalidated readout is not a screen.**

## 2. ★ The calibration anchor — a published expected value

The screen protocol had **no published expected value for its primary readout**, which was its main
weakness against the companion stability protocol. **This pilot has one.**

> **Matsuura *et al.* 2006 (PMID 16411201) measured BubR1 in three MVA patients at
> 22%, 25% and 29%** of the reference level.

**A working assay must reproduce roughly that.** If patient cells read at 80% of control, the assay
is not measuring BubR1 specifically. If they read at 3%, something else is wrong. **The pilot has a
number to hit, not merely a signal to observe.**

⚠️ **Two honest limits on the anchor.** Matsuura's figures are **% of HeLa**, a different cell type
from the lymphoblastoid lines used here, and **those patients are not this repository's donor**.
Treat 22–29% as an expected *range and direction*, not a target to be matched to the digit.

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
| isotype control | any | **mouse IgG2a**, matched concentration |
| secondary | Jackson ImmunoResearch | anti-mouse Alexa 488 — **715-545-150** |
| **patient cells** | NIGMS/Coriell | **GM21284** (LCL, *BUB1B* `753X`/`R814H`) |
| **control cells** | NIGMS/Coriell | **GM21657**, **GM22004** (unaffected parent LCLs) |
| positive control (raises BubR1) | Calbiochem | **MG132**, CAS **133407-82-6** |
| **specificity control** | Foley 2011 | **dsiBUBR1 5'-GUCUCACAGAUUGCUGCCUCAGAGC-3'** |
| mitotic arrest (optional arm) | Sigma | nocodazole **M1404-10MG** |

Cell lines ~**$262 US-academic / $448 international** each, MTA required.

## 5. Method — bench level

### 5.0 Culture

LCLs are EBV-transformed suspension B-cell lines. **RPMI-1640 + 15% FBS + 2 mM L-glutamine, 37 °C,
5% CO₂**, maintained between **3 × 10⁵ and 1 × 10⁶ cells/mL**; do not let them exceed 1 × 10⁶ or
they exit log phase and protein levels drift.
⚠️ **Take the definitive culture conditions from each line's own repository datasheet** — they are
line-specific and are published per catalogue number. Expand for **≥ 2 passages after thaw** before
any measurement; freshly thawed LCLs are not in steady state.

### 5.1 🔴 STEP ONE: antibody titration. This is not optional.

The antibody is **not validated for flow**, so **no dilution can be assumed** — the IF and WB
dilutions on the datasheet are for other applications and other fixation chemistries.

**Titrate before anything else:** 1:50 · 1:100 · 1:200 · 1:400 · 1:800, on control LCLs, stained
alongside a matched isotype at each concentration.
**Choose the dilution maximising the *stain index*:**

```
stain index = (median_stained - median_isotype) / (2 × robust SD_isotype)
```

**Not the dilution giving the brightest signal** — the brightest is usually not the most separated,
and picking on raw brightness is the standard way to enter a screen with a poor window.

### 5.2 Fix and permeabilise

Two conditions, **run in parallel on the first plate**, because BubR1 is nuclear/kinetochore-
associated and detergent versus alcohol permeabilisation are not interchangeable for such epitopes:

| | **Condition A** (published for BUBR1 staining) | **Condition B** (alcohol) |
|---|---|---|
| fix | **4% formaldehyde + 1% Triton X-100 in PBS, 20 min, RT** | 4% formaldehyde in PBS, **10 min, RT** |
| permeabilise | (simultaneous, above) | **ice-cold 90% methanol, 30 min, −20 °C** |
| wash | 2 × 200 µL PBS + 0.1% Triton | 2 × 200 µL PBS |

**Testing both once costs one day. Discovering the wrong one after the screen costs the screen.**

### 5.3 Staining — per well, 96-well V-bottom

1. **5 × 10⁵ cells** per well. Pellet **300 × g, 5 min**, discard supernatant.
2. Fix/permeabilise per §5.2. Pellet, wash twice.
3. **Block: 50 µL TBS + 0.1% Triton X-100 + 2% BSA, 30 min, RT.**
4. **Primary: 50 µL at the titrated dilution in block buffer, 1 h RT** (or overnight 4 °C — pick one
   and hold it constant; **do not mix incubation regimes across plates**).
5. Wash **2 × 200 µL** block buffer.
6. **Secondary: anti-mouse Alexa 488, 50 µL at 1:500 in block buffer, 30 min RT, protected from light.**
7. Wash 2 × 200 µL. **Resuspend in 200 µL PBS + 1% BSA.** Acquire same day.

### 5.4 🔴 Gating strategy — stated explicitly, because a flow assay without one is not defined

1. **FSC-A vs SSC-A** → the intact lymphoblast population, excluding debris at low FSC.
2. **FSC-H vs FSC-A** → **singlets.** Doublets carry double the signal and will otherwise widen the
   CV — which is the exact quantity this pilot must minimise.
3. **Viability dye vs FSC-A** → live cells only. Dead cells bind antibody non-specifically and
   inflate both signal and variance.
4. **BubR1 (Alexa 488) histogram** on the live-singlet gate.
5. **Report the MEDIAN fluorescence intensity of that gate**, not the mean — flow distributions are
   right-skewed and the mean is unstable to outliers.

**Collect ≥ 10,000 live singlet events per well.** Keep voltages, gates and compensation **identical
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

`dsiBUBR1 5'-GUCUCACAGAUUGCUGCCUCAGAGC-3'` (Foley 2011) is the right reagent, **but LCLs are
EBV-transformed B cells and are notoriously refractory to lipid transfection.** Assuming a
lipofection will work here is the kind of assumption that costs a month.

> **Therefore: run the knockdown specificity arm in an easily transfected adherent line
> (HeLa or U2OS), not in the LCLs.** Specificity is a property of the *antibody*, not of the cell
> line, so it transfers. **The anchor comparison (§ arms 3–4) stays in the LCL pair, where the
> published 22–29% expectation applies.**
> If a knockdown in LCLs is wanted regardless, it requires **nucleofection**, not lipofection, and
> the efficiency must be measured rather than assumed.

### 5.7 How the CV is computed, so criterion 4 is unambiguous

**CV = SD / mean of the per-well MEDIAN fluorescence intensities**, across the **n ≥ 6 replicate
wells of one arm on one plate** — *not* the CV of events within a well, which is a different and
much larger number that would fail the criterion for the wrong reason.
Report it **separately for each arm**, and **for arm 3 (patient baseline) it must meet §3's ≤ 6.7%**,
because that is the population the screen actually measures against.

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
