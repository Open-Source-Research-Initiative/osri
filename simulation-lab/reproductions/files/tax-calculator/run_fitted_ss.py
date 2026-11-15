"""Fresh author-code steady state using supplied calibrated/fitted inputs; no IRS PUF."""
from pathlib import Path
import os,sys,json,hashlib,pickle,time
import numpy as np
root=Path(__file__).resolve().parent;src=root/'source';sys.path.insert(0,str(src))
os.chdir(src)
from ogusa import SS
reference_path=src/'OUTPUT_BASELINE/_DEP_Age/SS/SS_vars.pkl'
params_path=src/'OUTPUT_BASELINE/_DEP_Age/model_params.pkl'
p=pickle.load(open(params_path,'rb'),encoding='latin1');ref=pickle.load(open(reference_path,'rb'),encoding='latin1')
keys=['Yss','Kss','Lss','rss','wss','Css']
target={'declared_before_run':True,'observable':'Baseline DEP_Age macro steady-state outputs under supplied public fitted tax functions','reference':{k:float(ref[k]) for k in keys},'relative_tolerance':1e-6,'absolute_tolerance':1e-8,'tolerance_basis':'Cross-platform numerical regression allowance chosen before the fresh solve; original solver has mindist_SS='+str(p['mindist_SS'])+'. Not a published scientific tolerance.','scope':'Fresh author SS solver from archived calibrated inputs, compared to author archive output. Does not rerun Tax-Calculator micro-estimation or paper transition paths; paper table identity not yet established.'}
(root/'target.json').write_text(json.dumps(target,indent=2)+'\n')
p['tax_func_type']='DEP';p['output_dir']=str(root/'output');p['run_params']={k:v for k,v in p.items() if k!='run_params'}
args=SS.create_steady_state_parameters(**p)
start=time.monotonic()
try:
 result=SS.run_SS(*args,baseline=True,baseline_spending=False,baseline_dir=str(root/'output'),client=None,num_workers=1)
 (root/'output').mkdir(exist_ok=True)
 with open(root/'output/SS_vars.pkl','wb') as f:pickle.dump(result,f)
 comparisons={k:{'reference':float(ref[k]),'actual':float(result[k]),'absolute_error':abs(float(result[k])-float(ref[k])),'passed':bool(np.isclose(result[k],ref[k],rtol=1e-6,atol=1e-8))} for k in keys}
 out={'elapsed_seconds':time.monotonic()-start,'exit_code':0,'status':'author_code_executed','comparison':comparisons,'all_compared_outputs_match':all(v['passed'] for v in comparisons.values()),'resource_constraint_error':float(result['Yss']-result['Css']-result['Iss']-result['Gss']), 'max_abs_euler_savings':float(np.abs(result['euler_savings']).max()), 'max_abs_euler_labor_leisure':float(np.abs(result['euler_labor_leisure']).max()),'scope':target['scope']}
 (root/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
except Exception as e:
 import traceback
 traceback.print_exc();(root/'results.json').write_text(json.dumps({'elapsed_seconds':time.monotonic()-start,'exit_code':1,'status':'attempted_blocked','exception':repr(e),'scope':target['scope']},indent=2)+'\n');raise
