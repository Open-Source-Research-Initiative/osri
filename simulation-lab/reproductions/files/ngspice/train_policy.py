# SPDX-License-Identifier: MIT
"""Bounded execution of the authors' public PPO training configuration.

64x64 network and default PPO settings follow public source; this differs from
the article's stated3x50 architecture. Circuit and reward remain unchanged.
"""
import os,sys,time,json,random
from pathlib import Path
from author_runtime import ROOT, TwoStageAmp
import numpy as np
import gym
import ray
from ray.rllib.agents import ppo
import tensorflow as tf

class WorkspaceEnv(TwoStageAmp):
    def __init__(self, config):
        import author_runtime  # Apply workspace/logging adapter in EVERY Ray worker.
        worker_seed=int(os.environ.get('AUTOCKT_SEED','100'))+getattr(config,'worker_index',0)
        random.seed(worker_seed);np.random.seed(worker_seed);tf.set_random_seed(worker_seed)
        super(WorkspaceEnv,self).__init__(config)
        # Correct metadata only: author's returned vector values are unchanged.
        # Upstream declares param indices fixed1 and normalized specs[-1,0],
        # although reset returns indices33 and positive normalized specs.
        self.observation_space=gym.spaces.Box(low=np.array([-1.0]*8+[0.0]*7,dtype=np.float32),high=np.array([1.0]*8+[98.0]*7,dtype=np.float32))

seed=int(os.environ.get('AUTOCKT_SEED','100'));random.seed(seed);np.random.seed(seed);tf.set_random_seed(seed)
output=ROOT/('training-seed'+str(seed));output.mkdir(exist_ok=True)
started=time.time();limit=int(os.environ.get('AUTOCKT_TRAIN_SECONDS','600'));iterations=int(os.environ.get('AUTOCKT_TRAIN_ITERATIONS','30'))
ray.init(num_cpus=7,num_gpus=0,object_store_memory=200000000,redis_max_memory=100000000,include_webui=False,temp_dir=os.environ.get('AUTOCKT_RAY_TMP','/workspace/tmp/builderbob/ac1115'),plasma_directory=str(ROOT/'tmp'))
config={'train_batch_size':1200,'horizon':30,'num_gpus':0,'model':{'fcnet_hiddens':[64,64]},'num_workers':6,'env_config':{'generalize':True,'run_valid':False}}
try:
    from ray.tune.logger import UnifiedLogger
    agent=ppo.PPOAgent(config=config,env=WorkspaceEnv,logger_creator=lambda cfg: UnifiedLogger(cfg,str(output)))
    for i in range(iterations):
        result=agent.train()
        with (output/'results.jsonl').open('a') as f:f.write(json.dumps(result,default=str)+'\n')
        checkpoint=agent.save(str(output))
        compact={'iteration':i+1,'episode_reward_mean':result.get('episode_reward_mean'),'timesteps_total':result.get('timesteps_total'),'episodes_total':result.get('episodes_total'),'seconds':time.time()-started,'checkpoint':checkpoint}
        print(json.dumps(compact),flush=True)
        (output/'latest.json').write_text(json.dumps(compact,indent=2)+'\n')
        if result.get('episode_reward_mean',-999)>=-.02:break
        if time.time()-started>limit:break
    (output/'configuration.json').write_text(json.dumps(config,indent=2)+'\n')
finally:
    ray.shutdown()
