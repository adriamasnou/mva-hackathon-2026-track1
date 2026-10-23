# Danis Phenopacket Store: supplementary review

Reviewed 2026-10-23 UTC. PMID **39394689**, PMCID **PMC11564936**, DOI [10.1016/j.xhgg.2024.100371](https://doi.org/10.1016/j.xhgg.2024.100371). This closes the previously recorded unread supplementary-figure gap for the source-method paper. It does not expand the scientific reading claim to every record or underlying publication in Phenopacket Store.

The [machine-readable sidecar](danis-supplement-review.json) retains the exact source inventory, hashes, page coverage, render comparisons, claim checks and frozen-input checks. No benchmark results were accessed and no inference was run. The frozen selection, phenotype arms, source-support groups and shared reading ledger were not edited.

## Source and exact coverage

The held main PDF is `papers-local/danis2025_hggadv_phenopacket_store.pdf`, SHA-256 `0b77a9a3f349bf320816719f3b0f75a0eb07e005ba3b56aad06ab6437fe26f7a`. The existing parent record covers its repository cover and seven article pages, including both main figures and Table 1. This task rechecked relevant methods/discussion passages; it does not claim a second independent complete main-text review.

The [official article XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11564936/fullTextXML) identifies exactly two supplementary documents. Both were obtained from the [official Europe PMC supplementary archive](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11564936/supplementaryFiles), with their XML-listed member names preserved. The PMC browser route returned a challenge, the Cell page returned 403, and a direct PMC `bin/mmc1.pdf` attempt returned 404; none of those failed routes is represented as a successful download.

Retained sources are under `papers-local/supplementary/danis2025_phenopacket_store/`:

- **Document S1, `mmc1.pdf`**: 76,297 bytes; SHA-256 `761acf891eec625cf9b2641c010214efcd6eb5a42a925b8ab301a93ec87dca24`. All three PDF pages read visually and textually: cover/title/authors; Figure S1's complete JSON representation and caption (printed p.1); Figure S2's complete JSON representation and caption (printed p.2).
- **Document S2, `mmc2.pdf`**: 1,949,704 bytes; SHA-256 `dd8d3795e14d232935cf071524aab57be39bd2dc13ba7307c365706c25492d48`. This is the combined article plus supplement. PDF pp.1–7 reproduce the held main PDF pp.2–8; pp.8–10 reproduce Document S1 pp.1–3. Every paired page rendered to identical PNG bytes using `pdftoppm -png -scale-to 1600`. Extracted text also matches. This establishes duplication at the checked text/render level; it is not a claim that the PDFs themselves have identical bytes. The supplement is counted once, and the earlier main-reading attribution is preserved.
- **Official asset ZIP**: 2,317,135 bytes; SHA-256 `788320b85669a82bcd93df5173d3e165611d9a177a1934369407321b973ab3f9`. Its six members are `mmc1.pdf`, `mmc2.pdf`, and GIF/JPEG renditions of main Figures 1 and 2. It contains no separate supplementary case table or additional explanatory document.
- **Official XML**: 94,263 bytes; SHA-256 `254394dbebded82660b4d76a98dd98e1d388ea0b38e7aa89764065ee0c1b4062`. This retains the article identity, supplementary captions and media references. Layout-text extractions and the six supplementary page renders are retained beside the PDFs; their hashes are in the JSON.

## What the supplementary figures establish

**Figure S1** illustrates a single-nucleotide variant representation for PAX3 in a Waardenburg syndrome type 3 record. It contains `SOLVED` and `CAUSATIVE`, HGNC:8617, `hg38`, chr2:222297048 G>A, and GENO:0000136 / homozygous. Both transcript and genomic HGVS expressions are included. The caption describes pyphetools using VariantValidator to derive gene, genomic HGVS and VCF-like information from HGVS input. This supports the interpretation of these fields by the frozen eligibility parser. It does not establish clinical validity merely because those fields are present.

**Figure S2** illustrates an ITPR1 deletion recorded as `DEL423kb`, with SO:1000029 / chromosomal_deletion and GENO:0000135 / heterozygous. It supplies neither an explicit VCF record nor exact breakpoints. The caption explains the qualitative representation of structural variants, using a size boundary of at least 50 nucleotides. This supports excluding such entries from a procedure that requires exact small-variant alleles. The main article's SLC9A3 deletion example is a different case; it must not be conflated with this ITPR1 figure.

Neither figure establishes trans phase for two heterozygous variants or validates an inheritance classification. Hemizygous GENO:0000134 is not illustrated. This review therefore adds no independent evidence for that ontology mapping, the X-case source assertions, or phase. The local design's genotype strata and explicit unphased encoding remain the appropriate description.

## Check against the frozen twelve-case design

The main article reports release 0.1.19 with 6,668 phenopackets, 475 diseases, 423 genes, 3,834 distinct variants and 959 publications (pp.1–2, Table 1; release statement p.5). These are corpus descriptions, not performance results or counts for our selected sample. The frozen plan pins the same release and archive hash.

The individual-level inclusion policy and exclusion of aggregate-only reports are explicit on main p.2. The format-QC discussion on p.3 and the worked supplementary examples support computational parsing. They do not guarantee that every phenotype was attributed to the correct individual or that every source diagnosis is sound. Thus this review does not override the existing ZIC3, OFD1, PAX4, MTOR, BCKDHB or other case-specific qualifications or change any source-support group.

The small-variant representation in S1 and the qualitative deletion in S2 support the frozen filter's requirement for explicit hg38 REF/ALT records. They do not supply the local choices of twelve cases, one gene per case, one or two variants, at least three positive HPO terms, genotype quotas, FGFR2/BUB1B exclusions, deterministic seed or four phenotype arms. Those choices belong to `selection-plan.json` and `prepare.py`; they should not be attributed to validation by Danis.

The discussion on main p.4 explicitly proposes simulations that spike reported causal variants into population-representative VCFs. This supports the general simulation approach. It does not make a causal-only VCF a genome-wide diagnostic evaluation, and does not establish clinical generalisation from our small selected set.

The PMID/individual-ID discussion on p.3 warns that a person can appear in multiple publications; a unique PMID-prefixed record ID does not resolve all person-level duplication. The discussion also describes Monarch's use of phenopackets in HPO annotation. Possible knowledge leakage remains a justified design caveat, but this review does not demonstrate leakage for any selected case or runtime.

## Coverage boundary and Kepler handoff

No unique supplementary explanatory page or figure remains unread among the two documents enumerated in the official article XML. This is a complete review of **two representation examples and their captions**, not all-record scientific interpretation of the 6,668-case bank. Raw parsing, archive inventory and checksum checks are not clinical adjudication. No original clinical publication underlying these two examples was independently re-adjudicated here, and no existing individual-paper reading gap is closed by this supplement review.

Before/after SHA-256 checks matched for all **31** files under `repo/examples/public-benchmark/source-selection/`, including the frozen selection and source-support records. Full file hashes are retained in the JSON; no source regeneration was performed.

For Kepler's ledger integration: preserve the existing main-text review attribution; replace “Supplementary S1/S2 not read” with the exact Document S1 and duplicate Document S2 coverage above; retain the corpus-versus-case-review boundary and all individual-source limitations. The shared ledger is untouched. Direct delivery to Kepler is not claimed: this session exposes no Kepler thread or subagent messaging route. These sidecars are ready for the parent to relay.
