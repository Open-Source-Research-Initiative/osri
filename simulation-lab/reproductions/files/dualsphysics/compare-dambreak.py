#!/usr/bin/env python3
"""Compare author gauge CSV with the bundled published-experiment fixture."""
import argparse,bisect,csv,hashlib,json,math,os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--gauge',type=Path,required=True);p.add_argument('--experiment',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--plot',action='store_true');a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
with a.gauge.open() as f:raw=list(csv.DictReader(f,delimiter=';'))
times=[float(r['time [s]']) for r in raw];front=[float(r['swlx [m]']) for r in raw]
with a.experiment.open(encoding='cp1252') as f:
 lines=f.readlines()[2:]
exp=[tuple(map(float,line.split())) for line in lines if line.strip()];exp=[(t,x) for t,x in exp if x<=3.9]
def interpolate(t):
 if not times[0]<=t<=times[-1]:raise ValueError('Simulation does not cover experiment time')
 j=bisect.bisect_left(times,t)
 if j==0:return front[0]
 u=(t-times[j-1])/(times[j]-times[j-1]);return front[j-1]+u*(front[j]-front[j-1])
rows=[{'time_s':t,'experimental_front_as_provided':x,'simulated_front_m':interpolate(t),'difference_m':interpolate(t)-x} for t,x in exp]
with (out/'front-comparison.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
errors=[r['difference_m'] for r in rows]
record={'performed':True,'passed':None,'observable':'Horizontal SWL-gauge front at z=0.03m, interpolated to fixture times','reference':'Koshizuka and Oka1996 values as bundled by the DualSPHysics authors','points':len(rows),'predeclared_selection':'Only reference x<=3.9, before4m right-wall contact','measurements':{'mae_m':sum(abs(x) for x in errors)/len(errors),'rmse_m':math.sqrt(sum(x*x for x in errors)/len(errors)),'max_abs_m':max(abs(x) for x in errors)},'input_hashes':{str(p.name):hashlib.sha256(p.read_bytes()).hexdigest() for p in [a.gauge,a.experiment]},'tolerance':None,'interpretation':'Numerical discrepancy against an upstream paper-associated validation fixture. No source uncertainty/acceptance threshold supplied. Fixture scaling/observable definition was not independently verified against the original1996 article; no paper-result reproduction is claimed.'}
(out/'comparison.json').write_text(json.dumps(record,indent=2)+'\n')
if a.plot:
 os.environ.setdefault('MPLCONFIGDIR',str(out/'.matplotlib-cache'))
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(1,2,figsize=(9,3.5),layout='constrained')
 relevant=[(t,x) for t,x in zip(times,front) if t<=.75]
 axes[0].plot([t for t,x in relevant],[x for t,x in relevant],label='DualSPHysics5.4 gauge')
 axes[0].plot([r['time_s'] for r in rows],[r['experimental_front_as_provided'] for r in rows],'o',label='Author experiment fixture')
 axes[0].set(xlabel='Time (s, author fixture scaling assumed)',ylabel='Front position (m)');axes[0].legend()
 axes[1].plot([r['time_s'] for r in rows],errors,'o-');axes[1].axhline(0,color='gray',lw=1);axes[1].set(xlabel='Time (s)',ylabel='Simulation minus fixture (m)')
 fig.savefig(out/'dambreak-comparison.svg');fig.savefig(out/'dambreak-comparison.png',dpi=160)
print(json.dumps(record,indent=2))
