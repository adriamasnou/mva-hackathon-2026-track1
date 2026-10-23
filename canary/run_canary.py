#!/usr/bin/env python3
"""Fail-closed SpliceAI regression panel. Model execution and harness self-test are distinct."""
import argparse
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
PANEL = ROOT / 'canary/canary_variants.tsv'


def load_panel(path=PANEL):
    rows = []
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        p = line.split('\t')
        if len(p) != 9 or p[5] != 'splice':
            raise ValueError('Malformed or unsupported panel row')
        rows.append(dict(id=p[0], chrom=p[1], pos=int(p[2]), ref=p[3], alt=p[4],
                         gene=p[6], positive='>=' in p[7]))
    if not rows or len({r['id'] for r in rows}) != len(rows):
        raise ValueError('Empty panel or duplicate identifiers')
    if not any(r['positive'] for r in rows) or not any(not r['positive'] for r in rows):
        raise ValueError('Panel needs both positive and negative controls')
    return rows


def key(row):
    return f"{row['chrom']}:{row['pos']}{row['ref']}>{row['alt']}"


def evaluate(stdout, rows, returncode=0):
    """Accept complete finite four-channel scores; do not turn absence into zero."""
    if returncode:
        return [f'Runner exited {returncode}']
    scores = {}
    errors = []
    expected = {(key(r), r['gene']) for r in rows}
    for line in stdout.splitlines():
        p = line.split()
        if len(p) < 2 or (p[0], p[1]) not in expected:
            continue
        try:
            ds = tuple(float(x) for x in p[2:6])
            maximum = float(p[6])
            if len(ds) != 4 or not all(math.isfinite(x) and 0 <= x <= 1 for x in (*ds, maximum)):
                raise ValueError('nonfinite/out-of-range')
            if abs(max(ds) - maximum) > 0.011:
                raise ValueError('inconsistent maximum')
            k = (p[0], p[1])
            if k in scores:
                raise ValueError('duplicate score')
            scores[k] = ds
        except (ValueError, IndexError):
            errors.append(f'Malformed score: {p[0]} {p[1]}')
    for r in rows:
        ds = scores.get((key(r), r['gene']))
        if ds is None:
            errors.append(f"{r['id']}: missing score for {r['gene']}")
        elif r['positive']:
            # First two are acceptor-loss controls; the remaining positives donor-loss.
            channel = 1 if r['id'] in ('SPL-01', 'SPL-02') else 3
            if ds[channel] < 0.5:
                errors.append(f"{r['id']}: expected loss channel >=0.5, got {ds[channel]:.2f}")
        elif max(ds) >= 0.2:
            errors.append(f"{r['id']}: negative control >=0.2")
    return errors


def fixture(rows):
    """Synthetic protocol fixture, never a measured model result."""
    lines = []
    for r in rows:
        ds = [0., 0., 0., 0.]
        if r['positive']:
            ds[1 if r['id'] in ('SPL-01', 'SPL-02') else 3] = 0.9
        lines.append(' '.join([key(r), r['gene'], *map(str, ds), str(max(ds)), 'fixture']))
    return '\n'.join(lines)


def self_test(rows):
    good = fixture(rows)
    faults = {
        'empty output': '', 'missing row': '\n'.join(good.splitlines()[:-1]),
        'all-zero output': good.replace('0.9', '0.0'),
        'nonfinite output': good.replace('0.9', 'nan'),
        'wrong chromosome convention': '\n'.join('chr'+s for s in good.splitlines()),
        'wrong gene': good.replace('WDR35', 'OTHER'),
        'duplicate row': good + '\n' + good.splitlines()[0],
        'out-of-range output': good.replace('0.9', '1.1'),
    }
    if evaluate(good, rows):
        raise AssertionError('Known-good protocol fixture rejected')
    for name, bad in faults.items():
        if not evaluate(bad, rows):
            raise AssertionError(f'Undetected failure: {name}')
    if not evaluate(good, rows, returncode=1):
        raise AssertionError('Runner failure accepted')
    print(f'PASS: harness rejected {len(faults)+1} injected failures and accepted its control.')
    print('This tests the harness, NOT SpliceAI inference. Run --splice with dependencies and reference for that.')
    return 0


def run_model(rows, runner, reference):
    if not runner.is_file() or not reference or not Path(reference).is_file():
        raise FileNotFoundError('Model runner and indexed GRCh38 FASTA required; set --reference or MVA_SPLICEAI_REFERENCE')
    with tempfile.TemporaryDirectory(prefix='mva-canary-') as tmp:
        vcf = Path(tmp) / 'public-controls.vcf'
        text = ['##fileformat=VCFv4.2']
        text += [f'##contig=<ID={c}>' for c in sorted({r['chrom'] for r in rows})]
        text += ['##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">',
                 '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tcanary']
        text += [f"{r['chrom']}\t{r['pos']}\t{r['id']}\t{r['ref']}\t{r['alt']}\t100\tPASS\t.\tGT\t0/1" for r in sorted(rows, key=lambda r:(r['chrom'],r['pos']))]
        vcf.write_text('\n'.join(text)+'\n')
        return subprocess.run([sys.executable, str(runner), str(vcf), '--reference', reference],
                              capture_output=True, text=True, timeout=600)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group()
    mode.add_argument('--self-test', action='store_true')
    mode.add_argument('--splice', action='store_true')
    mode.add_argument('--scores', type=Path, help='Evaluate previously captured model stdout; does not run inference')
    p.add_argument('--reference', default=os.environ.get('MVA_SPLICEAI_REFERENCE'))
    p.add_argument('--runner', type=Path, default=ROOT/'pipeline/spliceai_run.py')
    p.add_argument('--save-output', type=Path)
    args = p.parse_args()
    try:
        rows = load_panel()
        if args.self_test:
            return self_test(rows)
        if args.scores:
            output, code = args.scores.read_text(), 0
        else:
            proc = run_model(rows, args.runner, args.reference)
            output, code = proc.stdout, proc.returncode
            if code:
                print(proc.stderr[-2000:], file=sys.stderr)
        if args.save_output:
            args.save_output.write_text(output)
        errors = evaluate(output, rows, code)
        for error in errors:
            print('FAIL:', error)
        print(f'{len(rows)} controls requested; {len(errors)} failed assertions; inference={not bool(args.scores)}')
        return 1 if errors else 0
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f'NOT RUN: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
