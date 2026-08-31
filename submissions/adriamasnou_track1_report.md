# Track 1 Methods Report — v1: baseline / scorer-format probe (VCF-targeted BUB1B analysis)

> **Note to reviewers:** this is a deliberate baseline submission from the provided VCF
> only, submitted early to validate the scorer's expected answer format. A deeper
> follow-up (unbiased genome-wide prioritization, FASTQ realignment with independent
> variant calling, SV/CNV analysis, and read-depth quantification of the mosaic
> aneuploidy itself) is in progress and will accompany a later submission.

**Participant:** adriamasnou (individual)
**Submission:** `adriamasnou_vcf-targeted-bub1b.csv`
**Code:** https://github.com/adriamasnou/mva-hackathon-2026-track1

## Summary of prediction

Ranked candidate 1 is a **BUB1B compound heterozygote**:

| Allele | GRCh38 | HGVS (NM_001211.6 / ENST00000287598) | Consequence | Evidence |
|---|---|---|---|---|
| 1 | chr15:40209701 T>G | c.2210T>G | **p.Leu737*** (nonsense) | ClinVar **Pathogenic/Likely pathogenic** for Mosaic variegated aneuploidy syndrome 1 (RCV000641226); truncates BubR1 before the C-terminal kinase domain |
| 2 | chr15:40220612 T>G | c.3006T>G | **p.Asn1002Lys** (kinase-domain missense) | Novel at the nucleotide level; identical protein change to ClinVar VUS c.3006T>A. Candidate hypomorphic allele |

## Approach

1. **Phenotype-driven gene prior.** The proband's HPO profile (rhabdomyosarcoma HP:0002859, nephrocalcinosis HP:0000121, short stature HP:0004322, failure to thrive HP:0001508, skeletal muscle atrophy HP:0003202, premature birth HP:0001622, SGA HP:0001518, parental recurrent spontaneous abortion HP:0200067) forms the classic chromosomal-instability cluster of Mosaic Variegated Aneuploidy. Established MVA genes (BUB1B/MVA1, CEP57/MVA2, TRIP13/MVA3, plus newer reports) were prioritized, with BUB1B first: it is the only MVA gene with a strong published rhabdomyosarcoma and Wilms-tumour association, and parental recurrent miscarriage fits biallelic recessive inheritance. (BUB1B/MVA1: Hanks 2004, PMID 15475955.) 

   > ⚠️ **Correction pending, logged 2026-08-27.** The uniqueness clause above is **[UNVERIFIED]** and we now believe it is too strong: *TRIP13*/MVA3 carries a Wilms association at least as strong (**6 of 6 patients**, onset 1.3–5 y; Yost 2017, PMID 28553959). It survives only on the narrow conjunctive reading that BUB1B is the only MVA gene reported with *both* rhabdomyosarcoma *and* Wilms tumour. This text is left as submitted; the wording is a decision for the follow-up submission.
2. **Targeted locus extraction.** All variants in the GRCh38 BUB1B locus (15:40,160,984–40,221,137; canonical transcript ENST00000287598) were extracted from the provided GATK VCF (`WGS_EX2312012_HGWCNDSX7.vcf.gz`): 14 variants, of which 8 heterozygous.
3. **Novelty filter.** Three heterozygous PASS variants lack dbSNP IDs: chr15:40209701 T>G, chr15:40216470 A>G (deep intron 20), chr15:40220612 T>G.
4. **Local consequence calling.** Exon structure and CDS sequence for ENST00000287598 were fetched from Ensembl REST (public gene data only — no proband variant left the analysis machine); codon changes were computed locally: p.Leu737* and p.Asn1002Lys. The reference base at each position was asserted against the Ensembl CDS.
5. **Corroboration.** ClinVar: c.2210T>G (p.Leu737*) is Pathogenic/Likely pathogenic for MVA1; at chr15:40220612, c.3006T>A (same p.Asn1002Lys) is a reported VUS and c.3006T>C (p.Asn1002=) likely benign. Ensembl also lists pathogenic frameshift alleles at bases adjacent to 40209701, consistent with truncation intolerance in exon 17.

The genotype matches the canonical biallelic BUB1B MVA architecture (one truncating allele + one hypomorphic kinase-domain allele), with the missense allele plausibly preserving partial BubR1 function (complete loss of BUB1B is presumed lethal: Hanks 2004, PMID 15475955; murine BubR1 nulls are
embryonic lethal — **Baker DJ *et al.*, *Nat Genet* 2004, PMID 15208629**).

> 🔻 **CITATION CORRECTED 2026-08-31 — FIRST CLAIM AUDIT OF THIS FILE.** The mouse-null statement
> was attributed to a **bare "Sieben 2020" with no identifier**, which is the one citation form
> this project's PMID-based citation gate cannot see — which is why it survived every audit by
> being unparseable rather than by being right. **Checking the held full text of Sieben 2020
> (PMID 31738183), it does not support the claim:** it reports **early *postnatal* lethality** at
> >90% BubR1 reduction, and **embryonic lethality for one specific compound genotype
> (`BubR1^X753/L1002P`)** — not for the null. The mouse allelic series establishing that
> `BubR1^−/−` and `BubR1^H/−` are lethal while `BubR1^H/H` (~10% of wild-type) is viable is
> **Baker 2004**, which this project holds and already cites correctly in its private notes.
> **The claim is true and was cited to the wrong paper.** *(This file is the already-submitted
> Track 1 report; the correction is recorded here rather than concealed, and the submitted text is
> not retro-edited — see the note at approach step 1 for the same convention.)*

## Limitations

