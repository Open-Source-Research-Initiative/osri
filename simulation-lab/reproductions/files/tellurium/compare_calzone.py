"""Compare selected Figure4B Wee1c points with executed author COMBINE output.
Original OSRI comparison wrapper, MIT; digitized paper data attributed separately.
"""
from pathlib import Path
import argparse,json
import numpy as np
parser=argparse.ArgumentParser();parser.add_argument('--run',type=Path,required=True);parser.add_argument('--reference',type=Path,default=Path(__file__).with_name('paper-figure4b-wee1c-digitized.csv'));parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
a=np.load(args.run/'raw-results.npz');ref=np.genfromtxt(args.reference,delimiter=',',names=True)
t=np.asarray(a['plot_0_0_0']).reshape(-1);y=np.asarray(a['plot_0_0_1']).reshape(-1);observed=np.interp(ref['time'],t,y);error=observed-ref['Wee1c'];rmse=float(np.sqrt(np.mean(error**2)));max_abs=float(np.max(np.abs(error)))
args.output.mkdir(parents=True,exist_ok=True)
np.savetxt(args.output/'comparison-points.csv',np.column_stack((ref['time'],ref['Wee1c'],observed,error)),delimiter=',',header='time_model_units,paper_digitized_Wee1c,computed_Wee1c,error',comments='')
np.savetxt(args.output/'figure4b-traces.csv',np.column_stack([np.asarray(a[k]).reshape(-1) for k in ['plot_0_0_0','plot_0_0_1','plot_0_1_1','plot_0_2_1','plot_0_3_1']]),delimiter=',',header='time_model_units,Wee1c,MPFc,StgPc,CycBT',comments='')
record={'target':'Figure4B Wee1c at10 preselected times','reference_points':len(ref),'rmse':rmse,'max_abs':max_abs,'bounds':{'rmse':.03,'max_abs':.06},'passed':bool(rmse<=.03 and max_abs<=.06),'declared_before_run':True,'scope':'Selected10-point Figure4B Wee1c raster trace, not all6panels, original BIOCHAM result or biological validation.','checks':{'all_21_data_generators_finite':len(a.files)==21 and all(np.isfinite(a[k]).all() for k in a.files),'time1_1001_samples_0_to250':len(t)==1001 and float(t[0])==0 and float(t[-1])==250,'time2_1001_samples_0_to180':np.asarray(a['plot_2_0_0']).size==1001 and float(np.max(a['plot_2_0_0']))==180},'human_scientific_review':'pending'}
(args.output/'comparison.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
