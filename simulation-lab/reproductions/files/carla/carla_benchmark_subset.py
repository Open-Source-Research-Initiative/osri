from pathlib import Path
import sys,json,time,math
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'sources/driving-benchmarks'))
from version084.driving_benchmarks import CoRL2017
from version084.benchmark_tools.benchmark_runner import BenchmarkRunner
from version084.benchmark_tools.agent import ForwardAgent
from version084.carla.client import make_carla_client
class CPUCoRLSubset(CoRL2017):
 def build_experiments(self):
  ex=super().build_experiments()[0]
  ex.Poses=ex.Poses[:3]
  ex.Conditions._sensors=[]
  ex.Conditions.set(SynchronousMode=True,SeedVehicles=42,SeedPedestrians=42)
  return [ex]
suite=CPUCoRLSubset('Town01')
runner=BenchmarkRunner(city_name='Town01',name_to_save='headless-corl2017-subset',save_images=False)
start=time.time()
with make_carla_client('localhost',2000,timeout=40) as client:
 metrics=runner.benchmark_agent(suite,ForwardAgent(),client)
summary={'status':'adapted_run','experiment':'First3 Town01 straight-route CoRL2017 pose pairs, first training weather','agent':'Authors ForwardAgent, not original MP/IL/RL policies','metrics':metrics,'raw_output':runner.get_path(),'elapsed_seconds':time.time()-start,'changes':['Removed camera sensor because -nullrhi provides physics only','Selected first3 pose pairs and one weather from author suite','Applied PEP479 generator-return compatibility patch']}
(ROOT/'carla-output/benchmark-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
