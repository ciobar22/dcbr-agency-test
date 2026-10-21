# Sound design: SFX + per-ad music beds, synthesized (no samples, no credits).
import numpy as np, wave, os, json
SR = 48000
rng = np.random.default_rng(11)
os.makedirs("sfx", exist_ok=True); os.makedirs("music", exist_ok=True)

def save(p, x):
    if x.ndim == 1: x = np.stack([x, x], 1)
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
    with wave.open(p, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def T(d): return np.arange(int(d * SR)) / SR
def lp(x, fc):  # one-pole lowpass, vectorised via FFT-free IIR approximation
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y
def fftfilt(x, lo=None, hi=None):  # brickwall-ish band filter with soft edges
    X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.ones_like(f)
    if lo: g *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi: g *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * (g if x.ndim == 1 else g[:, None]), n=len(x), axis=0)
def reverb(x, decay=1.2, mix=0.25, hi=6000):
    L = int(decay * 1.6 * SR); t = np.arange(L) / SR
    ir = np.stack([rng.standard_normal(L), rng.standard_normal(L)], 1) * np.exp(-t * 6.9 / decay)[:, None]
    ir = fftfilt(ir, 200, hi); ir /= np.sqrt(np.sum(ir ** 2))
    if x.ndim == 1: x = np.stack([x, x], 1)
    n = len(x) + L; F = lambda a: np.fft.rfft(a, n, axis=0)
    wet = np.fft.irfft(F(x) * F(ir), n, axis=0)
    out = np.zeros((n, 2)); out[:len(x)] += x * (1 - mix); out += wet * mix * 3
    return out
def env(t, a, d): return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(t - a, 0) / d)

# ---------- SFX ----------
t = T(0.12)  # pop: soft bubbly UI pop
pop = np.sin(2 * np.pi * np.cumsum(1400 * np.exp(-t * 40) + 380) / SR) * env(t, 0.002, 0.03)
save("sfx/pop.wav", reverb(pop, 0.4, 0.12))

t = T(0.75)  # whoosh: band-passed noise swelling past
n = rng.standard_normal(len(t)); sh = np.sin(np.pi * np.clip(t / 0.7, 0, 1)) ** 2.5
lo = fftfilt(n, 300, 1500) ; hi_ = fftfilt(n, 1500, 7000)
mixw = np.clip(t / 0.7, 0, 1)
w = (lo * (1 - mixw) + hi_ * mixw * 0.6) * sh
pan = np.stack([w * (1 - 0.6 * mixw), w * (0.4 + 0.6 * mixw)], 1)
save("sfx/whoosh.wav", reverb(pan, 0.6, 0.2))

t = T(1.6)  # impact: sub drop + body + air
sub = np.sin(2 * np.pi * np.cumsum(38 + 90 * np.exp(-t * 9)) / SR) * env(t, 0.003, 0.45)
body = fftfilt(rng.standard_normal(len(t)), 80, 900) * env(t, 0.001, 0.08) * 0.7
save("sfx/impact.wav", reverb(sub + body, 1.4, 0.3, 3000))

t = T(0.5)  # thud: short punch for "TU NO."
th = np.sin(2 * np.pi * np.cumsum(55 + 160 * np.exp(-t * 30)) / SR) * env(t, 0.002, 0.12)
th += fftfilt(rng.standard_normal(len(t)), 100, 2500) * env(t, 0.001, 0.02) * 0.5
save("sfx/thud.wav", reverb(th, 0.5, 0.12))

t = T(1.2)  # riser into the reveal
r = fftfilt(rng.standard_normal(len(t)), 800, 9000) * (t / 1.2) ** 2.2
r += np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / 1.2) ** 2) / SR) * (t / 1.2) ** 2 * 0.35
save("sfx/riser.wav", reverb(r * np.minimum(1, (1.2 - t) / 0.02), 0.5, 0.15))

t = T(1.0)  # ding: notification chime ("3 like")
d = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in [(1318.5, 1, 4), (1975.5, .5, 6), (2637, .25, 9)])
d2 = np.zeros_like(d); o = int(0.09 * SR); d2[o:] = d[:-o] * 0.7 * (1567.98 / 1318.5)
save("sfx/ding.wav", reverb(d * env(t, 0.002, 0.5) + d2, 0.6, 0.15))

