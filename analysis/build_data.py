"""Build reproducible central output and independent JS-verification cases."""
from dataclasses import replace
from pathlib import Path
import json
from reference import Assumptions, reference_ledger, normalized_itc, facility_twh

ROOT=Path(__file__).resolve().parents[1]
p=Assumptions()
itc=normalized_itc(p)
central={'BAAJA':reference_ledger(p),'ITC':itc,
         'dollar_basis':'constant 2026 USD; undiscounted',
         'growth_note':'EPRI U.S. 2030 Medium anchor; IEA global 2030-35 Base multiplier transferred to U.S.; selected taper to 1.5% by 2040, then held to 2056. Not a published 2056 forecast.',
         'rate_note':'95.1 $/kW-year is a rounded national cost-to-peak proxy, not an observed tariff average.'}
(ROOT/'data/central-case.json').write_text(json.dumps(central,indent=2)+'\n')
cases=[]
for name,overrides in [('central',{}),('zero_cost',{'capex_per_mw':0}),
    ('zero_rate',{'nits_per_mw_year':0}),('high_cost_low_rate',{'capex_per_mw':1500000,'nits_per_mw_year':20000}),
    ('higher_of_high_cost',{'baseline':'higher_of','capex_per_mw':1500000}),('low_growth',{'growth_scenario':'low'}),('high_growth',{'growth_scenario':'high'}),
    ('high_rate',{'nits_per_mw_year':180000}),('low_cost',{'capex_per_mw':300000})]:
    q=replace(p,**overrides)
    cases.append({'name':name,'input':{'growth':q.growth_scenario,'cost':q.capex_per_mw/1e6,'nits':q.nits_per_mw_year/1000,'baseline':q.baseline},'reference':reference_ledger(q)})
(ROOT/'data/golden.json').write_text(json.dumps(cases,indent=2)+'\n')
growth={
    'as_of':'2026-10-23','unit':'TWh/year, total U.S. facility electricity use',
    'status':'Published U.S. 2030 endpoints with analyst extrapolations after 2030; not confidence intervals.',
    'baseline':{'year':2026,'twh':300,'status':'Selected common modeling baseline, not an observed annual total.'},
    'method':[
        '2027-2030: geometric interpolation from selected 2026 baseline to each EPRI endpoint.',
        '2031-2035: apply IEA GLOBAL 2030-2035 demand multiplier to each EPRI U.S. 2030 endpoint. This geographic and scope transfer is an analyst assumption.',
        '2036-2040: annual growth rate declines in five equal steps from bridge rate to selected mature rate.',
        '2041-2056: hold selected mature annual growth rate constant. No terminal value.'
    ],
    'sources':[
        {'organization':'EPRI','title':'Powering Intelligence 2026, Annual and Peak Electricity Use',
         'url':'https://powering-intelligence.epri.com/annual-peak-use.html','updated':'2026-02-24',
         'locator':'Text accompanying Figure 5','us_2030_twh':{'low':383,'medium':596,'high':793},
         'scope':'Includes small and large data centers and cryptocurrency mining.'},
        {'organization':'IEA','title':'Key Questions on Energy and AI, 2026',
         'url':'https://iea.blob.core.windows.net/assets/3179f7f8-01f6-4dd6-bffa-c9f7b73f1dc9/KeyQuestionsonEnergyandAI.pdf#page=108',
         'locator':'Table A.1, printed page 108, Total electricity consumption (TWh)',
         'global_2030_2035_twh':{'Headwinds':[833,942],'Base':[945,1193],'Lift-Off':[1008,1637]},
         'scope':'Global, scope differs from EPRI including cryptocurrency; 2035 figures are exploratory scenarios. Used only for growth multipliers, not U.S. absolute levels.'}
    ],
    'limitations':[
        'IEA global scenario multipliers are not U.S. forecasts. EPRI and IEA absolute levels are not averaged.',
        'Post-2035 taper and mature rates (0.5%, 1.5%, 2.5%) are selected assumptions to represent slower expansion after the initial buildout, not rates published by EPRI or IEA.',
        'The three cases are sensitivities, not probabilities or a comprehensive forecast range. A different 2026 baseline or realized location and tariff coverage changes receipts.'
    ],'scenarios':{}
}
for key,anchor,a,b,tail,iea in [('low',383,833,942,.005,'Headwinds'),('medium',596,945,1193,.015,'Base'),('high',793,1008,1637,.025,'Lift-Off')]:
    q=replace(p,growth_scenario=key)
    ledger=reference_ledger(q)
    growth['scenarios'][key]={'label':key.capitalize(),'epri_2030_twh':anchor,'iea_bridge_scenario':iea,
        'annual_growth_2031_2035':(b/a)**.2-1,'annual_growth_from_2040':tail,
        'annual_twh':{str(y):facility_twh(y,q) for y in range(2026,2057)},
        'A_billion':ledger['metrics']['A_extra_AND_vs_baseline_usd']['constant_2026_billion'],
        'B_billion':ledger['metrics']['B_above_incremental_transmission_cost_usd']['constant_2026_billion']}
(ROOT/'data/growth-scenarios.json').write_text(json.dumps(growth,indent=2)+'\n')
print(json.dumps({'A':central['BAAJA']['metrics']['A_extra_AND_vs_baseline_usd'],
                  'B':central['BAAJA']['metrics']['B_above_incremental_transmission_cost_usd'],
                  'ITC30':itc['repeated_30yr_constant_2026_billion']},indent=2))
