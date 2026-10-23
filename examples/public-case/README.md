# Public FGFR2 computational fixtures

**The August job YAML is missing and has not been recovered.** `job-template.yml`
is a new reconstruction from Exomiser 15.1.0's distributed
`pfeiffer-job-phenopacket.yml`. The two jobs frozen on 23 October 2026 are new
executions of that reconstruction. The batch completed on **23 October 2026 at
22:48:52 UTC**, exit 0, in **200.478 seconds including startup**. FGFR2 ranked first
without a tie among **2** mini-case genes and **471** genome-case genes. Its combined
scores were 0.9646647592821711 and 0.9654084759164547, respectively. These equal the
retained FGFR2 scores, while the historical gene counts remain **3** and **649**.
The genome spike is explicitly marked as contributing under autosomal dominant
inheritance; the same allele's contribution field is absent in the mini result.
Both records are whitelisted and passed filters. Preparation and export helpers
do not execute Exomiser; the completed execution is retained separately.

`historical-result-summary.json` contains retained August results and their source
hashes: FGFR2 first among 3 mini-case gene records and 649 genome-case gene records.
The summary bundles top rows, not every historical score. Historical and newly
executed ranks must remain separate even if they happen to agree.

Both are constructed known-variant execution controls. The HPO profile is specific,
FGFR2 is already known to the knowledge sources, and the background is not clinically
adjudicated as negative. They do not measure blinded diagnostic accuracy, novel-gene
discovery or therapeutic benefit. This reconstruction retains the runtime's default
ClinVar whitelist behavior; it is separate from the twelve-case public benchmark,
which explicitly disables that bypass.

## Inputs and what equality means

The unchanged `prepare.py` and `clinvar-smoke-variants.tsv` generate the 126-variant
mini-case with synthetic `0/1` genotypes. The genome fixture preserves the public
HG002 background's original genotypes and adds one synthetic FGFR2 heterozygote.

The only accepted background is the [official GIAB HG002 v4.2.1 GRCh38 autosomal
benchmark VCF](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NISTv4.2.1/GRCh38/HG002_GRCh38_1_22_v4.2.1_benchmark.vcf.gz).
The official directory listing and a bounded `curl --head` request confirmed this
link on 23 October 2026 UTC (HTTP 200; 156,252,944 bytes). The local original is named
`HG002.vcf.gz`; renaming does not change its required SHA-256:

```text
background: adb4d4a50048aa13353a06b84fcfcbca09a5d17525efaa4cea44f8822e81175c
historical spike-in: b31aaad49f8af6ad8522df5931fccc141152f13b8ad6e823f5807ad90e71f745
```

The full inserted VCF record is:

```text
chr10	121517378	.	C	T	500	PASS	.	GT:PS:DP:ADALL:AD:GQ	0/1:.:93:2,56:2,38:99
```

**The inserted QUAL, DP, ADALL, AD and GQ values are synthetic fixture fields, not
patient measurements, observed HG002 read support or evidence for the allele.**
The inserted GT is also constructed. Existing HG002 background GT strings,
including phase separators, are preserved. The GRCh38 reference base at this
position was independently checked as `C` with `samtools faidx` during preparation.

The retained historical header records `bcftools concat -a -Ou HG002.vcf.gz
spike.vcf.gz`; sorting afterward is an inference, not a recovered command.
The separate parent audit of the historical input compared all **4,048,342**
background coordinate/REF/ALT/literal phased-GT strings and found exactly one extra
record, the spike above. Total records are therefore **4,048,343**. This is the
measured input count; it must not be replaced by older prose counts.

`reconstruct.py` streams the source plus the spike directly to bcftools BGZF output,
without an uncompressed genome, a second compressed temporary genome or sort
scratch files. It checks sorting, every background coordinate/REF/ALT/GT, the exact
spike record and its multiplicity. Headers, compression, dates and non-GT FORMAT
serialization need not be byte-identical. In particular bcftools can add PASS and
version/command headers and fill an omitted trailing FORMAT PS value with `.`.
A raw-line diff is not a biological mismatch. The helper reports raw-line
differences separately; its semantic equality claim excludes other FORMAT values.
`--historical-genome` additionally compares every ordered coordinate/REF/ALT/GT
against the exact retained historical file, without claiming to recover its YAML.

## Prepare a portable new run

From the repository root, use Python 3.11+, bcftools (tested with 1.24), and the
PyYAML dependency pinned in `examples/public-benchmark/requirements-runtime.txt`.
Reuse an existing exact-hash public download when available. Otherwise download
the linked VCF to a new location on a sufficiently large disk; the helper rejects
any other byte hash. No network request or automatic download occurs in the helper.
Allow about 150 MiB for the rebuilt compressed genome plus its index; the original
download is referenced without copying. Keep these public genomes outside Git.

```sh
python3 examples/public-case/reconstruct.py \
  --background /path/to/HG002.vcf.gz \
  --out /path/to/NEW-fgfr2-work \
  --data-dir /path/to/verified-exomiser-data \
  --historical-genome /optional/path/to/retained/HG002_spiked.vcf.gz
```

Omit `--historical-genome` when the retained file is unavailable. For a repeat that
already has a rebuilt genome, `--reuse-genome /path/to/HG002_spiked.vcf.gz` verifies
every background allele/GT and the synthetic spike again, then references that
file without another large copy. The pinned original background is still required.
An existing destination, even from a failed preparation, is refused. Failures retain
their partial work and error receipt; choose a fresh directory for a retry.

