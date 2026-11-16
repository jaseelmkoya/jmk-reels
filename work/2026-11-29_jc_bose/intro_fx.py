"""16 Nov: animated version of JMK's intro (IMG_1763): old-film 'hidden history' look -> flash reveal ->
MARCONI pops, gets struck out (shake + impact) -> tricolour 'INDIAN SCIENTIST' -> zoom/fade into the bell hook.
Music bed (tension) + synth SFX under his voice."""
import sys, os, wave, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
T = "/home/claude/jmk-reels/tools"; sys.path.insert(0, T); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reelkit import W, H, text_img, paste, ease_out, ease_back, prog, clamp, YELLOW, RED, WHITE
from face_clip import render
import music as musicgen
from mix_voice import sfx, bandnoise, SR
from face_intro_outro import intro_l, intro_w, UP, OUT

A, B = 0.30, 6.84; DUR = B - A
ws = [w["start"] - A for w in intro_w]
T_SATYAM, T_REVEAL, T_RADIO, T_MARC, T_ALLA, T_IND, T_SCI = ws[5], ws[6] - 0.05, ws[7], ws[9], ws[10], ws[12], ws[13]
T_OUT = DUR - 0.28
BEBAS = os.path.join(T, "fonts/BebasNeue-Regular.ttf")
rng = np.random.default_rng(5)

def bebas(txt, size, fill=WHITE, stroke=0):
    f = ImageFont.truetype(BEBAS, size); bb = f.getbbox(txt, stroke_width=stroke)
    im = Image.new("RGBA", (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((20 - bb[0], 20 - bb[1]), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 200), (0, 0), im.getchannel("A"))
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (0, 6)); out.alpha_composite(im)
    return out

