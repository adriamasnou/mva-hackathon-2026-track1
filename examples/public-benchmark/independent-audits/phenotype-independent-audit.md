# Independent phenotype-only execution audit

Status: **complete_pass**. Recorded 2026-10-24T08:56:38.865592+00:00.

The validator independently reads raw TSVs and uses Decimal arithmetic; it imports no public runner, evaluator or exporter. No inference or shared gates were run.

Checks: 34 passed; 0 errors. Validator controls: 17.

Primary conservative top-1/5/10: **4/8/8 of 9**. All 12 frozen cases remain visible. Raw output: 230304 rows across 12 jobs, each with 19,192 unique gene-symbol records; all mode ANY, all variant scores zero and all candidate-gene flags zero.

- PAX4 (disputed PAX4): phenotype score 1.0000; conservative rank 1–1 of 19192.
- MTOR (primary): phenotype score 0.7747; conservative rank 5–5 of 19192.
- KCNJ2 (primary): phenotype score 0.9405; conservative rank 1–1 of 19192.
- CTCF (primary): phenotype score 0.8658; conservative rank 132–132 of 19192.
- LZTR1 (primary): phenotype score 0.8251; conservative rank 3–3 of 19192.
- INTS11 (primary): phenotype score 0.8874; conservative rank 4–4 of 19192.
- BCKDHB (primary): phenotype score 1.0000; conservative rank 1–1 of 19192.
- DOCK8 (primary): phenotype score 0.7319; conservative rank 2–2 of 19192.
- COG8 (primary): phenotype score 0.8731; conservative rank 1–1 of 19192.
- SLC35C1 (primary): phenotype score 0.9463; conservative rank 1–1 of 19192.
- ZIC3 (separate X control): phenotype score 0.7747; conservative rank 7–7 of 19192.
- OFD1 (separate X control): phenotype score 0.9627; conservative rank 3–3 of 19192.

Ranks are rederived from each unique gene’s best reported EXOMISER_GENE_PHENO_SCORE. The native #RANK and combined-score columns are not used. Worst ties are calculated at the reported four-decimal precision.

## Identifier qualification and preserved first failure

Each of the twelve TSVs has **19,192 unique symbols but 19,116 distinct nonzero Entrez IDs**. There are **57 shared-ID groups spanning 133 symbols**. No ID-zero sentinel occurs, no symbol maps to multiple Entrez IDs, and no target source symbol shares an ID. Examples of shared IDs include EIF3C/EIF3CL (728689) and SMN1/SMN2 (6607). These are observed shared identifiers; this audit does not adjudicate whether the symbols are synonyms, distinct loci or database mapping artifacts.

The frozen endpoint remains symbol-based. An explicitly separate sensitivity calculation collapses each Entrez ID to its maximum reported phenotype score: all twelve target ranks are unchanged, as is primary top-1/5/10. No cases or source records were dropped or modified. The complete shared-ID mapping is retained per case in the companion JSON.

The first validator incorrectly required a one-to-one symbol/Entrez mapping and failed all twelve outputs. Its exact script and both failing reports were preserved before revision in `phenotype-independent-audit-first-pass/`, with verified hashes recorded in this audit. The corrected validator reports shared-ID and sentinel anomalies, and tests these cases explicitly; the first failure is not erased.

## Frozen inputs, failed attempt and runtime

All twelve native HPO lists, subject IDs and sexes are checked against the old frozen phenopackets and the frozen source cases. The native sample adds explicit hg38 and changes output paths; eligibility, source labels, analysis steps, inheritance modes, runtime properties, software and the scoring wrapper remain unchanged.

The old attempt failed with exit 1 on unsupported hg19 before phenotype analysis, leaving zero outputs and twelve missing outputs. Its receipts, log and empty output directory are retained. The original comparator freeze precedes genomic outputs; the native wrapper repair occurred after genomic outcomes were known, as explicitly disclosed in the new protocol/addendum.

The completed execution log contains twelve “without VCF” analyses, twelve summaries reporting 19,192 genes and zero filtered variants, and a completed batch of twelve. The gene count in the log requires the symbol/Entrez qualification above. The log also reports **Loaded 287098 whitelist variants**. No input alleles exist for whitelist bypass to affect; this does not mean global knowledge or ClinVar was disabled. OMIM and hiPhive remain active.

Parent export checked read-only: 35 receipted members, 36 files including the receipt; all twelve compact unique-gene score maps equal the independently read raw TSVs. No export was modified.

## Errors and limits

- No audit errors detected.

- Knowledge-only source-label recovery, not genomic or clinical validation. No biological benefit or competitor superiority is inferred.
- The phenotype score uses existing human/model-organism/PPI knowledge. OMIM and hiPhive remain enabled; global knowledge is not disabled.
- Runtime loaded 287098 whitelist variants. With no VCF, no input alleles and zero filtered variants, this whitelist cannot bypass filtering of input alleles. This is not a claim that ClinVar/global knowledge was disabled.
- Ranks use the maximum reported phenotype score per unique gene and conservative worst ties at four-decimal TSV precision. These are not necessarily ties at internal full precision; TSV #RANK and combined-score columns are not the endpoint.
- This comparator scores 19192 unique gene-symbol records per case, representing 19116 distinct nonzero Entrez IDs. There are 57 shared-ID groups spanning 133 symbols. The frozen endpoint is symbol-based; shared identifiers do not establish biological synonymy or 19192 independent gene identities.
- Its search space differs from the filtered genomic arms; rank differences are not an isolated effect-size estimate for adding a VCF. Entrez-collapsed sensitivity is diagnostic only and does not replace the frozen symbol endpoint.
- Nine primary source labels retain their source qualifications; PAX4 remains disputed and ZIC3/OFD1 are separate controls. No new independent disease cases are created by another comparator.
- The original comparator was frozen before genomic outputs. Its native hg38 wrapper was repaired later, after genomic outcomes were known, with no phenotype outputs from the failed attempt. No external preregistration or proof of human non-inspection is claimed.
- Execution/script/software and extraction-receipt hashes are checked; multi-gigabyte database payloads and the Java executable are not rehashed. Native wrapper behavior is supported by exact input comparison and runtime logs, not a fresh Java bytecode review here.
- No repeat phenotype execution was requested; full JSON/TSV byte reproducibility across JVMs is not established.
- Phenotype-only ranks make no allele-recovery or phase claim. The earlier genomic COG8/SLC35C1 No-HPO best-mode limitation remains: one of two source alleles determines the best mode in each background.

## Changed paths and reproduction

- `pipeline/public_validation/audit_phenotype_execution.py`
- `dossier/sweeps/evidence-2026-10-23/rubric-repair/phenotype-independent-audit.json`
- `dossier/sweeps/evidence-2026-10-23/rubric-repair/phenotype-independent-audit.md`

The exact first failing script and JSON/Markdown reports are additionally preserved under `dossier/sweeps/evidence-2026-10-23/rubric-repair/phenotype-independent-audit-first-pass/` at the user’s request. These are historical failure snapshots, not the current audit result.

Run `python3 -B pipeline/public_validation/audit_phenotype_execution.py --self-test` for validator controls, or omit the flag for the complete read-only input/output audit and these two reports. Exit 0 means all executed checks passed; exit 1 means errors. No main-report, workbook, export, input, shared-gate, inference or commit operations are performed.
