"""Export maintained-model outputs; diagnostics do not verify a paper target."""
from pathlib import Path
from scipy.io import loadmat
import numpy as np
import json,csv
r=Path(__file__).resolve().parent
d=loadmat(r/'model-outputs.mat',simplify_cells=True);oo=d['oo_'];x=oo['shock_decomposition'];yi=list(d['M_']['endo_names']).index('y');series=x[yi]
with (r/'output-decomposition-y.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['observation']+list(d['M_']['exo_names'])+['initial_conditions','total']);w.writerows([i+1]+list(series[:,i]) for i in range(series.shape[1]))
result={'status':'author_code_executed','exit_code':0,'dynare_version':oo['dynare_version'],'octave_version':'9.4.0','statistics_version':'1.7.7','mh_replic':float(d['options_']['mh_replic']),'mode_compute':float(d['options_']['mode_compute']),'first_obs':float(d['options_']['first_obs']),'observations':int(d['options_']['nobs']),'shock_decomposition_shape':list(x.shape),'shock_decomposition_all_finite':bool(np.isfinite(x).all()),'max_abs_output_decomposition_sum_residual':float(np.abs(series[:-1].sum(axis=0)-series[-1]).max()),'laplace_log_data_density':float(oo['MarginalDensity']['LaplaceApproximation']),'scope':'Maintained author-derived model at supplied old mode; no optimization or MCMC. Original author archive requires login, so original sample/mode and printed paper targets not matched.','warnings':['Old mode file cannot be verified against current model.','gaminv prior-bound calculation did not converge for some values.','Negative array dimensions converted to zero in shock-decomposition setup.','33 preprocessor warnings from unassigned steady-state block variables.'],'interpretation':'Fresh model execution and finite native decomposition achieved, with exploratory summation diagnostic. No published-target comparison, posterior estimation, scientific acceptance or original-paper reproduction claimed.'}
(r/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps(result,indent=2))
