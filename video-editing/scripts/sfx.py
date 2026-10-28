#!/usr/bin/env python3
"""Original synthesized SFX + music bed for reels (no licensing issues).

Usage: python3 sfx.py --out sfx_lib   # writes every SFX + a 30s bed preview
Library use: from sfx import LIB, music_bed, write_wav
"""
import argparse
import os
import wave

import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000


def _t(d):
    return np.arange(int(d * SR)) / SR


def _band(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], btype="band", fs=SR, output="sos"), x)


def _hp(x, f):
    return sosfilt(butter(2, f, btype="high", fs=SR, output="sos"), x)


def _lp(x, f):
    return sosfilt(butter(2, f, btype="low", fs=SR, output="sos"), x)


def _norm(x, peak=0.9):
    m = float(np.max(np.abs(x))) or 1.0
    return x / m * peak


def _stereo(x, pan=None):
    if pan is None:
        return np.stack([x, x], 1)
    return np.stack([x * np.sqrt((1 - pan) / 2), x * np.sqrt((1 + pan) / 2)], 1) * 1.41


def sweep_noise(d, f0, f1, bw=0.5, seed=0):
    """Noise whose spectral band glides from f0 to f1 (log), bw in octaves."""
    rng = np.random.default_rng(seed)
    n, N, H = int(d * SR), 1024, 256
    x, win = rng.standard_normal(n + N), np.hanning(N)
    out, fr = np.zeros(n + N), np.fft.rfftfreq(N, 1 / SR)
    frames = max(n // H, 1)
    for i in range(frames):
        fc = f0 * (f1 / f0) ** (i / max(frames - 1, 1))
        X = np.fft.rfft(x[i * H:i * H + N] * win)
        X *= np.exp(-0.5 * (np.log2(np.maximum(fr, 1) / fc) / bw) ** 2)
        out[i * H:i * H + N] += np.fft.irfft(X, N) * win
    return out[:n]


def whoosh(d=0.45, up=True, seed=1):
    x = sweep_noise(d, 350, 4500, seed=seed) if up else sweep_noise(d, 4000, 300, seed=seed)
    t, p = _t(d), 0.62
    env = np.where(t < p * d, (t / (p * d)) ** 2, np.clip(1 - (t - p * d) / ((1 - p) * d), 0, 1) ** 1.5)
    return _stereo(_norm(x * env), np.linspace(-0.6, 0.6, len(x)))


def pop():
    t = _t(0.11)
    f = 950 * np.exp(-t * 38) + 230
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 42)
    x[:96] *= np.linspace(0, 1, 96)
    return _stereo(_norm(x, 0.85))


def boom():
    t = _t(1.2)
    f = 75 * np.exp(-t * 3) + 36
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    click = _lp(np.random.default_rng(5).standard_normal(len(t)), 2500) * np.exp(-t * 60) * 0.5
    return _stereo(_norm(np.tanh(2.2 * (body + click))))


def sparkle():
    t = _t(1.6)
    x, rng = np.zeros_like(t), np.random.default_rng(7)
    for k, f in enumerate([2093, 2637, 3136, 4186, 5274, 6272]):
        st = int(k * 0.045 * SR)
        tt = t[:len(t) - st]
        tone = np.sin(2 * np.pi * f * tt + rng.uniform(0, 6)) * np.exp(-tt * (3.5 + k * 0.6)) * 0.9 ** k
        x[st:] += tone * (1 + 0.25 * np.sin(2 * np.pi * 7 * tt))
    x += _hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * 5) * 0.05
    return _stereo(_norm(x, 0.8), 0.5 * np.sin(2 * np.pi * 1.3 * t))


def riser(d=1.2):
    x = sweep_noise(d, 250, 7000, bw=0.7, seed=9) * np.linspace(0, 1, int(d * SR)) ** 2
    return _stereo(_norm(x, 0.8))


def record_stop():
    """Comedic 'vinyl stop' glide for awkward/punchline beats."""
    t = _t(0.7)
    f = 420 * (1 - t / 0.7) ** 1.6 + 30
    x = sum(np.sin(2 * np.pi * np.cumsum(f * h) / SR) * 0.5 ** h for h in range(1, 4))
    return _stereo(_norm(x * np.exp(-t * 1.5), 0.7))