Preparation retains the exact two jobs, batch, runtime properties, pre-inference
protocol, command/version records, input/output hashes and semantic-audit receipt.
Each Exomiser 15.1.0 batch line is literal `--analysis /path/to/job.yml`, without
`analyse` or quotes. Its `BatchFileReader` splits on whitespace and does not parse
shell quoting. The helper rejects output/job paths containing whitespace or either
quote character before creating files. Choose a work directory without those
characters, including in its parent directories. The parent confirmed the command
form against the distributed `test-analysis-batch-commands.txt` and the parser
behavior through `javap`, after two rejected dry-runs before inference. Corrections
and failed dry-run evidence remain preserved; job YAML and input hashes did not
change. The separate external `final-recipe` retains its own invocation-fix evidence.
The mini helper also writes its usual standalone job; only `jobs/mini.yml` and
`jobs/genome.yml` belong to the two-job batch. The generated jobs were checked
against the already queued jobs and match after only input/output path substitution.
The copied phenopacket metadata dates/ontology label come from the distributed
template; they are not the execution date or a measurement of bundle contents.

For this local task the untouched frozen queue is
`pipeline/work/exomiser-reconstruction-20261023` in the outer workspace. Its genome
job references the exact historical input. The separate external input check is at
`/Volumes/easystore/MVA-public-exomiser-2512/runs/reconstruction-input-check`.
The check creates no inference result and does not replace the queue.

## Execute only after verified database extraction

Use Exomiser 15.1.0, a compatible Java runtime and the verified 2512 hg38/phenotype
bundles. Wait for extraction **and readback verification**, not just a completed
download. The common runner records receipts; it does not itself certify bundle
extraction. Keep both data receipts and the Java/JAR/library installation for export.
Run this only for the intended new work directory; do not launch a duplicate of the
already queued batch.

```sh
python3 examples/public-benchmark/run.py \
  --work /path/to/NEW-fgfr2-work \
  --java /path/to/java \
  --jar /path/to/exomiser-cli-15.1.0.jar \
  --properties /path/to/NEW-fgfr2-work/runtime.properties \
  --data-receipt /path/to/hg38-extraction-receipt.json \
  --data-receipt /path/to/phenotype-extraction-receipt.json
```

## Export only completed results

Use the dedicated exporter below, also for the existing two-job frozen queue. It
does not run inference or modify the source work directory. Missing, failed,
running, incomplete or hash-mismatched executions are refused before creating the
export directory. Source inputs, jobs, result JSONL, runtime properties, batch,
execution log, runner/evaluator, software and data receipts must still be available
and agree with the execution receipt. A rebuilt genome also needs its preparation
receipt and original exact-hash background. An existing export is never overwritten.

```sh
python3 examples/public-case/export_reconstruction.py \
  --work /path/to/completed-fgfr2-work \
  --out /path/to/NEW-compact-fgfr2-export
```

The compact package retains exact executed jobs/configuration/batch/log, execution
and database receipts, source hashes, recipe files, every scored gene's
full-precision combined/phenotype/variant scores and p-value, exact-score tie rank
intervals, FGFR2 spike contribution/filter diagnostics and a historical-versus-new
comparison. A missing FGFR2 gene remains `not_scored`; no successful rank is invented.
All compact files receive new hashes. Genome VCFs, databases, JARs and full raw JSONL
remain at their source locations; their hashes are retained. Individual copied files
are capped at 32 MiB and total copied artifacts at 128 MiB.
Available dry-run logs and superseded batch files are retained as separately hashed
invocation evidence; the execution binding applies to the actual executed batch.

The generic evaluator's conservative tie-ranking function is reused, without its
unrelated multi-case benchmark denominator or interpretation. Before these new
executions, the common runner was extended to bind the protocol and any preparation
receipt in `execution.design_records`, retaining each file's SHA-256 and JSON
content. When that mapping is present, the exporter requires matching membership,
hashes and content. Older receipts without it retain clearly labelled current
snapshots; no execution-time binding is asserted for those. Binding is provenance,
not independent proof of preregistration. Retained database receipts are not a new
readback of the bundles. Differences from August can reflect changed configuration
or annotation; they are not a controlled performance improvement or deterioration.

## Verify an extracted ZIP offline

The exporter includes a standalone, standard-library-only verifier at the package
root. After extracting a compact export ZIP into a clean directory, run:

```sh
python3 /path/to/extracted-export/verify_reconstruction.py \
  --export /path/to/extracted-export
python3 /path/to/extracted-export/test_verify_reconstruction.py
```

It requires no original work directory, genomes, Exomiser, database or PyYAML. It
checks the exact package member set and every member hash; binds copied jobs,
configuration, batch, log, code, design records and database receipts to the
execution receipt; and independently recomputes every gene's tie interval and
each FGFR2 result from the complete gene-score TSVs. The historical/new comparison
must match those recomputed results and the retained historical summary. Changing
a reported rank and updating its member hash still fails these consistency checks.

This is offline consistency verification, not proof of authenticity: the manifest
is unsigned, and omitted raw JSONL/genomes/software/databases cannot be rehashed
from the compact package. In particular, the full TSV's derivation from raw JSONL
is verified by the source exporter, not independently proved by this offline check.
