#!/usr/bin/env python3
"""Arithmetic only; no dosing recommendation. Label: MIPLYFFA 2026-03-18 §§11–12."""
import json
# Salt MW 505.90 minus citrate counterion 192.12 = free-base MW 313.78 g/mol.
MW = 505.90 - 192.12

def ng_ml_to_um(value):
    if value < 0:
        raise ValueError('Concentration cannot be negative')
    return value / MW

if __name__ == '__main__':
    print(json.dumps({'free_base_mw_g_mol':round(MW,2),
      'pediatric_NPC_mean_trough_um':ng_ml_to_um(206),
      'pediatric_NPC_mean_peak_um':ng_ml_to_um(523),
      'warning':'Serum estimates are not intracellular free concentrations or sustained peak exposure; this is not MVA dosing advice.'},indent=2))
