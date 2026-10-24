#!/usr/bin/env python3
"""Verify and replay the frozen sensitivity companion offline, without changing it."""
import sys
sys.dont_write_bytecode = True

import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
SOURCE_SHA = 'ddf90f9eaebab874d45805f2345e05246a9fdd61a0d348259770b3c1d10854a0'
DETERMINISTIC = ('methods.json', 'joined-cases.jsonl', 'all-strata.json', 'frozen-baseline-strata.json', 'findings.json')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def check_manifest(root):
    manifest = read(root / 'package-manifest.json')
    require(manifest['source_manifest_sha256'] == SOURCE_SHA, 'Wrong source freeze')
    paths = list(root.rglob('*'))
    require(not any(p.is_symlink() for p in paths), 'Package contains a symlink')
    files = manifest['files']
    actual = {p.relative_to(root).as_posix() for p in paths if p.is_file()}
    require(actual == set(files) | {'package-manifest.json'}, 'Package file set differs from manifest')
    for name, record in files.items():
        rel = PurePosixPath(name)
        require(not rel.is_absolute() and '..' not in rel.parts and '\\' not in name,
                'Unsafe manifest path: ' + name)
        p = root / name
        require(p.stat().st_size == record['bytes'] and sha(p) == record['sha256'],
                'Package hash/size mismatch: ' + name)
    return manifest


def check_provenance(root):
    original = root / 'provenance/analysis-2031'
    delivery = read(original / 'delivery-manifest.json')
    require(sha(original / 'delivery-manifest.json') ==
            (original / 'delivery-manifest.sha256').read_text().split()[0], 'Original seal mismatch')
    for name, record in delivery['local_deliverables'].items():
        require(sha(original / name) == record['sha256'] and
                (original / name).stat().st_size == record['bytes'], 'Original file changed: ' + name)
    for record in delivery['external_verifier_reports']:
        p = root / Path(record['path']).name
        require(sha(p) == record['sha256'] and p.stat().st_size == record['bytes'],
                'Archived benchmark verification changed')
    parent = read(root / 'provenance/parent/sensitivity-2031-independent-verification.json')
    require(parent['passed'] is True and parent['source_manifest_sha256'] == SOURCE_SHA,
            'Parent receipt not passed or wrong freeze')
    require(sha(root / 'provenance/parent/check-sensitivity-2031.py') == parent['code_sha256'],
            'Parent code changed')
    for name, digest in parent['analysis_deliverables'].items():
        require(sha(original / name) == digest, 'Parent verification binding changed: ' + name)
    return original, parent


def compare_volatile_receipt(actual, expected, volatile, label):
    """Exclude only named environment/time fields; all substantive fields must match."""
    require(set(actual) == set(expected), label + ' receipt fields changed')
    for key in actual:
        if key not in volatile:
            require(actual[key] == expected[key], label + ' receipt changed: ' + key)


def run_python_checks(root, original, parent_receipt, work):
    analysis = load('analyze', original / 'analyze.py')
    tests = load('test_analysis', original / 'test_analysis.py')
    suite = unittest.defaultTestLoader.loadTestsFromModule(tests)
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    require(result.wasSuccessful() and result.testsRun == 29, 'Original 29 tests failed:\n' + log.getvalue())

    # Preserve every source byte. Only runtime location globals/argv are replaced.
    analysis.HERE = work
    analysis.INPUT_ROOT = root / 'inputs'
    shutil.copyfile(original / 'immutable-input-hashes.json', work / 'immutable-input-hashes.json')
    previous_argv = sys.argv
    try:
        sys.argv = ['analyze.py', '--input-root', str(root / 'inputs')]
        with contextlib.redirect_stdout(io.StringIO()):
            analysis.main()
    finally:
        sys.argv = previous_argv
    for name in DETERMINISTIC[:-1]:
        require((work / name).read_bytes() == (original / name).read_bytes(),
                'Regenerated output differs byte-for-byte: ' + name)
    regenerated = read(work / 'validation.json')
    frozen = read(original / 'validation.json')
    compare_volatile_receipt(regenerated, frozen, {'at_utc', 'benchmark_verifier'}, 'Analysis')
    compare_volatile_receipt(regenerated['benchmark_verifier'], frozen['benchmark_verifier'],
                             {'path'}, 'Benchmark')

    # seal.py derives findings.json as well as a time/path-dependent seal.
    # Its base is __file__.parent, so relocate only that runtime path to scratch.
    for path in original.iterdir():
        if path.is_file() and not (work / path.name).exists():
            shutil.copyfile(path, work / path.name)
    seal = load('frozen_seal', original / 'seal.py')
    seal.__file__ = str(work / 'seal.py')
    with contextlib.redirect_stdout(io.StringIO()):
        seal.main()
    require((work / 'findings.json').read_bytes() == (original / 'findings.json').read_bytes(),
            'Regenerated findings differ byte-for-byte')

    # The unchanged parent implementation recomputes from scores/exact PASSED alleles.
    parent = load('parent_check', root / 'provenance/parent/check-sensitivity-2031.py')
    parent.HERE = work
    parent.ANALYSIS = original
    parent.ROOT = root / 'inputs'
    with contextlib.redirect_stdout(io.StringIO()):
        parent.main()
    fresh_parent = read(work / 'sensitivity-2031-independent-verification.json')
    compare_volatile_receipt(fresh_parent, parent_receipt, {'checked_at_utc'}, 'Parent')
    return {'original_tests_passed': result.testsRun,
            'deterministic_outputs_byte_identical': list(DETERMINISTIC),
            'source_snapshot_verifier_errors': regenerated['source_snapshot_verifier_errors'],
            'independent_parent_recomputation': 'passed',
            'receipt_comparison_exclusions': ['analysis.at_utc', 'analysis.benchmark_verifier.path',
                                              'parent.checked_at_utc']}


