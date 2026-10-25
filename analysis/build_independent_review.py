"""Publish checked findings and corrections from the authorized Claude review."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'data/evidence/claude-review-crosschecks.json').read_text())
c=d['central']
style='''body{margin:0;background:#f6f4ee;color:#1f2733;font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}main{max-width:1000px;margin:auto;padding:42px 35px 60px}h1,h2{font-family:Georgia,serif;color:#16284a}h1{font-size:38px;line-height:1.2}h2{font-size:25px;margin:35px 0 12px}.lead{font-size:19px}.eyebrow{font-size:11px;letter-spacing:1px}a{color:#16284a;text-underline-offset:3px}nav{display:flex;gap:24px;padding:15px 0 24px;border-bottom:2px solid #16284a}.table{overflow:auto}table{width:100%;border-collapse:collapse;background:white;font-size:13px}th,td{padding:11px 12px;text-align:left;vertical-align:top;border-bottom:1px solid #ddd7c9}th{background:#16284a;color:white;font-weight:500}@media(max-width:650px){main{padding:24px 18px}h1{font-size:30px}nav{gap:15px;font-size:13px}}'''
def table(headers,rows):
    return '<div class="table"><table><thead><tr>'+''.join('<th>'+html.escape(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
body='''<p class="eyebrow">DASHBOARD AMERICAN · INDEPENDENT REVIEW · 25 OCTOBER 2026</p><h1>Claude review: sound arithmetic, unresolved score</h1>
<p class="lead">Claude Opus 5.5, at high effort, independently reviewed the prepared public model and paper packet. It reproduced the arithmetic and found that the national estimate remains driven by unmeasured assumptions. Codex checked the numerical claims and challenged overstatements; Claude accepted the corrections in a separate follow-up.</p>
<nav><a href="index.html">Calculator</a><a href="literature-review.html">Paper review</a><a href="evidence.html">Project evidence</a></nav>
<h2>What the central case actually implies</h2>
<p>These are cumulative 2027-2056 payments in constant 2026 dollars, with charges from 2030. They retain the selected $0.65m/MW capital assumption, levelized real carrying charge, growth path, modeled-grid participation and zero offset for existing recovery.</p>'''
body+=table(['Central-case quantity','2026$bn'],[
    ('Modeled incremental transmission cost','80.5'),
    ('Data-center payments under embedded pricing','154.9'),
    ('Embedded payments above incremental cost',f"{c['baseline_above_incremental_billion']:.1f}"),
    ('Data-center payments under credited AND pricing','229.5'),
    ('Additional payments caused by AND pricing',f"{c['A_billion']:.1f}"),
    ('AND payments above incremental cost',f"{c['B_billion']:.1f}")])
body+='''<p><b>Under these assumptions, ordinary pricing already produces a positive contribution to the shared grid.</b> AND pricing adds to it. The model therefore does not show that the typical data center currently underpays incremental cost. Nor does that conditional aggregate result establish that every real project covers its costs. Contributions to the existing grid are not proof of an overcharge above fully allocated cost of service.</p>
<h2>Capital and timing drive the answer</h2>'''
body+=f'''<p>At central demand and the embedded comparator, each additional <b>$0.10m/MW</b> of assigned capital adds about <b>${c['A_change_per_100000_USD_per_MW_billion']:.1f}bn</b> of policy receipts. That is a model slope, not evidence about actual capital. At the selected $95.1/kW-year rate, ordinary embedded pricing stops covering modeled incremental cost at roughly <b>${c['capital_threshold_USD_per_MW']/1e6:.2f}m/MW</b>. This threshold assumes the levelized recovery profile; regional rates and front-loaded formula rates differ.</p>
<p>Changing eligibility can matter more than merely delaying the charge. The following scenarios retain the physical investment and billing demand of grandfathered entrants; they are not removed from the grid:</p>'''
body+=table(['Charges begin','Entrants eligible from','Net additional DC payments / relief to 2026 incumbents, $bn'],[
    (r['charges_begin'],r['first_eligible_entry_year'],f"{r['net_all_DC_extra_equals_2026_incumbent_relief_billion']:.1f}") for r in d['scope_cases']])
body+='''<p>Excluding 2027-2029 entrants gives $48.7bn rather than $74.6bn. Eligible entrants' gross increase is $50.0bn, while grandfathered data centers receive $1.3bn of shared-rate credits, leaving $48.7bn of net additional payments by all modeled data centers. These are implementation sensitivities, not a confidence interval or a finding that section2107(a) requires grandfathering. The explicit prospective-application clause in the draft appears in new FPA section228, introduced by section2107(b).</p>'''
body+=f'''<p>The central <b>${c['A_billion']:.1f}bn</b> undiscounted total has a <b>${c['A_PV_2026_at_3pct_real_billion']:.1f}bn present value</b> at an assumed 3% real discount rate to 2026. Neither is more “actual”: one is cumulative purchasing power and the other discounts later transfers. They must not be compared on mixed bases.</p>
<h2>Findings accepted after source and calculation checks</h2>
<p>The review reinforces the need to measure newly assignable capital, actual jurisdiction and service eligibility, existing additional recovery, nonfirm service and retail pass-through. A nationally calibrated BAAJA score does not emerge from confirming the equations. Section2107(a) and new section228 can reach the same transmission-cost dollars, so estimates for those provisions must not be added without an overlap ledger.</p>
<p>Prior recovery needs a cash-flow ledger. A TSA or minimum bill that only guarantees the embedded revenue already assumed by the model does not automatically reduce the policy uplift when the load materializes. CIAC, refundable advances, actual minimum-bill top-ups and contingent exit charges need separate treatment. Funding already deducted from the capital input must not be deducted a second time.</p>
<h2>Corrections to Claude's first pass</h2>'''
body+=table(['First-pass claim','Checked resolution, accepted by Claude'],[
    ('Host-zone and pooled runs bracket actual allocation','Withdrawn. A two-zone counterexample produces additional receipts above the pooled result. Actual Schedule12 allocations are required.'),
    ('Pool size is immaterial','Withdrawn. A depends on pool size; only the inherited NITS rate cancels under the specified embedded comparator.'),
    ('Section228 is effectively mandatory AND pricing','Qualified. It sets an incremental-cost floor and permits surplus recovery; this differs from the separate additive transmission requirement in2107(a).'),
    ('75% likely overstates legal coverage','Qualified. No direction of bias is established. The current 75% is a selected modeled-grid participation assumption, not a jurisdiction estimate.'),
    ('Grandfathering follows automatically for2107(a)','Qualified. It is an implementation scenario; the express prospective clause is in new228.'),
    ('The $84.6bn rate-base sensitivity was unpublished','Withdrawn. The existing evidence report already published it; the review packet omitted that report.'),
    ('Replace prior recovery with a CIAC-only parameter','Qualified. A mechanism-specific cash-flow ledger is broader and avoids double counting.')])
body+='''<p>The transmission-ITC bars remain an explicitly conditional scale comparison requested for this project. Repeating a historical ten-year federal budget profile is not an official 30-year score. Private bill transfers are not federal budget savings, and any combined policy model must account for the ITC lowering recoverable investment costs. The displayed ratio is arithmetic within these illustrations, not a conclusion about equivalent policy benefits.</p>
<h2>Review record</h2>
<p><a href="data/evidence/claude-review-first-pass.txt">Unrevised first-pass report—read with corrections</a> · <a href="data/evidence/claude-review-followup.txt">Claude's correction check</a> · <a href="data/evidence/claude-review-crosschecks.json">Verified calculations and counterexample</a> · <a href="data/evidence/claude-review-record.json">Review scope and provenance</a> · <a href="https://github.com/dashboardamerican/baaja-and-pricing/blob/main/analysis/review_checks.py">Reproduction script</a>.</p>
<p>The first run used read-only file tools. The follow-up used no tools and evaluated the supplied public statutory passages and explicit counterexamples. Both completed successfully with no reported permission denials. This is independent model critique, not an engineering validation, national empirical calibration, official fiscal score or legal determination.</p>'''
(ROOT/'independent-review.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>BAAJA · Independent Claude review</title><style>'+style+'</style></head><body><main>'+body+'</main></body></html>')
print(ROOT/'independent-review.html')
