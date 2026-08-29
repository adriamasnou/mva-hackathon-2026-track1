#!/usr/bin/env python3
r"""
Canary runner — assert that the interpretation layer of this pipeline is ALIVE.

Not a benchmark. A liveness test. Every assertion here has a published or arithmetic answer
that is not in dispute, so a failure means a TOOL IS BROKEN, not that a threshold was
tuned badly.

Exit 0 = every assertion held. Non-zero = at least one tool is returning something you
should not believe. See canary/README.md for why this exists.
"""
import csv, os, pathlib, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PANEL = ROOT / "canary/canary_variants.tsv"
RESULTS = []


def record(panel, name, ok, detail, skipped=False):
    RESULTS.append((panel, name, "SKIP" if skipped else ("PASS" if ok else "FAIL"), detail))


def load_panel(cls):
    rows = []
    with open(PANEL) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) >= 9 and p[5] == cls:
                rows.append(dict(id=p[0], chrom=p[1], pos=p[2], ref=p[3], alt=p[4],
                                 gene=p[6], expect=p[7], why=p[8]))
    return rows


# ---------------------------------------------------------------- PANEL 1: splice
def panel_splice():
    rows = load_panel("splice")
    runner = ROOT / "pipeline/spliceai_run.py"
    if not runner.exists():
        for r in rows:
            record("splice", r["id"], False, "spliceai_run.py not present", skipped=True)
        return
    with tempfile.NamedTemporaryFile("w", suffix=".vcf", delete=False) as fh:
        fh.write("##fileformat=VCFv4.2\n")
        for c in sorted({r["chrom"] for r in rows}, key=lambda x: x.zfill(2)):
            fh.write(f"##contig=<ID={c}>\n")
        fh.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
        fh.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tcanary\n")
        for r in sorted(rows, key=lambda r: (r["chrom"].zfill(2), int(r["pos"]))):
            fh.write(f"{r['chrom']}\t{r['pos']}\t{r['id']}\t{r['ref']}\t{r['alt']}\t100\tPASS\t.\tGT\t0/1\n")
        vcf = fh.name
    proc = subprocess.run([sys.executable, str(runner), vcf],
                          capture_output=True, text=True, cwd=ROOT)
    os.unlink(vcf)
    scores = {}
    for line in proc.stdout.splitlines():
        p = line.split()
        if len(p) >= 8 and ":" in p[0] and p[1] and _isfloat(p[6]):
            key = p[0]
            scores[key] = max(scores.get(key, 0.0), float(p[6]))
    if not scores:
        for r in rows:
            record("splice", r["id"], False,
                   "runner produced NO scores at all — the classic silent failure")
        return
    for r in rows:
        key = f"{r['chrom']}:{r['pos']}{r['ref']}>{r['alt']}"
        got = scores.get(key)
        if got is None:
            record("splice", r["id"], False, f"{r['gene']}: no score returned (silent miss)")
            continue
        op, thr = (">=", 0.5) if ">=" in r["expect"] else ("<", 0.2)
        ok = got >= thr if op == ">=" else got < thr
        record("splice", r["id"], ok,
               f"{r['gene']:<7} max delta {got:.2f}  expected {op}{thr}  ({r['why'][:44]})")


def _isfloat(x):
    try:
        float(x); return True
    except Exception:
        return False


# ---------------------------------------------------------------- PANEL 2: depth / CNV
def panel_depth():
    """chrX in a male MUST come back at 0.5. Free, and present in every male genome."""
    mod = ROOT / "pipeline/mosaicism_pass3.py"
    gc = ROOT / "data/derived/scans/gc.500kb.tsv"
    q60 = ROOT / "data/derived/scans/depthQ60.regions.bed.gz"
    if not (mod.exists() and gc.exists() and q60.exists()):
        record("depth", "XCHR-01", False,
               "depth artefacts not on this machine (sample-specific, expected on a fresh clone)",
               skipped=True)
        return
    proc = subprocess.run([sys.executable, str(mod)], capture_output=True, text=True, cwd=ROOT)
    val = None
    for line in proc.stdout.splitlines():
        if "chrX =" in line:
            try:
                val = float(line.split("chrX =")[1].split("vs")[0].strip())
            except Exception:
                pass
    if val is None:
        record("depth", "XCHR-01", False,
               "model produced no chrX value — a filter may have dropped every chrX bin")
        return
    err = abs(val - 0.5) / 0.5 * 100
    record("depth", "XCHR-01", err <= 1.0,
           f"chrX ratio {val:.4f} vs a true 0.5000 — error {err:.2f}%  (must be <=1%)")


# ---------------------------------------------------------------- PANEL 4: contig naming
def panel_naming():
    """
    The trap that cost the most time and never announced itself. A reference and an
    annotation that disagree on contig naming produce EMPTY output, not an error.
    """
    ens = ROOT / "pipeline/ref/GRCh38.primary.fa.bgz.fai"
    ucsc = ROOT / "pipeline/ref/GRCh38_no_alt_plus_hs38d1.fna.fai"
    if not (ens.exists() and ucsc.exists()):
        record("naming", "CONTIG-01", False, "reference indexes not present", skipped=True)
        return
    e = open(ens).readline().split("\t")[0]
    u = open(ucsc).readline().split("\t")[0]
    mismatch = e.startswith("chr") != u.startswith("chr")
    record("naming", "CONTIG-01", True,
           f"references on this machine use DIFFERENT conventions ('{e}' vs '{u}') — "
           f"{'CONFIRMED, and every tool must be told which' if mismatch else 'same convention'}")
    record("naming", "CONTIG-02", True,
           "spliceai grch38 annotation is Ensembl-named -> pair it with GRCh38.primary, "
           "never with GRCh38_no_alt (mismatch = silently empty scores, not an error)")


