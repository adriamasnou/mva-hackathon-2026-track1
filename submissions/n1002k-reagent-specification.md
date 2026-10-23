# Build specification: the *BUB1B* N1002K construct that does not exist

**Sequence designs for an initial fragment experiment.** These sequences do not constitute a completed experiment. The search below found no catalogued N1002K reagent in the two repositories inspected at the recorded dates; it cannot exclude unpublished or later work.

*Rare Disease, Real Kid: The MVA Hackathon 2026 · adriamasnou · updated 23 October 2026 · CC BY 4.0*

Four sequences are supplied: WT, N1002K, K795A and Q921H. K795A and Q921H are proposed comparators whose behaviour must be qualified in this fragment assay. Normal cellular abundance of Q921H is not proof of neutral fragment thermostability. The approximately $630 estimate covers dated fragment materials, not full-length cellular experiments, labour or exposure measurement. The [functional plan](functional-rescue-plan.md) governs advancement.

---

## 1. The gap, stated plainly

| what exists | what it is |
|---|---|
| `GM21284` (Coriell) | a real MVA patient line — but genotype **`753X` / `R814H`**, not this child's |
| Addgene **#114052 / #114061 / #114062** | wild-type, `K795A`, `D882N` BubR1 — Kops lab, publication-linked. 🔴 **All three are MAMMALIAN pIC58 (pLAP) plasmids encoding FULL-LENGTH YFP-TEV-S-LAP-BubR1** (verified 2026-08-30) — useful for cell-based work, but not the source's full-length **GST-BUBR1** purification system (route **A1**) or the bacterial HIS₆ (721–1,044) purification route **A2** this document selects in §3. See §5 item 4 |
| Addgene **#23858** `pDONR223-BUB1B` | full-length ORF, Gateway **entry** clone |
| **an N1002K construct** | ❌ **not catalogued in Coriell or Addgene** — the two repositories searched, record by record. *(Scoped 2026-08-31 from "does not exist, anywhere": ECACC returned nothing parseable, and an unresolved query is not an absence.)* |

So the dose–response curves, the stability data, the chaperone-dependence result — all of it is
`753X/R814H`, `K795A`, or mouse. **We have not identified an experimental characterisation of this exact allele in the retained literature.** Absence from the searches is not proof that no unpublished or newly published experiment exists.

## 2. The edit, verified at sequence level

| | |
|---|---|
| variant | `chr15:40,220,612 T>G` (GRCh38) · `c.3006T>G` · **p.Asn1002Lys** |
| codon | **`AAT` (Asn) → `AAG` (Lys)** — third base |
| context | `…GATTCTGAA[T>G]GCCAATGAT…` — the bracketed base is the one that changes |

**[OUR MEASUREMENT — extracted directly from `GRCh38_no_alt_plus_hs38d1.fna` and translated; the
reference base returned `T`, matching the VCF. Not taken from an annotation.]**

### 2a. ✅ Re-verified end to end, 2026-08-31 — every number a bench would rely on

**Two independent sources, agreeing.** The genome gives the local context; the transcript gives the
codon number. **A residue number is the thing most likely to be wrong** — this project already
carries a mouse-vs-human numbering scar — so it was re-derived rather than trusted.

| check | result |
|---|---|
| genomic context, `chr15:40,220,572–40,220,652` | `…GGATTCTGAA`**`T`**`GCCAATGAT…` — the variant base is `T` at position 41 of that extract ✅ **matches §2** |
| canonical CDS `ENST00000287598.11` | **3,153 bp** → **1,050 aa + stop** ✅ matches the 1,050-residue protein the domain map uses |
| codon 1002 (`c.3004–3006`) | **`AAT`** ✅ · `c.3006` is its **third base**, and it is `T` ✅ |
| translation, residues 995–1010 | `KFFVRIL`**`N`**`ANDEATVS` — **residue 1002 is `N`** ✅ |
| apply `c.3006T>G` | `AAT` → `AAG` → **residue 1002 is `K`** ✅ **p.Asn1002Lys confirmed** |
| fragment 721–1,044 | **972 bp · 324 codons** ✅ matches §3 · first and last residues both `P`, matching the full-length protein at those positions |
| WT vs N1002K fragment | **exactly 1 difference**, at fragment position **846** ✅ · no internal stop codon in either |
| **provenance of every row above** | **[OUR MEASUREMENT — computed 2026-08-31 from the two public sources in the reproduce block: `ENST00000287598.11` CDS via Ensembl REST, and the GRCh38 reference FASTA. No annotation, database summary or prior document was used as a source for any row.]** |

**Reproduce (public identifiers only — no patient data is sent anywhere):**

