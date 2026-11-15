# SPDX-License-Identifier: MIT
"""Workspace-only execution adapter for the pinned AutoCkt source.

Imports the authors' public ngspice environment and measurement code. The
adapter changes scratch placement and logging only; circuit parameters,
measurements, action mapping, observation and reward stay in author code.
"""
import os
import subprocess
from pathlib import Path

ROOT = Path(os.environ['AUTOCKT_RUN_ROOT']).resolve()
SOURCE = Path(os.environ.get('AUTOCKT_SOURCE_DIR',str(ROOT / 'AutoCkt'))).resolve()
os.chdir(str(SOURCE))
import sys
sys.path.insert(0, str(SOURCE))
from eval_engines.ngspice.ngspice_wrapper import NgSpiceWrapper

NgSpiceWrapper.BASE_TMP_DIR = str(ROOT / 'native')

def logged_simulate(self, fpath):
    if os.environ.get('AUTOCKT_ADD_QUIT')=='1':
        deck=Path(fpath);text=deck.read_text()
        if '\nquit\n' not in text:deck.write_text(text.replace('.endc','quit\n.endc'))
    self.last_native_deck=fpath
    destination = str(Path(fpath).with_suffix('.ngspice.log'))
    with open(destination, 'w') as log:
        completed = subprocess.run([os.environ.get('AUTOCKT_NGSPICE', 'ngspice'), '-b', fpath], stdout=log, stderr=subprocess.STDOUT, cwd=str(Path(fpath).parent))
    if completed.returncode != 0:
        raise RuntimeError('ngspice failed with code{}; see {}'.format(completed.returncode, destination))
    return 0

NgSpiceWrapper.simulate = logged_simulate
from autockt.envs.ngspice_vanilla_opamp import TwoStageAmp