# vignette + grain (precomputed)
yy, xx = np.mgrid[0:H, 0:W]
VIG = np.clip(1 - 0.75 * (((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2), 0.25, 1)[..., None].astype(np.float32)
GRAINS = [rng.normal(0, 14, (H // 2, W // 2, 1)).astype(np.float32) for _ in range(6)]

def zoom(fr, z, dx=0, dy=0, cy=0.42):
    if abs(z - 1) < 1e-3 and not dx and not dy: return fr
    w, h = W / z, H / z; x0 = (W - w) / 2 - dx / z; y0 = (H - h) * cy / 0.5 / 2 - dy / z
    x0 = clamp(x0, 0, W - w); y0 = clamp(y0, 0, H - h)
    return fr.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + w, y0 + h))

def zoom_at(t):
    z = 1.0 + 0.07 * ease_out(prog(t, 0, T_REVEAL)) if t < T_REVEAL else 1.0 + 0.04 * prog(t, T_REVEAL, T_IND - T_REVEAL)
    z = (1.12 - 0.12 * ease_out(prog(t, 0, 0.45))) if t < 0.45 else z           # punch-out at the start
    z += 0.035 * math.exp(-max(0, t - T_SATYAM) * 9) if t >= T_SATYAM else 0    # small hit on സത്യമുണ്ട്
    if t >= T_IND: z = 1.04 + 0.10 * ease_out(prog(t, T_IND, 0.18))              # punch-in on ഇന്ത്യൻ
    if t >= T_OUT: z += 0.35 * prog(t, T_OUT, DUR - T_OUT) ** 2                   # rush into the bell
    return z

# JMK's AI portrait of Bose (16 Nov) — full-screen cutaway on 'ഇന്ത്യൻ ശാസ്ത്രജ്ഞനാണ്' with a slow push-in and a pulsing spark
_P0 = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bose_ai_portrait.jpg")).convert("RGB")
# whole picture visible (JMK: nothing cut): fitted below the title, blurred copy fills the frame behind it
PY0 = 215; PH = H - PY0 - 10; PW = round(_P0.width * PH / _P0.height); PX0 = (W - PW) // 2
_PI = _P0.resize((PW, PH), Image.LANCZOS)
_s = max(W / _P0.width, H / _P0.height); _BG = _P0.resize((math.ceil(_P0.width * _s), math.ceil(_P0.height * _s)), Image.LANCZOS)
_BG = _BG.crop(((_BG.width - W) // 2, (_BG.height - H) // 2, (_BG.width - W) // 2 + W, (_BG.height - H) // 2 + H))
_BG = ImageEnhance.Brightness(_BG.filter(ImageFilter.GaussianBlur(28))).enhance(0.45)
SPARK = (PX0 + 375 / 808 * PW, PY0 + 1130 / 1447 * PH)
_g = np.exp(-(((xx - SPARK[0]) ** 2 + (yy - SPARK[1]) ** 2) / (2 * 60.0 ** 2)))[..., None].astype(np.float32)

def bose_frame(t):
    u = t - T_IND
    fr = zoom(_BG, 1.0 + 0.05 * clamp(u / 1.0))                     # only the blurred background moves
    s = 0.94 + 0.06 * ease_out(clamp(u / 0.3))                       # quick settle-in, ends at full size
    im = _PI if s > 0.999 else _PI.resize((round(PW * s), round(PH * s)), Image.BICUBIC)
    fr.paste(im, (PX0 + (PW - im.width) // 2, PY0 + (PH - im.height) // 2))
    a = np.asarray(fr).astype(np.float32)
    a += _g * (255, 200, 120) * (0.35 + 0.35 * abs(math.sin(t * 23)) * (rng.random() > 0.3))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def fx_pre(fr, t):
    if t >= T_IND: return bose_frame(t)
    sh = 0.0
    if t >= T_ALLA: sh = 18 * math.exp(-(t - T_ALLA) * 9)
    dx = sh * math.sin(t * 90); dy = sh * math.cos(t * 77)
    fr = zoom(fr, zoom_at(t), dx, dy)
    if t < T_REVEAL + 0.25:                                                       # old-film look, then colour snaps back
        k = 1 - clamp((t - T_REVEAL) / 0.25) if t >= T_REVEAL else 1
        a = np.asarray(fr).astype(np.float32)
        g = a.mean(2, keepdims=True); sep = np.concatenate([g * 1.07, g * 0.93, g * 0.74], 2)
        a = a * (1 - 0.75 * k) + sep * 0.75 * k
        a = a * (1 - (1 - VIG) * k)
        gr = np.repeat(np.repeat(GRAINS[int(t * 24) % 6], 2, 0), 2, 1)
        a += gr * k
        a *= 1 - 0.06 * k * (rng.random() > 0.7)                                  # flicker
        fr = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return fr

TAG = bebas("THE HIDDEN TRUTH", 92, fill=(255, 226, 170))
Q = text_img("Radio-യുടെ *പിതാവ്* ആര്?", 64, hl=YELLOW, max_w=980)
MARC = bebas("MARCONI", 190)
MARC_R = bebas("MARCONI", 190, fill=(255, 92, 92))
IND = bebas("INDIAN SCIENTIST", 124)
SAFF, GRN = (255, 153, 51), (19, 136, 8)

TOPG = Image.fromarray(np.dstack([np.zeros((520, W, 3), np.uint8),
        (np.linspace(185, 0, 520)[:, None] * np.ones((1, W))).astype(np.uint8)]), "RGBA")

def overlay(fr, t):
    fr = fr.convert("RGBA")
    if t >= T_RADIO - 0.1:                               # dark top gradient so white text reads on the white wall
        g = TOPG.copy(); g.putalpha(g.getchannel("A").point(lambda v: int(v * prog(t, T_RADIO - 0.1, 0.25)))); fr.alpha_composite(g)
    d = ImageDraw.Draw(fr)
    if t < T_REVEAL:                                     # typewriter tag
        n = int(len("THE HIDDEN TRUTH") * clamp((t - 0.25) / 1.1))
        if n > 0:
            tag = bebas("THE HIDDEN TRUTH"[:n], 92, fill=(255, 226, 170))
            fr.alpha_composite(tag, ((W - TAG.width) // 2, 170))
            if n < 16 and int(t * 8) % 2 == 0:
                d.rectangle(((W - TAG.width) // 2 + tag.width - 18, 205, (W - TAG.width) // 2 + tag.width - 6, 280), fill=(255, 226, 170))
    if T_RADIO - 0.1 <= t < T_MARC:
        paste(fr, Q, W / 2, 200, prog(t, T_RADIO - 0.1, 0.15), scale=0.85 + 0.15 * ease_back(prog(t, T_RADIO - 0.1, 0.3)))
    if T_MARC <= t < T_IND:
        s = 0.6 + 0.4 * ease_back(prog(t, T_MARC, 0.3))
        img = MARC_R if t >= T_ALLA else MARC
        paste(fr, img, W / 2, 150, prog(t, T_MARC, 0.1), scale=s)
        if t >= T_ALLA:                                  # strike-through + X stamp
            p = ease_out(prog(t, T_ALLA, 0.18)); cx = W / 2; y = 150 + MARC.height / 2
            x0 = cx - MARC.width / 2 + 30; x1 = x0 + (MARC.width - 60) * p
            d.line((x0, y + 8, x1, y - 8), fill=(255, 40, 40, 255), width=16)
            q = prog(t, T_ALLA + 0.06, 0.15)
            if q > 0:
                r = 120 * (1.6 - 0.6 * ease_out(q)); ccx, ccy = cx, y
                d.line((ccx - r, ccy - r, ccx + r, ccy + r), fill=(255, 40, 40, int(255 * q)), width=26)
                d.line((ccx - r, ccy + r, ccx + r, ccy - r), fill=(255, 40, 40, int(255 * q)), width=26)
            fl = 0.22 * math.exp(-(t - T_ALLA) * 10)
            fr.alpha_composite(Image.new("RGBA", (W, H), (255, 30, 30, int(255 * fl))))
    if t >= T_IND:                                       # tricolour sweep + INDIAN SCIENTIST
        p = ease_out(prog(t, T_IND, 0.25)); y0 = 30; bh = 18
        for i, c in enumerate((SAFF, (255, 255, 255), GRN)):
            pi = ease_out(prog(t, T_IND + i * 0.05, 0.25))
            d.rectangle((0, y0 + IND.height + 4 + i * bh, int(W * pi), y0 + IND.height + 4 + (i + 1) * bh - 4), fill=c + (235,))
        paste(fr, IND, W / 2, y0, p, scale=0.7 + 0.3 * ease_back(prog(t, T_IND, 0.3)))
    if T_IND <= t < T_IND + 0.25:
        fr.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(235 * (1 - (t - T_IND) / 0.25) ** 2))))
    if t >= T_IND:
        lab = text_img("AI recreation", 26, color=(230, 230, 230)); paste(fr, lab, W - 130, 1560, 0.7)
    if t < 0.12: fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * (1 - t / 0.12)))))
    if T_REVEAL <= t < T_REVEAL + 0.3:
        fr.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(220 * (1 - (t - T_REVEAL) / 0.3) ** 2))))
    if t >= T_OUT:
        fr.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, int(255 * prog(t, T_OUT, DUR - T_OUT) ** 1.5))))
    return fr.convert("RGB")

