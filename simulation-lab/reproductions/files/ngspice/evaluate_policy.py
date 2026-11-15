# SPDX-License-Identifier: MIT
"""Evaluate a newly trained policy on independently generated author-code targets.

This calls the authors' environment, observation/action/reward and simulator;
only invalid space metadata and execution/log paths are corrected.
"""
import os,sys,json,time,pickle,random,math,hashlib
from pathlib import Path
# Isolate held-out generation from any ongoing training workers.
root=Path(os.environ['AUTOCKT_RUN_ROOT']).resolve()
eval_source=root/('AutoCkt-evaluation-'+os.environ.get('AUTOCKT_EVAL_SEED','10000')+'-n'+os.environ.get('AUTOCKT_EVAL_COUNT','20'))
import subprocess
if not eval_source.exists():
    subprocess.check_call(['git','clone','--no-hardlinks',str(root/'AutoCkt'),str(eval_source)])
    subprocess.check_call([sys.executable,str(eval_source/'eval_engines/ngspice/ngspice_inputs/correct_inputs.py')])
os.environ['AUTOCKT_SOURCE_DIR']=str(eval_source)
from author_runtime import ROOT, SOURCE, TwoStageAmp
import numpy as np
import gym
import tensorflow as tf
import ray
from ray.rllib.agents import ppo
from ray.tune.logger import UnifiedLogger
from autockt.gen_specs import gen_data

seed=int(os.environ.get('AUTOCKT_EVAL_SEED','10000'));count=int(os.environ.get('AUTOCKT_EVAL_COUNT','20'));training_seed=int(os.environ.get('AUTOCKT_SEED','100'))
checkpoint=json.loads((ROOT/('training-seed'+str(training_seed))/'latest.json').read_text())['checkpoint']
output=ROOT/('evaluation-seed'+str(seed)+'-n'+str(count));output.mkdir(exist_ok=False)
spec_path=SOURCE/'autockt/gen_specs/ngspice_specs_gen_two_stage_opamp';original=spec_path.read_bytes();(output/'training-specs.pkl').write_bytes(original)
random.seed(seed);np.random.seed(seed);tf.set_random_seed(seed)
gen_data(str(SOURCE/'eval_engines/ngspice/ngspice_inputs/yaml_files/two_stage_opamp.yaml'),'two_stage_opamp',count)
heldout=spec_path.read_bytes();(output/'heldout-specs.pkl').write_bytes(heldout)
assert hashlib.sha256(original).digest()!=hashlib.sha256(heldout).digest()
training=pickle.loads(original);testing=pickle.loads(heldout)
train_vectors=set(zip(*[training[k] for k in sorted(training)]));test_vectors=list(zip(*[testing[k] for k in sorted(testing)]));assert not any(v in train_vectors for v in test_vectors)

class EvalEnv(TwoStageAmp):
    def __init__(self,config):
        super(EvalEnv,self).__init__(config)
        self.observation_space=gym.spaces.Box(low=np.array([-1.0]*8+[0.0]*7,dtype=np.float32),high=np.array([1.0]*8+[98.0]*7,dtype=np.float32))

ray.init(num_cpus=1,num_gpus=0,object_store_memory=100000000,redis_max_memory=50000000,include_webui=False,temp_dir=os.environ.get('AUTOCKT_RAY_TMP','/workspace/tmp/builderbob/ac1115e'),plasma_directory=str(ROOT/'tmp'))
config={'train_batch_size':1200,'horizon':30,'num_gpus':0,'model':{'fcnet_hiddens':[64,64]},'num_workers':0,'env_config':{'generalize':True,'run_valid':True}}
start=time.time();rows=[]
try:
    agent=ppo.PPOAgent(config=config,env=EvalEnv,logger_creator=lambda cfg: UnifiedLogger(cfg,str(output)))
    agent.restore(checkpoint)
    env=EvalEnv({'generalize':True,'run_valid':True,'num_valid':count})
    for index in range(count):
        obs=env.reset();steps=0;done=False;trajectory=[]
        while not done and steps<30:
            action=agent.compute_action(obs)
            obs,reward,done,info=env.step(action);steps+=1
            trajectory.append({'action':list(map(int,action)),'parameter_indices':env.cur_params_idx.tolist(),'metrics':env.cur_specs.tolist(),'reward':float(reward),'done':bool(done)})
        target=env.specs_ideal;metrics=env.cur_specs
        strict=bool(all((m<=t if name=='ibias_max' else m>=t) for name,m,t in zip(env.specs_id,metrics,target)))
        row={'index':index,'target':target.tolist(),'observable_order':env.specs_id,'final_metrics':metrics.tolist(),'author_success':bool(done),'strict_constraints_satisfied':strict,'action_steps':steps,'circuit_simulations_including_reset':steps+1,'trajectory':trajectory,'final_native_deck':getattr(env.sim_env,'last_native_deck',None)}
        rows.append(row)
        with (output/'trajectories.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(json.dumps({k:row[k] for k in ['index','author_success','strict_constraints_satisfied','action_steps']}),flush=True)
    import csv
    with (output/'episodes.csv').open('w') as f:
        writer=csv.writer(f);writer.writerow(['index','author_success','strict_constraints_satisfied','action_steps','target_gain_min','target_ibias_max_A','target_phm_min_deg','target_ugbw_min_Hz','actual_gain','actual_ibias_A','actual_phm_deg','actual_ugbw_Hz'])
        for row in rows:writer.writerow([row['index'],row['author_success'],row['strict_constraints_satisfied'],row['action_steps']]+row['target']+row['final_metrics'])
    successes=sum(r['author_success'] for r in rows);strict_successes=sum(r['strict_constraints_satisfied'] for r in rows)
    z=1.95996398454;p=successes/count;den=1+z*z/count;center=(p+z*z/(2*count))/den;half=z*math.sqrt(p*(1-p)/count+z*z/(4*count*count))/den;interval=[center-half,center+half]
    record={'status':'adapted_run','training_seed':training_seed,'evaluation_seed':seed,'count':count,'author_success_count':successes,'strict_success_count':strict_successes,'success_fraction':p,'success_wilson95':interval,'paper_fraction':.963,'paper_fraction_inside_interval':interval[0]<=.963<=interval[1],'mean_action_steps_successes':float(np.mean([r['action_steps'] for r in rows if r['author_success']])) if successes else None,'seconds':time.time()-start,'checkpoint':checkpoint,'heldout_sha256':hashlib.sha256(heldout).hexdigest(),'training_specs_sha256':hashlib.sha256(original).hexdigest(),'heldout_training_vectors_disjoint':True,'paper_result_reproduced':False,'limitations':['Newly trained public64x64 policy differs from article stated3x50 network.','ngspice41 and Python3.6 rather than original release27/Python3.5.','Original evaluation seeds and original policy unavailable.','Bounded training may not meet source convergence criterion.']}
    (output/'evaluation.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
finally:
    spec_path.write_bytes(original)
    ray.shutdown()
