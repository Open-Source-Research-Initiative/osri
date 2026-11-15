from pathlib import Path
from decimal import Decimal
import json,re,csv,statistics,hashlib,subprocess
root=Path(__file__).resolve().parent
ns=root/'ns3-output'
def parse(path):
 s=path.read_text();get=lambda key:re.search(re.escape(key)+r' = ([^\n]+)',s).group(1)
 return {'fct_us':get('Average FCT (all)').removesuffix('us'),'e2ed_us':get('Average end to end delay').removesuffix('us'),'throughput_gbps':get('Average flow throughput').removesuffix('Gbps'),'events':int(get('Event count')),'tx_packets':int(get('Total Tx packets')),'rx_packets':int(get('Total Rx packets')),'flow_count':int(get('Detected #flow')),'finished_flow_count':int(get('Finished #flow')),'wall_simulation_seconds':float(get('Simulation time').removesuffix('s'))}
references={'default_2':['650.89','15.14','6.81'],'unison_2':['632.52','15.03','6.99'],'default_4':['480.84','10.49','6.50'],'unison_4':['472.45','11.39','6.41']}
rows=[];checks=[]
for key,refs in references.items():
 mode,cluster=key.split('_');name=f'{mode}-cluster{cluster}'+(f'-thread{cluster}' if mode=='unison' else '')
 result=parse(ns/(name+'.log'));vals=[Decimal(result['fct_us'])/1000,Decimal(result['e2ed_us'])*2/1000,Decimal(result['throughput_gbps'])*1000]
 row={'simulator':mode,'cluster':int(cluster),'fct_ms':float(vals[0]),'rtt_ms':float(vals[1]),'throughput_mbps':float(vals[2]),**result};rows.append(row)
 for metric,observed,expected in zip(['fct_ms','rtt_ms','throughput_mbps'],vals,refs):
  diff=abs(observed-Decimal(expected));checks.append({'configuration':key,'metric':metric,'reference':float(expected),'observed':float(observed),'absolute_difference':float(diff),'tolerance':0.005,'passed':diff<=Decimal('0.005')})
with (ns/'table2-comparison.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=list(checks[0]));writer.writeheader();writer.writerows(checks)
with (root/'unison/results/accuracy-1115-2100.csv').open('w') as f:
 writer=csv.writer(f);writer.writerow(['program','simulator','cluster','core','fct','e2ed','throughput'])
 for row in rows:writer.writerow(['fat-tree',row['simulator'],row['cluster'],row['cluster'],row['fct_us'],row['e2ed_us'],row['throughput_gbps']])
proc=subprocess.run(['python3','process.py','2'],cwd=root/'unison',capture_output=True,text=True);(ns/'author-postprocess.log').write_text(proc.stdout+proc.stderr);assert proc.returncode==0
(root/'unison/results/2.csv').replace(ns/'author-table2.csv')
detfiles=['unison-cluster2-thread1','unison-cluster2-thread2','unison-cluster2-thread2-repeat','unison-cluster2-thread4'];det=[]
fields=['fct_us','e2ed_us','throughput_gbps','events','tx_packets','rx_packets','flow_count','finished_flow_count']
baseline={k:parse(ns/(detfiles[0]+'.log'))[k] for k in fields}
for name in detfiles:
 row=parse(ns/(name+'.log'));values={k:row[k] for k in fields};det.append({'run':name,'values':values,'matches_first_run':values==baseline})
report={'source_commit':'7b3274167615c55ae8d69f7edee4e2dc2d81f706','paper_identifier':'10.1145/3627703.3629574','paper_locator':'Section6.2, Table2; exact thread/result determinism paragraph after Figure11.','paper_url':'https://cs.nju.edu.cn/tianchen/lunwen/2024/eurosys24-final201.pdf','table_targets_declared_before_run':True,'table_comparison':checks,'table_checks_passed':all(c['passed'] for c in checks),'determinism':det,'determinism_passed':all(c['matches_first_run'] for c in det),'measurements':rows,'transforms':'Exactly authors process.py2: FCT=fct_us/1000; RTT=e2ed_us*2/1000; throughput=Gbps*1000.','claim_scope':'All12 table entries agree to the predeclared half-last-digit threshold. This does not independently establish validity of packet models, table uncertainty, other paper experiments or hardware speedups.','failed_attempts':['Initial GCC13 compile required -include cstdint; source unchanged.','0.05s diagnostic had no completed observed flow and NaN averages; preserved and excluded from comparison.','First sequential configure omitted Ninja PATH; corrected in isolated environment.']}
(ns/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['table_checks_passed'];assert report['determinism_passed']
print(json.dumps({'table_checks':len(checks),'table_passed':report['table_checks_passed'],'determinism_passed':report['determinism_passed']},indent=2))
