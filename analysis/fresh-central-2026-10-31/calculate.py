"""Fresh BAAJA planning projection; standard library, constant 2026 dollars.

Run python3 calculate.py. Inputs copied with their evidence metadata; no network
access needed. Dollars are levelized annual service/payment equivalents, not
literal cash timing of CIAC or a utility's filed revenue-requirement schedule.
"""
from pathlib import Path
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
GROWTH = json.loads((ROOT / 'growth-audit.json').read_text())
PJM = json.loads((ROOT / 'pjm-regional-inputs.json').read_text())
BASE = dict(growth_path='central', anchor2030=None, coverage=.75,
            physical_load_factor=.8, billing_multiplier=1.,
            gross_capital_million_per_MW=.65, existing_direct_fraction=.35,
            existing_om_direct_fraction=0.,
            real_capital_escalation=.01, real_financing=.05,
            recovery_life=40, annual_om_fraction=.015,
            incumbent_MW=829000., national_initial_rate_per_MW=95100.,
            regional=True, pjm_new_load_share=.5,
            incumbent_load_growth=.01, inherited_revenue_growth=.01,
            policy_start=2030, inflation=.025)


def calculate(**overrides):
    p = {**BASE, **overrides}
    demand = {int(y): v for y, v in GROWTH['annual_paths_TWh'][p['growth_path']].items()}
    if p['anchor2030'] is not None:
        old = demand[2030]
        for y in range(2027, 2057):
            demand[y] = (demand[2026] * (p['anchor2030']/demand[2026])**((y-2026)/4)
                         if y <= 2030 else demand[y]*p['anchor2030']/old)
    capacity = {y: max(0, demand[y]-demand[2026])*1e6/8760/p['physical_load_factor']*p['coverage']
                for y in range(2026, 2057)}
    factor = p['real_financing']/(1-(1+p['real_financing'])**-p['recovery_life']) + p['annual_om_fraction']
    if p['regional']:
        weights = {z: max(0, v['2035']-v['2026']) for z, v in PJM['large_load_forecast_B9b_MW'].items()}
        total = sum(weights.values())
        groups = {z: dict(N=n, rate=PJM['rates_USD_per_MW_year'][z],
                         w=p['pjm_new_load_share']*weights[z]/total)
                  for z, n in PJM['incumbent_MW'].items()}
        nrest = p['incumbent_MW']-sum(x['N'] for x in groups.values())
        brest = p['incumbent_MW']*p['national_initial_rate_per_MW']-sum(x['N']*x['rate'] for x in groups.values())
        groups['Other_US'] = dict(N=nrest, rate=brest/nrest, w=1-p['pjm_new_load_share'])
    else:
        groups = dict(US=dict(N=p['incumbent_MW'], rate=p['national_initial_rate_per_MW'], w=1))
    rows, details, cohorts = [], [], []
    payment_fields = ['gross_incremental_cost', 'common_existing_direct_equivalent',
                      'residual_incremental_cost', 'baseline_embedded_payment',
                      'higher_of_benchmark', 'and_payment', 'extra_above_baseline',
                      'total_above_defined_cost', 'baseline_shortfall_to_benchmark',
                      'above_incremental_cost', 'baseline_above_incremental_signed',
                      'other_ratepayer_relief', 'above_selected_fully_allocated',
                      'pure_gross_rollin_higherof', 'above_pure_gross_rollin_higherof']
    for y in range(2027, 2057):
        cohorts.append((y, capacity[y]-capacity[y-1]))
        capital = sum(mw*p['gross_capital_million_per_MW']*1e6*(1+p['real_capital_escalation'])**(entry-2026)
                      for entry, mw in cohorts if y-entry < p['recovery_life'])
        ctotal = capital*factor
        row = dict(year=y, facility_TWh=demand[y], covered_new_GW=capacity[y]/1000,
                   billed_new_GW=capacity[y]*p['billing_multiplier']/1000,
                   assigned_gross_capital_billion=capital/1e9,
                   incremental_dominant_GW_years=0., gross_rollin_incremental_dominant_GW_years=0.)
        row.update({f: 0. for f in payment_fields})
        for name, g in groups.items():
            q = capacity[y]*p['billing_multiplier']*g['w']
            n = g['N']*(1+p['incumbent_load_growth'])**(y-2026)
            b = g['N']*g['rate']*(1+p['inherited_revenue_growth'])**(y-2026)
            s = q/(n+q)
            c = ctotal*g['w']
            # CIAC covers capital, not automatically operating expense.
            d = capital*g['w']*(p['existing_direct_fraction']*(factor-p['annual_om_fraction'])
                                +p['existing_om_direct_fraction']*p['annual_om_fraction'])
            u = c-d
            embedded = s*(b+u)
            p0 = d+embedded
            h = max(p0, c)
            p1 = c+s*b
            a = p1-p0
            above_h = p1-h
            # Alternative removes existing direct obligations and puts gross
            # incremental cost in the common pool. It is a different baseline.
            egross = s*(b+c)
            hgross = max(egross, c)
            assert math.isclose(a, (1-s)*u, abs_tol=1e-5)
            assert math.isclose(above_h, min(a, s*b), abs_tol=1e-5)
            assert math.isclose(h, d+max(embedded,u), abs_tol=1e-5)
            assert math.isclose(p0+(1-s)*(b+u), b+c, abs_tol=1e-5)
            assert math.isclose(p1+(1-s)*b, b+c, abs_tol=1e-5)
            vals = dict(gross_incremental_cost=c, common_existing_direct_equivalent=d,
                        residual_incremental_cost=u, baseline_embedded_payment=p0,
                        higher_of_benchmark=h, and_payment=p1, extra_above_baseline=a,
                        total_above_defined_cost=above_h, baseline_shortfall_to_benchmark=h-p0,
                        above_incremental_cost=p1-c, baseline_above_incremental_signed=p0-c,
                        other_ratepayer_relief=(1-s)*u, above_selected_fully_allocated=p1-(c+s*b),
                        pure_gross_rollin_higherof=hgross, above_pure_gross_rollin_higherof=p1-hgross)
            if y >= p['policy_start']:
                for k, v in vals.items(): row[k] += v/1e9
                if c > p0: row['incremental_dominant_GW_years'] += q/1000
                if c > egross: row['gross_rollin_incremental_dominant_GW_years'] += q/1000
                details.append(dict(year=y, pool=name, billing_share=s,
                                    inherited_revenue_billion=b/1e9, billed_new_GW=q/1000,
                                    **{k:v/1e9 for k,v in vals.items()}))
        row['nominal_extra_above_baseline'] = row['extra_above_baseline']*(1+p['inflation'])**(y-2026)
        row['PV3_extra_above_baseline'] = row['extra_above_baseline']/(1.03)**(y-2026)
        rows.append(row)
    totals = {f: sum(r[f] for r in rows) for f in payment_fields+['nominal_extra_above_baseline','PV3_extra_above_baseline']}
    exposure = sum(r['billed_new_GW'] for r in rows if r['year'] >= p['policy_start'])
    shares = {k: sum(r[k] for r in rows)/exposure if exposure else 0.
              for k in ['incremental_dominant_GW_years','gross_rollin_incremental_dominant_GW_years']}
    return dict(inputs=p, annual_recovery_factor=factor, totals_billion_2026_USD=totals,
                cost_regime_exposure_shares=shares, annual=rows, pool_ledger=details)


