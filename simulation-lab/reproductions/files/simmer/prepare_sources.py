# SPDX-License-Identifier: MIT
"""Retrieve publisher/CRAN sources and refuse changed input bytes."""
from pathlib import Path
import hashlib
import urllib.request

BASE = Path(__file__).resolve().parent
SOURCES = {
    'replication.R': ('https://www.jstatsoft.org/article/download/v090i02/3818', '72131e759ea273394f7c78450ad0c5a4aebc310b3993679a9b6c814b06cb2478'),
    'simmer-publisher.tar.gz': ('https://www.jstatsoft.org/index.php/jss/article/view/v090i02/3817', '9a06202908ed78e4f3d15bfada06f06d85622c2070a89ac7318c450de2bbf5c8'),
    'BH_1.69.0-1.tar.gz': ('https://cran.r-project.org/src/contrib/Archive/BH/BH_1.69.0-1.tar.gz', 'a0fd4364b7e368f09c56dec030823f52c16da0787580af7e4615eddeb99baca2'),
}
(BASE / 'sources').mkdir(exist_ok=True)
for name, (url, expected) in SOURCES.items():
    path = BASE / 'sources' / name
    if not path.exists():
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError(f'Source bytes changed: {url}')
        path.write_bytes(data)
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError(f'Local input changed: {name}')
    print(name, expected)