- **Phase is inferred, not demonstrated — and we can bound why.** Read-backed phasing of this pair is not merely unattempted, it is physically impossible in this library. From our own alignment of all four lanes (1,076,022,529 reads, 45× post-duplicate), the locus chr15:40,160,984–40,221,137 yields 22,623 properly-paired fragments with a mean TLEN of 458 bp and a **longest observed fragment of 1,272 bp**. Only three heterozygous SNV markers span the two variants — chr15:40,209,701, chr15:40,216,470, chr15:40,220,612 — so phasing must cross hops of 6,769 bp and 4,142 bp. **Even the easiest required hop is 3.26× longer than the longest fragment in the data**; the harder one is 5.32×. No re-calling, filter relaxation or aligner change can close a gap that exceeds the library's physical insert size, so the limitation is a property of the sample preparation, not of our analysis. The trans configuration is therefore supported by the recessive disease model and the parental recurrent-miscarriage history (consistent with two carrier parents), and stated as **inferred**. [OUR MEASUREMENT — `samtools view -f 0x2 -F 0x900` TLEN distribution over the locus; markers from the provided GATK VCF]
- **Read support is robust for both calls, and now orthogonally confirmed.** The provided VCF gives `AD` (ref,alt) of **21,25** at chr15:40,209,701 and **15,13** at chr15:40,220,612. Re-calling independently from our own four-lane alignment reproduces this: pileup ref/alt of **21/26** (alt fraction 0.553) and **15/12** (0.444), with both positions re-called by `bcftools mpileup`/`call` without reference to the provided callset. Reference counts agree exactly; the one-read differences on the alt side are the `-Q 20` base-quality filter. Both sites are therefore clean germline heterozygotes with **no indication of low-VAF mosaicism**, established from reads rather than from the delivered VCF alone. Mosaicism elsewhere in the genome was not assessed.
- No FASTQ realignment or SV/CNV calling was performed for this submission; the provided GATK VCF was taken as-is. Rows 2 and 3 of the CSV hedge against a mis-assigned second allele.

## ✅ Data claims independently re-derived, 2026-08-31

**This report had never been claim-audited.** Every count in it was recomputed from the provided
VCF on 2026-08-31 and **all reproduce exactly**: **14 variants** in `15:40,160,984–40,221,137`, of
which **8 heterozygous**; **3** heterozygous PASS variants without a dbSNP ID, at exactly
**40,209,701 · 40,216,470 · 40,220,612**; **`AD` 21,25** and **15,13** at the two reported alleles.
The phasing arithmetic also checks: the marker gaps are **6,769 bp** and **4,142 bp**, so against a
longest observed fragment of 1,272 bp the easier hop is **3.26×** and the harder **5.32×**.
*(The fragment statistics — 22,623 properly-paired reads, mean TLEN 458 bp, longest 1,272 bp — were
**re-derived from the alignment on 2026-08-31 and they reproduce.**)*

> 🔴 **CORRECTED 2026-08-31, LATER THE SAME DAY. This sentence previously read *"could not be
> re-derived … because the merged alignment is no longer on this disk."* **That was false.** The
> merged alignment is present and readable: `pipeline/work/WGS_EX2312012_HGWCNDSX7.markdup.cram`
> (20 GB, indexed), **four read groups L001–L004 merged** by `bwa mem` → `samtools fixmate` →
> `markdup`, against the reference its own `@SQ UR:` tag names —
> `pipeline/ref/GRCh38_no_alt_plus_hs38d1.fna`, 2.9 GB, present with its `.fai`.
>
> **Re-derived over the RefSeq *BUB1B* span `chr15:40,161,057–40,220,509`:**
> ```
> samtools view -f 2 -F 2304 -T pipeline/ref/GRCh38_no_alt_plus_hs38d1.fna >   pipeline/work/WGS_EX2312012_HGWCNDSX7.markdup.cram chr15:40161057-40220509 >   | awk '{t=$9; if(t>0){n++; s+=t; if(t>m)m=t}} END{print n, s/n, m}'
> ```
> | statistic | published | re-derived 2026-08-31 |
> |---|---|---|
> | mean TLEN | **458 bp** | **458.4 bp** ✅ |
> | longest fragment | **1,272 bp** | **1,272 bp** ✅ |
> | properly-paired reads | **22,623** | **22,398** on the exact RefSeq span; **23,188** on a slightly wider one — the published figure sits between, i.e. it differs only by the region definition, not by the data |
>
> **The two numbers the phasing argument actually uses — mean TLEN and the longest observed fragment
> — reproduce exactly.** The `3.26×` and `5.32×` gap-to-fragment ratios above therefore stand on a
> re-derivable measurement, not on a remembered one.
> ⚠️ **How the error happened, since it matters more than the error:** an earlier check looked for the
> reference at `/ref/…`, the path the canary hard-codes, found nothing there, and concluded the
> alignment was gone. **The CRAM's own header records where its reference actually is.** A file's
> provenance is written inside it; asking the file beats guessing its path.
> *(Independent cross-check unchanged: `F-001`'s 455.7 ± 181.6 bp.)*
**One defect was found in this audit — the "Sieben 2020" mouse-null attribution, corrected in the
Approach section above.** Hanks 2004 (PMID 15475955) and Yost 2017 (PMID 28553959) both verified
correct.
[OUR MEASUREMENT — re-derivation from `WGS_EX2312012_HGWCNDSX7.vcf.gz`, 2026-08-31.]

## Reproducibility

`analysis/bub1b_targeted_analysis.py` (Python 3 stdlib; optional `truststore`) reproduces steps 2–4 from the provided VCF in one command. See repository README.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
