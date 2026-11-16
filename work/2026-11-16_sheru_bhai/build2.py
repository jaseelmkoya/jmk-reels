"""v2: dialogue voices + original beat, subtitles instead of big captions."""
import sys, os, re, math, subprocess, wave
import numpy as np
sys.path.insert(0, "/home/claude/sheru")
import build as B
from build import *   # layers, helpers, W, H, FPS
import sfx

VO = "/home/claude/sheru/vo"
SR = sfx.SR

def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)

def split(x, n_expected, min_sil=0.55):
    """split audio at the n_expected-1 longest silences"""
    win = int(0.02 * SR); e = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, mode="same"))
    thr = max(1e-4, 0.03 * e.max()); quiet = e < thr
    runs, s = [], None
    for i, q in enumerate(quiet):
        if q and s is None: s = i
        if not q and s is not None:
            if (i - s) / SR >= min_sil: runs.append((s, i))
            s = None
    inner = [r for r in runs if r[0] > 0.2 * SR and r[1] < len(x) - 0.2 * SR]
    inner = sorted(sorted(inner, key=lambda r: r[1] - r[0], reverse=True)[:n_expected - 1])
    cuts = [0] + [(a + b) // 2 for a, b in inner] + [len(x)]
    parts = []
    for a, b in zip(cuts, cuts[1:]):
        p = x[a:b]; idx = np.nonzero(np.abs(p) > thr)[0]
        parts.append(p[max(0, idx[0] - int(0.03 * SR)): idx[-1] + int(0.08 * SR)] if len(idx) else p)
    return parts

def trim(x):
    thr = 0.02 * np.abs(x).max(); idx = np.nonzero(np.abs(x) > thr)[0]
    return x[max(0, idx[0] - int(0.03 * SR)): idx[-1] + int(0.1 * SR)]

sheru1 = trim(load(f"{VO}/sheru1.mp3"))
sh = split(load(f"{VO}/sheru2.mp3"), 5)
owl = trim(load(f"{VO}/owl.mp3"))
chotu = trim(load(f"{VO}/chotu.mp3"))
jm = split(load(f"{VO}/jmk.mp3"), 2, min_sil=0.8)
L = lambda x: len(x) / SR
print("pieces", [round(L(p), 2) for p in sh], [round(L(p), 2) for p in jm])

# (scene index -> list of (offset, audio, speaker, subtitle))
SPK = {"sheru": ("ഷേരു ഭായ്", YEL), "owl": ("മൂങ്ങ", CYAN), "chotu": ("ചോട്ടു", PINK), "jmk": ("JMK", GREEN)}
LINES = {
    0: [(0.2, sheru1, "sheru", "Physics A+… Arban! Tarban! ഒരു Trillion… Zillion… GAZILLION dollar! 😂 ഷേരു ഭായ് വാങ്ങും!")],
    1: [(0.9, owl, "owl", "ക്ഷമിക്കണം ഷേരു ഭായ്… A+ വിൽപ്പനയ്ക്കില്ല!"),
        (0.9 + L(owl) + 0.15, sh[0], "sheru", "എന്ത്?! A+ വിൽപ്പനയ്ക്കില്ലേ?!")],
    2: [(0.8, chotu, "chotu", "അച്ഛാ… ലിഫ്റ്റിൽ കയറുമ്പോൾ നമ്മുടെ weight മാറുമോ?")],
    3: [(1.2, sh[1], "sheru", "അയ്യോ! ലിഫ്റ്റ് മുകളിലേക്ക് start ചെയ്തപ്പോൾ… 241 kg?!")],
    4: [(0.9, sh[2], "sheru", "താഴേക്ക് start ചെയ്തപ്പോൾ 159! Diet ഒന്നും വേണ്ടല്ലോ!")],
    5: [(0.5, jm[0], "jmk", None)],
    6: [(0.3, sh[3], "sheru", "ചോട്ടു… Physics പൈസക്ക് കിട്ടില്ല, പഠിക്കണം. ദാ, JMK Space!")],
    7: [(0.6, sh[4], "sheru", "Follow ചെയ്യൂ JMK Space… ഷേരു ഭായ് approved!")],
    8: [(0.4, jm[1], "jmk", None)],
}
base = [5.2, 6.0, 6.0, 6.0, 5.0, 10.0, 4.5, 5.0, 8.5]
dur = []
for i, b in enumerate(base):
    need = max([o + L(a) + (0.8 if i not in (5, 8) else 1.0) for o, a, _, _ in LINES[i]])
    if i == 8: need = max(need, L(jm[1]) + 3.0)
    dur.append(round(max(b, need), 2))
B.SEG = [(k, c, (0.0 if c == "s1" else s), d) for (k, c, s, _), d in zip(B.SEG, dur)]
B.STARTS = np.cumsum([0] + dur); B.TOTAL = float(B.STARTS[-1])
STARTS, TOTAL = B.STARTS, B.TOTAL
print("durations", dur, "total", TOTAL)

def sub_img(spk, text):
    name, col = SPK[spk]
    body = wrapb(f"*{name}:* {text}", 50, maxw=960, hl=col)
    return boxed(body, pad=20, fill=(0, 0, 0, 165), r=26)
SUBS = {i: [(o, o + L(a), sub_img(s, t)) for o, a, s, t in LINES[i] if t] for i in LINES}

def overlay(fr, i, t, raw=None):
    if i == 0:
        paste(fr, B.HOOK, W / 2, 400)
        pop(fr, B.SIGN, W / 2, 1030, t, 2.0)
    elif i == 1:
        pop(fr, B.STAMP, W / 2, 1150, t, 1.0, 3.0, rot=-8)
    elif i in (3, 4):
        up = i == 3
        ev = 1.7 if up else 1.2
        target = 241 if up else 159
        p = clamp((t - ev) / 0.6)
        val = 200 + (target - 200) * (1 - (1 - p) ** 3)
        col = WHITE if p <= 0 else (RED if up else GREEN)
        paste(fr, B.pill("⬆️ a" if up else "⬇️ a", 54, bg=RED if up else GREEN), W / 2, 360)
        paste(fr, readout(val, col), W / 2, 1100)
    elif i == 6:
        pop(fr, B.LBL_G, W / 2, 1150, t, 1.4)
    elif i == 7:
        pop(fr, B.CAP_H, W / 2, 1150, t, 2.0)
    for a, b, im in SUBS.get(i, []):
        if a - 0.05 <= t < b + 0.35:
            paste(fr, im, W / 2, 1420, clamp((t - a + 0.05) / 0.15))
B.overlay = overlay

# card timing follows the narration (approximate word timing by proportion)
def card(t):
    fr = B.CARD_BG.copy(); d = L(jm[0]); s = lambda f: 0.5 + f * d
    paste(fr, B.TAG, W / 2, 290, clamp(t / 0.3))
    pop(fr, B.K_T, W / 2, 430, t, 0.4)
    pop(fr, B.K_1, W / 2, 610, t, s(0.14))
    pop(fr, B.K_E1, W / 2, 810, t, s(0.36))
    pop(fr, B.K_E2, W / 2, 970, t, s(0.62))
    pop(fr, B.K_E3, W / 2, 1130, t, s(0.84))
    pop(fr, B.K_EX, W / 2, 1290, t, d + 0.3)
    pop(fr, B.K_PYQ, W / 2, 1420, t, d + 0.5)
    return fr
B.card = card

def build_audio(path):
    n = int(TOTAL * SR) + SR; voice = np.zeros(n); fx = np.zeros(n)
    def put(arr, x, t, g):
        s = int(t * SR); m = min(len(x), n - s); arr[s:s + m] += x[:m] * g
    for i, lines in LINES.items():
        for o, a, _, _ in lines:
            put(voice, a / (np.abs(a).max() + 1e-9), STARTS[i] + o, 0.95)
    S = STARTS
    for t, x, g in [(S[0] + 2.0, sfx.popf(700), 0.4), (S[1] + 1.0, sfx.vine_boom(0.6), 0.6), (S[3] + 1.7, sfx.popf(500), 0.5),
                    (S[4] + 1.2, sfx.popf(900), 0.5), (S[5], sfx.whoosh(0.6), 0.4), (S[6] + 1.4, sfx.kaching(), 0.45),
                    (S[7] + 2.0, sfx.vine_boom(), 0.8), (S[8], sfx.whoosh(0.6), 0.4)]:
        put(fx, x / (np.abs(x).max() + 1e-9), t, g)
    subprocess.run(["python3", "/home/claude/sheru/beat.py", str(TOTAL)], check=True)
    with wave.open("/home/claude/sheru/beat.wav") as w:
        mus = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768.0
    m = np.zeros(n); m[:len(mus)] = mus[:n]
    env = np.convolve((np.abs(voice) > 0.02).astype(float), np.ones(int(0.3 * SR)) / (0.3 * SR), mode="same")
    duck = 1 - 0.72 * np.clip(env * 3, 0, 1)
    a = voice + fx + m * 0.55 * duck
    a = a[:int(TOTAL * SR)]
    pcm = np.clip(a / (np.abs(a).max() + 1e-9) * 0.95, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((pcm * 32767).astype(np.int16).tobytes())
B.build_audio = build_audio

if __name__ == "__main__":
    OUT = sys.argv[1]
    if len(sys.argv) > 2:
        want = [float(x) for x in sys.argv[2].split(",")]; got = []
        for i, t, fr in B.frames():
            T = STARTS[i] + t
            if want and abs(T - want[0]) < 0.5 / FPS:
                got.append(B.finish(fr).convert("RGB").resize((360, 640))); want.pop(0)
            if not want: break
        sh_ = Image.new("RGB", (360 * min(6, len(got)), 640 * math.ceil(len(got) / 6)))
        for j, im in enumerate(got): sh_.paste(im, ((j % 6) * 360, (j // 6) * 640))
        sh_.save(OUT); sys.exit()
    wav = OUT[:-4] + "_audio.wav"; build_audio(wav)
    vtmp = OUT[:-4] + "_v.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", vtmp], stdin=subprocess.PIPE)
    for i, t, fr in B.frames():
        T = STARTS[i] + t; fr = B.finish(fr)
        if T > TOTAL - 0.4: fr = Image.blend(fr, Image.new("RGBA", fr.size, (0, 0, 0, 255)), (T - (TOTAL - 0.4)) / 0.4)
        p.stdin.write(fr.convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    tmp = OUT[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", vtmp, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=9", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, OUT); print("wrote", OUT)
