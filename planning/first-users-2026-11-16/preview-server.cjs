// Local static preview with byte-range responses for video seeking.
const http=require('http'),fs=require('fs'),path=require('path');
const root=path.resolve(process.argv[2]),port=Number(process.argv[3]||8798);
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webm':'video/webm','.vtt':'text/vtt','.woff2':'font/woff2','.csv':'text/csv'};
http.createServer((req,res)=>{
 let file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
 if(file!==root&&!file.startsWith(root+path.sep)){res.writeHead(403);return res.end();}
 try{if(fs.statSync(file).isDirectory())file=path.join(file,'index.html');const stat=fs.statSync(file);if(!stat.isFile())throw Error('not a file');
  let start=0,end=stat.size-1,status=200;const range=req.headers.range?.match(/^bytes=(\d+)-(\d*)$/);
  if(range){start=Number(range[1]);if(range[2])end=Math.min(Number(range[2]),end);status=206;}
  if(start>end||start>=stat.size){res.writeHead(416,{'Content-Range':`bytes */${stat.size}`});return res.end();}
  const headers={'Content-Type':types[path.extname(file)]||'application/octet-stream','Content-Length':end-start+1,'Accept-Ranges':'bytes'};
  if(status===206)headers['Content-Range']=`bytes ${start}-${end}/${stat.size}`;
  res.writeHead(status,headers);if(req.method==='HEAD')return res.end();fs.createReadStream(file,{start,end}).pipe(res);
 }catch{res.writeHead(404);res.end('Not found');}
}).listen(port,'127.0.0.1',()=>console.log(`Preview http://127.0.0.1:${port}`));
