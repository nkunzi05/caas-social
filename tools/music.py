"""Original, royalty-free background music for CAAS Studios Reels.

Everything is synthesised here from scratch (no samples, no downloads), so the tracks are ours and free to use:
no licence, no attribution, nothing for Instagram to mute.

Usage:
  python3 tools/music.py posts/<post-id>                 # add music to an existing reel.mp4 (video is copied, not re-encoded)
  python3 tools/music.py posts/<post-id> --style upbeat  # pick a style: lofi | upbeat | chill | house
  python3 tools/music.py --wav out.wav --seconds 22 --style chill   # just write a WAV
In code: make_track(seconds, style, seed) -> float32 stereo array at 44.1 kHz (tools/reel.py uses this).

The style is picked from the post id when not given, so every post gets a stable, different-sounding track.
"""
import argparse
import hashlib
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

SR = 44100
STYLES = ("lofi", "upbeat", "chill", "house")

# Chord progressions as semitone offsets from the key root (7th chords; voiced in make_track)
PROGRESSIONS = [
    [(0, [0, 4, 7, 11]), (9, [0, 3, 7, 10]), (5, [0, 4, 7, 11]), (7, [0, 4, 7, 10])],   # Imaj7 vi7 IVmaj7 V7
    [(2, [0, 3, 7, 10]), (7, [0, 4, 7, 10]), (0, [0, 4, 7, 11]), (9, [0, 3, 7, 10])],   # ii7 V7 Imaj7 vi7
    [(5, [0, 4, 7, 11]), (4, [0, 3, 7, 10]), (2, [0, 3, 7, 10]), (0, [0, 4, 7, 11])],   # IVmaj7 iii7 ii7 Imaj7
    [(0, [0, 4, 7, 11]), (5, [0, 4, 7, 11]), (9, [0, 3, 7, 10]), (5, [0, 4, 7, 11])],   # Imaj7 IVmaj7 vi7 IVmaj7
]

PRESETS = {  # bpm, swing, drum pattern, keys tone, filter brightness, crackle
    "lofi":   dict(bpm=84,  swing=0.18, kick="boombap", hats=8,  bright=0.35, crackle=0.010, keys="rhodes"),
    "chill":  dict(bpm=96,  swing=0.10, kick="sparse",  hats=8,  bright=0.50, crackle=0.004, keys="pad"),
    "upbeat": dict(bpm=112, swing=0.06, kick="pop",     hats=16, bright=0.70, crackle=0.0,   keys="pluck"),
    "house":  dict(bpm=120, swing=0.0,  kick="four",    hats=8,  bright=0.65, crackle=0.0,   keys="stab"),
}


def midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env_adsr(n, a, d, s, r, sustain_len=None):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    sl = n - a - d - r if sustain_len is None else int(sustain_len * SR)
    sl = max(sl, 0)
    e = np.concatenate([np.linspace(0, 1, max(a, 1)), np.linspace(1, s, max(d, 1)),
                        np.full(sl, s), np.linspace(s, 0, max(r, 1))])
    return np.pad(e, (0, max(n - len(e), 0)))[:n]


def lowpass(x, cutoff):
    """One-pole low-pass (cheap, warm)."""
    a = np.exp(-2 * np.pi * cutoff / SR)
    try:
        from scipy.signal import lfilter
        return lfilter([1 - a], [1, -a], x)
    except ImportError:  # pragma: no cover
        y = np.empty_like(x); acc = 0.0
        for i, v in enumerate(x):
            acc = (1 - a) * v + a * acc; y[i] = acc
        return y


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


def tone(freq, dur, kind, rng):
    n = int(dur * SR)
    t = np.arange(n) / SR
    det = 1 + rng.uniform(-0.0025, 0.0025)
    if kind == "rhodes":      # sine + bell-ish 2nd/3rd partials that die away fast
        x = np.sin(2 * np.pi * freq * det * t) + 0.25 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-t * 6) \
            + 0.12 * np.sin(2 * np.pi * 3.01 * freq * t) * np.exp(-t * 9)
        x *= 1 + 0.12 * np.sin(2 * np.pi * 4.5 * t)          # tremolo
        return x * env_adsr(n, 0.01, 0.5, 0.55, 0.35)
    if kind == "pad":
        x = sum(np.sin(2 * np.pi * freq * (1 + d) * t + p) for d, p in ((-0.004, 0), (0.0, 1.1), (0.0045, 2.3)))
        return x / 3 * env_adsr(n, 0.35, 0.3, 0.8, 0.5)
    if kind == "pluck":
        x = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * 2 * freq * t) + 0.15 * np.sin(2 * np.pi * 3 * freq * t)
        return x * np.exp(-t * 7)
    # stab: short saw-ish chord hit
    x = sum(np.sin(2 * np.pi * k * freq * t) / k for k in range(1, 7))
    return x * env_adsr(n, 0.004, 0.12, 0.25, 0.08, sustain_len=0.05)


