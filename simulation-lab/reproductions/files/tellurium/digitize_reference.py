"""Extract selected Figure4B Wee1c paper pixels, fixed original calibration."""
from pathlib import Path
import csv,hashlib,json
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parent
# Choose smooth Wee1c trace at the original preselected times.
a=np.asarray(Image.open(root/'calzone-figure4.png').convert('RGB'))
rows=[]
for t in [25,50,75,100,125,145,180,200,220,240]:
 x=int(round(2031+3.196*t));roi=a[360:790,x].astype(int)
 blue=(roi[:,0]<70)&(roi[:,1]>80)&(roi[:,1]<155)&(roi[:,2]>145)&(roi[:,2]<220)
 ys=np.where(blue)[0]+360
 # Legend begins x>2850; all sampled x are in plot. Near steep points, use median visible line pixels.
 if len(ys):rows.append([t,(790-float(np.median(ys)))/370,x,float(np.median(ys))])
with (root/'paper-figure4b-wee1c-digitized.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['time','Wee1c','pixel_x','pixel_y']);w.writerows(rows)
record={'source':'https://journals.plos.org/ploscompbiol/article/figure/image?size=large&id=10.1371/journal.pcbi.1006220.g004','source_sha256':hashlib.sha256((root/'calzone-figure4.png').read_bytes()).hexdigest(),'target':'Figure4B blue Wee1c trace only','calibration':{'x_time0':2031,'x_time250':2830,'y_zero':790,'y_one':420},'sample_times':[r[0] for r in rows],'tolerance':{'rmse_at_most':0.03,'max_abs_at_most':0.06},'basis':'Original PNG line about3-4pixels thick,370pixels per concentration unit; tolerance includes calibration, compression, time-pixel error and deterministic solver change. More generous max allowance near transients. Chosen before any Tellurium model execution.','declared_before_run':True,'limitations':['Comparison covers selected Wee1c points in Figure4B, not all6panels.','Manual plot calibration needs human scientific review.']}
(root/'digitization-protocol.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
