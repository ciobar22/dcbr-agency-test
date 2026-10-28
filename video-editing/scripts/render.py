#!/usr/bin/env python3
"""DCBR reel renderer: plan.json -> finished vertical reel (1080x1920, 30fps, -14 LUFS).

Pipeline: CFR transcode -> hook-first cut + jump-cut tightening -> face tracking ->
skin retouch + face-anchored punch-in zooms + emphasis bumps + end glow ->
animated ASS captions + hook title -> voice + ducked music bed + SFX mix.

Usage: python3 render.py plan.json [--work work_dir] [--preview]
See ../README.md / the reel-editor skill for the plan.json schema.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sfx  # noqa: E402

OW, OH, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.environ.get("REEL_FONTS", os.path.join(HERE, "..", "fonts"))
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/face_landmarker/"
             "face_landmarker/float16/1/face_landmarker.task")
YUNET_URL = ("https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/"
             "face_detection_yunet_2023mar.onnx")

# Caption presets, modelled on the Martina Bacci reference reels.
STYLES = {
    # @marti__marti98: one word at a time, high-contrast serif, white -> teal karaoke fill
    "serif": dict(font="DM Serif Display", size=112, primary="#5FB7C9", secondary="#FFFFFF",
                  outline="#141414", outline_w=3, shadow=2, mode="word", emph="#FF5FA2"),
    # @latuamartimarti: 2-3 word chunks, lowercase, cream geometric sans with soft shadow
    "sans": dict(font="Poppins SemiBold", size=80, primary="#F4E7B2", secondary="#F4E7B2",
                 outline="#000000", outline_w=0, shadow=4, mode="chunk", emph="#FFD23F"),
}

FACE_OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377,
             152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
LEFT_EYE = [263, 249, 390, 373, 374, 380, 381, 382, 362, 398, 384, 385, 386, 387, 388, 466]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
LEFT_BROW = [276, 283, 282, 295, 285, 300, 293, 334, 296, 336]
RIGHT_BROW = [46, 53, 52, 65, 55, 70, 63, 105, 66, 107]
LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185]

BAD = ("cazz", "scop", "stronz", "troi", "puttan", "fott", "minchi", "merd", "sborr", "coglion",
       "zoccol", "mignott", "sc*")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"command failed: {' '.join(cmd[:6])}...\n{r.stderr[-3000:]}")
    return r.stdout


def probe_duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]))


# ---------------------------------------------------------------- timeline

def flat_words(words):
    return [w for s in words["segments"] for w in s["words"]]


def build_timeline(plan, words):
    """Turn plan ranges (source seconds, output order) into frame-aligned pieces with zooms."""
    gap = plan.get("tighten", 0.35)
    pad_in, pad_out = plan.get("pad_in", 0.06), plan.get("pad_out", 0.10)
    fw = flat_words(words)
    pieces = []
    for r in plan["ranges"]:
        a, b = r["start"], r["end"]
        extra = {k: v for k, v in r.items() if k not in ("start", "end")}
        ws = [w for w in fw if w["s"] >= a - 0.05 and w["e"] <= b + 0.05]
        if not ws or not gap:
            pieces.append(dict(start=a, end=b, **extra))
            continue
        groups, cur = [], [ws[0]]
        for w in ws[1:]:
            if w["s"] - cur[-1]["e"] > gap:
                groups.append(cur)
                cur = [w]
            else:
                cur.append(w)
        groups.append(cur)
        for g in groups:
            # long continuous takes get punch-in cuts every ~max_shot s, at the widest word gap
            max_shot = plan.get("max_shot", 3.2)
            while g[-1]["e"] - g[0]["s"] > max_shot * 1.4:
                cands = [k for k in range(1, len(g)) if 1.8 <= g[k]["s"] - g[0]["s"] <= max_shot]
                if not cands:
                    break
                k = max(cands, key=lambda k: g[k]["s"] - g[k - 1]["e"])
                mid = (g[k - 1]["e"] + g[k]["s"]) / 2
                pieces.append(dict(start=max(a, g[0]["s"] - pad_in), end=mid, **extra))
                g = g[k:]
                g[0] = dict(g[0], s=mid + pad_in)
            pieces.append(dict(start=max(a, g[0]["s"] - pad_in), end=min(b, g[-1]["e"] + pad_out), **extra))
    cycle = plan.get("zoom_cycle", [1.0, 1.22, 1.08, 1.35])
    out, t, ci, prev_zoom = [], 0, 0, None
    for p in pieces:
        p["start"] = round(p["start"] * FPS) / FPS
        p["end"] = round(p["end"] * FPS) / FPS
        if p["end"] - p["start"] < 2 / FPS:
            continue
        p["dur"] = p["end"] - p["start"]
        if "zoom" not in p:
            # short fragments keep the framing so the cut reads as a jump cut, not a zoom spasm
            if prev_zoom is not None and p["dur"] < 0.7:
                p["zoom"] = prev_zoom
            else:
                p["zoom"] = cycle[ci % len(cycle)]
                ci += 1
        p.setdefault("push", 0.035)
        p["t0"], p["t1"] = t, t + p["dur"]
        t += p["dur"]
        prev_zoom = p["zoom"]
        out.append(p)
    return out, t


def remap_words(pieces, fw):
    out = []
    for p in pieces:
        for w in fw:
            s, e = max(w["s"], p["start"]), min(w["e"], p["end"])
            if e - s < 0.04:
                continue
            out.append(dict(w=w["w"], s=p["t0"] + s - p["start"], e=p["t0"] + e - p["start"]))
    return out


def cut(src, pieces, work):
    """Frame-accurate hook-first edit: CFR copy, then trim+concat video and audio together."""
    src30 = os.path.join(work, "src30.mov")
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf",
         "fps=30,scale='if(gt(ih,2880),-2,iw)':'if(gt(ih,2880),2880,ih)'",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p",
         "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", src30])
    fc = []
    for i, p in enumerate(pieces):
        # no de-click fades where the next piece continues the same take (punch-in only)
        cont_in = i > 0 and abs(pieces[i - 1]["end"] - p["start"]) < 1e-3
        cont_out = i + 1 < len(pieces) and abs(pieces[i + 1]["start"] - p["end"]) < 1e-3
        fades = ("" if cont_in else ",afade=t=in:d=0.008") + \
            ("" if cont_out else f",afade=t=out:st={max(p['dur'] - 0.012, 0):.4f}:d=0.012")
        fc.append(f"[0:v]trim=start={p['start']:.4f}:end={p['end']:.4f},setpts=PTS-STARTPTS[v{i}]")
        fc.append(f"[0:a]atrim=start={p['start']:.4f}:end={p['end']:.4f},asetpts=PTS-STARTPTS{fades}[a{i}]")
    n = len(pieces)
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
    cutp, voice = os.path.join(work, "cut.mp4"), os.path.join(work, "voice.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", src30, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", cutp,
         "-map", "[a]", "-ar", "48000", "-ac", "2", voice])
    return cutp, voice


# ---------------------------------------------------------------- face

def cached(url, name):
    path = os.path.join(os.path.expanduser("~/.cache/reel"), name)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        urllib.request.urlretrieve(url, path)
    return path


class FaceFinder:
    """Full-frame face box (x, y, w, h): YuNet handles small full-body faces; Haar is the last resort."""

    def __init__(self):
        self.yn = None
        try:
            self.yn = cv2.FaceDetectorYN.create(cached(YUNET_URL, "yunet.onnx"), "", (320, 320), 0.6)
        except Exception:
            self.casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def __call__(self, fr):
        sc = 960 / max(fr.shape[:2])
        small = cv2.resize(fr, None, fx=sc, fy=sc)
        if self.yn is not None:
            self.yn.setInputSize((small.shape[1], small.shape[0]))
            f = self.yn.detect(small)[1]
            f = [] if f is None else [r[:4] for r in f]
        elif not self.casc.empty():
            f = self.casc.detectMultiScale(cv2.cvtColor(small, cv2.COLOR_BGR2GRAY), 1.08, 5, minSize=(24, 24))
        else:
            f = []
        return np.array(max(f, key=lambda b: b[2] * b[3]), np.float32) / sc if len(f) else None


def crop_square(img, cx, cy, S):
    x0, y0 = int(cx - S / 2), int(cy - S / 2)
    pad = max(0, -x0, -y0, x0 + S - img.shape[1], y0 + S - img.shape[0])
    if pad:
        img = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_REPLICATE)
    return img[y0 + pad:y0 + pad + S, x0 + pad:x0 + pad + S], (x0, y0)


def track_faces(path, work):
    """Per-frame 478-point landmarks (full-res coords) or None; plain face boxes without mediapipe.

    Two-stage so small faces in wide shots still get a mesh: a detector finds the face, the landmarker
    runs on an upscaled square crop around it, and the next frame reuses the previous face as ROI.
    """
    cap = cv2.VideoCapture(path)
    find = FaceFinder()
    res = []
    try:
        import mediapipe as mp
        from mediapipe.tasks import python as mpt
        from mediapipe.tasks.python import vision
    except ImportError:
        while True:
            ok, fr = cap.read()
            if not ok:
                break
            res.append(find(fr))
        return res, "box"
    opts = vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=cached(MODEL_URL,
                                                                                             "face_landmarker.task")),
                                        running_mode=vision.RunningMode.IMAGE, num_faces=1)
    lm = vision.FaceLandmarker.create_from_options(opts)
    prev = None  # (cx, cy, size) of the last good face
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        pts = None
        for attempt in range(2):
            roi = prev
            if roi is None:
                b = find(fr)
                roi = (b[0] + b[2] / 2, b[1] + b[3] / 2, max(b[2], b[3])) if b is not None else None
            if roi is None:
                break
            S = max(int(roi[2] * 2.2), 64)
            crop, (ox, oy) = crop_square(fr, roi[0], roi[1], S)
            crop = cv2.cvtColor(cv2.resize(crop, (384, 384), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2RGB)
            r = lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=crop))
            if r.face_landmarks:
                pts = np.array([[p.x * S + ox, p.y * S + oy] for p in r.face_landmarks[0]], np.float32)
                o = pts[FACE_OVAL]
                prev = (o[:, 0].mean(), o[:, 1].mean(), float((o.max(0) - o.min(0)).max()))
                break
            prev = None  # lost: run the full-frame detector on the second attempt
        res.append(pts)
    lm.close()
    return res, "mesh"


def face_centers(tracks, kind, pieces, size):
    """Smoothed face centre per frame (no smoothing across cuts)."""
    W, H = size
    c = []
    for t in tracks:
        if t is None:
            c.append(None)
        elif kind == "mesh":
            o = t[FACE_OVAL]
            c.append([o[:, 0].mean(), o[:, 1].mean()])
        else:
            c.append([t[0] + t[2] / 2, t[1] + t[3] / 2])
    last = next((x for x in c if x is not None), [W / 2, H * 0.3])
    for i, x in enumerate(c):
        if x is None:
            c[i] = last
        last = c[i]
    c = np.array(c, np.float32)
    out = c.copy()
    sig = 0.35 * FPS
    k = np.exp(-0.5 * (np.arange(-int(3 * sig), int(3 * sig) + 1) / sig) ** 2)
    for p in pieces:
        a, b = int(round(p["t0"] * FPS)), min(int(round(p["t1"] * FPS)), len(c))
        if b - a < 3:
            continue
        seg = c[a:b]
        padded = np.pad(seg, ((len(k) // 2, len(k) // 2), (0, 0)), mode="edge")
        for d in range(2):
            out[a:b, d] = np.convolve(padded[:, d], k / k.sum(), mode="valid")[:b - a]
    return out


def skin_mask(shape, pts):
    m = np.zeros(shape[:2], np.uint8)
    cv2.fillPoly(m, [pts[FACE_OVAL].astype(np.int32)], 255)
    for idx, grow in ((LEFT_EYE, 1.45), (RIGHT_EYE, 1.45), (LIPS, 1.12), (LEFT_BROW, 1.25), (RIGHT_BROW, 1.25)):
        poly = pts[idx]
        cen = poly.mean(0)
        cv2.fillPoly(m, [cv2.convexHull(((poly - cen) * grow + cen).astype(np.int32))], 0)
    return m


def retouch(frame, track, kind, strength):
    """Beauty pass: edge-preserving skin smoothing that keeps pore texture, slight skin lift."""
    if track is None or strength <= 0:
        return frame
    H, W = frame.shape[:2]
    if kind == "mesh":
        o = track[FACE_OVAL]
        x0, y0 = o.min(0)
        x1, y1 = o.max(0)
    else:
        x0, y0, bw, bh = track
        x1, y1 = x0 + bw, y0 + bh
    fw = x1 - x0
    m = int(fw * 0.15)
    X0, Y0 = max(int(x0) - m, 0), max(int(y0) - m, 0)
    X1, Y1 = min(int(x1) + m, W), min(int(y1) + m, H)
    if X1 - X0 < 20 or Y1 - Y0 < 20:
        return frame
    roi = frame[Y0:Y1, X0:X1]
    if kind == "mesh":
        mask = skin_mask(roi.shape, track - [X0, Y0])
    else:
        mask = np.zeros(roi.shape[:2], np.uint8)
        cv2.ellipse(mask, ((roi.shape[1] / 2, roi.shape[0] / 2), (fw * 0.85, (y1 - y0) * 1.05), 0), 255, -1)
        ycc = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)
        mask &= cv2.inRange(ycc, (0, 133, 77), (255, 173, 127))
    mask = cv2.GaussianBlur(mask, (0, 0), max(fw * 0.025, 1)).astype(np.float32)[..., None] / 255 * strength
    d = int(max(5, fw * 0.035))
    smooth = cv2.bilateralFilter(roi, d, 45, d).astype(np.float32)
    rf = roi.astype(np.float32)
    detail = rf - cv2.GaussianBlur(roi, (0, 0), max(1.0, fw * 0.004)).astype(np.float32)
    out = rf * (1 - mask) + (smooth + detail * 0.45) * mask
    out *= 1 + 0.05 * mask
    frame[Y0:Y1, X0:X1] = np.clip(out, 0, 255).astype(np.uint8)
    return frame


# ---------------------------------------------------------------- look

def bump(t, hits):
    """Quick emphasis punch: snap in 60ms, ease back over ~300ms."""
    z = 0.0
    for h in hits:
        u = (t - h) / 0.36
        if 0 <= u < 1:
            z = max(z, u / 0.17 if u < 0.17 else (1 - (u - 0.17) / 0.83) ** 2)
    return z


def make_sparkles(n=36, seed=4):
    rng = np.random.default_rng(seed)
    pts = []
    while len(pts) < n:
        x, y = rng.uniform(0, OW), rng.uniform(0, OH * 0.85)
        if abs(x - OW / 2) > OW * 0.22 or y < OH * 0.18:  # keep the face/body clear
            pts.append((x, y, rng.uniform(0, 1), rng.uniform(10, 26)))
    return pts


def glow(frame, amt, t, sparkles, edge):
    f = frame.astype(np.float32) / 255
    b = cv2.GaussianBlur(frame, (0, 0), 30).astype(np.float32) / 255
    out = 1 - (1 - f) * (1 - b * amt * 0.45)
    out += edge[..., None] * np.array([1.0, 0.97, 0.92], np.float32) * amt * 0.18
    layer = np.zeros((OH, OW), np.float32)
    for x, y, ph, size in sparkles:
        br = max(0.0, np.sin(2 * np.pi * (t * 1.4 + ph))) ** 3 * amt
        if br < 0.05:
            continue
        L = int(size * (0.5 + br))
        cv2.line(layer, (int(x - L), int(y)), (int(x + L), int(y)), br, 2, cv2.LINE_AA)
        cv2.line(layer, (int(x), int(y - L)), (int(x), int(y + L)), br, 2, cv2.LINE_AA)
        cv2.circle(layer, (int(x), int(y)), 3, br, -1, cv2.LINE_AA)
    layer = layer + cv2.GaussianBlur(layer, (0, 0), 6) * 2
    out += layer[..., None]
    return np.clip(out * 255, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- captions

def ass_color(hexs, alpha=0):
    r, g, b = int(hexs[1:3], 16), int(hexs[3:5], 16), int(hexs[5:7], 16)
    return f"&H{alpha:02X}{b:02X}{g:02X}{r:02X}"


def ass_time(t):
    t = max(t, 0)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def censor(w):
    core = re.sub(r"[^\w*]", "", w.lower())
    if any(core.startswith(b) or (len(b) > 4 and b in core) for b in BAD):
        idx = [i for i, ch in enumerate(w) if ch.isalpha() or ch == "*"]
        if len(idx) > 2:
            keep = {idx[0], idx[-1]} if len(idx) <= 6 else set(idx[:2])
            return "".join(ch if (i in keep or not (ch.isalpha() or ch == "*")) else "*" for i, ch in enumerate(w))
    return w


def clean(w):
    w = re.sub(r"^[\"'«(]+|[\"'».,;:!)…]+$", "", w.strip())
    return w.replace("{", "(").replace("}", ")").replace("\\", "")


def is_emph(w, emph):
    return re.sub(r"[^\w]", "", w.lower()) in emph


def write_ass(path, words, plan, total):
    st = STYLES[plan.get("style", "serif")]
    y = int(OH * plan.get("caption_y", 0.62))
    emph = {e.lower() for e in plan.get("emphasis", [])}
    lower = plan.get("lowercase", True)
    hook = plan.get("hook")
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {OW}", f"PlayResY: {OH}", "WrapStyle: 2",
        "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, "
        "Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
        "MarginL, MarginR, MarginV, Encoding",
        f"Style: Cap,{st['font']},{st['size']},{ass_color(st['primary'])},{ass_color(st['secondary'])},"
        f"{ass_color(st['outline'])},{ass_color('#000000', 0x70)},0,0,0,0,100,100,1,0,1,"
        f"{st['outline_w']},{st['shadow']},5,60,60,0,1",
        f"Style: Hook,Poppins ExtraBold,84,{ass_color('#111111')},{ass_color('#111111')},{ass_color('#FFFFFF')},"
        f"{ass_color('#000000', 0x90)},0,0,0,0,100,100,0,0,3,24,0,8,70,70,{int(OH * 0.12)},1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    pop = r"\fscx72\fscy72\t(0,90,\fscx107\fscy107)\t(90,170,\fscx100\fscy100)"
    srt = []
    if hook:
        txt = hook["text"].replace("\n", r"\N")
        lines.append(f"Dialogue: 2,{ass_time(0)},{ass_time(hook.get('dur', 2.4))},Hook,,0,0,0,,"
                     r"{\fad(0,180)\fscx60\fscy60\t(0,130,\fscx104\fscy104)\t(130,220,\fscx100\fscy100)}" + txt)
    disp = [(censor(clean(w["w"])), w) for w in words]
    disp = [(d, w) for d, w in disp if d]
    if lower:
        disp = [(d.lower(), w) for d, w in disp]
    if st["mode"] == "word":
        for i, (d, w) in enumerate(disp):
            nxt = disp[i + 1][1]["s"] if i + 1 < len(disp) else total
            end = nxt if nxt - w["e"] < 0.6 else w["e"] + 0.25
            kf = max(int((w["e"] - w["s"]) * 100), 8)
            tag = pop + rf"\kf{kf}"
            if is_emph(d, emph):
                tag = (pop.replace("107", "122") + rf"\1c{ass_color(st['emph'])}\2c{ass_color('#FFFFFF')}"
                       rf"\fs{int(st['size'] * 1.22)}\frz-3\kf{kf}")
            lines.append(f"Dialogue: 1,{ass_time(w['s'])},{ass_time(end)},Cap,,0,0,0,,{{\\pos({OW // 2},{y}){tag}}}{d}")
            srt.append((w["s"], end, d))
    else:
        chunks, cur = [], []
        for d, w in disp:
            if cur and (len(cur) >= 3 or len(" ".join(x for x, _ in cur + [(d, w)])) > 18
                        or w["s"] - cur[-1][1]["e"] > 0.25):
                chunks.append(cur)
                cur = []
            cur.append((d, w))
        if cur:
            chunks.append(cur)
        for i, ch in enumerate(chunks):
            s = ch[0][1]["s"]
            nxt = chunks[i + 1][0][1]["s"] if i + 1 < len(chunks) else total
            end = nxt if nxt - ch[-1][1]["e"] < 0.6 else ch[-1][1]["e"] + 0.25
            parts = []
            for d, _ in ch:
                parts.append(rf"{{\1c{ass_color(st['emph'])}}}{d}{{\1c{ass_color(st['primary'])}}}"
                             if is_emph(d, emph) else d)
            lines.append(f"Dialogue: 1,{ass_time(s)},{ass_time(end)},Cap,,0,0,0,,{{\\pos({OW // 2},{y}){pop}}}"
                         + " ".join(parts))
            srt.append((s, end, " ".join(d for d, _ in ch)))
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.splitext(path)[0] + ".srt", "w") as f:
        for i, (s, e, txt) in enumerate(srt, 1):
            fmt = lambda t: f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(t % 1 * 1000):03d}"
            f.write(f"{i}\n{fmt(s)} --> {fmt(e)}\n{txt}\n\n")


# ---------------------------------------------------------------- audio

def build_audio(plan, pieces, words, total, work):
    n = int(total * sfx.SR) + sfx.SR
    track = np.zeros((n, 2))
    lib = {k: f() for k, f in sfx.LIB.items()}

    def place(name, t, gain):
        s = lib[name]
        i = max(int(t * sfx.SR), 0)
        if i < n:
            track[i:i + len(s)] += s[:n - i] * gain

    events = []
    if plan.get("sfx", True):
        events.append(("boom", 0.0, 0.45))
        for a, b in zip(pieces, pieces[1:]):
            if b["zoom"] > a["zoom"] + 0.05:
                events.append(("swish", b["t0"] - 0.14, 0.30))
            elif b["zoom"] < a["zoom"] - 0.05:
                events.append(("whoosh_down", b["t0"] - 0.12, 0.18))
        emph, last = {e.lower() for e in plan.get("emphasis", [])}, -9
        for w in words:
            if is_emph(w["w"], emph) and w["s"] - last > 1.2:
                events.append(("pop", w["s"] - 0.01, 0.40))
                last = w["s"]
        if plan.get("glow_end"):
            events.append(("sparkle", total - plan["glow_end"], 0.45))
    for e in plan.get("sfx_events", []):
        events.append((e["name"], e["t"], e.get("gain", 0.4)))
    for name, t, g in events:
        place(name, t, g)
    sfx.write_wav(os.path.join(work, "sfx.wav"), track[:int(total * sfx.SR)])
    bed = sfx.music_bed(total, bpm=plan.get("bpm", 98), seed=plan.get("seed", 0))
    sfx.write_wav(os.path.join(work, "bed.wav"), bed)
    return events


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--work", default=None)
    ap.add_argument("--preview", action="store_true", help="fast encode for review")
    a = ap.parse_args()
    plan = json.load(open(a.plan))
    base = os.path.dirname(os.path.abspath(a.plan))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    work = a.work or os.path.join(base, "work_" + os.path.splitext(os.path.basename(a.plan))[0])
    os.makedirs(work, exist_ok=True)
    words = json.load(open(rel(plan["words"])))

    pieces, total = build_timeline(plan, words)
    print(f"[1/5] {len(pieces)} pieces, {total:.2f}s")
    cutp, voice = cut(rel(plan["input"]), pieces, work)
    total = probe_duration(cutp)
    wmap = remap_words(pieces, flat_words(words))

    print("[2/5] face tracking")
    tracks, kind = track_faces(cutp, work)
    cap = cv2.VideoCapture(cutp)
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    centers = face_centers(tracks, kind, pieces, (W, H))

    print("[3/5] captions + audio")
    ass = os.path.join(work, "captions.ass")
    write_ass(ass, wmap, plan, total)
    events = build_audio(plan, pieces, wmap, total, work)

    print("[4/5] render frames")
    emph = {e.lower() for e in plan.get("emphasis", [])}
    hits, last = [], -9
    for w in wmap:
        if is_emph(w["w"], emph) and w["s"] - last > 1.2:
            hits.append(w["s"])
            last = w["s"]
    r = 9 / 16
    bw, bh = (H * r, H) if W / H > r else (W, W / r)
    glow_d = plan.get("glow_end", 0)
    sparkles = make_sparkles()
    yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32)
    edge = np.clip((((xx - OW / 2) / (OW * 0.55)) ** 2 + ((yy - OH / 2) / (OH * 0.55)) ** 2) - 0.35, 0, 1)
    edge = cv2.GaussianBlur(edge, (0, 0), 40)
    grade = plan.get("grade", "eq=contrast=1.04:saturation=1.07:gamma=1.02,colorbalance=rm=0.02:bm=-0.02")
    vf = f"{grade},ass={ass}:fontsdir={FONTS}" if grade else f"ass={ass}:fontsdir={FONTS}"
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{OW}x{OH}", "-r", str(FPS),
         "-i", "-", "-i", voice, "-i", os.path.join(work, "bed.wav"), "-i", os.path.join(work, "sfx.wav"),
         "-filter_complex",
         f"[0:v]{vf}[v];"
         "[1:a]highpass=f=80,acompressor=threshold=-21dB:ratio=3:attack=5:release=90:makeup=2,asplit=2[vo][sc];"
         f"[2:a]volume={plan.get('music_db', -20)}dB[bd0];[bd0][sc]sidechaincompress=threshold=0.03:ratio=8:"
         "attack=15:release=350[bd];[3:a]volume=0dB[fx];"
         "[vo][bd][fx]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]",
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast" if a.preview else "medium",
         "-crf", "20" if a.preview else "17", "-pix_fmt", "yuv420p", "-profile:v", "high",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", rel(plan["output"])],
        stdin=subprocess.PIPE)
    strength = plan.get("retouch", 0.55)
    piece_i, i = 0, 0
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        t = i / FPS
        while piece_i < len(pieces) - 1 and t >= pieces[piece_i]["t1"] - 1e-6:
            piece_i += 1
        p = pieces[piece_i]
        fr = retouch(fr, tracks[i] if i < len(tracks) else None, kind, strength)
        prog = (t - p["t0"]) / max(p["dur"], 1e-3)
        z = p["zoom"] * (1 + p["push"] * prog) * (1 + 0.065 * bump(t, hits))
        cw, ch = bw / z, bh / z
        fx, fy = centers[min(i, len(centers) - 1)]
        x0 = float(np.clip(fx - cw / 2, 0, W - cw))
        y0 = float(np.clip(fy - ch * plan.get("face_y", 0.32), 0, H - ch))
        s = OW / cw
        M = np.array([[s, 0, -x0 * s], [0, s, -y0 * s]], np.float32)
        out = cv2.warpAffine(fr, M, (OW, OH), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        if glow_d and t > total - glow_d:
            amt = min(1.0, (t - (total - glow_d)) / 0.35)
            out = glow(out, amt, t, sparkles, edge)
        ff.stdin.write(out.tobytes())
        i += 1
    ff.stdin.close()
    if ff.wait():
        sys.exit("final encode failed")
    print("[5/5] done ->", rel(plan["output"]))
    with open(os.path.join(work, "edl.json"), "w") as f:
        json.dump({"pieces": pieces, "sfx": events, "duration": total}, f, indent=1)


if __name__ == "__main__":
    main()
