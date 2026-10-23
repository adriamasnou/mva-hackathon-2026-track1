# Interpretation canary: missing output must not become a negative result

The executable public panel checks six GRCh38 SpliceAI controls: five splice-site variants and one coding negative control. It checks gene/variant identity, finite scores, the expected acceptor-loss or donor-loss channel, completeness, duplicates and process exit status. A complete, passing run exits 0; failed assertions exit 1; unavailable prerequisites exit 2. **A skipped or empty run never passes.**

These are regression expectations for this pinned tool and panel, not biological certainties for every splice predictor. Pathogenicity does not guarantee any predictor's score. The panel is a liveness/regression check, not a clinical sensitivity benchmark. Other depth and prioritisation experiments described in the report are not executed by this portable panel.

## Verify the harness without model downloads

```sh
python3 canary/run_canary.py --self-test
python3 -m unittest discover -s tests -v
```

The self-test accepts a synthetic known-good score fixture and rejects nine injected failures. It tests the **checker**, not model inference. Synthetic fixtures are labelled in code and never reported as measured model outputs.

## Execute real model inference

Use a separate Python environment with `spliceai==1.3.1`, `tf-keras`, `numpy` and `pysam` installed; consult the dependency snapshot for versions actually tested. SpliceAI and its model remain third-party dependencies under their own licences. Supply an indexed GRCh38 FASTA using Ensembl contig names (`1`, not `chr1`), consistent with the model's `grch38` annotation.

```sh
python3 canary/run_canary.py --splice --reference /path/to/GRCh38.primary.fa.bgz --save-output model-results.txt
```

The model runner is shipped at `pipeline/spliceai_run.py`. It includes the NumPy-compatible encoding fix; no patient dataset or reference genome is bundled. Missing dependencies, a nonzero subprocess exit, missing gene scores or a mismatched reference cannot produce a pass. To inspect previously captured output without rerunning inference, use `--scores model-results.txt`; the output labels that distinction.

## Limits

The six controls cannot establish accuracy across genes, indels, ancestries or diseases. A passing run does not make a low score evidence against disease on its own. The coding negative is a published finding from this project; it is not a benign clinical control. The original package could pass when it executed zero assertions: that defect is corrected and covered by a regression test.
