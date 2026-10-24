"""Local planning arithmetic, layouts and public-list baskets. No purchases or network.
These outputs are proposed procurement scopes, not experimental observations.
"""
from pathlib import Path
import json, math, random
from statistics import NormalDist
R=Path(__file__).resolve().parent

def save(name,obj): (R/name).write_text(json.dumps(obj,indent=2)+'\n')
# Read provider ledger, keeping null costs and independent currencies.
p=json.loads((R/'provider-evidence.json').read_text())
by={x['id']:x for x in p['items']}
baskets={
 'core_starter_materials': {'ARIMO':1,'NMN':1,'PBA':1,'MG132':1,'NOC':1,'RNAIMAX':1,'FBS':1,'PLATES96':1,'HELA':1},
 'LCL_pilot_additions': {'GM21284':1,'GM12878':1,'GM18502':1,'RPMI':4},
 'optional_nontransformed_model': {'RPE1':1},
 'alternative_Addgene_WT_route_not_additive_to_custom_vector': {'ADDGENE_WT':1},
}
out={}
for label,items in baskets.items():
 rows=[];sums={}
 for key,n in items.items():
  x=by[key]; amount=round(x['price']*n,2) if x['price'] is not None else None
  rows.append({'provider_item':key,'pack_quantity':n,'pack_size':x['pack'],'unit_price':x['price'],'currency':x['currency'],'extended':amount,'evidence_class':x['class'],'tier_and_eligibility':x.get('price_tier',x['notes'])})
  if amount is not None:sums[x['currency']]=round(sums.get(x['currency'],0)+amount,2)
 out[label]={'rows':rows,'known_list_price_subtotals_only':sums,'total_project_cost':None}
# Formula estimates intentionally separate from SKU list prices and service quotes.
out['formula_estimates']={
 'four_972bp_fragments_low_medium_standard_expression_USD':round(4*(972*.09+55),2),
 'four_972bp_fragments_independent_QC_USD':4*15,
 'four_3153bp_CDS_custom_vector_low_medium_USD':round(4*(3153*.13+75)+500,2),
 'four_CDS_plus_empty_vector_QC_USD':5*15,
 'warning':'Length brackets, complexity tier, custom vector acceptance, final junctions/tags and vector delivery unconfirmed. Empty-vector construction cost excluded. Custom formula is not a quote. No additive total across alternative construct routes.'}
out['conditional_facility_scenarios_EUR']={
 'CRG_6x48h_widefield_Academic_CERCA_eligibility_unconfirmed':round(288*35.28,2),
 'CRG_12h_supervision_same_eligibility':12*82.5,
 'CRG_24h_analysis_same_eligibility':24*89.16,
 'UB_8h_flow_public_institution_reduced':8*60.63,
 'UB_8h_flow_private_centre_official':8*99.03,
 'warning':'Conditional rate arithmetic only, NOT an imaging quote or demonstrated feasible schedule; six sequential 48h runs require counterbalanced staggered cultures or accepted multiposition capacity; eligibility, instrument mapping, staffing, VAT, minimum billing and booking unconfirmed. Not summed with each other.'}
save('budget-calculations.json',out)
# Explicit corrected flow precision layout: 12 conditions x12 technical wells.
conditions=['GM21284_unstained','GM21284_isotype','GM21284_secondary_only','GM21284_baseline','GM12878_baseline','GM18502_baseline','GM21284_vehicle_2h','GM21284_MG132_2h','GM21284_vehicle_4h','GM21284_MG132_4h','GM21284_vehicle_6h','GM21284_MG132_6h']
inner=[f'{r}{c:02}' for r in 'BCDEFG' for c in range(2,12)]
flow=[]
# Four repeats of every condition on EACH of three plates, positions randomized.
for day in [1,2]:
 for lot in ['A','B']:
  for plate in range(1,4):
   labels=[{'condition':c,'technical_rep_in_plate':i+1} for c in conditions for i in range(4)]
   random.Random(20261024+100*day+10*ord(lot)+plate).shuffle(labels)
   for well,label in zip(inner,labels):flow.append({'day':day,'antibody_lot':lot,'plate':plate,'well':well,**label})
