"""UCS published-demand and synthetic allocation checks; not a calibrated score."""
from pathlib import Path
import csv,json
from reference import facility_twh,Assumptions
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/evidence'
series={}
for row in csv.DictReader((DATA/'ucs-demand-inputs-MWh.csv').open()):
    total=sum(float(v) for k,v in row.items() if k not in ('scenario','subsector_group','year'))/1e6
    series.setdefault(row['scenario'],{})[int(row['year'])]=total
FACTOR=.05/(1-1.05**-40)+.015
def ledger(path,base):
    result={'A_billion_2026_USD':0.,'B_billion_2026_USD':0.,'incremental_cost_billion_2026_USD':0.}
    for year in range(2030,2057):
        mw=max(0,path[year]-base)/8.76/.8*1000*.75
        share=mw/(829000+mw)
        incremental=mw*650000*FACTOR
        result['A_billion_2026_USD']+=(1-share)*incremental/1e9
        result['B_billion_2026_USD']+=share*829000*95100/1e9
        result['incremental_cost_billion_2026_USD']+=incremental/1e9
    return result
existing={year:facility_twh(year,Assumptions()) for year in range(2026,2057)}
assert abs(ledger(existing,300)['A_billion_2026_USD']-74.5925364538903)<1e-9
results=[]
for name,points in series.items():
    path={}
    for year in range(2026,2051):
        lo=max(k for k in points if k<=year);hi=min(k for k in points if k>=year)
        path[year]=points[lo] if lo==hi else points[lo]+(points[hi]-points[lo])*(year-lo)/(hi-lo)
    for year in range(2051,2057):path[year]=path[2050]*1.015**(year-2050)
    common=path.copy()
    for year in range(2026,2031):common[year]=300+(points[2030]-300)*(year-2026)/4
    results.append({'source_scenario':name,'source_points_TWh':points,
        'interpolated_source_2026_TWh':path[2026],
        'tail_after_2050':'Selected 1.5% per year, not UCS forecast; common to all scenarios.',
        'source_2026_baseline_case':ledger(path,path[2026]),
        'common_300_TWh_2026_baseline_case':ledger(common,300)})
allocation=[]
for host_share in (1,.5,0):
    baseline=.5*host_share*100
    allocation.append({'incremental_cost_assigned_to_host_zone_share':host_share,
        'baseline_new_load_incremental_charge':baseline,
        'additional_after_direct_assignment':100-baseline,'other_customers_relief':100-baseline})
    assert abs((baseline+(100-baseline))-100)<1e-10
result={'status':'Research cross-checks, not new nationally calibrated score',
    'published_UCS_source':'https://github.com/ucsusa/eer_load_shapes/blob/7b980999a8f6e63172b834494b785f452b95fffb/UCS_load_profile_scaling/scaling_inputs_MWh.csv',
    'scope':'UCS data-center IT and cooling inputs; no presumption of identical crypto coverage to EPRI.',
    'baseline_model':ledger(existing,300),'UCS_path_sensitivities':results,
    'WIRES_reported_gross_capital_USD_per_MW':23.3e9/20000,
    'WIRES_ratio_caution':'23.3bn planned upgrades /20GW projected load; source authors estimate, not verified same-cohort, but-for, net newly assignable capital. Generator costs are not data-center observations.',
    'synthetic_two_zone_project_allocation':allocation,
    'project_allocation_caution':'Existing PJM zonal model places each zones selected incremental capital entirely in that zone. It does not replay actual Schedule12 hybrid LRS/DFAX project allocation.',
    'B_caution':'B measures transmission payment minus selected incremental transmission cost. It is not payment above fully allocated cost of service, profit, federal revenue, or policy-additional relief.'}
(DATA/'literature-crosschecks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'original':result['baseline_model'],'UCS_scenarios':results},indent=2))
print('PASS: original central result and synthetic allocation conservation.')
