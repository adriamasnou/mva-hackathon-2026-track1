import gzip
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

BASE=Path(__file__).resolve().parents[1]/'examples'/'public-benchmark'
def module(name):
    spec=importlib.util.spec_from_file_location('public_benchmark_'+name,BASE/(name+'.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
prep=module('prepare');ev=module('evaluate');runner=module('run')


class PublicBenchmarkTests(unittest.TestCase):
    def test_spike_collision_retains_other_loci_and_source_zygosity(self):
        rows=[['1','10','.','A','G','.','PASS','.','GT','0/1'],
              ['1','11','.','C','T','.','PASS','.','GT','1/1']]
        new,removed=prep.spike_rows(rows,[{'chrom':'1','pos':10,'ref':'A','alt':'T','genotype':'1/1'}])
        self.assertEqual(removed,[rows[0]])
        self.assertEqual(len(new),2)
        self.assertEqual(new[0][4:5],['T']);self.assertEqual(new[0][-1],'1/1')
        self.assertEqual(new[1],rows[1])

    def test_exon_union_uses_all_transcripts_without_gene_selection(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'gff.gz'
            with gzip.open(p,'wt') as f:
                f.write('1\tx\texon\t10\t30\t.\t+\t.\tgene=A\n1\tx\texon\t45\t50\t.\t+\t.\tgene=B\n2\tx\texon\t100\t110\t.\t+\t.\tgene=C\nX\tx\texon\t10\t30\t.\t+\t.\tgene=D\n')
            intervals,n=prep.merged_exons(p)
            self.assertEqual(n,3);self.assertEqual(intervals,[('1',0,70),('2',79,130)])

    def test_ties_use_conservative_rank_and_do_not_depend_on_order(self):
        rows=[{'geneSymbol':'TARGET','combinedScore':.8},{'geneSymbol':'B','combinedScore':.8},{'geneSymbol':'A','combinedScore':.9}]
        a=ev.rank_records(rows,'TARGET');b=ev.rank_records(rows[::-1],'TARGET')
        self.assertEqual(a,b);self.assertEqual((a['rank_min'],a['rank_max']),(2,3))

    def test_bad_scores_and_duplicate_genes_are_rejected(self):
        for value in [float('nan'),float('inf'),True,'0.8']:
            with self.subTest(value=value),self.assertRaises(ValueError):
                ev.rank_records([{'geneSymbol':'A','combinedScore':value}],'A')
        with self.assertRaises(ValueError):
            ev.rank_records([{'geneSymbol':'A','combinedScore':.1}]*2,'A')

    def test_missing_and_filtered_outputs_remain_in_denominator(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'result.jsonl';p.write_text(json.dumps({'geneSymbol':'OTHER','combinedScore':.8})+'\n')
            jobs=[{'case_id':str(i),'gene':'TARGET','stratum':'autosomal_single_heterozygous','arm':'original','primary_autosomal':True,'result_jsonl':str(p if i==0 else Path(d)/'absent')} for i in range(2)]
            result=ev.evaluate(jobs)['primary_autosomal']['original']
            self.assertEqual(result,{'denominator':2,'recovered':{'1':0,'5':0,'10':0},'not_scored':1,'failed_or_missing':1})

    def test_runtime_rejects_changed_input_before_execution(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'job.yml';p.write_text('original')
            v=Path(d)/'input.vcf';v.write_text('public fixture')
            job={'job':str(p),'job_sha256':runner.sha(p),'vcf':str(v),'vcf_sha256':runner.sha(v),'result_jsonl':str(Path(d)/'out.jsonl')}
            runner.check_inputs([job]);p.write_text('changed')
            with self.assertRaisesRegex(ValueError,'changed'):runner.check_inputs([job])

    def test_failed_execution_and_modified_results_cannot_count_as_recovery(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'result.jsonl';p.write_text(json.dumps({'geneSymbol':'TARGET','combinedScore':.8})+'\n')
            jobs=[{'case_id':'x','gene':'TARGET','stratum':'autosomal_single_heterozygous','arm':'original','primary_autosomal':True,'result_jsonl':str(p)}]
            receipt={'status':'failed','exit_code':1,'outputs':{str(p):runner.sha(p)}}
            result=ev.evaluate(jobs,receipt)
            self.assertEqual(result['all_case_results'][0]['status'],'execution_failed')
            self.assertEqual(result['primary_autosomal']['original']['recovered']['1'],0)
            receipt.update(status='completed',exit_code=0)
            self.assertEqual(ev.evaluate(jobs,receipt)['primary_autosomal']['original']['recovered']['1'],1)
            p.write_text(json.dumps({'geneSymbol':'TARGET','combinedScore':.9})+'\n')
            self.assertEqual(ev.evaluate(jobs,receipt)['all_case_results'][0]['status'],'invalid_output')

if __name__=='__main__':unittest.main()
