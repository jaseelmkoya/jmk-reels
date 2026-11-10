"""Context-aware background music for JMK's reels (synthesised, royalty-free, offline).

A topic file can set   MUSIC = [(start_s, "mood"), ...]   — the track changes mood scene by scene
with 1.2 s crossfades. One musical key per video (from MUSIC_SEED / topic name) so the moods blend.

Moods
  space      slow, airy pads + sparkling bells, no drums          (space, stars, night sky, universe)
  cinematic  slow minor piano + pads + soft low drum, story feel  (history, documentary openings)
  ocean      calm major arpeggio, bright pad, light shaker        (nature, water, sky, gentle explaining)
  curious    upbeat plucks + light beat                           (explaining a concept, everyday examples)
  tension    ticking, sustained dark chords, staccato             (quiz, mystery, "why?" moments, experiments)
  uplift     bright piano chords + full beat                      (discoveries, results, endings, Follow)
  electric   pulsing synth arps + tight beat                      (electricity, circuits, magnetism, tech)
"""
import math, wave
import numpy as np

SR = 48000
ROOTS = [57, 55, 60, 62, 53, 58]          # A, G, C, D, F, Bb
MAJ = [0, 2, 4, 5, 7, 9, 11]
MIN = [0, 2, 3, 5, 7, 8, 10]

MOODS = {
    #           bpm  scale  progression (scale degrees)  layers
    "space":    dict(bpm=68,  sc=MIN, prog=[0, 5, 2, 6], pad=1.0, bright=0.25, bell=0.5, bass=0.5),
    "cinematic": dict(bpm=76, sc=MIN, prog=[0, 5, 2, 6], pad=0.8, bright=0.35, piano=0.6, bass=0.6, tom=0.5),
    "ocean":    dict(bpm=84,  sc=MAJ, prog=[0, 3, 5, 4], pad=0.6, bright=0.6, arp=0.5, bass=0.45, shaker=0.25),
    "curious":  dict(bpm=104, sc=MAJ, prog=[0, 4, 5, 3], pad=0.35, bright=0.5, pluck=0.6, bass=0.55, kick=0.5, hat=0.3, clap=0.25),
    "tension":  dict(bpm=120, sc=MIN, prog=[0, 0, 5, 4], pad=0.6, bright=0.2, stacc=0.45, bass=0.5, kick=0.35, tick=0.5),
    "uplift":   dict(bpm=112, sc=MAJ, prog=[0, 4, 5, 3], pad=0.5, bright=0.7, chords=0.55, pluck=0.35, bass=0.6, kick=0.6, hat=0.35, clap=0.4),
    "electric": dict(bpm=118, sc=MIN, prog=[0, 5, 6, 4], pad=0.4, bright=0.6, synth=0.5, bass=0.6, kick=0.55, hat=0.35),
}

hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)

def _env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t * d)

def _tone(f, n, harm=((1, 1),), a=0.005, d=4.0):
    t = np.arange(n) / SR
    y = sum(amp * np.sin(2 * np.pi * f * k * t) for k, amp in harm)
    return y * _env(n, a, d)

def _add(buf, s0, y):
    if s0 >= len(buf): return
    e = min(len(buf), s0 + len(y)); buf[s0:e] += y[:e - s0]

