"""BAAJA planning score, constant 2026 dollars. No statistical forecast claim.

U is annual incremental transmission recovery still in shared rates under the
baseline, AFTER existing direct recovery. D (already direct) cancels between
policy worlds. No generation/distribution or federal revenue is counted.
"""
from pathlib import Path
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
GROWTH = json.loads((ROOT / 'growth-audit.json').read_text())
PJM = json.loads((ROOT / 'pjm-regional-inputs.json').read_text())
CENTRAL = dict(path='central', net_capital_million_per_MW=.4, coverage=.75,
               load_factor=.8, billing_multiplier=1., incumbent_MW=829000.,
               rate_USD_per_MW_year=95100., real_finance=.05, life=40,
               om=.015, inflation=.025, start=2030, first_eligible=2027,
               recovery='real_levelized', regional=False, pjm_share=.5,
               other_load_growth=0., inherited_cost_growth=0., terminal_protection=False,
               anchor2030=None, real_capital_growth=0.)


def paths(p):
    demand = {int(y): e for y, e in GROWTH['annual_paths_TWh'][p['path']].items()}
    if p['anchor2030'] is not None:
        # Keep the same 2026 cohort baseline across near-term forecast tests.
        base = demand[2026]
        old = demand[2030]
        for y in range(2027, 2057):
            demand[y] = (base * (p['anchor2030']/base)**((y-2026)/4)
                         if y <= 2030 else demand[y] * p['anchor2030']/old)
    return demand


def cost(cohorts, year, p, eligible_only=False):
    value = 0.
    for entry, mw in cohorts:
        age = year-entry
        if age >= p['life'] or (eligible_only and entry < p['first_eligible']):
            continue
        if p['recovery'] == 'real_levelized':
            f = p['real_finance']/(1-(1+p['real_finance'])**-p['life']) + p['om']
        elif p['recovery'] == 'nominal_rate_base':
            # Transparent synthetic utility profile; not a filed formula rate.
            # 50%equity, 10%ROE, 5%debt, 21%tax, 40yr straight-line depreciation.
            ret = .5*.05 + .5*.10/(1-.21)
            f = (ret*(1-(age+.5)/p['life'])+1/p['life'])/(1+p['inflation'])**age + p['om']
        else:
            raise ValueError(p['recovery'])
        # Optional expiry of ANNUAL contract recovery after20years. Irrevocable
        # upfront CIAC does not return to rate base. This is a selected scenario.
        k = p['net_capital_million_per_MW']
        if p['terminal_protection'] and age >= 20:
            k += .25
        value += mw*k*1e6*(1+p['real_capital_growth'])**(entry-2026)*f
    return value


