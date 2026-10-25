"""Verify the independent Claude review's quantitative claims and counterexamples.

Grandfathered entrants retain physical investment and ordinary billing obligations.
They can receive shared-rate credits, so eligible-only gross payments differ from
net payments by all modeled data centers and from 2026-incumbent bill relief.
"""
from pathlib import Path
from math import isclose
import json
from reference import Assumptions,reference_ledger,facility_twh
ROOT=Path(__file__).resolve().parents[1]
p=Assumptions();base=reference_ledger(p)
factor=base['annual_incremental_cost_per_mw']/p.capex_per_mw
A=base['metrics']['A_extra_AND_vs_baseline_usd']['constant_2026_billion']
B=base['metrics']['B_above_incremental_transmission_cost_usd']['constant_2026_billion']
baseline_surplus=sum(r['baseline_payment_usd']-r['incremental_cost_usd'] for r in base['annual'] if r['year']>=p.charging_start)/1e9
assert isclose(baseline_surplus,B-A,rel_tol=1e-12)

def scope_case(charge_start,first_eligible_year):
    pre_mw=(facility_twh(first_eligible_year-1,p)-300)/8.76/p.load_factor*1000*p.effective_chargeable_fraction
    incumbent_relief=eligible_extra=grandfathered_credit=0
    for row in base['annual']:
        if row['year']<charge_start:continue
        q=row['effective_new_billing_gw']*1000
        eligible=max(0,q-pre_mw)
        grandfathered=q-eligible
        total=p.incumbent_pool_mw+q
        increment=eligible*p.capex_per_mw*factor
        inc=p.incumbent_pool_mw/total*increment
        gross=(1-eligible/total)*increment
        credit=grandfathered/total*increment
        assert isclose(inc,gross-credit,rel_tol=1e-12)
        incumbent_relief+=inc/1e9;eligible_extra+=gross/1e9;grandfathered_credit+=credit/1e9
    return {'charges_begin':charge_start,'first_eligible_entry_year':first_eligible_year,
        'net_all_DC_extra_equals_2026_incumbent_relief_billion':incumbent_relief,
        'eligible_DC_gross_extra_billion':eligible_extra,
        'grandfathered_DC_shared_credit_billion':grandfathered_credit}
original=scope_case(2030,2027)
assert isclose(original['net_all_DC_extra_equals_2026_incumbent_relief_billion'],A,rel_tol=1e-12)
grand=scope_case(2030,2030)

# The pooled result is not a general upper bound on project-allocation effects.
# A zone has 100 incumbent and 100 new MW; B has 100 incumbent MW; cost is100.
host=100-(100/(100+100))*100
pooled=100-(100/300)*100
split=100-(100/(100+100))*50
hybrid=100-((100/300)*50+(100/(100+100))*0)
assert host<pooled<split<hybrid

result={'status':'Verified conditional model findings; not calibration or legal conclusions',
    'reviewer':'Claude Opus 5.5, high effort, CLI-reported model claude-opus-5-5',
    'central':{'A_billion':A,'B_billion':B,'baseline_above_incremental_billion':baseline_surplus,
        'A_PV_2026_at_3pct_real_billion':base['metrics']['A_extra_AND_vs_baseline_usd']['pv_2026_billion'],
        'capital_threshold_USD_per_MW':p.nits_per_mw_year/factor,
        'A_change_per_100000_USD_per_MW_billion':A*100000/p.capex_per_mw},
    'scope_cases':[original,scope_case(2032,2027),grand,scope_case(2032,2032),scope_case(2035,2035)],
    'pre2030_share_of_central_A':1-grand['net_all_DC_extra_equals_2026_incumbent_relief_billion']/A,
    'allocation_counterexample':{'host_only':host,'one_pooled_grid':pooled,'half_to_each_zone':split,
        'half_pooled_LRS_plus_half_DFAX_to_nonhost':hybrid},
    'qualifications':['Grandfathering here is an implementation sensitivity, not a claim that section2107(a) legally requires it.',
        'Section228 prospective applicability appears in section2107(b), not an express grandfathering rule in section2107(a).',
        'Section228 incremental-cost floor overlaps transmission dollars but does not itself mandate the full additive AND payment.',
        'The national baseline-surplus finding does not establish that every project or customer covers costs.',
        'The threshold assumes constant levelized costs and the national NITS proxy; regional rates and annual recovery profiles differ.',
        'The pooled result is not a general upper bound; actual project allocation data are required.',
        'A depends on pool size; it is independent of the inherited NITS rate only under the embedded comparator and fixed physical/billing assumptions.']}
(ROOT/'data/evidence/claude-review-crosschecks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
print('PASS: baseline surplus, exact PV/slope/threshold, grandfathering cash-flow conservation and allocation counterexample.')
