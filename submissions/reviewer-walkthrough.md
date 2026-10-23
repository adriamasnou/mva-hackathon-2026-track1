# Review the working tools

The [report](adriamasnou_track2_report.pdf) explains the candidate and proposed biology. These short examples let a reviewer inspect the delivered software locally. They require neither challenge data nor a network connection.

## Follow a gene to its source

Download [pgtm-navigator.html](pgtm-navigator.html), open it in a browser and search **BUB1B**. Inspect the candidate gene evidence, original condition name, identifier and source date. Compare that gene search with the condition's wording: the crosswalk can find a connection even when the register's title does not literally name the gene.

Next search **CHIME** and inspect the unresolved identifier warning. The complete register includes unmapped rows. A missing gene result does not establish ineligibility; a condition-level approval does not establish suitability for a particular variant or family. The [source audit](pgtm-expanded-validation.md) records which associations and qualifiers were checked, with explicit shared-source and developer-review limits.

## Inspect a false rescue signal

From the repository root, run:

```sh
python3 analysis/rescue_decision/decision.py examples/rescue-decision-demo/abundance_rise_benefit_ruled_out.json
```

The synthetic example supplies a protein increase but a functional-benefit interval below its illustrative programme threshold. The expected decision is **`WORTHWHILE_BENEFIT_RULED_OUT`**, with no replication candidate. Inspect the input: the confidence interval is supplied, not fitted by this program, and its threshold is not a clinical recommendation.

Two further examples distinguish a misleading survivor fraction from a failed measurement:

```sh
python3 analysis/rescue_decision/decision.py examples/rescue-decision-demo/selective_killing_despite_better_survivors.json
python3 analysis/rescue_decision/decision.py examples/rescue-decision-demo/failed_exposure_measurement.json
```

Expected decisions are **`DO_NOT_ADVANCE`** for the selection example and **`TECHNICALLY_INDETERMINATE`** for failed exposure measurement. The latter cannot establish biological inefficacy. Exit 0 means valid input, not a favourable biological result. These are three materialized examples from the existing frozen casebook, not additional independent validation cases. The [complete prototype evaluation](rescue-decision-validation.md) contains all 40 expected cases and the limits of its assertions.

## Reproduce the public software checks

```sh
python3 -m unittest discover -s tests -v
python3 canary/run_canary.py --self-test
python3 analysis/exposure_check.py
python3 tools/check_package.py
python3 examples/public-case/verify_reconstruction.py --export examples/public-case/reconstructed-results
```

The canary self-test injects faults into synthetic checker inputs. Its [separate measured SpliceAI controls](../canary/README.md) document actual inference. The [public Exomiser recipe](../examples/public-benchmark/README.md) requires the named Java runtime and large public databases; it is a separate computational evaluation. No check here measures N1002K rescue, clinical benefit or family usability.
