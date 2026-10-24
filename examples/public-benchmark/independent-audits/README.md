# Independent execution audit snapshots

These reports were produced by validators that read the original raw runtime outputs independently of the public exporter/evaluator. They retain input/output checksums, case-level failures and limitations. The adjacent Python files are exact source snapshots; their SHA-256 hashes are recorded in the reports.

The full local audit scripts require the original execution directories, software installation and receipts named in their source. They are provenance snapshots, not a claim that the entire runtime is bundled here. Use the portable verification commands in `submissions/public-validation.md` from the repository root to recompute the distributed ranks and source-allele evidence. Those commands do not rerun Exomiser inference.

The phenotype audit additionally qualifies 19,192 unique gene-symbol records as 19,116 distinct nonzero Entrez IDs. Its separate Entrez-collapsed sensitivity leaves all twelve target ranks unchanged; the frozen endpoint remains symbol-based. Its original failed one-to-one-identity assumption is disclosed in the report and retained in the local audit archive.
