"""Extract identified paper-figure line samples, with fixed pixel calibration.
Analysis of published figure pixels, not an edited image or a fitted model trace.
"""
from pathlib import Path
import csv,hashlib,json
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parent
# Brian Figure 3b: tick positions taken from original CDN JPEG. Author plot sets tickvals [-1,1].
a=np.asarray(Image.open(root/'brian-figure3.jpg').convert('RGB'))
rows=[]
for x in range(1080,1633,3):
 roi=a[425:497,x].astype(int)
 green=(roi[:,0]<105)&(roi[:,1]>85)&(roi[:,1]>roi[:,0]+30)&(roi[:,1]>roi[:,2]+30)
 black=(roi.max(axis=1)<85)&(roi.max(axis=1)-roi.min(axis=1)<25)&(np.arange(425,497)>=438)
 if green.any() and black.any():
  gy=float(np.median(np.where(green)[0]+425));by=float(np.median(np.where(black)[0]+425))
  rows.append([(x-1076)/55.9,(457.5-by)/44.5,(457.5-gy)/44.5,x,by,gy])
with (root/'paper-figure3b-digitized-v2.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['time_seconds','eye_position','object_position','pixel_x','eye_pixel_y','object_pixel_y']);w.writerows(rows)
record={'source':'https://cdn.elifesciences.org/articles/47314/elife-47314-fig3-v2.jpg','source_sha256':hashlib.sha256((root/'brian-figure3.jpg').read_bytes()).hexdigest(),'target':'Figure3b position traces','calibration':{'x_time0':1076,'x_time10':1635,'y_zero':457.5,'y_plus1':413,'y_minus1':502,'scale_basis':'Paper tick labels left/right correspond to -1/+1 in author Plotly cell.'},'samples':len(rows),'selection':'Every third x pixel in1080..1632, ROIy425..496; median of per-column green and black masks, only columns containing both. Axis/legend excluded. Revision2 clips black-mask y>=438 to exclude the object legend text; original revision1 comparison and failure retained.','exploratory_bounds':{'rmse_at_most':0.08,'max_abs_at_most':0.15},'basis':'Lines are about5-6pixels thick;44.5pixels/unit gives a roughly0.06-0.08unit half-width/calibration allowance. Max tolerance allows local steepness/time-pixel uncertainty. This is figure-resolution comparison, not a tolerance published by authors.','reviewed_repeat':'historical-run-3','declared_before_run':False,'limitations':['Manual calibration should receive human review.','Raster digitization cannot establish bitwise or all-spike reproduction.','Paper Figure3c and author notebook both use500ms; initial50ms reading corrected. This comparison tests Figure3b trace only.']}
(root/'digitization-protocol-v2.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))

# Revision2 corrects objectively identified legend contamination, without changing tolerance or model.
