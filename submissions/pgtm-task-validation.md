# PGT-M navigator: source-adjudicated task validation

**Observed 23 October 2026: 11/11 selected tasks passed.** In seven selected gene
queries, the navigator retrieved the manually identified target condition in 7/7
cases. Case-insensitive literal substring search of the same target condition
titles found 3/7. The four additional target retrievals were BUB1B, CFTR, FMR1 and
PAH. This establishes a small, reproducible example of added lookup functionality;
it is not an estimate of clinical accuracy, general population performance, time
saved, patient benefit, or superiority to the live HFEA website.

The executable result, including exact artifact hashes and individual outcomes, is
[pgtm-task-validation.json](pgtm-task-validation.json). Expected answers are in
[audit-tasks.json](../tools/pgtm/audit-tasks.json); source records are in
[audit-evidence.json](../tools/pgtm/audit-evidence.json). Neither expected gene sets
nor expected source disagreements were calculated from the builder output.

## Selection and adjudication

This is a deliberately small **convenience sample**, not random, blinded, independent
human review or preregistered evaluation. An AI reviewer read the original HFEA
workbook XML cells and the original mapping records, then explicitly transcribed
expected genes, source links, flags and status before running the audit. Existing
tool output informed anomaly selection. Seven gene tasks were chosen to include the
project anchor, other disease areas, a gene identifier entry, multiple identifiers
and a source disagreement. Four further tasks exercise failure/edge behavior.

The nine target register rows, quoted cell values and 25 mapping records are retained
with original row/line locators. All referenced records are public; no patient data
are included. The named targets are:

- **BUB1B / BUBR1:** workbook row 1399, MVA1, MIM 257300. ClinVar line 890 and HPO
  line 5976 both map BUB1B. The gene query and supported alias each retrieve this row.
- **CFTR:** row 503, cystic fibrosis, MIM 219700. ClinVar lines 1333, 2694 and 7913
  and HPO lines 872–874 retain CFTR, FCGR2A and TGFB1. HPO labels CFTR `MENDELIAN`
  and the other two `POLYGENIC`. The audit expects these source associations to be
  preserved with a multiple-candidate warning; it does **not** endorse all three as
  equivalent causal or PGT-M-eligible genes.
- **DMD:** row 1436, Duchenne muscular dystrophy, MIM 310200. ClinVar line 2126 and
  HPO line 6273 both map DMD. Its symbol is already present in the register title.
- **FMR1:** row 826, fragile X syndrome, MIM 300624. ClinVar line 2862 and HPO line
  7365 map FMR1; the gene symbol is absent from the condition title.
- **BRCA2:** row 182 contains `612555, 600185`. ClinVar line 864 and HPO line 5940
  map the phenotype identifier; OMIM line 8174 maps the gene identifier. Both MIMs
  and the multiple-identifier flag must survive.
- **CHEK2:** row 332 contains `* 604373`. OMIM line 12362 is a gene entry mapping
  CHEK2. This tests the gene-MIM route without treating OMIM's gene table as a
  phenotype-to-gene table.
- **PAH:** row 1675, phenylketonuria, MIM 261600. ClinVar line 5711 maps PAH and
  line 12260 lists QDPR in `RelatedGenes`; HPO line 2852 maps only PAH. The audit
  requires both candidate associations and a visible disagreement warning. It
  does not resolve QDPR's clinical interpretation or eligibility.
- **CHIME:** row 369 publishes `28000`, a five-digit identifier. The row remains
  visible and unmapped, with `malformed-mim-length`; it is not silently corrected.
- **SIX2:** row 1873 has no OMIM cell. A condition-text search retrieves it, but no
  gene mapping is invented from its name; `no-omim-cell` remains visible.
- **No-match:** `__AUDIT_NO_SUCH_GENE_20261023__` returns zero rows and explicitly
  suggests the condition name, OMIM number or live register. This synthetic token
  is not evidence about any real gene or family's eligibility.

Only the named target row for each positive query is adjudicated. Extra rows returned
by broad gene queries are reported in JSON but are not assessed as clinically right
or wrong. The three literal-title hits are DMD, BRCA2 and CHEK2. The alias task and
three other edge tasks are excluded from the seven-query comparison denominator.

## Authority, provenance and limits

