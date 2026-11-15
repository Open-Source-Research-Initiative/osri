#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Retrieve the exact2016 SUMO source release and author scenario."""
from pathlib import Path
import urllib.request,hashlib,tarfile,subprocess
root=Path(__file__).resolve().parent
path=root/'sumo-src-0.26.0.tar.gz'
if not path.exists():
 with urllib.request.urlopen('https://downloads.sourceforge.net/project/sumo/sumo/version%200.26.0/sumo-src-0.26.0.tar.gz',timeout=60)as response,path.open('wb')as out:
  while True:
   block=response.read(1024*1024)
   if not block:break
   out.write(block)
assert hashlib.sha256(path.read_bytes()).hexdigest()=='258ed74514ab119b5a812908a8bf97b4ea6ef91a3b921499feff3b642e4bad39','Source release changed'
if not (root/'sumo-0.26.0').exists():
 with tarfile.open(path)as archive:archive.extractall(root,filter='data')
if not (root/'LuSTScenario').exists():subprocess.run(['git','clone','https://github.com/lcodeca/LuSTScenario.git',str(root/'LuSTScenario')],check=True)
subprocess.run(['git','-C',str(root/'LuSTScenario'),'checkout','5edb7ecb9ad196c39172b6eb95d19ed789f4b1a6'],check=True)
print('Retrieved SUMO0.26.0 and pinned LuST scenario. SUMO source GPL-3.0-or-later; LuST scenario MIT.')
