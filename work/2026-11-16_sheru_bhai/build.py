import sys, os, math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/troll")
from kit import *
import sfx

C = "/home/claude/sheru/clips"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/sheru/sheru_v1.mp4"
W, H, FPS = 1080, 1920, 30
YEL, PINK, CYAN, RED, GREEN, WHITE = (255, 214, 0), (255, 110, 170), (90, 210, 255), (255, 70, 70), (90, 230, 140), (255, 255, 255)

# segments: (kind, clip, clip_start, dur)
SEG = [("v", "s1", 1.2, 5.0), ("v", "s2", 0.0, 6.0), ("v", "s3", 1.0, 6.0), ("v", "s4a", 0.3, 6.0),
       ("v", "s4b", 0.0, 5.0), ("card", None, 0, 10.0), ("v", "s6", 0.0, 4.5), ("v", "s7", 0.0, 5.0), ("quiz", None, 0, 8.5)]
STARTS = np.cumsum([0] + [s[3] for s in SEG])
TOTAL = float(STARTS[-1])

def read_clip(name, ss, dur):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-t", str(dur), "-i", f"{C}/{name}.mp4", "-vf",
                          f"fps={FPS},scale={W}:{H}:flags=lanczos,eq=contrast=1.05:saturation=1.08", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    n = len(raw) // (W * H * 3)
    return [raw[i * W * H * 3:(i + 1) * W * H * 3] for i in range(n)]

# ---------- watermark ----------
def avatar(ring, size=64):
    k = 4; S = size * k
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.ellipse((0, 0, S - 1, S - 1), fill=ring + (255,))
    inner = S - 6 * k
    ph = Image.open("/home/claude/troll/avatar.jpg").convert("RGB").resize((inner, inner), Image.LANCZOS)
    m = Image.new("L", (inner, inner), 0); ImageDraw.Draw(m).ellipse((0, 0, inner - 1, inner - 1), fill=255)
    img.paste(ph, (3 * k, 3 * k), m)
    return img.resize((size, size), Image.LANCZOS)

