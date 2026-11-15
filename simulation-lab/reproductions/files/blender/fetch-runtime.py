"""Retrieve author code and digest-pinned Blender module without a Docker daemon."""
from pathlib import Path
import hashlib,json,subprocess,tarfile,urllib.request,shutil
ROOT=Path(__file__).resolve().parent
ROOT.joinpath('sources').mkdir(exist_ok=True)
SOURCE=ROOT/'sources/kubric'
if not SOURCE.exists():subprocess.run(['git','clone','--filter=blob:none','--no-checkout','https://github.com/google-research/kubric.git',str(SOURCE)],check=True)
COMMIT='9a868cc735de955709c4c75d9655fff1e90c72e4'
subprocess.run(['git','fetch','--depth','1','origin',COMMIT],cwd=SOURCE,check=True)
subprocess.run(['git','checkout',COMMIT],cwd=SOURCE,check=True)
REPO='kubricdockerhub/blender';DIGEST='sha256:d75dc24ad0d664ba71d0c57c6707d23f582d7f65cc1ee616cfa74ffbfa91f507'
with urllib.request.urlopen('https://auth.docker.io/token?service=registry.docker.io&scope=repository:'+REPO+':pull') as response:token=json.load(response)['token']
headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.docker.distribution.manifest.v2+json'}
req=urllib.request.Request('https://registry-1.docker.io/v2/'+REPO+'/manifests/'+DIGEST,headers=headers)
with urllib.request.urlopen(req) as response:raw=response.read()
assert 'sha256:'+hashlib.sha256(raw).hexdigest()==DIGEST
manifest=json.loads(raw);(ROOT/'image-manifest.json').write_bytes(raw)
PREFIX='usr/local/lib/python3.9/dist-packages/'
for index in [4,5]:
 layer=manifest['layers'][index];archive=ROOT/('layer-'+str(index)+'.tar.gz')
 req=urllib.request.Request('https://registry-1.docker.io/v2/'+REPO+'/blobs/'+layer['digest'],headers=headers)
 with urllib.request.urlopen(req) as response,archive.open('wb') as output:shutil.copyfileobj(response,output)
 with archive.open('rb') as f:
  h=hashlib.sha256()
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 assert 'sha256:'+h.hexdigest()==layer['digest']
 with tarfile.open(archive) as tar:
  for member in tar:
   if not member.name.startswith(PREFIX):continue
   relative=Path(member.name[len(PREFIX):])
   if relative.is_absolute() or '..' in relative.parts:raise ValueError('Unsafe archive path')
   output=ROOT/'runtime'/relative
   if member.isdir():output.mkdir(parents=True,exist_ok=True)
   elif member.isfile():
    output.parent.mkdir(parents=True,exist_ok=True)
    with tar.extractfile(member) as source,output.open('wb') as destination:shutil.copyfileobj(source,destination)
   else:raise ValueError('Unexpected non-file archive member')
print('Author Blender2.93 module and paper-date source are ready.')