save('flow-precision-layout.json',{'status':'proposed; execute only after panel/depletion qualification','edges':'all perimeter wells buffer; no samples','samples_per_plate':48,'unallocated_inner_wells_per_plate':12,'samples_total':len(flow),'rows':flow,'external_compensation_tubes_per_day_lot':6,'notes':'Compensation tubes separate; unstained and secondary-only are omission controls. Two lots do not prove all future lots equivalent.'})
# Broad screen always uses all wells, with outer COLUMNS as controls, no false edge exclusion.
hts=[];compound=1
for plate in range(1,7):
 for ri,row in enumerate('ABCDEFGHIJKLMNOP'):
  for col in range(1,25):
   if col in [1,2,23,24]:
    condition=['vehicle','MG132_qualified','reference_GM12878','low_effect_qualified_control'][[1,2,23,24].index(col)]
   elif compound<=1760:condition=f'compound_{compound:04}';compound+=1
   else:condition='additional_vehicle'
   hts.append({'plate':plate,'well':f'{row}{col:02}','condition':condition})
save('hts-1760-layout.json',{'status':'proposed; perimeter positions require qualification; no low-effect drug known yet','rows':hts,'compound_wells':1760,'fixed_control_wells':384,'additional_vehicle_wells':160,'all_wells':len(hts)})
# Full-length discovery matrix; independent culture-day, clone and cell levels retained.
rows=[]
for block in range(1,4):
 for genotype in ['WT','N1002K_TG']:
  for clone in [1,2]:
   for dose in [0,.2,.6,1,2,4,10]:
    for duration in [6,24,48]:
     for assay in ['live','lysate','fixed']:
      rows.append({'culture_block':block,'genotype':genotype,'clone':clone,'arimoclomol_uM':dose,'duration_h':duration,'assay':assay,'volume_uL':150,'status':'pilot','independence':'cells nested in well/clone/culture block'})
# Within each block/assay 84 wells in 2 plates; no position shared deterministically with treatment.
for block in range(1,4):
 for ai,assay in enumerate(['live','lysate','fixed']):
  ix=[i for i,x in enumerate(rows) if x['culture_block']==block and x['assay']==assay]
  random.Random(20261024+10*block+ai).shuffle(ix)
  for j,i in enumerate(ix):rows[i]['plate']=1+j//42;rows[i]['well']=inner[j%42]
