# Synthetic efficacy-gate sidecar

This is a declared statistical model, not N1002K biology, clinical calibration,
calibration of the full rescue prototype, or sample-size advice. Every exposure,
fate, selection and assay gate is **assumed passed**. No patient inputs are used.

`plan.json` freezes 36 grid cells: 6/8/12 cultures per arm, ICC 0/.05/.15,
four truth scenarios, 150 completed first divisions per culture, and 20,000
experiments per cell. Four comparisons share one control arm. The estimator
uses culture-level variance and Welch t degrees of freedom. It compares
unadjusted 95% intervals with Bonferroni-four intervals targeting two-sided
95% family confidence. Welch coverage is approximate and is measured here.

Candidate means the **lower** bound is strictly greater than the illustrative
.05 reduction threshold. Reject means the **upper** bound is strictly lower.
Touching/crossing is inconclusive. Zero total variance is indeterminate; one
constant arm with positive total variance is retained and counted separately.
No clipping, rounded degrees of freedom, or outcome-driven tuning is used.

All grid cells and raw Monte Carlo event counts are retained in `results.json`.
Wilson intervals quantify only Monte Carlo error under these assumptions, are
pointwise across the grid, and use experiments rather than correlated contrasts
as independent trials. Coverage is reported both over all experiments (invalid
means not covering) and conditional on validity. Events with no eligible true
contrasts are marked inapplicable. Below-threshold positive benefits and
above-threshold benefits have separately labeled detection summaries.

Only experiment zero in each cell is retained as an individual example, with
four contrasts and both CI methods: 288 intervals selected before execution.
Each is reconstructed from culture counts and checked against the source-hashed
existing `decision.relation`. This does not invoke the complete decision engine.

## Reproduction

Use the existing **system** Python 3.13.14, NumPy 2.4.6, SciPy 1.18.0. The
parent assistant selected this runtime within the human-authorized project and
subagent work after finding no SciPy in bundled artifact Python. The frozen plan
and frozen README incorrectly attribute the exact runtime choice to the human;
see the [dated provenance erratum](PROVENANCE-ERRATUM-2026-10-24.md). Their original
bytes and all seeds/results are preserved; this current README is corrected.
No dependency installation or global configuration change is needed. The exact
executed command, runtime versions, times, plan hash, source hashes and per-cell
seed derivation are recorded. The distribution quantiles use `scipy.stats.t.ppf`.

From the repository root (`repo/`), the original pre-simulation freeze command is:

```sh
PYTHONDONTWRITEBYTECODE=1 /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 analysis/rescue_decision/simulation/freeze.py
```

That command refuses to replace the freeze. **Do not regenerate the plan for
reproduction**, since the existing plan hash participates in the seeds. Execute
the frozen source against the existing plan, with a new output filename:

```sh
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 analysis/rescue_decision/simulation/frozen-source/simulate.py --folder analysis/rescue_decision/simulation --out analysis/rescue_decision/simulation/reproduced-results.json
PYTHONDONTWRITEBYTECODE=1 python3 -S analysis/rescue_decision/simulation/frozen-source/verify.py --folder analysis/rescue_decision/simulation --results analysis/rescue_decision/simulation/results.json --compare analysis/rescue_decision/simulation/reproduced-results.json
```

The verifier checks every hash, seed, event denominator, category partition,
Wilson interval, selected example classification and paired interval ordering.
With `--compare` it checks all grid-cell scientific outputs exactly, excluding
timestamps and elapsed time. It cannot rederive unretained individual arrays
without the full seeded rerun. It also hashes the finished result file.

Tests do not simulate experiments:

```sh
# Root tests remain standard-library-only, with site packages disabled; no skips.
PYTHONDONTWRITEBYTECODE=1 python3 -S -m unittest discover -s tests -p test_rescue_simulation.py -v
# Optional scientific runtime tests are a separate suite; no root imports.
PYTHONDONTWRITEBYTECODE=1 /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m unittest discover -s analysis/rescue_decision/simulation -p test_numeric.py -v
```

The constant-arm SciPy reference fixture may emit its expected precision-loss
warning; the independent culture-variance calculation and both-zero-variance
handling are explicitly tested. No custom t-distribution inversion is retained.

Parameters are illustrative, and equal completed-division denominators are
fixed. There are no donor, plate, batch, lineage, temporal, attrition, arrest,
death, censoring or exposure effects. Correlation beyond a common control is
absent. Do not translate synthetic detection frequencies into measured power,
recommended culture counts, biological rescue, or comparative clinical benefit.
