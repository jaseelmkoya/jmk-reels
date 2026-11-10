"""Mix a rendered reel with JMK's voice-over, synthesized sound effects and a ducked music bed.
Usage: python3 mix_voice.py topics/<slug>.py out/<slug>_reel.mp4 out/<slug>_final.mp4
The topic file must define VOICE (wav path) and SFX = [(time_s, kind), ...].
"""
import sys, os, wave, subprocess, importlib.util, tempfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reelkit

SR = 48000
rng = np.random.default_rng(3)

def env(n, a=0.005, r=None, kind="exp", k=8.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4))
    if kind == "exp":
        e *= np.exp(-t * k)
    return e

def bandnoise(n, lo, hi):
    x = rng.standard_normal(n)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n)
    return y / (np.abs(y).max() + 1e-9)

def sfx(kind):
    if kind in ("whoosh", "swoosh"):
        d = 0.55 if kind == "whoosh" else 0.35
        n = int(d * SR); t = np.arange(n) / n
        y = bandnoise(n, 400, 5000) * np.sin(np.pi * t) ** 2
        return y * (0.22 if kind == "whoosh" else 0.18)
    if kind == "pop":
        n = int(0.09 * SR); t = np.arange(n) / SR
        f = 520 + 900 * t / t[-1]
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 45) * 0.28
    if kind == "ding":
        n = int(1.4 * SR); t = np.arange(n) / SR
        y = sum(a * np.sin(2 * np.pi * f * t) for f, a in ((1318.5, 1), (2637, .45), (3955, .2)))
        return y * np.exp(-t * 3.2) * np.minimum(1, t / 0.004) * 0.13
    if kind == "chime":
        a = sfx("ding"); b = sfx("ding")
        n = int(0.16 * SR); t = np.arange(len(b)) / SR
        b2 = sum(c * np.sin(2 * np.pi * f * t) for f, c in ((1975.5, 1), (3951, .4))) * np.exp(-t * 3) * np.minimum(1, t / .004) * 0.12
        out = np.zeros(len(a) + n); out[:len(a)] += a; out[n:n + len(b2)] += b2
        return out
    if kind == "boing":
        n = int(0.45 * SR); t = np.arange(n) / SR
        f = 380 * (1 - 0.45 * t / t[-1]) * (1 + 0.06 * np.sin(2 * np.pi * 14 * t))
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) * np.minimum(1, t / .01) * 0.25
    if kind == "brake":
        n = int(0.8 * SR); t = np.arange(n) / SR
        f = 2300 + 120 * np.sin(2 * np.pi * 9 * t) - 400 * t
        tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
        y = 0.55 * tone + 0.6 * bandnoise(n, 1800, 4500)
        e = np.minimum(1, t / 0.04) * np.minimum(1, (t[-1] - t) / 0.2)
        return y * e * 0.11
    if kind == "thud":
        n = int(0.35 * SR); t = np.arange(n) / SR
        y = np.sin(2 * np.pi * 65 * t) * np.exp(-t * 14) + 0.3 * bandnoise(n, 60, 600) * np.exp(-t * 30)
        return y * 0.45
    if kind == "engine":  # bus engine hum until the brake
        d = 5.1; n = int(d * SR); t = np.arange(n) / SR
        y = sum(np.sin(2 * np.pi * 52 * h * t + h) / h for h in range(1, 7)) * (1 + 0.25 * np.sin(2 * np.pi * 11 * t))
        y += 0.5 * bandnoise(n, 60, 300)
        e = np.minimum(1, t / 0.6) * np.clip((4.9 - t) / 0.6, 0, 1)
        return y / np.abs(y).max() * e * 0.07
    if kind == "ticks":  # clock ticks while viewers think
        d = 5.4; n = int(d * SR); y = np.zeros(n)
        for k in range(int(d / 0.5)):
            s = int(k * 0.5 * SR); m = int(0.02 * SR); tt = np.arange(m) / SR
            y[s:s + m] += np.sin(2 * np.pi * (2400 if k % 2 else 1900) * tt) * np.exp(-tt * 260)
        return y * 0.12
    raise ValueError(kind)

def read_wav(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if w.getnchannels() == 2: x = x.reshape(-1, 2).mean(1)
    assert w.getframerate() == SR, "voice must be 48 kHz"
    return x

def main(topic_path, video, out):
    spec = importlib.util.spec_from_file_location("topic", topic_path)
    tp = importlib.util.module_from_spec(spec); spec.loader.exec_module(tp)
    total = sum(d for d, _ in tp.SCENES)
    n = int(total * SR)
    voice = np.zeros(n)
    if getattr(tp, "VOICE", None):  # VOICE = None -> music + SFX only (fallback version)
        v = read_wav(os.path.join(os.path.dirname(os.path.abspath(__file__)), tp.VOICE))[:n]; voice[:len(v)] = v
    fx = np.zeros(n)
    for t0, kind in tp.SFX:
        s = sfx(kind); i = int(t0 * SR); j = min(n, i + len(s)); fx[i:j] += s[:j - i]
    # music bed, ducked under the voice
    tmp = tempfile.mkdtemp(); mp = os.path.join(tmp, "m.wav")
    reelkit.make_music(mp, total, sr=SR)
    music = np.zeros(n); m = read_wav(mp)[:n]; music[:len(m)] = m / (np.abs(m).max() + 1e-9)
    win = int(0.25 * SR)
    venv = np.convolve(np.abs(voice), np.ones(win) / win, mode="same")
    duck = np.where(venv > 0.02, 0.045, 0.11)
    duck = np.convolve(duck, np.ones(int(0.3 * SR)) / int(0.3 * SR), mode="same")
    mix = voice * 0.95 + fx + music * duck
    mix /= max(1.0, np.abs(mix).max() / 0.97)
    wp = os.path.join(tmp, "mix.wav")
    with wave.open(wp, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    tmpout = out[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", wp, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-shortest", "-movflags", "+faststart", tmpout], check=True)
    os.replace(tmpout, out)
    print("wrote", out)

if __name__ == "__main__":
    main(*sys.argv[1:4])
