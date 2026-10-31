"""Reproduce the one-pager scenario band, timing case and ITC comparison.

All cases hold other central inputs fixed; the band is selected, not statistical.
Run alongside calculate.py and its three input JSON files. No third-party packages.
"""
import json
from pathlib import Path
from calculate import calculate

ROOT = Path(__file__).resolve().parent
central = calculate()
results = {}
for name, overrides in [
    ('central', {}),
    ('lower_band_50pct_prior_capital_funding', {'existing_direct_fraction': .5}),
    ('upper_band_faster_growth_075m_capital', {'growth_path': 'eia_shape', 'gross_capital_million_per_MW': .75}),
    ('lower_cost_sensitivity', {'gross_capital_million_per_MW': .3}),
]:
    r = calculate(**overrides)['totals_billion_2026_USD']
    results[name] = dict(overrides=overrides, additional_payments_bn=r['extra_above_baseline'], above_higherof_bn=r['total_above_defined_cost'])

annual = {r['year']:r for r in central['annual']}
old_cap = annual[2029]['assigned_gross_capital_billion']
old_load = annual[2029]['billed_new_GW']
a = b = 0.
for r in central['pool_ledger']:
    year = annual[r['year']]
    old_fraction = old_cap / year['assigned_gross_capital_billion']
    s = r['billing_share'] * (1-old_load/year['billed_new_GW'])
    c = r['gross_incremental_cost'] * (1-old_fraction)
    d = r['common_existing_direct_equivalent'] * (1-old_fraction)
    k = r['inherited_revenue_billion'] + r['residual_incremental_cost'] * old_fraction
    p0 = d + s*(k+c-d)
    p1 = c + s*k
    a += p1-p0
    b += p1-max(p0,c)
results['only_2030_and_later_entrants'] = dict(additional_payments_bn=a, above_higherof_bn=b, method='Keep pre-2030 load in billing denominators and its residual upgrade costs in shared revenue; reprice only later entrants. Same investment and demand, collections beginning 2030.')

historical = dict(zip(range(2022,2032), [0,0,0,.788,1.213,1.213,1.213,2.001,2.426,2.425]))
itc = 3*sum(v/1.025**(y-2026) for y,v in historical.items())
assert abs(sum(historical.values())-11.279) < 1e-10
assert abs(a-35.354409864494535) < 1e-8
report = dict(
    description='Selected central-to-higher scenario band, rounded from $46.8bn to $103.4bn to approximately $50-100bn. Lower cases are explicitly disclosed; not a confidence interval or bounds. Central model unchanged.',
    units='Billions of constant 2026 dollars, undiscounted annual payment equivalents',
    scenarios=results,
    itc=dict(source='https://www.govinfo.gov/content/pkg/GOVPUB-Y4_T19_4-PURL-gpo172711/pdf/GOVPUB-Y4_T19_4-PURL-gpo172711.pdf', official_historical_nominal_bn=11.279, historical_fiscal_year_nominal_bn=historical, assumed_inflation=.025, illustrative_30year_bn=itc, method='Normalize each FY amount by 1.025^(year-2026), then repeat that real ten-year profile three times. This resets the historical ramp each decade. Not an official score or continuing-program forecast.'),
    comparison=dict(central_multiple=results['central']['additional_payments_bn']/itc, rounded_band_multiples=[50/itc,100/itc]),
)
(ROOT/'brief-scenarios.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
