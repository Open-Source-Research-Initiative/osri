"""Fetch immutable author input and paper reference figure; verify content hashes.
Original OSRI helper, MIT. Run explicitly; original inputs keep their own terms.
"""
from pathlib import Path
import hashlib,json,urllib.request
root=Path(__file__).resolve().parent
for name,source in json.loads((root/'source-manifest.json').read_text()).items():
    target=root/name
    if target.exists():
        data=target.read_bytes()
    else:
        with urllib.request.urlopen(source['url'],timeout=60) as response:
            data=response.read()
    if hashlib.sha256(data).hexdigest()!=source['sha256']:
        raise RuntimeError('Unexpected source bytes: '+name)
    if not target.exists(): target.write_bytes(data)
    print(name,source['sha256'])
