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

## Inspect public source-label recovery

The [multi-case writeup](public-validation.md) reports all 96 genomic and twelve phenotype-only jobs, including misses, source qualifications and two frozen source-support partitions. [Paired genomic results](../examples/public-benchmark/results/paired-summary.json) use the same nine primary source labels on both backgrounds; there are not eighteen independent cases.

Compare CTCF and DOCK8 in the [phenotype-only evaluation](../examples/public-benchmark/results/phenotype-only/evaluation.json) and the genomic [HG002](../examples/public-benchmark/results/HG002/evaluation.json) / [HG001](../examples/public-benchmark/results/HG001/evaluation.json) evaluations. All three recover eight of nine labels within ten, but CTCF ranks 132 versus 1/1 and DOCK8 ranks 2 versus 22/15. Different candidate universes and filtering prevent interpreting those changes as the causal value of sequencing.

Next compare the [HG002 source-allele diagnostic](../examples/public-benchmark/results/HG002/source-variant-audit.json) with the [raw source-gene record excerpts](../examples/public-benchmark/results/source-gene-evidence/records.json). COG8 and SLC35C1 have two exact, passed source alleles with contribution flags, yet each no-HPO best-scoring autosomal-dominant mode uses only one allele. The excerpt verifier below reproduces those four exceptions across both backgrounds. A global contribution flag does not establish joint pair recovery or phase.

Verify the compact exports without a reference genome, Java or annotation databases:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 examples/public-benchmark/verify_export.py examples/public-benchmark/results/HG002
PYTHONDONTWRITEBYTECODE=1 python3 examples/public-benchmark/verify_export.py examples/public-benchmark/results/HG001
PYTHONDONTWRITEBYTECODE=1 python3 examples/public-benchmark/export_phenotype.py --verify examples/public-benchmark/results/phenotype-only
PYTHONDONTWRITEBYTECODE=1 python3 examples/public-benchmark/source_evidence.py --verify examples/public-benchmark/results/source-gene-evidence
```

These checks verify hashes and rederive ranks from every retained gene-score table. The excerpt check also recomputes joint best-mode allele contribution and matches source-gene scores to the compact exports. Full source-file hashes were verified during extraction; the offline check can inspect their recorded hashes but cannot rehash undistributed original files. These checks do not rerun inference, independently confirm the published diagnoses or measure therapeutic benefit.

## Reproduce the public software checks

```sh
python3 -m unittest discover -s tests -v
python3 canary/run_canary.py --self-test
python3 analysis/exposure_check.py
python3 tools/check_package.py
python3 examples/public-case/verify_reconstruction.py --export examples/public-case/reconstructed-results
python3 -S analysis/rescue_decision/simulation/frozen-source/verify.py --folder analysis/rescue_decision/simulation --results analysis/rescue_decision/simulation/results.json --compare analysis/rescue_decision/simulation/parent-reproduced-results.json
```

The canary self-test injects faults into synthetic checker inputs. Its [separate measured SpliceAI controls](../canary/README.md) document actual inference. The simulation command checks retained results and an independently launched exact seeded rerun; [full execution instructions](../analysis/rescue_decision/simulation/README.md) require the pinned scientific runtime. The [public Exomiser recipe](../examples/public-benchmark/README.md) requires the named Java runtime and large public databases; it is a separate computational evaluation. No check here measures N1002K rescue, clinical benefit or family usability.

The [compact companion](compact-public-validation.md) provides a separate 713-signature, ten-hypothesis constructed benchmark. Use it to inspect the effect of removing HPO and whether both source alleles contribute within one best-scoring mode. These checks expose limitations hidden by gene-level recovery; they do not establish general diagnostic accuracy. The original parser failure and corrected baseline are both retained. Verify the raw results offline from the package root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 examples/compact-benchmark/verify.py examples/compact-benchmark/results-20261024-v1
```

In the 64 constructed source pairs, original-HPO top-1 with both source alleles PASSED was 58/64, but requiring both alleles within one best-scoring mode reduced it to 42/64. Without HPO, the corresponding counts were 59/64 and 2/64. A correct gene rank therefore does not establish that the complete source genotype determines the winning score. These are source-label metrics, not clinical or phase validation. **[OUR MEASUREMENT; OUR INFERENCE]**
