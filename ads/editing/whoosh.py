import wave, numpy as np
SR = 44100; L = int(0.7 * SR); t = np.arange(L) / SR
rng = np.random.default_rng(3); nz = rng.standard_normal(L)
out = np.zeros(L); acc = 0.0
for i in range(L):  # sweeping one-pole lowpass
    a = 0.02 + 0.5 * (i / L) ** 2 if i < L * 0.6 else 0.02 + 0.5 * (1 - (i - L * 0.6) / (L * 0.4)) * 0.36
    acc += a * (nz[i] - acc); out[i] = acc
env = np.sin(np.pi * np.clip(t / 0.7, 0, 1)) ** 2
out = out * env; out /= np.max(np.abs(out)); out *= 0.7
d = (np.repeat(out[:, None], 2, 1) * 32767).astype(np.int16)
with wave.open("sfx/whoosh.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())
