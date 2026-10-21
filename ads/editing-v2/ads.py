# DCBR reels v2 — text-led edit. usage: ads.py base|final ID
import sys, json, os, subprocess
import numpy as np, wave

FPS = 24
W, H = 1080, 1920
E = 2.8  # end card length

ADS = {
    "01": dict(music="playful", segs=[
        dict(s=0.0, e=2.2, sp=1.0, z=(1.00, 1.12), c=(0.50, 0.32)),
        dict(s=2.4, e=5.8, sp=1.15, z=(1.06, 1.16), c=(0.50, 0.42)),
        dict(s=6.3, e=9.3, sp=1.0, z=(1.10, 1.24), c=(0.42, 0.42)),
        dict(s=11.0, e=14.0, sp=1.0, z=(1.15, 1.38), c=(0.50, 0.30)),
    ], cards=[
        (0, 0.04, 0, None, "box", 1220, "I SOCIAL LI FA<br>MIO NIPOTE."),
        (1, 0.08, 1, None, "yel", 1130, "STRATEGIA:"),
        (1, 0.38, 1, None, "box", 1270, "BALLETTO<br>COL TRAPANO"),
        (2, 0.08, 2, None, "yel", 1080, "RISULTATO:"),
        (2, 0.36, 2, None, "big", 1250, "3 LIKE"),
        (2, 1.55, 2, None, "small", 1420, "(uno è di sua madre)"),
        (3, 0.12, 3, 1.45, "box", 1250, "TUO NIPOTE<br>TI VUOLE BENE."),
        (3, 1.55, 3, None, "yel", 1250, "NOI TI PORTIAMO<br>CLIENTI VERI."),
    ], sfx=[
        (0, 0.04, "pop", 0.7), (1, 0.0, "whoosh", 0.55), (1, 0.08, "pop", 0.6), (1, 0.38, "pop", 0.6),
        (2, 0.0, "whoosh", 0.55), (2, 0.08, "pop", 0.6), (2, 0.36, "ding", 0.8), (2, 1.55, "pop", 0.45),
        (3, 0.0, "womp", 0.6), (3, 0.12, "pop", 0.55), (3, 1.55, "pop", 0.65),
    ], flash=[]),
    "06": dict(music="warm", segs=[
        dict(s=1.0, e=3.9, sp=1.0, z=(1.00, 1.10), c=(0.62, 0.42)),
        dict(s=4.5, e=9.9, sp=1.6, z=(1.00, 1.08), c=(0.50, 0.50)),
        dict(s=10.0, e=15.0, sp=1.0, z=(1.16, 1.00), c=(0.42, 0.45)),
    ], cards=[
        (0, 0.04, 0, 1.35, "box", 1250, "LUI HA LA FILA."),
        (0, 1.40, 0, None, "yel", 1250, "TU IL GELATO<br>PIÙ BUONO."),
        (1, 0.10, 1, 1.95, "box", 1330, "LUI È OVUNQUE<br>SUI SOCIAL."),
        (1, 2.00, 1, None, "big", 960, "TU NO."),
        (2, 0.30, 2, 2.40, "box", 1250, "NON VINCE<br>IL MIGLIORE."),
        (2, 2.50, 2, None, "yel", 1250, "VINCE CHI<br>SI FA VEDERE."),
    ], sfx=[
        (0, 0.04, "pop", 0.7), (0, 1.40, "pop", 0.6),
        (1, 0.0, "whoosh", 0.5), (1, 0.10, "pop", 0.55),
        (1, 0.55, "tap", 0.5), (1, 1.05, "tap", 0.5), (1, 1.55, "tap", 0.5),
        (1, 2.00, "thud", 0.7), (1, 2.35, "riser", 0.55),
        (2, 0.0, "impact", 0.85), (2, 0.30, "pop", 0.55), (2, 2.50, "pop", 0.65),
    ], flash=[2]),
    "09": dict(music="cinematic", segs=[
        dict(s=0.0, e=4.2, sp=1.4, z=(1.30, 1.42), c=(0.43, 0.25)),
        dict(s=4.2, e=9.0, sp=1.6, z=(1.30, 1.00), c=(0.45, 0.35)),
        dict(s=9.5, e=14.5, sp=1.0, z=(1.00, 1.08), c=(0.50, 0.60)),
    ], cards=[
        (0, 0.04, 0, 1.45, "box", 1250, "LOCALE PERFETTO."),
        (0, 1.50, 0, None, "yel", 1250, "SALA VUOTA."),
        (1, 0.20, 1, None, "box", 1250, "IL PROBLEMA<br>NON È LA CUCINA."),
        (2, 0.20, 2, 2.45, "box", 1250, "È CHE NESSUNO<br>TI CONOSCE."),
        (2, 2.55, 2, None, "yel", 1250, "NOI TI FACCIAMO<br>TROVARE."),
    ], sfx=[
        (0, 0.0, "ticks", 0.45), (0, 0.04, "pop", 0.6), (0, 1.50, "pop", 0.6),
        (1, 0.0, "whoosh", 0.6), (1, 0.0, "impact", 0.55), (1, 0.20, "pop", 0.55),
        (2, 0.20, "pop", 0.55), (2, 2.55, "pop", 0.65),
    ], flash=[]),
}


def layout(ad):
    starts, t = [], 0.0
    for s in ad["segs"]:
        starts.append(t)
        t += (s["e"] - s["s"]) / s["sp"]
    return starts, t  # t = end of last segment = end card start


def run(cmd):
    subprocess.run(cmd, check=True)


