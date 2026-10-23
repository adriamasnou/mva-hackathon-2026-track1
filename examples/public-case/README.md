# Public computational fixture

`clinvar-smoke-variants.tsv` preserves the 126 public ClinVar variants used in the August 2026 mini-case. Genotypes are constructed heterozygotes, not a person's genotype. The historical output summary is extracted from retained Exomiser results and includes their SHA-256 hashes.

The original job configuration was not retained. `job-template.yml` is a **new reconstruction**, based on Exomiser 15.1.0's distributed `pfeiffer-job-phenopacket.yml`. Its preparation is tested, but its inference has **not** been rerun with the required database. It must not be presented as an exact replay of the old run. Database versions and changing annotations can change results.

```sh
python3 examples/public-case/prepare.py --out-dir /path/to/new-work-directory
java -Xmx6g -Dexomiser.data-directory=/path/to/exomiser-data \
  -Dexomiser.hg38.data-version=2512 -Dexomiser.phenotype.data-version=2512 \
  -jar /path/to/exomiser-cli-15.1.0.jar analyse \
  --analysis /path/to/new-work-directory/reconstructed-job.yml
```

The second command requires Java and Exomiser's matching GRCh38 and phenotype bundles. It is not part of the lightweight offline tests. The currently attached machine does not have the volume containing the variant bundle mounted. A completed re-execution must retain the job, versions, input/output hashes, logs and all resulting ranks.

The genome-scale HG002 spike-in is a separate historical run. The supplied summary contains 649 scored gene records, with FGFR2 first. The genome and full result are not bundled. Neither constructed case is a diagnostic benchmark: the pathogenic FGFR2 variants are already known to the underlying knowledge sources, phenotypes are specific, and the background is not clinically adjudicated as negative.
