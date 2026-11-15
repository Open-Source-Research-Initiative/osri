"""Run the paper author's immutable COMBINE archive, retain generated arrays.
Original OSRI wrapper, MIT; archive/model terms remain independent.
"""
from pathlib import Path
import argparse,hashlib,importlib.metadata,json,sys,time
import numpy as np
import tellurium as te
parser=argparse.ArgumentParser()
parser.add_argument('--archive',type=Path,default=Path(__file__).with_name('calzone-fig1-fig3.omex'))
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=False)
work=args.output/'extracted';work.mkdir()
start=time.time()
result=te.executeCombineArchive(str(args.archive),workingDir=str(work),createOutputs=True,saveOutputs=True,outputDir=str(args.output),plottingEngine='matplotlib')
summary={}
for file,data in result.items():
 print('RESULT',file,type(data),str(data.keys()) if isinstance(data,dict) else '')
 summary[file]={key: {'type':type(value).__name__,'shape':list(np.shape(value))} for key,value in data.items()} if isinstance(data,dict) else str(type(data))
 generators=data['dataGenerators']
 np.savez_compressed(args.output/'raw-results.npz',**{str(k):np.asarray(v) for k,v in generators.items()})
 keys=sorted(generators)
 np.savetxt(args.output/'data-generators.csv',np.column_stack([np.asarray(generators[k]).reshape(-1) for k in keys]),delimiter=',',header=','.join(keys),comments='')
 (args.output/'generated-sedml.py').write_text(data['code'])
record={'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'status':'author_code_executed','archive_sha256':hashlib.sha256(args.archive.read_bytes()).hexdigest(),'source_commit':'eff025846c5b12ee4350f043623332158e05f262','python':sys.version,'packages':{name:importlib.metadata.version(name) for name in ['tellurium','libroadrunner','python-libsedml','python-libsbml','numpy','scipy','matplotlib','six']},'elapsed_seconds':time.time()-start,'result_structure':summary,'comparison_pending':True,'human_scientific_review':'pending'}
(args.output/'run-record.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
