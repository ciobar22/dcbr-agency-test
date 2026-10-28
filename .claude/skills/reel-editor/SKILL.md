---
name: reel-editor
description: Edit raw talking-head footage into viral vertical reels (Instagram Reels / TikTok / Shorts) in the Martina Bacci style — hook-first cut, jump cuts, face-tracked punch-in zooms, face retouch, animated word-by-word captions with custom fonts, SFX, music bed, end glow. Use when the user asks to edit a video/reel, "editare i video di Martina", pick viral hooks or highlights from raw clips, add captions/zoom/effects/sounds, or retouch a face in video.
---

# Reel editor (DCBR)

Pipeline lives in `video-editing/scripts/` (repo root). Everything is local: ffmpeg + Python.
Claude does the editorial work (hook + highlights + emphasis words); the scripts do the craft.

## Setup (once per machine)
```bash
# macOS
brew install ffmpeg            # must include libass (brew's does)
pip3 install numpy scipy opencv-python-headless mediapipe faster-whisper
export REEL_FONTS="$(git rev-parse --show-toplevel)/video-editing/fonts"   # Poppins + DM Serif (OFL)
```
`render.py` downloads the MediaPipe face model on first run (~4 MB, storage.googleapis.com);
`transcribe.py` downloads the Whisper model on first run (Hugging Face). Without mediapipe it falls
back to OpenCV face boxes (retouch becomes ellipse + skin-colour mask).

## Workflow — for EACH raw video
1. **Inspect**: `ffprobe` duration/res/fps; contact sheet to see framing:
   `ffmpeg -i raw.mp4 -vf "fps=1/2,scale=180:-2,tile=8x3" -frames:v 1 sheet.jpg` → look at it.
2. **Transcribe** (word timestamps):
   `python3 video-editing/scripts/transcribe.py raw.mp4 -o raw.words.json --model medium`
   (`small` is faster; `medium` handles Roman dialect + slang much better).
3. **Pick the edit** (Claude's job — read the printed transcript):
   - **Hook (0–2s)**: the most provocative / polarising / curiosity-gap line in the whole clip,
     moved to the very start (cold open) even if it was said later. Must make sense alone.
   - **Highlights**: keep only the lines that build or pay off the hook; cut setup, repetitions,
     "ehm", false starts. Target 15–30s (Martina's top reels: 16–28s). One idea per reel.
   - Long raw clip → several reels, each with its own hook. Never take a line out of context
     so that it flips its meaning.
   - **Ending**: last line = punchline or open loop (makes people comment/rewatch). Glow on it.
   - **Emphasis words**: 3–6 punch words (get pop SFX + zoom bump + accent colour).
4. **Write `plan.json`** next to the video (schema below) and render:
   `python3 video-editing/scripts/render.py plan.json --preview` → review → final without `--preview`.
5. **QA before delivering** (never skip):
   - contact sheet of the output + 3–4 full-size frames (hook, a zoom, an emphasis, the end);
   - captions: spelling, censoring, nothing covering the face, inside safe zone (y 0.15–0.75);
   - `ffmpeg -i out.mp4 -af ebur128 -f null -` → integrated ≈ -14 LUFS;
   - retouch natural (no plastic skin), face never cropped at the top on max zoom.
6. Deliver `out.mp4` + `work_*/captions.srt` (for CapCut/IG) + a short note: chosen hook,
   cut lines, suggested on-screen title & caption, suggestion to add a trending sound in-app.

## plan.json
```json
{
  "input": "raw/IMG_1234.MOV",
  "words": "raw/IMG_1234.words.json",
  "output": "out/reel_01.mp4",
  "style": "serif",
  "ranges": [
    {"start": 41.20, "end": 44.10},
    {"start": 3.05,  "end": 18.40},
    {"start": 52.00, "end": 55.30, "zoom": 1.3}
  ],
  "tighten": 0.35,
  "zoom_cycle": [1.0, 1.22, 1.08, 1.35],
  "hook": {"text": "NON HO AMICI\nCON CUI NON VADO A LETTO", "dur": 2.4},
  "emphasis": ["letto", "amicizia", "esiste"],
  "retouch": 0.55,
  "glow_end": 1.6,
  "music_db": -20,
  "bpm": 98,
  "caption_y": 0.62,
  "face_y": 0.32,
  "sfx": true,
  "sfx_events": [{"t": 9.4, "name": "record_stop", "gain": 0.35}]
}
```
- `ranges` are SOURCE seconds in OUTPUT order (hook first). `tighten` splits each range at pauses
  longer than N s and removes them (jump cuts); each piece alternates `zoom_cycle` unless it sets
  its own `zoom`. Pieces < 0.7s keep the previous framing.
- `style`: `serif` = one word at a time, DM Serif Display, white→teal karaoke fill (as @marti__marti98);
  `sans` = 2–3 lowercase words, Poppins SemiBold cream with soft shadow (as @latuamartimarti).
- `retouch` 0–1 skin smoothing strength (0.4–0.6 natural). `glow_end` seconds of dreamy glow +
  sparkles on the final line. `music_db` bed level before ducking (-18 louder … -24 subtle).
- SFX library (synthesised, license-free): `whoosh`, `whoosh_down`, `swish`, `pop`, `boom`,
  `sparkle`, `riser`, `record_stop`. Auto: boom at 0, swish on punch-ins, pop on emphasis, sparkle
  on the glow. `sfx_events` times are OUTPUT seconds.
- Profanity in captions is auto-censored (c***o, sc*****) like the reference reels; audio is not.

## Reference style — Martina Bacci (studied 2026-10-28)
Accounts: @latuamartimarti (326k plays on ref reel DejJXTxOyQv), @marti__marti98 (ref De93aAXSQuD).
- Format: 9:16, 15–30s, talking head seated (armchair grey studio / white sofa), full-body wide.
- Hook from frame 0: the spiciest line, no intro. Provocative relationship/sex/dating opinions.
- Cuts: hard jump cuts every ~2–5s alternating wide ↔ punch-in (knees-up / waist-up). No slow pans.
- Captions mid-frame (chest/waist), never top; censored swear words with asterisks.
- Inserts: cut-out sticker pop-ins with coloured outline (e.g. a car sliding in on "ammazza"),
  B&W reaction cutaways of other people, glow + sparkles on the final punchline.
- Audio: original voice upfront, continuous quiet bed under it, mastered ≈ -14 LUFS.
- Skin: smooth, warm, bright (beauty-retouched look).

## Not automated yet (do by hand / in CapCut if asked)
Cut-out stickers & B&W meme cutaways need assets (PNG with alpha / clips): overlay with ffmpeg
`overlay` + `format=gray` for B&W. Trending sounds must be added in the IG/TikTok app (licensed there);
the built-in bed is original and safe for any platform.
