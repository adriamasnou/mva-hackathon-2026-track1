#!/usr/bin/env python3
"""Offline consistency checks for proposed designs, quantities and price metadata.
This is not biological, analytical, procurement or experimental validation.
"""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote, urlsplit
import hashlib, json, re, subprocess, sys, tempfile
R=Path(__file__).resolve().parent
ROOT=R.parents[1]
def read(n): return json.loads((R/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks={}
def check(name, condition):checks[name]=bool(condition)
s=read('construct-specifications.json'); designs={x['name']:x for x in s['full_length_designs']};wt=designs['WT']['insert_DNA_5to3']
bases='TCAG'; aas='FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
codons={a+b+c:aa for (a,b,c),aa in zip(((a,b,c) for a in bases for b in bases for c in bases),aas)}
def tr(seq):return ''.join(codons[seq[i:i+3]] for i in range(0,len(seq),3))
check('reference_CDS_length_translation',len(wt)==3153 and len(tr(wt))==1051 and tr(wt).endswith('*') and '*' not in tr(wt)[:-1])
for name,x in designs.items():
 seq=x['insert_DNA_5to3']; expected=list(wt);edits_ok=True
 for start,ref,alt in x['edits_1based']:
  edits_ok &= wt[start-1:start-1+len(ref)]==ref
  expected[start-1:start-1+len(ref)]=alt
 differences=[{'position_1based':i+1,'reference':a,'alternate':b} for i,(a,b) in enumerate(zip(tr(wt),tr(seq))) if a!=b]
 check('design_'+name,edits_ok and seq==''.join(expected) and len(seq)==x['length_nt'] and hashlib.sha256(seq.encode()).hexdigest()==x['sha256_sequence'] and differences==x['amino_acid_changes'])
for x in s['four_existing_fragments']:
 expected=designs[x['name']]['insert_DNA_5to3'][(721-1)*3:1044*3];seq=x['insert_DNA_5to3']
 check('fragment_'+x['name'],seq==expected and len(seq)==972 and hashlib.sha256(seq.encode()).hexdigest()==x['sha256_sequence'])
check('distinct_nucleotide_alleles',designs['N1002K_TG']['insert_DNA_5to3'][3003:3006]=='AAG' and designs['N1002K_TA']['insert_DNA_5to3'][3003:3006]=='AAA' and tr(designs['N1002K_TG']['insert_DNA_5to3'])==tr(designs['N1002K_TA']['insert_DNA_5to3']))
check('no_duplex_overclaim',len(s['published_dsiRNA']['RNA_25nt'])==25 and not s['published_dsiRNA']['CDS_match'])
p=read('provider-evidence.json');by={x['id']:x for x in p['items']}
check('provider_classes_dates',len(by)==33 and all(x['url'].startswith('https://') and x['retrieval_date']=='2026-10-24' and x['project_quote'] is False and x['order_placed'] is False for x in by.values()))
check('unpriced_not_zero',len(p['unpriced_dependencies'])==21 and all(x['cost'] is None for x in p['unpriced_dependencies']))
check('RPE1_tier_unresolved','not resolved' in by['RPE1']['price_tier'] and 'not a universal academic' in by['RPE1']['notes'])
b=read('budget-calculations.json')
check('core_basket',b['core_starter_materials']['known_list_price_subtotals_only']=={'USD':2056.5,'EUR':605} and b['core_starter_materials']['total_project_cost'] is None)
check('LCL_basket',b['LCL_pilot_additions']['known_list_price_subtotals_only']=={'USD':1344,'EUR':123.2})
check('conditional_rates',abs(b['conditional_facility_scenarios_EUR']['CRG_6x48h_widefield_Academic_CERCA_eligibility_unconfirmed']-288*35.28)<1e-7)
supp=read('facility-supplement.json'); facilities={x['id']:x for x in supp['sources']}; captures=supp['capture_metadata']
check('facility_receipt_metadata',len(captures)==7 and all(x['status']==200 and x['url'].startswith('https://') and x['retrieved_at_utc'].startswith('2026-10-24T') and re.fullmatch('[0-9a-f]{64}',x['sha256']) and 'path' not in x for x in captures))
uv=facilities['uv-2026']; lumc=facilities['lumc-current-page']; crg=facilities['crg-access-policy']
check('UV_conditional_arithmetic',uv['conditional_arithmetic']['assumed_environment_separately_additive'] and abs(uv['conditional_arithmetic']['instrument_plus_environment_EUR']-288*(uv['rates']['DMi8_live_fluorescence']+uv['rates']['temperature_and_CO2_separate_row']))<1e-7)
check('LUMC_tiers_arithmetic',lumc['price_year'] is None and lumc['conditional_288h_widefield_EUR']=={'academic_eligibility_unconfirmed':288*lumc['external_academic']['widefield_per_hour'],'nonacademic_eligibility_unconfirmed':288*lumc['external_nonacademic']['widefield_per_hour']})
check('CRG_training_and_conditional_schedule',crg['policy_date']=='2026-02-03' and crg['published_rules']['staff_training_mandatory'] and crg['published_rules']['training_request_advance_weeks']==2 and crg['published_rules']['normal_live_cell_overnight_bookings_per_person_per_week']==3 and 'at least four weekly quota periods' in crg['conditional_schedule_inference'])
check('facility_full_totals_unquoted',supp['project_total'] is None and len(facilities)==3 and all(x['project_total'] is None and x['project_quote_received'] is False for x in facilities.values()))
a=read('arimoclomol-pilot-layout.json');rows=a['rows']; counts=Counter((x['culture_block'],x['assay'],x['plate']) for x in rows)
check('main_scope_807',len(rows)==756 and a['additional_process_control_wells']==27 and a['separate_stress_control_wells']==24 and a['main_and_controls_total']==807)
check('balanced_main_plates',len(counts)==18 and set(counts.values())=={42})
check('no_main_well_collisions',len({(x['culture_block'],x['assay'],x['plate'],x['well']) for x in rows})==756)
q=read('quantities.json');i=q['imaging_main_feasibility']
check('imaging_unconfirmed',i['positions_per_cycle']==336 and i['images_per_cycle']==672 and i['reserved_plate_hours_if_that_design_accepted']==288 and 'UNCONFIRMED' in i['status'])
check('preflight_separate',q['imaging_preflight']['wells']==4 and q['imaging_preflight']['images_per_cycle']==64 and q['imaging_preflight']['vehicle_only'])
f=read('flow-precision-layout.json');fc=Counter((x['day'],x['antibody_lot'],x['plate']) for x in f['rows'])
check('flow_scope',len(f['rows'])==576 and len(fc)==12 and set(fc.values())=={48} and q['flow_precision']['compensation_tubes']==24)
check('flow_antibody',abs(q['flow_precision']['primary_ug_20percent_overage']-129.6)<1e-6)
h=read('hts-1760-layout.json');hc=Counter(x['condition'] for x in h['rows'])
check('HTS_scope',len(h['rows'])==2304 and sum(n for k,n in hc.items() if k.startswith('compound_'))==1760 and hc['additional_vehicle']==160 and sum(hc[x] for x in ['vehicle','MG132_qualified','reference_GM12878','low_effect_qualified_control'])==384)
check('exposure_scope',q['LCMS_arimoclomol_scope']['subtotal_samples_before_calibration_QC']==276)
check('power_not_observations','prospective' in read('power-scenarios.json')['status'])
c=read('rfq-channels.json');text=(R/'quote-requests.md').read_text()
check('five_unsent_RFQs',len(re.findall(r'^## RFQ-0[1-5] ',text,re.M))==5 and 'UNSENT' in c['status'] and all(not x['project_accepted'] and not x['written_project_quote_received'] for x in c['channels']))
# Rebuild in isolation and compare actual generated bytes, without changing originals.
outputs=['budget-calculations.json','quantities.json','power-scenarios.json','flow-precision-layout.json','hts-1760-layout.json','arimoclomol-pilot-layout.json']
with tempfile.TemporaryDirectory(prefix='mva-lab-replay-') as d:
 t=Path(d)
 for name in ['build_quantities.py','provider-evidence.json']:(t/name).write_bytes((R/name).read_bytes())
 r=subprocess.run([sys.executable,str(t/'build_quantities.py')],capture_output=True,text=True)
 check('arithmetic_layout_replay',r.returncode==0 and all((t/n).read_bytes()==(R/n).read_bytes() for n in outputs))
manifest=read('manifest.json');problems=[]
for x in manifest['files']:
 f=ROOT/x['path']
 if not f.is_file() or sha(f)!=x['sha256']:problems.append(x['path'])
check('manifest_hashes',not problems)
md=[ROOT/x['path'] for x in manifest['files'] if x['path'].endswith('.md')];broken=[]
for f in md:
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',f.read_text()):
  u=urlsplit(target.strip('<>'))
  if u.scheme or not u.path:continue
  pth=(f.parent/unquote(u.path)).resolve()
  if not pth.is_relative_to(ROOT) or not pth.exists():broken.append([str(f.relative_to(ROOT)),target])
check('portable_links',not broken)
check('no_prohibited_inputs',not any(p.suffix in {'.fasta','.fna','.vcf','.bam','.cram','.pdf','.html','.gb'} for p in R.rglob('*') if p.is_file()))
check('no_outer_or_private_paths',all('/Users/' not in p.read_text() and '/Volumes/' not in p.read_text() and 'papers-local/' not in p.read_text() for p in R.glob('*') if p.suffix in {'.md','.json'}))
result={'status':'PASS' if all(checks.values()) else 'FAIL','scope':'offline planning consistency only; no biological measurements or accepted project quote','checks':checks,'manifest_files':len(manifest['files']),'hash_errors':problems,'broken_links':broken}
print(json.dumps(result,indent=2));sys.exit(not all(checks.values()))
