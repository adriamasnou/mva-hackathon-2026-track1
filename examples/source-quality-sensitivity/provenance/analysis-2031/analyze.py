#!/usr/bin/env python3
"""PRIVATE post-hoc descriptive linkage. No inference or source re-adjudication."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT_ROOT = Path('/Volumes/easystore/MVA-deadline-build-20261024/sensitivity-2031/inputs')
SOURCE_MANIFEST = 'ddf90f9eaebab874d45805f2345e05246a9fdd61a0d348259770b3c1d10854a0'
CASE_SHA = '816f87efa1fc2bfcf8f0b6f3c9326cbb01f62c601f8ecaae4208d02086bd45fc'
EVAL_SHA = '54f7e82cbe62cc8f41913b7f3c8069cba4dd4ae26a3769bfec5f5def893ab9b5'
ARMS = ('original', 'none')
KS = ('1', '5', '10')
CATEGORIES = ('supported', 'qualified', 'contradicted', 'unresolved')
DIMENSIONS = {
    'all_linked_paper_completion': ('complete', 'incomplete', 'unreviewed'),
    'all_linked_packet_completion': ('complete', 'incomplete', 'unreviewed'),
    'all_linked_paper_and_packet_completion': ('complete', 'incomplete', 'unreviewed'),
    'selected_packet_category': CATEGORIES + ('unreviewed',),
    'selected_genotype_status': CATEGORIES + ('unreviewed',),
    'selected_causal_confidence': CATEGORIES + ('unreviewed',),
    'selected_phenotype_contradiction': ('present', 'none_recorded', 'unreviewed'),
}
COHORTS = {'all_713': 713, 'primary_autosomal_681': 681, 'technical_X_32': 32,
           'fallback_18': 18, 'without_fallback_695': 695, 'pairs_64': 64}
DIMENSION_FIELDS = ('patient_identity', 'genotype', 'segregation', 'phase',
                    'causal_confidence', 'phenotype_completeness')

def require(ok, message):
    if not ok:
        raise ValueError(message)

def unique_object(pairs):
    result = {}
    for k, v in pairs:
        require(k not in result, 'Duplicate JSON object key: ' + k)
        result[k] = v
    return result

def read(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=unique_object)

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()

def index_unique(rows, key, label):
    index = {}
    for r in rows:
        k = key(r)
        require(k not in index, f'Duplicate {label}: {k}')
        index[k] = r
    return index

def check_hash(path, expected):
    require(Path(path).is_file() and sha(path) == expected, 'Missing/hash mismatch: ' + str(path))

def verify_inputs(root, receipt):
    files = index_unique(receipt['files'], lambda x: x['relative_path'], 'input path')
    require({str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()} == set(files),
            'Frozen input file set changed')
    for name, record in files.items():
        p = root / name
        require(p.resolve().is_relative_to(root.resolve()) and not p.is_symlink(), 'Unsafe input path')
        check_hash(p, record['sha256'])
        require(p.stat().st_size == record['bytes'], 'Input size changed: ' + name)
    for name, digest in {'source/manifest.json': SOURCE_MANIFEST, 'benchmark/cases.json': CASE_SHA,
                         'benchmark/evaluations/corrected-v2.json': EVAL_SHA}.items():
        check_hash(root / name, digest)
    return files

def tags(case):
    return {'technical_X': any(v['chrom'] == 'X' for v in case['causal_variants']),
            'fallback': len(case['signature']) == 1 and
                        any(d['matching_tier'] != 'type_and_consequence' for d in case['decoys']),
            'pair': len(case['signature']) == 2}

def included(row, cohort):
    t = row['tags']
    return {'all_713': True, 'primary_autosomal_681': not t['technical_X'],
            'technical_X_32': t['technical_X'], 'fallback_18': t['fallback'],
            'without_fallback_695': not t['fallback'], 'pairs_64': t['pair']}[cohort]

def coordinate(v):
    return (str(v['chrom']).removeprefix('chr'), int(v['pos']), v['ref'], v['alt'])

def primary_hits(row):
    """Exactly the corrected primary endpoint; rank_min never decides success."""
    passed = row['all_source_alleles_passed']
    require(type(passed) is bool, 'Nonboolean source-allele pass state')
    rank = row['rank_max']
    if rank is not None:
        require(type(rank) is int and rank >= 1, 'Invalid worst-tied rank')
    success = row['status'] == 'scored' and passed and rank is not None
    return {k: bool(success and rank <= int(k)) for k in KS}

def validate_outcomes(cases, evaluation, corrected=True):
    case_index = index_unique(cases, lambda r: r['case_id'], 'case ID')
    rows = evaluation['all_case_arm_results']
    lookup = index_unique(rows, lambda r: (r['case_id'], r['arm']), 'case/arm outcome')
    expected = {(c, a) for c in case_index for a in ARMS}
    require(set(lookup) == expected, 'Missing/unexpected outcome arm or case')
    for (cid, arm), r in lookup.items():
        c = case_index[cid]
        require(r['gene'] == c['gene'], 'Outcome source gene mismatch')
        require(all(r[k] == v for k, v in tags(c).items()), 'Outcome cohort tags changed')
        if c['blockers']:
            require(r['status'] == 'preparation_failed' and r['reasons'] == c['blockers'],
                    'Preparation failure lost or altered')
        if corrected:
            # Full raw verification is separately required. This independently checks the
            # serialized exact-allele and score evidence used in this linkage.
            if r['status'] not in ('preparation_failed', 'invalid_output', 'missing_output'):
                observations = r['source_allele_audit']['source_variants']
                obs = index_unique(observations, lambda x: coordinate(x['source_coordinate']),
                                   'source allele observation')
                wanted = [coordinate(v) for v in c['causal_variants']]
                require(wanted and len(set(wanted)) == len(wanted), 'Empty/duplicate source alleles')
                require(set(obs) == set(wanted), 'Missing/extra exact source allele observation')
                all_passed = all(x['exact_matches_in_source_gene'] == 1 and len(x['matches']) == 1
                                 and x['matches'][0]['filterStatus'] == 'PASSED' for x in obs.values())
                require(all_passed == r['all_source_alleles_passed'], 'Exact PASSED evidence mismatch')
                genes = index_unique(r['gene_scores'], lambda x: x['geneSymbol'], 'passing gene symbol')
                require(len(genes) == r['filtered_gene_universe'], 'Passing gene universe mismatch')
                require(all(type(x['combinedScore']) in (int, float) and math.isfinite(x['combinedScore'])
                            for x in genes.values()), 'Invalid passing gene score')
                if c['gene'] in genes:
                    value = genes[c['gene']]['combinedScore']
                    low = 1 + sum(x['combinedScore'] > value for x in genes.values())
                    high = sum(x['combinedScore'] >= value for x in genes.values())
                    require((r['rank_min'], r['rank_max']) == (low, high), 'Exact tie/rank mismatch')
                else:
                    require(r['rank_min'] is None and r['rank_max'] is None, 'Absent gene has rank')
        hits = primary_hits(r)
        require(r['recovered'] == hits, 'Frozen primary endpoint mismatch')
        rr = 1 / r['rank_max'] if r['status'] == 'scored' and r['all_source_alleles_passed'] else 0
        require(math.isclose(r['reciprocal_rank'], rr, rel_tol=1e-12, abs_tol=1e-12),
                'Frozen primary reciprocal rank mismatch')
        if r['status'] in ('preparation_failed', 'invalid_output', 'missing_output', 'not_scored'):
            require(not any(hits.values()), 'Failed case counted as recovered')
    return lookup

def at_pointer(value, pointer):
    for piece in pointer.lstrip('/').split('/'):
        piece = piece.replace('~1', '/').replace('~0', '~')
        value = value[int(piece)] if isinstance(value, list) else value[piece]
    return value

def descriptor_pointers(packet):
    result = []
    for i, interpretation in enumerate(packet.get('interpretations', [])):
        for j, g in enumerate(interpretation.get('diagnosis', {}).get('genomicInterpretations', [])):
            if 'variationDescriptor' in g.get('variantInterpretation', {}):
                result.append(f'/interpretations/{i}/diagnosis/genomicInterpretations/{j}/variantInterpretation/variationDescriptor')
    return result

def validate_packet_binding(review, source, pmid):
    require(review['case_id'] == source['case_id'] and review['member'] == source['member']
            and review['packet_sha256'] == source['sha256'], 'Review packet/member/hash mismatch: ' + pmid)
    require(review['role'] == ('selected' if source['selected_record'] else 'alternate'), 'Review role mismatch')
    require(review['review_status'] in ('pending', 'adjudicated'), 'Unknown review state')
    require(review['category'] in CATEGORIES, 'Unknown raw packet category')
    for field in DIMENSION_FIELDS:
        require(review[field]['status'] in CATEGORIES, 'Unknown raw assessment status')
    for field, expected in [('phenotypes', [f'/phenotypicFeatures/{i}' for i in range(len(source['phenotypicFeatures']))]),
                            ('alleles', descriptor_pointers(source))]:
        entries = index_unique(review[field], lambda x: x['pointer'], 'packet item pointer')
        require(set(entries) == set(expected), 'Missing/extra source item pointer')
        for pointer, x in entries.items():
            original = at_pointer(source, pointer)
            require(x['snapshot'] == original and x['snapshot_sha256'] == canonical_sha(original),
                    'Source item snapshot hash/content mismatch')
            require(x['assessment']['status'] in CATEGORIES, 'Unknown item assessment status')

def source_indexes(source_root, cases, summary):
    inventory = read(source_root / 'inventory.json')
    require(inventory['case_manifest_sha256'] == CASE_SHA, 'Source inventory case binding mismatch')
    papers = index_unique(inventory['papers'], lambda x: x['pmid'], 'inventory PMID')
    reports = index_unique(summary['papers'], lambda x: x['pmid'], 'report PMID')
    contexts, reviews = {}, {}
    by_case = defaultdict(list)
    for pmid in papers:
        c = read(source_root / 'contexts' / pmid / 'source-context.json')
        require(c['pmid'] == pmid, 'Context PMID mismatch')
        mapping = index_unique(c['packets'], lambda x: (x['case_id'], x['member']), 'context mapping')
        for (cid, member), p in mapping.items():
            key = (cid, pmid, member)
            contexts[key] = p
            by_case[cid].append(key)
        if pmid in reports:
            record = read(source_root / 'records' / (pmid + '.json'))
            require(record['pmid'] == pmid and reports[pmid]['valid'] is True, 'Invalid record identity')
            index = index_unique(record['packets'], lambda x: (x['case_id'], x['member']), 'review mapping')
            require(set(index) == set(mapping), 'Missing/extra record packet mapping')
            for (cid, member), p in index.items():
                validate_packet_binding(p, mapping[cid, member], pmid)
                reviews[cid, pmid, member] = (p, record['audit']['outcome_exposure'])
    require(set(by_case) == {c['case_id'] for c in cases}, 'Source/case cohort mismatch')
    for c in cases:
        linked = by_case[c['case_id']]
        expected = index_unique(c['all_matching_packets'], lambda x: x['member'], 'case linked member')
        require(len(linked) == len(expected) and {k[2] for k in linked} == set(expected),
                'Missing/duplicate/extra linked packet')
        selected = [k for k in linked if contexts[k]['selected_record']]
        require(len(selected) == 1, 'Selected mapping not unique')
        s = contexts[selected[0]]
        require(s['member'] == c['member'] and s['sha256'] == c['packet_sha256'],
                'Selected packet member/hash differs from frozen case')
    return by_case, contexts, reviews, reports

def completion(total, complete, reviewed):
    require(total > 0 and 0 <= complete <= reviewed <= total, 'Invalid completion counts')
    return 'complete' if complete == total else 'unreviewed' if reviewed == 0 else 'incomplete'

def selection_annotation(packet):
    """Preserve raw labels; pending templates are separately reported as unreviewed."""
    done = packet is not None and packet['review_status'] == 'adjudicated'
    if not done:
        return {'selected_packet_category': 'unreviewed', 'selected_genotype_status': 'unreviewed',
                'selected_causal_confidence': 'unreviewed', 'selected_phenotype_contradiction': 'unreviewed'}
    return {'selected_packet_category': packet['category'],
            'selected_genotype_status': packet['genotype']['status'],
            'selected_causal_confidence': packet['causal_confidence']['status'],
            'selected_phenotype_contradiction': 'present' if any(x['assessment']['status'] == 'contradicted'
                                                               for x in packet['phenotypes']) else 'none_recorded'}

def compact_outcome(row, position):
    # Full unchanged rows remain in the frozen original and corrected JSONs.
    names = ('case_id', 'gene', 'arm', 'status', 'rank_min', 'rank_max', 'all_source_alleles_passed',
             'recovered', 'reciprocal_rank', 'reasons', 'error', 'output_sha256',
             'filtered_gene_universe', 'emitted_gene_universe', 'gene_only_recovered',
             'gene_only_reciprocal_rank', 'joint_best_recovered', 'joint_best_reciprocal_rank')
    return {**{k: row[k] for k in names if k in row}, 'evaluation_row_index': position,
            'full_evaluation_row_canonical_sha256': canonical_sha(row)}

def join_rows(cases, corrected, original, source_root, summary):
    index_unique(cases, lambda x: x['case_id'], 'case ID')
    ci = validate_outcomes(cases, corrected)
    oi = validate_outcomes(cases, original, corrected=False)
    positions = [{(r['case_id'], r['arm']): i for i, r in enumerate(e['all_case_arm_results'])}
                 for e in (corrected, original)]
    by_case, contexts, reviews, reports = source_indexes(source_root, cases, summary)
    rows = []
    for case_index, c in enumerate(cases):
        cid = c['case_id']; keys = by_case[cid]; pmids = sorted({k[1] for k in keys}, key=int)
        linked = []
        for key in keys:
            p, exposure = reviews.get(key, (None, None)); report = reports.get(key[1])
            linked.append({'pmid': key[1], 'member': key[2], 'packet_sha256': contexts[key]['sha256'],
                           'role': 'selected' if contexts[key]['selected_record'] else 'alternate',
                           'record_present': p is not None, 'paper_complete': bool(report and report['complete']),
                           'main_text_full': bool(report and report['main_text_full']),
                           'review_status': p['review_status'] if p else None,
                           'raw_packet_category': p['category'] if p else None,
                           'source_reviewer_outcome_exposure': exposure,
                           'context_path': f'contexts/{key[1]}/source-context.json',
                           'record_path': f'records/{key[1]}.json' if p else None})
        selected_key = next(k for k in keys if contexts[k]['selected_record'])
        selected, exposure = reviews.get(selected_key, (None, None))
        papers_present = sum(pmid in reports for pmid in pmids)
        papers_complete = sum(bool(reports.get(pmid, {}).get('complete')) for pmid in pmids)
        packets_adjudicated = sum(x['review_status'] == 'adjudicated' for x in linked)
        pc = completion(len(pmids), papers_complete, papers_present)
        # Packet completion requires actual adjudication; merely present templates do not count.
        kc = completion(len(keys), packets_adjudicated, packets_adjudicated)
        combined = 'complete' if pc == kc == 'complete' else 'unreviewed' if papers_present == 0 else 'incomplete'
        strata = {**selection_annotation(selected), 'all_linked_paper_completion': pc,
                  'all_linked_packet_completion': kc, 'all_linked_paper_and_packet_completion': combined}
        raw = None
        if selected:
            status = {f: selected[f]['status'] for f in DIMENSION_FIELDS}
            ph = [dict(pointer=x['pointer'], snapshot_sha256=x['snapshot_sha256'],
                       status=x['assessment']['status']) for x in selected['phenotypes']]
            alleles = [dict(pointer=x['pointer'], snapshot_sha256=x['snapshot_sha256'],
                            status=x['assessment']['status']) for x in selected['alleles']]
            nonphen_contradiction = any(status[f] == 'contradicted' for f in DIMENSION_FIELDS if f != 'phenotype_completeness') or any(x['status'] == 'contradicted' for x in alleles)
            phenotype_contradiction = any(x['status'] == 'contradicted' for x in ph)
            raw = {'review_status': selected['review_status'], 'category': selected['category'],
                   'assessment_statuses': status, 'phenotype_items': ph, 'allele_items': alleles,
                   'phenotype_status_counts': dict(Counter(x['status'] for x in ph)),
                   'allele_status_counts': dict(Counter(x['status'] for x in alleles)),
                   'recorded_nonphenotype_contradiction': nonphen_contradiction,
                   'phenotype_only_recorded_contradiction':
                       (phenotype_contradiction or status['phenotype_completeness'] == 'contradicted') and not nonphen_contradiction,
                   'source_reviewer_outcome_exposure': exposure}
        rows.append({'case_id': cid, 'case_index': case_index, 'gene': c['gene'],
                     'selected_member': c['member'], 'selected_packet_sha256': c['packet_sha256'],
                     'selected_pmid': selected_key[1], 'tags': tags(c), 'signature': c['signature'],
                     'preparation_status': c['preparation_status'], 'preparation_blockers': c['blockers'],
                     'original_labels_unchanged': True, 'analysis_outcome_exposure': 'per_case',
                     'selected_review_availability': 'no_record' if selected is None else selected['review_status'],
                     'source_counts': {'linked_papers': len(pmids), 'paper_records_present': papers_present,
                                       'complete_papers': papers_complete, 'linked_packets': len(keys),
                                       'adjudicated_packets': packets_adjudicated},
                     'strata': strata, 'linked_mappings': linked, 'selected_raw_review': raw,
                     'corrected_outcomes': {a: compact_outcome(ci[cid, a], positions[0][cid, a]) for a in ARMS},
                     'original_literal_outcomes': {a: compact_outcome(oi[cid, a], positions[1][cid, a]) for a in ARMS}})
    require(sum(r['strata']['all_linked_paper_and_packet_completion'] == 'complete' for r in rows)
            == summary['cases_complete'], 'Complete-case denominator differs from frozen snapshot')
    require({r['case_id'] for r in rows if r['strata']['all_linked_paper_and_packet_completion'] != 'complete'}
            == set(summary['incomplete_case_ids']), 'Complete-case membership differs from snapshot')
    return rows

def summarize(rows):
    n = len(rows)
    result = {'case_denominator': n, 'gene_denominator': len({r['gene'] for r in rows}),
              'case_ids': [r['case_id'] for r in rows], 'arms': {}, 'paired': {}}
    for arm in ARMS:
        rs = [r['corrected_outcomes'][arm] for r in rows]
        counts = {k: sum(r['recovered'][k] for r in rs) for k in KS}
        result['arms'][arm] = {'case_denominator': n, 'top_k_counts': counts,
                               'top_k_rates': {k: counts[k] / n if n else None for k in KS},
                               'status_counts': dict(Counter(r['status'] for r in rs)),
                               'tie_cases': sum(r['rank_min'] is not None and r['rank_min'] != r['rank_max'] for r in rs),
                               'all_source_alleles_passed_cases': sum(r['all_source_alleles_passed'] for r in rs)}
    for k in KS:
        counts = dict.fromkeys(('both_recovered', 'original_only', 'none_only', 'neither_recovered'), 0)
        for r in rows:
            a, b = (r['corrected_outcomes'][arm]['recovered'][k] for arm in ARMS)
            label = 'both_recovered' if a and b else 'original_only' if a else 'none_only' if b else 'neither_recovered'
            counts[label] += 1
        require(sum(counts.values()) == n, 'Paired partition lost cases')
        require(counts['both_recovered'] + counts['original_only'] == result['arms']['original']['top_k_counts'][k]
                and counts['both_recovered'] + counts['none_only'] == result['arms']['none']['top_k_counts'][k],
                'Paired and marginal counts disagree')
        result['paired'][k] = {**counts, 'paired_case_denominator': n,
                               'discordant_pair_denominator': counts['original_only'] + counts['none_only'],
                               'net_recovered_count_original_minus_none': counts['original_only'] - counts['none_only']}
    return result

def all_strata(rows, corrected):
    result = {}
    for cohort, expected_n in COHORTS.items():
        group = [r for r in rows if included(r, cohort)]
        require(len(group) == expected_n, 'Frozen cohort denominator changed: ' + cohort)
        baseline = summarize(group)
        for arm in ARMS:
            frozen = corrected['all_strata'][cohort][arm]
            require(baseline['arms'][arm]['top_k_counts'] == frozen['primary_full_source_allele_recovery']['top_k_counts']
                    and baseline['arms'][arm]['status_counts'] == frozen['status_counts']
                    and baseline['gene_denominator'] == frozen['gene_denominator'], 'Original full-cohort result changed')
        strata = {}
        for dim, categories in DIMENSIONS.items():
            strata[dim] = {c: summarize([r for r in group if r['strata'][dim] == c]) for c in categories}
            require(sum(x['case_denominator'] for x in strata[dim].values()) == len(group),
                    'Stratum partition lost or duplicated a case')
            for arm in ARMS:
                for k in KS:
                    require(sum(x['arms'][arm]['top_k_counts'][k] for x in strata[dim].values())
                            == baseline['arms'][arm]['top_k_counts'][k], 'Stratum totals differ')
        result[cohort] = {'baseline': baseline, 'source_audit_strata': strata}
    return result

def atomic(path, value, jsonl=False):
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('w') as f:
        if jsonl:
            for r in value:
                f.write(json.dumps(r, ensure_ascii=False, separators=(',', ':'), allow_nan=False) + '\n')
        else:
            json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False); f.write('\n')
        f.flush(); os.fsync(f.fileno())
    os.replace(temp, path)
    fd = os.open(path.parent, os.O_RDONLY); os.fsync(fd); os.close(fd)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', type=Path, default=INPUT_ROOT)
    args = parser.parse_args(); root = args.input_root
    receipt = read(HERE / 'immutable-input-hashes.json')
    files = verify_inputs(root, receipt)
    spec = importlib.util.spec_from_file_location('frozen_source_verify', root / 'source/verify.py')
    verifier = importlib.util.module_from_spec(spec); spec.loader.exec_module(verifier)
    source_errors = verifier.check(root / 'source')
    require(not source_errors, 'Source verifier failed: ' + str(source_errors))
    benchmark_receipt_path = root.parent / 'benchmark-verification.json'
    br = read(benchmark_receipt_path)
    require(br['status'] == 'verified' and br['cases'] == 713 and br['case_arm_rows'] == 1426,
            'Existing benchmark verification did not pass')
    require(br['export_receipt_sha256'] == sha(root / 'benchmark/export-receipt.json'),
            'Benchmark verification receipt is for another bundle')
    cases = read(root / 'benchmark/cases.json')['cases']
    corrected = read(root / 'benchmark/evaluations/corrected-v2.json')
    original = read(root / 'benchmark/evaluations/original.json')
    summary = read(root / 'source/summary.json')
    expected_counts = {'papers_main_text_full': 262, 'papers_complete': 147,
                       'packets_adjudicated': 1169, 'cases_complete': 322}
    require(all(summary[k] == v for k, v in expected_counts.items()), 'Wrong source snapshot counts')
    rows = join_rows(cases, corrected, original, root / 'source', summary)
    require(len(rows) == 713, 'Full cohort not retained')
    strata = all_strata(rows, corrected)
    methods = {'private': True, 'post_hoc': True, 'preregistered': False, 'outcome_exposure': 'per_case',
               'scope': 'Descriptive outcome-linked source-correspondence sensitivity; no clinical accuracy or causal effect.',
               'inputs': {'source_manifest_sha256': SOURCE_MANIFEST, 'cases_sha256': CASE_SHA, 'corrected_evaluation_sha256': EVAL_SHA},
               'endpoint': corrected['primary_rule'], 'failure_rule': corrected['failure_rule'],
               'dimensions': DIMENSIONS, 'cohorts': COHORTS,
               'definitions': {
                   'all_linked_paper_completion': 'complete if every linked paper is complete in frozen summary; unreviewed if no linked paper has a record; otherwise incomplete.',
                   'all_linked_packet_completion': 'complete if every selected/alternate packet is adjudicated; unreviewed if none is adjudicated; otherwise incomplete.',
                   'all_linked_paper_and_packet_completion': 'complete only if both preceding criteria complete; unreviewed if no linked paper record; otherwise incomplete. Must reproduce frozen322completecase membership.',
                   'selected_categories': 'Use raw category/genotype/causal status only for adjudicated selected packets. No record or pending selected packet maps to explicitly unreviewed; raw pending labels remain in joined rows.',
                   'selected_phenotype_contradiction': 'present means at least one selected packet phenotypicFeatures assessment is contradicted; none_recorded means zero such recorded items in an adjudicated packet, not absence of true discrepancy. Phenotype-completeness status retained separately.',
                   'zero_size': 'Every declared category is emitted for every cohort, even n=0; rates null, never zero or NaN for empty denominators.',
                   'paired': 'Both arms for every member of each stratum, including failures. Both recovered/original only/none only/neither sum to paired n. Discordant n separately reported.',
                   'partition': 'Separate marginal strata for each named dimension, not a favorable intersection chosen from outcome results.',
                   'original_arm': 'original denotes original-HPO arm; none denotes no-HPO arm. Original literal pre-correction evaluation is separately retained without replacing corrected results.'},
               'limitations': ['Source audit and this linkage are post inference and not blinded; analysis has explicit per_case exposure.',
                               'Review availability/completion is nonrandom and depends on access and reader coverage; subgroup contrasts do not estimate effects of review or phenotypes.',
                               'Contradicted packet can be phenotype-only or formal classification mismatch; it is not a disproved diagnosis. No frozen label is substituted.',
                               'Full component reading does not mean every source assertion is supported or causal confidence established.',
                               'Source-derived phenotype inputs and source labels may share knowledge with current databases; this is not an independent temporal holdout.',
                               'Ten constructed input hypotheses can map to smaller/different passing universes; top10 may be trivial.',
                               'Cases cluster by gene/publication and include alternate packets; no independence assumption, inference p-values or clinical accuracy claims.',
                               'No new source reading credits, source adjudication changes, inference reruns, provider contact or repository edits.']}
    atomic(HERE / 'methods.json', methods)
    atomic(HERE / 'joined-cases.jsonl', rows, jsonl=True)
    atomic(HERE / 'all-strata.json', strata)
    atomic(HERE / 'frozen-baseline-strata.json', {'corrected_v2': corrected['all_strata'], 'original_literal': original['all_strata']})
    # Recheck every frozen byte after joining and writing outputs.
    verify_inputs(root, receipt)
    validation = {'valid': True, 'at_utc': datetime.now(timezone.utc).isoformat(),
                  'analysis_code_sha256': sha(Path(__file__)), 'immutable_input_receipt_sha256': sha(HERE / 'immutable-input-hashes.json'),
                  'frozen_input_files': len(files), 'source_snapshot_verifier_errors': source_errors,
                  'benchmark_verifier': {'path': str(benchmark_receipt_path), 'sha256': sha(benchmark_receipt_path),
                                         **{k: br[k] for k in ('status', 'files', 'raw_outputs', 'cases', 'case_arm_rows', 'preparation_failures_per_arm')}},
                  'case_rows': len(rows), 'paired_case_arm_rows': len(rows) * 2,
                  'unique_selected_member_hash_joins': len(rows), 'all_linked_mappings': sum(len(r['linked_mappings']) for r in rows),
                  'source_snapshot_counts': expected_counts, 'selected_review_availability': dict(Counter(r['selected_review_availability'] for r in rows)),
                  'cohort_baselines_match_frozen_evaluation': True, 'all_dimension_partitions_reconcile': True,
                  'original_literal_results_retained': True, 'input_hashes_rechecked_after_analysis': True,
                  'outputs': {name: {'sha256': sha(HERE / name), 'bytes': (HERE / name).stat().st_size}
                              for name in ('methods.json', 'joined-cases.jsonl', 'all-strata.json', 'frozen-baseline-strata.json')}}
    atomic(HERE / 'validation.json', validation)
    print(json.dumps({k: v for k, v in validation.items() if k not in ('outputs', 'benchmark_verifier')}, indent=2))

if __name__ == '__main__':
    main()