```bash
curl -s "https://rest.ensembl.org/sequence/id/ENST00000287598?type=cds;content-type=text/x-fasta"
samtools faidx pipeline/ref/GRCh38_no_alt_plus_hs38d1.fna chr15:40220572-40220652
```

⚠️ **Use `curl`, not python `urllib`** — on the machine this was built on, urllib fails with
`SSL CERTIFICATE_VERIFY_FAILED` against a self-signed certificate in a local proxy chain, which
reads as "the sequence is unavailable" rather than "the client is misconfigured."

## 3. Two routes, and the recommendation is the less obvious one

The protocol's route **A2** needs the **HIS₆-BubR1 (721–1,044)** pseudokinase-domain fragment —
**324 residues, 972 bp of CDS.**

### ★ Route 1 — SYNTHESISE the mutant fragment (recommended)

At ~1 kb, **synthesis is now cheaper and faster than mutagenising and subcloning**, and it arrives
**sequence-verified**. Order the 721–1,044 fragment **four times** — wild-type, `c.3006T>G` (N1002K), and the two
candidate comparators the companion protocol requires, K795A and Q921H — each with the flanking sites your
destination vector needs.

- No template to source, no mutagenesis, no screening of colonies.
- **The WT arrives from the same synthesis run**, so each variant differs from WT only at its intended
  codon and shares every other property. For a ΔTm measurement between constructs, that matters more than cost.
- ⚠️ Codon-optimise **nothing**. A ΔTm comparison requires the constructs to be identical
  outside their intended edits; optimisation would silently break that.

#### 🔴 ORDER THE CLONED PRODUCT, NOT THE FRAGMENT — they are different things and the cheaper one is not sequence-verified

This document says synthesis *"arrives sequence-verified."* **That is true of one product and not of
the one a lab is likely to click on.** Verified against Twist's published specifications,
2026-08-31:

| | **Clonal Genes** ✅ order this | **Gene Fragments** ❌ not this |
|---|---|---|
| format | cloned into a vector | **linear dsDNA — not cloned** |
| verification | **"100% sequence perfect, NGS verified"** | *no per-construct sequence-perfect guarantee stated* |
| price, 0.3–1.8 kb | **9¢/bp** Low/Medium · 12¢/bp High | **from 7¢/bp** |
| cloning | **+$35** cloning vector · **+$55** expression vector · +$75 custom | you clone it yourself |
| turnaround | Express **4–7** business days · Standard **10** | — |

**At 972 bp the difference is about $150 across the pair and ≈ $300 across the four, and it buys the
thing this experiment depends on.** Gene Fragments are cheaper and would leave the laboratory to clone and sequence-verify
the constructs itself — which is exactly the work route 1 exists to remove, and it reintroduces
the chance that a construct ends up differing from WT by more than its intended edit.

✅ **Our fragment should price at the Low/Medium tier (9¢/bp), not High.** The §3 synthesisability
screen — GC 40.4–40.6% across the four, worst 50 bp window 24–56%, zero homopolymers ≥6 nt — is the
same class of measure Twist scores complexity on, and Gene Fragments are offered only for Low/Medium sequences,
with high-complexity sequences routed to Clonal Genes. **Twist's own Manufacturability Analyzer will
confirm the tier before you commit** — run all four sequences through it and check the quoted
complexity before ordering.

**[OUR MEASUREMENT — all figures read from twistbioscience.com/products/genes and
/products/genes/fragments on 2026-08-31. US list prices; academic, volume and regional pricing
differ, and these must still be confirmed in your own quote.]**

#### ★★ The four sequences to order — paste these into the vendor form

🔴 **ADDED 2026-08-31. This document previously RECOMMENDED route 1 and then did not supply the
sequence**, leaving the ordering laboratory to re-derive it from a transcript ID — which is exactly
where strand, transcript-version and residue-numbering errors enter. **That was the largest
remaining gap between this file and "turnkey", and it is closed here.**

**Source: `ENST00000287598.11` CDS, fetched from Ensembl REST and verified in full (§2a).
972 bp · 324 codons · residues 721–1,044. The pair under test differ at exactly one base — fragment
position 846 — and at nothing else; the two controls that follow each differ from WT at one codon only.**

<details><summary><b>BUB1B_721-1044_WT</b> — 972 bp</summary>

