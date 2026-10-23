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
phenotype=module('run_phenotype')
exporter=module('export_results')
export_verifier=module('verify_export')
phenotype_exporter=module('export_phenotype')
provenance=module('export_provenance')


class PublicBenchmarkTests(unittest.TestCase):
    def test_execution_binding_rejects_changed_configuration_and_design(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            properties=root/'runtime.properties';properties.write_text('whitelist=false\n')
            design=root/'protocol-before-inference.json';design.write_text('{"arm":"original"}\n')
            receipt={'properties_sha256':runner.sha(properties),'properties_text':properties.read_text(),
                     'design_records':{design.name:{'sha256':runner.sha(design),'content':json.loads(design.read_text())}}}
            provenance.verify(root,receipt)
            properties.write_text('whitelist=true\n')
            with self.assertRaises(ValueError):provenance.verify(root,receipt)
            properties.write_text(receipt['properties_text'])
            design.write_text('{"arm":"changed"}\n')
            with self.assertRaises(ValueError):provenance.verify(root,receipt)

    def test_phenotype_export_preserves_ties_after_original_outputs_are_removed(self):
        with tempfile.TemporaryDirectory() as d:
            work=Path(d)/'work';work.mkdir();(work/'results').mkdir()
            job=work/'case.yml';job.write_text('public phenotype fixture')
            jobs=[{'case_id':'x','gene':'TARGET','job':str(job),'job_sha256':runner.sha(job)}]
            protocol=work/'protocol-before-inference.json';protocol.write_text(json.dumps({'jobs':jobs}))
            source=work/'results/x.phenotype_only.genes.tsv'
            source.write_text('GENE_SYMBOL\tEXOMISER_GENE_PHENO_SCORE\nTARGET\t0.5000\nTARGET\t0.4000\nOTHER\t0.5000\n')
            record=work/'execution.json'
            record.write_text(json.dumps({'status':'completed','exit_code':0,'missing_outputs':[],
                'protocol_sha256':runner.sha(protocol),'outputs':{str(source):runner.sha(source)}}))
            row={'case_id':'x','output_sha256':runner.sha(source),**ev.rank_records(phenotype.phenotype_records(source),'TARGET')}
            (work/'evaluation.json').write_text(json.dumps({'execution_receipt_sha256':runner.sha(record),'all_case_results':[row]}))
            for name in ['batch.txt','runtime.properties']:(work/name).write_text('public fixture')
            out=Path(d)/'export';self.assertEqual(phenotype_exporter.export(work,out)['jobs_verified'],1)
            source.unlink();job.unlink()
            self.assertEqual(phenotype_exporter.verify(out)['jobs_verified'],1)
            compact=out/'gene-scores/x.tsv'
            compact.write_text(compact.read_text().replace('OTHER\t0.5','OTHER\t0.4999'))
            receipt=out/'export-receipt.json';r=json.loads(receipt.read_text())
            r['file_sha256']['gene-scores/x.tsv']=runner.sha(compact);receipt.write_text(json.dumps(r))
            with self.assertRaisesRegex(ValueError,'do not reproduce phenotype rank'):
                phenotype_exporter.verify(out)

    def test_portable_export_recomputes_ranks_without_original_files(self):
        with tempfile.TemporaryDirectory() as d:
            work=Path(d)/'work';work.mkdir()
            result=work/'result.jsonl'
            result.write_text('\n'.join(json.dumps({'geneSymbol':g,'combinedScore':score,'priorityScore':.5,'variantScore':.8}) for g,score in [('TARGET',.8),('OTHER',.8)])+'\n')
            job=work/'case.yml';job.write_text('retained public job fixture')
            jobs=[{'case_id':'x','gene':'TARGET','stratum':'autosomal','arm':'original','primary_autosomal':True,
                   'job':str(job),'job_sha256':runner.sha(job),'result_jsonl':str(result)}]
            manifest=work/'jobs-manifest.json';manifest.write_text(json.dumps(jobs))
            (work/'execution.json').write_text(json.dumps({'status':'completed','exit_code':0,'jobs_manifest_sha256':runner.sha(manifest),'outputs':{str(result):runner.sha(result)}}))
            cases=work/'cases.json';cases.write_text(json.dumps({'cases':[{'case_id':'x','gene':'TARGET','causal_variants':[]}]}))
            out=Path(d)/'export';exporter.export(work,out,cases)
            result.unlink();job.unlink()
            self.assertEqual(export_verifier.verify(out)['jobs_verified'],1)
            evaluation=out/'evaluation.json';data=json.loads(evaluation.read_text())
            data['all_case_results'][0]['rank_max']=1
            evaluation.write_text(json.dumps(data))
            receipt=out/'export-receipt.json';data=json.loads(receipt.read_text())
            data['file_sha256']['evaluation.json']=runner.sha(evaluation)
            receipt.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,'do not reproduce rank'):
                export_verifier.verify(out)

    def test_gene_recovery_does_not_imply_source_allele_contribution(self):
        case={'gene':'TARGET','causal_variants':[{'chrom':'1','pos':10,'ref':'A','alt':'G'}]}
        other={'contigName':'1','start':11,'ref':'C','alt':'T','filterStatus':'PASSED','contributesToGeneScore':True}
        record={'geneSymbol':'TARGET','combinedScore':.9,'variantEvaluations':[other]}
        audit=exporter.variant_audit([record],case)
        self.assertTrue(audit['source_gene_in_output'])
        self.assertEqual(audit['source_variants'][0]['exact_matches_in_source_gene'],0)
        record['variantEvaluations'].append({'contigName':'chr1','start':10,'ref':'A','alt':'G','filterStatus':'FAILED','contributesToGeneScore':False})
        matched=exporter.variant_audit([record],case)['source_variants'][0]
        self.assertEqual(matched['exact_matches_in_source_gene'],1)
        self.assertFalse(matched['matches'][0]['contributesToGeneScore'])

    def test_batch_cannot_skip_duplicate_or_substitute_a_frozen_job(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'batch.txt';jobs=[{'job':'/a/first.yml'},{'job':'/a/second.yml'}]
            valid='--analysis /a/first.yml\n--analysis /a/second.yml\n'
            p.write_text(valid);runner.check_batch(p,jobs)
            for invalid in [valid.splitlines()[0],valid+valid,valid.replace('second','other'),'analyse '+valid,
                            valid.replace('/a/first.yml','"/a/first.yml"')]:
                p.write_text(invalid)
                with self.assertRaises(ValueError):runner.check_batch(p,jobs)
            self.assertEqual(prep.batch_line('/a/first.yml'),valid.splitlines(True)[0])
            with self.assertRaises(ValueError):prep.batch_line('/space here/job.yml')

    def test_phenotype_comparator_collapses_modes_and_retains_rounded_ties(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'genes.tsv'
            p.write_text('GENE_SYMBOL\tEXOMISER_GENE_PHENO_SCORE\nA\t0.5000\nA\t0.4000\nB\t0.5000\n')
            ranked=ev.rank_records(phenotype.phenotype_records(p),'A')
            self.assertEqual((ranked['rank_min'],ranked['rank_max'],ranked['scored_genes']),(1,2,2))
            p.write_text('GENE_SYMBOL\tEXOMISER_GENE_PHENO_SCORE\nA\tnan\n')
            with self.assertRaises(ValueError):phenotype.phenotype_records(p)

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
