# Public Exomiser controls: historical runs and completed reconstruction

**Historical runs: August 2026. New reconstructed batch completed 23 October 2026, 22:48:52 UTC.**

These constructed public cases test execution and ranking at different input sizes. They do not validate the child's diagnosis or estimate diagnostic sensitivity and specificity. No hackathon data is used in either case.

## Small public fixture

The retained input contains 126 ClinVar GRCh38 variants: six pathogenic FGFR2 variants and 120 benign-labelled decoys in large genes. All genotypes are constructed heterozygotes. Six Pfeiffer-syndrome HPO terms provide a specific phenotype. Exomiser 15.1.0 ranked FGFR2 first of three scored genes, with combined score 0.964664759, phenotype score 0.859871439 and variant score 1.0. The earlier report recorded 90 variants surviving filtering and 5.2 seconds after startup. These timings are historical machine-specific observations. **[OUR MEASUREMENT]**

The [public fixture](../examples/public-case/README.md) ships the TSV, preparation recipe and retained historical summary. A new reconstruction has now executed successfully, as reported separately below. **The original August job YAML was not retained and has not been recovered.** A completed reconstruction does not establish exact historical replay.

## Genome-scale spike-in

A public GIAB HG002 GRCh38 v4.2.1 benchmark VCF contained 4,048,342 records. A heterozygous FGFR2 chr10:121517378 C>T spike brought that to 4,048,343 records. The run processed 4,096,123 normalized variants, retained 22,644 after the coding-effect filter, 1,625 after frequency filtering and 1,123 after inheritance filtering. The retained result contains **649 scored gene records**. **[OUR MEASUREMENT — August run records and retained result, recounted 23 October]**

FGFR2 ranked first: combined score 0.965408476, phenotype score 0.859871439 and variant score 1.0. KRT17 followed at combined score approximately 0.3954. The recorded runtime was 9 minutes 20 seconds on a laptop using an external database volume. It is not a hardware-independent performance benchmark. The [packaged summary](../examples/public-case/historical-result-summary.json) preserves leading scores and hashes of the original result files.

The result includes contributions from REVEL, MVP, ALPHA_MISSENSE and precomputed SPLICE_AI annotations. This is distinct from running the SpliceAI model directly, which is documented in the [canary](../canary/README.md). The whole-genome job YAML was not retained, so the result does not establish an exact rerun recipe.

## New reconstructed execution: measured separately

The two-job batch ran Exomiser 15.1.0 with the 2512 GRCh38 and phenotype bundles and OpenJDK 21.0.12.1. It started at 22:45:32 UTC and completed at 22:48:52 UTC on 23 October 2026, exit 0, with both expected outputs present. The retained wrapper measured **200.4780619580015 seconds for the whole batch including startup**. That interval is not directly comparable with the historical single-case timings above. Exact jobs, runtime properties, Java/software/input/output hashes, database receipts, execution log and pre-inference protocol/addenda are in the [compact execution package](../examples/public-case/reconstructed-results/execution.json). **[OUR MEASUREMENT]**

- **Mini:** FGFR2 rank **1 of 2** scored genes, exact tie interval **[1, 1]**, combined score **0.9646647592821711**. The historical result was rank **1 of 3**, with the same retained FGFR2 combined score.
- **Genome:** FGFR2 rank **1 of 471** scored genes, exact tie interval **[1, 1]**, combined score **0.9654084759164547**. The historical result was rank **1 of 649**, with the same retained FGFR2 combined score.

In both new cases the FGFR2 phenotype score is **0.8598714392999345** and variant score is **1.0**. Every new scored gene is retained, not just leading candidates: [mini scores](../examples/public-case/reconstructed-results/gene-scores/mini.tsv), [genome scores](../examples/public-case/reconstructed-results/gene-scores/genome.tsv). The [machine-readable historical/new comparison](../examples/public-case/reconstructed-results/historical-vs-reconstructed.json) preserves both denominators. Matching FGFR2 scores do not imply matching complete results or recovery of the missing August configuration. **[OUR MEASUREMENT; interpretation is OUR INFERENCE]**

The new genome execution log separately reports **4,048,343 input records → 4,096,123 single-allele variants**, then **22,644** passing the effect filter, **1,253** passing frequency filtering and **794** passing inheritance filtering. These are the **new** counts; the August values of **1,625**, **1,123** and **649 scored genes** above remain historical observations. We have not isolated a cause for the difference, and do not describe it as an improvement in accuracy. **[OUR MEASUREMENT; causal explanation not established]**

