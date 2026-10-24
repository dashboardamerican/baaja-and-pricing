"""Manually reviewed joins of MISO cost cards, load tables, and CAP references.
Do not interpret this nonrandom matched sample as a national capital estimate.
"""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/evidence'
cards={r['project_id']:r for r in json.loads((OUT/'miso26-cost-cards.json').read_text())['latest_cards']}
# Capacity entries are checked against the September 8 EPR statistics (PDF pages
# 3-8), with Prairie Link's ultimate 1000 MW from the July 7 cost card page 10.
cases=[
 ('Gallagher crypto','computational',150,['51207'],[],['20260908 statistics p3','20260407 cost card p13'],'Existing infrastructure; crypto explicitly identified; broader pre-existing CAP costs not quantified.'),
 ('Wishek NW','computational',50,['51219'],[],['20260908 statistics p4','20260407 cost card p11'],'Small connection to existing infrastructure; not a representative hyperscale build.'),
 ('Hannover','computational',430,['51293'],['51404'],['20260908 statistics p5','20260707 cost cards pp22-24'],'Includes additional $1m CAP, which was Appendix B rather than approved Appendix A in the source.'),
 ('Cannoli','computational_external_identification',1000,['51220'],['18201'],['20260908 statistics p4','20260707 cost cards pp18-20'],'CAP also addresses an existing MTEP19 overload; 0-100% attribution range used. DC identity independently identified by Wayne County Oct1 statement.'),
 ('Van Meter','large_load_type_unverified',300,['51216'],[],['20260908 statistics p4','20260407 cost card p14'],'Large-load benchmark; data-center use is not established by these records.'),
 ('Galet phase 2','large_load_type_unverified',250,['51238'],[],['20260908 statistics p5','20260908 cost card p14'],'Incremental phase; data-center use and earlier-phase cost not established.'),
 ('Macaw','large_load_type_unverified',200,['51299'],[],['20260908 statistics p5','20260804 cost card p7'],'Large-load benchmark; existing corrective-action plans may already support it.'),
 ('Marquette','large_load_type_unverified',116,['51298'],[],['20260908 statistics p5','20260908 cost card p23'],'Large-load benchmark; data-center use not established.'),
 ('Skyway','large_load_type_unverified',780,['51366'],[],['20260908 statistics p8','20260804 cost card p4'],'Published analysis found no new CAP projects required, but complete customer facilities and net funding not established.'),
 ('Big Cedar addition','large_load_type_unverified',370,['51259'],['51416'],['20260908 statistics p5','20260908 cost cards pp4-6'],'Adds associated MEC mitigation. Three LRTP facility dates accelerated for this load; their acceleration costs are not quantified.'),
 ('Mogul phase 3 plus Prairie Link full package','large_load_type_unverified',1365,['51303','51304','51313'],['50798','50805','50809','51405','51406'],['20260908 statistics pp6-7','20260707 cost cards pp4-16'],'365 MW Mogul + ultimate 1000 MW Prairie Link, not 365+700+300+1000. Shared Disco CAP counted once. Includes temporary connection cost but no separate duplicate temporary load.')]
rows=[]
for label,kind,mw,base,caps,sources,notes in cases:
 cost=sum(cards[k]['cost_USD'] for k in base)
 cap=sum(cards[k]['cost_USD'] for k in caps)
 # Treat all CAP costs as potentially attributable except identified pre-existing
 # Cannoli need, where an explicit 0-100% allocation sensitivity is retained.
 low=cost if label=='Cannoli' else cost+cap
 high=cost+cap
 rows.append({'case':label,'load_type_evidence':kind,'MW':mw,'project_ids':';'.join(base+caps),
  'documented_package_cost_low_USD':low,'documented_package_cost_high_USD':high,
  'package_USD_per_MW_low':low/mw,'package_USD_per_MW_high':high/mw,
  'completeness':'Documented study package, not certified full system cost or net newly-assignable cost.',
  'review_notes':notes,'capacity_and_cost_locators':'; '.join(sources),
  'identity_source_url': 'https://www.waynecountymi.gov/News/Commission/Wayne-County-Commission-Van-Buren-%E2%80%9CProject-Cannoli%E2%80%9D-Data-Center-Statement' if label=='Cannoli' else '',
  'cost_documents':'; '.join(sorted(set(cards[k]['document'] for k in base+caps)))})
# Check that no CAP or connection project has been counted in two included cases.
ids=[id for r in rows for id in r['project_ids'].split(';')]
assert len(ids)==len(set(ids)), 'Duplicate project cost across matched cases.'
with (OUT/'miso26-matched-packages.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
computational=[r for r in rows if r['load_type_evidence'].startswith('computational')]
summary={'status':'Descriptive convenience sample, not national calibration. Estimated project costs, not realized expenditures.',
 'scope':'February, April and June 2026 EPR cycles with published matching MW and reviewed cost/CAP cards. Conflicted and overlapping cases excluded.',
 'included_cases':len(rows),'included_load_MW':sum(r['MW'] for r in rows),
 'documented_package_cost_USD':sum(r['documented_package_cost_high_USD'] for r in rows),
 'sample_MW_weighted_package_USD_per_MW':sum(r['documented_package_cost_high_USD'] for r in rows)/sum(r['MW'] for r in rows),
 'computational_cases':len(computational),'computational_load_MW':sum(r['MW'] for r in computational),
 'computational_MW_weighted_package_USD_per_MW':sum(r['documented_package_cost_high_USD'] for r in computational)/sum(r['MW'] for r in computational),
 'excluded_cases':[
  {'case':'West Fork Creek / St Landry / El Dorado-Smalling','ids':['51262','51263','51264'],
   'cost_USD':sum(cards[k]['cost_USD'] for k in ['51262','51263','51264']),
   'reason':'September statistics p5 reports 4500 MW while September cost card p16 reports 1.0 MW. Visually confirmed source conflict; excluded from sample mean.',
   'conditional_USD_per_MW_if_4500_MW_is_correct':sum(cards[k]['cost_USD'] for k in ['51262','51263','51264'])/4500},
  {'case':'Truett phases and temporary connection','reason':'Temporary 500 MW request overlaps phase sequence; capacity and cost package cannot be added blindly.'},
  {'case':'Ozaukee','reason':'Changing PSC scope and dedicated customer-funded E-STATCOM; first-phase versus ultimate load denominator not matched in this sample.'}
 ],
 'limitations':['Sample favors projects with disclosed MW and separable packages; it is not random or exhaustive.',
 'Existing infrastructure, customer-owned facilities, earlier phases, acceleration of shared projects, and prior contractual payments remain incompletely measured.',
 'Reported cost vintage is 2026 study estimates with source-specific price bases; no unverified inflation harmonization applied.',
 'Do not replace the national capital slider with the sample weighted mean.']}
(OUT/'matched-sample-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
