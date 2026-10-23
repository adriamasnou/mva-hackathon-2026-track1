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
