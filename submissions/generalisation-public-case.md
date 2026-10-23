# Public Exomiser smoke tests: measured scale and limits

**Historical runs, August 2026. Reproducibility audit updated 23 October 2026.**

These constructed public cases test execution and ranking at different input sizes. They do not validate the child's diagnosis or estimate diagnostic sensitivity and specificity. No hackathon data is used in either case.

## Small public fixture

The retained input contains 126 ClinVar GRCh38 variants: six pathogenic FGFR2 variants and 120 benign-labelled decoys in large genes. All genotypes are constructed heterozygotes. Six Pfeiffer-syndrome HPO terms provide a specific phenotype. Exomiser 15.1.0 ranked FGFR2 first of three scored genes, with combined score 0.964664759, phenotype score 0.859871439 and variant score 1.0. The earlier report recorded 90 variants surviving filtering and 5.2 seconds after startup. These timings are historical machine-specific observations. **[OUR MEASUREMENT]**

The [public fixture](../examples/public-case/README.md) now ships as a TSV, a preparation script, a reconstructed job and a compact result summary. The preparation script is tested independently of Exomiser. **The reconstructed job has not been re-executed**, and is not the original configuration. The original job was not retained. Exact historical replay is therefore not established.

## Genome-scale spike-in

A public GIAB HG002 GRCh38 v4.2.1 benchmark VCF contained 4,048,342 records. A heterozygous FGFR2 chr10:121517378 C>T spike brought that to 4,048,343 records. The run processed 4,096,123 normalized variants, retained 22,644 after the coding-effect filter, 1,625 after frequency filtering and 1,123 after inheritance filtering. The retained result contains **649 scored gene records**. **[OUR MEASUREMENT — August run records and retained result, recounted 23 October]**

FGFR2 ranked first: combined score 0.965408476, phenotype score 0.859871439 and variant score 1.0. KRT17 followed at combined score approximately 0.3954. The recorded runtime was 9 minutes 20 seconds on a laptop using an external database volume. It is not a hardware-independent performance benchmark. The [packaged summary](../examples/public-case/historical-result-summary.json) preserves leading scores and hashes of the original result files.

The result includes contributions from REVEL, MVP, ALPHA_MISSENSE and precomputed SPLICE_AI annotations. This is distinct from running the SpliceAI model directly, which is documented in the [canary](../canary/README.md). The whole-genome job YAML was not retained, so the result does not establish an exact rerun recipe.

## What these results establish

The recorded genome-scale run completed and put the intended spike at the top. It demonstrates that execution at that scale. The following limits are interpretive rather than measured accuracy results. **[OUR INFERENCE]** It does not establish:

- General diagnostic performance, performance with noisy or sparse phenotypes, or performance on novel variants.
- That HG002's other genes are clinically true-negative controls.
- Freedom from knowledge leakage: the spike is a known pathogenic ClinVar variant and the bundle incorporates prior knowledge. Score decomposition cannot rule this out.
- Biological truth, phase or treatment responsiveness for the BUB1B findings. **[OUR INFERENCE]**

A useful next evaluation would freeze complete jobs and database versions, include independent phenotypes and variants, define leakage controls, and report failures as well as recovered answers. That evaluation has not been performed. The historical missing configuration remains a limitation rather than being silently replaced by a claim of full reproducibility.
