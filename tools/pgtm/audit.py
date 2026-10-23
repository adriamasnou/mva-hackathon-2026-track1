#!/usr/bin/env python3
"""Offline, source-adjudicated PGT-M retrieval audit; no clinical accuracy claim.

Expected answers live in audit-tasks.json, not in the builder. Default mode checks
bundled source excerpts. Supply BOTH original-source arguments to verify whole-file
hashes, row locators and the completeness of selected-MIM mapping excerpts as well.
Python 3 + Node.js; no network and no third-party packages.
"""
import argparse
import csv
import datetime
import hashlib
import json
import pathlib
import subprocess
import xml.etree.ElementTree as ET
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
SUBMISSIONS = HERE.parents[1] / 'submissions'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def xlsx_cells(path):
    """Read cell coordinates directly, without importing the production parser."""
    ns = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
    with zipfile.ZipFile(path) as z:
        strings = [''.join(t.text or '' for t in si.iter(ns+'t'))
                   for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        result = {}
        for cell in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).iter(ns+'c'):
            value = cell.findtext(ns+'v', '')
            result[cell.attrib['r']] = strings[int(value)] if cell.get('t') == 's' else value
    return result


def record_mim(name, line):
    fields = line.split('\t')
    if name == 'gene_condition_source_id':
        return fields[7] if len(fields) > 7 else ''
    if name == 'genes_to_disease.txt':
        return fields[3][5:] if len(fields) > 3 and fields[3].startswith('OMIM:') else ''
    return fields[0]


def verify_originals(evidence, source_dir, hfea):
    paths = {name: (hfea if name.endswith('.xlsx') else source_dir/name)
             for name in evidence['sources']}
    for name, path in paths.items():
        if sha(path) != evidence['sources'][name]['sha256']:
            raise ValueError('Original source hash mismatch: '+name)
    cells = xlsx_cells(hfea)
    for row in evidence['hfea_rows'].values():
        for coordinate, value in row['cells'].items():
            if cells.get(coordinate) != value:
                raise ValueError('HFEA excerpt differs at '+coordinate)
    for name, excerpt in evidence['mapping_records'].items():
        lines = paths[name].read_text().splitlines()
        records = [{'line':i,'text':line} for i,line in enumerate(lines,1)
                   if record_mim(name,line) in evidence['selection_mims']]
        if records != excerpt['records']:
            raise ValueError('Missing or altered mapping excerpt: '+name)


def source_evidence(evidence, mims):
    """Interpret the retained raw records, separately from production functions."""
    result = {}
    for name, excerpt in evidence['mapping_records'].items():
        for item in excerpt['records']:
            fields = item['text'].split('\t')
            mim = record_mim(name,item['text'])
            if mim not in mims:
                continue
            if name == 'gene_condition_source_id':
                source = 'ClinVar'
                genes = (fields[1]+';'+fields[2]).replace('|',';').replace(',',';').split(';')
            elif name == 'genes_to_disease.txt':
                source, genes = 'HPO', [fields[1]]
            else:
                source, genes = 'OMIM-geneMIM', [fields[3]] if fields[1] == 'gene' else []
            for gene in genes:
                if gene.strip() and gene.strip() != '-':
                    result.setdefault(gene.strip(),set()).add((source,mim))
    return {gene:sorted(items) for gene,items in result.items()}


def canonical_evidence(ev):
    return {gene:sorted((x['source'],x['omim']) for x in items) for gene,items in ev.items()}


