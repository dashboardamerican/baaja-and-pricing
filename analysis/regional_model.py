"""Conditional regional and national sensitivity ledger, not an official score.

PJM observed rate/NSPL inputs are paired with published large-load forecasts.
Capital, eligibility, prior recovery and post-2046 demand remain scenarios.
"""
from pathlib import Path
from math import isclose
import json
from reference import Assumptions,facility_twh,normalized_itc
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/evidence'
INPUT=json.loads((OUT/'pjm-regional-inputs.json').read_text())
FACTOR=.05/(1-1.05**-40)+.015

def cohort_cost(cohorts,year,capital,recovery):
 total=0
 for entry,mw in cohorts:
  age=year-entry
  if age>=40:continue
  if recovery=='annuity':factor=FACTOR
  elif recovery=='nominal_rate_base':
   # Synthetic utility-style profile, NOT a measured or approved revenue requirement.
   equity_share=.5;roe=.10;debt=.05;tax=.21;inflation=.025
   return_factor=(1-equity_share)*debt+equity_share*roe/(1-tax)
   factor=(return_factor*(1-(age+.5)/40)+1/40)/(1+inflation)**age+.015
  else:raise ValueError(recovery)
  total+=mw*capital*1e6*factor
 return total

def run(paths,pools,rates,capital=.65,coverage=.75,prior_recovery=0,recovery='annuity'):
 assert 0<=coverage<=1 and 0<=prior_recovery<=1
 cohorts={k:[] for k in paths};rows=[]
 for y in range(2027,2057):
  totals={k:0. for k in ['incremental','embedded','higher_of','AND','A_embedded','A_higher_of','B','existing_relief_embedded','A_after_prior_recovery']}
  for k,path in paths.items():
   q=coverage*path[y];previous=coverage*path[y-1]
   assert q+1e-8>=previous,'Nonmonotone cumulative path requires a retirement/exit model.'
   cohorts[k].append((y,max(0,q-previous)))
   I=cohort_cost(cohorts[k],y,capital,recovery);B0=pools[k]*rates[k];s=q/(pools[k]+q)
   embedded=s*(B0+I);higher=max(embedded,I);andpay=s*B0+I
   aE=andpay-embedded;aH=andpay-higher;b=andpay-I
   assert isclose(aE,(1-s)*I,abs_tol=.0001)
   assert isclose(aH,min((1-s)*I,s*B0),abs_tol=.0001)
   assert isclose(aE,(B0+I-embedded)-(B0+I-andpay),abs_tol=.0001)
   if y>=2030:
    values=[I,embedded,higher,andpay,aE,aH,b,aE,(1-prior_recovery)*aE]
    for name,v in zip(totals,values):totals[name]+=v/1e9
  rows.append({'year':y,**totals})
 summary={k:sum(r[k] for r in rows) for k in totals}
 return {'capital_million_per_MW':capital,'coverage':coverage,'prior_recovery_share_of_embedded_uplift':prior_recovery,
  'recovery':recovery,'summary_billion_2026_USD':summary,'annual_billion_2026_USD':rows}

# Reported total associated load (B9b), not adjustments above statistical trends.
# Hold the 2026 baseline fixed; cap at the maximum prior net-new load to avoid
# classifying a small forecast decrease as a new negative cohort.
paths={}
for zone,series in INPUT['large_load_forecast_B9b_MW'].items():
 series={int(k):v for k,v in series.items()};base=series[2026];path={2026:0};mx=0
 for y in range(2027,2047):mx=max(mx,series[y]-base,0);path[y]=mx
 for y in range(2047,2057):path[y]=path[2046]*1.015**(y-2046)
 paths[zone]=path
pools=INPUT['incumbent_MW'];rates=INPUT['rates_USD_per_MW_year']
regional=run(paths,pools,rates)
pooled_paths={'pooled':{y:sum(p[y] for p in paths.values()) for y in range(2026,2057)}}
pooled_pools={'pooled':sum(pools.values())}
pooled_rates={'pooled':sum(pools[k]*rates[k] for k in pools)/sum(pools.values())}
pooled=run(pooled_paths,pooled_pools,pooled_rates)