```
CCATGGTGTTCACAGTATCGCAGACAGCTACTGAAGTCCCTACCAGAGTTAAGTGCCTCT
GCAGAGTTGTGTATAGAAGACAGACCAATGCCTAAGTTGGAAATTGAGAAGGAAATTGAA
TTAGGTAATGAGGATTACTGCATTAAACGAGAATACCTAATATGTGAAGATTACAAGTTA
TTCTGGGTGGCGCCAAGAAACTCTGCAGAATTAACAGTAATAAAGGTATCTTCTCAACCT
GTCCCATGGGACTTTTATATCAACCTCAAGTTAAAGGAACGTTTAAATGAAGATTTTGAT
CATTTTTGCAGCTGTTATCAATATCAAGATGGCTGTATTGTTTGGCACCAATATATAAAC
TGCTTCACCCTTCAGGATCTTCTCCAACACAGTGAATATATTACCCATGAAATAACAGTG
TTGATTATTTATAACCTTTTGACAATAGTGGAGATGCTACACAAAGCAGAAATAGTCCAT
GGTGACTTGAGTCCAAGGTGTCTGATTCTCAGAAACAGAATCCACGATCCCTATGATTGT
AACAAGAACAATCAAGCTTTGAAGATAGTGGACTTTTCCTACAGTGTTGACCTTAGGGTG
CAGCTGGATGTTTTTACCCTCAGCGGCTTTCGGACTGTACAGATCCTGGAAGGACAAAAG
ATCCTGGCTAACTGTTCTTCTCCCTACCAGGTAGACCTGTTTGGTATAGCAGATTTAGCA
CATTTACTATTGTTCAAGGAACACCTACAGGTCTTCTGGGATGGGTCCTTCTGGAAACTT
AGCCAAAATATTTCTGAGCTAAAAGATGGTGAATTGTGGAATAAATTCTTTGTGCGGATT
CTGAATGCCAATGATGAGGCCACAGTGTCTGTTCTTGGGGAGCTTGCAGCAGAAATGAAT
GGGGTTTTTGACACTACATTCCAAAGTCACCTGAACAAAGCCTTATGGAAGGTAGGGAAG
TTAACTAGTCCT
```
</details>

<details><summary><b>BUB1B_721-1044_N1002K</b> — 972 bp, <code>c.3006T&gt;G</code> at fragment position 846</summary>

```
CCATGGTGTTCACAGTATCGCAGACAGCTACTGAAGTCCCTACCAGAGTTAAGTGCCTCT
GCAGAGTTGTGTATAGAAGACAGACCAATGCCTAAGTTGGAAATTGAGAAGGAAATTGAA
TTAGGTAATGAGGATTACTGCATTAAACGAGAATACCTAATATGTGAAGATTACAAGTTA
TTCTGGGTGGCGCCAAGAAACTCTGCAGAATTAACAGTAATAAAGGTATCTTCTCAACCT
GTCCCATGGGACTTTTATATCAACCTCAAGTTAAAGGAACGTTTAAATGAAGATTTTGAT
CATTTTTGCAGCTGTTATCAATATCAAGATGGCTGTATTGTTTGGCACCAATATATAAAC
TGCTTCACCCTTCAGGATCTTCTCCAACACAGTGAATATATTACCCATGAAATAACAGTG
TTGATTATTTATAACCTTTTGACAATAGTGGAGATGCTACACAAAGCAGAAATAGTCCAT
GGTGACTTGAGTCCAAGGTGTCTGATTCTCAGAAACAGAATCCACGATCCCTATGATTGT
AACAAGAACAATCAAGCTTTGAAGATAGTGGACTTTTCCTACAGTGTTGACCTTAGGGTG
CAGCTGGATGTTTTTACCCTCAGCGGCTTTCGGACTGTACAGATCCTGGAAGGACAAAAG
ATCCTGGCTAACTGTTCTTCTCCCTACCAGGTAGACCTGTTTGGTATAGCAGATTTAGCA
CATTTACTATTGTTCAAGGAACACCTACAGGTCTTCTGGGATGGGTCCTTCTGGAAACTT
AGCCAAAATATTTCTGAGCTAAAAGATGGTGAATTGTGGAATAAATTCTTTGTGCGGATT
CTGAAGGCCAATGATGAGGCCACAGTGTCTGTTCTTGGGGAGCTTGCAGCAGAAATGAAT
GGGGTTTTTGACACTACATTCCAAAGTCACCTGAACAAAGCCTTATGGAAGGTAGGGAAG
TTAACTAGTCCT
```
</details>

<details><summary><b>BUB1B_721-1044_K795A</b> — 972 bp, candidate destabilising comparator, fragment behaviour unvalidated: codon 795 <code>AAG</code>→<code>GCG</code>, fragment positions 223–224 (<code>c.2383_2384delinsGC</code>)</summary>

