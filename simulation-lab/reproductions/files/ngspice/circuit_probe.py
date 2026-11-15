# SPDX-License-Identifier: MIT
"""Run the actual author's fixed reset design and one actual environment action."""
import json,time,hashlib,sys,os
from pathlib import Path
from author_runtime import ROOT, SOURCE, TwoStageAmp
import numpy as np
start=time.time()
env=TwoStageAmp({'generalize':True,'run_valid':True,'num_valid':20})
initial=env.reset()
case_dirs=[Path(env.sim_env.last_native_deck).parent]
before={'parameter_indices':env.cur_params_idx.tolist(),'specs':env.cur_specs.tolist(),'target':env.specs_ideal.tolist(),'reward':float(env.reward(env.cur_specs,env.specs_ideal))}
ob,reward,done,info=env.step([1]*7)
case_dirs.append(Path(env.sim_env.last_native_deck).parent)
after={'parameter_indices':env.cur_params_idx.tolist(),'specs':env.cur_specs.tolist(),'reward':float(reward),'done':bool(done)}
assert np.isfinite(env.cur_specs).all()
assert np.all(env.cur_specs==np.asarray(before['specs']))
native=[]
for p in [f for d in case_dirs for f in d.iterdir()]:
 if p.is_file():native.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
record={'status':'author_code_executed','python':sys.version,'before':before,'after':after,'observable_order':env.specs_id,'seconds':time.time()-start,'checks':{'finite_specs':True,'hold_action_preserves_specs':True},'native_outputs':native,'interpretation':'Executes author circuit and its measurement/reward environment. This is an initial circuit check, not learned-policy held-out evaluation or a reproduced paper target.'}
(ROOT/'circuit-probe.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
