#!/usr/bin/env python3
"""Retrieve the pinned sources and conda archives, then write a local explicit spec."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import shutil
from urllib.parse import urlsplit
from urllib.request import urlopen

PACKET = Path(__file__).resolve().parent


def digest(path):
    with path.open('rb') as stream:
        hash_value = sha256()
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            hash_value.update(block)
    return hash_value.hexdigest()


def fetch(task):
    path, pin = task
    if path.exists():
        if digest(path) != pin['sha256']:
            raise ValueError(f'Cached input does not match the SHA-256 pin: {path}')
        return
    staging = path.with_name(path.name + '.partial')
    try:
        with urlopen(pin['url'], timeout=90) as response, staging.open('wb') as output:
            shutil.copyfileobj(response, output)
        if digest(staging) != pin['sha256']:
            raise ValueError(f'Input does not match the SHA-256 pin: {pin["url"]}')
        staging.replace(path)
    finally:
        staging.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('work', type=Path)
    work = parser.parse_args().work.resolve()
    inputs = json.loads((PACKET / 'inputs.lock.json').read_text())
    sources = work / 'sources'
    archives = work / 'conda-archives'
    sources.mkdir(parents=True, exist_ok=True)
    archives.mkdir(parents=True, exist_ok=True)
    packages = [
        (archives / Path(urlsplit(pin['url']).path).name, pin)
        for pin in inputs['conda_linux_64']
    ]
    tasks = [(sources / name, pin) for name, pin in inputs['sources'].items()] + packages
    with ThreadPoolExecutor(max_workers=8) as workers:
        list(workers.map(fetch, tasks))
    lines = ['@EXPLICIT', *(f'{path.as_uri()}#{pin["md5"]}' for path, pin in packages)]
    (work / 'conda-explicit-local.txt').write_text('\n'.join(lines) + '\n')
    print(f'Verified SHA-256 for {len(tasks)} inputs.')


if __name__ == '__main__':
    main()
