from pathlib import Path
import os,runpy,sys
ROOT=Path(__file__).resolve().parent
(ROOT/'scratch').mkdir(exist_ok=True)
os.environ['CLOUD_ML_HP_METRIC_FILE']=str(ROOT/'scratch/hypertune.metrics')
os.environ.setdefault('OMP_NUM_THREADS','2');os.environ.setdefault('TF_NUM_INTRAOP_THREADS','2');os.environ.setdefault('TF_NUM_INTEROP_THREADS','1')
if hasattr(os,'sched_setaffinity'):os.sched_setaffinity(0,sorted(os.sched_getaffinity(0))[:2])
sys.path.insert(0,str(ROOT/'runtime'));sys.path.insert(0,str(ROOT/'sources/kubric'))
worker=ROOT/'sources/kubric/examples/movi/movi_ab_worker.py'
sys.argv=[str(worker),'--objects_set=clevr','--background=clevr','--camera=clevr','--seed=42','--job-dir='+str(ROOT/'output'),'--scratch_dir='+str(ROOT/'scratch'),'--save_state']
runpy.run_path(str(worker),run_name='__main__')