def check_html(root, work):
    builder = load('build_viewer', root / 'build_viewer.py')
    html = (root / 'index.html').read_text(encoding='utf-8')
    require(html == builder.render(root), 'HTML differs from deterministic viewer build')
    data, script = builder.extract(html)
    require(data['strata'] == read(root / 'provenance/analysis-2031/all-strata.json'),
            'Embedded HTML data differs from all-strata.json')
    require(data['methods'] == read(root / 'provenance/analysis-2031/methods.json'),
            'Embedded definitions differ from frozen methods')
    entries = [s for c in data['strata'].values() for d in c['source_audit_strata'].values() for s in d.values()]
    require(len(entries) == 162 and sum(s['case_denominator'] == 0 for s in entries) == 15,
            'HTML category/empty-category count changed')
    node = shutil.which('node')
    js_status = 'not run: Node.js unavailable; exact prechecked script bytes verified'
    if node:
        script_path = work / 'viewer.js'
        script_path.write_text(script, encoding='utf-8')
        syntax = subprocess.run([node, '--check', str(script_path)], capture_output=True, text=True)
        require(syntax.returncode == 0, 'Node syntax check failed: ' + syntax.stderr)
        smoke = subprocess.run([node, str(root / 'test_viewer.cjs'), str(root / 'index.html')],
                               capture_output=True, text=True)
        require(smoke.returncode == 0, 'Viewer rendering checks failed: ' + smoke.stdout + smoke.stderr)
        js_status = json.loads(smoke.stdout)
    return {'embedded_data_exact': True, 'categories': len(entries), 'empty_categories': 15,
            'node_checks': js_status}


def deny_network(event, args):
    if event in ('socket.connect', 'socket.connect_ex', 'socket.getaddrinfo', 'socket.bind'):
        raise RuntimeError('Network access is disabled by the offline verifier')


def main():
    require(sys.version_info >= (3, 11), 'Python 3.11 or newer is required')
    require(__debug__, 'Run without -O/PYTHONOPTIMIZE; original parent checks use assertions')
    sys.addaudithook(deny_network)
    before = sha(ROOT / 'package-manifest.json')
    manifest = check_manifest(ROOT)
    original, parent = check_provenance(ROOT)
    portable_tests = load('test_portable', ROOT / 'test_portable.py')
    log = io.StringIO()
    portable_result = unittest.TextTestRunner(stream=log).run(
        unittest.defaultTestLoader.loadTestsFromModule(portable_tests))
    require(portable_result.wasSuccessful() and portable_result.testsRun == 8,
            'Portable integrity controls failed: ' + log.getvalue())
    with tempfile.TemporaryDirectory(prefix='source-quality-check-') as temp:
        work = Path(temp)
        require(not work.is_relative_to(ROOT), 'Temporary directory must be outside the package')
        checks = run_python_checks(ROOT, original, parent, work)
        viewer = check_html(ROOT, work)
    require(sha(ROOT / 'package-manifest.json') == before, 'Manifest changed during verification')
    check_manifest(ROOT)
    print(json.dumps({'passed': True, 'scope': 'Offline software replay of existing verified analysis',
                      'source_manifest_sha256': SOURCE_SHA, 'package_manifest_sha256': before,
                      'package_files_hashed': len(manifest['files']), 'frozen_inputs': 621,
                      'cases': 713, 'arm_rows': 1426, 'cohorts': 6, 'dimensions': 7,
                      'portable_integrity_controls_passed': portable_result.testsRun,
                      **checks, 'viewer': viewer, 'package_unchanged': True,
                      'benchmark_raw_verification': 'Archived original receipt hash-checked; full raw benchmark not rerun here',
                      'limits': 'Post hoc, non-blinded, per_case exposure. Source correspondence is not clinical truth; no inference or biomedical source review.'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