def kick(rng, punch=1.0):
    n = int(0.38 * SR); t = np.arange(n) / SR
    f = 48 + 95 * np.exp(-t * 32)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5) * punch
    x[: int(0.003 * SR)] += rng.uniform(-0.4, 0.4, int(0.003 * SR))     # click
    return x


def snare(rng, clap=False):
    n = int(0.25 * SR); t = np.arange(n) / SR
    noise = highpass(rng.uniform(-1, 1, n), 1200)
    if clap:
        e = sum(np.exp(-np.clip(t - o, 0, None) * 60) * (t >= o) for o in (0, 0.011, 0.022)) * 0.6 + np.exp(-t * 18) * 0.5
        return noise * e * 0.7
    body = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 25)
    return (noise * np.exp(-t * 16) * 0.55 + body * 0.45)


def hat(rng, open_=False):
    n = int((0.22 if open_ else 0.05) * SR); t = np.arange(n) / SR
    return highpass(rng.uniform(-1, 1, n), 7000) * np.exp(-t * (14 if open_ else 70))


def add(buf, sig, start, gain=1.0, pan=0.0):
    s = int(start * SR)
    if s >= buf.shape[0] or s < 0:
        return
    sig = sig[: buf.shape[0] - s] * gain
    buf[s:s + len(sig), 0] += sig * np.sqrt(0.5 * (1 - pan))
    buf[s:s + len(sig), 1] += sig * np.sqrt(0.5 * (1 + pan))