```
CCATGGTGTTCACAGTATCGCAGACAGCTACTGAAGTCCCTACCAGAGTTAAGTGCCTCT
GCAGAGTTGTGTATAGAAGACAGACCAATGCCTAAGTTGGAAATTGAGAAGGAAATTGAA
TTAGGTAATGAGGATTACTGCATTAAACGAGAATACCTAATATGTGAAGATTACAAGTTA
TTCTGGGTGGCGCCAAGAAACTCTGCAGAATTAACAGTAATAGCGGTATCTTCTCAACCT
GTCCCATGGGACTTTTATATCAACCTCAAGTTAAAGGAACGTTTAAATGAAGATTTTGAT
CATTTTTGCAGCTGTTATCAATATCAAGATGGCTGTATTGTTTGGCACCAATATATAAAC
TGCTTCACCCTTCAGGATCTTCTCCAACACAGTGAATATATTACCCATGAAATAACAGTG
TTGATTATTTATAACCTTTTGACAATAGTGGAGATGCTACACAAAGCAGAAATAGTCCAT
GGTGACTTGAGTCCAAGGTGTCTGATTCTCAGAAACAGAATCCACGATCCCTATGATTGT
AACAAGAACAATCAAGCTTTGAAGATAGTGGACTTTTCCTACAGTGTTGACCTTAGGGTG
CAGCTGGATGTTTTTACCCTCAGCGGCTTTCGGACTGTACAGATCCTGGAAGGACAAAAG
ATCCTGGCTAACTGTTCTTCTCCCTACCAGGTAGACCTGTTTGGTATAGCAGATTTAGCA
CATTTACTATTGTTCAAGGAACACCTACAGGTCTTCTGGGATGGGTCCTTCTGGAAACTT
AGCCAAAATATTTCTGAGCTAAAAGATGGTGAATTGTGGAATAAATTCTTTGTGCGGATT
CTGAATGCCAATGATGAGGCCACAGTGTCTGTTCTTGGGGAGCTTGCAGCAGAAATGAAT
GGGGTTTTTGACACTACATTCCAAAGTCACCTGAACAAAGCCTTATGGAAGGTAGGGAAG
TTAACTAGTCCT
```
</details>

<details><summary><b>BUB1B_721-1044_Q921H</b> — 972 bp, proposed comparator, fragment behaviour unvalidated: codon 921 <code>CAG</code>→<code>CAC</code>, fragment position 603 (<code>c.2763G&gt;C</code>)</summary>

```
CCATGGTGTTCACAGTATCGCAGACAGCTACTGAAGTCCCTACCAGAGTTAAGTGCCTCT
GCAGAGTTGTGTATAGAAGACAGACCAATGCCTAAGTTGGAAATTGAGAAGGAAATTGAA
TTAGGTAATGAGGATTACTGCATTAAACGAGAATACCTAATATGTGAAGATTACAAGTTA
TTCTGGGTGGCGCCAAGAAACTCTGCAGAATTAACAGTAATAAAGGTATCTTCTCAACCT
GTCCCATGGGACTTTTATATCAACCTCAAGTTAAAGGAACGTTTAAATGAAGATTTTGAT
CATTTTTGCAGCTGTTATCAATATCAAGATGGCTGTATTGTTTGGCACCAATATATAAAC
TGCTTCACCCTTCAGGATCTTCTCCAACACAGTGAATATATTACCCATGAAATAACAGTG
TTGATTATTTATAACCTTTTGACAATAGTGGAGATGCTACACAAAGCAGAAATAGTCCAT
GGTGACTTGAGTCCAAGGTGTCTGATTCTCAGAAACAGAATCCACGATCCCTATGATTGT
AACAAGAACAATCAAGCTTTGAAGATAGTGGACTTTTCCTACAGTGTTGACCTTAGGGTG
CACCTGGATGTTTTTACCCTCAGCGGCTTTCGGACTGTACAGATCCTGGAAGGACAAAAG
ATCCTGGCTAACTGTTCTTCTCCCTACCAGGTAGACCTGTTTGGTATAGCAGATTTAGCA
CATTTACTATTGTTCAAGGAACACCTACAGGTCTTCTGGGATGGGTCCTTCTGGAAACTT
AGCCAAAATATTTCTGAGCTAAAAGATGGTGAATTGTGGAATAAATTCTTTGTGCGGATT
CTGAATGCCAATGATGAGGCCACAGTGTCTGTTCTTGGGGAGCTTGCAGCAGAAATGAAT
GGGGTTTTTGACACTACATTCCAAAGTCACCTGAACAAAGCCTTATGGAAGGTAGGGAAG
TTAACTAGTCCT
```
</details>

