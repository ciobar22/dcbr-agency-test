# usage: edit.py ID  (expects raw/ID.mp4, vo/ID.mp3, music/MOOD.wav, sfx/whoosh.wav)
import sys, json, re, subprocess, unicodedata, difflib
ID = sys.argv[1]
cfg = json.load(open("ads.json"))[ID]
VDUR = 15.104
VO_START = 0.25

def run(cmd):
    subprocess.run(cmd, check=True)

def probe(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip())

# 1. clean VO: trim leading/trailing silence, speed up if needed so it ends by ~12.9s
run(["ffmpeg", "-v", "error", "-y", "-i", f"vo/{ID}.mp3", "-af",
     "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.22:stop_threshold=-45dB:stop_silence=0.18,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
     "-ar", "44100", "-ac", "2", f"work/{ID}_vo0.wav"])
d = probe(f"work/{ID}_vo0.wav")
tempo = max(1.0, d / 12.55)
if tempo > 1.0:
    run(["ffmpeg", "-v", "error", "-y", "-i", f"work/{ID}_vo0.wav", "-af", f"atempo={tempo:.4f}", f"work/{ID}_vo.wav"])
else:
    run(["cp", f"work/{ID}_vo0.wav", f"work/{ID}_vo.wav"])
d = probe(f"work/{ID}_vo.wav")
vo_end = VO_START + d
T = min(13.1, max(12.0, vo_end + 0.25))  # end card start

# 2. word timings from whisper, aligned onto the script tokens
from faster_whisper import WhisperModel
model = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = model.transcribe(f"work/{ID}_vo.wav", language="it", word_timestamps=True, initial_prompt=cfg["text"])
ww = [(w.word.strip(), w.start + VO_START, w.end + VO_START) for s in segs for w in s.words]

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))

toks = cfg["text"].split()
a = [norm(t) for t in toks]
b = [norm(w[0]) for w in ww]
times = [None] * len(toks)
for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
    for k in range(blk.size):
        times[blk.a + k] = (ww[blk.b + k][1], ww[blk.b + k][2])
# interpolate gaps
known = [i for i, x in enumerate(times) if x]
if not known:
    times = [(VO_START + d * i / len(toks), VO_START + d * (i + 1) / len(toks)) for i in range(len(toks))]
else:
    for i in range(len(toks)):
        if times[i]: continue
        p = max([k for k in known if k < i], default=None)
        n = min([k for k in known if k > i], default=None)
        s = times[p][1] if p is not None else VO_START
        e = times[n][0] if n is not None else vo_end
        lo = p if p is not None else -1
        hi = n if n is not None else len(toks)
        span = (e - s) / (hi - lo - 1)
        times[i] = (s + span * (i - lo - 1), s + span * (i - lo))

# collapse "Di Ci Bi Erre" -> "DCBR"
words = []
i = 0
while i < len(toks):
    if [norm(t) for t in toks[i:i + 4]] == ["di", "ci", "bi", "erre"]:
        punct = re.sub(r"[\w']", "", toks[i + 3])
        words.append(["DCBR" + punct, times[i][0], times[i + 3][1]]); i += 4
    else:
        words.append([toks[i], times[i][0], times[i][1]]); i += 1

# 3. ASS subtitles
def ts(x):
    x = max(0, x); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def clean(w):
    w = w.replace("...", "")
    keep_q = w.endswith("?")
    w = re.sub(r"[.,:;!?]+$", "", w)
    return w.upper() + ("?" if keep_q else "")

chunks, cur = [], []
for k, w in enumerate(words):
    cur.append(w)
    end_punct = re.search(r"[.,:;!?]$", w[0]) or w[0].endswith("...")
    gap = words[k + 1][1] - w[2] if k + 1 < len(words) else 9
    if len(cur) == 3 or end_punct or gap > 0.35:
        chunks.append(cur); cur = []
if cur: chunks.append(cur)

ev = []
YEL, WHT = r"{\c&H0000D4FF&}", r"{\c&H00FFFFFF&}"
for ci, ch in enumerate(chunks):
    cend = chunks[ci + 1][0][1] if ci + 1 < len(chunks) else ch[-1][2] + 0.35
    cend = min(cend, ch[-1][2] + 0.6, T)
    for wi, w in enumerate(ch):
        s = w[1]
        e = ch[wi + 1][1] if wi + 1 < len(ch) else cend
        if s >= T: continue
        e = min(e, T)
        if e <= s: continue
        txt = " ".join((YEL if j == wi else WHT) + clean(x[0]) for j, x in enumerate(ch))
        pop = r"{\fscx88\fscy88\t(0,90,\fscx100\fscy100)}" if wi == 0 else ""
        ev.append(f"Dialogue: 1,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\pos(540,1230)}}{pop}{txt}")

