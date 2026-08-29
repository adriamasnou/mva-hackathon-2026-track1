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

**It does not improve the odds.** Those remain **25–40%** for a usable hit and **well under 10%**
for anything a child could take. **An airtight protocol for a long-odds experiment is still a
long-odds experiment.**

## 1. The question the screen asks

Does any approved drug **raise the amount of BubR1** in patient cells? The thesis is that the
lesion is one of protein *abundance*, not of catalytic activity — so the screen measures amount,
and function is confirmed separately.

## 2. ★ The design decision everything else follows from

The published functional readout is **the MPM-2⁺ fraction of the 4N population after 16 h
nocodazole, by flow cytometry** (Suijkerbuijk 2010). That is the right *confirmatory* assay and the
wrong *primary* one — it is slow, and it measures the consequence rather than the thing the thesis
is about.

> **Primary screen: BubR1 ABUNDANCE, by intracellular antibody stain, read on a
> high-throughput flow cytometer in 384-well format.
> Secondary confirmation: the published MPM-2 / 4N functional assay, on hits only.**

Cheap primary, expensive orthogonal secondary — standard screening architecture, and here it is
also forced by the biology: **the patient line is a lymphoblastoid line, i.e. suspension cells.**
Suspension makes high-content imaging awkward and makes flow the natural platform, so the
throughput objection to a flow readout dissolves at 384-well.

## 3. Cells — real catalogue numbers

| line | type | genotype | role |
|---|---|---|---|
| **GM21284** | LCL | *BUB1B* `4-bp ins 2211GTTA` / `R814H` | **the screen line** |
| GM21657 · GM22004 | LCL | unaffected parents (families 2680 / 2741) | normal-abundance reference |
| GM21654 · GM21655 | LCL | *CEP57* patients | specificity control — a different MVA gene |

**~$262 US-academic / $448 international each, MTA required** (NIGMS Human Genetic Cell Repository).

🔴 **Limitation, stated up front: `GM21284` has no matched parent in the repository.** The
unaffected LCLs above are from *other families and a different gene*, so they are population
references, not matched controls. **[VERIFIED from the repository's own records; the trio structure
of families 2680 and 2741 does not extend to the *BUB1B* donor.]**
⚠️ And `GM21284` is **not this child's genotype** — no N1002K line exists, which is what the
accompanying reagent specification addresses.

## 4. Assay validation — to the Assay Guidance Manual, with its numbers