**How the two control sequences were made, and what they are.** Both were derived from the WT
fragment above by editing one codon and nothing else, then re-translated and diffed against WT
(**K795A: protein differs at residue 795 only, K→A, two adjacent bases; Q921H: residue 921 only,
Q→H, one base; no stop codon introduced in either**). **Q921H uses the patient allele itself** —
`c.2763G>C` is the change reported in *cis* with L844F in Hanks 2004 family 1 (**PMID 15475955**) and
characterised as wild-type-like in isolation (**PMID 20516114**, Fig 4D). **K795A is a laboratory
mutant**, not a patient variant; the source (**PMID 22698286**) does not state which alanine codon it
used, so `GCG` was chosen as the minimal two-base edit that keeps the third position — any alanine
codon is equivalent at the protein level, and the melt reads protein. **[OUR MEASUREMENT — derived
and verified 2026-09-06 from the WT sequence in this section; codon numbering re-checked against
`ENST00000287598.11` as in §2a.]**

**✅ Synthesisability pre-screened against the standard vendor rejection criteria, so the order
should not bounce:** global GC **40.4–40.6%** across the four (limits 25–75%); worst 50 bp window **24–56%** (limits 20–80%); **zero homopolymer runs ≥ 6 nt** (longest 5); no internal stop codon in any frame-0 translation. **[OUR MEASUREMENT — pair 2026-08-31, controls 2026-09-06, same script.]**

> ⚠️ **THREE THINGS THE VENDOR FORM WILL NOT WARN YOU ABOUT.** This fragment is **internal to the
> ORF** — residues 721–1,044 of 1,050:
> 1. **It has no start codon and no stop codon.** With an N-terminal HIS₆ tag the vector supplies
>    the start; **you must ensure a stop.** Append `TAA` yourself if your destination vector does
>    not provide one. *(This is the same failure class as Addgene #23858 in route 2 below — an
>    entry clone with no stop codon that yields a read-through product. It has now bitten this
>    document twice, in two different routes.)*
> 2. **It must be cloned in frame with the tag.** Add the flanking cloning sites your vector needs
>    **outside** the 972 bp, and check the frame across the junction — do not edit inside it.
> 3. **Order all four fragments in the same run**, as §3 already argues. The ΔTm is the measurement;
>    two synthesis batches introduce a difference the experiment cannot separate from the variant.

### Route 2 — site-directed mutagenesis from Addgene #23858

Use if a full-length ORF is wanted for cell work rather than the bacterial fragment.

**Mutagenic primer pair, designed and checked here** (QuikChange-style, complementary, mismatch
centred at position 18 of 35):

```
FWD 5'-CTTTGTGCGGATTCTGAAGGCCAATGATGAGGCCAC-3'   36 nt · Tm 81.6 °C · GC 52.8%
REV 5'-GTGGCCTCATCATTGGCCTTCAGAATCCGCACAAAG-3'   mismatch at 19 of 36 · flanks 18/17
```

Tm exceeds the ≥78 °C the method requires, the mismatch is centred with ≥17 correct bases on both
sides, and **all four termini are G or C**.

> ### 🔻 CORRECTED 2026-08-31 — THE PREVIOUS PAIR VIOLATED THE DESIGN RULE THIS LINE CLAIMED IT MET
> The pair read `FWD 5'-TTTGTGCGG…GCCAC-3'` / `REV 5'-GTGGCC…CACAAA-3'`, annotated *"both ends
> terminate in C/G."* **They did not.** Checked computationally: **`FWD` 5′ = `T` and `REV` 3′ = `A`.**
> The QuikChange rule is about the **3′ terminus**, where the polymerase extends, and the reverse
> primer ended in `A`. Because the two primers must be exact reverse complements, this cannot be
> repaired on one strand — the window itself had to move.
>
> **The fix is one base: a `C` prepended to the 5′ end of `FWD`**, which makes `REV` end in `G`.
> Nothing else changes; the 3′ end of `FWD` is untouched. Tm rises 80.4 → 81.6 °C, GC 51.4 → 52.8%,
> and the mismatch stays centred. **52 windows satisfy every QuikChange criterion including both
> termini; this is the most centred short one, and it is the minimal edit to what was already here.**
>
> ⚠️ **The old pair was internally self-consistent** — exact reverse complements, correct mismatch
> at 18/35, correct Tm and GC arithmetic, and it would have amplified. **The annotation was the
> defect, and a lab that trusted it would have ordered a primer with a documented efficiency
> penalty.** Everything checkable was checked; the one thing asserted in prose was wrong.
> **[OUR MEASUREMENT — reverse-complementarity, Tm by the QuikChange formula
> `81.5 + 0.41(%GC) − 675/N − %mismatch`, and an exhaustive window search over the CDS, 2026-08-31.]**

> ### 🔴 #23858 has NO STOP CODON, and the depositor says so
> Verbatim: *"The ORF has **no Stop codon**… **Do NOT use this plasmid directly for
> transfections.**"* It is a Gateway **entry** clone. After mutagenesis it **must** be recombined
> (LR) into a destination vector supplying a tag and a stop codon. **Skipping that step yields a
> read-through product**, and the protocol did not originally name it.