ev.append(f"Dialogue: 2,{ts(0.15)},{ts(2.9)},Hook,,0,0,0,,{{\\pos(540,330)\\fad(120,200)\\fscx92\\fscy92\\t(0,140,\\fscx100\\fscy100)}}{cfg['hook']}")
E = ts(VDUR)
ev += [
    f"Dialogue: 3,{ts(T + 0.10)},{E},Brand,,0,0,0,,{{\\pos(540,800)\\fad(250,0)\\fscx70\\fscy70\\t(0,260,\\fscx100\\fscy100)}}DCBR",
    f"Dialogue: 3,{ts(T + 0.30)},{E},Sub,,0,0,0,,{{\\pos(540,940)\\fad(250,0)}}A G E N C Y",
    f"Dialogue: 3,{ts(T + 0.55)},{E},Small,,0,0,0,,{{\\pos(540,1040)\\fad(250,0)}}Marketing per piccole e medie imprese",
    f"Dialogue: 3,{ts(T + 0.85)},{E},Cta,,0,0,0,,{{\\pos(540,1210)\\fad(200,0)\\fscx80\\fscy80\\t(0,180,\\fscx106\\fscy106)\\t(180,300,\\fscx100\\fscy100)}}SCRIVICI IN DM",
]
head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat ExtraBold,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,3,5,60,60,0,1
Style: Hook,Montserrat ExtraBold,62,&H00FFFFFF,&H00FFFFFF,&H00FF6B2F,&H00FF6B2F,0,0,0,0,100,100,1,0,3,20,0,5,60,60,0,1
Style: Brand,Montserrat ExtraBold,230,&H00FFFFFF,&H00FFFFFF,&H00FF6B2F,&H00000000,0,0,0,0,100,100,4,0,1,0,0,5,0,0,0,1
Style: Sub,Montserrat ExtraBold,52,&H00FF8A5A,&H00FF8A5A,&H00000000,&H00000000,0,0,0,0,100,100,6,0,1,0,0,5,0,0,0,1
Style: Small,Metropolis Extra Bold,40,&H00E6E6E6,&H00E6E6E6,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Cta,Montserrat ExtraBold,64,&H00111111,&H00111111,&H0000D4FF,&H0000D4FF,0,0,0,0,100,100,1,0,3,26,0,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(f"work/{ID}.ass", "w").write(head + "\n".join(ev) + "\n")

# 4. render
fc = (
    f"[0:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.5,split[a][b];"
    f"[b]gblur=sigma=28,eq=brightness=-0.28:saturation=0.75,format=yuva420p,fade=t=in:st={T:.2f}:d=0.35:alpha=1[bb];"
    f"[a][bb]overlay,ass=work/{ID}.ass,format=yuv420p[v];"
    f"[1:a]adelay={int(VO_START*1000)}:all=1,apad,asplit[vo][sc];"
    f"[2:a]volume=0.30[m];[m][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[md];"
    f"[3:a]asplit[w1][w2];[w1]volume=0.35[w1v];[w2]adelay={int((T-0.2)*1000)}:all=1,volume=0.6[w2v];"
    f"[vo][md][w1v][w2v]amix=inputs=4:normalize=0:duration=first,atrim=0:{VDUR},"
    f"loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[aout]"
)
run(["ffmpeg", "-v", "error", "-y", "-i", f"raw/{ID}.mp4", "-i", f"work/{ID}_vo.wav", "-i", f"music/{cfg['mood']}.wav", "-i", "sfx/whoosh.wav",
     "-filter_complex", fc, "-map", "[v]", "-map", "[aout]", "-t", str(VDUR),
     "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"out/DCBR_ad{ID}.mp4"])
print(json.dumps({"id": ID, "vo_dur": round(d, 2), "tempo": round(tempo, 3), "endcard": round(T, 2),
                  "matched": f"{sum(1 for x in times if x)}/{len(toks)}", "whisper": " ".join(w[0] for w in ww)}))
