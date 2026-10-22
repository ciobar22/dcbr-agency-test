# Adds a native-Italian voiceover (edge-tts neural voices, free) to the v2 edits.
# usage: vo.py ID   (needs work/ID/base timing, out/DCBR_v2_adID_solo-effetti.mp4, sfx/, music/)
import sys, os, json, subprocess, asyncio, wave
import numpy as np
import edge_tts

SR = 48000
ID = sys.argv[1]
VO = {
    "01": dict(voice="it-IT-GiuseppeMultilingualNeural", rate=6, pitch=0, lines=[
        (0.10, "I social? Li fa mio nipote."),
        (2.45, "La strategia? Balletti con il trapano."),
        (5.20, "Risultato: tre like."),
        (6.85, "Uno è di sua madre."),
        (8.30, "Tuo nipote ti vuole bene."),
        (9.75, "Noi ti portiamo clienti."),
        (11.30, "Di Ci Bi Erre. Scrivici."),
    ]),
    "06": dict(voice="it-IT-IsabellaNeural", rate=4, pitch=0, lines=[
        (0.15, "Lui ha la fila."),
        (1.45, "Tu hai il gelato più buono."),
        (3.15, "Ma lui è ovunque sui social."),
        (4.95, "E tu no."),
        (6.60, "Non vince il migliore."),
        (8.80, "Vince chi si fa vedere."),
        (11.50, "Di Ci Bi Erre. Scrivici."),
    ]),
    "09": dict(voice="it-IT-GiuseppeMultilingualNeural", rate=-4, pitch=-2, lines=[
        (0.20, "Locale perfetto."),
        (1.55, "Sala vuota."),
        (3.25, "Il problema non è la cucina."),
        (6.25, "È che nessuno ti conosce."),
        (8.60, "Noi ti facciamo trovare."),
        (11.05, "Di Ci Bi Erre. Scrivici."),
    ]),
}[ID]

tl = json.load(open(f"work/{ID}/timeline.json"))
total = tl["dur"]
os.makedirs(f"work/{ID}/vo", exist_ok=True)

def readwav(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        return x.reshape(-1, w.getnchannels())

def writewav(p, x):
    with wave.open(p, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())

async def tts(text, rate, path):
    c = edge_tts.Communicate(text, VO["voice"], rate=f"{rate:+d}%", pitch=f"{VO['pitch']:+d}Hz")
    await c.save(path)

def make_line(i, text, rate):
    mp3, wav = f"work/{ID}/vo/{i}.mp3", f"work/{ID}/vo/{i}.wav"
    asyncio.run(tts(text, rate, mp3))
    # trim silence, broadcast-style voice chain: HPF, gentle presence lift, compression
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-af",
                    "silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                    "silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                    "highpass=f=85,equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=250:t=q:w=1:g=-1.5,"
                    "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=3",
                    "-ar", str(SR), "-ac", "2", wav], check=True)
    return readwav(wav)

N = int(total * SR)
vo = np.zeros((N, 2), np.float32)
report = []
lines = VO["lines"]
for i, (t0, text) in enumerate(lines):
    limit = (lines[i + 1][0] if i + 1 < len(lines) else total - 0.15) - t0 - 0.05
    rate = VO["rate"]
    x = make_line(i, text, rate)
    while len(x) / SR > limit and rate < VO["rate"] + 12:  # speed up only as much as needed
        rate += 4; x = make_line(i, text, rate)
    a = int(t0 * SR); L = min(len(x), N - a)
    vo[a:a + L] += x[:L]
    report.append(("!! " if len(x)/SR>limit else "   ")+f"{t0:5.2f}s {len(x)/SR:4.2f}s/{limit:4.2f}s rate{rate:+d}% {text}")
vo *= 0.89 / (np.max(np.abs(vo)) + 1e-9)

# ducking envelope from the voice (fast attack, slow release)
env = np.abs(vo).max(1)
k = int(0.02 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
act = (env > 0.02).astype(np.float32)
rel = int(0.35 * SR); act = np.convolve(act, np.ones(rel) / rel, mode="full")[:N]
act = np.clip(act * 3, 0, 1)

fx = readwav(f"work/{ID}/A.wav")[:N]                     # SFX bed from the v2 edit
if len(fx) < N: fx = np.pad(fx, ((0, N - len(fx)), (0, 0)))
m = readwav(f"music/{ID}.wav")[:N]
if len(m) < N: m = np.pad(m, ((0, N - len(m)), (0, 0)))
fade = np.ones(N); fo = int(0.9 * SR); fade[-fo:] = np.linspace(1, 0, fo) ** 1.5

def master(x, target_rms=0.19):
    x = np.tanh(x * 1.2) / np.tanh(1.2)
    return x * min(target_rms / (np.sqrt(np.mean(x ** 2)) + 1e-9), 0.89 / (np.max(np.abs(x)) + 1e-9))

fxg = fx * (1 - 0.7 * act[:, None])                     # SFX tucked under the voice
A = master(vo * 1.0 + fxg * 0.32)
B = master(vo * 1.0 + fxg * 0.3 + m * fade[:, None] * (0.42 - 0.30 * act[:, None]))
writewav(f"work/{ID}/VA.wav", A); writewav(f"work/{ID}/VB.wav", B)

for tag, wavp in (("voce", "VA"), ("voce-musica", "VB")):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"out/DCBR_v2_ad{ID}_solo-effetti.mp4", "-i", f"work/{ID}/{wavp}.wav",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-t", f"{total:.3f}", "-movflags", "+faststart", f"out/DCBR_v3_ad{ID}_{tag}.mp4"], check=True)
print(ID, "VO ok\n" + "\n".join(report))
