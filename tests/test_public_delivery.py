import csv,gzip,importlib.util,json,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
 s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
coverage=module('coverage','tools/pgtm/expert_coverage.py')
fixture=module('fixture','examples/public-case/prepare.py')
builder=module('pgtmbuilder','tools/pgtm/build.py')
package=module('packagecheck','tools/check_package.py')
class PublicDeliveryTests(unittest.TestCase):
 def test_coverage_provenance_detects_changed_source(self):
  self.assertEqual(package.provenance_errors(ROOT),[])
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'submissions').mkdir()
   for name in ['hfea-pgtm-gene-crosswalk.csv','expert-coverage.json']:
    (p/'submissions'/name).write_bytes((ROOT/'submissions'/name).read_bytes())
   crosswalk=p/'submissions/hfea-pgtm-gene-crosswalk.csv'
   crosswalk.write_bytes(crosswalk.read_bytes()+b'\n')
   self.assertEqual(package.provenance_errors(p),['Coverage provenance does not match the shipped crosswalk'])
 def test_coverage_denominator_excludes_unmapped(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);bulk=p/'bulk.gz';cross=p/'cross.csv'
   with gzip.open(bulk,'wt') as f:f.write('GeneSymbol\tReviewStatus\nBUB1B\treviewed by expert panel\nOTHER\tcriteria provided, single submitter\n')
   cross.write_text('n_genes,genes\n1,BUB1B\n1,OTHER\n0,\n')
   result=coverage.compute(bulk,cross)
   self.assertEqual(result['fraction_of_mapped'],.5);self.assertEqual(result['fraction_of_all'],1/3);self.assertEqual(result['unassessed_rows'],1)
 def test_coverage_empty_or_no_mapped_fails(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);bulk=p/'bulk.gz';cross=p/'cross.csv';cross.write_text('n_genes,genes\n0,\n')
   with gzip.open(bulk,'wt') as f:f.write('GeneSymbol\tReviewStatus\nBUB1B\treviewed by expert panel\n')
   with self.assertRaisesRegex(ValueError,'No mapped'):coverage.compute(bulk,cross)
   with gzip.open(bulk,'wt') as f:f.write('unexpected\nvalue\n')
   with self.assertRaisesRegex(ValueError,'schema'):coverage.compute(bulk,cross)
 def test_inline_xlsx_and_multimim_are_preserved(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'input.xlsx'
   xml='<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
   for n,vals in enumerate([['Condition name','Status','OMIM number'],['Example','approved','612555, 600185'],['Unmapped','approved','ARVC/D']],1):
    xml+='<row>'+''.join(f'<c r="{col}{n}" t="inlineStr"><is><t>{v}</t></is></c>' for col,v in zip('ABC',vals))+'</row>'
   xml+='</sheetData></worksheet>'
   with zipfile.ZipFile(p,'w') as z:z.writestr('xl/worksheets/sheet1.xml',xml)
   old=builder.XLSX;builder.XLSX=p
   try:rows=builder.read_hfea()
   finally:builder.XLSX=old
   self.assertEqual(rows[0]['mims'],['612555','600185']);self.assertEqual(rows[1]['mims'],[]);self.assertIn('text-not-a-number',rows[1]['flags'])
 def test_public_fixture_prepares_complete_sorted_vcf(self):
  with tempfile.TemporaryDirectory() as td:
   vcf,job=fixture.prepare(Path(td))
   rows=[x.split('\t') for x in vcf.read_text().splitlines() if not x.startswith('#')]
   self.assertEqual(len(rows),126);self.assertEqual(sum(r[0]=='10' for r in rows),6)
   coords=[(int(r[0]),int(r[1])) for r in rows];self.assertEqual(coords,sorted(coords))
   self.assertIn(str(vcf),job.read_text());self.assertNotIn('__VCF__',job.read_text())
   with self.assertRaises(FileExistsError):fixture.prepare(Path(td))
if __name__=='__main__':unittest.main()
