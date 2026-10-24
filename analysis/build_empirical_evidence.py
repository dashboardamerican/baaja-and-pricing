"""Audit public project inventories and match PJM tariffs to published demand.

Uses archived raw files in research/2026-10-23/; never treats missing load data
as zero and never treats Customer Service or Load Growth as synonymous with DC.
Raw snapshots are local; source-manifest.json records URLs and SHA-256 hashes.
"""
from pathlib import Path
from openpyxl import load_workbook
from pypdf import PdfReader
import collections,csv,json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'research/2026-10-23/raw'
EXTRACT=ROOT/'research/2026-10-23/extracted'
OUT=ROOT/'data/evidence';OUT.mkdir(exist_ok=True)

def dump(name,value): (OUT/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def csvwrite(name,rows):
 with (OUT/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

# Full PJM published inventory. Cost values are millions of dollars.
pjm=[{x.tag:(x.text or '').strip() for x in e} for e in ET.parse(RAW/'pjm-projects.xml').getroot()]
assert len(pjm)==15838,'Snapshot changed: update and audit source manifest.'
explicit=[r for r in pjm if re.search(r'data\s*cent',r.get('Description','')+' '+r.get('Driver',''),re.I)]
# Do not sum parent and child project costs or call Customer Service a DC flag.
recent=[r for r in pjm if 'Customer Service' in r.get('Driver','') and
 any(r.get(k,'').endswith(('2024','2025','2026')) for k in ('InitialTEACDate','PJMBoardApprovalDate'))]
fields=['UpgradeId','ProjectType','Description','Driver','TransmissionOwner','State','Status','CostEstimate','InitialTEACDate','PJMBoardApprovalDate','ActualInServiceDate','ProjectedInServiceDate','LastUpdated']
csvwrite('pjm-customer-service-screen.csv',[{k:r.get(k,'') for k in fields} for r in recent])
csvwrite('pjm-explicit-dc-records.csv',[{k:r.get(k,'') for k in fields} for r in explicit])
pjm_audit={'inventory_records':len(pjm),'project_type_counts':dict(collections.Counter(r['ProjectType'] for r in pjm)),
 'explicit_dc_keyword_records':len(explicit),'recent_customer_service_candidates':len(recent),
 'recent_definition':'Customer Service in Driver; InitialTEACDate or PJMBoardApprovalDate in 2024-2026. Includes all statuses. Not all DCs; may contain related project components.',
 'limitations':['No complete DC attribution flag or paired customer MW field in this export.',
 'Keyword absence does not mean a project is unrelated to data centers.',
 'Parent/child upgrades, cancellations, vintage, mixed drivers and upstream project scope must be reconciled before summing attributable costs.']}

# MISO 2025 full Appendix A workbook, not a selected set of announcements.
wb=load_workbook(EXTRACT/'MTEP25 Appendix A - New Local Reliability Projects.xlsx',read_only=True,data_only=True)
vals=list(wb['MTEP25 Appendix A'].values);headers=vals[1]
miso=[dict(zip(headers,r)) for r in vals[2:] if r[1]]
assert len(miso)==432
load=[r for r in miso if r['Other Type']=='Load Growth']
csvwrite('miso25-load-growth.csv',load)
dc=[r for r in load if re.search(r'data\s*cent',r['Project Description'] or '',re.I)]
paired=[r for r in dc if re.search(r'\b\d[\d,.]*\s*MW\b',r['Project Description'],re.I)]
miso_audit={'inventory_projects':len(miso),'portfolio_cost_usd':sum(r['Current Cost'] or 0 for r in miso),
 'load_growth_projects':len(load),'load_growth_project_cost_usd':sum(r['Current Cost'] or 0 for r in load),
 'explicit_dc_projects':len(dc),'explicit_dc_with_MW_projects':len(paired),
 'limitations':['Load Growth includes ordinary load growth, industrial loads and distribution-related work.',
 'Many customer identities and MW are not disclosed in project descriptions.',
 'Individual connection-project estimates do not establish the complete attributable upstream network cost or net customer-funded amount.']}
# Three explicit DC/MW records plus associated LEAP second phase. Partial packages only.
byid={str(r['MTEP Project ID']):r for r in miso}
matches=[]
for label,ids,mw,scope in [
 ('Merom',['50599'],620,'One-mile transmission connection; broader upstream upgrades and customer-owned facilities not established.'),
 ('Marble Hill',['50614'],310,'Ring-bus station; customer builds an adjacent station. Complete upstream cost not established.'),
 ('LEAP initial phase',['50208'],600,'Published network package for initial 600 MW; not proof of all system-wide upgrades.'),
 ('LEAP two-phase package',['50208','50628'],1200,'Initial 600 MW plus explicit additional 600 MW. Replaces, and must not be added to, the initial-phase row.')]:
 cost=sum(byid[i]['Current Cost'] for i in ids)
 matches.append({'case':label,'project_ids':';'.join(ids),'load_MW':mw,'reported_cost_usd':cost,'reported_component_cost_per_MW':cost/mw,
  'status':'Partial documented package, not a complete or net newly-assignable cost estimate.','scope':scope,
  'source':'MTEP25 Appendix A - New Local Reliability Projects.xlsx; MTEP25 Report ZIP'})
csvwrite('miso25-matched-components.csv',matches)

# Actual PJM zonal NITS rates; preserve published DOM underground rider separately.
s=load_workbook(RAW/'pjm-nits-august-2026.xlsx',read_only=True,data_only=True).active
rates={};zone=None
for n,r in enumerate(s.values,1):
 if n<3 or n>59:continue
 if r[0]:zone=str(r[0]).strip().upper()
 if isinstance(r[4],(int,float)):
  if n==29:continue # DOM underground rider is not a universal zonal charge.
  rates[zone]=float(r[4])
# Read published NSPL table, not total demand from mismatched planning data.
text=PdfReader(RAW/'pjm-nspl-2026.pdf').pages[0].extract_text()
peaks={}
for line in text.splitlines():
 m=re.match(r'^(AECO|AEP|APS|ATSI|BGE|COMED|DAY|DEOK|DOM|DPL|DUQ|EKPC|JCPL|METED|OVEC|PECO|PENELEC|PEPCO|PPL|PSEG|RECO)\s+.*?([\d,]+\.\d)\s+\d+/\d+/2025\b',line)
 if m:peaks[m[1]]=float(m[2].replace(',',''))
assert len(peaks)==21,peaks
rates['METED']=rates.pop('ME')
assert set(rates)==set(peaks),(set(rates)-set(peaks),set(peaks)-set(rates))
forecast=load_workbook(RAW/'pjm-load-2026.xlsx',read_only=True,data_only=True)
b9b=list(forecast['Table B9b'].values);years=b9b[6][1:]
lookup={'AE':'AECO','PL':'PPL','PS':'PSEG','DAYTON':'DAY','DLCO':'DUQ','PENLC':'PENELEC'}
paths={}
for r in b9b[7:]:
 k=lookup.get(r[0],r[0])
 if k in peaks:paths[k]={int(y):float(v or 0) for y,v in zip(years,r[1:])}
assert set(paths)==set(peaks)
annualFactor=.05/(1-1.05**-40)+.015
zonal=[]
for k in peaks:
 zonal.append({'zone':k,'NITS_USD_per_MW_year':rates[k],'NSPL_2026_MW':peaks[k],
 'break_even_capital_USD_per_MW_at_model_factor':rates[k]/annualFactor,
 'large_load_B9b_2026_MW':paths[k][2026],
 'positive_net_large_load_2030_MW':max(0,paths[k][2030]-paths[k][2026]),
 'positive_net_large_load_2035_MW':max(0,paths[k][2035]-paths[k][2026]),
 'positive_net_large_load_2046_MW':max(0,paths[k][2046]-paths[k][2026])})
csvwrite('pjm-zonal-rates-and-load.csv',zonal)
rate_audit={'NSPL_weighted_NITS_USD_per_kW_year':sum(rates[k]*peaks[k] for k in peaks)/sum(peaks.values())/1000,
 'NSPL_total_GW':sum(peaks.values())/1000,
 'demand_growth_weighted_NITS_USD_per_kW_year':{},
 'DOM_underground_rider_USD_per_MW_year':518.27,
 'sources':{'rates':'https://www.pjm.com/-/media/DotCom/markets-ops/settlements/network-integration-trans-service-august-2026-xls.xlsx',
 'peaks':'https://www.pjm.com/-/media/DotCom/markets-ops/settlements/network-service-peak-loads-2026.pdf',
 'load':'https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/2026-load-report-tables.xlsx'},
 'limitations':['PJM-only; not a national rate.',
 'Published zonal NITS rates exclude separately billed regional/service-specific charges; DOM underground rider kept separate.',
 'ME/PENELEC share published MAIT rate; their NSPLs are kept separate; UGI load is within PPL and is not counted twice.',
 'Table B9b includes total loads associated with adjustments, not only the adjustment above statistical embedded trends. Net increases from 2026 are used.',
 'Large-load adjustments are mostly data centers but include other adjustments. Forecast MW is not a signed billing commitment or an observed 1CP customer peak.',
 'Published 2026 NSPL is metered demand at each zone peak in November 2024-October 2025; using it as a fixed incumbent pool is a modeling assumption.']}
for year in (2030,2035,2046):
 q={k:max(0,paths[k][year]-paths[k][2026]) for k in peaks}
 rate_audit['demand_growth_weighted_NITS_USD_per_kW_year'][str(year)]={'rate':sum(q[k]*rates[k] for k in peaks)/sum(q.values())/1000,'new_load_GW':sum(q.values())/1000}
# Save source paths for regional modeling with honest scope labels.
dump('pjm-regional-inputs.json',{'status':'Observed tariff/NSPL inputs plus published large-load forecast; no measured DC-attributable cost per MW.',
 'rates_USD_per_MW_year':rates,'incumbent_MW':peaks,'large_load_forecast_B9b_MW':paths,'rate_audit':rate_audit})
dump('inventory-audit.json',{'as_of':'2026-10-23','pjm':pjm_audit,'miso25':miso_audit,'pjm_rates':rate_audit})
manifest=json.loads((ROOT/'research/2026-10-23/source-manifest.json').read_text());dump('source-manifest.json',manifest)
print(json.dumps({'pjm':pjm_audit,'miso25':miso_audit,'rates':rate_audit},indent=2))
