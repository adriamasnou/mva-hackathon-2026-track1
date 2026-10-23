# Functional rescue plan: full-length N1002K and exposure-limited arimoclomol

**Proposed experiments; not performed. Protocol revision: 23 October 2026.**

This is the decision protocol for the [Track 2 candidate](adriamasnou_track2_report.md). The fragment reagent specification remains an optional mechanistic sub-study. Neither a fragment melting curve nor increased BubR1 alone is sufficient to advance a drug.

## Primary question

Does arimoclomol reduce chromosome-segregation errors per completed division in an N1002K replacement system at a measured exposure compatible with the human pharmacokinetic anchor, without doing so through reduced division, cell death or selection? **[PROPOSED EXPERIMENT]**

## Stage 1: qualify the genotype model

Use a laboratory-validated full-length BUB1B replacement system with the same backbone, promoter, tag placement and endogenous depletion strategy across WT, N1002K and controls. Confirm sequence, expression and depletion; test the tag's effect with an orthogonal untagged or endogenous readout. Use a published destabilising MVA allele as a mechanistic control, selected against the primary paper's specific phenotype. Empty/depleted and WT-rescue controls establish dynamic range. Cells must be authenticated and mycoplasma-negative. A transformed-cell result needs confirmation in a relevant non-transformed or patient-derived system before translation. PMID 20516114. **[PROPOSED EXPERIMENT]**

Measure BUB1B transcript, full-length protein, turnover and kinetochore localisation. Quantify protein within a validated linear range and test normaliser stability. Compare N1002K both with ordinary WT rescue and with WT titrated to matched abundance. Define an acceptable matching tolerance from pilot assay precision before unblinding functional results; if the ranges do not overlap, the function-at-matched-abundance comparison is indeterminate. **[PROPOSED EXPERIMENT]**

Assignment is descriptive: low abundance with retained function when matched; reduced function despite matched abundance; both; or indeterminate. Do not use Q921H's normal abundance as proof of a specific PP2A defect, and do not infer N1002K behaviour from domain membership. PMID 20516114; PMID 33207204. **[OUR INFERENCE]**

## Stage 2: exposure and response qualification

Proposed concentration series: vehicle, 0.2, 0.6, 1 and 2 µM arimoclomol; exploratory 4 and 10 µM reported separately. Sample multiple prespecified times, initially 6, 24 and 48 hours, to distinguish transient stress-response induction from sustained rescue. Those times and concentrations are design choices, not validated optima or human dosing instructions. Start with single-agent treatment; combinations require a separate hypothesis and control structure. **[PROPOSED EXPERIMENT]**

The label gives estimated paediatric NPC serum trough/peak means equivalent to approximately 0.66/1.67 µM, not free intracellular concentrations. Measure medium stability and cellular exposure where possible and record protein content/binding. Use a pharmacology review before calling any tested concentration clinically reachable. Even 2 µM is a screening bracket, not a proven sustained therapeutic exposure. [MIPLYFFA label](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5feffc0e-453d-47fa-91dd-38d4952309bc); [calculation](../analysis/exposure_check.py).

Assay HSPA1A with BubR1 and a justified additional pathway readout. Include an independently qualified stress-response positive control on separate wells. A heat-shock control demonstrates assay capability; it must not be used to claim efficacy of the candidate under ordinary disease conditions. Cell type and initiating stress affect arimoclomol response. PMID 31900865. **[PROPOSED EXPERIMENT]**

If controls pass and exposure is confirmed but the drug does not engage the proposed response, this is a negative result for that mechanism in that system. If measurement controls fail, it is indeterminate. HSP70 response alone neither proves direct target binding nor establishes rescue of BubR1 function. **[OUR INFERENCE]**

## Stage 3: prespecified outcomes and analysis

**Primary outcome:** fraction of completed divisions with a prespecified segregation error, scored from blinded time-lapse imaging. Define lagging chromosomes, bridges and multipolar divisions in an image-scoring manual before analysis. Track cells from entry through exit, death or arrest so exclusions cannot remove failed divisions. **[PROPOSED EXPERIMENT]**

**Required secondary outcomes:** chromosome alignment, checkpoint response and mitotic duration; full-length BubR1 abundance/localisation; viability, apoptosis, division rate and cell-cycle distribution. A fall in micronuclei without a matched division/fate analysis is insufficient, because survival and proliferation can change the observed fraction. **[PROPOSED EXPERIMENT]**

Independent culture preparations are biological replicates. Cells and fields are nested observations, not independent n. Randomize treatments across plates and positions; blind imaging/scoring; record every excluded well and its prespecified technical reason. Use a hierarchical model or replicate-level estimates appropriate to the event counts. Correct for the planned concentration comparisons and report effect sizes with confidence intervals, not only p-values. **[PROPOSED EXPERIMENT]**

A separate pilot estimates baseline error, overdispersion, usable divisions per culture and assay CV. Freeze a power calculation and confirmatory sample size before evaluating the candidate's confirmatory response. Three convenient wells do not establish adequate power. Do not derive cellular assay precision from interpatient PBMC variability in the NPC trial (PMID 34418116).

Before confirmation, the laboratory must register the smallest worthwhile reduction in segregation errors and acceptable proliferation/viability bounds. These are programme decisions to be justified by the pilot, not a claimed clinical benefit threshold. The protocol is therefore **ready for laboratory design review, not fully preregistered or executable without that review**. The computational work cannot honestly supply missing pilot variance or clinical thresholds.

## Advancement rules

1. Advance only with reproducible functional benefit at qualified exposure, accompanied by a coherent protein/response readout and without cytostasis or selective killing explaining the result.
2. Protein-only improvement fails the efficacy gate. A high-dose-only effect fails the current translational gate.
3. An informative drug negative does not prove the target class impossible. A failed control cannot support a biological negative.
4. Replicate the positive result in an independent experiment and a relevant genotype model; require specialist clinical and oncology review before considering human investigation.
5. Publish every outcome category and its denominator, including inconclusive assays and failed concentrations. No patient treatment is proposed within this competition. **[OUR INFERENCE; PROPOSED EXPERIMENT]**

## Resources and limits

The fragment sequence/primer package is supplied separately. Its historical list-price materials estimate excludes full-length replacement-system development, cell culture, assay qualification, quantitative exposure work, labour and independent validation. A current laboratory quote is required; the full programme has no established cost or completion date. No external laboratory, patient-cell access or clinical collaborator is claimed. **[ESTIMATE; PROPOSED EXPERIMENT]**
