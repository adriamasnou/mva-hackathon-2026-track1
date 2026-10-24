#!/usr/bin/env python3
"""Package a completed, explicitly released compact713 run; never runs inference."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
import verify

HERE = Path(__file__).resolve().parent
SOURCE_ROOT = HERE.parents[2]


def write_new(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def export_bundle(work, out, source_root, cases_path, original, corrected, correction_dir,
                  parent_ready=False):
    """The ready assertion is an operator decision, never inferred from completion."""
    verify.require(parent_ready, 'Parent readiness is required in addition to terminal execution')
    work, out, source_root = (Path(p).resolve() for p in (work, out, source_root))
    verify.require(not out.exists() and not out.is_symlink(), 'Never overwrite an existing version')
    execution_path = work / 'execution.json'
    execution = verify.read_json(execution_path)
    verify.terminal(execution)  # Before creating any directory or copying outputs.
    jobs = verify.read_json(work / 'jobs-manifest.json')
    cases = verify.read_json(cases_path)['cases']
    verify.require(verify.sha(cases_path) == verify.CASE_SHA, 'Wrong full713 source case file')
    verify.require(verify.sha(work / 'cases.json') == verify.CASE_SHA, 'Executed cases changed')
    verify.ledger(cases, jobs)
    sources, included, omitted = {}, {}, {}

    def add(source, portable):
        source = Path(source)
        verify.require(not source.is_symlink() and source.is_file(), 'Missing/symlink source: ' + str(source))
        source = source.resolve()
        verify.require(portable not in sources, 'Duplicate portable destination: ' + portable)
        verify.require(str(source) not in included, 'Duplicate source mapping: ' + str(source))
        sources[portable] = source
        included[str(source)] = portable

    for name in ('execution.json', 'jobs-manifest.json', 'protocol-before-inference.json',
                 'preparation-receipt.json', 'runtime.properties', 'batch.txt', 'execution.log'):
        add(work / name, name)
    add(cases_path, 'cases.json')
    included[str(work / 'cases.json')] = 'cases.json'
    verify.require(isinstance(execution.get('pre_inference_addenda'), dict), 'Missing addenda object')
    for name in execution['pre_inference_addenda']:
        verify.require(Path(name).name == name and name.startswith('addendum-') and name.endswith('.json'),
                       'Unexpected addendum filename')
        add(work / name, name)
    for i, source in enumerate(sorted(execution['data_receipts'])):
        verify.require(Path(source).resolve().parent == work.parents[1], 'Unexpected public data receipt path')
        add(source, 'data-receipts/' + str(i) + '-' + Path(source).name)
    for job in jobs:
        stem = job['case_id'] + '.' + job['arm']
        for field, expected in [('job', work / 'jobs' / (stem + '.yml')),
                                ('result_jsonl', work / 'results' / (stem + '.jsonl')),
                                ('vcf', work / 'inputs' / (job['case_id'] + '.vcf'))]:
            verify.require(job[field] == str(expected) and not expected.is_symlink(),
                           'Unexpected executed public path: ' + field)
        add(job['job'], 'jobs/' + stem + '.yml')
        add(job['result_jsonl'], 'raw/' + stem + '.jsonl')
        omitted[job['vcf']] = job['vcf_sha256']
    # Read public compact VCFs only to confirm unchanged executed bytes. Never copy.
    for path, digest in omitted.items():
        verify.require(verify.sha(path) == digest, 'Executed public VCF changed: ' + path)
    temporal = source_root / 'pipeline/public_validation/temporal_compact'
    add(temporal / 'evaluate_adapter.py', 'code/original/evaluate_adapter.py')
    add(temporal.parent / 'evaluate_temporal_compact.py', 'code/original/joint_mode.py')
    base = source_root / 'repo/examples/public-benchmark'
    for name in ('evaluate.py', 'export_results.py', 'run.py', 'export_provenance.py'):
        add(base / name, 'code/reused/' + name)
    correction_dir = Path(correction_dir).resolve()
    correction = verify.read_json(correction_dir / 'correction-receipt.json')
    for name in ('evaluate_adapter.py', 'joint_mode.py'):
        add(correction_dir / name, 'code/correction-v2/' + name)
    for name in ('correction-receipt.json', 'adapter.diff', 'helper.diff', *correction['evidence_sha256']):
        verify.require(Path(name).name == name, 'Unsafe correction evidence path')
        add(correction_dir / name, 'correction-v2/' + name)
    for name in ('ModeScoreProbe.java', 'output.txt', 'receipt.json'):
        add(correction_dir / 'serialization-probe' / name, 'correction-v2/serialization-probe/' + name)
    add(temporal / 'source-reading-crosscheck.json', 'source-reading-crosscheck.json')
    add(original, 'evaluations/original.json')
    add(corrected, 'evaluations/corrected-v2.json')
    for name in ('verify.py', 'export.py', 'test_verify.py', 'README.md'):
        add(HERE / name, name)
    before = {name: verify.sha(path) for name, path in sources.items()}
    verify.require(before['execution.json'] == verify.sha(execution_path), 'Execution changed during preparation')
    # Stage only after completion/readiness and full input preflight. No final version
    # exists until the staged bundle has passed its own standalone verifier.
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.' + out.name + '.staging-', dir=out.parent) as staging:
        stage = Path(staging)
        for name, source in sources.items():
            destination = stage / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            with source.open('rb') as src, destination.open('xb') as dst:
                shutil.copyfileobj(src, dst)
            verify.require(verify.sha(destination) == before[name], 'Source changed while copying: ' + name)
        write_new(stage / 'path-map.json', {'included': included, 'omitted_vcf_sha256': omitted,
            'note': 'Original files retain absolute provenance strings. Resolve included files only through this map; no inference rerun is provided.'})
        inventory = dict(before, **{'path-map.json': verify.sha(stage / 'path-map.json')})
        write_new(stage / 'export-receipt.json', {
            'schema': 'compact713-portable-v1', 'exported_utc': datetime.now(timezone.utc).isoformat(),
            'parent_release_ready_asserted': True, 'source_work': str(work),
            'source_case_path': str(Path(cases_path).resolve()), 'file_sha256': inventory,
            'excluded': ['VCFs', 'Java binaries', 'databases'], 'limitations': verify.LIMITS})
        result = verify.verify_bundle(stage)
        # Detect changes between preflight and release, including inputs deliberately
        # omitted from the portable package. No source file is modified.
        for name, source in sources.items():
            verify.require(verify.sha(source) == before[name], 'Source changed before release: ' + name)
        for path, digest in omitted.items():
            verify.require(verify.sha(path) == digest, 'VCF changed before release: ' + path)
        out.mkdir()  # Exclusive creation: also rejects a concurrently created version.
        # Move within the same filesystem, without a second ~120 MB copy. Receipt last.
        for child in sorted(stage.iterdir(), key=lambda p: p.name == 'export-receipt.json'):
            child.rename(out / child.name)
    return {k: result[k] for k in ('status', 'files', 'raw_outputs', 'cases', 'case_arm_rows',
                                  'preparation_failures_per_arm', 'export_receipt_sha256')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True, help='New immutable version directory')
    parser.add_argument('--source-root', type=Path, default=SOURCE_ROOT)
    parser.add_argument('--cases', type=Path, required=True)
    parser.add_argument('--original-evaluation', type=Path, required=True)
    parser.add_argument('--corrected-evaluation', type=Path, required=True)
    parser.add_argument('--correction-dir', type=Path, required=True)
    parser.add_argument('--parent-ready', action='store_true',
                        help='Assert parent has explicitly approved export after completion')
    args = parser.parse_args()
    try:
        result = export_bundle(args.work, args.out, args.source_root, args.cases,
                               args.original_evaluation, args.corrected_evaluation,
                               args.correction_dir, args.parent_ready)
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as error:
        print('EXPORT REFUSED: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
