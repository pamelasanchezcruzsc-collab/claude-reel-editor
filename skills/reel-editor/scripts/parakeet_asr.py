#!/usr/bin/env python3
"""Offline word-timed transcript with NVIDIA Parakeet TDT v3 (25 European languages, incl. Spanish) via sherpa-onnx.
Used when Whisper's model download is blocked. Model: k2-fsa/sherpa-onnx GitHub release
sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8, unpacked to ~/.cache/reels/parakeet-v3 (or PARAKEET_DIR).
Usage: python3 parakeet_asr.py <video-or-audio> <out.json>  -> [{"text","start","end"}, ...]"""
import json, os, subprocess, sys, tempfile
from pathlib import Path
import numpy as np, sherpa_onnx, soundfile as sf

src, out = sys.argv[1], sys.argv[2]
m = Path(os.environ.get("PARAKEET_DIR", "~/.cache/reels/parakeet-v3")).expanduser()
rec = sherpa_onnx.OfflineRecognizer.from_transducer(
    encoder=str(m / "encoder.int8.onnx"), decoder=str(m / "decoder.int8.onnx"), joiner=str(m / "joiner.int8.onnx"),
    tokens=str(m / "tokens.txt"), model_type="nemo_transducer", num_threads=os.cpu_count() or 4)
with tempfile.TemporaryDirectory() as tmp:
    wav = Path(tmp) / "a.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
    audio, sr = sf.read(str(wav), dtype="float32")
audio = np.concatenate([audio, np.zeros(sr, dtype=np.float32)])   # 1 s of tail silence: both models drop the last words without it

# Parakeet handles ~20 s comfortably: decode in chunks split at the quietest point near each 20 s mark
CH, words, pos = 20 * sr, [], 0
while pos < len(audio):
    end = min(len(audio), pos + CH)
    if end < len(audio):   # cut in the quietest 50 ms window of the last 4 s
        win = audio[end - 4 * sr:end]; e = np.convolve(win ** 2, np.ones(800), "valid")
        end = end - 4 * sr + int(np.argmin(e)) + 400
    s = rec.create_stream(); s.accept_waveform(sr, audio[pos:end]); rec.decode_stream(s)
    r, off = s.result, pos / sr
    durs = list(getattr(r, "durations", []) or [])
    for i, (tok, t) in enumerate(zip(r.tokens, r.timestamps)):
        t0 = off + t
        t1 = t0 + (durs[i] if i < len(durs) and durs[i] > 0 else 0.08)
        if tok.startswith(" ") or tok.startswith("▁") or not words or words[-1].get("_chunk") != pos:
            words.append({"text": tok.replace("▁", "").strip(), "start": t0, "end": t1, "_chunk": pos})
        else:
            words[-1]["text"] += tok; words[-1]["end"] = t1
    pos = end
words = [{"text": w["text"], "start": round(w["start"], 3), "end": round(max(w["end"], w["start"] + 0.05), 3)}
         for w in words if w["text"]]

# Parakeet picks the language itself and drifts into English on Spanglish lines. When a language is set
# (brand.json "language"), take the WORDS from multilingual Whisper turbo forced to that language
# (~/.cache/reels/sherpa-onnx-whisper-turbo, also a sherpa-onnx GitHub release) and keep Parakeet's TIMING.
bj = Path(os.environ.get("REELS_HOME", "~/reels")).expanduser() / "brand.json"
lang = (json.load(open(bj)).get("language") if bj.exists() else None) or "en"
wd = Path(os.environ.get("WHISPER_DIR", "~/.cache/reels/sherpa-onnx-whisper-turbo")).expanduser()
if lang != "en" and wd.exists() and words:
    import difflib, re
    wr = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=str(wd / "turbo-encoder.int8.onnx"),
        decoder=str(wd / "turbo-decoder.int8.onnx"), tokens=str(wd / "turbo-tokens.txt"),
        language=lang, task="transcribe", num_threads=os.cpu_count() or 4)
    text, pos = [], 0
    while pos < len(audio):   # Whisper (sherpa) windows are 30 s: same quiet-point chunking at 25 s
        end = min(len(audio), pos + 25 * sr)
        if end < len(audio):
            win = audio[end - 4 * sr:end]; e = np.convolve(win ** 2, np.ones(800), "valid")
            end = end - 4 * sr + int(np.argmin(e)) + 400
        st = wr.create_stream(); st.accept_waveform(sr, audio[pos:end]); wr.decode_stream(st)
        text += st.result.text.split(); pos = end
    norm = lambda t: re.sub(r"[^\w]", "", t.lower())
    sm = difflib.SequenceMatcher(None, [norm(w["text"]) for w in words], [norm(t) for t in text], autojunk=False)
    new = []
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if b0 == b1:                                              # Whisper skipped it (it sometimes stops early): keep Parakeet's
            new += [{k: w[k] for k in ("text", "start", "end")} for w in words[a0:a1]]; continue
        if a0 == a1:                                              # Whisper-only word: squeeze into the gap
            t0 = words[a0 - 1]["end"] if a0 else words[0]["start"]
            t1 = words[a0]["start"] if a0 < len(words) else t0 + 0.3 * (b1 - b0)
            t1 = max(t1, t0 + 0.1 * (b1 - b0))
        else:
            t0, t1 = words[a0]["start"], words[a1 - 1]["end"]
        if op == "equal":
            new += [{"text": text[b0 + i], "start": words[a0 + i]["start"], "end": words[a0 + i]["end"]} for i in range(b1 - b0)]
        else:                                                     # spread the span by word length
            L = [max(len(t), 2) for t in text[b0:b1]]; acc = t0
            for t, l in zip(text[b0:b1], L):
                d = (t1 - t0) * l / sum(L); new.append({"text": t, "start": round(acc, 3), "end": round(acc + d, 3)}); acc += d
    words = new
    print(f"words from Whisper turbo ({lang}), timing from Parakeet")
for a, b in zip(words, words[1:]):   # a word never runs into the next one
    a["end"] = min(a["end"], b["start"])
json.dump(words, open(out, "w"), ensure_ascii=False)
print(f"transcribed with local Parakeet v3: {len(words)} words")