def _chord_notes(root, sc, deg, octave=0):
    n = lambda i: root + 12 * octave + sc[(deg + i) % 7] + 12 * ((deg + i) // 7)
    return [n(0), n(2), n(4)]

def mood_track(mood, dur, root, rng):
    P = MOODS[mood]; n = int(dur * SR); t = np.arange(n) / SR
    beat = 60 / P["bpm"]; bar = 4 * beat
    out = np.zeros(n)
    nbars = int(math.ceil(dur / bar)) + 1
    for b in range(nbars):
        deg = P["prog"][b % len(P["prog"])]
        ch = _chord_notes(root, P["sc"], deg)
        s0 = int(b * bar * SR); L = int((bar + 0.6) * SR)
        if s0 >= n: break
        tt = np.arange(L) / SR
        # pad: detuned saws softened (brightness = less smoothing)
        if P.get("pad"):
            env = np.minimum(1, tt / 0.7) * np.minimum(1, np.maximum(0, bar + 0.6 - tt) / 0.6)
            y = np.zeros(L)
            for m in ch + [ch[0] - 12]:
                for det in (-0.07, 0.07):
                    f = hz(m) * 2 ** (det / 12)
                    y += 2 * ((f * tt + rng.random()) % 1) - 1
            k = int(6 + (1 - P["bright"]) * 40)
            y = np.convolve(y, np.ones(k) / k, mode="same")
            _add(out, s0, y * env * 0.05 * P["pad"])
        if P.get("bass"):
            f = hz(ch[0] - 24)
            y = _tone(f, int(bar * SR), ((1, 1), (2, 0.3)), 0.02, 0.9)
            if P["bpm"] > 95:  # driving bass on beats 1 and 3
                y = np.zeros(int(bar * SR))
                for q in (0, 2):
                    _add(y, int(q * beat * SR), _tone(f, int(1.6 * beat * SR), ((1, 1), (2, 0.35)), 0.01, 2.5))
            _add(out, s0, y * 0.35 * P["bass"])
        if P.get("piano"):   # slow broken chords, low register
            pat = [0, 1, 2, 1]
            for q in range(4):
                m = ch[pat[q]] - 12 + (12 if q == 2 else 0)
                _add(out, s0 + int(q * beat * SR), _tone(hz(m), int(2.5 * SR), ((1, 1), (2, 0.45), (3, 0.15)), 0.004, 1.6) * 0.22 * P["piano"])
        if P.get("chords"):  # piano chord stabs on 1 and the "and" of 2
            for q in (0, 1.5, 2.5):
                for m in ch:
                    _add(out, s0 + int(q * beat * SR), _tone(hz(m), int(1.4 * SR), ((1, 1), (2, 0.4), (3, 0.12)), 0.004, 2.8) * 0.12 * P["chords"])
        if P.get("arp"):     # gentle 8th-note arpeggio
            pat = [0, 1, 2, 1, 2, 1, 0, 1]
            for q in range(8):
                m = ch[pat[q]] + 12
                _add(out, s0 + int(q * beat / 2 * SR), _tone(hz(m), int(1.2 * SR), ((1, 1), (2, 0.25)), 0.003, 3.5) * 0.12 * P["arp"])
        if P.get("pluck"):
            pat = [0, 2, 1, 2, 0, 2, 1, 2]
            for q in range(8):
                if rng.random() < 0.15: continue
                m = ch[pat[q]] + 12
                _add(out, s0 + int(q * beat / 2 * SR), _tone(hz(m), int(0.5 * SR), ((1, 1), (2, 0.5), (3, 0.25), (4, 0.1)), 0.002, 9) * 0.13 * P["pluck"])
        if P.get("stacc"):   # nervous 16ths on the root
            for q in range(16):
                m = ch[0] + (12 if q % 4 == 2 else 0)
                _add(out, s0 + int(q * beat / 4 * SR), _tone(hz(m), int(0.15 * SR), ((1, 1), (3, 0.3)), 0.002, 30) * 0.10 * P["stacc"])
        if P.get("synth"):   # pulsing saw arp
            for q in range(16):
                m = ch[q % 3] + 12
                L2 = int(beat / 4 * SR * 0.9); t2 = np.arange(L2) / SR
                y = (2 * ((hz(m) * t2) % 1) - 1) * np.exp(-t2 * 14)
                y = np.convolve(y, np.ones(5) / 5, mode="same")
                _add(out, s0 + int(q * beat / 4 * SR), y * 0.07 * P["synth"])
        if P.get("bell"):
            for q in range(8):
                if rng.random() < 0.55: continue
                m = ch[rng.integers(0, 3)] + 24
                f = hz(m); L2 = int(3.0 * SR); t2 = np.arange(L2) / SR
                y = (np.sin(2 * np.pi * f * t2) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t2)) * _env(L2, 0.002, 1.3)
                _add(out, s0 + int(q * beat / 2 * SR), y * 0.07 * P["bell"])
        # drums
        for q in range(4):
            sq = s0 + int(q * beat * SR)
            if P.get("kick") and (q in (0, 2) or P["bpm"] >= 110 and P.get("clap")):
                L2 = int(0.3 * SR); t2 = np.arange(L2) / SR
                f = 120 * np.exp(-t2 * 28) + 45
                _add(out, sq, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t2 * 11) * 0.5 * P["kick"])
            if P.get("tom") and q == 0:
                L2 = int(0.6 * SR); t2 = np.arange(L2) / SR
                f = 90 * np.exp(-t2 * 6) + 55
                _add(out, sq, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t2 * 5) * 0.35 * P["tom"])
            if P.get("clap") and q in (1, 3):
                L2 = int(0.12 * SR); y = rng.standard_normal(L2)
                y = y - np.convolve(y, np.ones(8) / 8, mode="same")
                _add(out, sq, y * np.exp(-np.arange(L2) / SR * 30) * 0.12 * P["clap"])
            for h in ((0.5,) if P.get("hat") else ()):
                L2 = int(0.05 * SR); y = rng.standard_normal(L2); y = y - np.convolve(y, np.ones(3) / 3, mode="same")
                _add(out, sq + int(h * beat * SR), y * np.exp(-np.arange(L2) / SR * 80) * 0.12 * P["hat"])
            if P.get("shaker"):
                for h in (0.0, 0.5):
                    L2 = int(0.08 * SR); y = rng.standard_normal(L2); y = y - np.convolve(y, np.ones(2) / 2, mode="same")
                    _add(out, sq + int(h * beat * SR), y * np.sin(np.linspace(0, np.pi, L2)) * 0.06 * P["shaker"])
            if P.get("tick"):
                for h in (0.0, 0.5):
                    L2 = int(0.02 * SR); t2 = np.arange(L2) / SR
                    _add(out, sq + int(h * beat * SR), np.sin(2 * np.pi * (2300 if h else 1800) * t2) * np.exp(-t2 * 250) * 0.18 * P["tick"])
    return out

