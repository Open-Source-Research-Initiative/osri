"""Fresh paired SS solves using author archived public calibration/fits, no PUF."""
from pathlib import Path
import runpy,os,sys,json,pickle,time,shutil
import numpy as np
root=Path(__file__).resolve().parent;src=root/'source';sys.path.insert(0,str(src))
target={'declared_before_run':True,'paper_version':'May 2018 author manuscript DEP_TaxFuncs.pdf at pinned replication commit; not independently matched to final 2019 journal version','locator':'Table 7/8, steady-state GDP percent change, ratio of polynomials varying by age and income source','observable':'100*(Y_TCJA/Y_2017law-1) from freshly solved macro steady states using supplied fitted tax functions','reference':0.07,'tolerance':0.005,'units':'percentage points','tolerance_basis':'Half of the reported 0.01 percentage point precision, fixed before paired solve.','scope':'Macro steady-state stage only; Tax-Calculator PUF microsimulation and transition paths are not rerun.'}
(root/'pair-target.json').write_text(json.dumps(target,indent=2)+'\n')
start=time.monotonic();runpy.run_path(str(root/'run_fitted_ss.py'),run_name='__main__')
from ogusa import SS
p=pickle.load(open(src/'OUTPUT_REFORM/_DEP_Age/model_params.pkl','rb'),encoding='latin1')
p['tax_func_type']='DEP';p['output_dir']=str(root/'pair-output/reform');p['run_params']={k:v for k,v in p.items() if k!='run_params'}
base=root/'pair-output/baseline/SS';base.mkdir(parents=True,exist_ok=True);shutil.copy2(str(root/'output/SS_vars.pkl'),str(base/'SS_vars.pkl'))
args=SS.create_steady_state_parameters(**p)
result=SS.run_SS(*args,baseline=False,baseline_spending=False,baseline_dir=str(root/'pair-output/baseline'),client=None,num_workers=1)
(root/'pair-output/reform').mkdir(parents=True,exist_ok=True)
with open(root/'pair-output/reform/SS_vars.pkl','wb') as f:pickle.dump(result,f)
b=pickle.load(open(base/'SS_vars.pkl','rb'));actual=float(100*(b['Yss']/result['Yss']-1));error=abs(actual-target['reference'])
reference=pickle.load(open(src/'OUTPUT_REFORM/_DEP_Age/SS/SS_vars.pkl','rb'),encoding='latin1')
out={'status':'author_code_executed','elapsed_seconds':time.monotonic()-start,'observable':target['observable'],'reference_percentage_points':0.07,'actual_percentage_points':actual,'absolute_error_percentage_points':error,'tolerance_percentage_points':0.005,'passed':bool(error<=0.005),'baseline_Y_TCJA':float(b['Yss']),'counterfactual_Y_2017law':float(result['Yss']),'counterfactual_Y_archive':float(reference['Yss']),'counterfactual_Y_archive_error':abs(float(result['Yss'])-float(reference['Yss'])),'max_abs_reform_euler_savings':float(np.abs(result['euler_savings']).max()),'max_abs_reform_euler_labor_leisure':float(np.abs(result['euler_labor_leisure']).max()),'reform_resource_constraint_error':float(result['Yss']-result['Css']-result['Iss']-result['Gss']),'scope':target['scope'],'paper_version':target['paper_version'], 'baseline_government_spending':float(b['Gss']), 'counterfactual_government_spending':float(result['Gss']), 'economic_feasibility_passed':bool(b['Gss']>=0 and result['Gss']>=0), 'feasibility_note':'Author solver warns negative government spending under the target debt closure; a numeric table match does not establish economic feasibility.'}
(root/'pair-results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps(out,indent=2))
