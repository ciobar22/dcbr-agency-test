# Procedural music bed generator (numpy). usage: music.py mood out.wav seconds
import sys, wave, numpy as np
mood, out, dur = sys.argv[1], sys.argv[2], float(sys.argv[3])
SR = 44100
N = int(SR * dur)
rng = np.random.default_rng(7)
cfg = {
    "upbeat":    dict(bpm=104, chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]], kick="four", hats=True, arp=True, pad=0.18),
    "chill":     dict(bpm=84,  chords=[[50,53,57,60],[55,58,62],[48,52,55,59],[53,57,60,64]], kick="half", hats=True, arp=True, pad=0.22),
    "cinematic": dict(bpm=70,  chords=[[45,52,57],[41,48,53],[48,55,60],[43,50,55]], kick="boom", hats=False, arp=False, pad=0.32),
}[mood]
beat = 60 / cfg["bpm"]
bar = beat * 4
t = np.arange(N) / SR
mix = np.zeros(N)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)

def lowpass(x, a):
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc); y[i] = acc
    return y

# pad: detuned saws, slow attack, low-passed
pad = np.zeros(N)
nb = int(np.ceil(dur / bar))
for b in range(nb):
    s, e = int(b * bar * SR), min(N, int((b + 1) * bar * SR))
    seg = t[s:e] - t[s]
    env = np.minimum(1, seg / 0.6) * np.minimum(1, (seg[-1] - seg + 1e-3) / 0.3)
    for m in cfg["chords"][b % 4]:
        for d in (-0.08, 0.08):
            f = hz(m) * 2 ** (d / 12)
            pad[s:e] += (2 * ((seg * f) % 1) - 1) * env
pad = lowpass(pad, 0.035)
mix += cfg["pad"] * pad / np.max(np.abs(pad) + 1e-9)

# bass on root
bass = np.zeros(N)
for b in range(nb):
    root = cfg["chords"][b % 4][0] - 12
    for k in range(4 if mood != "cinematic" else 1):
        s = int((b * bar + k * beat) * SR); L = int((beat if mood != "cinematic" else bar) * SR)
        if s >= N: break
        seg = np.arange(min(L, N - s)) / SR
        bass[s:s + len(seg)] += np.sin(2 * np.pi * hz(root) * seg) * np.exp(-seg * (3 if mood != "cinematic" else 0.8))
mix += 0.22 * bass

# kick
def kick_at(time, strength=1.0, long=False):
    s = int(time * SR)
    if s >= N: return
    L = min(int((0.9 if long else 0.35) * SR), N - s)
    seg = np.arange(L) / SR
    f = 45 + 110 * np.exp(-seg * (18 if not long else 6))
    ph = 2 * np.pi * np.cumsum(f) / SR
    mix[s:s + L] += strength * np.sin(ph) * np.exp(-seg * (9 if not long else 2.5))
nbeats = int(dur / beat) + 1
for k in range(nbeats):
    if cfg["kick"] == "four": kick_at(k * beat, 0.55)
    elif cfg["kick"] == "half" and k % 2 == 0: kick_at(k * beat, 0.45)
    elif cfg["kick"] == "boom" and k % 8 == 0: kick_at(k * beat, 0.6, long=True)

# hats: high-passed noise ticks on off-beats
if cfg["hats"]:
    for k in range(nbeats * 2):
        if k % 2 == 1:
            s = int(k * beat / 2 * SR)
            if s >= N: break
            L = min(int(0.05 * SR), N - s)
            nz = rng.standard_normal(L); nz = nz - lowpass(nz, 0.5)
            mix[s:s + L] += 0.06 * nz * np.exp(-np.arange(L) / SR * 60)

# pluck arpeggio (Karplus-Strong)
def pluck(f, L):
    p = int(SR / f); buf = rng.uniform(-1, 1, p); out = np.empty(L)
    for i in range(L):
        out[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out
if cfg["arp"]:
    step = beat / 2
    for k in range(int(dur / step)):
        b = int(k * step / bar); notes = cfg["chords"][b % 4]
        m = notes[k % len(notes)] + 12
        s = int(k * step * SR); L = min(int(0.5 * SR), N - s)
        if L <= 0: break
        mix[s:s + L] += 0.07 * pluck(hz(m), L)

# master: fade in/out, normalize
fade = np.ones(N)
fi, fo = int(0.3 * SR), int(1.2 * SR)
fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
mix *= fade
mix = np.tanh(mix * 1.2)
mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.8
data = (np.repeat(mix[:, None], 2, axis=1) * 32767).astype(np.int16)
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