LIB = {
    "whoosh": lambda: whoosh(0.45, True, 1),
    "whoosh_down": lambda: whoosh(0.4, False, 2),
    "swish": lambda: whoosh(0.28, True, 3),
    "pop": pop,
    "boom": boom,
    "sparkle": sparkle,
    "riser": riser,
    "record_stop": record_stop,
}

NOTE = lambda m: 440.0 * 2 ** ((m - 69) / 12)
# Am - F - C - G : (bass midi, chord tones)
PROG = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]


def music_bed(dur, bpm=98, seed=0):
    """Light pluck/lo-fi loop meant to sit ~20 dB under the voice."""
    beat = 60 / bpm
    bar, n = 4 * beat, int(dur * SR) + SR
    out, rng = np.zeros((n, 2)), np.random.default_rng(seed)

    def add(sig, t0, gain, pan=0.0):
        i = int(t0 * SR)
        if i >= n:
            return
        s = sig[:n - i]
        out[i:i + len(s), 0] += s * gain * np.sqrt((1 - pan) / 2) * 1.41
        out[i:i + len(s), 1] += s * gain * np.sqrt((1 + pan) / 2) * 1.41

    tk = _t(0.45)
    kick = np.sin(2 * np.pi * np.cumsum(110 * np.exp(-tk * 28) + 44) / SR) * np.exp(-tk * 7)
    ts = _t(0.22)
    snare = _band(rng.standard_normal(len(ts)), 1200, 5000) * np.exp(-ts * 22) * 0.8 \
        + np.sin(2 * np.pi * 190 * ts) * np.exp(-ts * 30) * 0.4
    th = _t(0.05)
    hat = _hp(rng.standard_normal(len(th)), 7000) * np.exp(-th * 90)

    def pluck(m, d=0.5):
        t, f = _t(d), NOTE(m)
        x = sum(np.sin(2 * np.pi * f * h * t) * 0.6 ** (h - 1) * np.exp(-t * (6 + 2 * h)) for h in range(1, 6))
        return x * np.minimum(1, t * 400)

    def bass(m, d):
        t, f = _t(d), NOTE(m)
        x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)
        return np.tanh(1.5 * x) * np.minimum(1, t * 80) * np.exp(-t * 1.2)

    def pad(ms, d):
        t = _t(d)
        x = sum(np.sin(2 * np.pi * NOTE(m) * t) + 0.3 * np.sin(2 * np.pi * NOTE(m) * 2.003 * t) for m in ms)
        return _lp(x * np.minimum(1, t / 0.4) * np.clip((d - t) / 0.3, 0, 1), 1800)

    arp_order = [0, 1, 2, 3, 2, 1, 2, 3]
    for b in range(int(dur / bar) + 2):
        t0 = b * bar
        root, tones = PROG[b % 4]
        add(pad(tones, bar), t0, 0.06)
        add(bass(root, bar * 0.95), t0, 0.32)
        for q in range(4):
            tb = t0 + q * beat
            if q in (0, 2):
                add(kick, tb, 0.55)
            if q == 3 and b % 2:
                add(kick, tb + beat * 0.5, 0.3)
            if q in (1, 3):
                add(snare, tb, 0.28)
            add(hat, tb, 0.16, 0.3)
            add(hat, tb + beat / 2, 0.09, 0.3)
        arp = tones + [tones[0] + 12]
        for e in range(8):
            add(pluck(arp[arp_order[e]] + 12), t0 + e * beat / 2, 0.13, -0.25 if e % 2 else 0.25)
    out = np.tanh(out[:int(dur * SR)] * 1.2)
    fi, fo = int(0.3 * SR), int(1.0 * SR)
    out[:fi] *= np.linspace(0, 1, fi)[:, None]
    out[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return _norm(out, 0.7)


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="sfx_lib")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for name, fn in LIB.items():
        write_wav(os.path.join(a.out, f"{name}.wav"), fn())
    write_wav(os.path.join(a.out, "bed_preview.wav"), music_bed(30))
    print("wrote", sorted(os.listdir(a.out)))
