#!/usr/bin/env python3
"""Jump-cut an approved edl.json down to the voice: inside every kept span, keep only where she is speaking
(level above --thresh on the cleaned voice), drop every gap longer than --gap, and leave --air seconds either side.
Removes breaths and pauses between sentences, which tighten.py's pacing presets leave in.
Usage: python3 jumpcut.py <reel> --gap 0.12 --air 0.04 [--thresh -38] [--words transcript.json] [--out edl_jump.json]"""
import argparse, json
from pathlib import Path
import numpy as np, soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument("reel"); ap.add_argument("--gap", type=float, default=0.12); ap.add_argument("--air", type=float, default=0.04)
ap.add_argument("--thresh", type=float, default=-38); ap.add_argument("--min-speech", type=float, default=0.06)
ap.add_argument("--words", default="transcript.json", help="source word timings: a cut never lands inside a word")
ap.add_argument("--min-cut", type=float, default=0.12)
ap.add_argument("--edl", default="edl.json"); ap.add_argument("--out", default="edl_jump.json")
a = ap.parse_args()
reel = Path(a.reel).expanduser()
edl = json.load(open(reel / a.edl))
x, sr = sf.read(str(reel / edl.get("audio", "voice.wav"))); x = x if x.ndim == 1 else x.mean(1)
H = int(sr * 0.01)
lv = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(H) / H, "same")[::H]) + 1e-9)   # 10 ms level track

wf = reel / a.words
WORDS = json.load(open(wf)) if wf.exists() else []
keep = []
for s, e in edl["keep"]:
    i0, i1 = int(s * 100), int(e * 100)
    on = lv[i0:i1] > a.thresh
    regs, st = [], None
    for k, v in enumerate(list(on) + [False]):
        if v and st is None: st = k
        if not v and st is not None:
            if (k - st) / 100 >= a.min_speech: regs.append([s + st / 100, s + k / 100])
            st = None
    words = [(w["start"], w["end"]) for w in WORDS if s <= w["start"] < e]
    for ws, we in words:   # protect each word's onset: soft first consonants read as quiet and would be clipped
        regs.append([max(s, ws - 0.03), min(e, ws + 0.15)])
    regs = sorted(r for r in regs if r[1] > r[0])
    merged = []
    for r in regs:   # join speech separated by gaps shorter than --gap
        if merged and r[0] - merged[-1][1] <= a.gap: merged[-1][1] = max(merged[-1][1], r[1])
        else: merged.append(r)
    # stray scraps: a breath with no word in it, or the first sound of a line that was cut right after it
    merged = [r for r in merged if r[1] - r[0] >= 0.5 or any(r[0] - 0.05 <= ws < r[1] and ws < e - 0.25 for ws, _ in words)]
    pre = a.air + 0.03   # a little more room before speech than after: clipped onsets are what the ear notices
    keep += [[round(max(s, r0 - pre), 3), round(min(e, r1 + a.air), 3)] for r0, r1 in merged]
# a removal shorter than --min-cut saves nothing you can hear but still makes the picture jump: keep it
tidy = []
for p0, p1 in keep:
    if tidy and p0 - tidy[-1][1] < a.min_cut and p0 >= tidy[-1][0]: tidy[-1][1] = max(tidy[-1][1], p1)
    else: tidy.append([p0, p1])
keep = tidy
before, after = sum(e - s for s, e in edl["keep"]), sum(e - s for s, e in keep)
json.dump({**edl, "keep": keep}, open(reel / a.out, "w"))
print(f"{len(edl['keep'])} spans -> {len(keep)} pieces, {before:.1f}s -> {after:.1f}s kept")
