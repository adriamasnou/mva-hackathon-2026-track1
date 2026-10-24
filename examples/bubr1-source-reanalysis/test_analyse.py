#!/usr/bin/env python3
"""Check source reproduction and fail-closed treatment of incomplete data."""
import copy
import json
from pathlib import Path
import unittest
from analyse import analyse

SOURCE = json.loads(Path(__file__).with_name('observations.json').read_text())

class SourceReanalysisTests(unittest.TestCase):
    def test_published_tpr_counts_and_medians(self):
        result = analyse(SOURCE)['tpr_2026_panels']
        self.assertEqual([g['n'] for g in result['Figure 4B']], [27, 38, 39, 37])
        self.assertEqual([round(g['median']) for g in result['Figure 4B']], [650, 110, 60, 40])
        self.assertEqual([g['n'] for g in result['Figure 4F']], [40, 40, 40])
        self.assertEqual([round(g['median']) for g in result['Figure 4F']], [455, 295, 175])

    def test_missing_panel_is_not_success(self):
        d = copy.deepcopy(SOURCE)
        del d['tpr_2026']['panels']['Figure 4F']
        with self.assertRaises(ValueError): analyse(d)

    def test_missing_group_is_not_success(self):
        d = copy.deepcopy(SOURCE)
        d['tpr_2026']['panels']['Figure 4B'].pop()
        with self.assertRaises(ValueError): analyse(d)

    def test_bad_observations_are_not_imputed(self):
        for bad in (None, float('nan'), float('inf'), -1, True):
            with self.subTest(bad=bad):
                d = copy.deepcopy(SOURCE)
                d['tpr_2026']['panels']['Figure 4B'][0]['observations'][0]['value'] = bad
                with self.assertRaises(ValueError): analyse(d)

    def test_deleted_cell_fails(self):
        d = copy.deepcopy(SOURCE)
        d['tpr_2026']['panels']['Figure 4B'][0]['observations'].pop()
        with self.assertRaises(ValueError): analyse(d)

    def test_changed_distribution_fails(self):
        d = copy.deepcopy(SOURCE)
        for row in d['tpr_2026']['panels']['Figure 4B'][0]['observations']:
            row['value'] += 10
        with self.assertRaises(ValueError): analyse(d)

    def test_nonfinite_comparator_fails(self):
        d = copy.deepcopy(SOURCE)
        d['tpr_2026']['panels']['Figure 4B'][0]['printed_median'] = float('nan')
        with self.assertRaises(ValueError): analyse(d)

if __name__ == '__main__': unittest.main()
