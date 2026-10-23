#!/usr/bin/env python3
r"""
Run the SpliceAI MODEL (not precomputed scores) over a VCF.

WHY THE MODEL AND NOT THE PRECOMPUTED SCORES
--------------------------------------------
Exomiser's `2512_hg38` bundle does carry real SpliceAI delta scores and applies them --
verified with actual values, not just the source name appearing in the output. But in a
test run only **32% of variant records carried a delta**. A variant absent from the
precomputed set returns NO score, and a missing score is indistinguishable from a benign
one at the point of use. For a small number of variants that actually matter, that gap is
the whole question, so the model is run directly.

Illumina's precomputed score files are behind a BaseSpace login. The MODEL is pip-
installable and GPL-3.0, needs no account, and scores anything -- including indels, which
the precomputed SNV set does not cover. The login-gated artefact is the weaker one.

🔴 CHROMOSOME NAMING -- the fifth instance of this trap in one day.
SpliceAI's bundled `grch38` annotation is ENSEMBL-named ("1", not "chr1"). It therefore
matches `pipeline/ref/GRCh38.primary.fa.bgz` and our patient VCF, and does NOT match
`GRCh38_no_alt_plus_hs38d1.fna`, which is UCSC-named and is what the CRAM and every
mosdepth artefact use. Passing the wrong reference produces no error -- it produces
silently empty scores.

PACKAGING: spliceai does `from keras.models import load_model`, which under Keras 3
resolves to the wrong API. `tf_keras` (Keras 2) is aliased in before the import.

Usage: python3 pipeline/spliceai_run.py <in.vcf.gz> [dist]
Output: one line per variant per gene -- DS_AG, DS_AL, DS_DG, DS_DL and their positions.
        Delta scores run 0-1; Illumina suggest 0.5 as a recommended cutoff, 0.2 high
        sensitivity, 0.8 high precision.
"""
import argparse, os, sys
from pathlib import Path
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")

import tf_keras
sys.modules["keras"] = tf_keras
sys.modules["keras.models"] = tf_keras.models
sys.modules["keras.backend"] = tf_keras.backend

import numpy as np
import pysam
import spliceai.utils as _su
from spliceai.utils import Annotator, get_delta_scores

# 🔴 SpliceAI 1.3.1 predates numpy 2. Its one_hot_encode calls np.fromstring in binary
# mode, which numpy REMOVED -- the package installs and imports cleanly and then dies on
# the first variant. Patched here rather than in site-packages so the fix travels with
# this repo and is visible to anyone reading it. Semantics are identical: frombuffer over
# the same bytes.
#
# 🔻 MY FIRST VERSION OF THIS PATCH SILENTLY BROKE THE MODEL. It called frombuffer on the
# RAW LETTERS and dropped the upstream byte substitution, so 'A'(65)%5=0 was read as N and
# 'G'(71)%5=1 was read as A. The model then scored noise and returned 0.00 for everything
# -- including five canonical splice-site pathogenic variants used as a positive control.
# It did not error. It returned a plausible "no splice signal" for every input.
# The substitution below is not decoration: it IS the encoding.
_MAP = np.asarray([[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
def _one_hot_encode(seq):
    seq = (seq.upper().replace("A", "\x01").replace("C", "\x02")
                      .replace("G", "\x03").replace("T", "\x04").replace("N", "\x00"))
    return _MAP[np.frombuffer(seq.encode("latin-1"), np.int8) % 5]
_su.one_hot_encode = _one_hot_encode

def main():
    parser = argparse.ArgumentParser(description="Run SpliceAI 1.3.1 with an explicit GRCh38 reference")
    parser.add_argument("vcf")
    parser.add_argument("distance", nargs="?", type=int, default=500)
    parser.add_argument("--reference", default=os.environ.get("MVA_SPLICEAI_REFERENCE"))
    args = parser.parse_args()
    if not args.reference or not Path(args.reference).is_file():
        parser.error("Set --reference or MVA_SPLICEAI_REFERENCE to an indexed Ensembl-named GRCh38 FASTA")
    if args.distance < 0:
        parser.error("distance must be nonnegative")
    vcf_path, dist = args.vcf, args.distance
    ann = Annotator(args.reference, "grch38")
    vcf = pysam.VariantFile(vcf_path)
    absent = set(vcf.header.contigs) - set(ann.ref_fasta.keys())
    if absent:
        parser.error("VCF contigs absent from reference: " + ", ".join(sorted(absent)))
    print(f"{'variant':<28} {'gene':<10} {'DS_AG':>6} {'DS_AL':>6} {'DS_DG':>6} {'DS_DL':>6}  max  verdict")
    n = 0
    for rec in vcf:
        scores = get_delta_scores(rec, ann, dist, 0)
        if not scores:
            print(f"{rec.chrom}:{rec.pos}{rec.ref}>{rec.alts[0]:<10}  (no gene overlap / no score)")
            continue
        for s in scores:
            f = s.split("|")
            gene = f[1]
            ds = [float(x) for x in f[2:6]]
            mx = max(ds)
            verdict = ("LIKELY SPLICE-ALTERING" if mx >= 0.5 else
                       "possible (>=0.2)" if mx >= 0.2 else "no splice signal")
            v = f"{rec.chrom}:{rec.pos}{rec.ref}>{rec.alts[0]}"
            print(f"{v:<28} {gene:<10} {ds[0]:>6.2f} {ds[1]:>6.2f} {ds[2]:>6.2f} {ds[3]:>6.2f}  "
                  f"{mx:.2f}  {verdict}")
            n += 1
    print(f"\n{n} gene-level score(s). Cutoffs: 0.2 high-sensitivity, 0.5 recommended, 0.8 high-precision.")

if __name__ == "__main__":
    main()
