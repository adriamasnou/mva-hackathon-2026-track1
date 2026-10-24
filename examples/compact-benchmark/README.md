# Portable compact713 raw-result verification

These tools package the completed public compact benchmark and independently
recalculate both the frozen original and corrected v2 evaluations. They run with
Python 3.9+ and the standard library, without importing either evaluator, their
helpers, the independent outer audit, or any inference package. No Java, network,
VCF or database is needed for **offline verification**.

The completed export is `results-20261024-v1/`. All 1,418 raw outputs and both
evaluations passed independent portable verification. From the extracted package
root, run `python3 -B examples/compact-benchmark/verify.py examples/compact-benchmark/results-20261024-v1`.
The copied README inside that immutable export preserves its preparation-time wording.

The accompanying report and figure are maintained separately. The full local
independent audit is retained under `independent-audit/`; its source snapshot needs
the original execution directories and is not a standalone inference environment.

## What is retained

- All 713 case records, byte-for-byte, including four preparation failures in each
  arm. The fixed ledger contains 1,426 case/arm rows and exactly 1,418 executable
  jobs, with original-HPO and no-HPO arms.
- Every full raw JSONL, byte-for-byte (approximately 120 MB uncompressed), and every
  executed job YAML. SHA256 links run from raw bytes to the execution receipt.
- The original execution/manifest, frozen protocol, preparation receipt, runtime
  property bytes and text, batch, log, addenda and database extraction receipts.
- Original and corrected evaluations; original adapter/helper and reused scoring,
  exporter and runner source; corrected adapter/helper; correction receipt and
  exact diffs; installed-bytecode evidence and the empirical serialization probe
  (`ModeScoreProbe.java`, output and receipt). Java **source** is evidence; no Java
  binaries are included or executed.
- The source-reading crosscheck, its prior reading-ledger hash, this verifier,
  exporter, focused tests, and this README.
- `path-map.json` maps original absolute paths to portable relative paths and
  records the omitted VCF hashes. Files retain their original provenance strings;
  the verifier never follows them to external locations.

The case file's legacy `DRAFT_NOT_FROZEN` string is preserved. Its exact SHA256 is
bound by the later `FROZEN_BEFORE_INFERENCE` protocol and checked against a fixed
case-file hash in the verifier. Rewriting that string would change the evidence.

The exporter reads only the public compact input VCFs to check their hashes before
and after packaging, but does not include them. Offline verification cannot recheck
absent VCF bytes, Java binaries or databases: it cross-links their retained receipts.
Copied evaluator code is provenance; its original absolute layout is not a portable
inference environment. SHA256 consistency is not an external signature or timestamp.

## Endpoints and retained failures

Every emitted gene must have a unique, nonempty symbol and finite numeric
`combinedScore`, including genes excluded by filtering. The ranking universe is
genes with at least one allele whose `filterStatus` is exactly `PASSED`. Best rank
is one plus the number of strictly greater scores; conservative worst rank counts
all scores greater than or equal to the source-gene score. Ties are exact numeric
ties, not rounded display scores.

Three distinct endpoints are recalculated:

1. **Primary:** every exact source allele occurs exactly once within the source
   gene and is `PASSED`, plus worst-tied gene rank within top 1, 5 or 10.
2. **Gene-only:** the gene rank alone, retaining cases where a source allele was
   filtered or unrepresented as failures for the primary endpoint.
3. **Strict joint best mode:** the primary endpoint plus all exact source alleles
   listed in the contributing variants of at least one **individual** inheritance
   mode tied at the reported best gene score. A union across separate modes cannot
   establish this endpoint. Every-best-mode recovery is retained separately.

Global contribution flags are separate from best-mode evidence. Missing
contribution flags or mode contribution lists stay unknown and cannot establish
strict success. An omitted mode-level `combinedScore` defaults to zero in v2,
matching installed Java primitive-double `NON_DEFAULT` serialization. Explicit
null, boolean and nonfinite scores remain invalid. A missing **gene-level** score
does not inherit this correction. Original literal evaluation remains retained and
independently recalculated, including the failures its missing-score rule produced.
Every changed case/arm is listed in the optional verification report.

