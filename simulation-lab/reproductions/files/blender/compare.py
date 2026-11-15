from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
out=ROOT/'output';prior=ROOT/'prior-output'
m=json.loads((out/'metadata.json').read_text());meta=m['metadata']
frames=sorted(out.glob('rgba_*.png'));segments=sorted(out.glob('segmentation_*.png'))
checks={'frames_equal24':len(frames)==24,'all_images_256_square':all(Image.open(p).size==(256,256) for p in frames),'instances_in3_to10':3<=len(m['instances'])<=10,'metadata_frames_equal24':meta['num_frames']==24,'frame_rate12':meta['frame_rate']==12,'segmentation_frames24':len(segments)==24}
checks['segmentation_labels_in0_to_num_instances']=all(np.asarray(Image.open(p)).max()<=len(m['instances']) for p in segments)
depths=[np.asarray(Image.open(p)) for p in sorted(out.glob('depth_*.tiff'))]
checks['finite_positive_depth']=all(np.isfinite(a).all() and np.all(a>=0) for a in depths)
checks['objects_move']=any(not np.array_equal(inst['positions'][0],inst['positions'][-1]) for inst in m['instances'])
repeat={}
if (prior/'metadata.json').exists():
 old=json.loads((prior/'metadata.json').read_text())
 repeat['prior_run_finished_numeric_outputs_then_failed_optional_hypertune_import']=True
 repeat['instance_metadata_exactly_equal']=m['instances']==old['instances']
 repeat['rgba_sha256_equal_frames']=sum(hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256((prior/p.name).read_bytes()).digest() for p in frames)
 repeat['rgba_frames_compared']=len(frames)
result={'status':'author_code_executed','paper':'https://arxiv.org/html/2203.03570v1','locator':'Section4.1/Figure5 MOVi-A dataset design; not Table3 learning scores','paper_design':{'clip_frames':24,'resolution':[256,256],'max_moving_objects':10},'measured':meta,'checks':checks,'all_design_checks_passed':all(checks.values()),'repeatability':repeat,'limitations':['A newly generated scene, not a pixel-exact reconstruction of a figure5illustration.','Public currentKuBasic assets; exact original2022asset bytes are not established.','ModernPyBullet/TensorFlow dependency versions differ from original rendering image package set.','No SAVi/SIMONe training or foregroundARI reproduction.','Human scientific review pending.']}
(out/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
assert all(checks.values());print(json.dumps(result,indent=2))
# A contact sheet made only from actually rendered frames.
thumbs=[Image.open(frames[i]).convert('RGB') for i in [0,5,11,17,23]]
canvas=Image.new('RGB',(256*5,256),'white')
for i,p in enumerate(thumbs):canvas.paste(p,(i*256,0))
canvas.save(out/'preview.png')
