"""Append one methodology page to the existing brief; preserve the original brief."""
from pathlib import Path
import json, html
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
OUT=BASE/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
TMP=BASE/'tmp/pdfs/fresh-central';TMP.mkdir(parents=True,exist_ok=True)
data=json.loads((ROOT/'methodology-content.json').read_text())
fonts=Path(reportlab.__file__).parent/'fonts'
pdfmetrics.registerFont(TTFont('Vera',str(fonts/'Vera.ttf')))
pdfmetrics.registerFont(TTFont('VeraBold',str(fonts/'VeraBd.ttf')))
S={
 'title':ParagraphStyle('title',fontName='VeraBold',fontSize=17,leading=21),
 'heading':ParagraphStyle('heading',fontName='VeraBold',fontSize=10,leading=12.5),
 'body':ParagraphStyle('body',fontName='Vera',fontSize=9.5,leading=12.5),
 'equation':ParagraphStyle('equation',fontName='Vera',fontSize=9,leading=12),
 'source':ParagraphStyle('source',fontName='Vera',fontSize=8.2,leading=10),
}
page=TMP/'methodology-page.pdf';c=canvas.Canvas(str(page),pagesize=(612,792));y=752;W=524
def add(text,kind,gap=4):
 global y
 p=Paragraph(text,S[kind]);_,h=p.wrap(W,800)
 if y-h<34:raise RuntimeError(f'Methodology page overflow: bottom={y-h}')
 p.drawOn(c,44,y-h);y-=h+gap
add('Methodology and full source links','title',9)
md=['# Methodology and full source links','']
for section in data['sections']:
 add(html.escape(section['heading']),'heading',3);md+=['## '+section['heading'],'']
 for text in section['paragraphs']:
  add(html.escape(text),'body',5);md += [text,'']
 for text in section.get('equations',[]):
  add(html.escape(text),'equation',3);md += [text,'']
add('Sources (same numbers as page 1, with additional inputs below)','heading',4)
md+=['## Sources','']
for n,label,url in data['sources']:
 esc=html.escape(url,quote=True)
 add(f'[{n}] {html.escape(label)}<br/><link href="{esc}">{html.escape(url)}</link>','source',3)
 md += [f'[{n}] {label}  ',url,'']
c.save()
source=OUT/'baaja-central-estimate-one-pager.pdf'
if not source.exists():source=BASE/'baaja-central-estimate-one-pager.pdf'
original=PdfReader(source);assert len(original.pages)==1,'Expected original one-page brief'
w=PdfWriter();w.append(original);w.append(PdfReader(page));w.add_metadata({'/Title':'BAAJA: additional transmission payments - brief and methodology','/Author':'Dashboard American'})
final=OUT/'baaja-brief-and-methodology.pdf'
with final.open('wb') as f:w.write(f)
(ROOT/'METHODOLOGY_PAGE.md').write_text('\n'.join(md)+'\n')
assert len(PdfReader(final).pages)==2
print(json.dumps({'pdf':str(final),'pages':2,'methodology_bottom_y':y,'bytes':final.stat().st_size},indent=2))