def make_track(seconds: float, style: str = "lofi", seed: int = 0) -> np.ndarray:
    p = PRESETS[style]
    rng = np.random.default_rng(seed)
    key = 48 + int(rng.integers(0, 12)) % 12                          # C3..B3
    key = key if key <= 53 else key - 12                              # keep it warm (C3..F3, or lower)
    prog = PROGRESSIONS[int(rng.integers(0, len(PROGRESSIONS)))]
    beat = 60.0 / p["bpm"]
    bar = beat * 4
    total = int((seconds + 0.5) * SR)
    keys_b = np.zeros((total, 2)); drums_b = np.zeros((total, 2)); bass_b = np.zeros((total, 2)); mel_b = np.zeros((total, 2))

    def swung(step16):  # time of a 16th step with swing on the off-16ths
        return step16 * beat / 4 + (p["swing"] * beat / 4 if step16 % 2 else 0)

    n_bars = int(np.ceil(seconds / bar)) + 1
    scale = [0, 2, 4, 7, 9]                                            # major pentatonic for the little top line
    for b in range(n_bars):
        t0 = b * bar
        root_off, chord = prog[b % len(prog)]
        root = key + root_off
        # --- keys ---
        voicing = [root + 12 + c for c in chord]
        if p["keys"] in ("rhodes", "pad"):
            for i, m in enumerate(voicing):
                add(keys_b, tone(midi_hz(m), bar * (0.98 if p["keys"] == "pad" else 0.9), p["keys"], rng),
                    t0 + i * 0.012, 0.16, pan=(i - 1.5) * 0.25)
            if p["keys"] == "rhodes":     # a soft re-hit on beat 3 and 4-and
                for at in (2.0, 3.5):
                    for i, m in enumerate(voicing[1:]):
                        add(keys_b, tone(midi_hz(m), beat * 1.2, "rhodes", rng), t0 + at * beat + p["swing"] * beat / 4 * (at % 1 > 0), 0.07, pan=(i - 1) * 0.3)
        else:
            hits = (0, 3, 6, 10, 12, 14) if p["keys"] == "pluck" else (2, 6, 10, 14)
            for h in hits:
                for i, m in enumerate(voicing):
                    add(keys_b, tone(midi_hz(m), beat * 0.9, p["keys"], rng), t0 + swung(h), 0.11, pan=(i - 1.5) * 0.3)
        # --- bass ---
        bass_pat = {"boombap": [(0, 1.5), (2.5, 0.5), (3, 1)], "sparse": [(0, 2), (2.5, 1.5)],
                    "pop": [(0, .5), (1, .5), (1.5, .5), (2, .5), (3, .5), (3.5, .5)],
                    "four": [(0.5, .4), (1.5, .4), (2.5, .4), (3.5, .4)]}[p["kick"]]
        for at, ln in bass_pat:
            f = midi_hz(root - 12)
            n = int(ln * beat * SR); tt = np.arange(n) / SR
            x = np.tanh(1.6 * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt))) * env_adsr(n, 0.005, 0.1, 0.8, 0.06)
            add(bass_b, x, t0 + at * beat, 0.30)
        # --- drums ---
        kpat = {"boombap": [0, 7, 10], "sparse": [0, 10], "pop": [0, 6, 8, 11], "four": [0, 4, 8, 12]}[p["kick"]]
        for s in kpat:
            add(drums_b, kick(rng), t0 + swung(s), 0.55)
        for s in (4, 12):
            add(drums_b, snare(rng, clap=p["kick"] in ("pop", "four")), t0 + swung(s), 0.30, pan=0.05)
        step = 16 // p["hats"]
        for s in range(0, 16, step):
            open_ = p["kick"] == "four" and s % 4 == 2
            add(drums_b, hat(rng, open_), t0 + swung(s), (0.10 if s % 4 == 0 else 0.07) * (1.4 if open_ else 1), pan=0.35)
        # --- a few melody notes, every other bar ---
        if b % 2 == 1:
            for k in range(3):
                deg = scale[int(rng.integers(0, len(scale)))]
                m = key + 24 + deg + (12 if rng.random() < 0.2 else 0)
                add(mel_b, tone(midi_hz(m), beat * 1.1, "pluck", rng), t0 + swung(int(rng.choice([2, 6, 8, 10, 13]))) + k * 0.001, 0.08, pan=-0.2)

    keys_b = np.stack([lowpass(keys_b[:, c], 900 + 4000 * p["bright"]) for c in (0, 1)], 1)
    mel_b = np.stack([lowpass(mel_b[:, c], 1500 + 5000 * p["bright"]) for c in (0, 1)], 1)
    # simple sidechain feel: duck the music under the kick on four-on-the-floor / pop
    mix = keys_b + mel_b + bass_b
    if p["kick"] in ("four", "pop"):
        tt = np.arange(total) / SR
        duck = 1 - 0.35 * np.exp(-((tt % beat) / beat) * 6)
        mix *= duck[:, None]
    mix += drums_b
    # little room: a short stereo delay of the music bed
    d = int(0.023 * SR)
    mix[d:, 0] += 0.18 * (keys_b + mel_b)[:-d, 1]
    mix[d * 2:, 1] += 0.18 * (keys_b + mel_b)[:-d * 2, 0]
    if p["crackle"]:
        c = (rng.random(total) < 0.0007) * rng.uniform(-1, 1, total)
        mix += (lowpass(c, 3000) * 4 + lowpass(rng.normal(0, 1, total), 400) * 0.15)[:, None] * p["crackle"]
    mix = mix[: int(seconds * SR)]
    # fade in 0.4 s, fade out 1.5 s
    n = len(mix)
    fade = np.ones(n)
    fi, fo = int(0.4 * SR), int(1.5 * SR)
    fade[:fi] = np.linspace(0, 1, fi)
    fade[-fo:] = np.linspace(1, 0, fo) ** 1.5
    mix *= fade[:, None]
    mix = np.tanh(mix * 1.3) / np.tanh(1.3)                           # gentle glue/limiting
    rms = np.sqrt(np.mean(mix ** 2)) or 1
    mix *= min(0.18 / rms, 0.89 / (np.abs(mix).max() or 1))           # ~ -15 dBFS RMS: present but not loud
    return mix.astype(np.float32)


def pick_style(post_id: str) -> tuple[str, int]:
    h = int(hashlib.sha1(post_id.encode()).hexdigest(), 16)
    return STYLES[h % len(STYLES)], h % 100000


def write_wav(path: Path, x: np.ndarray):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def video_seconds(mp4: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(mp4)], capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def apply_to_reel(folder: Path, style: str | None):
    mp4 = folder / "reel.mp4"
    if not mp4.exists():
        sys.exit(f"{mp4} not found")
    auto_style, seed = pick_style(folder.name)
    style = style or auto_style
    secs = video_seconds(mp4)
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "music.wav"
        write_wav(wav, make_track(secs, style, seed))
        tmp = Path(td) / "reel.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-i", str(wav), "-map", "0:v:0", "-map", "1:a:0",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(tmp)], check=True)
        tmp.replace(mp4)
    print(f"{mp4}: added '{style}' track ({secs:.1f} s)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", nargs="?")
    ap.add_argument("--style", choices=STYLES)
    ap.add_argument("--wav")
    ap.add_argument("--seconds", type=float, default=22)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    if a.wav:
        write_wav(Path(a.wav), make_track(a.seconds, a.style or "lofi", a.seed))
        print(a.wav)
    elif a.folder:
        apply_to_reel(Path(a.folder), a.style)
    else:
        ap.error("give a post folder or --wav")