t = T(0.06)  # tap: soft phone scroll tick
tap = fftfilt(rng.standard_normal(len(t)), 1500, 8000) * env(t, 0.0005, 0.008)
save("sfx/tap.wav", tap)

t = T(1.3)  # womp: comedic two-note sad horn
def horn(f0, d, gl):
    tt = T(d); f = f0 * (1 - gl * tt / d); ph = 2 * np.pi * np.cumsum(f) / SR
    v = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph) + 0.12 * np.sin(4 * ph)
    vib = 1 + 0.02 * np.sin(2 * np.pi * 5.5 * tt)
    return lp(v * vib, 1800) * np.minimum(1, tt / 0.03) * np.minimum(1, (d - tt) / 0.08)
womp = np.concatenate([horn(233, 0.42, 0.03), horn(207, 0.75, 0.12)])
save("sfx/womp.wav", reverb(womp, 0.5, 0.15))

t = T(3.0)  # ticks: clock ticking (tension), every 0.5s
tk = np.zeros(len(t))
for k in range(6):
    i = int(k * 0.5 * SR); c = fftfilt(rng.standard_normal(1200), 2000, 6000) * np.exp(-np.arange(1200) / SR / 0.004)
    tk[i:i + 1200] += c * (1 if k % 2 == 0 else 0.7)
save("sfx/ticks.wav", reverb(tk, 0.8, 0.25))

# ---------- music ----------
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def epiano(f, d):  # FM electric piano
    tt = T(d); idx = 2.2 * np.exp(-tt * 3)
    v = np.sin(2 * np.pi * f * tt + idx * np.sin(2 * np.pi * f * tt)) * np.exp(-tt * 1.6)
    v += 0.3 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 4)
    return v * np.minimum(1, tt / 0.004) * np.minimum(1, (d - tt) / 0.05)
def piano(f, d):  # additive piano with slight inharmonicity
    tt = T(d); v = np.zeros_like(tt)
    for k in range(1, 8):
        fk = f * k * np.sqrt(1 + 0.0004 * k * k); v += np.sin(2 * np.pi * fk * tt) * np.exp(-tt * (0.9 + 0.7 * k)) / k ** 1.3
    return v * np.minimum(1, tt / 0.003) * np.minimum(1, (d - tt) / 0.08)
def pluck(f, d):
    p = int(SR / f); n = int(d * SR); buf = rng.uniform(-1, 1, p); out = np.empty(n)
    for i in range(n):
        j = i % p; out[i] = buf[j]; buf[j] = 0.5 * (buf[j] + buf[(j + 1) % p]) * 0.994
    return lp(out, 3500)
def pad(fs, d):
    tt = T(d); v = np.zeros_like(tt)
    for f in fs:
        for det in (-0.12, 0, 0.12):
            ph = 2 * np.pi * f * 2 ** (det / 12) * tt; v += (2 * ((ph / (2 * np.pi)) % 1) - 1)
    return fftfilt(v, 80, 1400) * np.minimum(1, tt / 0.8) * np.minimum(1, (d - tt) / 0.8)
def kick(g=1):
    tt = T(0.4); return g * np.sin(2 * np.pi * np.cumsum(48 + 120 * np.exp(-tt * 28)) / SR) * env(tt, 0.002, 0.13)
def snare(g=1):
    tt = T(0.25); return g * (fftfilt(rng.standard_normal(len(tt)), 900, 7000) * env(tt, 0.001, 0.06) * 0.7
                              + np.sin(2 * np.pi * 190 * tt) * env(tt, 0.001, 0.04) * 0.5)
def hat(g=1):
    tt = T(0.06); return g * fftfilt(rng.standard_normal(len(tt)), 7000, None) * env(tt, 0.0005, 0.015)
def put(tr, x, t0, g=1.0, p=0.0):
    i = int(t0 * SR)
    if i >= len(tr): return
    x = x[:len(tr) - i]
    if x.ndim == 1: x = np.stack([x * (1 - max(p, 0)), x * (1 + min(p, 0))], 1)
    tr[i:i + len(x)] += x * g

