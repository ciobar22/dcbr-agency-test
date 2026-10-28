Edit the raw videos in this folder (`~/Desktop/edit martina`) into viral Instagram reels in the style of Martina Bacci (@latuamartimarti, @marti__marti98). The reference reels are ONLY a style reference for the final result: https://www.instagram.com/reel/DejJXTxOyQv/ and https://www.instagram.com/reel/De93aAXSQuD/

## 1. Setup (once)
The pipeline and the `reel-editor` skill are already built and tested, in the GitHub repo `ciobar22/dcbr-agency-test`, branch `claude/lucid-feynman-vh90mx`:
```bash
cd ~ && git clone -b claude/lucid-feynman-vh90mx https://github.com/ciobar22/dcbr-agency-test.git
mkdir -p ~/.claude/skills && cp -r ~/dcbr-agency-test/.claude/skills/reel-editor ~/.claude/skills/
brew install ffmpeg
pip3 install numpy scipy opencv-python-headless mediapipe faster-whisper
export REEL_FONTS=~/dcbr-agency-test/video-editing/fonts
```
(If the clone asks for credentials: `gh auth login`, or download the branch ZIP from GitHub.)
Then read `~/.claude/skills/reel-editor/SKILL.md` and follow it: it has the workflow, the `plan.json` schema and the style guide.
Scripts: `~/dcbr-agency-test/video-editing/scripts/` (`transcribe.py`, `render.py`, `sfx.py`).

## 2. What to do for EACH video in the folder
1. Look at it (ffprobe + a frame contact sheet) and transcribe it word by word:
   `python3 ~/dcbr-agency-test/video-editing/scripts/transcribe.py VIDEO -o VIDEO.words.json --model medium`
2. **Pick the highlights and the viral hooks**: the spiciest or most polarising line goes in the first 2 seconds (cold open, even if it was said later). Keep only the lines that build or pay it off, cut dead air, repetitions and "ehm". Target 15–30s. If a video is long, make several reels, each with its own hook. End on the punchline. Never cut a line in a way that changes its meaning.
3. Write a `plan.json` (hook first, a big on-screen hook title, 3–6 emphasis words, `retouch` 0.5–0.6, `glow_end` 1.5) and render: `python3 .../render.py plan.json --preview`, then do the final render without `--preview`.
4. Quality check: look at a contact sheet of the output and 4 full-size frames (hook, zoom, emphasis word, ending). Check caption spelling and censoring, that no caption covers the face, that the retouch looks natural, and that loudness is ≈ -14 LUFS.
5. Put the results in `~/Desktop/edit martina/EXPORT/` (mp4 + .srt), plus a short note per reel: the hook you chose, what you cut, and a suggested IG caption.

## 3. What the pipeline already does (tested)
- Hook-first cut + automatic jump cuts (pauses removed), a punch-in cut every ~3s alternating wide and tight framing, centred on the face (two-stage face tracking: YuNet + MediaPipe mesh)
- Face retouching: skin smoothing that keeps texture and slightly brightens the skin (eyes, lips and eyebrows are excluded)
- Animated captions: `serif` = one word at a time in DM Serif Display with white→teal karaoke fill (@marti__marti98 style) or `sans` = 2–3 lowercase words in cream Poppins (@latuamartimarti style); emphasis words in colour with a zoom pop; swear words censored (c***o)
- Hook title box in Poppins ExtraBold at the top for the first ~2.4s
- Sounds: boom on the hook, swish on the zooms, pop on the emphasis words, sparkle on the ending; original licence-free music bed that ducks under the voice; master at -14 LUFS
- Dreamy glow + sparkles on the final line

## 4. Do by hand if needed / ask me
Cut-out sticker pop-ins and black-and-white meme cutaways (they need PNG/clip assets); trending music should be added in the IG app (licensed there).