def run(taskfile=HERE/'audit-tasks.json', submissions=SUBMISSIONS, source_dir=None, hfea=None, node='node'):
    tasks = json.loads(taskfile.read_text())
    result = {'schema_version':1,'claim_scope':tasks['scope'],
              'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'tasks_passed':0,'tasks_total':len(tasks['tasks']),'tasks_executed':0,
              'source_verification':'whole files and excerpts' if source_dir and hfea else 'bundled excerpts only',
              'input_sha256':{'taskset':sha(taskfile)},'errors':[],'tasks':[]}
    try:
        if bool(source_dir) != bool(hfea):
            raise ValueError('Supply --source-dir and --hfea together')
        evidence_path = taskfile.parent/tasks['evidence_file']
        if sha(evidence_path) != tasks['evidence_sha256']:
            raise ValueError('Bundled evidence hash mismatch')
        evidence = json.loads(evidence_path.read_text())
        result['input_sha256']['evidence'] = sha(evidence_path)
        result['input_sha256']['audit.py'] = sha(HERE/'audit.py')
        result['input_sha256']['audit_query.cjs'] = sha(HERE/'audit_query.cjs')
        if source_dir and hfea:
            verify_originals(evidence,source_dir,hfea)
        for name in ['pgtm-navigator.html','hfea-pgtm-gene-crosswalk.csv','hfea-pgtm-gene-index.json','hfea-pgtm-provenance.json']:
            result['input_sha256'][name] = sha(submissions/name)
        with (submissions/'hfea-pgtm-gene-crosswalk.csv').open(newline='') as f:
            rows = list(csv.DictReader(f))
        index = json.loads((submissions/'hfea-pgtm-gene-index.json').read_text())['index']
        provenance = json.loads((submissions/'hfea-pgtm-provenance.json').read_text())
        if {s['name'] for s in provenance['sources']} != set(evidence['sources']):
            raise ValueError('Output provenance has missing or unexpected sources')
        for source in provenance['sources']:
            original = evidence['sources'][source['name']]
            if any(source[key] != original[key] for key in ['sha256','url','bytes']):
                raise ValueError('Output provenance differs from adjudicated source: '+source['name'])
        html = (submissions/'pgtm-navigator.html').read_text()
        embedded = json.loads(html.split('<script id="dataset" type="application/json">',1)[1].split('</script>',1)[0])
        normalized = [dict(r,n_genes=int(r['n_genes'])) for r in rows]
        if embedded['rows'] != normalized or embedded['provenance'] != provenance:
            raise ValueError('HTML payload and CSV/provenance disagree')
        # This executes the actual shipped JavaScript, not a Python imitation of search.
        completed = subprocess.run([node,str(HERE/'audit_query.cjs'),str(submissions/'pgtm-navigator.html')],
                                   input=json.dumps([t['query'] for t in tasks['tasks']]),
                                   text=True,capture_output=True,check=True,timeout=30)
        queries = json.loads(completed.stdout)
        if len(queries) != len(tasks['tasks']):
            raise ValueError('Query runner returned incomplete results')
    except (OSError,ValueError,KeyError,IndexError,subprocess.SubprocessError) as exc:
        result['errors'].append(str(exc)); result['status'] = 'ERROR'; return result
    for task, found in zip(tasks['tasks'],queries):
        errors = []
        expected = task.get('expected')
        record = {'id':task['id'],'query':task['query'],'kind':task['kind'],
                  'matched_rows':len(found['rows'])}
        if not expected:
            if len(found['rows']) != task['expected_count'] or task['status_contains'] not in found['status']:
                errors.append('No-match behavior differs')
        else:
            rownum = str(task['hfea_row'])
            cells = evidence['hfea_rows'].get(rownum,{}).get('cells',{})
            for col,key in [('A','condition'),('B','hfea_status'),('C','omim_as_published')]:
                if cells.get(col+rownum) != expected[key]: errors.append('Source cell differs: '+col+rownum)
            wanted_ev = canonical_evidence(expected['gene_evidence'])
            if source_evidence(evidence,expected['omim'].split(';')) != wanted_ev:
                errors.append('Expected genes/source evidence disagree with original records')
            matches = [r for r in found['rows'] if r['condition'] == expected['condition']]
            if len(matches) != 1:
                errors.append('Expected exactly one target condition row')
            else:
                row = matches[0]
                for key in ['hfea_status','omim_as_published','omim','clinvar_hpo','register_defect']:
                    if row[key] != expected[key]: errors.append('Wrong '+key)
                if row['genes'].split(';') != expected['genes'] and (row['genes'] or expected['genes']):
                    errors.append('Wrong candidate gene set')
                if row['n_genes'] != len(expected['genes']): errors.append('Wrong n_genes')
                if canonical_evidence(json.loads(row['gene_evidence'])) != wanted_ev:
                    errors.append('Wrong per-gene provenance')
                card = next((c for c in found['cards'] if expected['condition'] in c),[])
                if not card: errors.append('Target card not rendered')
                if expected['clinvar_hpo'] == 'differ' and 'Sources disagree — review required' not in card:
                    errors.append('Missing disagreement warning')
                if len(expected['genes']) > 1 and 'Multiple candidate genes' not in card:
                    errors.append('Missing multiple-gene warning')
                if expected['register_defect'] and 'Register flags: '+expected['register_defect'] not in card:
                    errors.append('Missing register-defect warning')
                for gene in expected['genes']:
                    if expected['condition'] not in index.get(gene,[]): errors.append('Target missing from gene index: '+gene)
            if task['kind'] == 'gene':
                record['literal_title_baseline_hit'] = task['query'].casefold() in expected['condition'].casefold()
        record.update(passed=not errors,errors=errors)
        result['tasks'].append(record)
    result['tasks_executed'] = len(result['tasks'])
    result['tasks_passed'] = sum(t['passed'] for t in result['tasks'])
    gene_tasks = [t for t in result['tasks'] if t['kind'] == 'gene']
    result['target_retrieval'] = {'navigator_passed':sum(t['passed'] for t in gene_tasks),
                                'literal_condition_title_hits':sum(t['literal_title_baseline_hit'] for t in gene_tasks),
                                'denominator':len(gene_tasks)}
    result['status'] = 'PASS' if result['tasks_passed'] == result['tasks_total'] and result['tasks_total'] else 'FAIL'
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--tasks',type=pathlib.Path,default=HERE/'audit-tasks.json')
    ap.add_argument('--submissions',type=pathlib.Path,default=SUBMISSIONS)
    ap.add_argument('--source-dir',type=pathlib.Path)
    ap.add_argument('--hfea',type=pathlib.Path)
    ap.add_argument('--node',default='node')
    ap.add_argument('--output',type=pathlib.Path)
    args = ap.parse_args()
    result = run(args.tasks,args.submissions,args.source_dir,args.hfea,args.node)
    rendered = json.dumps(result,indent=2)+'\n'
    if args.output: args.output.write_text(rendered)
    print(rendered,end='')
    raise SystemExit(0 if result['status'] == 'PASS' else 2 if result['status'] == 'ERROR' else 1)


if __name__ == '__main__':
    main()