def build(dur, plan=None, seed=1):
    """plan: [(start_s, mood), ...]. Returns float array at SR, peak-normalised to 0.9."""
    rng = np.random.default_rng(seed)
    root = ROOTS[seed % len(ROOTS)]
    plan = sorted(plan or [(0.0, "curious")])
    n = int(dur * SR); out = np.zeros(n)
    xf = 1.2
    for i, (st, mood) in enumerate(plan):
        en = plan[i + 1][0] if i + 1 < len(plan) else dur
        a = max(0.0, st - xf / 2); b = min(dur, en + xf / 2)
        seg = mood_track(mood, b - a, root if MOODS[mood]["sc"] is MAJ or True else root, rng)
        L = len(seg); tt = np.arange(L) / SR
        g = np.ones(L)
        if i > 0: g *= np.clip(tt / xf, 0, 1)
        if i + 1 < len(plan): g *= np.clip((b - a - tt) / xf, 0, 1)
        # loudness-match moods roughly
        rms = np.sqrt(np.mean(seg ** 2)) + 1e-9
        seg = seg / rms * 0.12
        _add(out, int(a * SR), seg * g)
    t = np.arange(n) / SR
    out *= np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 2.0)
    return out / (np.abs(out).max() + 1e-9) * 0.9

def write(path, dur, plan=None, seed=1, sr=SR):
    y = build(dur, plan, seed)
    if sr != SR:
        y = np.interp(np.arange(int(dur * sr)) / sr, np.arange(len(y)) / SR, y)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((y * 0.28 * 32767).astype(np.int16).tobytes())
