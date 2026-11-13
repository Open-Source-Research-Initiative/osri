#!/usr/bin/env python3
"""Rebuild the Chinese navigation-label font from the kit's OFL font."""
from pathlib import Path
import subprocess
import sys
import tempfile
from fontTools.ttLib import TTFont

site = Path(__file__).resolve().parents[1]
source = site.parent / 'identity/shared-language/fonts/NotoSansCJKSC-Regular.woff2'
output = site / 'assets/fonts/OSRI-CJK-link-subset.woff2'
text = '简体中文（待审核）'
names = {1: 'OSRI CJK Link Subset', 2: 'Regular', 3: 'OSRI CJK Link Subset Regular 2026', 4: 'OSRI CJK Link Subset Regular', 6: 'OSRICJKLinkSubset-Regular', 16: 'OSRI CJK Link Subset', 17: 'Regular'}
with tempfile.TemporaryDirectory(dir=output.parent) as temp_dir:
    subset = Path(temp_dir) / 'subset.woff2'
    subprocess.run([sys.executable, '-m', 'fontTools.subset', str(source), '--text=' + text, '--flavor=woff2', '--name-IDs=*', '--name-legacy', '--name-languages=*', '--no-recalc-timestamp', '--output-file=' + str(subset)], check=True)
    font = TTFont(subset, recalcTimestamp=False)
    for record in font['name'].names:
        if record.nameID in names:
            record.string = names[record.nameID].encode(record.getEncoding())
    font.save(subset)
    rebuilt = TTFont(subset)
    missing = sorted({char for char in text if ord(char) not in rebuilt.getBestCmap()})
    if missing:
        raise ValueError('Missing label characters: ' + ''.join(missing))
    subset.replace(output)
print(f'Built {output.name}: {len(set(text))} distinct label characters, {output.stat().st_size} bytes')
