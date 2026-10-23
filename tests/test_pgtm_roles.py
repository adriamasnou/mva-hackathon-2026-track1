"""Original role preservation and visible UI payload checks; no clinical truth claim."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('role_builder', ROOT / 'tools/pgtm/build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class SourceRoleTests(unittest.TestCase):
    def test_same_gene_preserves_both_clinvar_fields_without_inventing_type(self):
        with tempfile.TemporaryDirectory() as td, patch.object(builder, 'SRC', Path(td)):
            Path(td, 'gene_condition_source_id').write_text(
                'DiseaseMIM\tAssociatedGenes\tRelatedGenes\n'
                '123456\tSYN1\tSYN1;SYN2\n123456\tSYN1\t-\n')
            result = builder.read_clinvar_evidence()['123456']
            self.assertEqual(result['SYN1'], [
                {'source': 'ClinVar', 'omim': '123456', 'source_field': 'AssociatedGenes', 'association_type': None},
                {'source': 'ClinVar', 'omim': '123456', 'source_field': 'RelatedGenes', 'association_type': None}])
            self.assertEqual(result['SYN2'][0]['source_field'], 'RelatedGenes')
            self.assertNotIn('-', result)

    def test_multiple_hpo_roles_for_one_gene_survive_and_are_not_normalized(self):
        with tempfile.TemporaryDirectory() as td, patch.object(builder, 'SRC', Path(td)):
            Path(td, 'genes_to_disease.txt').write_text(
                'disease_id\tgene_symbol\tassociation_type\n'
                'OMIM:123456\tSYN1\tPOLYGENIC\nOMIM:123456\tSYN1\tMENDELIAN\n'
                'OMIM:123456\tSYN1\tPOLYGENIC\nOMIM:123456\tSYN2\tFUTURE_SOURCE_TYPE\n'
                'OMIM:123456\tSYN3\t\n')
            result = builder.read_hpo_evidence()['123456']
            self.assertEqual([r['association_type'] for r in result['SYN1']], ['POLYGENIC', 'MENDELIAN'])
            self.assertEqual(result['SYN2'][0]['association_type'], 'FUTURE_SOURCE_TYPE')
            self.assertEqual(result['SYN3'][0]['association_type'], '')
            self.assertEqual(result['SYN1'][0]['source_field'], 'gene_symbol')

    def test_missing_or_renamed_hpo_role_header_fails_closed(self):
        with tempfile.TemporaryDirectory() as td, patch.object(builder, 'SRC', Path(td)):
            for header, row in [('disease_id\tgene_symbol', 'OMIM:257300\tBUB1B'),
                                ('disease_id\tgene_symbol\trenamed_type', 'OMIM:257300\tBUB1B\tMENDELIAN')]:
                Path(td, 'genes_to_disease.txt').write_text(header + '\n' + row + '\n')
                with self.assertRaisesRegex(ValueError, 'schema'):
                    builder.read_hpo_evidence()

    def test_omim_gene_entry_remains_distinct_from_phenotype_mapping(self):
        with tempfile.TemporaryDirectory() as td, patch.object(builder, 'SRC', Path(td)):
            Path(td, 'mim2gene.txt').write_text(
                '# comment\n123456\tgene\t1\tSYN1\n654321\tphenotype\t1\tSYN2\n')
            self.assertEqual(builder.read_mim2gene_evidence(), {'123456': {'SYN1': [
                {'source': 'OMIM-geneMIM', 'omim': '123456', 'source_field': 'Approved Gene Symbol (HGNC)',
                 'entry_type': 'gene', 'association_type': None}]}})


class VisibleRoleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        completed = subprocess.run(['node', str(ROOT / 'tools/pgtm/audit_query.cjs'),
                                    str(ROOT / 'submissions/pgtm-navigator.html')],
                                   input=json.dumps(['CFTR', 'QDPR', 'BRCA1', 'CHEK2']),
                                   text=True, capture_output=True, check=True, timeout=30)
        cls.results = {r['query']: r for r in json.loads(completed.stdout)}

    def test_cftr_query_shows_other_genes_roles_outside_details(self):
        result = self.results['CFTR']
        i = next(i for i, row in enumerate(result['rows']) if row['omim'] == '219700')
        groups = {g['gene']: g['labels'] for g in result['geneGroups'][i]}
        self.assertIn('HPO: Mendelian association · OMIM 219700', groups['CFTR'])
        self.assertIn('HPO: polygenic association · OMIM 219700', groups['FCGR2A'])
        self.assertIn('HPO: polygenic association · OMIM 219700', groups['TGFB1'])
        self.assertNotIn('HPO: Mendelian association · OMIM 219700', groups['FCGR2A'])
        self.assertTrue(any('"association_type"' in t for t in result['cards'][i]))
        self.assertFalse(any('"association_type"' in t for t in result['visibleCards'][i]))

    def test_relatedgenes_is_not_promoted_to_associatedgenes(self):
        result = self.results['QDPR']
        i = next(i for i, row in enumerate(result['rows']) if row['omim'] == '261600')
        groups = {g['gene']: g['labels'] for g in result['geneGroups'][i]}
        self.assertIn('ClinVar: related gene · OMIM 261600', groups['QDPR'])
        self.assertIn('ClinVar: associated gene · OMIM 261600', groups['PAH'])
        self.assertIn('Sources disagree — review required', result['visibleCards'][i])
        self.assertFalse(any(t.startswith('ClinVar: associated gene') for t in groups['QDPR']))

    def test_unexpected_source_category_is_preserved_without_clinical_reclassification(self):
        result = self.results['BRCA1']
        self.assertTrue(any('HPO: polygenic association · OMIM 604370' in group['labels']
                            for groups in result['geneGroups'] for group in groups if group['gene'] == 'BRCA1'))
        self.assertTrue(all('Source descriptions, not clinical classifications or gene-level approvals.' in card
                            for card in result['visibleCards']))

    def test_status_is_condition_level_and_gene_identifier_caveat_is_visible(self):
        for result in self.results.values():
            for row, card, groups in zip(result['rows'], result['visibleCards'], result['geneGroups']):
                self.assertIn('Condition status: ' + row['hfea_status'], card)
                self.assertNotIn(row['hfea_status'], card)
                self.assertFalse(any(row['hfea_status'] in label for group in groups for label in group['labels']))
        self.assertTrue(any(t.startswith('OMIM: gene identifier only · OMIM ')
                            for card in self.results['CHEK2']['visibleCards'] for t in card))

    def test_one_group_per_gene_and_no_implementation_labels_in_visible_text(self):
        for result in self.results.values():
            for row, card, groups in zip(result['rows'], result['visibleCards'], result['geneGroups']):
                self.assertEqual([g['gene'] for g in groups], sorted(json.loads(row['gene_evidence'])))
                self.assertFalse(any('field:' in text or 'association_type:' in text for text in card))
                self.assertTrue(all(' · OMIM ' in label for group in groups for label in group['labels']))

    def test_unknown_hpo_types_remain_literal_and_raw_evidence_unchanged(self):
        html = (ROOT / 'submissions/pgtm-navigator.html').read_text()
        marker = '<script id="dataset" type="application/json">'
        before, tail = html.split(marker, 1)
        payload, after = tail.split('</script>', 1)
        data = json.loads(payload)
        row = dict(self.results['CFTR']['rows'][0])
        evidence = {'SYNTHETIC': [
            {'source': 'HPO', 'source_field': 'gene_symbol', 'omim': '123456', 'association_type': 'FUTURE_SOURCE_TYPE'},
            {'source': 'HPO', 'source_field': 'gene_symbol', 'omim': '123456', 'association_type': ''}]}
        row.update(genes='SYNTHETIC', n_genes=1, gene_evidence=json.dumps(evidence))
        data['rows'] = [row]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'synthetic-role.html'
            path.write_text(before + marker + json.dumps(data) + '</script>' + after)
            completed = subprocess.run(['node', str(ROOT / 'tools/pgtm/audit_query.cjs'), str(path)],
                                       input='["SYNTHETIC"]', text=True, capture_output=True, check=True, timeout=30)
        result = json.loads(completed.stdout)[0]
        self.assertEqual(result['geneGroups'][0], [{'gene': 'SYNTHETIC', 'labels': [
            'HPO: association type “FUTURE_SOURCE_TYPE” (unrecognized label) · OMIM 123456',
            'HPO: association type not supplied · OMIM 123456']}])
        self.assertEqual(json.loads(result['rows'][0]['gene_evidence']), evidence)
        self.assertIn(json.dumps(evidence, indent=2, ensure_ascii=False), result['cards'][0])


if __name__ == '__main__':
    unittest.main()