save('arimoclomol-pilot-layout.json',{'status':'proposed not performed; final seeding and imaging require qualification','main_wells':len(rows),'main_plates':18,'main_wells_per_plate':42,'usable_inner_capacity':60,'balance_note':'Randomized 42+42 main wells per block/assay; final layout and sequential culture blocking require laboratory approval','rows':rows,'additional_process_control_wells':27,'separate_stress_control_wells':24,'main_and_controls_total':807})
# Dose mass and counts for explicit scopes, not for an undefined entire project.
quant={
 'imaging_preflight':{'status':'proposed development only; not efficacy or a powered defect test','wells':4,'conditions':['WT replacement depleted','N1002K replacement depleted','empty depleted','WT nondepleted'],'clones_per_construct':1,'culture_preparations':1,'vehicle_only':True,'fields_per_well':8,'channels':2,'positions_per_cycle':32,'images_per_cycle':64,'cadence_minutes_proposed_not_accepted':3},
 'imaging_main_feasibility':{'wells_per_plate':42,'fields_per_well':8,'channels':2,'positions_per_cycle':336,'images_per_cycle':672,'proposed_cycle_seconds':180,'maximum_mean_seconds_per_image_including_all_overhead':180/672,'single_plate_48h_runs':6,'reserved_plate_hours_if_that_design_accepted':288,'status':'UNCONFIRMED; demonstrate exposure, autofocus, stage and channel-switch cycle; counterbalance staggered cultures or use accepted multiposition capacity; otherwise downsize/recalculate'},
 'model_titration':{'genotypes':5,'induction_levels_ng_mL':[0,1,10,100],'depletion_conditions':2,'culture_blocks':3,'clones_per_genotype':1,'assays':2,'wells':5*4*2*3*2},
 'arimoclomol_pilot':{'main_wells':756,'additional_controls':51,'total':807,'media_mL_main':756*.15,'arimoclomol_mg_main_no_overage':sum(x['arimoclomol_uM']*.15/1000*313.8/1000 for x in rows),'media_with_20percent_handling_mL_main':756*.15*1.2},
 'comparator_window_pilot':{'genotypes':2,'PBA_uM':[100,300,1000],'NMN_uM':[50,100,500],'vehicle_conditions':2,'times_h':[24,48],'culture_blocks':3,'assays':2,'wells':2*8*2*3*2},
 'four_way_comparison':{'genotypes':2,'conditions':4,'culture_blocks':3,'clones':2,'assays':3,'times':1,'wells':2*4*3*2*3,'status':'pilot design; final confirmatory n unknown'},
 'HSP_dependency_pilot':{'genotypes':2,'RNAi_conditions':['NC1','HSPA1A_B_duplex1','HSPA1A_B_duplex2'],'drug_conditions':2,'culture_blocks':3,'assays':3,'wells':2*3*2*3*3},
 'LCMS_arimoclomol_scope':{'cell_conditions_samples':144,'matched_vehicle_samples':36,'cell_free_stability_samples':48,'binding_free_total_samples':48,'subtotal_samples_before_calibration_QC':276,'calibration_QC_and_method_development':None},
 'flow_precision':{'samples':576,'compensation_tubes':24,'cells_per_sample':500000,'minimum_loaded_cells':600*500000,'cells_with20percent_handling':600*500000*1.2,'staining_volume_uL_per_sample':50,'primary_positive_samples':9*12*4,'primary_ug_at_5ug_mL':9*12*4*.05*5,'primary_ug_20percent_overage':9*12*4*.05*5*1.2,'excludes':'titration, specificity, WB and repeat failures'},
 'HTS_1760':{'plates':6,'all_wells':2304,'candidate_cells_per_well_to_qualify':50000,'cells_at_candidate_scale':2304*50000,'cells_if_unminiaturized_500000':2304*500000,'staining_uL':20,'primary_ug_at_5ug_mL':2304*.02*5,'primary_ug_with20percent_overage':2304*.02*5*1.2,'events_at25000_each':2304*25000,'acquisition_hours_at_1000_events_second_excluding_every_overhead':2304*25000/1000/3600,'sample_cycle_hours_at60seconds_per_well':2304*60/3600,'warning':'event-rate arithmetic is not demonstrated throughput; 50k loaded may fail 25k retained; scale back up if recovery fails'},
 'HTS_confirm_per_hit':{'doses':10,'starting_uM':30,'dilution_factor':3,'independent_days':3,'wells_per_day_dose':1,'total_wells_per_hit':30,'plus':'vehicle/reference/fluorescence/counter-screen/fate and function controls separate'},
 'fragment_production':{'constructs':4,'independent_preps_each':3,'preps':12,'requested_final_mass_mg_each':0.5,'total_mg':6,'purity_requested_percent':90,'target_monomer_percent':80,'numbers_status':'proposed RFQ acceptance criteria, not existing yield'},
}
save('quantities.json',quant)
# Prospective approximate normal-theory paired-block sample sizes, NOT a data analysis.
z=NormalDist().inv_cdf(.975)+NormalDist().inv_cdf(.90)
save('power-scenarios.json',{'status':'prospective examples only; final n requires pilot variance, biologically justified margins, multiplicity and cluster simulation','unit':'independent paired culture-day difference in error proportion, clones/cells nested','formula':'ceil((z_0.975+z_0.90)^2 * SD_difference^2 / (expected_effect - minimum_worthwhile_effect)^2)','rows':[{'SD_difference':s,'effect_above_margin':g,'normal_approximate_n':math.ceil(z*z*s*s/(g*g)),'planning_minimum_blocks':max(6,math.ceil(z*z*s*s/(g*g)))} for s in [.025,.05,.1] for g in [.025,.05]],'power':.90,'two_sided_alpha':.05,'not_accounted':'small-n t critical values, variance uncertainty, failed cultures, dose selection/multiple comparisons, clone correlations; counts are not released confirmatory sample sizes'})
print('Saved budgets, three proposed layouts, quantities and prospective power scenarios.')
