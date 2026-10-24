"""Generate an auditable HTML research report from the reviewed evidence files."""
from pathlib import Path
import json,csv,html
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/evidence'
a=json.loads((DATA/'inventory-audit.json').read_text());s=json.loads((DATA/'matched-sample-audit.json').read_text());r=json.loads((DATA/'regional-model-results.json').read_text())
packages=list(csv.DictReader((DATA/'miso26-matched-packages.csv').open()))
def esc(x):return html.escape(str(x))
def table(headers,rows):
 return '<div class="table"><table><thead><tr>'+''.join('<th>'+esc(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
regional=r['PJM_regional']['summary_billion_2026_USD'];pooled=r['PJM_pooled']['summary_billion_2026_USD']
medium=[x for x in r['national_sensitivities'] if x['growth']=='medium']
body='''<p class="eyebrow">DASHBOARD AMERICAN · RESEARCH UPDATE · 23 OCTOBER 2026</p>
<h1>What can we actually measure?</h1>
<p class="lead">The $75bn national result remains a conditional benchmark. We now have a reproducible regional tariff calculation and a reviewed set of project-cost matches. Neither establishes a measured national cost per new data-center MW.</p>
<nav><a href="index.html">Calculator</a><a href="baaja-one-pager.pdf">One-page brief</a><a href="https://github.com/dashboardamerican/baaja-and-pricing">Code &amp; data</a></nav>
<h2>1. Start with inventories, then match records</h2>'''
body+=table(['Source','Records reviewed','What the review established'],[
 ('PJM project export','15,838 upgrade records','816 recent Customer Service candidates; only 3 explicit data-center keyword records. Customer Service is not a DC classification.'),
 ('MISO MTEP25 Appendix A','432 projects','99 Load Growth projects; 4 explicitly identify data centers, and 3 of those disclose MW in the description.'),
 ('MISO MTEP26 expedited reviews','27 PDFs; 90 unique project cost cards','11 manually reviewed load packages / 5,011 MW joined to cost and corrective-action records. Four packages have computational-load identification.')])
body+='''<p>The MISO monthly reports disclose more load information than the summary workbook. Project IDs allow connection work and additional corrective-action plans (CAPs) to be joined. Temporary connections and permanent phases must share a reconciled demand denominator.</p>
<p><a href="data/evidence/inventory-audit.json">Inventory audit</a> · <a href="data/evidence/pjm-customer-service-screen.csv">PJM screening inventory</a> · <a href="data/evidence/miso25-load-growth.csv">MISO25 load-growth inventory</a> · <a href="data/evidence/miso26-cost-cards.json">MISO26 cost-card facts and locators</a></p>
<h2>2. Documented packages vary sharply</h2>'''
body+=table(['Reviewed case','Requested MW','Documented package, $m','Package $m/MW'],[(x['case'],f"{float(x['MW']):,.0f}",f"{float(x['documented_package_cost_high_USD'])/1e6:,.2f}",f"{float(x['package_USD_per_MW_high'])/1e6:.3f}") for x in packages])
body+='''<p><b>These are estimated study packages, not net newly assignable capital.</b> Some use substantial existing infrastructure. Some omit customer-owned equipment, earlier phases, or acceleration costs for shared projects. Seven cases have an unverified large-load type rather than a demonstrated data-center identity. The $0.235m/MW weighted sample intensity is descriptive, not a national calibration. All cases are in the public MISO record; selection is not random.</p>
<p>Hannover includes its additional $1m CAP. Cannoli is identified as a data center by the <a href="https://www.waynecountymi.gov/News/Commission/Wayne-County-Commission-Van-Buren-%E2%80%9CProject-Cannoli%E2%80%9D-Data-Center-Statement">Wayne County Commission</a>; MISO itself describes an industrial customer. Cannoli includes a $0.5m CAP with an existing-system need, so its attributable share is retained as a range. Mogul and Prairie Link are grouped so the shared CAP is counted once; Prairie Link's temporary 300 MW connection is not added again to its ultimate 1,000 MW.</p>
<p><b>Excluded high-cost case:</b> West Fork Creek and associated lines total $3.48bn. The September load table reports 4,500 MW, while the project card reports 1.0 MW. The discrepancy is visible in the original PDF, not an extraction error. We retain the conflict and exclude the case from the sample mean. At 4,500 MW the package intensity would be $0.773m/MW, showing why its exclusion matters.</p>
<p><a href="data/evidence/miso26-matched-packages.csv">Matched packages, IDs and source pages</a> · <a href="data/evidence/matched-sample-audit.json">Selection, exclusions and scope notes</a>. Source: <a href="https://www.misoenergy.org/planning/transmission-planning/mtep/">MISO planning reports</a>, including the <a href="https://cdn.misoenergy.org/MTEP26%20-%20Draft784746.zip">MTEP26 draft archive</a>.</p>
<h2>3. Replace an unweighted rate guess with observed regional weights</h2>'''
ra=a['pjm_rates']
body+=table(['PJM weighting','NITS $/kW-year'],[
 ('2026 published network-service peak load',f"{ra['NSPL_weighted_NITS_USD_per_kW_year']:.1f}"),
 ('Positive net new large-load forecast, 2026–2030',f"{ra['demand_growth_weighted_NITS_USD_per_kW_year']['2030']['rate']:.1f}"),
 ('Positive net new large-load forecast, 2026–2035',f"{ra['demand_growth_weighted_NITS_USD_per_kW_year']['2035']['rate']:.1f}")])
body+='''<p>The $94.7 new-load-weighted result is close to the dashboard's $95.1 national proxy. That is a PJM cross-check, not proof of a national average. Published zonal NITS excludes separate service-specific charges; Dominion's underground rider is kept separate. Forecast adjustments mostly concern data centers but also include other changes. They are not signed billing commitments.</p>
<p>Sources: <a href="https://www.pjm.com/-/media/DotCom/markets-ops/settlements/network-integration-trans-service-august-2026-xls.xlsx">August 2026 tariff schedule</a>, <a href="https://www.pjm.com/-/media/DotCom/markets-ops/settlements/network-service-peak-loads-2026.pdf">2026 NSPL</a>, and <a href="https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/2026-load-report-tables.xlsx">load forecast Table B9b</a>. <a href="data/evidence/pjm-zonal-rates-and-load.csv">Joined zonal data</a>.</p>
<h2>4. Regional billing pools change the answer</h2>
<p>Hold the capital assumption at $0.65m/MW and effective coverage at 75%. Use published PJM load paths through 2046, then a selected 1.5% annual increase in the new-load stock through 2056. Hold inherited pools and rates flat in real terms. These are conditional large-load scenarios, not forecasts of DC-only BAAJA receipts.</p>'''
body+=table(['2027–2056 cumulative, 2026$bn','Separate PJM zones','One pooled PJM calculation'],[
 ('Additional versus embedded',f"{regional['A_embedded']:.1f}",f"{pooled['A_embedded']:.1f}"),
 ('Additional versus higher-of',f"{regional['A_higher_of']:.1f}",f"{pooled['A_higher_of']:.1f}"),
 ('Above incremental cost',f"{regional['B']:.1f}",f"{pooled['B']:.1f}")])
body+=f'''<p>Pooling overstates the embedded-baseline uplift by <b>{(pooled['A_embedded']/regional['A_embedded']-1)*100:.0f}%</b> in this scenario. It changes billing shares and obscures regional higher-of thresholds. This percentage is not a measured correction to the national result.</p>
<h2>5. Existing obligations are part of the counterfactual</h2>
<p>No tariff named AND does not mean all incremental infrastructure payments would be new. AEP reports SB Energy's commitment to fund $4.2bn of Piketon transmission. Wisconsin's PSC identifies $1.099bn of Oracle-funded E-STATCOM equipment. Entergy's SEC filing describes incremental-cost recovery from Meta through contributions in aid of construction, advance payments and minimum bills. These arrangements require project-specific reconciliation before estimating additional policy receipts.</p>
<p><a href="data/evidence/existing-obligations.json">Evidence and source links</a>. These examples do not establish a national prior-recovery share, and bundled utility savings claims cannot be deducted dollar-for-dollar from a transmission estimate.</p>
<h2>6. What remains conditional in the national result</h2>
<p>Keep Medium demand, 80% load factor, 75% coverage, no prior-payment offset, a single national billing pool and the 7.33% levelized annual cost factor. Only change capital:</p>'''
body+=table(['Capital, $m/MW','Additional vs embedded, $bn','Additional vs higher-of, $bn'],[(f"{x['capital_million_per_MW']:.2f}",f"{x['summary_billion_2026_USD']['A_embedded']:.1f}",f"{x['summary_billion_2026_USD']['A_higher_of']:.1f}") for x in medium])
body+='''<p>This range is a sensitivity, not a confidence interval. The evidence does not yet identify how to weight these national capital scenarios. The $0.65m/MW default is retained as an illustrative benchmark; the convenience sample mean is not substituted for it.</p>'''
body+=table(['Other Medium-case sensitivity','Additional $bn'],[
 ('No additional prior recovery','74.6'),('25% of uplift already collected beyond embedded charges','55.9'),('50% already collected','37.3'),
 ('Synthetic nominal rate-base recovery profile, no prior offset','84.6')])
body+='''<p>The prior-payment percentages are selected assumptions. The 75% coverage factor means participation in this modeled grid: the remaining demand is excluded from both investment and billing shares. It does not model an exemption for customers still using the grid. The alternative recovery profile uses 40-year straight-line depreciation, 50% equity, 10% nominal ROE, 5% debt, 21% federal tax, 1.5% real O&amp;M and 2.5% inflation; it omits ADIT and state taxes. It demonstrates timing sensitivity rather than reproducing an approved utility formula rate. The national growth paths after 2030 remain extrapolations, and eligibility, site exits, load response, future tariff changes and attribution are unresolved.</p>
<h2>7. Correct the comparator and preserve the distinction between the two outputs</h2>
<p>For inherited requirement <code>B0</code>, annual incremental cost <code>I</code> and new-load billing share <code>s</code>:</p>
<pre>Embedded payment = s × (B0 + I)
Higher-of payment = max[embedded payment, I]
Credited AND payment = s × B0 + I
Additional vs embedded = (1 − s) × I
Additional vs higher-of = min[(1 − s) × I, s × B0]
Above incremental cost = s × B0</pre>
<p>Both cases collect the same total grid requirement. Additional receipts equal other-customer bill relief under full crediting. Above-incremental payments and additional payments overlap; do not add them. With embedded pricing, additional receipts can exceed the amount above incremental cost because the baseline may shift some incremental cost to others. The calculator now defaults to embedded and retains higher-of under Details.</p>
<p>For policy scale, compare additional receipts to the ITC illustration. JCT's historical official score is $11.279bn nominal over FY2022–2031. Repeating its normalized ten-year profile gives $31.7bn over 30 years; retaining the initial profile then holding its final annual level for 20 more years gives about $53.4bn. Both are analyst extrapolations, not official 30-year scores or estimates of guaranteed ratepayer savings. Private bill transfers are not federal budget offsets.</p>
<h2>Audit trail</h2>
<p><a href="data/evidence/regional-model-results.json">Full annual results and sensitivities</a> · <a href="data/evidence/source-manifest.json">Source URLs and SHA-256 hashes</a> · <a href="https://github.com/dashboardamerican/baaja-and-pricing/tree/main/analysis">Reproduction scripts</a>.</p>
<p>The raw source archives are retained locally. Inventory and project-data extracts are provided separately. Checks cover payment conservation, customer-bill transfers, zero-cost boundaries, prior-recovery scaling, comparator distinctions and pooling effects. No power-flow model has been calibrated to an actual utility network; the financial analysis does not prove which upgrades are necessary.</p>'''
style='''body{margin:0;background:#f6f4ee;color:#1f2733;font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}main{max-width:1000px;margin:auto;padding:42px 35px 60px}h1,h2{font-family:Georgia,serif;color:#16284a}h1{font-size:38px;line-height:1.2;margin:12px 0 20px}h2{font-size:25px;margin:38px 0 15px}.eyebrow{font-size:11px;letter-spacing:1px;color:#4a5563}.lead{font-size:19px}nav{display:flex;gap:24px;border-bottom:2px solid #16284a;padding:15px 0 24px}a{color:#16284a;text-underline-offset:3px}.table{overflow:auto}table{width:100%;border-collapse:collapse;font-size:13px;background:white}th,td{padding:11px 12px;text-align:left;vertical-align:top;border-bottom:1px solid #ddd7c9}th{background:#16284a;color:white;font-weight:500}pre{white-space:pre-wrap;background:#efece3;padding:18px;font-size:13px}code{font-size:13px}@media(max-width:650px){main{padding:24px 18px}h1{font-size:30px}h2{font-size:23px}nav{gap:18px;font-size:13px}}@media print{body{background:white}main{max-width:none;padding:0}nav{display:none}h2{break-after:avoid}tr{break-inside:avoid}a{color:inherit}}'''
(ROOT/'evidence.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>BAAJA · Regional evidence and model audit</title><style>'+style+'</style></head><body><main>'+body+'</main></body></html>')
print(ROOT/'evidence.html')
