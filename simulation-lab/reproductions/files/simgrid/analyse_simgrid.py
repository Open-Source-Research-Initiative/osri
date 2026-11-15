from pathlib import Path
import json,csv,statistics,re
root=Path(__file__).resolve().parent
# Extract SimGrid performance endpoints with repetition-level observations and summary.
sg=json.loads((root/'simgrid-output/comparison.json').read_text());summaries=[]
# Author driver measures GNU time's elapsed field; keep wrapper overhead separately.
for run in sg['runs']:
    raw=(root/run['path']/'stderr.log').read_text()
    match=re.search(r'Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([\d:.]+)',raw)
    assert match,run['path']
    tokens=match.group(1).split(':')
    run['native_elapsed_seconds']=float(tokens[-1])+60*float(tokens[-2])+(3600*float(tokens[-3]) if len(tokens)==3 else 0)
    run['harness_elapsed_seconds']=run['elapsed_seconds']
sg['timing_observable']='Primary timing is native /usr/bin/time -v elapsed, as author run_experiments.py extracts. Python subprocess wrapper elapsed is retained separately and is not the paper metric.'

for tasks in [4000,60000]:
 pair={v:[x for x in sg['runs'] if x['tasks']==tasks and not x['validation_logging'] and x['version']==v] for v in ['3.10','3.36']}
 for v,runs in pair.items():
  times=[x['native_elapsed_seconds'] for x in runs];rss=[x['max_rss_kib'] for x in runs]
  summaries.append({'tasks':tasks,'version':v,'repetitions':len(runs),'elapsed_mean_seconds':statistics.mean(times),'elapsed_min_seconds':min(times),'elapsed_max_seconds':max(times),'elapsed_sample_sd_seconds':statistics.stdev(times),'max_rss_mean_kib':statistics.mean(rss),'max_rss_min_kib':min(rss),'max_rss_max_kib':max(rss)})
sg['performance_summaries']=summaries;sg['local_ratios']=[]
for tasks in [4000,60000]:
 a,b=[next(x for x in summaries if x['tasks']==tasks and x['version']==v) for v in ['3.10','3.36']]
 sg['local_ratios'].append({'tasks':tasks,'mean_wall_time_ratio_3_10_over_3_36':a['elapsed_mean_seconds']/b['elapsed_mean_seconds'],'mean_rss_ratio_3_10_over_3_36':a['max_rss_mean_kib']/b['max_rss_mean_kib'],'paper_reported_min_rss_ratio':4.1,'paper_rss_bound_observed_locally':a['max_rss_mean_kib']/b['max_rss_mean_kib']>=4.1,'historical_hardware_speedup_reproduced':False})
(root/'simgrid-output/comparison.json').write_text(json.dumps(sg,indent=2)+'\n')
with (root/'simgrid-output/performance-summary.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(summaries[0]));w.writeheader();w.writerows(summaries)
perf=[{k:r[k] for k in ['version','hosts','cores_per_host','tasks','seed','native_elapsed_seconds','harness_elapsed_seconds','max_rss_kib','cpu_affinity']} for r in sg['runs'] if not r['validation_logging']]
with (root/'simgrid-output/performance-replications.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(perf[0]));w.writeheader();w.writerows(perf)
print(json.dumps({'makespan_checks_passed':sg['makespan_checks_passed'],'local_ratios':sg['local_ratios']},indent=2))
