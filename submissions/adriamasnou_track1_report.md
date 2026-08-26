# Track 1 Methods Report — VCF-targeted BUB1B analysis

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

1. **Phenotype-driven gene prior.** The proband's HPO profile (rhabdomyosarcoma HP:0002859, nephrocalcinosis HP:0000121, short stature HP:0004322, failure to thrive HP:0001508, skeletal muscle atrophy HP:0003202, premature birth HP:0001622, SGA HP:0001518, parental recurrent spontaneous abortion HP:0200067) forms the classic chromosomal-instability cluster of Mosaic Variegated Aneuploidy. Established MVA genes (BUB1B/MVA1, CEP57/MVA2, TRIP13/MVA3, plus newer reports) were prioritized, with BUB1B first: it is the only MVA gene with a strong published rhabdomyosarcoma and Wilms-tumour association, and parental recurrent miscarriage fits biallelic recessive inheritance.
2. **Targeted locus extraction.** All variants in the GRCh38 BUB1B locus (15:40,160,984–40,221,137; canonical transcript ENST00000287598) were extracted from the provided GATK VCF (`WGS_EX2312012_HGWCNDSX7.vcf.gz`): 14 variants, of which 8 heterozygous.
3. **Novelty filter.** Three heterozygous PASS variants lack dbSNP IDs: chr15:40209701 T>G, chr15:40216470 A>G (deep intron 20), chr15:40220612 T>G.
4. **Local consequence calling.** Exon structure and CDS sequence for ENST00000287598 were fetched from Ensembl REST (public gene data only — no proband variant left the analysis machine); codon changes were computed locally: p.Leu737* and p.Asn1002Lys. The reference base at each position was asserted against the Ensembl CDS.
5. **Corroboration.** ClinVar: c.2210T>G (p.Leu737*) is Pathogenic/Likely pathogenic for MVA1; at chr15:40220612, c.3006T>A (same p.Asn1002Lys) is a reported VUS and c.3006T>C (p.Asn1002=) likely benign. Ensembl also lists pathogenic frameshift alleles at bases adjacent to 40209701, consistent with truncation intolerance in exon 17.

The genotype matches the canonical biallelic BUB1B MVA architecture (one truncating allele + one hypomorphic kinase-domain allele), with the missense allele plausibly preserving partial BubR1 function (complete loss of BUB1B is presumed lethal).

## Limitations

- **Phase is assumed, not demonstrated.** The two variants are 10.9 kb apart; single-sample short-read data cannot phase them and no parental genotypes are provided. The trans configuration is supported by the recessive disease model and the parental recurrent-miscarriage history (consistent with two carrier parents).
- Read support is robust for both calls (21/25 and 15/13 alt/ref reads), giving no indication of low-VAF mosaicism at these sites, but mosaicism elsewhere was not assessed.
- No FASTQ realignment or SV/CNV calling was performed for this submission; the provided GATK VCF was taken as-is. Rows 2 and 3 of the CSV hedge against a mis-assigned second allele.

## Reproducibility

`analysis/bub1b_targeted_analysis.py` (Python 3 stdlib; optional `truststore`) reproduces steps 2–4 from the provided VCF in one command. See repository README.

## Acknowledgement

This work was made possible through the Hackathon, organized by Sage Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The Benchmarking, Evaluation, and Assessment Consortium for Science), with prize sponsorship from AWS and Anthropic. We are deeply grateful to the child and their family who generously contributed their data and their story to advance research into this rare disease. We acknowledge their trust in making this Hackathon possible.