national=[]
for growth in ('low','medium','high'):
 p=Assumptions(growth_scenario=growth)
 national_path={'US':{y:max(0,facility_twh(y,p)-300)/8.76/.8*1000 for y in range(2026,2057)}}
 for capital in (.25,.4,.65,1,1.3,2):
  result=run(national_path,{'US':829000},{'US':95100},capital=capital)
  national.append({'growth':growth,**result})
central=next(r for r in national if r['growth']=='medium' and r['capital_million_per_MW']==.65)
p=Assumptions();npath={'US':{y:(facility_twh(y,p)-300)/8.76/.8*1000 for y in range(2026,2057)}}
prior=[run(npath,{'US':829000},{'US':95100},prior_recovery=f) for f in (0,.25,.5)]
coverage=[run(npath,{'US':829000},{'US':95100},coverage=f) for f in (.5,.75,1)]
recovery=[run(npath,{'US':829000},{'US':95100},recovery=f) for f in ('annuity','nominal_rate_base')]
# Boundary and aggregation checks have economic content, not only golden values.
zero=run(npath,{'US':829000},{'US':95100},capital=0)
assert abs(zero['summary_billion_2026_USD']['A_embedded'])<1e-9
assert isclose(prior[1]['summary_billion_2026_USD']['A_after_prior_recovery'],.75*central['summary_billion_2026_USD']['A_embedded'])
assert pooled['summary_billion_2026_USD']['A_embedded']>=regional['summary_billion_2026_USD']['A_embedded']
assert isclose(central['summary_billion_2026_USD']['A_embedded'],74.5925364538903,rel_tol=1e-12)
result={'status':'Conditional scenarios with measured regional inputs; not a calibrated national forecast or official fiscal score.',
 'horizon':'2027-2056; policy on in 2030; constant 2026 USD; undiscounted',
 'regional_scope':'PJM large-load-related forecast increments, not exclusively DCs; 2026 NSPL pools and August2026 NITS held fixed in real terms.',
 'post_2046':'Selected 1.5% annual growth of the new-load stock; not a PJM forecast.',
 'PJM_regional':regional,'PJM_pooled':pooled,
 'national_sensitivities':national,'national_prior_recovery_sensitivity':prior,
 'national_coverage_sensitivity':coverage,'national_cost_recovery_sensitivity':recovery,
 'ITC_repeated_30_year_billion':normalized_itc()['repeated_30yr_constant_2026_billion'],
 'cautions':['Incremental capital is assigned entirely to the host zone in this synthetic regional scenario; actual Schedule12 hybrid LRS/DFAX project allocation is not replayed.',
 'All capital values are scenarios; no national mean inferred from the matched convenience sample.',
 'Prior-recovery share is the fraction of modeled uplift already collected beyond embedded charges; it is not the prevalence of a tariff named AND. No national measured share is available.',
 'The synthetic nominal-rate-base sensitivity assumes 40-year straight-line depreciation, 50% equity, 10% nominal ROE, 5% debt, 21% federal income tax, 1.5% real O&M and 2.5% inflation. No ADIT or state-tax model; not an actual utility formula rate.',
 'Neither financial model establishes which physical upgrades are necessary or legally attributable.',
 'With an embedded baseline A can exceed B; the excess represents incremental cost shifted to others under the baseline. Do not describe A as always a subset of B.']}
(OUT/'regional-model-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'PJM_regional':regional['summary_billion_2026_USD'],'PJM_pooled':pooled['summary_billion_2026_USD'],
 'central':central['summary_billion_2026_USD'],
 'prior_recovery':[(r['prior_recovery_share_of_embedded_uplift'],r['summary_billion_2026_USD']['A_after_prior_recovery']) for r in prior],
 'recovery':[(r['recovery'],r['summary_billion_2026_USD']['A_embedded']) for r in recovery]},indent=2))
print('PASS: revenue transfers, comparator identities, no-cost boundary, prior-recovery scaling, aggregation effect and national JS benchmark.')
