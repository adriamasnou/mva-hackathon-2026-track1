"""Adversarial checks against manually adjudicated public-source task answers."""
import csv
import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT/'tools/pgtm'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name,path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


audit = module('pgtm_audit',TOOLS/'audit.py')
builder = module('pgtm_audit_builder',TOOLS/'build.py')


class PgtmAuditTests(unittest.TestCase):
    def test_adjudicated_tasks_run_actual_javascript(self):
        result = audit.run()
        self.assertEqual(result['status'],'PASS',result)
        self.assertEqual((result['tasks_passed'],result['tasks_total']),(11,11))
        self.assertEqual(result['target_retrieval'],{
            'navigator_passed':7,'literal_condition_title_hits':3,'denominator':7})

    def test_consistent_output_corruption_still_fails_external_expectation(self):
        # CSV and HTML agree on the wrong data. An equality-only test would pass.
        with tempfile.TemporaryDirectory() as td:
            destination = Path(td)
            for name in ['hfea-pgtm-gene-crosswalk.csv','pgtm-navigator.html',
                         'hfea-pgtm-gene-index.json','hfea-pgtm-provenance.json']:
                shutil.copyfile(ROOT/'submissions'/name,destination/name)
            path = destination/'hfea-pgtm-gene-crosswalk.csv'
            with path.open(newline='') as f: rows = list(csv.DictReader(f))
            row = next(r for r in rows if r['condition'] == 'Mosaic Variegated Aneuploidy Syndrome 1 (MVA1)')
            row['genes'] = 'FABRICATED_GENE'
            row['gene_evidence'] = row['gene_evidence'].replace('BUB1B','FABRICATED_GENE')
            with path.open('w',newline='') as f:
                w = csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n'); w.writeheader(); w.writerows(rows)
            path = destination/'pgtm-navigator.html'
            text = path.read_text(); marker = '<script id="dataset" type="application/json">'
            start, tail = text.split(marker,1); payload, end = tail.split('</script>',1)
            data = json.loads(payload); data['rows'] = [dict(r,n_genes=int(r['n_genes'])) for r in rows]
            path.write_text(start+marker+json.dumps(data)+'</script>'+end)
            result = audit.run(submissions=destination)
            self.assertEqual(result['status'],'FAIL',result)
            failed = {t['id'] for t in result['tasks'] if not t['passed']}
            self.assertEqual(failed,{'T01','T11'})

    def test_missing_and_corrupted_bundled_evidence_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            task = folder/'audit-tasks.json'; shutil.copyfile(TOOLS/task.name,task)
            self.assertEqual(audit.run(taskfile=task)['status'],'ERROR')
            shutil.copyfile(TOOLS/'audit-evidence.json',folder/'audit-evidence.json')
            with (folder/'audit-evidence.json').open('a') as f:f.write(' ')
            result = audit.run(taskfile=task)
            self.assertEqual(result['status'],'ERROR')
            self.assertIn('Bundled evidence hash mismatch',result['errors'])
            self.assertEqual(result['tasks_executed'],0)

    def test_removed_record_fails_even_if_excerpt_hash_is_updated(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td); task = folder/'audit-tasks.json'; evidence_path = folder/'audit-evidence.json'
            manifest = json.loads((TOOLS/task.name).read_text())
            evidence = json.loads((TOOLS/evidence_path.name).read_text())
            records = evidence['mapping_records']['gene_condition_source_id']['records']
            evidence['mapping_records']['gene_condition_source_id']['records'] = [r for r in records if r['line'] != 12260]
            evidence_path.write_text(json.dumps(evidence))
            manifest['evidence_sha256'] = audit.sha(evidence_path); task.write_text(json.dumps(manifest))
            result = audit.run(taskfile=task)
            self.assertEqual(result['status'],'FAIL')
            self.assertFalse(next(t for t in result['tasks'] if t['id']=='T07')['passed'])

    def test_altered_original_hash_fails_before_parsing(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td); path = folder/'source.xlsx'; path.write_bytes(b'original')
            evidence = {'sources':{'source.xlsx':{'sha256':audit.sha(path)}}}
            path.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'Original source hash mismatch'):
                audit.verify_originals(evidence,folder,path)

    def test_missing_node_is_error_not_skipped_success(self):
        result = audit.run(node='/nonexistent/pgtm-audit-node')
        self.assertEqual(result['status'],'ERROR')
        self.assertEqual(result['tasks_executed'],0)

    def test_renamed_relatedgenes_header_rejected_despite_bub1b_control(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            (folder/'gene_condition_source_id').write_text(
                'DiseaseMIM\tAssociatedGenes\tRenamedRelatedGenes\n257300\tBUB1B\t\n256000\t\tBCS1L\n')
            previous = builder.SRC; builder.SRC = folder
            try:
                with self.assertRaisesRegex(ValueError,'schema'):builder.read_clinvar()
            finally:builder.SRC = previous

    def test_partial_rows_rejected_after_valid_control_row(self):
        examples = [
            ('gene_condition_source_id','DiseaseMIM\tAssociatedGenes\tRelatedGenes\n257300\tBUB1B\t\n256000\t\n',builder.read_clinvar),
            ('genes_to_disease.txt','disease_id\tgene_symbol\nOMIM:257300\tBUB1B\nOMIM:219700\n',builder.read_hpo)]
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td); previous = builder.SRC; builder.SRC = folder
            try:
                for filename,text,read in examples:
                    with self.subTest(filename=filename):
                        (folder/filename).write_text(text)
                        with self.assertRaisesRegex(ValueError,'partial'):read()
            finally:builder.SRC = previous


if __name__ == '__main__':
    unittest.main()