**[NIH/NCATS Assay Guidance Manual — these thresholds are the AGM's, quoted, not invented here.]**

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
- **Maximum signal** = patient cells + a **proteasome inhibitor** (e.g. MG132). Blocking degradation
  **must** raise BubR1 if the readout works at all.
- ⚠️ **The positive control is an assay control, not a hit mimic.** A proteasome inhibitor raises
  everything and is toxic. It defines the assay window; it is not a candidate, and a compound that
  merely reproduces its profile is a counter-screen failure, not a hit.

**Gate: no compound plate is read until Z′ ≥ 0.4 on validation plates.** Cited in advance so it
cannot be relaxed after seeing data.

## 5. Library — named, and filtered for a reason

| library | size | note |
|---|---|---|
| **Prestwick Chemical Library** | **~1,520** | ~all off-patent approved drugs — **recommended primary** |
| NCATS Pharmaceutical Collection | ~2,750 | approved/investigational, NIH |
| Broad Drug Repurposing Hub | ~6,800 | broadest, richly annotated |

**1,520 compounds in 384-well = 4 assay plates.** That is the reason to start with Prestwick: the
whole primary screen is a handful of plates, not a campaign.

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
| confirmation | **10-point dose–response, 3-fold dilutions from 30 µM, in triplicate** |
| criterion for a real hit | **≥ 2-fold increase in BubR1 abundance**, dose-dependent, reproduced on a separate day |

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

## 8. Cost and duration

| item | estimate |
|---|---|
| cell lines (4 × ~$262–448) | **$1,050–1,800** |
| Prestwick library access (facility-dependent) | **[VARIES — often already held by the facility]** |
| 384-well plates, antibodies, staining reagents, ~6 plates + validation | **$2,000–5,000** |
| high-throughput flow time | **[NOT ESTIMATED — facility rate]** |
| **elapsed time, validation → confirmed hits** | **[ESTIMATE] 3–5 months** |

**[OUR ESTIMATE. Cell-line prices are `[VERIFIED]` from the repository. Everything else is a range
for scoping, not a quote — and labour is not included, not because it is small but because
inventing it would be worse than admitting it.]**

## 9. Adversarial review — of THIS document

The previous adversarial pass in this project reviewed the *stability protocol*, not the screen.
Three attacks on this one:

**A1 — "The primary readout does not measure what you care about."** Partly lands. Abundance is a
proxy for function; a compound could raise a non-functional pool. **Mitigated but not removed** by
the MPM-2 secondary. **A hit that raises abundance without restoring function is a real possible
outcome and would not be a treatment.**

**A2 — "GM21284 is the wrong genotype."** Lands fully. It is `753X/R814H`, not N1002K, so a hit
found here **may not transfer to this child** — the odds table already scores that transfer as
`unknown`. The screen is a **class** experiment, not a personal one, and should be described that
way.

**A3 — "A proteasome inhibitor positive control guarantees a Z′ you cannot achieve with a real
hit."** Lands, and it is the sharpest. The assay window is defined by a maximal, toxic
intervention; genuine hits will sit far below it. **Z′ ≥ 0.4 against that control does not
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
| Alexa-conjugated secondaries | Jackson ImmunoResearch, 711-545-152 etc. | ✅ catalogued |

> ### The risk, stated plainly
> **BubR1 HAS been read by FACS** — Janssen 2009 lists it among antibodies used for "Western blot,
> Immunofluorescence, and FACS analysis", so the readout is not unprecedented. **But that antibody
> was "a gift from R. Freire" — not a commercial reagent.** The commercial candidate above is
> evidenced in our holdings only for immunofluorescence.
>
> **So the most important reagent in this screen is unvalidated for the application it is being
> asked to perform.** That is a real risk to the primary readout, not a formality.
>
> **Therefore the first bench task is not the screen. It is: does A300-386A give a specific,
> quantitative intracellular BubR1 signal by flow in LCLs, with a window between patient and
> control cells?** If it does not, the primary readout must change — most likely to a tagged
> reporter line — and that is a different, larger project. **This gate comes before the Z′ gate.**

⚠️ **A discrepancy a lab must not inherit.** Our holdings contain one passage using **A300-386A to
detect BUB1** and another specifying **BUB1 = A300-373A, BUBR1 = A300-386A**. Those cannot both be
right. **Confirm the catalogue number against the vendor's own datasheet before ordering** — BUB1
and BUBR1 are different proteins and the wrong tube produces a confidently meaningless screen.
**[OUR MEASUREMENT — both passages are in papers held in `papers-local/`; the inconsistency is in
the published text, not introduced here.]**

## 11. How this document compares to the stability protocol, measured

Asked directly whether this is as precise as the accompanying stability protocol: **it is not, and
the gap is measurable.**

| | stability protocol | this document |
|---|---|---|
| catalogue numbers | 28 | 8 → **12** |
| **published expected values / calibration anchors** | **71** | **0** |
| derived statistics | 41 | 2 |

**The zero is the honest headline.** Every construct in the stability protocol carries a *published
expected result*, so a lab knows on day one whether the assay works. **This screen has no such
anchor for its primary readout, because no drug-induced BubR1-abundance measurement has ever been
published** — that is the same absence that makes §0's odds estimates rather than measurements.

**Consequently the ≥2-fold hit criterion in §6 is asserted, not derived.** The stability protocol
tabulated its minimum detectable ΔTm across the unknown standard deviation. The equivalent cannot
be done here until the pilot in §10 produces a signal window. **It is a placeholder with a number
on it, and it should be replaced by a derived threshold once the pilot exists.**

**What that means practically: the stability protocol can be sent to a laboratory. This one can be
sent to a laboratory for a pilot.** They are not at the same readiness and should not be presented
as though they were.

## 12. What still needs a person

- 🔴 **A screening facility.** Nothing here can be ordered by us.
- MTAs for the cell lines; library access is facility-dependent.
- **The paediatric filter list** should be reviewed by someone with paediatric pharmacology
  expertise before it is applied — filtering wrongly is as harmful as not filtering.
- **A2 above is a scoping decision**, not a technical one: is this a screen for *this child*, or for
  *BUB1B*-MVA as a class? **The honest answer is the class, and the document should not be allowed
  to drift into implying otherwise.**
