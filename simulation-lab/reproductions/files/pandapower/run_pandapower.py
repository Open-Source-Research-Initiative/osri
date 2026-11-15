# SPDX-License-Identifier: MIT
from __future__ import print_function
import os,json,time,hashlib,sys,warnings
from pathlib import Path
os.environ['MPLBACKEND']='Agg'
import numpy as np
import pandas as pd
root=Path(__file__).resolve().parent
source=Path(sys.argv[sys.argv.index('--source')+1]).resolve() if '--source' in sys.argv else root/'pandapower-paper';out=root/'pandapower-output';out.mkdir(exist_ok=True)
os.chdir(str(source));started=time.time();warnings.filterwarnings('ignore',category=FutureWarning)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ns={'__name__':'__main__'}
def cell(name,index):
 nb=json.loads((source/name).read_text());return ''.join(nb['cells'][index]['source'])
for i in [2,4,6,9,12,15,16,20]:
 print('Switch notebook cell',i,flush=True);exec(compile(cell('switch_evaluation.ipynb',i),'switch_evaluation.ipynb:'+str(i),'exec'),ns)
sw=ns['sw'];sw.to_json(str(out/'switches.json'));sw.to_csv(str(out/'switches.csv'))
counts={'all_states':len(sw),'infeasible_topology':int(((sw.supplied==False)|(sw.radial==False)).sum()),'short_circuit_invalid':int((sw.sc_valid==False).sum()),'valid_states':int(sw.valid.sum())}
expected={'all_states':276,'infeasible_topology':96,'short_circuit_invalid':100,'valid_states':80}
reference=pd.read_json(str(source/'results/results_switches.json')).reindex(sw.index)
checks={'published_switch_counts':counts==expected,'reference_valid_switch_ids':set(sw[sw.valid].index)==set(reference[reference.valid].index)}
diff_sc=float(np.nanmax(np.abs(pd.to_numeric(sw.min_sc).values-pd.to_numeric(reference.min_sc).values)))
checks['reference_short_circuit_currents']=diff_sc<=1e-5
partial={'source_commit':'6213b92acd265cf7803ff4b8978542957d0c9777','paper_doi':'10.1109/TPWRS.2018.2829021','stage':'switch_analysis','counts':counts,'checks':checks,'max_current_difference_ka':diff_sc,'elapsed_seconds':time.time()-started}
(out/'switch-comparison.json').write_text(json.dumps(partial,indent=2)+'\n');print(json.dumps(partial),flush=True)
if '--full-day' not in sys.argv:
    partial['status']='target_compared'
    partial['scope']='Section VII-B switching analysis only'
    partial['passed']=all(checks.values())
    (out/'run-record.json').write_text(json.dumps(partial,indent=2)+'\n')
    sys.exit(0 if partial['passed'] else 1)
for i in [2,4,8,10,12]:
 print('Timeseries notebook cell',i,flush=True);exec(compile(cell('timeseries_simulation.ipynb',i),'timeseries_simulation.ipynb:'+str(i),'exec'),ns)
print('Executing actual author run_timeseries, 97 timesteps',flush=True)
exec(compile(cell('timeseries_simulation.ipynb',14),'timeseries_simulation.ipynb:14','exec'),ns)
r=ns['results'];r.to_json(str(out/'timeseries.json'));r.to_csv(str(out/'timeseries.csv'))
ref=pd.read_json(str(source/'results/results_timeseries.json'),convert_axes=False).reindex(r.index)
tolerances={'losses':0.001,'max_line_loading':0.001,'max_trafo_loading':0.001,'min_voltage':1e-6,'max_voltage':1e-6,'tp_2w':0,'tp_3w':0,'min_sc':1e-5}
errors={k:float(np.max(np.abs(pd.to_numeric(r[k]).values-pd.to_numeric(ref[k]).values)))for k in tolerances}
ref_checks={k:errors[k]<=tolerances[k]for k in tolerances};ref_checks['switches']=r.switches.tolist()==ref.switches.tolist()
constraints={'voltage_within_0.97_1.03':bool((r.min_voltage>=0.97-1e-6).all()and(r.max_voltage<=1.03+1e-6).all()),'line_loading_below_50_percent':bool((r.max_line_loading<50+1e-3).all()),'transformer_loading_below_50_percent':bool((r.max_trafo_loading<50+1e-3).all()),'minimum_fault_current_above_1.1_ka':bool((r.min_sc>1.1-1e-5).all()),'published_nine_switching_states':len(set(tuple(v)for v in r.switches))==9}
import pandapower as pp,scipy,networkx,matplotlib
matplotlib.use('Agg');import matplotlib.pyplot as plt
fig,axes=plt.subplots(3,1,figsize=(10,8),sharex=True)
axes[0].plot(range(len(r)),r.losses.astype(float));axes[0].set_ylabel('15-min losses (kWh)')
axes[1].plot(range(len(r)),r.min_voltage.astype(float),label='minimum');axes[1].plot(range(len(r)),r.max_voltage.astype(float),label='maximum');axes[1].axhline(.97,c='gray',ls=':');axes[1].axhline(1.03,c='gray',ls=':');axes[1].set_ylabel('Voltage (pu)');axes[1].legend()
axes[2].plot(range(len(r)),r.max_line_loading.astype(float),label='line');axes[2].plot(range(len(r)),r.max_trafo_loading.astype(float),label='transformer');axes[2].axhline(50,c='gray',ls=':');axes[2].set_ylabel('Loading (%)');axes[2].legend();axes[2].set_xticks([0,24,48,72,96]);axes[2].set_xticklabels(['00:00','06:00','12:00','18:00','24:00']);axes[2].set_xlabel('Time');fig.tight_layout();fig.savefig(str(out/'timeseries.png'),dpi=150)
record={'status':'target_compared','paper_doi':'10.1109/TPWRS.2018.2829021','paper_targets':'Section VII-B switching-state counts; VII-D/Figure7 operational limits and nine selected states','source_commit':'6213b92acd265cf7803ff4b8978542957d0c9777','counts':counts,'switch_checks':checks,'max_current_difference_ka':diff_sc,'timeseries_rows':len(r),'selected_states':len(set(tuple(v)for v in r.switches)),'paper_operational_checks':constraints,'author_reference_max_errors':errors,'author_reference_checks':ref_checks,'tolerances':tolerances,'published_count_target_passed':all(checks.values()),'full_comparison_passed':all(checks.values())and all(constraints.values())and all(ref_checks.values()),'limits':'Any failed reference comparisons are preserved, not silently normalized. Pin version matches article; exact dependency lock was reconstructed. Scientific review pending.','environment':{'python':sys.version,'pandapower':pp.__version__,'numpy':np.__version__,'scipy':scipy.__version__,'pandas':pd.__version__,'networkx':networkx.__version__,'matplotlib':matplotlib.__version__},'elapsed_seconds':time.time()-started,'input_hashes':{str(p.relative_to(source)):sha(p)for p in [source/'data/case_study_grid.xlsx',source/'data/profiles.csv',source/'results/results_switches.json',source/'results/results_timeseries.json']},'source_hashes':{name:sha(source/name)for name in ['switch_evaluation.ipynb','timeseries_simulation.ipynb']}}
(out/'run-record.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2),flush=True)
