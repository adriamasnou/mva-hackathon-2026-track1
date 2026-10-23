# Executable functional-rescue decision rules: prototype validation

**Research software prototype; no experiments performed. Not a medical device, biological rescue result or clinically validated decision system.**

The [validator](../analysis/rescue_decision/decision.py) implements a bounded part of the [functional rescue plan](functional-rescue-plan.md): determining whether supplied, qualified functional estimates are eligible for independent research replication. It uses only Python's standard library. The [input contract and usage](../analysis/rescue_decision/README.md) distinguish laboratory qualification assertions from what software can verify.

**Result: 40/40 frozen synthetic cases matched their expected decisions; 31 focused tests passed, with no failures, errors or skips. Seven deliberately faulty in-memory versions were all detected by the frozen cases.** The [machine-readable result](rescue-decision-validation.json) contains every case, decision, reason, denominator, source hash and the focused test execution record. Tests ran on Python 3.13.14; no broader interpreter compatibility or runtime benchmark is claimed.

## What the executable checks

- For supplied multiplicity-accounted-for benefit CI [L,U], L > δ passes, U < δ rules out the programme's worthwhile benefit at that exposure, and touching or crossing δ is inconclusive. Decimal boundaries are not rounded or softened with a tolerance.
- Model, function controls, HSP-response controls, exposure measurement, and fate measurement/coverage are separate prerequisites. Missing or malformed inputs fail closed. Failed controls produce technical indeterminacy, never a biological negative.
- Division-rate, excess-death, excess-arrest and excess-censoring intervals are assessed separately; detected selection and out-of-window exposure block replication eligibility. Fate-bound touching is inconclusive under an explicitly declared conservative strict-interior convention. The programme must justify its own bounds; these are not clinical thresholds.
- Protein improvement or better normal-cell fractions among survivors cannot override function, exposure or fate. Qualified absent HSP response with positive function prompts replication and mechanism investigation; it is not automatically rejected or labelled HSP-mediated rescue.
- All declared confirmatory comparisons must be supplied and covered by the multiplicity plan. Exploratory results are reported but cannot enter the confirmatory candidate list. Every culture's starting cells, entrants, completed divisions, errors, deaths, arrests and censoring are retained; cells are not counted as biological replicates.

The strongest label, `REPLICATION_CANDIDATE`, means **eligible for independent research replication under the declared inputs**. It does not mean independently reproduced, clinically beneficial, safe for a child or ready for human investigation. Raw interval relations remain explicitly uninterpretable when a required control fails.

## Frozen cases and test strength

The [expected cases](../analysis/rescue_decision/expected-cases.json) and [hash receipt](../analysis/rescue_decision/expected-cases.freeze.json) were written before the evaluator existed or ran. A documented preimplementation refinement added separate fate qualification and three cases, producing the frozen set of 40. No expectations were changed to fit observed outputs. The same developer wrote expectations and code: this is execution-independent specification, **not independent human validation or external preregistration**.

The fixtures cover adequate functional signals, abundance rise with benefit ruled out, cytostasis, selective killing, missing measurements, nonfinite values, exact CI boundaries, unqualified controls, failed exposure, missing family members and invalid replicate accounting. The focused tests additionally delete every required key, inject invalid values into numeric fields, check denominator consistency and family ordering, and show that increasing protein/survivor markers cannot overturn blocked decisions.

The seven deliberate faults alter threshold equality, bypass fate measurement, bypass exposure, ignore harmful fate bounds, incorrectly reject qualified HSP-negative functional signals, or force efficacy to pass. All seven caused disagreements with the frozen expected decisions. This checks specific failure modes; it does not establish exhaustive mutation coverage or absence of software defects.

## Comparison with incomplete decision rules

Across **29 contrasts in structurally valid fixtures**, five are expected replication candidates. The validator returns those five. A naive protein-ratio > 1 rule accepts 28 contrasts: 24 acceptances violate the frozen programme rules and one expected candidate is missed. A naive positive-survivor-fraction rule has the same aggregate counts, with a different missed candidate. Cytostasis and selective killing illustrate why separate functional and fate checks matter. The JSON also reports all-input counts separately, including 13 malformed-input cases.

These are deliberately incomplete illustrative rules, **not implementations of named competitors' proposals**. Fixtures intentionally overrepresent failures and boundaries. The counts are not estimates of sensitivity, specificity, biological false-positive rates, clinical benefit or competitive superiority.

## Reproduce and interpret the limits

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_rescue_decision.py -v
PYTHONDONTWRITEBYTECODE=1 python3 analysis/rescue_decision/validate_cases.py
```

The second command prints a fresh JSON record and runs only these focused tests and deliberate-fault checks. Shared project gates, public-case benchmarks and runtime studies are outside this validation.

Fixture CIs are supplied synthetic inputs, not fitted to the illustrative counts; the three example cultures do not establish statistical power. No clinical threshold is supplied by this software. Measured pilot variance, overdispersion and usable divisions per culture remain unavailable.

A separate [frozen simulation sidecar](../analysis/rescue_decision/simulation/README.md) now fits culture-level Welch intervals under declared beta-binomial assumptions. All 720,000 experiments were rerun with exactly matching scientific outputs. This tests only the efficacy interval rule, assuming every exposure, fate and assay gate passes; it does not calibrate this complete prototype. In one illustrative boundary scenario (six cultures per arm, ICC .05, four true benefits equal to the .05 threshold), family false advancement was 1,387/20,000 (6.935%) with unadjusted intervals and 365/20,000 (1.825%) with Bonferroni-four intervals. Wider intervals also reduced detection. All 36 cells, denominators, coverage, Monte Carlo intervals, seeds, code and a runtime-attribution erratum are retained. These model-conditional frequencies are neither laboratory sample-size advice nor biological validation. **[OUR MEASUREMENT — synthetic model]**

The prototype cannot authenticate qualification records, actual preregistration, independent culture identity, exposure review, selection exclusion, CI coverage or the completeness of an honestly declared experiment family. It neither fits hierarchical models nor computes multiplicity adjustments. Only the first completed division per starting cell is supported. Stage 1 abundance equivalence, N1002K defect classification, actual arimoclomol rescue and independent replication remain laboratory questions. This deliverable establishes executable protocol discipline and tested software behaviour, not biological efficacy or an unequivocal comparative lead.
