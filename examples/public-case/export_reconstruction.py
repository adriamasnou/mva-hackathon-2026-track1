#!/usr/bin/env python3
"""Export completed, verified FGFR2 reconstructions; never execute Exomiser."""
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
import reconstruct as recipe

ROOT = Path(__file__).resolve().parent
BENCHMARK = ROOT.parent / 'public-benchmark'
MINI_SHA256 = '5d15afff2a67c073fe480595f312270b911087ff45ad1384cafdb207376699e0'
LIMIT = 32 * 1024 * 1024  # No raw JSONL, genome, database, JAR or large logs in this package.
CURRENT_SNAPSHOT = object()


def export(work, out):
    import yaml

    if out.exists():
        raise FileExistsError('Preserve prior exports; choose a NEW destination')
    runner = recipe.load_module('reconstruction_runner', BENCHMARK / 'run.py')
    evaluator = recipe.load_module('reconstruction_evaluator', BENCHMARK / 'evaluate.py')
    receipt = work / 'execution.json'
    execution = json.loads(receipt.read_text())
    if (execution.get('status') != 'completed' or execution.get('exit_code') != 0
            or execution.get('missing_outputs') != [] or execution.get('planned_jobs') != 2):
        raise ValueError('Both jobs must have completed successfully with no missing outputs')
    copies = {}
    checked = {}

    def verify(path, expected):
        path = Path(path)
        if path not in checked:
            checked[path] = recipe.sha(path)
        actual = checked[path]
        if not expected or actual != expected:
            raise ValueError('Missing or mismatched recorded SHA256: ' + str(path))
        return actual

    def retain(path, relative, expected=CURRENT_SNAPSHOT):
        path = Path(path)
        if path.stat().st_size > LIMIT:
            raise ValueError('Compact export limit exceeded: ' + str(path))
        if relative in copies:
            raise ValueError('Duplicate export filename: ' + relative)
        if expected is CURRENT_SNAPSHOT:
            expected = recipe.sha(path)
        copies[relative] = (path, verify(path, expected))

    manifest = work / 'jobs-manifest.json'
    retain(manifest, manifest.name, execution.get('jobs_manifest_sha256'))
    jobs = json.loads(manifest.read_text())
    if [j['case_id'] for j in jobs] != ['mini', 'genome'] or any(j['gene'] != 'FGFR2' for j in jobs):
        raise ValueError('Expected exactly the mini and genome FGFR2 reconstructions, in that order')
    expected_outputs = {j['result_jsonl'] for j in jobs}
    if set(execution.get('outputs', {})) != expected_outputs:
        raise ValueError('Execution output membership differs from the two-job manifest')
    retain(receipt, receipt.name)
    retain(work / 'batch.txt', 'batch.txt', execution.get('batch_sha256'))
    if (work / 'batch.txt').read_text().splitlines() != [recipe.batch_line(j['job']) for j in jobs]:
        raise ValueError('Batch must contain literal unquoted --analysis job paths')
    runner.check_batch(work / 'batch.txt', jobs)
    properties = work / 'runtime.properties'
    retain(properties, properties.name, execution.get('properties_sha256'))
    if properties.read_text() != execution.get('properties_text'):
        raise ValueError('Runtime properties text differs from execution receipt')
    retain(work / 'execution.log', 'execution.log', execution.get('log_sha256'))
    retain(BENCHMARK / 'run.py', 'code/run.py', execution.get('wrapper_sha256'))
    retain(BENCHMARK / 'evaluate.py', 'code/evaluate.py', execution.get('evaluation_script_sha256'))
    if not execution.get('software_sha256') or not execution.get('data_receipts'):
        raise ValueError('Execution lacks software or database provenance')
    for path, expected in execution['software_sha256'].items():
        verify(path, expected)
    for i, (path, record) in enumerate(execution['data_receipts'].items(), 1):
        retain(path, f'data-receipts/{i}-{Path(path).name}', record['sha256'])
        if json.loads(Path(path).read_text()) != record['content']:
            raise ValueError('Database receipt content differs from execution receipt')
    protocol = work / 'protocol-before-inference.json'
    preparation = work / 'preparation-receipt.json'
    design_paths = [p for p in (protocol, preparation) if p.exists()]
    design_bound = 'design_records' in execution
    if design_bound:
        if set(execution['design_records']) != {p.name for p in design_paths}:
            raise ValueError('Design record membership differs from execution receipt')
        for path in design_paths:
            record = execution['design_records'][path.name]
            retain(path, path.name, record.get('sha256'))
            if json.loads(path.read_text()) != record.get('content'):
                raise ValueError('Design record content differs from execution: ' + path.name)
    else:
        for path in design_paths:
            retain(path, path.name)
    if json.loads(protocol.read_text()).get('template_sha256') != recipe.TEMPLATE_SHA256:
        raise ValueError('Unexpected reconstruction template provenance')
    verify(ROOT / 'job-template.yml', recipe.TEMPLATE_SHA256)
    for path in sorted(work.glob('addendum-*.json')):
        record = execution.get('pre_inference_addenda', {}).get(path.name, {})
        retain(path, path.name, record.get('sha256'))
        if not record or json.loads(path.read_text()) != record.get('content'):
            raise ValueError('Addendum was not bound to execution: ' + path.name)
    if set(execution.get('pre_inference_addenda', {})) != {p.name for p in work.glob('addendum-*.json')}:
        raise ValueError('An executed addendum is missing')
    invocation_evidence = [work / 'dry-run.log', *sorted(work.glob('batch-before-*.txt')),
                           *sorted((work / 'dry-run-attempts').rglob('*'))]
    for path in invocation_evidence:
        if path.is_file():
            retain(path, str(path.relative_to(work)))
    for path in [Path(__file__), ROOT / 'reconstruct.py', ROOT / 'prepare.py',
                 ROOT / 'job-template.yml', ROOT / 'clinvar-smoke-variants.tsv', ROOT / 'README.md']:
        retain(path, 'recipe/' + path.name)
    retain(ROOT / 'verify_reconstruction.py', 'verify_reconstruction.py')
    retain(ROOT / 'test_verify_reconstruction.py', 'test_verify_reconstruction.py')
    history_path = ROOT / 'historical-result-summary.json'
    retain(history_path, history_path.name)
    history = {r['case']: r for r in json.loads(history_path.read_text())['results']}
    results, comparisons, scores, audits = [], [], {}, []
    for job in jobs:
        case = job['case_id']
        for kind in ('job', 'vcf'):
            verify(job[kind], job[kind + '_sha256'])
            if execution.get('inputs_sha256', {}).get(job[kind]) != job[kind + '_sha256']:
                raise ValueError('Executed input differs from manifest: ' + job[kind])
        # Accept only the public fixture, never an arbitrary genotype-scale input.
        if case == 'mini':
            verify(job['vcf'], MINI_SHA256)
        elif job['vcf_sha256'] != recipe.HISTORICAL_SHA256:
            if not preparation.exists():
                raise ValueError('A rebuilt genome requires its preparation receipt')
            prep = json.loads(preparation.read_text())
            verify(prep['background'], recipe.BACKGROUND_SHA256)
            if prep.get('genome_sha256') != job['vcf_sha256']:
                raise ValueError('Rebuilt genome does not match preparation receipt')
            recipe.audit_background(Path(prep['background']), Path(job['vcf']))
        expected = yaml.safe_load((ROOT / 'job-template.yml').read_text())
        expected['phenopacket']['id'] = case
        expected['phenopacket']['subject']['id'] = 'smoke' if case == 'mini' else 'HG002'
        expected['phenopacket']['htsFiles'][0]['uri'] = job['vcf']
        expected['outputOptions'].update(outputDirectory=str(Path(job['result_jsonl']).parent), outputFileName=case)
        if yaml.safe_load(Path(job['job']).read_text()) != expected:
            raise ValueError('Job differs from the declared FGFR2 reconstruction: ' + case)
        retain(job['job'], 'jobs/' + case + '.yml', job['job_sha256'])
        raw = Path(job['result_jsonl'])
        verify(raw, execution['outputs'][str(raw)])
        rows, matches = [], []
        with raw.open() as stream:
            for line in stream:
                if not line.strip():
                    continue
                gene = json.loads(line)
                row = {k: gene.get(k) for k in ['geneSymbol', 'combinedScore', 'priorityScore', 'variantScore', 'pValue']}
                for name in ['priorityScore', 'variantScore', 'pValue']:
                    value = row[name]
                    if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)):
                        raise ValueError('Invalid gene score: ' + case + '/' + name)
                rows.append(row)
                if gene['geneSymbol'] == 'FGFR2':
                    for variant in gene.get('variantEvaluations', []):
                        key = (str(variant['contigName']).removeprefix('chr'), variant['start'], variant['ref'], variant['alt'])
                        if key == ('10', 121517378, 'C', 'T'):
                            matches.append({k: variant.get(k) for k in ['filterStatus', 'contributesToGeneScore',
                                'whiteListed', 'passedFilterTypes', 'failedFilterTypes', 'variantScore',
                                'compatibleInheritanceModes', 'contributingInheritanceModes']})
        if not rows:
            raise ValueError('Empty result file: ' + str(raw))
        if recipe.sha(raw) != execution['outputs'][str(raw)]:
            raise ValueError('Output changed while reading: ' + str(raw))
        result = {'case_id': case, 'gene': 'FGFR2', **evaluator.rank_records(rows, 'FGFR2'),
                  'output_sha256': execution['outputs'][str(raw)]}
        results.append(result)
        scores[case] = sorted(rows, key=lambda r: (-r['combinedScore'], r['geneSymbol']))
        audits.append({'case_id': case, 'coordinate': 'GRCh38 chr10:121517378 C>T',
                       'input_gt': '0/1', 'exact_matches_in_FGFR2_output': len(matches), 'matches': matches,
                       'scope': 'GT is established by the pinned/verified input. JSONL may omit genotype. '
                                'Gene rank alone does not establish spike contribution; an unmatched allele needs review.'})
        old = history['mini' if case == 'mini' else 'HG002-spiked']
        old_fgfr2 = next(r for r in old['top'] if r['geneSymbol'] == 'FGFR2')
        comparisons.append({'case_id': case,
            'historical': {'rank': 1, 'rank_basis': 'Retained August summary; only top rows bundled',
                           'scored_genes': old['gene_records'], 'source_jsonl_sha256': old['source_sha256'], **old_fgfr2},
            'new_reconstructed': result,
            'interpretation': 'Different executions with unrecovered August YAML; score/rank differences are not a controlled performance comparison.'})
    if sum(p.stat().st_size for p, _ in copies.values()) > 4 * LIMIT:
        raise ValueError('Compact export would exceed 128 MiB')
    out.mkdir(parents=True)
    for relative, (source, expected) in copies.items():
        target = out / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with source.open('rb') as src, target.open('xb') as dst:
            shutil.copyfileobj(src, dst)
        if recipe.sha(target) != expected:
            raise ValueError('Source changed while copying; partial export retained: ' + str(source))
    (out / 'gene-scores').mkdir()
    for case, rows in scores.items():
        counts = Counter(r['combinedScore'] for r in rows)
        bounds, before = {}, 0
        for score, count in sorted(counts.items(), reverse=True):
            bounds[score] = (before + 1, before + count)
            before += count
        with (out / 'gene-scores' / (case + '.tsv')).open('x') as stream:
            writer = csv.DictWriter(stream, delimiter='\t', fieldnames=[
                'rank_min', 'rank_max', 'geneSymbol', 'combinedScore', 'priorityScore', 'variantScore', 'pValue'])
            writer.writeheader()
            for row in rows:
                lo, hi = bounds[row['combinedScore']]
                writer.writerow({'rank_min': lo, 'rank_max': hi, **row})
    recipe.write_json(out / 'evaluation.json', {
        'interpretation': 'Known-variant FGFR2 execution controls, not diagnostic accuracy or therapeutic evidence.',
        'tie_policy': 'Full-precision combined scores; exact ties retain best and worst rank.',
        'all_case_results': results})
    recipe.write_json(out / 'historical-vs-reconstructed.json', comparisons)
    recipe.write_json(out / 'source-variant-audit.json', audits)
    recipe.write_json(out / 'export-receipt.json', {
        'status': 'verified_compact_export', 'created_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Every scored gene, exact jobs/config/batch/log, runtime/software/input/output hashes and database receipts. '
                 'Genome VCFs, raw output JSONL, JARs and databases remain at source paths; not copied.',
        'design_record_binding': 'Hashes and JSON content verified against execution.design_records' if design_bound
                                 else 'Older receipt without design_records: current snapshots only; no execution-time binding asserted',
        'limits': ['Database receipts are retained and checked against execution, not a fresh readback of large bundles.',
                   'Execution-bound design hashes show which documents the runner retained, not independent proof of preregistration.',
                   'Historical summary is retained, not a fresh audit of all historical results.',
                   'Raw JSONL hashes come from execution; compact score files are newly derived and separately hashed.'],
        'execution_receipt_sha256': checked[receipt],
        'file_sha256': {str(p.relative_to(out)): recipe.sha(p) for p in sorted(out.rglob('*')) if p.is_file()}})
    return out / 'export-receipt.json'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    print(export(args.work.resolve(), args.out.resolve()))
