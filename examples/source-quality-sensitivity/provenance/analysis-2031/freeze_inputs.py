#!/usr/bin/env python3
"""Freeze only the explicitly requested public snapshots; never change originals."""
import hashlib
import json
import os
from pathlib import Path
import shutil
from datetime import datetime, timezone

ROOT = Path('/Users/adriamasnou/mva-hackathon')
HERE = Path(__file__).resolve().parent
FROZEN = Path('/Volumes/easystore/MVA-deadline-build-20261024/sensitivity-2031/inputs')
EXPECTED = {
    'source/manifest.json': 'ddf90f9eaebab874d45805f2345e05246a9fdd61a0d348259770b3c1d10854a0',
    'benchmark/cases.json': '816f87efa1fc2bfcf8f0b6f3c9326cbb01f62c601f8ecaae4208d02086bd45fc',
    'benchmark/evaluations/corrected-v2.json': '54f7e82cbe62cc8f41913b7f3c8069cba4dd4ae26a3769bfec5f5def893ab9b5',
}

def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def main():
    source = ROOT / 'repo/examples/compact-source-audit'
    benchmark = ROOT / 'repo/examples/compact-benchmark/results-20261024-v1'
    assert not FROZEN.exists(), 'Never overwrite a frozen input tree'
    assert sha(source / 'manifest.json') == EXPECTED['source/manifest.json']
    files = {f'source/{p.relative_to(source)}': p for p in source.rglob('*')
             if p.is_file() and '__pycache__' not in p.parts}
    for name in ('cases.json', 'evaluations/corrected-v2.json', 'evaluations/original.json',
                 'verify.py', 'test_verify.py', 'README.md', 'export-receipt.json',
                 'protocol-before-inference.json'):
        files['benchmark/' + name] = benchmark / name
    hashes = {name: sha(p) for name, p in files.items()}
    for name, expected in EXPECTED.items():
        assert hashes[name] == expected, name
    FROZEN.mkdir(parents=True)
    entries = []
    for name, p in files.items():
        assert not p.is_symlink(), p
        target = FROZEN / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
        with target.open('rb') as f:
            os.fsync(f.fileno())
        assert sha(target) == hashes[name] == sha(p), name
        target.chmod(0o444)
        entries.append({'relative_path': name, 'original_path': str(p),
                        'frozen_path': str(target), 'sha256': hashes[name],
                        'bytes': target.stat().st_size})
    # Verify the whole source manifest rather than trusting the advertised count.
    manifest = json.loads((FROZEN / 'source/manifest.json').read_text())
    assert set(manifest['files']) == {n.removeprefix('source/') for n in files
                                     if n.startswith('source/') and n != 'source/manifest.json'}
    for name, digest in manifest['files'].items():
        assert hashes['source/' + name] == digest, name
    receipt = {'created_at_utc': datetime.now(timezone.utc).isoformat(),
               'private': True, 'post_hoc': True, 'outcome_exposure': 'per_case',
               'input_root': str(FROZEN), 'expected_hashes': EXPECTED,
               'files': sorted(entries, key=lambda r: r['relative_path']),
               'note': 'Read-only byte copies with durable hashes; no external signature. '
                       'Full raw benchmark remains in its unchanged original bundle and is '
                       'checked by the existing offline verifier. No inference rerun.'}
    out = HERE / 'immutable-input-hashes.json'
    with out.open('x') as f:
        json.dump(receipt, f, indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
    for directory in sorted([p for p in FROZEN.rglob('*') if p.is_dir()] + [FROZEN], reverse=True):
        fd = os.open(directory, os.O_RDONLY); os.fsync(fd); os.close(fd)
        directory.chmod(0o555)
    print(json.dumps({'frozen_files': len(entries), 'bytes': sum(x['bytes'] for x in entries),
                      'receipt': str(out), 'receipt_sha256': sha(out)}))

if __name__ == '__main__':
    main()
