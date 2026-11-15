#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Run a bounded real LuST city model; no paper validation is asserted."""
import argparse,os,subprocess,time,json,statistics,xml.etree.ElementTree as ET,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--sumo',type=Path,default=Path('build/bin/sumo'));p.add_argument('--scenario',type=Path,default=Path('LuSTScenario/scenario/dua.static.sumocfg'));p.add_argument('--runtime-lib',type=Path,default=Path('.runtime/lib'));p.add_argument('--output',type=Path,default=Path('run-output'));a=p.parse_args()
exe=a.sumo.resolve();config=a.scenario.resolve();base=a.output.resolve();base.mkdir(parents=True,exist_ok=True)
env=dict(os.environ);env['LD_LIBRARY_PATH']=str(a.runtime_lib.resolve())+((':'+env['LD_LIBRARY_PATH'])if env.get('LD_LIBRARY_PATH')else'')
records=[]
for seed in [42,43,44]:
 out=base/('seed'+str(seed));out.mkdir(exist_ok=True)
 argv=[str(exe),'-c',str(config),'--end','3600','--seed',str(seed),'--no-step-log','true','--duration-log.statistics','true','--xml-validation','never','--log',str(out/'run.log'),'--summary-output',str(out/'summary.xml'),'--tripinfo-output',str(out/'tripinfo.xml')]
 t=time.monotonic()
 with (out/'console.log').open('w')as log:result=subprocess.run(argv,env=env,stdout=log,stderr=subprocess.STDOUT)
 assert result.returncode==0,(out/'console.log').read_text()
 steps=ET.parse(out/'summary.xml').getroot().findall('step');trips=ET.parse(out/'tripinfo.xml').getroot().findall('tripinfo');durations=[float(row.attrib['duration'])for row in trips]
 assert steps[-1].attrib['time']=='3599.00'
 records.append({'seed':seed,'argv':argv,'exit_code':result.returncode,'elapsed_seconds':time.monotonic()-t,'summary_last_step':steps[-1].attrib,'completed_trip_rows':len(trips),'completed_trip_mean_duration_seconds':statistics.mean(durations),'completed_trip_duration_sd_seconds':statistics.stdev(durations)})
report={'status':'adapted_run','paper_doi':'10.1109/MITS.2017.2666585','source_commit':'5edb7ecb9ad196c39172b6eb95d19ed789f4b1a6','duration_seconds':3600,'runs':records,'mean_of_seed_means_seconds':statistics.mean(r['completed_trip_mean_duration_seconds']for r in records),'sd_of_seed_means_seconds':statistics.stdev(r['completed_trip_mean_duration_seconds']for r in records),'paper_validation_performed':False,'interpretation':'Whole author network and demand, bounded to first hour. Completed-trip durations are censored at3600s and cannot describe all trips/full-day travel times. Original2017 numeric target and observation data remain unavailable.'}
(base/'run-record.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
