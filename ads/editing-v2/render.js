// Renders the animated text overlay as a transparent PNG sequence. usage: node render.js ID
const { chromium } = require('playwright');
const fs = require('fs');
const ID = process.argv[2];
const tl = JSON.parse(fs.readFileSync(`work/${ID}/timeline.json`, 'utf8'));
const outDir = `work/${ID}/ov`;
fs.rmSync(outDir, { recursive: true, force: true });
fs.mkdirSync(outDir, { recursive: true });

const html = `<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;width:1080px;height:1920px;background:transparent;overflow:hidden}
*{box-sizing:border-box}
.card{position:absolute;left:70px;width:800px;text-align:center;transform-origin:50% 50%;
  font-family:'Montserrat';font-weight:800;opacity:0;will-change:transform}
.card span{display:inline;-webkit-box-decoration-break:clone;box-decoration-break:clone;
  padding:10px 26px;border-radius:22px;line-height:1.42}
.box span{background:#fff;color:#111;font-size:66px;box-shadow:0 10px 30px rgba(0,0,0,.28)}
.yel span{background:#FFD23F;color:#111;font-size:66px;box-shadow:0 10px 30px rgba(0,0,0,.28)}
.small span{background:rgba(17,17,17,.82);color:#fff;font-size:44px;font-weight:700;padding:8px 22px}
.big{font-size:170px;line-height:1;color:#fff;letter-spacing:-2px;
  text-shadow:0 6px 0 #111,0 0 40px rgba(0,0,0,.55)}
.big span{padding:0;background:none}
#end{position:absolute;inset:0;opacity:0}
#end .logo{position:absolute;top:640px;width:100%;text-align:center;font-family:'Montserrat';font-weight:800;
  font-size:250px;color:#fff;letter-spacing:4px;line-height:1}
#end .ag{position:absolute;top:905px;width:100%;text-align:center;font-family:'Montserrat';font-weight:800;
  font-size:46px;color:#FFD23F;letter-spacing:26px;padding-left:26px}
#end .line{position:absolute;top:1000px;left:50%;height:5px;background:#FFD23F;border-radius:3px;transform:translateX(-50%)}
#end .tag{position:absolute;top:1040px;width:100%;text-align:center;font-family:'Metropolis';font-weight:800;
  font-size:42px;color:#f2f2f2}
#end .cta{position:absolute;top:1170px;left:50%;transform:translateX(-50%);background:#FFD23F;color:#111;
  font-family:'Montserrat';font-weight:800;font-size:58px;padding:26px 54px;border-radius:999px;white-space:nowrap;
  box-shadow:0 14px 40px rgba(255,210,63,.35)}
</style></head><body>
${tl.cards.map((c, i) => `<div class="card ${c.style}" id="c${i}"><span>${c.html}</span></div>`).join('')}
<div id="end"><div class="logo">DCBR</div><div class="ag">AGENCY</div><div class="line"></div>
<div class="tag">Marketing per piccole e medie imprese</div><div class="cta">SCRIVICI IN DM &rarr;</div></div>
<script>
const TL = ${JSON.stringify(tl)};
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const outBack = x => { const c = 1.9; x = clamp(x); return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const outCubic = x => 1 - Math.pow(1 - clamp(x), 3);
const cards = TL.cards.map((c, i) => { const el = document.getElementById('c' + i); return { c, el }; });
function layoutCards() {
  for (const { c, el } of cards) el.style.top = (c.y - el.offsetHeight / 2) + 'px';
}
window.setTime = (t) => {
  const st = [];
  for (const { c, el } of cards) {
    let o = 0, s = 1, y = 0;
    if (t >= c.t0 && t <= c.t1 + 0.16) {
      const a = (t - c.t0) / 0.26;
      o = clamp((t - c.t0) / 0.1); s = 0.55 + 0.45 * outBack(a); y = 40 * (1 - outCubic(a));
      if (c.style === 'big') { s = 1.6 - 0.6 * outBack(a); y = 0; }
      if (t > c.t1) { const b = (t - c.t1) / 0.16; o *= 1 - b; s *= 1 - 0.06 * b; }
    }
    el.style.opacity = o.toFixed(3);
    el.style.transform = 'translateY(' + y.toFixed(1) + 'px) scale(' + s.toFixed(3) + ')';
    st.push(o.toFixed(2), s.toFixed(3), y.toFixed(0));
  }
  const e = document.getElementById('end'), te = t - TL.end;
  if (te < 0) { e.style.opacity = 0; st.push('e0'); return st.join(','); }
  e.style.opacity = clamp(te / 0.25);
  const L = e.querySelector('.logo'), A = e.querySelector('.ag'), Li = e.querySelector('.line'),
        T = e.querySelector('.tag'), C = e.querySelector('.cta');
  const lp = outBack((te - 0.05) / 0.35);
  L.style.transform = 'scale(' + (0.7 + 0.3 * lp).toFixed(3) + ')'; L.style.opacity = clamp((te - 0.05) / 0.12);
  A.style.opacity = clamp((te - 0.3) / 0.2); A.style.letterSpacing = (40 - 14 * outCubic((te - 0.3) / 0.5)).toFixed(1) + 'px';
  Li.style.width = (220 * outCubic((te - 0.45) / 0.35)).toFixed(0) + 'px';
  T.style.opacity = clamp((te - 0.6) / 0.25); T.style.transform = 'translateY(' + (20 * (1 - outCubic((te - 0.6) / 0.3))).toFixed(1) + 'px)';
  const cp = outBack((te - 1.0) / 0.3), pulse = te > 1.5 ? 1 + 0.035 * Math.sin((te - 1.5) * 2 * Math.PI * 1.4) : 1;
  C.style.opacity = clamp((te - 1.0) / 0.1);
  C.style.transform = 'translateX(-50%) scale(' + ((0.5 + 0.5 * cp) * pulse).toFixed(3) + ')';
  st.push(te.toFixed(3));
  return st.join(',');
};
document.fonts.ready.then(() => { layoutCards(); window.READY = true; });
</script></body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.setContent(html);
  await page.waitForFunction('window.READY === true');
  const N = Math.ceil(tl.dur * tl.fps);
  let prev = null, prevFile = null, rendered = 0;
  for (let f = 0; f < N; f++) {
    const name = `${outDir}/${String(f + 1).padStart(4, '0')}.png`;
    const state = await page.evaluate(t => window.setTime(t), f / tl.fps);
    if (state === prev) { fs.copyFileSync(prevFile, name); continue; }
    await page.screenshot({ path: name, omitBackground: true });
    prev = state; prevFile = name; rendered++;
  }
  await browser.close();
  console.log(`${ID}: ${N} frames, ${rendered} rendered`);
})();
