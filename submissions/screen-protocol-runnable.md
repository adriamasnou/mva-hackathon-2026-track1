# Optional LCL abundance screen — conditional execution specification

**Proposed; not performed. Revised 24 October 2026.** This document replaces the historical “runnable” screen's contradictory control, library, throughput and budget fields. The programme prioritizes the [full-length functional-rescue study](functional-rescue-plan.md). Broad screening is a separately quoted, separately gated optional branch and cannot establish N1002K rescue from an abundance hit. [Execution readiness](laboratory-execution-readiness.md).

## Entry gate and models

Do not purchase/execute a library screen until the [flow pilot](pilot-protocol-bubr1-flow.md) passes specificity, linearity, repeatability, recovery, day/lot and cell-fate criteria and the laboratory accepts the throughput/cost scope. Use qualified GM21284 and population-reference GM12878/GM18502. GM21284 is catalogued S738fsX753/R814H, not N1002K. Do not label GM21657/GM22004 molecular carriers without genotype evidence; CEP57 lines are disease-context comparators, not BubR1 antibody specificity controls. [Coriell GM21284](https://catalog.coriell.org/0/Sections/Search/Sample_Detail.aspx?Product=CC&Ref=GM21284); checked 24 October 2026.

Use the frozen 8G1 IgG1κ/detection/viability/DNA panel from the pilot, not the legacy BD IgG2a panel. No same-host dual stain is interpreted as separate BubR1 and unrelated protein signals. Antibody application listings and monoclonality do not remove the need for actual specificity, precision and lot qualification. **[OUR INFERENCE; PROPOSED EXPERIMENT]**

## Library, layout and dose

The official [Prestwick 1760 catalogue](https://www.prestwickchemical.com/prestwick-chemical-library-1760-drugs-mainly-fda-approved/), retrieved 24 October 2026, lists 1,760 compounds and 98% marketed content, 10 mM DMSO solutions and 96/384-well options. Approval annotation remains compound-specific; neither the library label nor prior approval establishes pediatric MVA safety. The library is quote-only here; no facility-owned access is assumed.

At 320 compound slots/384-well plate, ceil(1760/320) = **six plates**. The [capacity layout](../examples/laboratory-readiness/hts-1760-layout.json) has 1,760 compound wells, 384 fixed control wells and 160 additional vehicle wells. It uses columns 1, 2, 23, 24 for controls. It **does not exclude the full perimeter**: rows A/P contain samples and need position/evaporation qualification. The sixth plate has 160 compounds and 160 extra vehicles. Replace placeholder compound IDs with the delivered barcode/CAS/concentration map and validate it before dosing. **[PROPOSED EXPERIMENT; ESTIMATE]**

Proposed primary conditions: 10 µM compound, 24 h, 0.1% DMSO matched vehicle if tolerated. Controls: vehicle, a qualified MG132 abundance control, a reference line and a qualified low-effect control. No suitable low-effect drug control is yet established. MG132 does not establish achievable separation for realistic functional hits. Freeze acceptance criteria and normalization using qualification data; do not choose B-score correction after seeing favourable hits. Proposed Z′ ≥ 0.4 is an engineering target requiring actual qualification. These assay settings are unverified in this system. **[PROPOSED EXPERIMENT] [UNVERIFIED]**

## Miniaturization and real throughput

Proposed starting scale 50,000 loaded cells/well, 20 µL stain, 5 µg/mL primary must be tested for viability, mixing, wash loss and enough retained events. This would load 115.2 million cells for 2,304 wells and consume 230.4 µg primary, 276.48 µg with 20% handling. Retaining the old 500,000 cell scale requires **1.152 billion cells** before loss. Miniaturization is not an assumed saving. Expansion medium, labour and banking are extra. **[PROPOSED EXPERIMENT; ESTIMATE]**

At 25,000 events/well the screen requires 57.6 million events. At 1,000 events/s that is 16 hours of event collection alone; a 60 second total sample cycle implies 38.4 hours. Neither rate has been demonstrated here. The facility must measure compatible 384-well loader/washer recovery, carryover, aggregation, fluorescence QC and per-well overhead before committing instrument/staff hours. 50,000 loaded cells do not guarantee 25,000 retained events. Record actual throughput and revise quantities/cost before release. **[ESTIMATE; PROPOSED EXPERIMENT]**

## Hits, resupply and biological interpretation

Predefine normalization, exclusion and a provisional abundance-hit rule after the pilot establishes background and variance. ≥ 3 SD above vehicle or ≥ 2-fold signal are possible engineering criteria, not therapeutic thresholds. Record all plates/wells and failed QC; do not discard toxic concentrations to improve the hit rate. Include compound autofluorescence and detection-chain interference controls. **[PROPOSED EXPERIMENT]**

Retest fresh compound at ten 3-fold dilutions from 30 µM on three independent days: 30 dose wells/hit, plus vehicle, reference, fluorescence/secondary-only, unrelated-protein, viability and orthogonal WB controls. Technical replicate wells are not independent days. Each qualified hit then needs the common full-length segregation/division/fate framework. An increase in BubR1 or other proteins does not by itself distinguish stabilization, cell-cycle shift, generalized stress or survivor selection. A class-level LCL result does not resolve N1002K function or clinical benefit. **[PROPOSED EXPERIMENT; OUR INFERENCE]**

Reject technical failures as uninterpretable; do not use them to falsify a mechanism. Stop advancement for cytostasis/selection, incompatible exposure, absent orthogonal confirmation or unresolved assay interference. Report all tested denominators and confidence intervals. Compound resupply and confirmation cost remain per-hit options because hit count is unknown. No speculative “25–40% usable hit” probability is used for funding or readiness. **[PROPOSED EXPERIMENT; OUR INFERENCE]**

## Resources and release

[Provider evidence](../examples/laboratory-readiness/provider-evidence.json), [quantities](../examples/laboratory-readiness/quantities.json) and [unsent RFQ-03](../examples/laboratory-readiness/quote-requests.md) separately specify library, stocks, controls, cells, antibody, plates, washing, acquisition, analysis and retests. Historical USD 2,000–5,000 estimates are not a current full budget and are withdrawn. There is no written project quote, booking or accepted lab scope; all full programme costs remain unpriced. No cash-prize commitment is made; credits apply only to eligible computation. **[ESTIMATE; PROPOSED EXPERIMENT]**