def make_bed(path):
    n = int(DUR * SR); y = np.zeros(n)
    mpath = path + ".m.wav"; musicgen.write(mpath, DUR + 1.5, [(0.0, "tension")], seed=11, sr=SR)
    w = wave.open(mpath); m = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; os.remove(mpath)
    m = m[int(0.9 * SR):][:n]; m = np.pad(m, (0, n - len(m)))           # skip the slow fade-in
    duck = np.ones(n); y += m * 0.55 * duck
    def add(t0, s, g=1.0):
        i = int(t0 * SR); s = s[:max(0, n - i)]; y[i:i + len(s)] += s * g
    tt = np.arange(int(0.6 * SR)) / SR
    boom = np.sin(2 * np.pi * (55 + 40 * np.exp(-tt * 12)) * tt) * np.exp(-tt * 6) * 0.6 + bandnoise(len(tt), 50, 400) * np.exp(-tt * 18) * 0.3
    crack = bandnoise(len(tt), 1500, 8000) * np.exp(-tt * 25) * 0.25
    rl = int(1.1 * SR); rt = np.arange(rl) / rl
    riser = bandnoise(rl, 800, 9000) * rt ** 2.5 * 0.16
    typ = np.zeros(int(1.2 * SR))
    for k in range(9):
        i = int((0.0 + k * 0.125) * SR); m2 = int(0.012 * SR); tk = np.arange(m2) / SR
        typ[i:i + m2] += bandnoise(m2, 2000, 6000) * np.exp(-tk * 400) * 0.25
    add(0.0, boom, 0.9); add(0.25, typ); add(T_SATYAM, sfx("thud"), 0.8)
    add(T_REVEAL - 0.35, sfx("whoosh"), 1.3); add(T_REVEAL, crack, 0.8)
    add(T_RADIO - 0.1, sfx("pop")); add(T_MARC, sfx("pop"), 1.2)
    add(T_ALLA, boom, 1.0); add(T_ALLA, crack, 1.0)
    add(T_IND - 0.25, sfx("whoosh")); add(T_IND, sfx("chime"), 0.9)
    add(T_OUT - 0.8, riser); add(T_OUT - 0.1, sfx("whoosh"), 1.3)
    y = np.clip(y, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype(np.int16).tobytes())

if __name__ == "__main__":
    bed = f"{OUT}/intro_bed.wav"; make_bed(bed)
    if len(sys.argv) > 1:   # stills check
        import subprocess
        sys.exit()
    render(f"{UP}/d9661876-IMG_1763.mov", f"{OUT}/intro_fx.mp4", A, B, intro_l, intro_w, fx_pre=fx_pre, fx_post=overlay, bed=bed, bed_gain=0.5)
