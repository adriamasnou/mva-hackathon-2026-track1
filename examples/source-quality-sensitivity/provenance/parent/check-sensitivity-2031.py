#!/usr/bin/env python3
"""Independent recomputation from frozen records; no analysis-module imports."""
from pathlib import Path
from collections import Counter
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
ANALYSIS = HERE.parent / 'sensitivity-2031'
ROOT = Path('/Volumes/easystore/MVA-deadline-build-20261024/sensitivity-2031/inputs')
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    receipt = read(ANALYSIS / 'immutable-input-hashes.json')
    for f in receipt['files']:
        p = ROOT / f['relative_path']
        assert sha(p) == f['sha256'] and p.stat().st_size == f['bytes'], p
    cases = read(ROOT / 'benchmark/cases.json')['cases']
    results = read(ROOT / 'benchmark/evaluations/corrected-v2.json')['all_case_arm_results']
    declared = read(ANALYSIS / 'all-strata.json')
    joined = [json.loads(x) for x in (ANALYSIS / 'joined-cases.jsonl').read_text().splitlines()]
    summaries = read(ROOT / 'source/summary.json')
    paper_reports = {x['pmid']: x for x in summaries['papers']}
    records = {p.stem: read(p) for p in (ROOT / 'source/records').glob('*.json')}
    contexts = [read(p) for p in (ROOT / 'source/contexts').glob('*/source-context.json')]
    lookup = {}
    for c in contexts:
        for p in c['packets']:
            key = (p['case_id'], p['member'])
            assert key not in lookup
            lookup[key] = (c['pmid'], p)
    assert len(cases) == len(joined) == len({x['case_id'] for x in cases}) == 713
    assert len(results) == len({(r['case_id'], r['arm']) for r in results}) == 1426
    ev = {(r['case_id'], r['arm']): r for r in results}
    expected = []
    for c, j in zip(cases, joined):
        cid = c['case_id']
        assert (cid, c['member'], c['packet_sha256']) == (j['case_id'], j['selected_member'], j['selected_packet_sha256'])
        links = [lookup[(cid, x['member'])] for x in c['all_matching_packets']]
        assert len(links) == len(j['linked_mappings'])
        pmids = set(pmid for pmid, _ in links)
        selected_pmid, selected_context = lookup[cid, c['member']]
        assert selected_context['selected_record'] and selected_context['sha256'] == c['packet_sha256']
        assert sum(p['selected_record'] for _, p in links) == 1
        reviews = []
        selected = None
        for pmid, p in links:
            rr = records.get(pmid)
            matched = [] if rr is None else [x for x in rr['packets'] if x['case_id'] == cid and x['member'] == p['member']]
            assert len(matched) == (1 if rr else 0)
            if matched:
                assert matched[0]['packet_sha256'] == p['sha256']
                reviews.append(matched[0])
                if p['selected_record']:
                    selected = matched[0]
        all_papers = all(paper_reports.get(p, {}).get('complete', False) for p in pmids)
        any_paper = any(p in paper_reports for p in pmids)
        n_adjudicated = sum(r['review_status'] == 'adjudicated' for r in reviews)
        all_packets = n_adjudicated == len(links)
        strata = {
            'all_linked_paper_completion': 'complete' if all_papers else 'incomplete' if any_paper else 'unreviewed',
            'all_linked_packet_completion': 'complete' if all_packets else 'incomplete' if n_adjudicated else 'unreviewed',
            'all_linked_paper_and_packet_completion': 'complete' if all_packets and all_papers else 'incomplete' if any_paper else 'unreviewed',
        }
        done = selected is not None and selected['review_status'] == 'adjudicated'
        strata.update({
            'selected_packet_category': selected['category'] if done else 'unreviewed',
            'selected_genotype_status': selected['genotype']['status'] if done else 'unreviewed',
            'selected_causal_confidence': selected['causal_confidence']['status'] if done else 'unreviewed',
            'selected_phenotype_contradiction': ('present' if any(p['assessment']['status'] == 'contradicted' for p in selected['phenotypes']) else 'none_recorded') if done else 'unreviewed',
        })
        assert strata == j['strata'], cid
        hits = {}
        for arm in ('original', 'none'):
            r = ev[cid, arm]
            # Do not use the author's recovered flags or rank_max to determine hits.
            score = {g['geneSymbol']: g['combinedScore'] for g in r.get('gene_scores', [])}
            worst = sum(v >= score[c['gene']] for v in score.values()) if c['gene'] in score else None
            obs = r.get('source_allele_audit', {}).get('source_variants', [])
            coord = lambda v: (str(v['chrom']).removeprefix('chr'), int(v['pos']), v['ref'], v['alt'])
            wanted = {coord(v) for v in c['causal_variants']}
            got = {coord(v['source_coordinate']) for v in obs}
            passes = wanted == got and len(obs) == len(wanted) and all(v['exact_matches_in_source_gene'] == 1 and len(v['matches']) == 1 and v['matches'][0]['filterStatus'] == 'PASSED' for v in obs)
            hits[arm] = {str(k): bool(r['status'] == 'scored' and passes and worst is not None and worst <= k) for k in (1, 5, 10)}
            assert hits[arm] == r['recovered'] == j['corrected_outcomes'][arm]['recovered'], (cid, arm)
            if c['blockers']:
                assert r['status'] == 'preparation_failed' and not any(hits[arm].values())
        x = any(v['chrom'] == 'X' for v in c['causal_variants'])
        fallback = len(c['signature']) == 1 and any(d['matching_tier'] != 'type_and_consequence' for d in c['decoys'])
        cohorts = {'all_713': True, 'primary_autosomal_681': not x, 'technical_X_32': x, 'fallback_18': fallback, 'without_fallback_695': not fallback, 'pairs_64': len(c['signature']) == 2}
        expected.append((cid, c['gene'], strata, hits, cohorts))
    checked = 0
    for cohort, report in declared.items():
        group = [r for r in expected if r[4][cohort]]
        for dimension, categories in report['source_audit_strata'].items():
            assert {r[2][dimension] for r in group}.issubset(categories)
            assert sum(s['case_denominator'] for s in categories.values()) == len(group)
            for category, s in categories.items():
                chosen = [r for r in group if r[2][dimension] == category]
                assert s['case_ids'] == [r[0] for r in chosen]
                assert s['case_denominator'] == len(chosen)
                assert s['gene_denominator'] == len({r[1] for r in chosen})
                for k in ('1', '5', '10'):
                    pairs = Counter((r[3]['original'][k], r[3]['none'][k]) for r in chosen)
                    mapped = {(True, True): 'both_recovered', (True, False): 'original_only', (False, True): 'none_only', (False, False): 'neither_recovered'}
                    for flags, label in mapped.items():
                        assert s['paired'][k][label] == pairs[flags]
                    assert s['paired'][k]['paired_case_denominator'] == len(chosen)
                    assert s['paired'][k]['discordant_pair_denominator'] == pairs[True, False] + pairs[False, True]
                    for arm in ('original', 'none'):
                        count = sum(r[3][arm][k] for r in chosen)
                        assert s['arms'][arm]['top_k_counts'][k] == count
                        assert s['arms'][arm]['top_k_rates'][k] == (count / len(chosen) if chosen else None)
                checked += 1
    assert {r[0] for r in expected if r[2]['all_linked_paper_and_packet_completion'] != 'complete'} == set(summaries['incomplete_case_ids'])
    result = {'passed': True, 'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'reviewer': 'parent', 'method': 'Independent Python implementation; no imports of analysis code; exact selected/member/hash and all alternate joins, source strata, primary outcomes from gene scores plus exact PASSED alleles, all marginal categories and paired counts.', 'source_manifest_sha256': sha(ROOT / 'source/manifest.json'), 'input_files_hashed': len(receipt['files']), 'cases': 713, 'arm_rows': 1426, 'stratum_categories': checked, 'code_sha256': sha(Path(__file__)), 'analysis_deliverables': {n: sha(ANALYSIS/n) for n in ['analyze.py','all-strata.json','joined-cases.jsonl','methods.json','README.md']}, 'limits': ['Not an independent re-read of every source annotation.', 'No inference rerun or clinical truth validation.', 'Post hoc and not blinded; no outcomes or source labels changed.']}
    (HERE / 'sensitivity-2031-independent-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
