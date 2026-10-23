# A dated, source-traceable gene-to-condition lookup

**Rebuilt 23 October 2026 from a retained HFEA workbook dated 5 August 2026.**

Open [the offline navigator](pgtm-navigator.html), search a gene and inspect the candidate condition mappings. It sends no query to a server. Confirm findings with the [current HFEA register](https://www.hfea.gov.uk/pgt-m-conditions/) and a genetics/fertility clinic.

The workbook has condition, status and OMIM fields. We join phenotype OMIM identifiers through ClinVar and HPO; gene-MIM identifiers use OMIM's gene index. The latter is not a phenotype-to-gene table. Per-gene evidence records the source and exact OMIM link. Source disagreement may reflect biology, curation differences or mapping error; it is never automatically declared resolved.

## Measured output

The current builder produces **2,063 rows**, **2,028 mapped**, **35 unmapped**, **1,782 gene symbols** and **nine ClinVar/HPO disagreement rows**. Both ClinVar AssociatedGenes and RelatedGenes are read; taking one field only discarded four symbols. All rows remain in the CSV, including malformed/missing OMIM fields and unmapped conditions. **[OUR MEASUREMENT — `tools/pgtm/build.py`, source hashes in `hfea-pgtm-provenance.json`]**

Of the indexed symbols, **1,692/1,782 (94.9%)** are not literal whole-word matches in their associated workbook condition names. This is a text-matching statistic on a snapshot, not a measured failure rate for the current website's search or for a family's access to testing. Aliases and alternative search paths matter. **[OUR MEASUREMENT]**

## Reproduce and inspect

- [Builder and instructions](../tools/pgtm/README.md).
- [Complete CSV](hfea-pgtm-gene-crosswalk.csv), with per-gene evidence.
- [Gene index](hfea-pgtm-gene-index.json).
- [Source hashes, dates and counts](hfea-pgtm-provenance.json).
- [Curation-coverage audit](register-audit.md).

## Interpretation limits

The source files are retained snapshots, not a live registry mirror. A source association is a **candidate mapping**, not a clinical assertion that every listed gene causes every presentation of that condition. Multiple genes, conflicting sources and unparsed identifiers require review. A row's approval status does not establish the classification of an individual's variant, clinic test feasibility, funding or family eligibility. No match is not evidence of ineligibility.

This tool has not undergone a family/clinician usability study. Cross-gene coverage is measured; improved access and clinical outcomes are not. We make no exclusivity claim for the idea of a gene-indexed register.
