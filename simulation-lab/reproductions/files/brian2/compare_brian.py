"""Recompute exploratory raster-reference comparison. Original OSRI code, MIT.
Uses data exported by run_brian_historical.py and digitized-v2 reference.
"""
from pathlib import Path
import argparse,json
import numpy as np
parser=argparse.ArgumentParser();parser.add_argument('--run',type=Path,required=True);parser.add_argument('--reference',type=Path,default=Path(__file__).with_name('paper-figure3b-digitized-v2.csv'));parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
a=np.load(args.run/'trajectories.npz');ref=np.genfromtxt(args.reference,delimiter=',',names=True)
metrics={};columns=[ref['time_seconds']];names=['time_seconds']
for field,label in [('eye','eye_position'),('object','object_position')]:
 observed=np.interp(ref['time_seconds'],a['t_seconds'],a[field]);error=observed-ref[label]
 metrics[field]={'rmse':float(np.sqrt(np.mean(error**2))),'max_abs':float(np.max(np.abs(error))),'within_exploratory_bounds':bool(np.sqrt(np.mean(error**2))<=.08 and np.max(np.abs(error))<=.15)}
 columns += [ref[label],observed,error];names += ['paper_'+field,'computed_'+field,field+'_error']
args.output.mkdir(parents=True,exist_ok=True)
np.savetxt(args.output/'comparison-points.csv',np.column_stack(columns),delimiter=',',header=','.join(names),comments='')
record={'scope':'Exploratory Figure3b raster comparison only','points':len(ref),'metrics':metrics,'passed':all(m['within_exploratory_bounds'] for m in metrics.values()),'declared_before_first_run':False,'protocol_note':'Tolerances and image ROI were refined after prior modern output and a first historical run existed; the initial failed legend-contaminated extraction is retained. A later deterministic repeat is not a new prospective study.','paper_source_correction':'Published figure and author notebook both use tau_object500ms; initial50ms transcription was corrected.','human_scientific_review':'pending'}
(args.output/'comparison.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
