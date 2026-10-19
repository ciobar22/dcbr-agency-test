import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {makeServer,publicFile} from '../scripts/serve.mjs';
test('the server exposes runtime assets, not credentials or generation inputs',async()=>{
  for(const url of ['/.env.local','/pipeline/ltx.mjs','/inputs/front.png','/generated/take/request.json','/public/%2e%2e%2f.env.local','/src/%5cprivate.js'])assert.equal(publicFile(url),null,url);
  const server=makeServer();await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const url='http://127.0.0.1:'+server.address().port;
  try{
    const response=await fetch(url+'/');assert.equal(response.status,200);assert.match(response.headers.get('content-type'),/text\/html/);
    const config=await fetch(url+'/config/catalog.json');const served=await config.json();const expected=JSON.parse(await readFile(new URL('../config/catalog.json',import.meta.url),'utf8'));assert.deepEqual(served,expected);
    assert.equal((await fetch(url+'/.env.local')).status,404);
    assert.equal((await fetch(url+'/',{method:'POST'})).status,405);
    const manifest=await (await fetch(url+'/public/'+served.items[0].motion)).json();const atlas=await fetch(url+'/public/'+served.items[0].motion.replace(/[^/]+$/,manifest.atlas));assert.equal(atlas.status,200);assert.equal(atlas.headers.get('content-type'),'image/webp');
    // A second page reads its own catalog and web fonts through the same allowlist.
    const page=await fetch(url+'/lionel.html');assert.equal(page.status,200);assert.match(await page.text(),/data-catalog="lionel"/);
    const lionel=await (await fetch(url+'/config/lionel.json')).json();assert.ok(lionel.items.every(item=>item.price));
    assert.equal((await fetch(url+'/public/fonts/Anton-Regular.woff2')).headers.get('content-type'),'font/woff2');
    for(const path of ['/concepts/lionel/prints.py','/work/lionel/prints/studio-black-on-bone.png','/config/../.env'])assert.equal((await fetch(url+path)).status,404,path);
  }finally{await new Promise(resolve=>server.close(resolve));}
});