def calculate(**overrides):
    p = {**CENTRAL, **overrides}
    assert p['net_capital_million_per_MW'] >= 0 and 0 <= p['coverage'] <= 1
    demand = paths(p)
    physical_path = {y: max(0., demand[y]-demand[2026])/8.76/p['load_factor']*1000*p['coverage']
             for y in range(2026,2057)}
    qpath = {y:mw*p['billing_multiplier'] for y,mw in physical_path.items()}
    if p['regional']:
        # Regional stress test, not empirical national regional attribution.
        # Split half covered growth to PJM, using actual zonal billing pools and
        # 2035 forecast-growth weights; rest retains residual national cost pool.
        wg = {z:max(0., v['2035']-v['2026']) for z,v in PJM['large_load_forecast_B9b_MW'].items()}
        wtot = sum(wg.values())
        groups = {z:dict(w=p['pjm_share']*wg[z]/wtot, N=n, rate=PJM['rates_USD_per_MW_year'][z])
                  for z,n in PJM['incumbent_MW'].items()}
        nrest = p['incumbent_MW']-sum(g['N'] for g in groups.values())
        brest = p['incumbent_MW']*p['rate_USD_per_MW_year']-sum(g['N']*g['rate'] for g in groups.values())
        assert nrest>0 and brest>0
        groups['Other_US'] = dict(w=1-p['pjm_share'], N=nrest, rate=brest/nrest)
    else:
        groups = {'US':dict(w=1., N=p['incumbent_MW'], rate=p['rate_USD_per_MW_year'])}
    cohorts = {z:[] for z in groups}
    rows = []
    for y in range(2027,2057):
        row = dict(year=y, facility_TWh=demand[y], covered_new_GW=physical_path[y]/1000,
                   billing_new_GW=qpath[y]/1000,
                   additional_payments=0., new_positive_surplus=0., deficit_repair=0.,
                   postpolicy_surplus=0., baseline_signed_surplus=0.,
                   net_incremental_recovery=0., noneligible_dc_credit=0.,
                   inherited_customer_relief=0.)
        for z,g in groups.items():
            q = qpath[y]*g['w']
            cohorts[z].append((y,(physical_path[y]-physical_path[y-1])*g['w']))
            qeligible = sum(mw for entry,mw in cohorts[z] if entry>=p['first_eligible'])*p['billing_multiplier']
            n = g['N']*(1+p['other_load_growth'])**(y-2026)
            b = g['N']*g['rate']*(1+p['inherited_cost_growth'])**(y-2026)
            u = cost(cohorts[z],y,p)
            ue = cost(cohorts[z],y,p,True)
            s = q/(n+q)
            se = qeligible/(n+q)
            # Common already-direct D omitted equally from payments and cost.
            pre = se*(b+u)
            post = ue+se*(b+u-ue)
            a = post-pre
            gnew = max(post-ue,0.)-max(pre-ue,0.)
            noneligible_credit = (s-se)*ue
            incumbent_relief = (1-s)*ue
            assert math.isclose(a, (1-se)*ue, abs_tol=1e-4)
            assert math.isclose(a, noneligible_credit+incumbent_relief, abs_tol=1e-4)
            assert math.isclose(pre+(1-se)*(b+u), b+u, abs_tol=1e-4)
            assert math.isclose(post+(1-se)*(b+u-ue), b+u, abs_tol=1e-4)
            assert gnew >= -1e-4 and gnew <= a+1e-4
            if p['first_eligible']==2027:
                assert math.isclose(gnew,min(a,s*b),abs_tol=1e-4)
            if y >= p['start']:
                for key,v in [('additional_payments',a),('new_positive_surplus',gnew),
                              ('deficit_repair',max(0.,a-gnew)),('postpolicy_surplus',post-ue),
                              ('baseline_signed_surplus',pre-ue),('net_incremental_recovery',ue),
                              ('noneligible_dc_credit',noneligible_credit),
                              ('inherited_customer_relief',incumbent_relief)]:
                    row[key] += v/1e9
        row['nominal_new_positive_surplus'] = row['new_positive_surplus']*(1+p['inflation'])**(y-2026)
        row['PV3_new_positive_surplus'] = row['new_positive_surplus']/(1.03)**(y-2026)
        rows.append(row)
    keys=[k for k in rows[0] if k not in ['year','facility_TWh','covered_new_GW','billing_new_GW']]
    totals={k:sum(r[k] for r in rows) for k in keys}
    return dict(assumptions=p,totals_billion=totals,annual=rows)