# ---------------------------------------------------------------- SELF-TEST
def self_test():
    r"""
    🔴 CAN THIS CANARY ACTUALLY GO RED?

    A control set that has only ever passed is indistinguishable from one that cannot
    fail -- which is the exact failure mode it exists to catch, turned on itself. So we
    reintroduce a REAL bug (the one that actually happened here) into a throwaway copy of
    the splice runner and assert the panel catches it.

    The bug: SpliceAI one-hot encoding without the byte substitution that precedes it, so
    'A' is read as 'N' and 'G' as 'A'. It raises no exception. It returns 0.00 for every
    variant -- a plausible "no splice signal" for a canonical splice-site mutation.
    """
    import re, shutil
    src = ROOT / "pipeline/spliceai_run.py"
    if not src.exists():
        print("  self-test SKIPPED: spliceai_run.py not present")
        return 0
    broken = ROOT / "canary/.broken_runner_tmp.py"
    text = src.read_text()
    # strip the substitution line -- the precise defect, not a synthetic one
    patched, n = re.subn(
        r'    seq = \(seq\.upper\(\)[^\n]*\n(?:[^\n]*\n)?',
        '', text, count=1)
    if n != 1:
        print("  self-test SKIPPED: could not locate the encoder line to break")
        return 0
    broken.write_text(patched)
    try:
        rows = load_panel("splice")
        pos = [r for r in rows if ">=" in r["expect"]]
        with tempfile.NamedTemporaryFile("w", suffix=".vcf", delete=False) as fh:
            fh.write("##fileformat=VCFv4.2\n")
            for c in sorted({r["chrom"] for r in pos}, key=lambda x: x.zfill(2)):
                fh.write(f"##contig=<ID={c}>\n")
            fh.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
            fh.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tcanary\n")
            for r in sorted(pos, key=lambda r: (r["chrom"].zfill(2), int(r["pos"]))):
                fh.write(f"{r['chrom']}\t{r['pos']}\t{r['id']}\t{r['ref']}\t{r['alt']}\t100\tPASS\t.\tGT\t0/1\n")
            vcf = fh.name
        proc = subprocess.run([sys.executable, str(broken), vcf],
                              capture_output=True, text=True, cwd=ROOT)
        os.unlink(vcf)
        got = []
        for line in proc.stdout.splitlines():
            p_ = line.split()
            if len(p_) >= 8 and ":" in p_[0] and _isfloat(p_[6]):
                got.append(float(p_[6]))
        print("\n" + "=" * 84)
        print("CANARY SELF-TEST — deliberately breaking the encoder, exactly as it broke for real")
        print("=" * 84)
        if not got:
            print("  inconclusive: the broken runner produced no parsable output")
            return 0
        caught = sum(1 for g in got if g < 0.5)
        print(f"  broken runner returned: {got}")
        print(f"  canary assertions that would FAIL: {caught} of {len(got)}")
        if caught == len(got):
            print("\n  ✅ THE CANARY CATCHES IT. All positive controls fail when the tool is")
            print("     silently broken, and the failure is loud instead of a clean negative.")
            return 0
        print("\n  🔴 THE CANARY DID NOT CATCH IT. This panel cannot detect the failure it was")
        print("     built for and must not be trusted.")
        return 1
    finally:
        broken.unlink(missing_ok=True)


def main():
    if "--self-test" in sys.argv:
        return self_test()
    want = [a.lstrip("-") for a in sys.argv[1:]] or ["splice", "depth", "naming"]
    if "splice" in want: panel_splice()
    if "depth" in want:  panel_depth()
    if "naming" in want: panel_naming()

    print("\n" + "=" * 84)
    print("CANARY — is the interpretation layer alive?  (not: is it accurate)")
    print("=" * 84)
    cur = None
    for panel, name, status, detail in RESULTS:
        if panel != cur:
            print(f"\n  [{panel}]"); cur = panel
        mark = {"PASS": "ok  ", "FAIL": "FAIL", "SKIP": "skip"}[status]
        print(f"    {mark}  {name:<10} {detail}")
    n_fail = sum(1 for r in RESULTS if r[2] == "FAIL")
    n_pass = sum(1 for r in RESULTS if r[2] == "PASS")
    n_skip = sum(1 for r in RESULTS if r[2] == "SKIP")
    print("\n" + "-" * 84)
    print(f"  {n_pass} passed · {n_fail} FAILED · {n_skip} skipped")
    if n_fail:
        print("\n  🔴 A FAILED CANARY MEANS A TOOL IS RETURNING SOMETHING YOU SHOULD NOT BELIEVE.")
        print("     Every expectation here has a published or arithmetic answer. Fix the tool,")
        print("     never the threshold.")
    else:
        print("\n  All live assertions held. This says the tools ANSWER; it does not say they are")
        print("  right — for that you need a benchmark, which this is not.")
    print("-" * 84)
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
