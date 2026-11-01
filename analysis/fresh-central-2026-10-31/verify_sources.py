"""Verify downloaded original files and exact XLSX cells, using the standard library.

Usage: python3 verify_sources.py /path/to/original/files
Download URLs and required filenames are in review/sources.json. No network calls.
Missing files and hash changes are reported, not silently accepted. PDF contents
still need manual page review; only workbook cells are automatically inspected.
"""
from pathlib import Path
import csv, hashlib, json, math, posixpath, sys, zipfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def sheet_cells(path,sheet):
    with zipfile.ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            strings=[''.join(n.itertext()) for n in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS)]
        rels={n.attrib['Id']:n.attrib['Target'] for n in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        book=ET.fromstring(z.read('xl/workbook.xml'))
        chosen=next(n for n in book.findall('m:sheets/m:sheet',NS) if n.attrib['name']==sheet)
        target=rels[chosen.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
        target=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
        result={}
        for n in ET.fromstring(z.read(target)).findall('.//m:c',NS):
            value=n.find('m:v',NS)
            if value is not None:
                result[n.attrib['r']]=strings[int(value.text)] if n.attrib.get('t')=='s' else value.text
        return result

def main(directory):
    source_list=json.loads((ROOT/'review/sources.json').read_text())['sources']
    sources={r['id']:r for r in source_list}
    files={};found=[];missing=[];changed=[];unarchived=[]
    for r in source_list:
        if not r['archived_sha256']:
            unarchived.append(r['id']);continue
        p=directory/r['original_filename']
        if not p.exists():missing.append(r['id']);continue
        actual=hashlib.sha256(p.read_bytes()).hexdigest()
        if actual!=r['archived_sha256']:changed.append(r['id']);continue
        files[r['id']]=p;found.append(r['id'])
    cache={};checked=0
    for r in csv.DictReader((ROOT/'review/source-values.csv').open()):
        sid=r['source_id']
        if sid not in files or files[sid].suffix!='.xlsx':continue
        sheet,cell=r['locator'].rsplit('!',1)
        key=(sid,sheet)
        if key not in cache:cache[key]=sheet_cells(files[sid],sheet)
        actual=float(cache[key][cell]);expected=float(r['value'])
        if not math.isclose(actual,expected,rel_tol=1e-12,abs_tol=1e-9):raise AssertionError(r)
        checked+=1
    status='PASS_FOR_ARCHIVED_FILES' if not missing and not changed else 'INCOMPLETE_OR_CHANGED'
    return dict(status=status,matched_original_hashes=found,missing_files=missing,changed_originals=changed,workbook_cells_verified=checked,sources_without_archived_binary=unarchived,limits='Hash and XLSX-cell verification only. PDF pages, unarchived web sources, and evidence representativeness require manual review. A source refresh may change a hash without making either vintage wrong.')

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit(__doc__)
    try:
        report=main(Path(sys.argv[1]));print(json.dumps(report,indent=2));sys.exit(0 if report['status']=='PASS_FOR_ARCHIVED_FILES' else 2)
    except Exception as e:print(json.dumps(dict(status='FAIL',error=str(e)),indent=2));sys.exit(1)
