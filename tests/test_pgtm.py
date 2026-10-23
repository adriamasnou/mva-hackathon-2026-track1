import csv,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('builder',ROOT/'tools/pgtm/build.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

class PgtmTests(unittest.TestCase):
 def test_both_clinvar_fields_survive(self):
  with tempfile.TemporaryDirectory() as td:
   Path(td,'gene_condition_source_id').write_text('DiseaseMIM\tAssociatedGenes\tRelatedGenes\n257300\tBUB1B\tGENE2;GENE3\n257300\t-\tGENE4\n')
   old=b.SRC;b.SRC=Path(td)
   try:self.assertEqual(b.read_clinvar()['257300'],{'BUB1B','GENE2','GENE3','GENE4'})
   finally:b.SRC=old
 def test_null_gene_is_not_indexed(self):
  with tempfile.TemporaryDirectory() as td:
   Path(td,'genes_to_disease.txt').write_text('disease_id\tgene_symbol\tassociation_type\nOMIM:257300\t-\tMENDELIAN\nOMIM:257300\tBUB1B\tMENDELIAN\n')
   old=b.SRC;b.SRC=Path(td)
   try:self.assertEqual(b.read_hpo()['257300'],{'BUB1B'})
   finally:b.SRC=old
 def test_packaged_rows_and_per_gene_evidence(self):
  with (ROOT/'submissions/hfea-pgtm-gene-crosswalk.csv').open() as f:rows=list(csv.DictReader(f))
  manifest=json.loads((ROOT/'submissions/hfea-pgtm-provenance.json').read_text())
  self.assertEqual(len(rows),manifest['stats']['rows'])
  self.assertEqual(sum(not int(r['n_genes']) for r in rows),manifest['stats']['unmapped_rows'])
  for r in rows:
   genes=set(filter(None,r['genes'].split(';')));ev=json.loads(r['gene_evidence'])
   self.assertEqual(genes,set(ev));self.assertEqual(len(genes),int(r['n_genes']))
   for sources in ev.values():
    self.assertTrue(sources);self.assertTrue(all(x['omim'] in r['omim'].split(';') for x in sources))
  for gene,mim in [('BUB1B','257300'),('CEP57','614114'),('TRIP13','617598'),('CFTR','219700')]:
   self.assertTrue(any(gene in r['genes'].split(';') and mim in r['omim'].split(';') for r in rows),(gene,mim))
 def test_embedded_data_equal_csv(self):
  text=(ROOT/'submissions/pgtm-navigator.html').read_text();payload=text.split('<script id="dataset" type="application/json">')[1].split('</script>',1)[0]
  data=json.loads(payload);self.assertEqual(data['provenance']['stats']['rows'],len(data['rows']))
  self.assertNotIn('fetch(',text);self.assertNotIn('__DATA__',text)

if __name__=='__main__':unittest.main()
