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

The genotype matches the canonical biallelic BUB1B MVA architecture (one truncating allele + one hypomorphic kinase-domain allele), with the missense allele plausibly preserving partial BubR1 function (complete loss of BUB1B is presumed lethal: Hanks 2004, PMID 15475955; murine BubR1 nulls are embryonic lethal, Sieben 2020).

## Limitations

- **Phase is inferred, not demonstrated — and we can bound why.** Read-backed phasing of this pair is not merely unattempted, it is physically impossible in this library. From our own alignment of all four lanes (1,076,022,529 reads, 45× post-duplicate), the locus chr15:40,160,984–40,221,137 yields 22,623 properly-paired fragments with a mean TLEN of 458 bp and a **longest observed fragment of 1,272 bp**. Only three heterozygous SNV markers span the two variants — chr15:40,209,701, chr15:40,216,470, chr15:40,220,612 — so phasing must cross hops of 6,769 bp and 4,142 bp. **Even the easiest required hop is 3.26× longer than the longest fragment in the data**; the harder one is 5.32×. No re-calling, filter relaxation or aligner change can close a gap that exceeds the library's physical insert size, so the limitation is a property of the sample preparation, not of our analysis. The trans configuration is therefore supported by the recessive disease model and the parental recurrent-miscarriage history (consistent with two carrier parents), and stated as **inferred**. [OUR MEASUREMENT — `samtools view -f 0x2 -F 0x900` TLEN distribution over the locus; markers from the provided GATK VCF]
- **Read support is robust for both calls, and now orthogonally confirmed.** The provided VCF gives `AD` (ref,alt) of **21,25** at chr15:40,209,701 and **15,13** at chr15:40,220,612. Re-calling independently from our own four-lane alignment reproduces this: pileup ref/alt of **21/26** (alt fraction 0.553) and **15/12** (0.444), with both positions re-called by `bcftools mpileup`/`call` without reference to the provided callset. Reference counts agree exactly; the one-read differences on the alt side are the `-Q 20` base-quality filter. Both sites are therefore clean germline heterozygotes with **no indication of low-VAF mosaicism**, established from reads rather than from the delivered VCF alone. Mosaicism elsewhere in the genome was not assessed.
- No FASTQ realignment or SV/CNV calling was performed for this submission; the provided GATK VCF was taken as-is. Rows 2 and 3 of the CSV hedge against a mis-assigned second allele.

## Reproducibility

`analysis/bub1b_targeted_analysis.py` (Python 3 stdlib; optional `truststore`) reproduces steps 2–4 from the provided VCF in one command. See repository README.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
