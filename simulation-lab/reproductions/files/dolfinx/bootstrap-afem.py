#!/usr/bin/env python3
"""Prepare the tested isolated Linux environment and exact author sources."""
from pathlib import Path
import argparse,os,subprocess
p=argparse.ArgumentParser();p.add_argument('--mamba',default='micromamba');p.add_argument('--work',type=Path,default=Path('afem-work'));a=p.parse_args();root=a.work.resolve();root.mkdir(parents=True,exist_ok=True);env=root/'env';here=Path(__file__).resolve().parent
os.environ.update(MAMBA_ROOT_PREFIX=str(root/'mamba'),TMPDIR=str(root/'tmp'),PIP_CACHE_DIR=str(root/'cache/pip'))
(root/'tmp').mkdir(exist_ok=True)
def run(args,**kw):subprocess.run([str(x) for x in args],check=True,**kw)
run([a.mamba,'create','-y','-p',env,'--file',here/'conda-linux64.lock'])
run([env/'bin/python','-m','pip','install','setuptools==80.9.0'])
for name,url,sha in [('source','https://github.com/brodbeck-m/AFEM-by-Equilibration.git','3d9741498712c13ce901f5fbd6255a82a3cec1ac'),('dolfinx_eqlb','https://github.com/brodbeck-m/dolfinx_eqlb.git','16f5ea6e16aa15d856381e32a3be5fc2f913215a')]:
 dest=root/name
 if dest.exists():raise SystemExit(f'Refusing to overwrite {dest}')
 run(['git','init',dest]);run(['git','-C',dest,'fetch','--depth','1',url,sha]);run(['git','-C',dest,'checkout','--detach','FETCH_HEAD'])
base=[a.mamba,'run','-p',env]
run(base+['cmake','-S',root/'dolfinx_eqlb/cpp','-B',root/'build-cpp','-G','Ninja','-DCMAKE_BUILD_TYPE=Release',f'-DCMAKE_INSTALL_PREFIX={env}'])
run(base+['cmake','--build',root/'build-cpp','--parallel','2']);run(base+['cmake','--install',root/'build-cpp'])
# Match the successful isolated build. These add missing include search paths;
# no author model, estimator, or mesh-refinement code is modified.
os.environ['CXXFLAGS']=f'-I{env}/lib/python3.10/site-packages/dolfinx/wrappers -I{env}/include/eigen3'
os.environ['CMAKE_PREFIX_PATH']=str(env)
run(base+['python','-m','pip','install','--no-build-isolation','--no-deps',root/'dolfinx_eqlb/python'])
print('Ready. Run:',env/'bin/python',here/'run-afem.py','--source',root/'source','--output',root/'results')
