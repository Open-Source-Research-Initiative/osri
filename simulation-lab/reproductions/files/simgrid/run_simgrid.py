"""Run author coordinator-worker code; binaries must be built as in build-network-tools.sh."""
from pathlib import Path
import subprocess,os,time,json,re,hashlib,shutil,csv
root=Path(__file__).resolve().parent
output=root/'simgrid-output';output.mkdir(exist_ok=True)
# Keep each measured subprocess on one CPU; this affects only this harness and children.
available=sorted(os.sched_getaffinity(0));os.sched_setaffinity(0,{available[0]})
env=os.environ.copy()
# Optional compiler-matched dependency prefix; equivalent to BOOST_ROOT used at build.
dependency_prefix=os.environ.get('SIMGRID_DEPENDENCY_PREFIX',os.environ.get('BOOST_ROOT',''))
if dependency_prefix:env['LD_LIBRARY_PATH']=str(Path(dependency_prefix)/'lib')+(':'+env['LD_LIBRARY_PATH'] if env.get('LD_LIBRARY_PATH') else '')
results=[]
def one(version,hosts,tasks,seed,logging):
 name=f'v{version}-hosts{hosts}-tasks{tasks}-seed{seed}'+('-validation' if logging else '-performance');dest=output/name;dest.mkdir(exist_ok=False)
 args=[str(root/f'coordinator-workspace-v{version}'),str(hosts),'4','100','200','100','100','200','10',str(tasks),'100','100','100','100',str(seed)]
 if version!='3.10':args+=['--cfg=plugin:host_energy']
 if not logging:args+=['--log=root.thresh:critical']
 start=time.monotonic()
 with (dest/'stdout.log').open('w') as stdout,(dest/'stderr.log').open('w') as stderr:
  proc=subprocess.run(['/usr/bin/time','-v']+args,cwd=root,env=env,stdout=stdout,stderr=stderr,timeout=180)
 elapsed=time.monotonic()-start;log=(dest/'stderr.log').read_text()
 m=re.search(r'\s([0-9]+\.[0-9]+)\].*ALL DONE',log)
 if m is None:m=re.search(r':\([^)]*\) ([0-9]+\.[0-9]+)\].*ALL DONE',log)
 rss=re.search(r'Maximum resident set size \(kbytes\): (\d+)',log)
 row={'version':version,'hosts':hosts,'cores_per_host':4,'tasks':tasks,'seed':seed,'validation_logging':logging,'exit_code':proc.returncode,'elapsed_seconds':elapsed,'max_rss_kib':int(rss.group(1)) if rss else None,'makespan_seconds':float(m.group(1)) if m else None,'cpu_affinity':[available[0]],'argv':args,'path':str(dest.relative_to(root))}
 (dest/'run.json').write_text(json.dumps(row,indent=2)+'\n')
 if logging:
  for f in (root/'tmp').glob('platform_master_worker*.xml'):shutil.copy2(f,dest/f.name)
 results.append(row);print(json.dumps(row),flush=True)
 (output/'runs.json').write_text(json.dumps(results,indent=2)+'\n')
 assert proc.returncode==0
for seed in range(3):
 for version in ['3.10','3.36']:one(version,4,40,seed,True)
# Paper Figure13 lower/upper anchor workloads; original 10-repeat seed range.
for tasks in [4000,60000]:
 for seed in range(10):
  for version in ['3.10','3.36']:one(version,1000,tasks,seed,False)
# Native makespan comparison on the paper lower anchor (outside timed measurement).
for version in ['3.10','3.36']:one(version,1000,4000,0,True)
comparisons=[]
for hosts,tasks,seeds in [(4,40,range(3)),(1000,4000,[0])]:
 for seed in seeds:
  pair=[next(x for x in results if x['version']==v and x['hosts']==hosts and x['tasks']==tasks and x['seed']==seed and x['validation_logging']) for v in ['3.10','3.36']]
  assert all(x['makespan_seconds'] is not None for x in pair)
  delta=abs(pair[1]['makespan_seconds']-pair[0]['makespan_seconds']);comparisons.append({'hosts':hosts,'tasks':tasks,'seed':seed,'v3_10_makespan':pair[0]['makespan_seconds'],'v3_36_makespan':pair[1]['makespan_seconds'],'absolute_difference':delta,'tolerance_seconds':1e-6,'passed':delta<=1e-6})
summary={'author_commit':'b09453d19541b7186703f4d651c1bba790461e44','simgrid_commits':{'3.10':'9a82cac1b6f73bb342495c39807acd7380e153d5','3.36':'7ed73b43153fc79a8c5eb5cff8e9f81e4f52e619'},'source_changes':'Only two hardcoded /tmp XML paths moved under run directory. Author Dockerfile CMake workaround used for3.10.','comparison_scope':'Figure13 lower/upper workload anchors,10 repeats; intermediate sweep points and exact historical CPU/compiler are not reproduced. Native makespan consistency checked separately.','runs':results,'makespan_comparisons':comparisons,'makespan_checks_passed':all(c['passed'] for c in comparisons)}
(output/'comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
