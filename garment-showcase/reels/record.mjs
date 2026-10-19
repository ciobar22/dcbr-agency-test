// Render a reel from composer.html frame by frame, then encode it with FFmpeg.
// The page clock is faked, so the garment turns, swipes and captions land on exact frames.
// Usage: node reels/record.mjs lionel|dcbr [--fps 30] [--from 0 --to 3]   (needs Playwright + FFmpeg)
import http from 'node:http';
import path from 'node:path';
import {readFile,mkdir,rm} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {chromium} from 'playwright';

const root=path.resolve(fileURLToPath(new URL('../',import.meta.url)));
const args=process.argv.slice(2);const name=args[0]||'lionel';
const opt=(key,fallback)=>{const i=args.indexOf('--'+key);return i<0?fallback:Number(args[i+1]);};
const fps=opt('fps',30);
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp','.jpg':'image/jpeg','.ttf':'font/ttf','.woff2':'font/woff2','.woff':'font/woff'};
// Local, read-only and only for this render: the composer and the site must share an origin.
const server=http.createServer(async(req,res)=>{
  const file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://x').pathname));
  if(!file.startsWith(root+path.sep)||/[\\/](\.env|work|inputs|generated)/.test(file.slice(root.length))){res.writeHead(404);res.end();return;}
  try{const data=await readFile(file);res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream'});res.end(data);}catch{res.writeHead(404);res.end();}
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const base=`http://127.0.0.1:${server.address().port}`;
const frames=path.join(root,'work/reels',name);await rm(frames,{recursive:true,force:true});await mkdir(frames,{recursive:true});
const browser=await chromium.launch(process.env.CHROMIUM?{executablePath:process.env.CHROMIUM}:{});
try{
  const page=await (await browser.newContext({viewport:{width:1080,height:1920},deviceScaleFactor:1})).newPage();
  page.on('pageerror',e=>console.error('page error:',e.message));
  await page.clock.install({time:new Date('2026-10-19T10:00:00Z')});
  await page.goto(`${base}/reels/composer.html?reel=${name}`);
  let ready=false;
  for(let i=0;i<400&&!ready;i++){ready=await page.evaluate(()=>Boolean(window.reelLoaded&&window.reel.isReady()));if(!ready){await page.clock.runFor(50);await new Promise(r=>setTimeout(r,25));}}
  if(!ready)throw new Error('Composer or site did not become ready.');
  await page.evaluate(()=>window.reel.prepare());await page.clock.runFor(1500);
  const duration=await page.evaluate(()=>window.reel.duration);
  const first=Math.round(opt('from',0)*fps),last=Math.round(opt('to',duration)*fps);
  let prev={down:false,x:NaN,y:NaN};
  for(let i=first;i<last;i++){
    const t=i/fps,p=await page.evaluate(t=>window.reel.frame(t),t);
    if((p.visible||p.down)&&(p.x!==prev.x||p.y!==prev.y))await page.mouse.move(p.x,p.y);
    if(p.down&&!prev.down)await page.mouse.down();
    if(!p.down&&prev.down)await page.mouse.up();
    prev=p;
    await page.clock.runFor(1000/fps);
    await page.screenshot({path:path.join(frames,String(i-first).padStart(5,'0')+'.jpg'),type:'jpeg',quality:94});
    if(i%60===0)console.log(`${name}: ${t.toFixed(1)}s / ${duration}s`);
  }
}finally{await browser.close();server.close();}
const out=path.join(root,'reels/out');await mkdir(out,{recursive:true});
const file=path.join(out,`${name}-reel-1080x1920.mp4`);
const run=spawnSync(process.env.FFMPEG||'ffmpeg',['-y','-hide_banner','-loglevel','error','-framerate',String(fps),'-i',path.join(frames,'%05d.jpg'),'-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',file],{stdio:'inherit'});
if(run.status!==0)throw new Error('FFmpeg failed.');
console.log('Wrote '+path.relative(root,file));
