#!/usr/bin/env python3
"""Run one unchanged author AFEM Figure2(a) case and compare printed targets."""
import argparse, importlib.util, hashlib, json, os, sys, time
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
source=args.source.resolve();output=args.output.resolve();output.mkdir(parents=True,exist_ok=True)
script=source/'case_poisson_riviere/solve_riviere.py'
record={'tool_id':'dolfinx','status':'attempted_blocked','author_source_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'target':{'reference':'arXiv:2410.09764v1 Section4.1 Figure2(a), contrast5 k1 m2','rateuh1':0.50,'ieff':1.06,'absolute_tolerance':0.005,'tolerance_basis':'Half last printed unit at two decimals; tests reporting-precision agreement only.'},'inputs':{'order_prime':1,'order_eqlb':2,'nref':20,'doerfler':0.5,'ratio_k':5},'comparison':{'performed':False,'passed':None},'human_scientific_review':'pending'}
(output/'declared-run.json').write_text(json.dumps(record,indent=2)+'\n')
start=time.monotonic()
try:
 os.chdir(output)
 spec=importlib.util.spec_from_file_location('author_riviere',script);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 module.adaptive_solver(1,2,20,0.5,5)
 import numpy as np
 csvs=list(output.glob('*.csv'));assert len(csvs)==1
 values=np.loadtxt(csvs[0],delimiter=',');last=values[-1]
 measures={'rows':len(values),'elements':float(last[0]),'ndofs':float(last[1]),'energy_error':float(last[2]),'rateuh1':float(last[3]),'estimator':float(last[4]),'ieff':float(last[6])}
 checks={key:abs(measures[key]-record['target'][key])<=0.005 for key in ['rateuh1','ieff']}
 record.update(status='target_compared',comparison={'performed':True,'passed':all(checks.values()),'measurements':measures,'checks':checks,'interpretation':'One author-code preprint parameter combination; comparison uses rounded printed reference values, with human scientific review pending.'})
except Exception as e:
 import traceback
 record['failure']=repr(e);traceback.print_exc()
finally:
 record['elapsed_seconds']=time.monotonic()-start
 record['outputs']=[{'path':str(p.relative_to(output)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in output.iterdir() if p.is_file() and p.suffix in ['.csv','.h5','.xdmf']]
 (output/'run-record.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
 if record['status']=='attempted_blocked':sys.exit(1)
