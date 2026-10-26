"""Worked annual accounting examples for METHODS.md, not empirical forecasts.
Run from any directory; outputs data/evidence/methods-examples.json.
"""
from pathlib import Path
from math import isclose
import json
ROOT=Path(__file__).resolve().parents[1]
def example(added_cost):
 inherited_cost=100.;old_MW=1000.;new_MW=100.;share=new_MW/(old_MW+new_MW)
 total=inherited_cost+added_cost
 dc_baseline=share*total
 dc_and=added_cost+share*inherited_cost
 old0=inherited_cost;old1=total-dc_baseline;old2=total-dc_and
 harm=old1-old0;relief=old1-old2;net=old2-old0
 assert isclose(old1+dc_baseline,total) and isclose(old2+dc_and,total)
 assert isclose(net,harm-relief) and isclose(relief,dc_and-dc_baseline)
 assert isclose(dc_and-added_cost,-net)
 return {'inputs':{'inherited_annual_cost_million':inherited_cost,'inherited_billing_demand_MW':old_MW,'new_billing_demand_MW':new_MW,'added_annual_cost_million':added_cost},'world0':{'total_requirement_million':inherited_cost,'DC_payment_million':0.,'existing_payment_million':old0},'world1':{'total_requirement_million':total,'DC_payment_million':dc_baseline,'existing_payment_million':old1},'world2':{'total_requirement_million':total,'DC_payment_million':dc_and,'existing_payment_million':old2},'H_existing_bill_change_from_DC_million':harm,'R_additional_policy_relief_million':relief,'net_existing_bill_change_with_policy_million':net,'DC_payment_above_incremental_cost_with_policy_million':dc_and-added_cost}
a=example(15.);b=example(5.)
assert isclose(a['H_existing_bill_change_from_DC_million'],50/11)
assert isclose(a['R_additional_policy_relief_million'],150/11)
assert isclose(b['H_existing_bill_change_from_DC_million'],-50/11)
assert isclose(b['R_additional_policy_relief_million'],50/11)
result={'status':'Selected illustrations, not utility observations. Single pool, fixed physical build, no other revenues, direct capital funding or demand response. All amounts millions of dollars per year.','cases':{'ordinary_pricing_raises_existing_bills':a,'ordinary_pricing_already_reduces_existing_bills':b},'checks':['Revenue conservation in both pricing worlds','H minus R equals net incumbent change','Extra DC payments equal all-other-customer relief in the specified two-group pool','Positive and negative baseline impacts against exact hand-calculated values']}
(ROOT/'data/evidence/methods-examples.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: three-world accounting, positive and negative baseline effects, and bill-transfer conservation.')
