#!/usr/bin/env python3
"""Scientific companion figure; read final versioned evaluation, never inference."""
import argparse
from collections import Counter
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--evaluation', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    d = json.loads(a.evaluation.read_text())
    if d.get('analysis_version') != 'post-freeze-correction-v2':
        raise ValueError('Use the explicitly versioned, retained correction')
    group = d['all_strata']['primary_autosomal_681']
    for arm in ('original', 'none'):
        if group[arm]['case_denominator'] != 681 or group[arm]['gene_denominator'] != 245:
            raise ValueError('Primary denominator changed')
    colors = {'original': '#22689A', 'none': '#7F8791'}
    labels = {'original': 'Original HPO', 'none': 'No HPO'}
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.subplots_adjust(top=.84, bottom=.20, hspace=.61, wspace=.29)
    fig.suptitle('Compact public benchmark: source-label recovery', x=.065, ha='left', y=.97, fontsize=19, weight='bold')
    fig.text(.065, .912, '681 autosomal signatures · 245 source genes · 10 constructed input hypotheses per case', fontsize=11)
    for ax, key, title in [(axes[0, 0], 'case_top_k_rates', 'A  Case-weighted recovery'),
                           (axes[0, 1], 'gene_macro_top_k_rates', 'B  Equal-weight gene average')]:
        x = np.arange(3)
        for i, arm in enumerate(('original', 'none')):
            result = group[arm]['primary_full_source_allele_recovery']
            rates = [result[key][str(k)] * 100 for k in (1, 5, 10)]
            bars = ax.bar(x + (i - .5)*.36, rates, width=.34, color=colors[arm], label=labels[arm])
            ax.bar_label(bars, labels=[f'{v:.1f}%' for v in rates], fontsize=9, padding=3)
        ax.set(xticks=x, xticklabels=['Top 1', 'Top 5', 'Top 10'], ylim=(0, 112), ylabel='Recovery (%)')
        ax.set_title(title, loc='left', fontsize=12, weight='bold')
        ax.grid(axis='y', alpha=.18); ax.set_axisbelow(True)
    axes[0, 0].legend(frameon=False, fontsize=9, loc='upper left', bbox_to_anchor=(-.01, 1.24), ncol=2)
    rows = [r for r in d['all_case_arm_results'] if not r['technical_X']]
    counts = {arm: Counter(r['filtered_gene_universe'] for r in rows if r['arm'] == arm) for arm in ('original', 'none')}
    if any(None in c for c in counts.values()):
        raise ValueError('Figure requires explicitly valid autosomal output universes; report failures first')
    support = sorted(set(counts['original']) | set(counts['none']))
    x = np.arange(len(support))
    for i, arm in enumerate(('original', 'none')):
        axes[1, 0].bar(x + (i - .5)*.36, [counts[arm][k] for k in support], width=.34, color=colors[arm])
    axes[1, 0].set(xticks=x, xticklabels=support, xlabel='Genes with ≥1 PASSED allele per output', ylabel='Number of cases')
    axes[1, 0].set_title('C  Surviving candidate universe', loc='left', fontsize=12, weight='bold')
    axes[1, 0].grid(axis='y', alpha=.18); axes[1, 0].set_axisbelow(True)
    pair = d['all_strata']['pairs_64']
    ax = axes[1, 1]; x = np.arange(2)
    for i, arm in enumerate(('original', 'none')):
        g = pair[arm]
        n = g['case_denominator']
        values = [g[name]['top_k_counts']['1'] for name in ('primary_full_source_allele_recovery', 'secondary_joint_best_mode_recovery')]
        bars = ax.bar(x + (i - .5)*.36, values, width=.34, color=colors[arm])
        ax.bar_label(bars, labels=[f'{v}/{n}' for v in values], fontsize=9, padding=3)
    ax.set(xticks=x, xticklabels=['All source alleles PASS\n+ source gene top 1', 'All source alleles in\none best mode + top 1'], ylim=(0, 74), ylabel='Recovered source pairs')
    ax.set_title('D  Stricter joint-mode check (64 pairs)', loc='left', fontsize=12, weight='bold')
    ax.grid(axis='y', alpha=.18); ax.set_axisbelow(True)
    for ax in axes.flat:
        for edge in ('top', 'right'): ax.spines[edge].set_visible(False)
        ax.tick_params(labelsize=9)
    fig.text(.065, .085, 'Primary success requires every exact source allele PASSED and conservative worst-tied gene rank.\nAll fixed denominators retain failures. Current database knowledge remains; source clinical papers are unadjudicated.\nThis compact construction is not whole-genome or clinical accuracy, a temporal knowledge holdout, or treatment validation.', fontsize=9, linespacing=1.5)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.output, dpi=180, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    main()
