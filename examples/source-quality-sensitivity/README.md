# Source-quality sensitivity: offline companion

Software and editorial packaging of the **existing verified 20:31 analysis**. Open `index.html` directly in a browser; it needs no server, fetch, network, font download or external asset. Keep this directory together when moving it. No hosting or submission has been performed.

**Post hoc, non-blinded, explicit `per_case` outcome exposure.** The results concern source correspondence and source-label recovery, not clinical truth, clinical accuracy, an effect of review/HPO, or biological benefit. Packaging performs no biomedical source review, re-adjudication, experimental design or inference rerun. Safety-stopped biological reviews are outside this work's scope.

## One-command verification

From this directory, with Python **3.11 or newer on macOS or Linux** (the preserved freeze scripts use POSIX directory syncing):

```sh
python3 -B verify.py
```

The command also works from another working directory when given the path to `verify.py`. Do not run Python with `-O` or `PYTHONOPTIMIZE`; the preserved parent checker uses assertions and the wrapper rejects optimized mode. Only the Python standard library is required. If Node.js is on PATH, the same command additionally performs `node --check` and minimal-DOM execution checks for every selector combination. If Node is absent, its checks are explicitly reported as not run; the exact prechecked viewer script and all embedded data are still verified. No package file is written, including bytecode caches.

Verification creates and removes a temporary directory using the platform default temporary location. `TMPDIR` may point to a writable scratch directory **outside this package**. Console JSON is the fresh result; redirect it outside the package if a receipt is wanted. The package manifest rejects additional files inside the package.

The command checks all packaged hashes and original provenance bindings, runs the original **29 failure-injection tests** unchanged plus eight packaging integrity controls, and uses the original analysis and seal code to regenerate these five files in temporary storage:

- `methods.json`
- `joined-cases.jsonl`
- `all-strata.json`
- `frozen-baseline-strata.json`
- `findings.json`

Each is compared **byte-for-byte** to its frozen original. The original parent implementation is rerun independently from scores, exact PASSED allele evidence and selected/alternate joins across **713 cases, 1,426 arms and 162 categories**. It does not import the analysis code. Its newly produced receipt is compared to the included original receipt, excluding only the run timestamp. Analysis validation receipts exclude only their run timestamp and relocated benchmark-receipt path; every substantive field must remain identical. The original time/path-dependent delivery seal is preserved as evidence, not required to be byte-identical to a newly created temporary seal.

The source snapshot consistency verifier runs against the packaged inputs. The earlier **raw benchmark verifier report is included and hash-checked**, bound to the included export receipt. Its 2,870-file / 1,418-raw-output verification was performed previously: the complete raw inference-output bundle is not in this companion, and that earlier raw-output check is **not rerun here**. The parent recomputation here works from the frozen score and exact-allele evidence in the corrected evaluation.

## Frozen scope

- All **713** cases: **681** primary autosomal and **32** technical X; both arms, including all failures.
- All **six** overlapping cohorts and **seven** separate marginal source dimensions; **162** categories, including **15** empty groups with null rates.
- Exact **621** frozen inputs, **87,464,273 bytes**: 613 source snapshot files plus eight benchmark/provenance files. They are JSON, Python and Markdown; no raw article PDFs or gated hackathon data are added.
- Source manifest SHA256: `ddf90f9eaebab874d45805f2345e05246a9fdd61a0d348259770b3c1d10854a0`.
- Both the corrected-v2 and original literal pre-correction evaluation remain intact. The viewer and sensitivity analysis use corrected v2.

For all 713 cases, original-HPO versus no-HPO recovery at top 1/5/10 remains **581/681/693 versus 449/677/693**. Primary autosomal counts remain **556/653/665 versus 430/649/665**, each over 681. Technical-X counts remain **25/28/28 versus 19/28/28**, each over 32; all four preparation failures per arm remain. These are source-label recovery counts, not clinical accuracy.

All contrary pairs and adverse strata are retained. In the full-cohort incomplete-paper group, top-5 counts are 297/316 with original HPO versus 300/316 with no HPO. Among unresolved selected packets they are 297/308 versus 300/308; among genotype-supported packets, 146/153 versus 147/153. The fixed 64-signature two-allele cohort has top-1 counts 58/64 versus 59/64. Complete review does not imply supported labels; a contradiction is not a disproved diagnosis.

## Viewer

The default view shows all 713 cases, all seven dimensions, and top 1. The cohort and threshold selectors also cover all six cohorts and top 5/10. No category or outcome filter exists. Every category remains visible within each selected dimension, including empty categories. A fixed, unfiltered reference always shows all six cohort baselines at all three thresholds; no favorable filtered headline is calculated.

Each category shows case and gene denominators, both arm counts/rates, neutral bars, all four paired counts, and the total and discordant pair denominators. Expand the details for status/failure counts, tie counts, exact-allele pass counts, discordant shares and case IDs. The same all-strata object is embedded in full, including every case ID. Definitions and limitations are included inline. Percentages are display-rounded; integer counts and original JSON values are preserved.

The HTML generator is deterministic and its output is checked by `verify.py`. To produce a comparison copy outside the package:

```sh
python3 -B build_viewer.py --output ../sensitivity-viewer-check.html
```

The generator refuses to overwrite an existing file. The standalone HTML remains self-contained if moved alone, but its relative links to code/data then require the full directory.

## Files and provenance

- `inputs/` — exact frozen input bytes, addressed by relative paths at runtime.
- `provenance/analysis-2031/` — every original analysis file, unchanged, including code, original 29 tests, results, methods, assumptions, canonical object hashes, input receipt, freeze/seal scripts and delivery manifests.
- `provenance/parent/` — unchanged independent parent code and original verification receipt.
- `benchmark-verification.json` and `benchmark-verifier.stdout.json` — unchanged earlier raw-benchmark verification artifacts.
- `verify.py` — portable read-only orchestration; no new analysis algorithm.
- `index.html`, `viewer.template.html`, `build_viewer.py`, `test_viewer.cjs` — viewer, deterministic source and Node execution checks.
- `test_portable.py` — eight integrity-boundary controls.
- `package-manifest.json` — package-relative size/SHA256 inventory; covers every other file, including verifier and HTML. The manifest cannot hash itself; its digest is supplied in the external packaging receipt. Hashes establish byte integrity, not an external signature or clinical validity.

Original absolute paths are retained **only as provenance**. The wrapper relocates the analysis `HERE`/`INPUT_ROOT`, parent `HERE`/`ANALYSIS`/`ROOT`, seal `__file__` location and command-line input argument at runtime. Original Python source bytes are unchanged; no algorithm, endpoint, label or frozen input is edited. Run the wrapper, not the historical scripts' machine-specific default commands.

This freeze remains fixed even if the live source audit subsequently changes. Review completion is nonrandom; cases share genes and papers; source inputs and labels can overlap current knowledge; top 10 can be trivial in the constructed passing-gene universes. There are no inferential p-values, independent clinical-truth claims or new reading credits. Existing original documents describe their original scope and history; this companion is the bounded software implementation described above.
