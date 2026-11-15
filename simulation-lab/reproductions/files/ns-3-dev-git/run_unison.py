"""Execute author Table2 settings; model source remains unchanged."""
from pathlib import Path
import subprocess,time,json
root=Path(__file__).resolve().parent
out=root/'ns3-output';out.mkdir(exist_ok=False)
records=[]
def run(mode,cluster,threads=None,suffix=''):
 binary=root/'unison'/('build' if mode=='unison' else 'build-default')/'scratch/ns3.36.1-fat-tree-optimized'
 args=[str(binary),'--k=4',f'--cluster={cluster}','--delay=500000','--bandwidth=100Mbps','--buffer=100p','--ecn=false','--flow=false','--tcp=ns3::TcpNewReno','--size=500','--load=0.7','--incast=0.1',f'--victim={"-".join(str(4*cluster-i-1) for i in range(4))}','--time=5','--interval=0','--flowmon=true']
 if threads is not None:args.append(f'--thread={threads}')
 name=f'{mode}-cluster{cluster}'+(f'-thread{threads}' if threads is not None else '')+suffix
 start=time.monotonic()
 with (out/(name+'.log')).open('w') as stdout,(out/(name+'-time.log')).open('w') as stderr:
  p=subprocess.run(['/usr/bin/time','-v']+args,cwd=root/'unison',stdout=stdout,stderr=stderr,timeout=180)
 record={'name':name,'argv':args,'cwd':'unison','exit_code':p.returncode,'elapsed_seconds':time.monotonic()-start};records.append(record);(out/'commands.json').write_text(json.dumps(records,indent=2)+'\n');assert p.returncode==0
for cluster in [2,4]:
 run('unison',cluster,cluster);run('default',cluster)
for threads in [1,4]:run('unison',2,threads)
run('unison',2,2,'-repeat')