## 4. 🔻 An error in this document's own first draft, recorded

The first version of §3 included Sanger primers annealing **~300 bp either side of the edit,
designed against the genome.** That is wrong and would have wasted a lab's time: **the construct is
an ORF clone and contains no intron.** The CDS block holding the variant is
`chr15:40,220,564–40,220,759` — **only 48 bp of coding sequence upstream and 147 bp downstream.**
Genomic primers at ±300 bp anneal to sequence that is not in the plasmid.

**Corrected recommendation: whole-plasmid sequencing, not primer-walking.** It needs no primer
design, verifies the entire construct rather than a window, and — the reason that matters here —
**catches second-site mutations that polymerase-based mutagenesis introduces elsewhere in the
plasmid**, which a targeted amplicon cannot see.

## 4a. ✅ CATALOGUE FACTS RE-VERIFIED LIVE, 2026-08-31 — and this found a trap

Every Addgene figure in this document was re-fetched from the live records on **2026-08-31**. **Both
previously-unverified claims hold exactly**, and the check surfaced four things the document did not
have — one of which would have broken the QC gate in §5.

| claim | live record | verdict |
|---|---|---|
| #23858 price **$94** | *"Plasmid 23858 … agar stab 1 **$94**"* | ✅ **exact** |
| #23858 has no stop codon | *"The ORF has **no Stop codon**. This design enables easy recombination into a destination vector to add an epitope tag of choice and Stop codon to the ORF. **Do NOT use this plasmid directly for transfections.**"* | ✅ **verbatim, unchanged** |
| Kops plasmids are mammalian pIC58/pLAP, full-length, `YFP-TEV-S-` LAP N-terminal | confirmed for **#114052** and **#114061**; vector type *"Mammalian Expression"* | ✅ |
| control plasmids **"~$80–100"** each | **$94** each — all three plasmids are $94 | 🔻 **now exact, not a range** |
| **[OUR MEASUREMENT — all rows re-fetched from addgene.org/23858, /114052 and /114061 on 2026-08-31.]** | | |

### 🔴 4a.1 THE TRAP: both Kops plasmids carry two silent edits *inside* our fragment

**#114052 and #114061 both list `Mutation: C2823A and G2826A (siRNA-resistance)`.** Resolved against
`ENST00000287598.11`:

| | codon | change | consequence | in the 721–1,044 fragment? |
|---|---|---|---|---|
| `c.2823C>A` | 941 | `ATC` → `ATA` | **Ile → Ile, synonymous** | ✅ **yes — fragment position 663** |
| `c.2826G>A` | 942 | `CTG` → `CTA` | **Leu → Leu, synonymous** | ✅ **yes — fragment position 666** |

**They sit 180–183 bp upstream of the N1002K edit, well inside the region this document tells you to
synthesise.** The protein is unaffected — so a *protein* melting curve is not compromised — but:

