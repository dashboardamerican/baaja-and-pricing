"""Two cost regimes crossed with two tariff baselines; selected scenarios only."""
import json
import math
from pathlib import Path
from score import calculate, CENTRAL

ROOT=Path(__file__).resolve().parent

def annual_example(incremental):
    b,s=100.,.1
    e=s*(b+incremental)
    after=s*b
    and_payment=incremental+after
    higher=max(e,incremental)
    return dict(unit='million dollars per year',inherited_requirement=b,billing_share=s,
                incremental=incremental,embedded_before_credit=e,embedded_after_credit=after,
                higher_of=higher,AND=and_payment,
                additional_vs_embedded=and_payment-e,
                additional_vs_higher_of=and_payment-higher,
                shortfall_under_embedded=max(incremental-e,0.))

def mixture(high_share):
    # Independent pools have the SAME demand-to-incumbent ratio and tariff rate.
    # Split both inherited pool and new demand. Only residual capital differs.
    # This produces a transparent weighted illustration, not measured geography.
    totals={k:0. for k in ['additional_payments','additional_vs_higher_of','deficit_repair','postpolicy_surplus']}
    for fraction,capital in [(1-high_share,.4),(high_share,2.)]:
        if fraction==0:continue
        c=calculate(incumbent_MW=CENTRAL['incumbent_MW']*fraction,
                    coverage=CENTRAL['coverage']*fraction,
                    net_capital_million_per_MW=capital)['totals_billion']
        for k in totals:totals[k]+=c[k]
    assert math.isclose(totals['additional_payments'],totals['additional_vs_higher_of']+totals['deficit_repair'],abs_tol=1e-8)
    return {'selected_high_cost_share_of_billing_exposure':high_share,'totals_billion_2026_USD':totals}

examples=[annual_example(5),annual_example(20)]
assert math.isclose(examples[0]['additional_vs_higher_of'],4.5)
assert math.isclose(examples[1]['additional_vs_higher_of'],10.)
assert math.isclose(examples[1]['additional_vs_embedded'],18.)
mix=[mixture(x) for x in [0,.25,.5,.75,1]]
assert math.isclose(mix[2]['totals_billion_2026_USD']['additional_vs_higher_of'],
                    (mix[0]['totals_billion_2026_USD']['additional_vs_higher_of']+mix[-1]['totals_billion_2026_USD']['additional_vs_higher_of'])/2,abs_tol=1e-8)
result={'as_of':'2026-10-26',
 'status':'Conditional regime scenarios; no measured national mixture or independent fully allocated cost-of-service finding.',
 'definitions':{'E':'ordinary rolled-in charge before the new direct-payment credit',
                'I':'annual incremental recovery not already directly funded; common direct payments omitted equally',
                'E_after':'embedded charge after incremental payments are credited to shared revenue requirement',
                'AND':'I + E_after',
                'higher_of':'max(E,I)'},
 'formulas':{'E':'s*(B+I)','E_after':'s*B = E-s*I',
             'above_embedded':'(1-s)*I',
             'above_higher_of':'min((1-s)*I,s*B)'},
 'threshold_capital_million_per_MW':CENTRAL['rate_USD_per_MW_year']/(.05/(1-1.05**-40)+.015)/1e6,
 'threshold_scope':'Only with constant unit costs, billing proxy=physical proxy, same cost pool, stated financing and no other cohort costs. Not national empirical breakpoint.',
 'annual_examples':examples,
 'mixture_assumptions':{'low_residual_capital_million_per_MW':.4,'high_residual_capital_million_per_MW':2.,
     'pool_structure':'Independent proportional clones of the central national pool. High share is analyst-selected; it is not share of sites or a measured US fraction.'},
 'mixtures':mix}
(ROOT/'regime-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
