#!/usr/bin/env python3
"""Retrieve pinned author tools and build the CPU solver locally."""
import argparse,os,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=Path('DualSPHysics'));a=p.parse_args();src=a.source.resolve();sha='ef3721a861fda961f0e2f9ec4cd317b19de99086'
if src.exists():raise SystemExit(f'Refusing to overwrite {src}')
def run(args,**kw):subprocess.run([str(x) for x in args],check=True,**kw)
run(['git','init',src]);run(['git','-C',src,'remote','add','origin','https://github.com/DualSPHysics/DualSPHysics.git']);run(['git','-C',src,'sparse-checkout','init','--cone']);run(['git','-C',src,'sparse-checkout','set','src/source','src/lib','bin/linux','examples/main/01_DamBreak']);run(['git','-C',src,'fetch','--depth','1','--filter=blob:none','origin',sha]);run(['git','-C',src,'checkout','--detach','FETCH_HEAD'])
# GCC13 needs a cstdint include for SIZE_MAX. Disable optional components unused
# by this dam-break case. Keep the upstream fast-math setting and model unchanged.
run(['make','-f','Makefile_cpu','-j2','CC=g++ -include cstdint','COMPILE_CHRONO=NO','COMPILE_WAVEGEN=NO','COMPILE_MOORDYNPLUS=NO'],cwd=src/'src/source')
for name in ['GenCase_linux64','DualSPHysics5.4CPU_linux64']:
 p=src/'bin/linux'/name;p.chmod(p.stat().st_mode|0o100)
print('Solver:',src/'bin/linux/DualSPHysics5.4CPU_linux64')