The pinned source files are the [HFEA workbook dated 5 August 2026](https://www.hfea.gov.uk/media/ssapbtyc/2026-08-05-pgt-m-full-approved-condition-list.xlsx),
[ClinVar gene-condition mappings](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/gene_condition_source_id),
[HPO gene-disease associations](https://purl.obolibrary.org/obo/hp/hpoa/genes_to_disease.txt)
and [OMIM gene-identifier mappings](https://omim.org/static/omim/data/mim2gene.txt).
Their complete SHA-256 hashes, exact record text and locators are in the evidence
JSON. The mapping files were retained on 29 August 2026; filesystem dates do not
establish a source's publication or currentness. Consult the [live HFEA register](https://www.hfea.gov.uk/pgt-m-conditions/)
for current condition status.

**Shared-source limitation:** these snapshots also feed the builder. Reading their
original records independently of the code makes transcription and retrieval
checkable; it does not make the underlying biology independently true. ClinVar and
HPO can inherit common upstream evidence. A union of source associations must not
be promoted into a list of validated causal genes or approvals for every variant.

Separate NIH/NCI pages were read on 23 October to corroborate the selected links
for [BUB1B/MVA1](https://medlineplus.gov/genetics/condition/mosaic-variegated-aneuploidy-syndrome/),
[CFTR/cystic fibrosis](https://medlineplus.gov/genetics/condition/cystic-fibrosis/),
[DMD/Duchenne muscular dystrophy](https://medlineplus.gov/genetics/condition/duchenne-and-becker-muscular-dystrophy/),
[FMR1/fragile X](https://medlineplus.gov/genetics/condition/fragile-x-syndrome/),
[BRCA2/breast-ovarian cancer susceptibility](https://www.cancer.gov/about-cancer/causes-prevention/genetics/brca-fact-sheet)
and [PAH/phenylketonuria](https://medlineplus.gov/genetics/condition/phenylketonuria/).
These are authoritative corroborating pages outside the builder inputs, not six
independent experimental datasets. No separate corroborating page was adjudicated
for CHEK2, the extra CFTR associations, QDPR, or the unresolved rows. The web pages
were not downloaded or hashed; their inspection is a manual provenance record,
not part of offline integrity verification.

## Reproduction and deliberate failures

From the repository root:

```sh
python3 tools/pgtm/audit.py
python3 -m unittest discover -s tests -p 'test_pgtm_audit.py' -v
```

The audit uses Python standard-library code plus Node.js to execute the **actual
shipped JavaScript search function** with a minimal DOM adapter. It checks returned
rows, source evidence and emitted warning text. It does not test browser layout,
accessibility, user comprehension or a clinical workflow. Missing Node.js is an
error, not skipped success. Exit codes: 0 = all tasks pass; 1 = task failure;
2 = inputs/integrity/runtime error. `--output` writes a machine-readable receipt.

The default validates bundled excerpts. For the stronger mode used for the recorded
result, supply the retained originals (no downloads occur):

```sh
python3 tools/pgtm/audit.py --hfea /path/to/hfea_pgtm_2026-08-05.xlsx --source-dir /path/to/crosswalk-sources --output /path/to/result.json
```

That mode verifies all four whole-file hashes, the original workbook cells and the
complete set of mapping records for the selected MIMs. The excerpts' hash is pinned
in the task manifest. This detects accidental missing/changed evidence; it is not
protection against someone rewriting the test expectations and all trust anchors.

All eight audit regression tests passed. The negative tests demonstrate rejection
of jointly corrupted CSV/HTML data despite their mutual consistency, missing or
altered evidence, a deleted QDPR record even after its excerpt hash is updated,
an altered original-source hash, a missing JavaScript runtime, renamed ClinVar
`RelatedGenes`, and partial ClinVar/HPO records after a valid BUB1B control row.

The last two cases reproduce a concrete builder defect: previously a renamed column
or a partial row silently removed associations while the BUB1B positive control
still passed. Required headers, duplicate headers and row widths are now checked.
A correctly delimited file truncated between rows still requires source-integrity
checking; the parser cannot infer what rows are absent. Rebuilding with the repaired
parser against the intact snapshots produced byte-identical CSV and gene-index
outputs. No clinical mappings or existing submission artifacts were changed.
