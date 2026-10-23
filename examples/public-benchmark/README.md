# Public Exomiser evaluation recipe

This recipe constructs literature-derived variant/phenotype cases on public GIAB backgrounds. It tests execution, source-label recovery and sensitivity to altered phenotype inputs. These are **semi-synthetic cases, not independent diseased genomes or a clinical accuracy study**. No MVA input is used.

The frozen source selection uses Phenopacket Store 0.1.19, excludes BUB1B and the previous FGFR2 example, and samples twelve different genes across prespecified genotype patterns. The source labels are evaluation keys, never candidate-gene or disease hints supplied to Exomiser. PAX4 is disputed causal truth; ZIC3/OFD1 are limited technical cases because the backgrounds contain no chromosome X. All cases remain visible. Consult the accompanying source adjudication before interpreting recovery.

## Prepare and run

Required software: Exomiser 15.1.0, its matching 2512 hg38/phenotype bundles, a supported Java runtime, Python, bcftools and the pinned preparation dependency in `requirements-runtime.txt`. Preparation below uses bcftools 1.24 and PyYAML 6.0.3. Lightweight unit tests do not require these runtimes or any patient data.

```sh
python3 examples/public-benchmark/prepare.py \
  --cases /path/to/frozen-cases.json \
  --background /path/to/public-HG002-or-HG001.vcf.gz \
  --gff /path/to/Homo_sapiens.GRCh38.116.gff3.gz \
  --template examples/public-case/job-template.yml \
  --out /path/to/new-work
```

Use each public GIAB v4.2.1 GRCh38 autosomal benchmark VCF with its matching index. These historical versions are deliberately pinned, not described as the latest GIAB release. Preparation takes **all** canonical autosomal exons in Ensembl 116, across transcripts and biotypes, plus 20-base flanks; it does not select only disease genes. It splits multiallelic background records, keeps their observed genotypes, removes conflicting records at each spike position and inserts the frozen source allele/genotype. Every replacement is recorded. Splitting is not a claim of reference-based left normalization. Causal REF strings were checked separately against GRCh38.

Create a retained properties file pointing at the verified bundles:

```properties
exomiser.data-directory=/path/to/exomiser-data
exomiser.hg38.data-version=2512
exomiser.phenotype.data-version=2512
exomiser.hg38.use-clinvar-white-list=false
spring.cache.type=caffeine
spring.cache.caffeine.spec=maximumSize=60000
logging.level.com.zaxxer.hikari=ERROR
```

The explicit whitelist setting prevents the default ClinVar filter bypass. It does **not** remove all ClinVar annotations, predictor training information or HPO/OMIM knowledge of the published cases. No temporal holdout or novel-gene performance is established. The separate reconstruction of the historical FGFR2 runs retains its own configuration and must not be conflated with this evaluation.

```sh
python3 examples/public-benchmark/run.py \
  --work /path/to/new-work \
  --java /path/to/java \
  --jar /path/to/exomiser-cli-15.1.0.jar \
  --properties /path/to/new-work/runtime.properties \
  --data-receipt /path/to/hg38-extraction-receipt.json \
  --data-receipt /path/to/phenotype-extraction-receipt.json
python3 examples/public-benchmark/evaluate.py --work /path/to/new-work
```

Data receipts must describe the independently verified local extraction. The runner records them; it does not replace the extraction/hash verification. It checks frozen input hashes, refuses existing results, retains the exact command, Java and library versions/hashes, logs, exit status, runtime and result hashes. A failure requires a new documented run, not overwritten evidence.

## Comparisons and limitations

Each case has four fixed arms: original positive HPO terms, a seeded half retained, a seeded other-case profile, and no HPO. The first three change only the phenotype list. The no-HPO arm also removes `hiPhivePrioritiser`; its OMIM inheritance prior remains. No arm represents a healthy or genuinely unsolved person, and swapped profiles can share features with the source case.

Top-1/5/10 recovery uses the **worst rank in an exact-score tie**. Missing outputs, execution failures and unscored source genes stay in the denominator. Report per-background results and paired recovery on both backgrounds; two backgrounds do not double the number of independent disease cases. Gene recovery does not establish that every causal allele was retained or correctly phased.

The pre-inference protocols, source-selection receipt and later execution/evaluation records are separate artifacts. Changes made before inference—including disabling the whitelist and adding the second public background—are dated addenda, not retrospective edits disguised as an original plan. The final report must state which analyses actually completed.

```sh
python3 -m unittest discover -s tests -p test_public_benchmark.py -v
```

These tests exercise splice construction, background selection, conservative ties, failed-run denominators, malformed scores and changed-input rejection. Passing them is not executing Exomiser.
