# Rebuild the PGT-M navigator

Python 3 standard library only. Download the public source files to a directory you control. The shipped output is a dated snapshot, and the SHA-256 manifest identifies the exact files used; public URLs can change contents. Do not claim an exact historical rebuild with newer files unless the hashes match.

Sources:

- [HFEA workbook dated 5 August 2026](https://www.hfea.gov.uk/media/ssapbtyc/2026-08-05-pgt-m-full-approved-condition-list.xlsx), with [live register](https://www.hfea.gov.uk/pgt-m-conditions/) for current checking.
- [ClinVar gene_condition_source_id](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/gene_condition_source_id).
- [HPO genes_to_disease.txt](https://purl.obolibrary.org/obo/hp/hpoa/genes_to_disease.txt).
- [OMIM mim2gene.txt](https://omim.org/static/omim/data/mim2gene.txt), for gene-MIM entries only. Observe source-specific terms when reusing or redistributing data.

Keep the three mapping filenames as listed. The workbook path is explicit:

```sh
python3 tools/pgtm/build.py --hfea /path/to/hfea.xlsx --source-dir /path/to/mappings --snapshot-date 2026-08-05 --register-source-url https://www.hfea.gov.uk/media/ssapbtyc/2026-08-05-pgt-m-full-approved-condition-list.xlsx --out-dir /path/to/output
```

Open the generated `pgtm-navigator.html` locally. Its data are embedded; searching does not fetch or transmit anything. The full CSV includes all rows, even when the browser limits a broad result display to 60. Source disagreements, malformed identifiers and missing mappings remain visible.

To reproduce the expert-assertion coverage proxy, also obtain [ClinVar variant_summary.txt.gz](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz):

```sh
python3 tools/pgtm/expert_coverage.py --clinvar /path/to/variant_summary.txt.gz --crosswalk /path/to/output/hfea-pgtm-gene-crosswalk.csv --output /path/to/output/expert-coverage.json
```

The proxy measures qualifying review-status records, not the existence of experts, diagnostic validity, variant classification or PGT-M eligibility. Read the [audit limitations](../../submissions/register-audit.md).

## Source-adjudicated task check

Run `python3 tools/pgtm/audit.py` from the repository root. This needs Python 3 and
Node.js on PATH, with no third-party packages or network access. It executes the
actual shipped navigator JavaScript through a minimal DOM adapter. A missing
runtime, source excerpt or malformed input fails rather than reporting skipped
checks as success. `--node /path/to/node` selects a runtime explicitly.

The default checks the bundled, manually reviewed excerpts. For the stronger check
against the **exact original snapshots**, supply both source arguments:

```sh
python3 tools/pgtm/audit.py --hfea /path/to/hfea.xlsx --source-dir /path/to/mappings --output /path/to/task-result.json
python3 -m unittest discover -s tests -p 'test_pgtm_audit.py' -v
```

`audit-tasks.json` contains explicit expected answers, selection reasons and the
shared-source limitation. `audit-evidence.json` records exact HFEA cell coordinates,
25 original mapping lines, source URLs and whole-file SHA-256 hashes. The full-source
mode checks all four input hashes, original cells/lines and completeness of mapping
excerpts for the selected identifiers. It does not fetch newer files. Source URLs
are mutable; a newer snapshot requires a new adjudication, not a changed hash alone.

The [task-validation record](../../submissions/pgtm-task-validation.md) describes
the 11-task convenience sample and its limited comparison with literal condition-title
search. This is not a clinical benchmark or a user study. NIH/NCI pages separately
corroborate six selected gene/condition relationships; their live contents were
read manually and are not part of the cryptographically pinned offline evidence.

The builder rejects missing/duplicate required ClinVar/HPO headers and partial or
extra-column TSV rows. A file truncated cleanly at a record boundary can still look
valid; pinned source hashes in the audit address integrity for this dated snapshot.