def main():
    central = calculate()
    variants = {
        'gross_cost_030m': dict(gross_capital_million_per_MW=.3),
        'gross_cost_100m': dict(gross_capital_million_per_MW=1.),
        'gross_cost_200m_stress': dict(gross_capital_million_per_MW=2.),
        'no_prior_direct_funding': dict(existing_direct_fraction=0.),
        'prior_direct_funding70pct': dict(existing_direct_fraction=.7),
        'all_already_directly_funded': dict(existing_direct_fraction=1.,existing_om_direct_fraction=1.),
        '35pct_allin_funding_including_OM': dict(existing_om_direct_fraction=.35),
        'flat_energy_after2030': dict(growth_path='flat_after_2030'),
        'faster_EIA_server_growth_shape': dict(growth_path='eia_shape'),
        'LBNL_low2030': dict(anchor2030=521),
        'LBNL_high2030': dict(anchor2030=843),
        'IEA_2030_anchor': dict(anchor2030=426),
        'coverage50pct': dict(coverage=.5),
        'coverage90pct': dict(coverage=.9),
        'billing90pct': dict(billing_multiplier=.9),
        'physical_load_factor90pct': dict(physical_load_factor=.9),
        'pooled_US': dict(regional=False),
        'PJM70pct': dict(pjm_new_load_share=.7),
        'no_real_construction_escalation': dict(real_capital_escalation=0.),
        'construction_escalation2pct': dict(real_capital_escalation=.02),
        'NITS_grows1pct_real': dict(inherited_revenue_growth=.02),
        'NITS_declines1pct_real_approx': dict(inherited_revenue_growth=0.),
        'financing4pct': dict(real_financing=.04),
        'financing6pct': dict(real_financing=.06),
        'policy_start2028': dict(policy_start=2028),
        'policy_start2033': dict(policy_start=2033),
        'joint_low': dict(gross_capital_million_per_MW=.3,existing_direct_fraction=.7,growth_path='flat_after_2030',coverage=.5),
        'joint_high': dict(gross_capital_million_per_MW=1.,existing_direct_fraction=0.,growth_path='eia_shape',coverage=.9),
    }
    sensitivities=[]
    for name, override in variants.items():
        result=calculate(**override)
        sensitivities.append(dict(scenario=name, changed_inputs=override,
                                 **result['totals_billion_2026_USD'],
                                 incremental_dominant_exposure_share=result['cost_regime_exposure_shares']['incremental_dominant_GW_years']))
    t=central['totals_billion_2026_USD']
    tests=[]
    def check(label, condition):
        assert condition,label
        tests.append(dict(check=label,passed=True))
    check('Primary two headlines differ only by baseline shortfall to the specified benchmark', math.isclose(t['extra_above_baseline']-t['total_above_defined_cost'],t['baseline_shortfall_to_benchmark'],abs_tol=1e-8))
    check('Extra payments equal other-ratepayer credits', math.isclose(t['extra_above_baseline'],t['other_ratepayer_relief'],abs_tol=1e-8))
    check('AND minus total incremental cost equals inherited contribution', math.isclose(t['and_payment']-t['gross_incremental_cost'],t['above_incremental_cost'],abs_tol=1e-8))
    check('Selected fully allocated benchmark gives zero above-benchmark payment', abs(t['above_selected_fully_allocated'])<1e-8)
    fullyfunded=next(r for r in sensitivities if r['scenario']=='all_already_directly_funded')
    check('Full existing direct funding gives no additional payments', abs(fullyfunded['extra_above_baseline'])<1e-8)
    check('No growth gives zero payments', abs(calculate(growth_path='flat_after_2030',anchor2030=GROWTH['baseline_2026_TWh'])['totals_billion_2026_USD']['extra_above_baseline'])<1e-8)
    check('Two cost regimes occur in actual zonal central implementation',0<central['cost_regime_exposure_shares']['incremental_dominant_GW_years']<1)
    output=dict(as_of='2026-10-31',unit='billions of constant 2026 USD; undiscounted sum of levelized annual payment equivalents',
                horizon='2027–2056 eligible growth; charges 2030–2056',
                scope='Transmission only; fixed demand/investment between tariff worlds; excludes generation, distribution, crypto, pre-2027 existing DCs, and other bill provisions.',
                status='Evidence-informed central planning judgment, not a probability-weighted forecast or official fiscal score.',
                headline_definitions=dict(extra_above_baseline='AND less the sum of embedded transmission charges and common preexisting direct obligations.',
                    total_above_defined_cost='AND less the chosen higher-of adequate-service-payment benchmark: maximum of the total embedded-plus-direct obligation and full attributable incremental service cost. This is an operational allocation benchmark, not independently established fully allocated cost of service.'),
                headline_rounded_billion=dict(extra_above_baseline=55,total_above_defined_cost=55),
                central=central,sensitivities=sensitivities,checks=tests,
                input_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['growth-audit.json','pjm-regional-inputs.json','capital-evidence.json']})
    (ROOT/'final-results.json').write_text(json.dumps(output,indent=2)+'\n')
    for filename, data in [('annual.csv', central['annual']),('pool-ledger.csv',central['pool_ledger']),('sensitivity.csv',sensitivities)]:
        with (ROOT/filename).open('w') as f:
            writer=csv.DictWriter(f,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
    print(json.dumps(dict(central=t,regimes=central['cost_regime_exposure_shares'],checks=tests,
                         sensitivity=[dict(case=r['scenario'],A=round(r['extra_above_baseline'],2),B=round(r['total_above_defined_cost'],2)) for r in sensitivities]),indent=2))


if __name__ == '__main__': main()
