"""CPU replay of the paper authors' released frozen Minitaur policies.
Source import compatibility patch is recorded separately. No network retraining.
"""
from pathlib import Path
import csv,json,time,hashlib,sys,os
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/bullet3/examples/pybullet/gym'))
import tensorflow as tf
from pybullet_envs.minitaur.agents.scripts import utility
from pybullet_envs.minitaur.envs import simple_ppo_agent
import pybullet_data
OUT=ROOT/'bullet-output';OUT.mkdir(exist_ok=True)
start=time.time();all_results=[]
for gait in ['trotting','reactive']:
 tf.reset_default_graph()
 logdir=Path(pybullet_data.getDataPath())/'policies/ppo'/('minitaur_'+gait+'_env')
 cfg=utility.load_config(str(logdir))
 env=cfg.env(render=False)
 config=tf.ConfigProto(intra_op_parallelism_threads=2,inter_op_parallelism_threads=1,device_count={'GPU':0})
 with tf.Session(config=config) as sess:
  agent=simple_ppo_agent.SimplePPOPolicy(sess,env,cfg.network,policy_layers=cfg.policy_layers,value_layers=cfg.value_layers,checkpoint=str(logdir/'model.ckpt-14000000'))
  for seed in range(5):
   env.seed(seed)
   obs=env.reset()
   sess.run(agent.last_state.initializer)
   initial=np.array(env.minitaur.GetBasePosition())
   trace=[];total=0.
   for i in range(1000):
    action=agent.get_action([obs])[0]
    obs,reward,done,info=env.step(action)
    pos=np.array(env.minitaur.GetBasePosition())
    t=float(env.minitaur.GetTimeSinceReset())
    total+=reward
    trace.append([i+1,t,*pos,float(reward),*map(float,obs),*map(float,action)])
    if done:break
   a=np.array(trace)
   assert np.isfinite(a).all()
   displacement=float(a[-1,2]-initial[0]);duration=float(a[-1,1])
   result={'gait':gait,'seed':seed,'steps':len(a),'time_s':duration,'distance_x_m':displacement,'mean_forward_speed_m_s':displacement/duration,'reward':total,'ended_before_1000_steps':len(a)<1000,'final_height_m':float(a[-1,4]),'policy_layers':list(cfg.policy_layers),'value_layers':list(cfg.value_layers)}
   all_results.append(result)
   with (OUT/f'{gait}-seed{seed}.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['step','time_s','x_m','y_m','z_m','reward']+['observation_'+str(j) for j in range(len(obs))]+['action_'+str(j) for j in range(len(action))]);w.writerows(a)
   print(json.dumps(result),flush=True)
 env.close()
summary={}
for gait in ['trotting','reactive']:
 r=[x for x in all_results if x['gait']==gait];v=np.array([x['mean_forward_speed_m_s'] for x in r])
 summary[gait]={'mean_speed_m_s':float(v.mean()),'sd_speed_m_s':float(v.std(ddof=1)),'completed_1000_steps':sum(not x['ended_before_1000_steps'] for x in r),'n':len(r),'published_simulation_speed_m_s':.50 if gait=='trotting' else 1.34,'paper_checkpoint_matched':False}
(OUT/'summary.json').write_text(json.dumps({'status':'adapted_run','episodes':all_results,'summary':summary,'elapsed_seconds':time.time()-start,'limitations':['Released network sizes differ from paper Table II; modern PyBullet engine also differs.','Measured mean episode speed includes startup and differs from unspecified steady-state paper-speed estimator.','No physical evaluation or reproduction of paper population of trained controllers.']},indent=2)+'\n')
print(json.dumps(summary,indent=2))
