"""Extract individual cost cards from the complete MTEP26 EPR archive.
No inferred costs, no assumed load where the source omits MW.
"""
from pathlib import Path
from pypdf import PdfReader
import re,json,csv
ROOT=Path(__file__).resolve().parents[1];folder=ROOT/'research/2026-10-23/miso26';out=ROOT/'data/evidence'
cards=[]
for pdf in sorted(folder.glob('*.pdf')):
 if 'Statistics' in pdf.name:continue
 for page,p in enumerate(PdfReader(pdf).pages,1):
  t=p.extract_text() or '';id=re.search(r'Project\s*#\s*(\d{5})\b',t)
  if not id:continue
  price=re.search(r'Current Cost\s*\$\s*([\d,.]+)\s*([MB])\b',t,re.I)
  name=re.search(r'Project Name\s+(.*?)\s+Project Type',t,re.S)
  cap=re.search(r'Spot Load Value\s*\(MW\)\s*([\d,.]+)',t,re.I)
  cards.append({'project_id':id[1],'document':pdf.name,'document_date':pdf.name[:8],'pdf_page':page,
    'project_name':' '.join(name[1].split()) if name else None,
    'cost_USD':float(price[1].replace(',',''))*(1e9 if price[2].upper()=='B' else 1e6) if price else None,
    'reported_spot_load_MW':float(cap[1].replace(',','')) if cap else None,
    'CAP_parent_context':' '.join(t.split('Project #')[0].split()) if 'Corrective Action' in t else '',
    'excerpt':t})
latest={}
for c in cards: latest[c['project_id']]=c
(out/'miso26-cost-cards.json').write_text(json.dumps({'source_archive':'https://cdn.misoenergy.org/MTEP26%20-%20Draft784746.zip',
 'card_count':len(cards),'unique_project_count':len(latest),'latest_cards':[{k:v for k,v in c.items() if k!='excerpt'} for c in latest.values()],
 'limitations':['Latest available individual card may differ from the draft portfolio cost table.',
 'CAP parents need manual review; costs are not necessarily all attributable to a single load.',
 'MW omissions and conflicting reported MW are preserved, not filled with zero.']},indent=2)+'\n')
print('Cards',len(cards),'unique projects',len(latest),'with parsed costs',sum(c['cost_USD'] is not None for c in latest.values()))
for id in ['51219','51293','51404','51220','18201','51366','51299','51298','51259','51416','51304','51313','50798','50805','50809','51405','51406','51262','51263','51264']:
 c=latest.get(id)
 print(id,{k:c[k] for k in ('project_name','cost_USD','reported_spot_load_MW','document','pdf_page')} if c else None)
