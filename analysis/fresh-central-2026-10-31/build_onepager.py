"""Render a plain, one-page brief; content and citations match the Markdown."""
from pathlib import Path
import html
import json
import re
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent
OUT = BASE / 'output/pdf'
OUT.mkdir(parents=True, exist_ok=True)
data = json.loads((ROOT / 'brief-content.json').read_text())
fonts = Path(reportlab.__file__).parent / 'fonts'
pdfmetrics.registerFont(TTFont('Vera', str(fonts / 'Vera.ttf')))
pdfmetrics.registerFont(TTFont('VeraBold', str(fonts / 'VeraBd.ttf')))
styles = {
    'title': ParagraphStyle('title', fontName='VeraBold', fontSize=18, leading=22),
    'subtitle': ParagraphStyle('subtitle', fontName='Vera', fontSize=8.8, leading=12),
    'heading': ParagraphStyle('heading', fontName='VeraBold', fontSize=10.7, leading=14),
    'body': ParagraphStyle('body', fontName='Vera', fontSize=10.3, leading=13.8),
    'source': ParagraphStyle('source', fontName='Vera', fontSize=8.2, leading=10.8),
}
pdf = OUT / 'baaja-central-estimate-one-pager.pdf'
c = canvas.Canvas(str(pdf), pagesize=(612, 792))
c.setTitle(data['title'])
c.setAuthor('Dashboard American')
y = 752
width = 524
source_urls = {n: url for n, label, url in data['sources']}

def citations(text):
    escaped = html.escape(text).replace('[2-4]', '[2, 3, 4]')
    def replace(match):
        return '[' + ', '.join('<link href="' + source_urls[n.strip()] + '">' + n.strip() + '</link>' for n in match.group(1).split(',')) + ']'
    return re.sub(r'\[([1-5](?:, [1-5])*)\]', replace, escaped)

def add(text, kind, gap):
    global y
    p = Paragraph(text, styles[kind])
    _, height = p.wrap(width, 800)
    if y - height < 33:
        raise RuntimeError(f'One-page overflow at {kind}: bottom={y-height}')
    p.drawOn(c, 44, y - height)
    y -= height + gap

add(html.escape(data['title']), 'title', 7)
add(html.escape(data['subtitle']), 'subtitle', 12)
md = ['# ' + data['title'], '', data['subtitle'], '', '[Download the one-page brief](baaja-central-estimate-one-pager.pdf)', '']
for section in data['sections']:
    add(html.escape(section['heading']), 'heading', 4)
    md += ['## ' + section['heading'], '']
    for text in section['paragraphs']:
        add(citations(text), 'body', 7)
        md += [text, '']
add('Sources', 'heading', 3)
md += ['## Sources', '']
for n, label, url in data['sources']:
    add(f'[{n}] <link href="{html.escape(url, quote=True)}">{html.escape(label)}</link>', 'source', 2)
    md += [f'[{n}] [{label}]({url})', '']
c.save()
(ROOT / 'ONE_PAGER.md').write_text('\n'.join(md))
print(json.dumps({'pdf':str(pdf), 'bottom_y':y, 'bytes':pdf.stat().st_size}, indent=2))
