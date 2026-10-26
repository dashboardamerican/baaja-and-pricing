"""Primary estimand: DC payment increase vs embedded, equal to other-payer relief.

This explicitly includes correction of any baseline incremental-cost deficit.
It differs from the positive-surplus estimand in the earlier score assessment.
"""
from pathlib import Path
import csv
import json
import math
from score import calculate, CENTRAL
ROOT=Path(__file__).resolve().parent

def short(name,**kw):
    c=calculate(**kw)
    t=c['totals_billion']
    return {'scenario':name,'assumptions':c['assumptions'],
       'additional_DC_payments_billion_2026':t['additional_payments'],
       'other_payer_relief_billion_2026':t['inherited_customer_relief']+t['noneligible_dc_credit'],
       'baseline_deficit_repair_billion_2026':t['deficit_repair'],
       'above_higher_of_billion_2026':t['additional_vs_higher_of'],
       'nominal_equivalent_billion':t['nominal_additional_payments'],
       'PV3_billion_2026':t['PV3_additional_payments'],
       'incremental_dominant_exposure_share':c['incremental_dominant_share_of_charged_billing_MW_years']}

capital=[short(f'Residual capital ${k:.2f}m/MW',net_capital_million_per_MW=k) for k in [.15,.4,.8,1.3,2.]]
sens=[short('Reference'),short('All prior direct recovery',net_capital_million_per_MW=0),
 short('No growth after2030',path='flat_after_2030'),short('EIA server growth shape',path='eia_shape'),
 short('LBNL521TWh2030',anchor2030=521),short('LBNL843TWh2030',anchor2030=843),
 short('IEA426TWh2030',anchor2030=426),short('Coverage50%',coverage=.5),short('Coverage90%',coverage=.9),
 short('PJM zones50% of covered growth',regional=True),short('PJM zones70% of covered growth',regional=True,pjm_share=.7),
 short('Utility rate-base recovery',recovery='nominal_rate_base'),
 short('Only post2029 entrants eligible',first_eligible=2030),
 short('Construction real escalation2%',real_capital_growth=.02),
 short('Joint lower scenario',anchor2030=521,path='flat_after_2030',net_capital_million_per_MW=.15,coverage=.5,billing_multiplier=.9),
 short('Joint higher scenario',path='eia_shape',net_capital_million_per_MW=2,coverage=.9,regional=True)]
matrix=[short(f'{path}, ${k}m/MW',path=path,net_capital_million_per_MW=k)
        for path in ['flat_after_2030','central','eia_shape'] for k in [.15,.4,.8,1.3,2.]]
mix=json.loads((ROOT/'regime-results.json').read_text())['mixtures']
tests=[]
for r in capital+sens+matrix:
    assert math.isclose(r['additional_DC_payments_billion_2026'],r['other_payer_relief_billion_2026'],abs_tol=1e-7)
    assert math.isclose(r['additional_DC_payments_billion_2026'],r['baseline_deficit_repair_billion_2026']+r['above_higher_of_billion_2026'],abs_tol=1e-7)
tests+=['Every scenario reconciles DC payment increase to total other-payer credits.',
        'Every scenario splits total relief into deficit repair and gain above higher-of.']
assert capital[-1]['nominal_equivalent_billion']>calculate(net_capital_million_per_MW=2)['totals_billion']['nominal_new_positive_surplus']
tests+=['High-cost nominal transfer uses total payments, not positive-surplus-only series.']
assert math.isclose(capital[-1]['additional_DC_payments_billion_2026'],234.05554758957456,rel_tol=1e-12)
assert math.isclose(mix[2]['totals_billion_2026_USD']['additional_payments'],140.43332855374473,rel_tol=1e-12)
tests+=['High-cost and50/50mix match independent algebraic scaling of reference residual cost.']
result={'as_of':'2026-10-26','estimand':'BAAJA minus embedded-baseline DC payments, including deficit repair; equals credits to other payers at fixed total recovery.',
 'scope':'Introduced S5653 section2107(a), specified credited-AND implementation, new2027–2056 DCgrowth; charges2030–2056; constant2026USD levelized equivalents.',
 'status':'Conditional scenario analysis. No measured national residual cost, regime mix, statutory implementation or probability distribution.',
 'headline':'About$50bn reference; selected capital scenarios about$20–235bn at central growth. Not probability bounds.',
 'capital_scenarios':capital,'sensitivities':sens,'growth_cost_matrix':matrix,'mixtures':mix,'checks':tests}
(ROOT/'transfer-results.json').write_text(json.dumps(result,indent=2)+'\n')
columns=[k for k in capital[0] if k!='assumptions']
with (ROOT/'transfer-scenarios.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=columns);w.writeheader()
    for r in capital+sens+matrix:w.writerow({k:r[k] for k in columns})
print(json.dumps({'capital':[{k:r[k] for k in columns} for r in capital],
                 'sensitivities':{r['scenario']:r['additional_DC_payments_billion_2026'] for r in sens},'checks':tests},indent=2))
