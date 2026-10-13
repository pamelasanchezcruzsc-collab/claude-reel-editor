#!/usr/bin/env python3
"""Speech denoise with GTCRN via sherpa-onnx (no PyTorch needed). Model: sherpa-onnx GitHub release
speech-enhancement-models/gtcrn_simple.onnx in ~/.cache/reels. Works at 16 kHz, output resampled to 48 kHz.
Usage: python3 denoise_sherpa.py <in.wav> <out.wav>"""
import os, subprocess, sys, tempfile
from pathlib import Path
import sherpa_onnx, soundfile as sf
src, out = sys.argv[1], sys.argv[2]
m = Path(os.environ.get("GTCRN_MODEL", "~/.cache/reels/gtcrn_simple.onnx")).expanduser()
cfg = sherpa_onnx.OfflineSpeechDenoiserConfig(model=sherpa_onnx.OfflineSpeechDenoiserModelConfig(
    gtcrn=sherpa_onnx.OfflineSpeechDenoiserGtcrnModelConfig(model=str(m)), num_threads=4))
d = sherpa_onnx.OfflineSpeechDenoiser(cfg)
with tempfile.TemporaryDirectory() as tmp:
    w16 = Path(tmp) / "a.wav"; o16 = Path(tmp) / "o.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", str(w16)], check=True)
    a, sr = sf.read(str(w16), dtype="float32")
    r = d(a, sr)
    sf.write(str(o16), r.samples, r.sample_rate)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(o16), "-af", "aresample=48000:resampler=soxr", str(out)], check=True)
