#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Bounded author-input construction, never an optimization or paper result."""
import argparse,json,time,resource,signal,traceback,sys
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--model-directory',type=Path,required=True,help='Extracted archive directory containing create_input.py and model/');parser.add_argument('--glpsol',type=Path);parser.add_argument('--memory-gib',type=int,default=12);parser.add_argument('--wall-seconds',type=int,default=1200);parser.add_argument('--output',type=Path,default=Path('resource-check'))
a=parser.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
resource.setrlimit(resource.RLIMIT_AS,(a.memory_gib*1024**3,a.memory_gib*1024**3))
def expired(signum,frame):raise TimeoutError('Declared process wall-time cap reached')
signal.signal(signal.SIGALRM,expired);signal.alarm(a.wall_seconds);start=time.monotonic()
report={'scope':'Author input-construction resource check only. No solver runs on the study model.','address_space_cap_gib':a.memory_gib,'wall_cap_seconds':a.wall_seconds,'solver_run_on_study_model':False,'native_inputs_persisted':False,'stages':[]}
def save(stage):
 report['stages'].append({'stage':stage,'elapsed_seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss});(out/'resource-check.json').write_text(json.dumps(report,indent=2,default=int)+'\n');print(stage,flush=True)
exit_code=0
try:
 import calliope
 from calliope.core.model import Model
 from pyomo.opt import SolverFactory
 import pyomo.environ
 if a.glpsol:report['glpk_available_to_author_pyomo']=bool(SolverFactory('glpk',executable=str(a.glpsol.resolve())).available(False))
 original=Model._init_from_model_run
 def measured(self,model_run,debug):
  report['source_set_counts']={k:len(v)for k,v in model_run['sets'].items()};save('author_yaml_preprocessing_complete');return original(self,model_run,debug)
 Model._init_from_model_run=measured
 scenario='industry_fuel_shared,transport,heat,config_overrides,res_2h,gas_storage,link_cap_dynamic,freeze-hydro-capacities,add-biofuel'
 save('constructing_original_inputs')
 model=calliope.Model(str(a.model_directory.resolve()/'model/eurospores/model-2018.yaml'),scenario=scenario)
 model.to_netcdf(str(out/'baseline-inputs.nc'));report['native_inputs_persisted']=True;save('native_inputs_persisted');report['status']='input_construction_completed_without_optimization'
except BaseException as error:
 report['status']='attempted_blocked';report['exception_type']=type(error).__name__;report['exception']=str(error);traceback.print_exc();exit_code=2
finally:
 report['elapsed_seconds']=time.monotonic()-start;report['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;(out/'resource-check.json').write_text(json.dumps(report,indent=2,default=int)+'\n');print(json.dumps(report,indent=2,default=int),flush=True)
sys.exit(exit_code)
