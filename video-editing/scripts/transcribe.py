#!/usr/bin/env python3
"""Word-level transcription (faster-whisper) -> words.json + readable transcript with pauses.

Usage: python3 transcribe.py raw.mp4 -o words.json [--model medium] [--lang it]
"""
import argparse
import json

from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("-o", "--out", default="words.json")
ap.add_argument("--model", default="small")
ap.add_argument("--lang", default="it")
a = ap.parse_args()

model = WhisperModel(a.model, device="cpu", compute_type="int8")
segs, info = model.transcribe(a.video, language=a.lang, word_timestamps=True, vad_filter=True, beam_size=5)
out = {"language": info.language, "duration": info.duration, "segments": []}
for s in segs:
    out["segments"].append({
        "start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(),
        "words": [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 2)}
                  for w in s.words],
    })
with open(a.out, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

prev_end = 0.0
for s in out["segments"]:
    gap = s["start"] - prev_end
    if gap > 0.6:
        print(f"         ... pausa {gap:.1f}s")
    print(f'[{s["start"]:7.2f}-{s["end"]:7.2f}] {s["text"]}')
    prev_end = s["end"]
