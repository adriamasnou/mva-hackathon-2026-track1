"""Small synthetic package checks; no original work directory or inference is used."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('offline_reconstruction', ROOT / 'verify_reconstruction.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class OfflinePackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='fgfr2-offline-')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.package = self.base / 'compact'
        self.package.mkdir()
        self.unavailable = self.base / 'source-directory-that-never-existed'
        self.build_fixture()

    def put(self, name, value):
        path = self.package / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + '\n' if not isinstance(value, str) else value)

    def get(self, name):
        return json.loads((self.package / name).read_text())

    def digest(self, name):
        return verifier.sha(self.package / name)

    def reseal(self):
        receipt = self.get('export-receipt.json')
        receipt['file_sha256'] = {p.relative_to(self.package).as_posix(): verifier.sha(p)
                                 for p in self.package.rglob('*') if p.is_file() and p.name != 'export-receipt.json'}
        receipt['execution_receipt_sha256'] = self.digest('execution.json')
        self.put('export-receipt.json', receipt)

    def build_fixture(self):
        jobs, results, comparisons, historical, audits = [], [], [], [], []
        for case in ('mini', 'genome'):
            source_job = str(self.unavailable / 'jobs' / (case + '.yml'))
            self.put('jobs/' + case + '.yml', '# Synthetic binding fixture; never executed\nphenopacket: {id: ' + case + '}\n')
            job = {'case_id': case, 'gene': 'FGFR2', 'job': source_job,
                   'job_sha256': self.digest('jobs/' + case + '.yml'),
                   'vcf': str(self.unavailable / (case + '.vcf')), 'vcf_sha256': 'a' * 64,
                   'result_jsonl': str(self.unavailable / (case + '.jsonl'))}
            jobs.append(job)
            self.put('gene-scores/' + case + '.tsv',
                     'rank_min\trank_max\tgeneSymbol\tcombinedScore\tpriorityScore\tvariantScore\tpValue\n'
                     '1\t1\tHIGHER\t0.9\t0.8\t1.0\t0.01\n'
                     '2\t3\tFGFR2\t0.5\t0.4\t0.7\t0.2\n'
                     '2\t3\tTIED\t0.5\t0.3\t0.8\t0.2\n')
            result = {'case_id': case, 'gene': 'FGFR2', 'status': 'scored', 'rank_min': 2, 'rank_max': 3,
                      'scored_genes': 3, 'combined_score': 0.5, 'priority_score': 0.4,
                      'variant_score': 0.7, 'output_sha256': 'b' * 64}
            results.append(result)
            old_row = {'geneSymbol': 'FGFR2', 'combinedScore': 0.9, 'priorityScore': 0.8, 'variantScore': 1.0}
            old = {'case': 'mini' if case == 'mini' else 'HG002-spiked', 'source_sha256': 'c' * 64,
                   'gene_records': 3, 'top': [old_row]}
            historical.append(old)
            comparisons.append({'case_id': case, 'new_reconstructed': copy.deepcopy(result),
                                'historical': {'rank': 1, 'rank_basis': 'Retained August summary; only top rows bundled',
                                               'scored_genes': 3, 'source_jsonl_sha256': 'c' * 64, **old_row}})
            audits.append({'case_id': case, 'fixture_only': True})
        self.put('jobs-manifest.json', jobs)
        self.put('batch.txt', ''.join('--analysis ' + j['job'] + '\n' for j in jobs))
        self.put('runtime.properties', 'fixture_only=true\n')
        self.put('execution.log', 'Synthetic fixture only; no inference\n')
        self.put('code/run.py', '# synthetic recorded wrapper\n')
        self.put('code/evaluate.py', '# synthetic recorded evaluator\n')
        self.put('protocol-before-inference.json', {'fixture_only': True})
        self.put('data-receipts/1-database.json', {'fixture_only': True})
        self.put('evaluation.json', {'all_case_results': results})
        self.put('historical-vs-reconstructed.json', comparisons)
        self.put('historical-result-summary.json', {'results': historical})
        self.put('source-variant-audit.json', audits)
        shutil.copyfile(ROOT / 'verify_reconstruction.py', self.package / 'verify_reconstruction.py')
        self.put('execution.json', {
            'fixture_only': True, 'status': 'completed', 'exit_code': 0, 'planned_jobs': 2, 'missing_outputs': [],
            'jobs_manifest_sha256': self.digest('jobs-manifest.json'), 'batch_sha256': self.digest('batch.txt'),
            'properties_sha256': self.digest('runtime.properties'), 'properties_text': 'fixture_only=true\n',
            'log_sha256': self.digest('execution.log'), 'wrapper_sha256': self.digest('code/run.py'),
            'evaluation_script_sha256': self.digest('code/evaluate.py'),
            'software_sha256': {str(self.unavailable / 'runtime.jar'): 'd' * 64},
            'design_records': {'protocol-before-inference.json': {'sha256': self.digest('protocol-before-inference.json'),
                                                                 'content': {'fixture_only': True}}},
            'pre_inference_addenda': {},
            'data_receipts': {str(self.unavailable / 'database.json'): {'sha256': self.digest('data-receipts/1-database.json'),
                                                                      'content': {'fixture_only': True}}},
            'inputs_sha256': {j[k]: j[k + '_sha256'] for j in jobs for k in ('job', 'vcf')},
            'outputs': {j['result_jsonl']: 'b' * 64 for j in jobs}})
        self.put('export-receipt.json', {'status': 'verified_compact_export',
                                       'design_record_binding': 'Hashes and JSON content verified against execution.design_records'})
        self.reseal()

    def test_zip_verifies_with_all_source_paths_absent(self):
        self.assertFalse(self.unavailable.exists())
        archive = self.base / 'fresh-fixture.zip'
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
            for path in self.package.rglob('*'):
                if path.is_file():
                    z.write(path, path.relative_to(self.package))
        shutil.rmtree(self.package)
        isolated = self.base / 'extracted'
        with zipfile.ZipFile(archive) as z:
            z.extractall(isolated)
        completed = subprocess.run([sys.executable, '-I', str(isolated / 'verify_reconstruction.py'),
                                    '--export', str(isolated)], cwd=isolated, capture_output=True, text=True, check=True)
        result = json.loads(completed.stdout)
        self.assertEqual(result['status'], 'verified_offline')
        self.assertEqual([(r['rank_min'], r['rank_max']) for r in result['all_case_results']], [(2, 3), (2, 3)])

    def test_changed_reported_rank_fails_even_with_updated_hashes(self):
        evaluation = self.get('evaluation.json')
        evaluation['all_case_results'][0]['rank_min'] = 1
        evaluation['all_case_results'][0]['rank_max'] = 1
        comparison = self.get('historical-vs-reconstructed.json')
        comparison[0]['new_reconstructed'] = evaluation['all_case_results'][0]
        self.put('evaluation.json', evaluation)
        self.put('historical-vs-reconstructed.json', comparison)
        self.reseal()
        with self.assertRaisesRegex(ValueError, 'FGFR2 evaluation rank/score'):
            verifier.verify(self.package)

    def test_changed_tsv_rank_fails_even_with_updated_hash(self):
        path = self.package / 'gene-scores/mini.tsv'
        path.write_text(path.read_text().replace('2\t3\tFGFR2', '1\t1\tFGFR2'))
        self.reseal()
        with self.assertRaisesRegex(ValueError, 'TSV rank/tie interval'):
            verifier.verify(self.package)

    def test_changed_job_still_fails_execution_binding_after_rehash(self):
        self.put('jobs/mini.yml', 'changed: true\n')
        self.reseal()
        with self.assertRaisesRegex(ValueError, 'Receipt binding mismatch: jobs/mini.yml'):
            verifier.verify(self.package)

    def test_design_content_checked_independently_of_updated_hash(self):
        self.put('protocol-before-inference.json', {'fixture_only': False})
        execution = self.get('execution.json')
        execution['design_records']['protocol-before-inference.json']['sha256'] = self.digest('protocol-before-inference.json')
        self.put('execution.json', execution)
        self.reseal()
        with self.assertRaisesRegex(ValueError, 'Design content mismatch'):
            verifier.verify(self.package)

    def test_unhashed_change_rejected(self):
        self.put('execution.log', 'changed\n')
        with self.assertRaisesRegex(ValueError, 'Member hash mismatch'):
            verifier.verify(self.package)

    def test_extra_member_rejected(self):
        self.put('unexpected.txt', 'extra\n')
        with self.assertRaisesRegex(ValueError, 'member set differs'):
            verifier.verify(self.package)

    def test_not_scored_is_rederived(self):
        path = self.package / 'gene-scores/mini.tsv'
        path.write_text('rank_min\trank_max\tgeneSymbol\tcombinedScore\tpriorityScore\tvariantScore\tpValue\n'
                        '1\t1\tHIGHER\t0.9\t0.8\t1.0\t0.01\n')
        absent = {'case_id': 'mini', 'gene': 'FGFR2', 'status': 'not_scored', 'rank_min': None,
                  'rank_max': None, 'scored_genes': 1, 'output_sha256': 'b' * 64}
        evaluation = self.get('evaluation.json'); evaluation['all_case_results'][0] = absent
        comparisons = self.get('historical-vs-reconstructed.json'); comparisons[0]['new_reconstructed'] = absent
        self.put('evaluation.json', evaluation); self.put('historical-vs-reconstructed.json', comparisons)
        self.reseal()
        self.assertEqual(verifier.verify(self.package)['all_case_results'][0]['status'], 'not_scored')


if __name__ == '__main__':
    unittest.main()