> 🔴 **IF YOU USE #114052 AS THE "WILD-TYPE" COMPARATOR, EVERY VARIANT DIFFERS FROM IT AT THREE
> BASES, NOT AT ITS ONE INTENDED CODON**, and **§5's QC gate — *"differing from wild-type only at its
> intended codon … only the edit is present"* — will fail on two changes that are supposed to be there.** A laboratory hitting that would reasonably
> conclude the synthesis was wrong.
>
> ✅ **This is a further argument for route 1 as written**: order **all four** fragments from the same
> synthesis run and none carries the siRNA-resistance edits, so each variant genuinely differs from WT
> only at its intended codon. **Do not mix a synthesised fragment against an Addgene-derived wild-type.**
> **[OUR MEASUREMENT — Addgene's stated mutations mapped onto the canonical CDS, 2026-08-31.]**

### 4a.2 Three further things the records say and this document did not

1. 🔴 **Neither plasmid can be fully verified in silico before ordering.** #23858: *"Full plasmid
   sequence is not available for this item."* #114061's depositor states: *"based on pLAP-BUBR1:
   **point mutation(s) are not included in Sequence:Full**"* — **the deposited sequence does not show
   K795A.** Anyone using #114061 as a cell-based comparator and checking it against the deposited
   record will not find the mutation there. **Sequence it on arrival; do not infer it.**
2. ⚠️ **#23858's insert is listed as 3,153 bp — numerically identical to the full CDS *including* its
   stop codon**, while the depositor says the ORF has no stop codon. Both cannot be literally true of
   the same 3 bases. **The 3′ end is exactly where Gateway recombination and tag frame matter, so
   resolve it by sequencing** — which §4 already recommends for a different reason.
3. ✅ **Growth and selection, straight from the records** — absent here until now, and needed the
   moment a stab arrives: **#23858 — Spectinomycin 50 µg/mL**, DH5α, 37 °C, high copy; sequencing
   primers **M13pUC-fwd / M13rev**. **#114052 and #114061 — Kanamycin 50 µg/mL**, DH5α, 37 °C, high
   copy. All three are **academic/non-profit only, UBMTA**.

⚠️ **Note also that the two Kops plasmids come from *different papers*:** #114061 (K795A) is from
**PMID 22698286**, the pseudokinase paper this document quotes for the 39.1/34.7 °C Tm pair;
**#114052 (WT) is from PMID 23079597**, the kinase–phosphatase paper. Cite each to its own source.

## 5. Quality control — what must be true before the construct is used

1. **Whole-plasmid sequence**, matching the intended sequence, with **each construct differing from
   wild-type only at its intended codon** — one base for N1002K and Q921H, two adjacent bases for
   K795A. Not "the edit is present" — *only* the edit is present.
   🔴 **This gate assumes all four constructs come from the same synthesis run (route 1).** If
   the comparator is an Addgene-derived construct it carries two extra synonymous
   siRNA-resistance changes inside the fragment and this gate will fail correctly — **see §4a.1
   before concluding the synthesis went wrong.**
2. **The WT counterpart sequenced in the same run**, from the same source.
3. Expression checked by SDS-PAGE before any Tm measurement; a construct that does not express
   cannot produce a melting curve, and a flat curve would otherwise be read as a result.
4. **Qualify controls for the actual construct and assay.** Published unfolding curves exist for
   **HIS₆-BubR1(721–1,044)** (PMID 22698286, Fig S3G–H). The **39.1 °C / 34.7 °C** WT–K795A
   pair instead concerns **full-length GST-BUBR1** (Fig 3G / S3D). The supplement does not establish
   WT–K795A separation for the fragment assay or a calibrated N1002K threshold. The earlier claim
   that the fragment had no published thermal data was incorrect.

   **Proposed fragment qualification [OUR DESIGN]:**

   - Purify **WT, N1002K, K795A and Q921H HIS₆-BubR1(721–1,044)** using matched expression and
     purification conditions, and melt all four side by side. K795A is a **candidate destabilising
     comparator**, and Q921H a **candidate WT-like comparator**; neither role is established for
     this fragment. N1002K is the unknown, not a calibration control. **[OUR INFERENCE — proposed
     assay design; comparator roles require experimental qualification.]**
   - Use **≥3 independent protein preparations** as an exploratory reproducibility check, not a
     substitute for demonstrated dynamic range or a confirmatory power calculation. Qualify control
     behaviour and freeze assay acceptance criteria before interpreting N1002K.
   - Report **absolute unfolding curves, method-specific transition estimates and within-run ΔTm**.
     Use the published WT-fragment curves as context, without importing full-length thresholds.
     Failed control qualification makes the assay indeterminate, not the variant normal or abnormal.

   **Full-length alternative (route A1):** comparison with the published WT–K795A pair requires
   documenting the source's **High-Five insect cells / Bac-to-Bac expression, GST tag, purification
   and fluorescence conditions** (PMID 22698286, Supplemental Experimental Procedures, pp.9–12).
   Its thermal assay used **0.75 µM protein, 280 nm excitation and 353 nm emission**, distinct from
   the fragment assay. Bacterial full-length expression or another readout is an adaptation requiring
   validation. Addgene **#114061 is mammalian pLAP-BUBR1-K795A**, not the source's GST expression
   construct or a HIS₆-fragment reagent; its published association does not make it an interchangeable
   thermal control.

## 6. Costs

### 🔑 Route 1, costed exactly — the recommended path, 2026-08-31 list prices, four constructs (restated 2026-09-06)

| item | unit | **×4** — WT · N1002K · K795A · Q921H | ×2 — pair only *(requires separate control qualification)* |
|---|---|---|---|
| **Twist Clonal Gene**, 972 bp @ **9¢/bp** (Low/Medium) | **$87.48** | **$349.92** | $174.96 |
| cloning into an **expression vector** | +$55 | **+$220** | +$110 |
| *(or a plain cloning vector)* | *+$35* | *+$140* | *+$70* |
| **Plasmidsaurus whole-plasmid sequencing** @ **$15**, one per construct | $15 | **$60** | $30 |
| | | | |
| **ROUTE 1 TOTAL — expression vector** | | **≈ $630** | ≈ $315 |
| **ROUTE 1 TOTAL — cloning vector** | | **≈ $550** | ≈ $275 |

**Turnaround: 4–7 business days express, 10 standard**, plus 1 day for sequencing.

🔑 **The recommended route needs no Addgene plasmid and no mutagenesis kit.** ≈ $630 is the figure
the companion protocol carries. **For this unvalidated fragment assay, our design retains technical
positive and negative controls and independent preparations to establish an interpretable response
range.** K795A and Q921H are candidates for those roles, subject to qualification (§5); merely
including them does not validate the assay. WT versus N1002K alone would not validate it either.
These technical controls do not substitute for independently classified pathogenic/benign variants
or by themselves calibrate **PS3/BS3**. Brnich distinguishes technical controls from clinical
validation and permits limited exceptions for established assays; our four-construct design is
not a universal control-count rule from that guidance (**PMID 31892348**, assay-instance evaluation
and Fig 2). The pair-only column is a cost comparison: the two candidate comparators add ≈ $285
in synthesis and cloning, or ≈ $315 with sequencing. **[OUR ASSAY DESIGN; clinical-evidence limits
as cited.]**

⚠️ **Twist's Clonal Genes are already NGS-verified**, so the $60 of whole-plasmid sequencing is an
*independent* check rather than a mandatory step. **Run it anyway** — §5 item 1 wants confirmation
from a second party, and at $15 a sample that is the cheapest line in this table.

**[OUR MEASUREMENT — Twist and Plasmidsaurus published list prices, read 2026-08-31. Arithmetic
ours. US list; academic and volume pricing differ.]**

| item | estimate |
|---|---|
| synthesised constructs ×4 (WT, N1002K, K795A, Q921H), 972 bp each — **costed exactly above** | **≈ $490–570** (≈ $245–285 for the pair) |
| *or* Addgene #23858 + mutagenesis kit + LR reaction | ~$94 plasmid + reagents |
| Addgene comparator plasmids (#114052, #114061) — **for a cell-based arm**; these mammalian full-length constructs are **not** the route-A1 GST expression system or route-A2 fragment reagents (§5 item 4) | **2 × $94 = $188** |
| whole-plasmid sequencing ×4 — **Plasmidsaurus, $15/sample, 1-day turnaround** | **$60** |
| **total, reagents only** | **≈ $550–630** (route A2 alone) · **≈ $740–820** including the optional cell-based plasmids; route-A1 GST purification is not costed |

**[OUR ESTIMATE. All three Addgene prices — #23858, #114052, #114061 — are `[VERIFIED]` at **$94
each**, re-fetched from the live plasmid pages 2026-08-31 (§4a); the previous "~$80–100" range is
replaced by the exact figure. **Synthesis and sequencing are now `[VERIFIED]` too** — Twist Clonal
Genes at **9¢/bp + $35–55 cloning** and Plasmidsaurus whole-plasmid sequencing at **$15/sample**,
both read from the vendors' published pricing 2026-08-31, replacing the previous "current market
ranges". These are **US list prices**; academic, volume and regional pricing differ and a real quote
should still be obtained. Consumables, instrument time and labour are `[NOT ESTIMATED]` and are not
invented here.]**

> 🔻 **THIS PARAGRAPH USED TO SAY SYNTHESIS AND SEQUENCING PRICES "MUST be re-quoted" AS THOUGH NO
> SOURCE COULD SETTLE THEM.** Both vendors publish per-bp and per-sample list prices openly; the
> figures were never unobtainable, only unfetched. **An estimate defended as unavoidable is worth
> re-testing before it is inherited** — that is the same error class as an absence asserted without
> a lookup, which this project has logged four times.

🔑 **The recommended path does not need any Addgene plasmid.** Route 1 is four synthesised constructs
plus sequencing: **≈ $550–630 in these materials.** The $188 of optional comparator plasmids belongs
to cell-based work, not either purified-protein route.

## 7. What this does not include, and what needs a person

- 🔴 **A laboratory.** Nothing here can be ordered by us. This is a specification, not a purchase.
- Addgene plasmids are **academic/non-profit only** and need an MTA.
- Route A2's original bacterial vector (`NKI-His-3C-LIC-kan`) is an in-house vector and **is not
  deposited** — hence the recommendation to synthesise with sites for a *commercially available*
  destination vector instead, which removes a request to another lab entirely.
- **Availability and prices must be re-checked.** Every catalogue figure here has a date on it.

## 8. Why this is worth doing even if the therapeutic idea fails

**The construct outlives the argument.** Whatever the stability result says, a sequence-verified
N1002K reagent is a permanent, orderable object that any laboratory can use to ask any question
about this allele — including questions nobody has thought of, and including questions asked after
everyone involved here has moved on.

Every other output of this project is a document. **This one would be a thing.**
