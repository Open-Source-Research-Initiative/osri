#!/usr/bin/env python3
"""Run unchanged author dam-break case, retaining a timed-out run and restart."""
import argparse,os,subprocess,time,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--wall-seconds',type=int,default=300);a=p.parse_args();source=a.source.resolve();root=a.output.resolve();root.mkdir(parents=True,exist_ok=False)
env=os.environ.copy();env['OMP_NUM_THREADS']='2';start=time.monotonic();commands=[]
def run(args,log,timeout=None):
 cmd=[str(x) for x in args]
 with (root/log).open('w') as f:
  try:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=timeout);code=r.returncode
  except subprocess.TimeoutExpired:code=124
 commands.append({'argv':cmd,'exit_code':code,'log':log})
 return code
case=source/'examples/main/01_DamBreak/CaseDambreakVal2D_Def';initial=root/'initial';binary=source/'bin/linux/DualSPHysics5.4CPU_linux64'
code=run([source/'bin/linux/GenCase_linux64',case,initial/'CaseDambreakVal2D','-save:all'],'gencase.log');assert code==0
code=run([binary,'-ompthreads:2',initial/'CaseDambreakVal2D',initial],'solver-initial.log',a.wall_seconds)
if code==124:
 parts=sorted((initial/'data').glob('Part_*.bi4'));part=int(parts[-1].stem.split('_')[1])
 code=run([binary,'-ompthreads:2',f'-partbegin:{part}',initial/'data',initial/'CaseDambreakVal2D',root/'resumed'],'solver-resumed.log',a.wall_seconds)
record={'source_commit':'ef3721a861fda961f0e2f9ec4cd317b19de99086','commands':commands,'exit_code':code,'elapsed_seconds':time.monotonic()-start,'note':'Native restart uses author single-precision position files; the upstream solver warns of minor restart differences. Pre-impact comparison data are in the initial run.'}
(root/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
raise SystemExit(code)
