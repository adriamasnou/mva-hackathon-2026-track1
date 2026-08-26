#!/usr/bin/env python3
"""Targeted BUB1B analysis for the MVA Hackathon 2026 (Track 1).

Strategy: the proband carries a clinical diagnosis of Mosaic Variegated
Aneuploidy (MVA), so we place strong prior mass on the known MVA genes
(BUB1B, CEP57, TRIP13, and newer reports). This script performs the
BUB1B-targeted pass that identified the candidate compound heterozygote:

  1. Extract all variants in the GRCh38 BUB1B locus from the provided
     GATK VCF (no realignment needed for this pass).
  2. Keep PASS heterozygous variants; flag variants absent from dbSNP
     (no rsID) as candidate-novel.
  3. Map candidate-novel variants onto the canonical transcript
     (ENST00000287598) exon structure fetched from Ensembl REST, and
     compute protein consequences locally against the Ensembl CDS.

Privacy note: only public identifiers (gene symbol, transcript ID) are
sent to Ensembl; no proband variant ever leaves the local machine.

Usage:
    python3 bub1b_targeted_analysis.py path/to/WGS_<id>.vcf.gz

Requires: python3 stdlib only (urllib, gzip, json).
"""
import gzip
import json
import sys
import time
import urllib.request

try:  # use the OS trust store when available (macOS keychain, etc.)
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

ENSEMBL = "https://rest.ensembl.org"
GENE = "BUB1B"


def _fetch(path, accept):
    req = urllib.request.Request(ENSEMBL + path, headers={"Accept": accept})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as r:
                return r.read().decode()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 4:
                time.sleep(2 ** attempt)
                continue
            raise


def fetch_json(path):
    return json.loads(_fetch(path, "application/json"))


def fetch_text(path):
    return _fetch(path, "text/plain")


CODON_TABLE = {}
_bases = "TCAG"
_aas = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
_i = 0
for _b1 in _bases:
    for _b2 in _bases:
        for _b3 in _bases:
            CODON_TABLE[_b1 + _b2 + _b3] = _aas[_i]
            _i += 1


def main(vcf_path):
    gene = fetch_json(f"/lookup/symbol/homo_sapiens/{GENE}?expand=1")
    chrom, gstart, gend = gene["seq_region_name"], gene["start"], gene["end"]
    tx = next(t for t in gene["Transcript"] if t.get("is_canonical"))
    exons = sorted((e["start"], e["end"]) for e in tx["Exon"])
    tr = fetch_json(f"/lookup/id/{tx['id']}?expand=1")["Translation"]
    cds_start, cds_end = tr["start"], tr["end"]
    cds = fetch_text(f"/sequence/id/{tx['id']}?type=cds").strip().replace("\n", "")
    print(f"{GENE} {chrom}:{gstart}-{gend} ({tx['id']}, {len(exons)} exons, "
          f"CDS {cds_start}-{cds_end}, {len(cds)//3 - 1} aa)")

    def cds_pos(g):
        pos = 0
        for s, e in exons:
            cs, ce = max(s, cds_start), min(e, cds_end)
            if cs > ce:
                continue
            if cs <= g <= ce:
                return pos + (g - cs) + 1
            pos += ce - cs + 1
        return None

    hits = []
    opener = gzip.open if vcf_path.endswith(".gz") else open
    with opener(vcf_path, "rt") as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            c, pos, rsid, ref, alt, _, filt = fields[:7]
            if c.lstrip("chr") != chrom or not gstart <= int(pos) <= gend:
                continue
            gt = fields[9].split(":")[0]
            hits.append((int(pos), rsid, ref, alt, filt, gt))

    print(f"\n{len(hits)} variants in locus; heterozygous PASS without rsID:")
    for pos, rsid, ref, alt, filt, gt in hits:
        if filt != "PASS" or rsid != "." or gt not in ("0/1", "0|1", "1|0"):
            continue
        cp = cds_pos(pos)
        if cp is None or len(ref) != 1 or len(alt) != 1:
            print(f"  {chrom}:{pos} {ref}>{alt} {gt}  non-coding or indel (CDS pos: {cp})")
            continue
        ci, off = (cp - 1) // 3, (cp - 1) % 3
        codon = cds[ci * 3:ci * 3 + 3]
        assert codon[off] == ref, f"reference mismatch at {pos}"
        newc = codon[:off] + alt + codon[off + 1:]
        print(f"  {chrom}:{pos} {ref}>{alt} {gt}  c.{cp}{ref}>{alt}  "
              f"p.{CODON_TABLE[codon]}{ci + 1}{CODON_TABLE[newc]}")


if __name__ == "__main__":
    main(sys.argv[1])
