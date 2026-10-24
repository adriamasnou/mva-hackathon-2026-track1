# Independent public execution audit

Status: **complete_pass**. Recorded 2026-10-24T00:54:20.967050+00:00.

This sidecar reads frozen public inputs and raw JSONL, recomputes ranks by direct arithmetic, and does not import the public evaluator/exporter. Shared gates, inference inputs and execution are untouched.

Checks: 113 passed; 0 errors. Full outcome audit is recorded only for a completed execution receipt.

## HG002

Execution: completed.

Checked 48 expected jobs; 48 passed raw-output validation. The accepted files contain 22560 gene rows with unique per-job identities and finite combined scores. Per-allele whitelist fields: 0 explicit true, 0 explicit false, 38072 unavailable. Unavailable fields remain null; runtime zero-whitelist evidence is separate.

The retained execution log reports `Loaded 0 whitelist variants`; the recorded properties disable the ClinVar whitelist. This is runtime evidence, not an observed false flag on each allele.

Across all four arms, 56 of 56 source-allele observations match the target gene exactly; 56 are marked contributing under at least one reported mode and 0 are unmatched. This does not mean all source alleles jointly determine the best gene score; that is audited separately below. Gene rank remains distinct from allele recovery and phase.

- original: conservative top-1/5/10 = 6/7/8 of 9; not scored 0.
- half_missing: conservative top-1/5/10 = 6/7/8 of 9; not scored 0.
- swapped: conservative top-1/5/10 = 3/5/6 of 9; not scored 0.
- none: conservative top-1/5/10 = 0/0/6 of 9; not scored 0.

All twelve case rows, both source-support partitions, allele flags and exact hashes are retained in the companion JSON.

- COG8 / none: rank 8–8; best-scoring modes use AUTOSOMAL_DOMINANT: 1/2 source alleles. A gene can rank without both source alleles determining that score, even when both have a global contribution flag.
- SLC35C1 / none: rank 8–8; best-scoring modes use AUTOSOMAL_DOMINANT: 1/2 source alleles. A gene can rank without both source alleles determining that score, even when both have a global contribution flag.

## HG001

Execution: completed.

Checked 48 expected jobs; 48 passed raw-output validation. The accepted files contain 16512 gene rows with unique per-job identities and finite combined scores. Per-allele whitelist fields: 0 explicit true, 0 explicit false, 28184 unavailable. Unavailable fields remain null; runtime zero-whitelist evidence is separate.

The retained execution log reports `Loaded 0 whitelist variants`; the recorded properties disable the ClinVar whitelist. This is runtime evidence, not an observed false flag on each allele.

Across all four arms, 56 of 56 source-allele observations match the target gene exactly; 56 are marked contributing under at least one reported mode and 0 are unmatched. This does not mean all source alleles jointly determine the best gene score; that is audited separately below. Gene rank remains distinct from allele recovery and phase.

- original: conservative top-1/5/10 = 7/8/8 of 9; not scored 0.
- half_missing: conservative top-1/5/10 = 7/8/8 of 9; not scored 0.
- swapped: conservative top-1/5/10 = 5/6/6 of 9; not scored 0.
- none: conservative top-1/5/10 = 0/0/0 of 9; not scored 0.

All twelve case rows, both source-support partitions, allele flags and exact hashes are retained in the companion JSON.

- COG8 / none: rank 11–11; best-scoring modes use AUTOSOMAL_DOMINANT: 1/2 source alleles. A gene can rank without both source alleles determining that score, even when both have a global contribution flag.
- SLC35C1 / none: rank 11–11; best-scoring modes use AUTOSOMAL_DOMINANT: 1/2 source alleles. A gene can rank without both source alleles determining that score, even when both have a global contribution flag.

## Interrupted attempt and relaunch

All completed prior outputs were retained and compared; the first attempt remains interrupted after two outputs. Scientific YAML is unchanged except output directory; input VCF paths/hashes are unchanged; properties differ only in bounded cache size 60000 → 300000.

- PMID_36595822_nan.original.jsonl: 470 gene rows, all three ranking-score fields equal; changed p-values 469; changed reported phenotype-model evidence 101; byte equality False.
- PMID_36595822_nan.half_missing.jsonl: 470 gene rows, all three ranking-score fields equal; changed p-values 470; changed reported phenotype-model evidence 106; byte equality False.

## Errors and pending checks

- No errors detected in executed checks.

## Limits and unsupported claims

- Public synthetic spike/background ranking agreement only; no biological rescue, clinical accuracy, therapeutic benefit or competitor superiority follows.
- Nine primary labels retain their source qualifications. PAX4 is disputed; ZIC3/OFD1 are technical cases without an X background. No cases are replaced or dropped.
- Original 4/3/2 and current 4/5 source-support partitions are separate. Later visual follow-up is not retroactive pre-inference evidence.
- No gene or diagnosis field is supplied to inference; provenance IDs remain, and source HPO terms can themselves be disease-specific. OMIM inheritance priors and other database knowledge remain.
- PASS_ONLY raw output cannot establish why an absent allele disappeared. Absence after bounded representation review is not proof of a particular filter failure.
- An omitted per-allele whiteListed field is retained as null/unavailable, never converted into an observed false flag. Runtime bypass disabled is supported separately by the retained Loaded 0 whitelist variants log.
- Gene ranking is not recovery of every source allele, proof of trans phase, or independent confirmation of a published diagnosis.
- A true contributesToGeneScore flag means contribution under a reported inheritance mode; it does not by itself prove a joint causal configuration or biological function.
- Only the two completed outputs of the interrupted first attempt can be compared across JVMs. Full JSON byte reproducibility is not claimed.
- The cache relaunch occurred after inference began. Equality of retained scientific inputs supports an operational-only change, not a claim of external preregistration or proof of human non-inspection.
- Database receipt files and installed software are hashed; multi-gigabyte database payloads are not rehashed by this sidecar. Reference allele windows and FAI are checked, not the entire reference FASTA.
- Genotypes and all non-spike rows are compared to retained public normalized backgrounds. The GFF/exon extraction and source literature adjudications are not independently rerun here.

## Changed paths and reproduction

- `pipeline/public_validation/audit_public_execution.py`
- `dossier/sweeps/evidence-2026-10-23/rubric-repair/public-execution-independent-audit.md`
- `dossier/sweeps/evidence-2026-10-23/rubric-repair/public-execution-independent-audit.json`

Run `python3 pipeline/public_validation/audit_public_execution.py --self-test` for bounded negative controls; run without flags after completion for the full audit. `--inputs-only` audits inputs without reading inference outputs. Exit 2 means pending, not success. No commits, push, submission, contact, shared gates, or gated patient-data access are performed.
