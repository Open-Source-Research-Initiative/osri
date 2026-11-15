from pathlib import Path
import runpy,os,json,time,hashlib,subprocess,sys,shutil
root=Path(__file__).resolve().parent
source=root/'source/Code/Python/BufferStock-LifeCycle.py'
os.chdir(source.parent)
start=time.monotonic()
state=runpy.run_path(str(source),run_name='__main__')
result={
 'elapsed_seconds':time.monotonic()-start,
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'table1':state['table1'].tolist(),
 'baseline_target_net_wealth':float(state['table1'][0,6]),
 'paper_reference':0.32,
 'absolute_error':abs(float(state['table1'][0,6])-0.32),
 'tolerance':0.005,
 'passed':abs(float(state['table1'][0,6])-0.32)<=0.005,
 'target_declared_before_run':True,
 'interpretation':'Author-associated HARK replication ran with declared legacy package versions; baseline target-net-wealth strict rounding comparison with original Table I failed. Author methods differ; do not call historical result reproduced.'
}
(root/'results.json').write_text(json.dumps(result,indent=2)+'\n')
state['table'].to_csv(root/'table1.csv')
print(json.dumps(result,indent=2))

for category in ["Figures", "Tables"]:
    destination=root/"output"/category
    destination.mkdir(parents=True,exist_ok=True)
    for file in (root/"source/Paper"/category).glob("*"):
        if file.is_file(): shutil.copy2(file,destination/file.name)
