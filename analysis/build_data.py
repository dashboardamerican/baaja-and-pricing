"""Build reproducible central output and independent JS-verification cases."""
from dataclasses import replace
from pathlib import Path
import json
from reference import Assumptions, reference_ledger, normalized_itc

ROOT=Path(__file__).resolve().parents[1]
p=Assumptions()
itc=normalized_itc(p)
central={'BAAJA':reference_ledger(p),'ITC':itc,
         'dollar_basis':'constant 2026 USD; undiscounted',
         'rate_note':'95.1 $/kW-year is a rounded national cost-to-peak proxy, not an observed tariff average.'}
(ROOT/'data/central-case.json').write_text(json.dumps(central,indent=2)+'\n')
cases=[]
for name,overrides in [('central',{}),('zero_cost',{'capex_per_mw':0}),
    ('zero_rate',{'nits_per_mw_year':0}),('high_cost_low_rate',{'capex_per_mw':1500000,'nits_per_mw_year':20000}),
    ('no_post_2030_growth',{'after_2030_growth':0}),('high_growth',{'after_2030_growth':.06}),
    ('high_rate',{'nits_per_mw_year':180000}),('low_cost',{'capex_per_mw':300000})]:
    q=replace(p,**overrides)
    cases.append({'name':name,'input':{'growth':q.after_2030_growth*100,'cost':q.capex_per_mw/1e6,'nits':q.nits_per_mw_year/1000},'reference':reference_ledger(q)})
(ROOT/'data/golden.json').write_text(json.dumps(cases,indent=2)+'\n')
print(json.dumps({'A':central['BAAJA']['metrics']['A_extra_AND_vs_higher_of_usd'],
                  'B':central['BAAJA']['metrics']['B_above_incremental_transmission_cost_usd'],
                  'ITC30':itc['repeated_30yr_constant_2026_billion']},indent=2))
