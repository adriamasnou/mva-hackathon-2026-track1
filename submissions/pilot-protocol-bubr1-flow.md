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

## 5. Method

**Fix/permeabilise — published conditions, used for BUBR1 staining specifically:**
**4% formaldehyde + 1% Triton X-100 in PBS, 20 min at room temperature.** Block and dilute
antibody in **TBS + 0.1% Triton X-100 + 2% BSA**. These are taken from published work staining
BUB1/BUBR1, not invented here.

⚠️ **Run a second condition in parallel on the first plate: 4% formaldehyde 10 min, then ice-cold
90% methanol.** BubR1 is nuclear/kinetochore-associated, and methanol frequently outperforms
detergent for such epitopes. **Testing two conditions once costs a day; discovering the wrong one
after the screen costs the screen.**

**Cells** are suspension LCLs — no trypsinisation, no scraping; stain in tube or 96-well V-bottom.

**Arms** (each ≥ 6 replicate wells):
1. patient + isotype control
2. patient + secondary only
3. **patient + anti-BUBR1** ← baseline
4. **control LCL + anti-BUBR1** ← the anchor comparison
5. **patient + dsiBUBR1 knockdown + anti-BUBR1** ← specificity
6. **patient + MG132 + anti-BUBR1** ← positive control

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