def watermark():
    parts = []
    for label, handle, ring, lc in (("Instagram", "@jmk.space", (225, 48, 108), (255, 120, 170)), ("YouTube", "@jaseelmkoyajmk", (255, 0, 0), (255, 60, 60))):
        av = avatar(ring); lab = font("lat", 20); hf = font("lat", 28)
        tw = int(max(lab.getlength(label), hf.getlength(handle)))
        p = Image.new("RGBA", (78 + tw, 64), (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
        p.paste(av, (0, 0), av); pd.text((78, 2), label, font=lab, fill=lc); pd.text((78, 26), handle, font=hf, fill=(245, 247, 255))
        parts.append(p)
    w = sum(p.width for p in parts) + 36 + 44
    img = Image.new("RGBA", (w, 92), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w - 1, 91), radius=46, fill=(9, 14, 38, 170), outline=(255, 255, 255, 40), width=2)
    x = 22
    for p in parts: img.alpha_composite(p, (x, 14)); x += p.width + 36
    return img
WM = watermark()

def wrapb(text, size, maxw=980, **kw):
    lines, cur = [], ""
    for para in text.split("|"):
        for w_ in para.split(" "):
            t = (cur + " " + w_).strip()
            if cur and line_img(t, size, **kw).width > maxw:
                lines.append(cur); cur = w_
            else:
                cur = t
        lines.append(cur); cur = ""
    return block(lines, size, gap=-6, **kw)

def cap(text, size=64, hl=YEL, **kw):
    return boxed(wrapb(text, size, hl=hl, **kw), pad=22, fill=(0, 0, 0, 150), r=30)

def pill(text, size, fg=(10, 10, 20), bg=YEL):
    t = line_img(text, size, fill=fg, stroke=bg, sw=0)
    im = Image.new("RGBA", (t.width + 60, t.height + 16), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=im.height // 2, fill=bg + (255,))
    im.alpha_composite(t, (30, 8)); return im

# ---------- text layers ----------
HOOK = wrapb("ഷേരു ഭായിക്ക് പോലും|*പൈസ കൊടുത്ത് വാങ്ങാൻ* പറ്റാത്തത്? 😱", 70, hl=YEL)
SIGN = pill("ലേലം: Physics A+ 🏆", 60)
STAMP = None
def make_stamp():
    t = line_img("NOT FOR SALE ❌", 78, fill=(255, 255, 255), stroke=(140, 0, 0), sw=6)
    im = Image.new("RGBA", (t.width + 60, t.height + 30), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=24, fill=(220, 20, 40, 235), outline=(255, 255, 255, 255), width=6)
    im.alpha_composite(t, (30, 15)); return im
STAMP = make_stamp()
CAP_B1 = cap("സാറേ, *A+ വിൽപ്പനയ്ക്കില്ല!*", 64)
CAP_B2 = wrapb("ഷേരു ഭായ് ഷോക്ക്ഡ് 😱", 76, hl=YEL)
CAP_C0 = pill("ചോട്ടുവിന്റെ ഡൗട്ട് 🤔", 52, bg=CYAN)
CAP_C = cap("ലിഫ്റ്റിൽ നമ്മുടെ *weight* മാറുമോ?", 66)
CAP_D = cap("ലിഫ്റ്റ് മുകളിലേക്ക് *accelerate* ⬆️", 62)
CAP_D2 = wrapb("*Weight* കൂടി?! 😱", 84, hl=RED)
CAP_E = cap("ലിഫ്റ്റ് താഴേക്ക് *accelerate* ⬇️", 62)
CAP_E2 = wrapb("*Weight* കുറഞ്ഞു! 😎", 84, hl=GREEN)
CAP_G = cap("Physics പൈസക്ക് കിട്ടില്ല,|*പഠിക്കണം!* 📚", 62)
LBL_G = pill("📱 @jmk.space", 64, bg=CYAN)
CAP_H0 = wrapb("ഷേരു ഭായ് approved 😎", 70, hl=YEL)
CAP_H = boxed(wrapb("Follow *@jmk.space* 🔔", 80, hl=YEL), pad=26, fill=(0, 0, 0, 170), r=34, outline=(255, 214, 0, 255))

def readout(val, col):
    t = line_img(f"{val:.0f} kg", 96, fill=col, stroke=(0, 0, 0), sw=4)
    lab = line_img("Scale reading", 30, fill=(200, 200, 200), sw=2)
    im = Image.new("RGBA", (max(t.width, lab.width) + 70, t.height + lab.height + 30), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=26, fill=(15, 18, 25, 225), outline=col + (255,), width=5)
    im.alpha_composite(lab, ((im.width - lab.width) // 2, 10)); im.alpha_composite(t, ((im.width - t.width) // 2, 10 + lab.height))
    return im

# card scene
def blur_bg(frame_bytes):
    im = Image.frombuffer("RGB", (W, H), frame_bytes).filter(ImageFilter.GaussianBlur(18))
    im = Image.blend(im, Image.new("RGB", (W, H), (8, 10, 30)), 0.62)
    return im.convert("RGBA")

TAG = pill("PLUS ONE PHYSICS · LAWS OF MOTION", 34, bg=CYAN)
K_T = wrapb("ഇതാണ് *Apparent weight* 💡", 64, hl=YEL)
K_1 = wrapb("മെഷീൻ കാണിക്കുന്നത്|*normal reaction* R ആണ്", 58, hl=CYAN)
def eqcard(left, eq, col):
    a = line_img(left, 54, hl=col); b = line_img(eq, 70, fill=WHITE)
    w = 960; h = max(a.height, b.height) + 40
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=28, fill=(255, 255, 255, 22), outline=col + (230,), width=4)
    im.alpha_composite(a, (30, (h - a.height) // 2)); im.alpha_composite(b, (w - b.width - 30, (h - b.height) // 2))
    return im
K_E1 = eqcard("⬆️ *a* മുകളിലേക്ക്", "R = m(g + a)", RED)
K_E2 = eqcard("⬇️ *a* താഴേക്ക്", "R = m(g - a)", GREEN)
K_E3 = eqcard("*Uniform velocity*", "R = mg", CYAN)
K_EX = wrapb("200 kg, a = 2 m/s²: 241 kg / 159 kg", 44, fill=(220, 220, 230), hl=YEL)
K_PYQ = pill("📝 Lift question: Plus One March 2022", 36, fg=WHITE, bg=(90, 60, 170))

Q_P = pill("QUIZ TIME 🧠", 64, bg=PINK)
Q_T = wrapb("ലിഫ്റ്റിന്റെ കയർ പൊട്ടി *free fall* ആയാൽ, ഷേരു ഭായിയുടെ മെഷീൻ കാണിക്കുന്നത്?", 58, hl=YEL)
def opt(t, col):
    tx = line_img(t, 66, fill=WHITE)
    im = Image.new("RGBA", (440, 170), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, 439, 169), radius=34, fill=col + (60,), outline=col + (255,), width=5)
    im.alpha_composite(tx, ((440 - tx.width) // 2, (170 - tx.height) // 2)); return im
Q_A = opt("A) mg", CYAN); Q_B = opt("B) 0", (255, 159, 67))
Q_C = wrapb("ഉത്തരം *comment* ചെയ്യൂ! 👇", 66, hl=CYAN)
Q_F = wrapb("Follow *@jmk.space* 🔔", 56, hl=YEL)

def fade_in(t, s, d=0.3): return clamp((t - s) / d)

def overlay(fr, i, t, raw=None):
    T = STARTS[i] + t
    if i == 0:
        paste(fr, HOOK, W / 2, 400)                     # visible from frame 0
        pop(fr, SIGN, W / 2, 1300, t, 2.0)
    elif i == 1:
        pop(fr, STAMP, W / 2, 1150, t, 1.0, 2.9, rot=-8)
        pop(fr, CAP_B1, W / 2, 1380, t, 1.1, 2.9)
        pop(fr, CAP_B2, W / 2, 1380, t, 3.1)
    elif i == 2:
        pop(fr, CAP_C0, W / 2, 330, t, 0.1)
        pop(fr, CAP_C, W / 2, 1380, t, 0.3)
    elif i in (3, 4):
        up = i == 3
        paste(fr, CAP_D if up else CAP_E, W / 2, 360, fade_in(t, 0.05, 0.2))
        ev = 1.7 if up else 1.2
        target = 241 if up else 159
        p = clamp((t - ev) / 0.6)
        val = 200 + (target - 200) * (1 - (1 - p) ** 3)
        col = WHITE if p <= 0 else (RED if up else GREEN)
        sc = 1 + (0.12 * math.sin(min(1, (t - ev) / 0.3) * math.pi) if 0 < t - ev < 0.3 else 0)
        paste(fr, readout(val, col), W / 2, 1180, 1, sc)
        pop(fr, CAP_D2 if up else CAP_E2, W / 2, 1400, t, ev + 0.7)
    elif i == 6:
        paste(fr, CAP_G, W / 2, 380, fade_in(t, 0.05, 0.25))
        pop(fr, LBL_G, W / 2, 1350, t, 1.4)
    elif i == 7:
        pop(fr, CAP_H0, W / 2, 350, t, 0.2)
        pop(fr, CAP_H, W / 2, 1330, t, 2.0)

CARD_BG = None; QUIZ_BG = None
def card(t):
    fr = CARD_BG.copy()
    paste(fr, TAG, W / 2, 290, fade_in(t, 0, 0.3))
    pop(fr, K_T, W / 2, 430, t, 0.2)
    pop(fr, K_1, W / 2, 610, t, 1.2)
    pop(fr, K_E1, W / 2, 810, t, 3.0)
    pop(fr, K_E2, W / 2, 970, t, 4.6)
    pop(fr, K_E3, W / 2, 1130, t, 6.2)
    pop(fr, K_EX, W / 2, 1290, t, 7.4)
    pop(fr, K_PYQ, W / 2, 1420, t, 8.2)
    return fr

def quiz(t):
    fr = QUIZ_BG.copy()
    pop(fr, Q_P, W / 2, 330, t, 0.0)
    pop(fr, Q_T, W / 2, 610, t, 0.3)
    pop(fr, Q_A, 290, 920, t, 2.6)
    pop(fr, Q_B, 790, 920, t, 3.0)
    pop(fr, Q_C, W / 2, 1150, t, 4.2)
    pop(fr, Q_F, W / 2, 1300, t, 5.4)
    return fr

def key_green(fr_bytes):
    a = np.frombuffer(fr_bytes, np.uint8).reshape(H, W, 3).copy().astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (g > 120) & (g > r + 40) & (g > b + 40)
    yy, xx = np.nonzero(m)
    if len(yy) > 50:
        y0, y1 = yy.min(), yy.max()
        grad = np.linspace(0, 1, max(1, y1 - y0 + 1))[:, None]
        col = np.concatenate([(40 + 40 * grad), (80 + 60 * grad), (200 + 40 * grad)], axis=1)
        a[m] = col[yy - y0].astype(np.int16)
    return a.astype(np.uint8).tobytes()

# ---------- music ----------
def music(dur, sr=sfx.SR):
    n = int(dur * sr); t = np.arange(n) / sr; out = np.zeros(n)
    bpm = 100; beat = 60 / bpm
    chords = [[57, 60, 64], [53, 57, 60], [55, 59, 62], [52, 55, 59]]
    bar = beat * 4
    for i in range(int(dur / bar) + 1):
        a = int(i * bar * sr); b = min(n, int((i + 1) * bar * sr))
        if a >= n: break
        tt = t[a:b] - i * bar
        for m in chords[i % 4]:
            f = 440 * 2 ** ((m - 69) / 12)
            out[a:b] += np.sin(2 * np.pi * f * tt) * 0.12 * np.minimum(1, tt / 0.05) * np.exp(-tt * 0.6)
        fb = 440 * 2 ** ((chords[i % 4][0] - 24 - 69) / 12)
        for k in range(4):   # bass + kick on beats
            s = a + int(k * beat * sr)
            if s >= n: break
            L = min(int(0.35 * sr), n - s); tk = np.arange(L) / sr
            out[s:s + L] += np.sin(2 * np.pi * fb * tk) * np.exp(-tk * 6) * 0.5
            out[s:s + L] += np.sin(2 * np.pi * (55 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 18) * 0.6
        for k in range(8):   # hats
            s = a + int((k + 0.5) * beat / 2 * sr)
            if s >= n: break
            L = min(int(0.04 * sr), n - s)
            out[s:s + L] += sfx.rng.normal(0, 1, L) * np.exp(-np.arange(L) / sr * 120) * 0.08
    out *= np.minimum(1, t / 0.5) * np.minimum(1, (dur - t) / 1.0)
    return out / (np.abs(out).max() + 1e-9)

def build_audio(path):
    SR = sfx.SR; n = int(TOTAL * SR) + SR; a = np.zeros(n)
    def put(x, t, g):
        s = int(t * SR); L = min(len(x), n - s); x = x / (np.abs(x).max() + 1e-9); a[s:s + L] += x[:L] * g
    put(music(TOTAL), 0, 0.22)
    S = STARTS
    for t, x, g in [(S[0] + 2.0, sfx.popf(700), 0.5), (S[0] + 4.9, sfx.whoosh(0.5), 0.4),
                    (S[1] + 1.0, sfx.vine_boom(0.6), 0.8), (S[1] + 3.1, sfx.vine_boom(), 0.9), (S[2] - 0.2, sfx.whoosh(0.5), 0.4),
                    (S[2] + 0.3, sfx.popf(600), 0.5), (S[3] + 0.05, sfx.chime((84, 88)), 0.5), (S[3] + 1.7, sfx.popf(500), 0.6),
                    (S[3] + 2.4, sfx.vine_boom(), 0.8), (S[4] + 0.05, sfx.chime((84, 88)), 0.5), (S[4] + 1.2, sfx.popf(900), 0.6),
                    (S[4] + 1.9, sfx.chime((79, 83, 86, 91)), 0.6), (S[5], sfx.whoosh(0.6), 0.5),
                    (S[5] + 3.0, sfx.popf(600), 0.5), (S[5] + 4.6, sfx.popf(700), 0.5), (S[5] + 6.2, sfx.popf(800), 0.5),
                    (S[6], sfx.whoosh(0.5), 0.4), (S[6] + 1.4, sfx.kaching(), 0.6), (S[7] + 2.0, sfx.vine_boom(), 1.0),
                    (S[8], sfx.whoosh(0.6), 0.5), (S[8] + 2.6, sfx.popf(600), 0.5), (S[8] + 3.0, sfx.popf(800), 0.5)]:
        put(x, t, g)
    a = a[:int(TOTAL * SR)]
    pcm = np.clip(a / (np.abs(a).max() + 1e-9) * 0.9, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((pcm * 32767).astype(np.int16).tobytes())

def frames():
    global CARD_BG, QUIZ_BG
    for i, (kind, clip, ss, dur) in enumerate(SEG):
        N = int(round(dur * FPS))
        if kind == "v":
            fs = read_clip(clip, ss, dur + 0.2)
            if clip == "s4a": CARD_BG = blur_bg(fs[min(len(fs) - 1, 70)])
            if clip == "s7": QUIZ_BG = blur_bg(fs[-1])
            for k in range(N):
                b = fs[min(k, len(fs) - 1)]
                if clip == "s6": b = key_green(b)
                fr = Image.frombuffer("RGB", (W, H), b).convert("RGBA")
                overlay(fr, i, k / FPS)
                yield i, k / FPS, fr
        else:
            for k in range(N):
                yield i, k / FPS, (card if kind == "card" else quiz)(k / FPS)

def finish(fr):
    paste(fr, WM, W / 2, 166, 0.95)
    return fr

if __name__ == "__main__":
    mode = sys.argv[2] if len(sys.argv) > 2 else "full"
    if mode == "stills":
        want = [float(x) for x in sys.argv[3].split(",")]; got = []
        for i, t, fr in frames():
            T = STARTS[i] + t
            if want and abs(T - want[0]) < 0.5 / FPS:
                got.append(finish(fr).convert("RGB").resize((360, 640))); want.pop(0)
            if not want: break
        sh = Image.new("RGB", (360 * min(6, len(got)), 640 * math.ceil(len(got) / 6)))
        for j, im in enumerate(got): sh.paste(im, ((j % 6) * 360, (j // 6) * 640))
        sh.save(OUT); print("sheet"); sys.exit()
    wav = OUT[:-4] + "_audio.wav"; build_audio(wav)
    vtmp = OUT[:-4] + "_v.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", vtmp], stdin=subprocess.PIPE)
    n = 0
    for i, t, fr in frames():
        T = STARTS[i] + t
        fr = finish(fr)
        if T > TOTAL - 0.4: fr = Image.blend(fr, Image.new("RGBA", fr.size, (0, 0, 0, 255)), (T - (TOTAL - 0.4)) / 0.4)
        p.stdin.write(fr.convert("RGB").tobytes()); n += 1
        if n % 300 == 0: print(n, flush=True)
    p.stdin.close(); p.wait()
    tmp = OUT[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", vtmp, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, OUT); print("wrote", OUT, n)