### Input identity and spike contribution

The executed genome uses the retained public spike-in with SHA-256 `b31aaad49f8af6ad8522df5931fccc141152f13b8ad6e823f5807ad90e71f745`. A separate complete comparison against the exact public HG002 source established equality of all **4,048,342 background coordinate/REF/ALT/literal phased-GT strings**, plus exactly one added `chr10:121517378 C>T 0/1` record. The portable recipe independently rebuilt that semantic input and verified it against the retained file. This is semantic equality: compression, headers and serialization of omitted FORMAT values can differ. It is not a claim of original YAML recovery. **[OUR MEASUREMENT; recipe and pinned source hash in the public fixture README]**

The inserted record's QUAL **500**, DP **93**, ADALL **2,56**, AD **2,38** and GQ **99** are **synthetic fixture fields, not patient measurements or observed HG002 support for that allele**. Its heterozygous genotype is constructed; background genotypes are preserved. The mini-case genotypes and QUAL values are also constructed. No read-support or allele-balance inference should be drawn from these inserted values.

The [exact-coordinate output audit](../examples/public-case/reconstructed-results/source-variant-audit.json) finds this allele once within FGFR2 in each new output. Both records are `PASSED`, `whiteListed: true`, with variant score **1.0**. In the **genome** result, `contributesToGeneScore: true` and `contributingInheritanceModes: [AUTOSOMAL_DOMINANT]` explicitly support contribution by the spike. In the **mini** result, those contribution fields are absent in the source JSONL and preserved as `null` in the compact audit. The allele is present, but the mini gene rank must not be attributed to that allele alone. An absent serialized field is not an absent variant. **[OUR MEASUREMENT]**

The reconstruction leaves ClinVar whitelist behavior at the runtime default. The observed whitelist flags are a material knowledge-leakage limitation; these cases are execution controls, not a test of discovering an unknown causal variant. This differs from the separate multi-case benchmark's explicit whitelist-disable setting.

### Portable package and offline verification

The [fresh compact ZIP](../examples/public-case/reconstructed-results.zip) is **80,997 bytes**, SHA-256 `dd9e3f5c927beaeda5bef10ccb4889ad6c162952ab63a17f804e638e4e9951eb`. Recipe/code files were hash-frozen before export and remained unchanged through verification. Original and failed batch-invocation evidence is retained: the correct batch line is literal `--analysis /path/to/job.yml`, without an `analyse` prefix or shell quoting. Those invocation-only fixes preceded inference and did not change job YAML or input data.

A fresh extraction passed the packaged standalone verifier: **35 hashed members**, both FGFR2 results, every gene's score/tie interval, copied job/configuration hashes and execution/design/database receipt bindings. A restricted file-access check allowed reads only within the extracted package, so this verification did not require original filesystem paths. All **8** packaged offline tests passed, including absent-source verification and rejection of altered reported or TSV ranks even after their member hashes were updated. [Verification receipt](../examples/public-case/reconstructed-results-verification.json). **[OUR MEASUREMENT]**

The compact package omits whole genomes, databases, software binaries and full raw JSONL, retaining their recorded hashes. Its verifier checks package consistency and rank arithmetic; it cannot independently regenerate the TSV from omitted raw JSONL or authenticate an unsigned manifest. The source exporter verified the raw-output hashes before deriving the complete gene-score TSVs. Neither test passes nor offline integrity establish clinical validity.

## What these results establish

The historical genome-scale run and the newly declared reconstruction completed, and both ranked FGFR2 first. The new genome result explicitly marks the intended spike as contributing. This demonstrates execution at that scale under the recorded conditions. The following limits are interpretive rather than measured accuracy results. **[OUR INFERENCE]** It does not establish:

- General diagnostic performance, performance with noisy or sparse phenotypes, or performance on novel variants.
- That HG002's other genes are clinically true-negative controls.
- Freedom from knowledge leakage: the spike is a known pathogenic ClinVar variant and the bundle incorporates prior knowledge. Score decomposition cannot rule this out.
- Biological truth, phase or treatment responsiveness for the BUB1B findings. **[OUR INFERENCE]**

Broader evaluation requires independently selected phenotypes and variants, explicit leakage controls and reporting of failures as well as recovered answers. The separate multi-case evaluation has its own protocol and results; its cases must not be pooled with these known-FGFR2 controls to claim diagnostic accuracy. The historical missing configuration remains a limitation even though the new reconstruction now has an executed, inspectable recipe and verified compact outputs.
