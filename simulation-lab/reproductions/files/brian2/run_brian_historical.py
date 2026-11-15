"""Execute pinned author model cells; export data without modifying equations.
Author notebook: brian-team/brian2_paper_examples, MIT or CC-BY-4.0.
This wrapper is original OSRI code, MIT. Python 3.6 compatible.
"""
from pathlib import Path
import argparse, csv, hashlib, json, sys, time
import numpy as np
import brian2 as b
parser=argparse.ArgumentParser()
parser.add_argument('--notebook',type=Path,default=Path(__file__).with_name('example_2_eye_movements.ipynb'))
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
args.output.mkdir(parents=True,exist_ok=False)
blocks=[''.join(c['source']) for c in json.loads(args.notebook.read_text())['cells'] if c['cell_type']=='code']
assert len(blocks)==9 and blocks[-1].startswith('from plotly import tools')
b.prefs.codegen.target='numpy'
ns={'__name__':'__main__'}
start=time.time()
for block in blocks[:-1]:exec(compile(block,str(args.notebook),'exec'),ns)
M=ns['M'];retina=ns['S_retina'];motor=ns['S_motoneurons']
t=np.asarray(M.t/b.second);x=np.asarray(M.x[0]);obj=np.asarray(M.x_object[0]);target=np.asarray(M.x0[0])
np.savez_compressed(str(args.output/'trajectories.npz'),t_seconds=t,eye=x,object=obj,muscle_target=target,retinal_spike_t_seconds=np.asarray(retina.t/b.second),retinal_spike_i=np.asarray(retina.i),motor_spike_t_seconds=np.asarray(motor.t/b.second),motor_spike_i=np.asarray(motor.i))
np.savetxt(str(args.output/'positions.csv'),np.column_stack((t,x,obj,target)),delimiter=',',header='time_seconds,eye_position,object_position,muscle_target',comments='')
record={'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'status':'author_code_executed','source_commit':'73045cd61322e923e96883dc97c0848154f79f8c','paper':'10.7554/eLife.47314','paper_target':'Figure3b/c','python':sys.version,'packages':{'brian2':b.__version__,'numpy':np.__version__},'source_notebook_sha256':hashlib.sha256(args.notebook.read_bytes()).hexdigest(),'model_cells_sha256':hashlib.sha256('\n'.join(blocks[:-1]).encode()).hexdigest(),'model_cells_modified':False,'presentation_omitted':'Only final Plotly cell; all 8 model cells unchanged.','tau_object_seconds':float(ns['tau_object']/b.second),'dt_seconds':float(b.defaultclock.dt/b.second),'samples':len(t),'retinal_spikes':int(retina.num_spikes),'motor_spikes':list(map(int,motor.count)),'eye_object_rmse':float(np.sqrt(np.mean((x-obj)**2))),'elapsed_seconds':time.time()-start,'checks':{'samples_100000':len(t)==100000,'finite_positions':bool(np.isfinite(np.column_stack((t,x,obj,target))).all()),'strictly_increasing_time':bool((np.diff(t)>0).all())},'paper_discrepancy':'Paper Figure3c and author notebook both use tau_object500ms; earlier50ms manual transcription corrected. Figure3b uses qualitative tick labels; numeric scale recovered from author Plotly code.','human_scientific_review':'pending'}
record['outputs']={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in args.output.iterdir() if p.is_file()}
(args.output/'run-record.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2));assert all(record['checks'].values())
