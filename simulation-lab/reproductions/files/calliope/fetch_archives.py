#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Retrieve immutable author archives. Defaults to results (~1.1GB)."""
from pathlib import Path
import argparse,urllib.request,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--model',action='store_true');a=p.parse_args()
items=[('6546817','euro-spores-results-v2022-05-13.zip','bf96601426a9a12811b939d228fa8762')]
if a.model:items.append(('5774988','euro-calliope-sector-coupled-v0.1.zip','6a9229f24e1331418dea288841ef3fd4'))
for record,name,expected in items:
 path=Path(name)
 if not path.exists():
  with urllib.request.urlopen(f'https://zenodo.org/api/records/{record}/files/{name}/content',timeout=90)as response,path.open('wb')as out:
   while True:
    block=response.read(1024*1024)
    if not block:break
    out.write(block)
 digest=hashlib.md5()
 with path.open('rb')as f:
  for block in iter(lambda:f.read(1024*1024),b''):digest.update(block)
 assert digest.hexdigest()==expected,f'Checksum mismatch: {name}'
 print(json.dumps({'archive':name,'doi':'10.5281/zenodo.'+record,'bytes':path.stat().st_size,'md5':expected}))
