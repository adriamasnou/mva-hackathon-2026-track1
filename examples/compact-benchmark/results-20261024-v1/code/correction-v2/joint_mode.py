"""Versioned post-freeze correction: omitted primitive mode score is zero.

No CLI, inference, aggregation, imports of active audit code, or file writes.
Uses the audit_public_execution.py mode_contributions logic with exact matching
only: no equivalent-haplotype rescue and no union across inheritance modes.
"""
import math


def source_key(variant):
    return (str(variant['chrom']).removeprefix('chr'), int(variant['pos']),
            variant['ref'], variant['alt'])


def output_key(variant):
    return (str(variant['contigName']).removeprefix('chr'), int(variant['start']),
            variant['ref'], variant['alt'])


def exact_alleles(records, case):
    """Return exact retention, global flags, and joint best-mode contribution.

Call only on validated, hash-verified output. Missing raw flags/mode evidence
    remain None; an absent target gene is observed nonrecovery. Missing output
    is NOT an empty records list: caller retains unknown evidence and zero
    endpoint success for that case. PASSED/filter status remains explicit.
    """
    sources = [source_key(v) for v in case['causal_variants']]
    if not sources or len(sources) != len(set(sources)):
        raise ValueError('Empty or duplicated source alleles')
    targets = [r for r in records if r['geneSymbol'] == case['gene']]
    if len(targets) > 1:
        raise ValueError('Duplicate source gene')
    target = targets[0] if targets else None
    detail = []
    for source, key in zip(case['causal_variants'], sources):
        matches = [v for v in target.get('variantEvaluations', []) if output_key(v) == key] if target else []
        flags = [v.get('contributesToGeneScore') for v in matches]
        if any(flag is not None and not isinstance(flag, bool) for flag in flags):
            raise ValueError('Invalid contributesToGeneScore flag')
        available = target is None or 'variantEvaluations' in target
        detail.append({'source': list(key), 'input_genotype': source.get('genotype'),
                       'matches': [{'filter_status': v.get('filterStatus'),
                                    'contributes_to_gene_score': v.get('contributesToGeneScore')}
                                   for v in matches],
                       'target_gene_matched': bool(matches) if available else None,
                       'target_gene_contributing': (True if True in flags else
                           None if None in flags or not available else False)})
    modes = []
    if target is not None:
        score = target['combinedScore']
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score):
            raise ValueError('Invalid gene score')
        for mode in target.get('geneScores', []):
            # Installed Exomiser 15.1.0 writes primitive doubles with NON_DEFAULT.
            # Absence is suppressed zero; explicit null remains invalid.
            value = mode.get('combinedScore', 0.0)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError('Invalid inheritance-mode score')
            if value > score:
                raise ValueError('Mode score exceeds reported best gene score')
            keys = {output_key(v) for v in mode.get('contributingVariants', [])}
            matched = [list(k) for k in sources if k in keys]
            modes.append({'inheritance_mode': mode['modeOfInheritance'], 'combined_score': value,
                          'is_best_score': value == score, 'contributing_source_alleles': matched,
                          'all_source_alleles_contribute': (len(matched) == len(sources)
                              if 'contributingVariants' in mode else None)})
    best = [m for m in modes if m['is_best_score']]
    values = [m['all_source_alleles_contribute'] for m in best]
    any_best = True if True in values else (None if not values or None in values else False)
    every_best = False if False in values else (None if not values or None in values else True)
    if target is None:
        any_best = every_best = False
    retained = [a['target_gene_matched'] for a in detail]
    flags = [a['target_gene_contributing'] for a in detail]
    return {'source_alleles': detail, 'reported_score_modes': modes,
            'mode_evidence_status': ('source_gene_absent' if target is None else
                'complete' if best and None not in values else 'incomplete'),
            'all_source_alleles_matched': False if False in retained else None if None in retained else True,
            'all_source_alleles_contributing': False if False in flags else None if None in flags else True,
            'all_source_alleles_in_any_best_mode': any_best,
            'all_source_alleles_in_every_best_mode': every_best}
