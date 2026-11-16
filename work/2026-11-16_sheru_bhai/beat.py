"""Original 'boss entry' trap beat: hit build-up, then a heavy drop. Writes beat.wav (mono 48k)."""
import sys, wave
import numpy as np
sys.path.insert(0, "/home/claude/troll")
import sfx
SR = sfx.SR
rng = np.random.default_rng(11)

def note(m): return 440 * 2 ** ((m - 69) / 12)

def kick(d=0.5):
    n = int(d * SR); t = np.arange(n) / SR
    f = 45 + 120 * np.exp(-t * 35)
    return np.tanh(2.2 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 6)

def eight08(m, d):
    n = int(d * SR); t = np.arange(n) / SR
    f = note(m) * (1 + 0.6 * np.exp(-t * 40))
    return np.tanh(1.8 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.minimum(1, t / 0.005) * np.exp(-t * 1.2)

def snare():
    n = int(0.3 * SR); t = np.arange(n) / SR
    return (rng.normal(0, 1, n) * np.exp(-t * 18) * 0.7 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25) * 0.6)

def hat(d=0.05):
    n = int(d * SR); x = rng.normal(0, 1, n)
    x = x - np.convolve(x, np.ones(6) / 6, mode="same")
    return x * np.exp(-np.arange(n) / SR * 90) * 0.5

def hit(m=45):
    n = int(0.9 * SR); t = np.arange(n) / SR
    body = sum(np.sin(2 * np.pi * note(m + k) * t) for k in (0, 7, 12)) / 3
    noise = rng.normal(0, 1, n) * np.exp(-t * 30) * 0.5
    return np.tanh(2 * (body * np.exp(-t * 3.5) + noise))

def bell(m, d=0.6):
    n = int(d * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * note(m) * t) + 0.4 * np.sin(2 * np.pi * note(m) * 2.76 * t)) * np.exp(-t * 5)

def make(total):
    n = int(total * SR); out = np.zeros(n + SR)
    def put(x, t, g):
        s = int(t * SR); L = min(len(x), len(out) - s)
        if L > 0: out[s:s + L] += x[:L] * g
    bpm = 140; b = 60 / bpm
    # build-up: 8 orchestral-style hits, accelerating slightly, rising pitch
    t = 0.3
    for k in range(8):
        put(hit(40 + (k % 4)), t, 0.8)
        t += b * (2 if k < 6 else 1)
    drop = t + b
    put(sfx.whoosh(1.0), drop - 1.0, 0.6)
    # drop: half-time trap, minor bell melody, 808 line
    mel = [69, 72, 76, 74, 72, 69, 67, 69]
    bass = [45, 45, 48, 43]
    bar = b * 4; i = 0; T = drop
    while T < total:
        for beat in range(4):
            tb = T + beat * b
            if beat in (0,) or (beat == 2 and i % 2 == 1): put(kick(), tb, 0.9)
            if beat == 2: put(snare(), tb, 0.55)
            for h in range(4 if i % 4 == 3 and beat == 3 else 2):
                put(hat(), tb + h * b / (4 if i % 4 == 3 and beat == 3 else 2), 0.35)
        put(eight08(bass[i % 4] - 12, bar * 0.95), T, 0.55)
        for k in range(2):
            put(bell(mel[(2 * i + k) % len(mel)]), T + k * 2 * b, 0.18)
        T += bar; i += 1
    out = out[:n]
    tt = np.arange(n) / SR
    out *= np.minimum(1, (total - tt) / 1.0)
    return out / (np.abs(out).max() + 1e-9) * 0.9, drop

if __name__ == "__main__":
    total = float(sys.argv[1]) if len(sys.argv) > 1 else 60
    x, drop = make(total)
    with wave.open("/home/claude/sheru/beat.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())
    print("drop at", round(drop, 2))
