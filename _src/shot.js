const { chromium } = require('playwright'); const http=require('http'),fs=require('fs'),path=require('path');
const root='/home/claude/site4', out='/home/claude/shots4'; fs.mkdirSync(out,{recursive:true});
const T={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.jpg':'image/jpeg','.webp':'image/webp','.png':'image/png'};
const srv=http.createServer((q,r)=>{let p=decodeURIComponent(q.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';fs.readFile(path.join(root,p),(e,d)=>{if(e){r.writeHead(404);r.end();return}r.writeHead(200,{'content-type':T[path.extname(p)]||'text/plain'});r.end(d)})}).listen(8767);
const pages=(process.argv[2]||'zh:/,en:/,fr:/fr/,note:/notes/french-business-titles/,noten:/en/notes/french-business-titles/').split(',').map(x=>x.split(':'));
(async()=>{const b=await chromium.launch();
 for(const [n,u] of pages){ for(const [dev,vp] of [['desk',{width:1366,height:900}],['mob',{width:390,height:844}]]){
  const p=await b.newPage({viewport:vp}); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.route(/fonts\.(googleapis|gstatic)/,r=>r.abort());
  await p.goto('http://localhost:8767'+(n==='en'?'/en/':u)); await p.waitForTimeout(300);
  await p.evaluate(()=>{document.querySelectorAll('.rv').forEach(x=>x.classList.add('in'));document.querySelector('.hero')&&document.querySelector('.hero').classList.add('ld')});
  await p.waitForTimeout(1600);
  await p.screenshot({path:`${out}/${n}-${dev}.png`,fullPage:true});
  console.log(n,dev,'ovx',await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth),errs.join('|'));
  await p.close();}}
 await b.close(); srv.close();})();
