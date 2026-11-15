# SPDX-License-Identifier: MIT
"""Retrieve the author repository locally without vendoring it into the Lab."""
import subprocess,sys,os
from pathlib import Path
root=Path(os.environ.get('AUTOCKT_RUN_ROOT','.')).resolve()
source=root/'AutoCkt'
url='https://github.com/ksettaluri6/AutoCkt.git';commit='a6c8a61d3dffb8b433f19251e135994a5b0f6ee4'
if source.exists():
    actual=subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD']).decode().strip()
    if actual!=commit:raise RuntimeError('Existing source is at a different commit; inspect it instead of overwriting.')
else:
    subprocess.check_call(['git','clone',url,str(source)])
    subprocess.check_call(['git','-C',str(source),'checkout',commit])
subprocess.check_call([sys.executable,str(source/'eval_engines/ngspice/ngspice_inputs/correct_inputs.py')])
print('Retrieved author source at '+commit+'; no license detected, do not redistribute repository contents.')
