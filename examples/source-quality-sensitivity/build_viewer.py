#!/usr/bin/env python3
"""Deterministically embed the complete frozen summaries in the offline viewer."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def render(root=ROOT):
    original = root / 'provenance/analysis-2031'
    payload = {
        'strata': read(original / 'all-strata.json'),
        'methods': read(original / 'methods.json'),
        'findings': read(original / 'findings.json'),
        'parent_verification': read(root / 'provenance/parent/sensitivity-2031-independent-verification.json'),
        'hashes': {name: hashlib.sha256((original / name).read_bytes()).hexdigest()
                   for name in ('all-strata.json', 'methods.json', 'joined-cases.jsonl')},
    }
    inline = json.dumps(payload, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
    inline = inline.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    template = (root / 'viewer.template.html').read_text(encoding='utf-8')
    if template.count('@@FROZEN_DATA@@') != 1:
        raise ValueError('Expected one data placeholder')
    return template.replace('@@FROZEN_DATA@@', inline)


def extract(html):
    data = re.search(r'<script id="frozen-data" type="application/json">(.*?)</script>', html, re.S)
    script = re.search(r'<script id="viewer-code">(.*?)</script>', html, re.S)
    if not data or not script:
        raise ValueError('Missing inline data or viewer code')
    return json.loads(data.group(1)), script.group(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='Explicit output path; no files overwritten by default')
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Refuse to overwrite existing file')
    args.output.write_text(render(), encoding='utf-8')
