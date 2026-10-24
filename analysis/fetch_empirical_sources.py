"""Download the exact public source snapshots listed in the evidence manifest.
Requires network access; about 220 MB. A changed public snapshot is rejected,
so rerunning later cannot silently overwrite the audited vintage.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from zipfile import ZipFile
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];RAW=ROOT/'research/2026-10-23/raw';RAW.mkdir(parents=True,exist_ok=True)
for row in json.loads((ROOT/'data/evidence/source-manifest.json').read_text()):
 if 'sha256' not in row:continue
 file=RAW/row['file']
 if not file.exists():
  b=urlopen(Request(row['url'],headers={'User-Agent':'Mozilla/5.0'}),timeout=90).read()
  if hashlib.sha256(b).hexdigest()!=row['sha256']:raise ValueError('Source vintage changed: '+row['file'])
  file.write_bytes(b)
 assert hashlib.sha256(file.read_bytes()).hexdigest()==row['sha256'],row['file']
for archive in ('mtep25.zip','mtep26-draft.zip'):
 with ZipFile(RAW/archive) as z:
  for name in z.namelist():
   folder=None
   if archive=='mtep25.zip' and name.endswith('.xlsx'):folder=RAW.parent/'extracted'
   if archive=='mtep26-draft.zip' and 'MTEP26 EPR TSTF' in name and name.endswith('.pdf'):folder=RAW.parent/'miso26'
   if folder:
    folder.mkdir(exist_ok=True);(folder/Path(name).name).write_bytes(z.read(name))
print('Verified source hashes and extracted the workbooks and EPR reports.')