def song(style, dur, opens_at):
    N = int(dur * SR); keys = np.zeros((N, 2)); drums = np.zeros((N, 2)); bassn = np.zeros((N, 2)); pads = np.zeros((N, 2))
    if style == "playful":
        bpm = 112; chords = [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]]
    elif style == "warm":
        bpm = 90; chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]
    else:
        bpm = 72; chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
    b = 60 / bpm; bar = 4 * b; nb = int(dur / bar) + 2
    for k in range(nb):
        ch = chords[k % 4]; t0 = k * bar
        if style == "playful":
            for s in range(8):  # pizzicato arpeggio
                f = mtof(ch[[0, 1, 2, 1, 0, 2, 1, 2][s]] + 12); put(keys, pluck(f, 0.45), t0 + s * b / 2, 0.55, 0.3 * (-1) ** s)
            put(bassn, pluck(mtof(ch[0] - 24), 0.9), t0, 0.8); put(bassn, pluck(mtof(ch[0] - 24), 0.9), t0 + 2 * b, 0.7)
            for q in range(4):
                put(drums, kick(0.8 if q in (0, 2) else 0), t0 + q * b); put(drums, snare(0.35 if q in (1, 3) else 0), t0 + q * b)
                put(drums, hat(0.25), t0 + q * b + b / 2, p=0.3)
        elif style == "warm":
            for f in ch: put(keys, epiano(mtof(f), bar * 0.95), t0 + 0.012 * ch.index(f), 0.32)
            put(keys, epiano(mtof(ch[-1] + 12), b), t0 + 2.5 * b, 0.18)
            put(bassn, np.sin(2 * np.pi * mtof(ch[0] - 24) * T(bar * 0.9)) * env(T(bar * 0.9), 0.01, 0.9), t0, 0.7)
            for q in range(4):
                sw = 0.62 * b  # swing
                put(drums, kick(0.75 if q in (0, 2) else 0), t0 + q * b); put(drums, snare(0.3 if q in (1, 3) else 0), t0 + q * b)
                put(drums, hat(0.2), t0 + q * b, p=-0.3); put(drums, hat(0.13), t0 + q * b + sw, p=0.3)
        else:
            for s, idx in enumerate([0, 1, 2, 1]):
                put(keys, piano(mtof(ch[idx] + 12), b * 1.8), t0 + s * b, 0.45, 0.25 * (-1) ** s)
            put(keys, piano(mtof(ch[0]), bar), t0, 0.35)
            if t0 + bar > opens_at:
                put(pads, pad([mtof(f) for f in ch], bar + 0.6), max(t0 - 0.3, 0), 0.22)
                put(bassn, piano(mtof(ch[0] - 24), bar), t0, 0.55)
    if style == "warm":  # filtered until the reveal, then it opens up
        cut = int(opens_at * SR); keys[:cut] = fftfilt(keys[:cut], None, 700); drums[:cut] = fftfilt(drums[:cut], None, 600) * 0.7
    if style == "cinematic":
        drums[:] = 0; put(drums, kick(1.0), opens_at);
    mix = keys + drums * 0.9 + bassn * 0.8 + pads
    vinyl = (rng.random(N) < 0.0006) * rng.standard_normal(N) * 0.15 if style == "warm" else np.zeros(N)
    mix += np.stack([vinyl, vinyl], 1)
    mix = reverb(mix, 1.8 if style == "cinematic" else 1.0, 0.22 if style == "cinematic" else 0.12)[:N]
    f = np.ones(N); f[:int(0.15 * SR)] = np.linspace(0, 1, int(0.15 * SR))
    return np.tanh(mix * f[:, None] * 0.9)

tl = {i: json.load(open(f"work/{i}/timeline.json")) for i in ("01", "06", "09")}
opens = {"01": 0, "06": 6.275, "09": 3.0}
for i, st in (("01", "playful"), ("06", "warm"), ("09", "cinematic")):
    save(f"music/{i}.wav", song(st, tl[i]["dur"] + 0.5, opens[i]))
print("sfx+music ok")
