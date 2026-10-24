"""Render the one-page PDF from the verified central-case data. Requires reportlab."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/central-case.json').read_text())
A=DATA['BAAJA']['metrics']['A_extra_AND_vs_baseline_usd']['constant_2026_billion']
B=DATA['BAAJA']['metrics']['B_above_incremental_transmission_cost_usd']['constant_2026_billion']
ITC=DATA['ITC']['repeated_30yr_constant_2026_billion']
GROWTH=json.loads((ROOT/'data/growth-scenarios.json').read_text())
W,H=612,792
PAPER='#F6F4EE'; INK='#16284A'; MUTED='#4A5563'; TEAL='#16284A'; GOLD='#8A6D1F'; LINE='#DDD7C9'
c=canvas.Canvas(str(ROOT/'baaja-one-pager.pdf'),pagesize=(W,H))
c.setTitle('BAAJA AND Pricing | Thirty-Year Central Case')
c.setAuthor('Dashboard American')
c.setFillColor(HexColor(PAPER));c.rect(0,0,W,H,fill=1,stroke=0)

def txt(x,y,text,size=10,font='Helvetica',color=INK):
    c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,y,text)

def para(text,x,y,width=528,size=9.1,color=INK,leading=13):
    style=ParagraphStyle('body',fontName='Helvetica',fontSize=size,leading=leading,textColor=HexColor(color),spaceAfter=0)
    p=Paragraph(text,style);_,height=p.wrap(width,1000);p.drawOn(c,x,y-height);return y-height

def rule(y):
    c.setStrokeColor(HexColor(LINE));c.setLineWidth(.6);c.line(42,y,570,y)

txt(42,753,'DASHBOARD AMERICAN / BAAJA',8,'Helvetica-Bold',TEAL)
txt(42,716,'Who pays for the grid?',30,'Times-Roman')
para('A 30-year estimate of data-center transmission payments under AND pricing',42,699,size=10.5,color=MUTED)

# Two distinct measures. Metric B includes, rather than adds to, metric A.
for x,amount,label,title,body,dark in [
    (42,A,'A / ADDITIONAL PAYMENTS','Conditional additional payments','Above the embedded-price baseline; matched by lower bills for other customers.',True),
    (312,B,'B / ABOVE INCREMENTAL COST','Total inherited-grid contribution','Above incremental transmission cost; includes payments already made under the baseline.',False)]:
    c.setFillColor(HexColor(TEAL if dark else '#FFFEFA'));c.setStrokeColor(HexColor(TEAL if dark else LINE));c.roundRect(x,510,258,160,9,fill=1,stroke=1)
    col='#FFFFFF' if dark else INK
    txt(x+17,647,label,7.5,'Helvetica-Bold',col)
    txt(x+17,626,title,10,'Helvetica',col)
    txt(x+17,575,f'${amount:.0f}bn',39,'Times-Roman',col)
    para(body,x+17,551,224,8.6,'#D3EBE3' if dark else MUTED,12)
para('<b>2027-2056, constant 2026 dollars, undiscounted.</b> In this central case, A is part of B; do not add them. B excludes modeled incremental transmission cost; it is not an overcharge above fully allocated cost of service.',42,497,size=8.6,color=MUTED,leading=12)

txt(42,451,'Low / Medium / High demand paths',15,'Times-Roman')
txt(42,432,'U.S. facility TWh/year',8.5,'Helvetica-Bold')
for x,k in [(294,'low'),(390,'medium'),(486,'high')]:
    txt(x,432,k.capitalize(),8.5,'Helvetica-Bold')
for y,year in [(415,2030),(399,2035),(383,2056)]:
    txt(42,y,f'{year}'+(' (EPRI)' if year==2030 else ' (extrapolated)'),8.4)
    for x,k in [(294,'low'),(390,'medium'),(486,'high')]:
        txt(x,y,f"{GROWTH['scenarios'][k]['annual_twh'][str(year)]:,.0f}",8.8,'Helvetica')
para('After 2030, transfer IEA global scenario growth rates through 2035; taper to selected 0.5% / 1.5% / 2.5% annual growth by 2040, then hold to 2056. These are our U.S. extrapolations, not published long-run forecasts. Medium is the default.',42,372,size=7.8,color=MUTED,leading=10.3)
txt(42,334,'Central: $0.65m/MW capital; $95.1/kW-year NITS proxy; 80% load factor.',8.7,'Helvetica-Bold')
rule(329)

txt(42,306,'A comparable policy scale',17,'Times-Roman')
mx=max(A,ITC)
for y,label,value,col in [(279,'BAAJA additional payments',A,TEAL),(247,'Transmission ITC illustration',ITC,GOLD)]:
    txt(42,y+2,label,8.7)
    c.setFillColor(HexColor(LINE));c.roundRect(222,y-3,260,15,2,fill=1,stroke=0)
    c.setFillColor(HexColor(col));c.roundRect(222,y-3,260*value/mx,15,2,fill=1,stroke=0)
    txt(494,y+1,f'${value:.0f}bn',11,'Helvetica-Bold')
para(f'<b>About {A/ITC:.1f} times the ITC illustration.</b> JCT officially scored BBB\'s transmission ITC at <b>$11.279bn over FY2022-2031</b>. For a common 30-year comparison, we normalize its annual cash flows to 2026 dollars at an assumed 2.5% inflation rate and repeat that real ten-year profile three times: <b>${ITC:.1f}bn</b>. This is our repeated-program illustration, not an official 30-year score or the 30-year benefit of a single ten-year credit. BAAJA transfers private bills; the ITC costs the federal budget and does not guarantee equivalent bill savings.',42,220,size=8.5,leading=12)

rule(134)
para('<b>Mechanism and limits.</b> AND collects the full annual cost of attributable upgrades plus a contribution to the inherited grid. Incremental receipts are credited out of the shared revenue requirement. Fixed: 75% modeled-grid participation; an 829 GW planning-peak proxy for the incumbent pool; charges from 2030, including prospective charges on 2027-2029 entrants; 40-year assets, 5% real financing and 1.5% O&amp;M. Other demand excluded from costs and billing. No prior-payment offset. Growth, cost, coverage and national pooling are assumptions. PUDL v2026.10.0 was reviewed; it does not establish a matched national NITS rate or DC-attributable capital per MW.',42,122,size=7.5,color=MUTED,leading=10.3)

source='Sources: EPRI Powering Intelligence 2026, Figure5; IEA Key Questions on Energy and AI, TableA.1; BAAJA draft s.2107(a); JCT JCX-46-21 p.2; EIA AEO2026 Table54; Grid Strategies Nov2025 p.33. Full source links and calculations accompany the dashboard.'
para(source,42,56,size=7.1,color=MUTED,leading=9.3)
txt(42,21,'dashboardamerican.github.io/baaja-and-pricing/',7.5,'Helvetica-Bold',TEAL)
c.linkURL('https://dashboardamerican.github.io/baaja-and-pricing/',(42,17,320,30),relative=0,thickness=0)
txt(501,21,'24 OCT 2026',7.2,'Helvetica',MUTED)
c.showPage();c.save()
print(ROOT/'baaja-one-pager.pdf')