def main():
    cases = {'central':calculate()}
    variants = {
        'low_residual_capital':dict(net_capital_million_per_MW=.15),
        'high_residual_capital':dict(net_capital_million_per_MW=.8),
        'all_costs_already_directly_recovered':dict(net_capital_million_per_MW=0.),
        'old_065_all_newly_assignable':dict(net_capital_million_per_MW=.65),
        'flat_after2030':dict(path='flat_after_2030'),
        'EIA_US_server_growth_shape':dict(path='eia_shape'),
        'BNEF_US_capacity_growth_shape':dict(path='bnef_shape'),
        'LBNL_521_anchor':dict(anchor2030=521),
        'LBNL_843_anchor':dict(anchor2030=843),
        'IEA_426_anchor':dict(anchor2030=426),
        'coverage50pct':dict(coverage=.5),
        'coverage90pct':dict(coverage=.9),
        'billing90pct':dict(billing_multiplier=.9),
        'billing83pct':dict(billing_multiplier=.83),
        'effective_facility_load_factor90pct':dict(load_factor=.9),
        'effective_pool75pct':dict(incumbent_MW=829000*.75),
        'nominal_rate_base_profile':dict(recovery='nominal_rate_base'),
        'first_eligible2030':dict(first_eligible=2030),
        'start2028':dict(start=2028),
        'start2033':dict(start=2033),
        'other_load_grows1pct':dict(other_load_growth=.01),
        'inherited_cost_declines1pct':dict(inherited_cost_growth=-.01),
        'NITS60k':dict(rate_USD_per_MW_year=60000.),
        'NITS150k':dict(rate_USD_per_MW_year=150000.),
        'regional_PJM50pct':dict(regional=True),
        'regional_PJM70pct':dict(regional=True,pjm_share=.7),
        'regional_high_cost':dict(regional=True,net_capital_million_per_MW=.8),
        'protection_ends20years':dict(terminal_protection=True),
        'real_construction_cost_growth1pct':dict(real_capital_growth=.01),
        'real_construction_cost_growth2pct':dict(real_capital_growth=.02),
        'joint_low':dict(anchor2030=521,path='flat_after_2030',net_capital_million_per_MW=.15,coverage=.5,billing_multiplier=.9),
        'joint_high':dict(path='eia_shape',net_capital_million_per_MW=.8,coverage=.9,regional=True),
    }
    cases.update({k:calculate(**v) for k,v in variants.items()})
    tests=[]
    def check(name,condition):
        assert condition,name
        tests.append({'check':name,'passed':True})
    c=cases['central']['totals_billion']
    check('Central payment gain equals new positive surplus; no pooled baseline deficit',math.isclose(c['additional_payments'],c['new_positive_surplus'],abs_tol=1e-8))
    check('Postpolicy minus baseline signed contribution equals additional payments',math.isclose(c['postpolicy_surplus']-c['baseline_signed_surplus'],c['additional_payments'],abs_tol=1e-8))
    check('All prior direct recovery means zero additional score',cases['all_costs_already_directly_recovered']['totals_billion']['new_positive_surplus']==0)
    check('Zero growth means zero score',calculate(anchor2030=GROWTH['baseline_2026_TWh'],path='flat_after_2030')['totals_billion']['new_positive_surplus']<1e-9)
    check('Zero inherited charge leaves no above-incremental surplus',abs(calculate(rate_USD_per_MW_year=0)['totals_billion']['new_positive_surplus'])<1e-8)
    check('NITS changes do not change total uplift under fixed residual costs',math.isclose(cases['NITS60k']['totals_billion']['additional_payments'],c['additional_payments'],abs_tol=1e-8))
    check('Billing-only coincidence change preserves physical cost',math.isclose(cases['billing90pct']['totals_billion']['net_incremental_recovery'],c['net_incremental_recovery'],abs_tol=1e-8))
    check('Higher cost case separates deficit repair from surplus',calculate(net_capital_million_per_MW=2.)['totals_billion']['deficit_repair']>0)
    check('Grandfathered DC credits reconcile to all eligible additional payments',math.isclose(cases['first_eligible2030']['totals_billion']['additional_payments'],cases['first_eligible2030']['totals_billion']['noneligible_dc_credit']+cases['first_eligible2030']['totals_billion']['inherited_customer_relief'],abs_tol=1e-8))
    # Hand examples independent of national calibration.
    for i,expectedA,expectedG in [(15,150/11,100/11),(5,50/11,50/11)]:
        s=100/1100;pre=s*(100+i);post=i+s*100
        check(f'Hand example I={i}',math.isclose(post-pre,expectedA) and math.isclose(max(post-i,0)-max(pre-i,0),expectedG))
    out={'as_of':'2026-10-25','status':'Judgmental central planning case, not a measured national expectation, fully allocated cost-of-service finding, or official fiscal score.',
         'scope':'New DC cohort2027–2056; policy charges2030–2056; constant2026USD levelized-payment equivalents; excludes cryptocurrency, generation/distribution and pre2027existingDCincremental obligations.',
         'estimand':'Increase in positive contribution above incremental transmission service cost: sum(max(P_AND-C,0)-max(P_baseline-C,0)); costs and physical service held fixed.',
         'central_choice':'0.4m/MW residual newlyassignablecapital is author judgment informed by primary cost and funding examples. It is NOT a nationally estimated residual cost or a quantified prior-recovery fraction.',
         'rounded_central_billion_2026_USD':50,
         'one_way_capital_scenario_range_billion_2026_USD':[20,100],
         'range_status':'Rounded one-at-a-time residual-capital scenarios only; not a confidence interval or joint bounds. Zero and wider joint cases also reported.',
         'cases':cases,'checks':tests,
         'input_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'growth-audit.json',ROOT/'capital-evidence.json',ROOT/'pjm-regional-inputs.json']}}
    (ROOT/'score-results.json').write_text(json.dumps(out,indent=2)+'\n')
    with (ROOT/'central-annual.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(cases['central']['annual'][0]));w.writeheader();w.writerows(cases['central']['annual'])
    with (ROOT/'sensitivity.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=['case']+list(c));w.writeheader()
        for name,r in cases.items():w.writerow({'case':name,**r['totals_billion']})
    print(json.dumps({'central':c,'cases':{k:round(v['totals_billion']['new_positive_surplus'],3) for k,v in cases.items()},'checks':len(tests)},indent=2))


if __name__=='__main__':
    main()