All six fixed strata are checked: all 713/261 source genes, autosomal primary
681/245, technical X 32/16, matching fallback 18/13, no fallback 695/257, and pairs
64/41. Each endpoint has case-level and equal-weight gene-macro top1/5/10 and MRR.
Gene macro first averages all signatures within each source gene, including
failures, then averages across genes. Arithmetic uses exact fractions, allowing
only a 1e-12 tolerance when comparing serialized evaluator aggregate floats.

Preparation, missing and invalid outputs, and failed/unrepresented source alleles
remain in the ledger with endpoint reciprocal rank zero as applicable. A verified
empty JSONL has a zero emitted universe and observed nonrecovery; a missing output
has unknown evidence. Both original and corrected evaluations must match the
independent row and aggregate calculations. The package release gate is stricter
than the protocol's allowance for a failed batch: it requires completed exit 0,
all 1,418 receipt-backed outputs and no missing-output list. It does **not** require
every output to be scientifically successful or even evaluable; those failures stay.

## Commands

From the extracted review-package root, run the focused synthetic tests (no mounted data required):

```sh
python3 -B -m unittest discover -s examples/compact-benchmark -p test_verify.py -v
```

From the original working checkout (which contains the nested `repo/` directory),
only after release review, export to a new destination version:

```sh
python3 -B repo/examples/compact-benchmark/export.py \
  --work /Volumes/easystore/MVA-public-exomiser-2512/runs/public-temporal-compact-20261024 \
  --cases pipeline/public_validation/temporal_compact/draft-01/cases.planned.json \
  --original-evaluation pipeline/public_validation/temporal_compact/evaluation-20261024.json \
  --corrected-evaluation pipeline/public_validation/temporal_compact/correction-v2/evaluation-20261024.json \
  --correction-dir pipeline/public_validation/temporal_compact/correction-v2 \
  --out repo/examples/compact-benchmark/results-20261024-v1 \
  --parent-ready
```

The exporter requires fresh destination creation, checks source hashes, copies to a
temporary sibling directory, independently verifies the staged bundle, rechecks
source hashes, then moves the verified files into the new version (receipt last).
Existing destinations are never overwritten. No inference or evaluation producer
is run. An interrupted final move can leave an incomplete directory: preserve it
and choose a new version; do not treat an incomplete directory as verified.

Move the bundle anywhere and verify it offline:

```sh
python3 -B /path/to/bundle/verify.py /path/to/bundle \
  --report /path/to/new-independent-verification.json
```

The optional report is created exclusively outside the immutable bundle. It retains
both full case/arm ledgers, six-stratum summaries, source/mode observations, errors,
and every correction-affected case/arm. Without `--report`, verification prints a
compact receipt and correction-change list. A missing file, changed SHA, duplicate
job, path traversal, symlink, denominator drift, provenance mismatch or discrepant
evaluation causes a nonzero exit. No fallback to the source mount is allowed.

## Interpretation limits

This is our 713-signature reconstruction, not the authors' exact 719-case cohort.
There are 322 source PMIDs. The retained crosscheck reports only PMID 37054711 in
the prior 51-main-text reading ledger, with 321 absent. The verifier checks that
these lists partition the frozen source PMIDs, but the prior reading ledger is not
bundled and its contents are not re-adjudicated here. No new paper read or clinical
truth adjudication is claimed; even the overlap does not validate a selected case.

There are ten constructed input hypotheses per case, but mapping/filtering changes
the emitted and passing gene universes. Top10 may be trivial. These candidate
universes differ from the whole-genome and phenotype-only benchmarks and from the
authors' experiments. Current 2512 disease/gene/phenotype knowledge remains active;
this is not a temporal knowledge holdout. Synthetic decoy genotypes, unasserted
phase and technical X handling further limit interpretation. No clinical accuracy,
biological or therapeutic benefit, or competitor superiority follows from recovery.