def base(ID):
    ad = ADS[ID]; os.makedirs(f"work/{ID}", exist_ok=True)
    starts, T = layout(ad)
    total = T + E
    parts, n = [], len(ad["segs"])
    for i, s in enumerate(ad["segs"]):
        d = (s["e"] - s["s"]) / s["sp"]
        D = d + (E if i == n - 1 else 0)
        z0, z1 = s["z"]; cx, cy = s["c"]
        Z = f"({z0}+({z1}-{z0})*min(t/{D:.4f},1))"
        # smooth zoom: upscale per-frame then crop around focus point (clamped)
        chain = (f"[0:v]trim=start={s['s']}:end={s['e']},setpts=(PTS-STARTPTS)/{s['sp']},fps={FPS},"
                 + (f"tpad=stop_mode=clone:stop_duration={E}," if i == n - 1 else "")
                 + f"scale=w='trunc({W}*{Z}/2)*2':h='trunc({H}*{Z}/2)*2':eval=frame:flags=lanczos,"
                 f"crop={W}:{H}:x='min(max(iw*{cx}-{W}/2,0),iw-{W})':y='min(max(ih*{cy}-{H}/2,0),ih-{H})',"
                 f"setsar=1,format=yuv420p[s{i}]")
        parts.append(chain)
    fc = ";".join(parts) + ";" + "".join(f"[s{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[cat];"
    # end card background: blur + darken fading in
    fc += (f"[cat]split[a][b];[b]gblur=sigma=30,eq=brightness=-0.32:saturation=0.6,format=yuva420p,"
           f"fade=t=in:st={T:.3f}:d=0.35:alpha=1[bb];[a][bb]overlay[v0]")
    last = "v0"
    for k, si in enumerate(ad["flash"]):
        t0 = starts[si]
        fc += (f";color=white:s={W}x{H}:r={FPS}:d=0.4,format=rgba,fade=t=in:st=0:d=0.04:alpha=1,"
               f"fade=t=out:st=0.04:d=0.3:alpha=1,setpts=PTS+{t0 - 0.04:.3f}/TB[fl{k}];"
               f"[{last}][fl{k}]overlay=eof_action=pass[v{k+1}]")
        last = f"v{k+1}"
    fc += f";[{last}]trim=duration={total:.3f},unsharp=5:5:0.4[vout]"
    run(["ffmpeg", "-v", "error", "-y", "-i", f"raw/{ID}.mp4", "-filter_complex", fc, "-map", "[vout]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", f"work/{ID}/base.mp4"])
    cards = []
    for (si, off, ei, eoff, style, y, html) in ad["cards"]:
        t0 = starts[si] + off
        if eoff is None:
            t1 = (starts[ei + 1] if ei + 1 < n else T) - 0.02
        else:
            t1 = starts[ei] + eoff
        cards.append(dict(t0=round(t0, 3), t1=round(t1, 3), style=style, y=y, html=html))
    json.dump(dict(fps=FPS, dur=round(total, 3), end=round(T, 3), cards=cards),
              open(f"work/{ID}/timeline.json", "w"), ensure_ascii=False, indent=1)
    print(ID, "segments", [round(x, 2) for x in starts], "end", round(T, 2), "total", round(total, 2))


# ---------------- audio ----------------
SR = 48000

def readwav(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels())

def writewav(p, x):
    x = np.clip(x, -1, 1)
    with wave.open(p, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def place(track, clip, t, g):
    i = int(t * SR)
    if i >= len(track): return
    L = min(len(clip), len(track) - i)
    track[i:i + L] += clip[:L] * g

def final(ID):
    ad = ADS[ID]; starts, T = layout(ad); total = T + E
    N = int(total * SR) + SR // 10
    fx = np.zeros((N, 2), np.float32)
    for (si, off, name, g) in ad["sfx"]:
        place(fx, readwav(f"sfx/{name}.wav"), starts[si] + off, g)
    # end card: whoosh in, impact, CTA pop
    place(fx, readwav("sfx/whoosh.wav"), T - 0.25, 0.55)
    place(fx, readwav("sfx/impact.wav"), T + 0.12, 0.45)
    place(fx, readwav("sfx/pop.wav"), T + 1.05, 0.6)
    fx = fx[:int(total * SR)]
    # A: SFX only (add a trending sound in-app)
    a = np.tanh(fx * 1.4) / np.tanh(1.4)
    a *= 0.6 / (np.max(np.abs(a)) + 1e-9)
    writewav(f"work/{ID}/A.wav", a)
    # B: music + SFX
    m = readwav(f"music/{ID}.wav")[:len(fx)]
    if len(m) < len(fx): m = np.pad(m, ((0, len(fx) - len(m)), (0, 0)))
    fade = np.ones(len(m)); fo = int(0.9 * SR); fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
    b = m * fade[:, None] * 0.62 + fx * 0.8
    b = np.tanh(b * 1.3) / np.tanh(1.3)
    rms = np.sqrt(np.mean(b ** 2)); b *= min(0.2 / (rms + 1e-9), 0.89 / (np.max(np.abs(b)) + 1e-9))
    writewav(f"work/{ID}/B.wav", b)
    os.makedirs("out", exist_ok=True)
    for ver in "AB":
        run(["ffmpeg", "-v", "error", "-y", "-i", f"work/{ID}/base.mp4", "-framerate", str(FPS), "-i", f"work/{ID}/ov/%04d.png",
             "-i", f"work/{ID}/{ver}.wav", "-filter_complex", "[0:v][1:v]overlay=eof_action=pass,format=yuv420p[v]",
             "-map", "[v]", "-map", "2:a", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
             "-profile:v", "high", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
             f"out/DCBR_v2_ad{ID}_{'solo-effetti' if ver == 'A' else 'con-musica'}.mp4"])
    print(ID, "final ok", round(total, 2))


if __name__ == "__main__":
    {"base": base, "final": final}[sys.argv[1]](sys.argv[2])
