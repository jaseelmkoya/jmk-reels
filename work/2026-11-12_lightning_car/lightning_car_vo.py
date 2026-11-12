"""AI-VOICE version (JMK cloned voice, eleven_v4). Word times from ElevenLabs transcript (lc_words.json),
voice re-spaced with pauses (build_voice in this file). Topic: Lightning — are we safe inside a car? Electrostatic shielding (Gauss's theorem).
Plus Two · Ch1 Electric Charges and Fields. Hook: Thulavarsham thunderstorms / IMD alerts in Kerala (Nov 2026).
No-voice version: words appear at reading pace (PACE s/word). For a voiced version, replace WT with
transcript word times (see meteor_vo.py) — display tokens below are one-to-one with the VO script words."""
import math, sys, os, random, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import reelkit
from reelkit import *
reelkit.SYMBOLS |= set("∮εₒ₀₁₂⋅✓✗")

HANDLE = "@jmk.space"
TAG = pill("PLUS TWO PHYSICS · ELECTRIC CHARGES AND FIELDS", 26, bg=CYAN)
def top_tag(fr, t, fade=False):
    paste(fr, TAG, W / 2, 250, ease_out(prog(t, 0.1, 0.4)) if fade else 1.0)

PACE = 0.42
# scene durations

# ---------------- narration blocks: key -> (scene, local start, text, style) ----------------
BLOCKS = {
    "HOOK":  (0, 0.3, "ഇടിമിന്നൽ സമയത്ത് *car*-നുള്ളിൽ ഇരുന്നാൽ നമ്മൾ *safe* ആണോ?", dict(size=64, max_w=940, hl=YELLOW)),
    "CAP1":  (0, 7.6, "മിന്നൽ *car*-ൽ അടിച്ചു... പക്ഷെ ഉള്ളിലുള്ളയാൾ *safe!*", dict(size=54, max_w=940, hl=GREEN)),
    "MYTH":  (1, 0.3, "*Rubber tyre* ഉള്ളതുകൊണ്ടാണോ?", dict(size=66, max_w=940, hl=ORANGE)),
    "FACT":  (1, 3.8, "അല്ല! രക്ഷിക്കുന്നത് *car*-ന്റെ *metal body* ആണ്.", dict(size=54, max_w=940, hl=CYAN)),
    "FLOW":  (1, 7.4, "*Current* പുറത്തെ *metal*-ലൂടെ ഒഴുകി *ground*-ലേക്ക് പോകുന്നു.", dict(size=50, max_w=940, hl=YELLOW)),
    "WHY":   (2, 0.2, "കാരണം: *Electrostatic shielding*", dict(size=60, max_w=1000, hl=CYAN)),
    "SURF":  (2, 1.6, "*Conductor*-ലെ *charge* പുറം *surface*-ൽ മാത്രം നിൽക്കുന്നു.", dict(size=48, max_w=960, hl=YELLOW)),
    "ZERO":  (2, 8.6, "അതുകൊണ്ട് ഉള്ളിലെ *cavity*-ൽ *electric field* *zero* ആണ്.", dict(size=52, max_w=960, hl=GREEN)),
    "DEF":   (3, 0.7, "The *electric field* inside the *cavity* of a *conductor* is *zero*.", dict(size=56, max_w=880, hl=YELLOW, lh=1.45)),
    "DEF_ML": (3, 6.4, "പുറത്ത് എത്ര വലിയ *field* ഉണ്ടായാലും ഉള്ളിലേക്ക് അത് എത്തില്ല.", dict(size=48, max_w=940, hl=CYAN)),
    "GAUSS_ML": (3, 13.2, "*Gauss's theorem* പ്രകാരം, *shell*-ന്റെ ഉള്ളിൽ *charge* ഇല്ല, അതുകൊണ്ട് *field* *zero*.", dict(size=50, max_w=960, hl=GREEN)),
    "TIP1":  (4, 0.6, "*Window* അടച്ച്, *metal* ഭാഗങ്ങൾ തൊടാതെ ഇരിക്കുക.", dict(size=50, max_w=940, hl=YELLOW)),
    "TIP2":  (4, 4.6, "*Bike*-ലോ തുറന്ന വാഹനത്തിലോ ഈ *shielding* ഇല്ല!", dict(size=50, max_w=940, hl=RED)),
    "Q":     (5, 0.9, "*Charge* ഉള്ള ഒരു *spherical shell*-ന്റെ ഉള്ളിൽ *electric field* എത്ര?", dict(size=56, max_w=920, hl=YELLOW)),
    "OPTS":  (5, 5.0, "Option A, അല്ലെങ്കിൽ option B?", dict(size=40, max_w=900, hl=YELLOW)),   # spoken only, not drawn
    "CMT":   (5, 7.6, "ഉത്തരം *comment* ചെയ്യൂ!", dict(size=56, max_w=900, hl=CYAN)),
    "FOL":   (5, 9.4, "*Follow* ചെയ്യൂ", dict(size=56, max_w=900, hl=YELLOW)),
}
HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ["HOOK", "CAP1", "MYTH", "FACT", "FLOW", "WHY", "SURF", "ZERO", "DEF", "DEF_ML", "GAUSS_ML", "TIP1", "TIP2", "Q", "OPTS", "CMT", "FOL"]
GAP = dict(HOOK=0.6, CAP1=2.3, MYTH=1.3, FACT=0.9, FLOW=0.5, WHY=1.1, SURF=0.3, ZERO=1.4, DEF=1.3, DEF_ML=0.8, GAUSS_ML=2.0,
           TIP1=1.2, TIP2=0.7, Q=1.3, OPTS=0.2, CMT=1.4, FOL=0.4)
TAIL, RAW_END = 1.8, 48.77
RAW = json.load(open(os.path.join(HERE, "lc_words.json")))
SEGS, WT = [], {}
_k, _t = 0, 0.0
for _key in ORDER:
    _n = len(BLOCKS[_key][2].split()); _ws = RAW[_k:_k + _n]; _k += _n
    _ra = _ws[0]; _rb = RAW[_k] if _k < len(RAW) else RAW_END
    _t += GAP[_key]
    WT[_key] = [_t + (w - _ra) for w in _ws]
    SEGS.append((_ra, _rb, _t)); _t += _rb - _ra
assert _k == len(RAW), _k
END = _t + TAIL
S0 = [0.0, WT["MYTH"][0] - 0.5, WT["WHY"][0] - 0.5, WT["DEF"][0] - 0.7, WT["TIP1"][0] - 0.6, WT["Q"][0] - 0.8]
D = [(S0[i + 1] if i + 1 < len(S0) else END) - S0[i] for i in range(len(S0))]
EV = dict(STRIKE=WT["CAP1"][0] - 1.6, X=WT["MYTH"][-1] + 0.7, SRC=WT["FACT"][0] + 0.4, E0=WT["ZERO"][5], GAUSS=WT["GAUSS_ML"][0] - 1.3,
          OPT_A=WT["OPTS"][1], OPT_B=WT["OPTS"][4], EXAM=S0[5] + 0.4)

def build_voice(raw_wav, out_wav, sr=48000):
    """Re-space the TTS voice: each block placed at its new start with silence between."""
    import wave, numpy as np
    w = wave.open(raw_wav); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    out = np.zeros(int(END * sr), dtype=np.int16)
    for ra, rb, na in SEGS:
        a = max(0, int((ra - 0.05) * sr)); b = min(len(x), int((rb - 0.05) * sr)); o = max(0, int((na - 0.05) * sr))
        seg = x[a:b].astype(np.float32); f = int(0.01 * sr)
        seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        out[o:o + len(seg)] = seg.astype(np.int16)[:len(out) - o]
    with wave.open(out_wav, "wb") as o_:
        o_.setnchannels(1); o_.setsampwidth(2); o_.setframerate(sr); o_.writeframes(out.tobytes())

_RC = {}
def say(fr, key, x, y, t, sc, out_at=None):
    times = [g - S0[sc] for g in WT[key]]
    n = sum(1 for v in times if v <= t)
    if n == 0: return
    a = min(1.0, (t - times[n - 1]) / 0.15)
    oa = 1.0 if out_at is None else 1 - prog(t, out_at, 0.3)
    if oa <= 0: return
    ck = (key, n, round(a, 1))
    if ck not in _RC:
        _, _, s, kw = BLOCKS[key]; kw = dict(kw); size = kw.pop("size")
        _RC[ck] = text_img(s, size, reveal=(n, a), **kw)
    paste(fr, _RC[ck], x, y, oa)

def ev(k, sc): return EV[k] - S0[sc]

# ---------------- drawing ----------------
random.seed(5)
DROPS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(18, 34), random.uniform(900, 1400)) for _ in range(90)]
def rain(d, t, alpha=1.0, y0=300, y1=1560):
    for x, y, ln, sp in DROPS:
        yy = y0 + (y + t * sp) % (y1 - y0)
        xx = (x - (yy - y0) * 0.18) % W
        c = int(140 * alpha)
        d.line((xx, yy, xx - ln * 0.18, yy - ln), fill=(90 + c // 3, 110 + c // 3, 150 + c // 2), width=2)

def ground(d, y=1235):
    d.rectangle((0, y, W, y + 300), fill=(20, 22, 46))
    d.line((0, y, W, y), fill=(110, 120, 180), width=5)
    for x in range(-40, W, 170):
        d.rounded_rectangle((x, y + 55, x + 90, y + 66), radius=6, fill=(170, 175, 215))

# car geometry (side view), base at ground y=1235
CX0 = 210
def car_pts(cx=CX0, gy=1235, s=1.0):
    P = lambda x, y: (cx + x * s, gy - y * s)
    body = [P(0, 60), P(10, 125), P(150, 140), P(230, 235), P(470, 235), P(560, 145), P(650, 130), P(660, 60), P(600, 45), P(70, 45)]
    return body, P

def outline_path(cx=CX0, gy=1235, s=1.0):
    """Points along the outer metal skin from roof (strike point) down both sides to the ground."""
    _, P = car_pts(cx, gy, s)
    front = [P(350, 235), P(470, 235), P(560, 145), P(650, 130), P(660, 60), P(640, 0)]
    back = [P(350, 235), P(230, 235), P(150, 140), P(10, 125), P(0, 60), P(20, 0)]
    return front, back

def along(path, f):
    seg = [math.dist(path[i], path[i + 1]) for i in range(len(path) - 1)]
    L = sum(seg) * f
    for i, s in enumerate(seg):
        if L <= s:
            u = L / s; return (path[i][0] + (path[i + 1][0] - path[i][0]) * u, path[i][1] + (path[i + 1][1] - path[i][1]) * u)
        L -= s
    return path[-1]

def draw_car(fr, cx=CX0, gy=1235, s=1.0, glow=0.0, tyre_hl=0.0, person=True):
    L = SS(W, 520); d = L.d; k = L.s
    off = gy - 400
    body, P = car_pts(cx, gy, s)
    sh = lambda pts: [c for (x, y) in pts for c in k(x, y - off)]
    d.polygon(sh(body), fill=(70, 120, 200, 255), outline=(200, 220, 255, 255))
    # windows
    win1 = [P(165, 140), P(240, 222), P(340, 222), P(340, 140)]
    win2 = [P(360, 140), P(360, 222), P(462, 222), P(540, 140)]
    for w_ in (win1, win2):
        d.polygon(sh(w_), fill=(150, 205, 245, 255))
    if person:  # passenger silhouette in the front window
        hx, hy = P(410, 180)
        r = 26 * s
        d.ellipse(k(hx - r, hy - off - r, hx + r, hy - off + r), fill=(60, 45, 40, 255))
        d.rectangle(k(hx - 34 * s, hy - off + r, hx + 34 * s, P(0, 140)[1] - off), fill=(40, 60, 120, 255))
    d.line(sh([P(350, 140), P(350, 60)]), fill=(40, 70, 140, 255), width=int(4 * s * 2))
    d.ellipse(k(*P(640, 110), *P(660, 90)) if False else k(P(636, 118)[0], P(636, 118)[1] - off, P(658, 96)[0], P(658, 96)[1] - off), fill=(255, 245, 200, 255))
    for wx in (150, 520):
        x, y = P(wx, 45)
        r = 58 * s
        col = (int(30 + 200 * tyre_hl), int(30 + 60 * tyre_hl), 40, 255)
        d.ellipse(k(x - r, y - off - r, x + r, y - off + r), fill=col)
        d.ellipse(k(x - r * 0.45, y - off - r * 0.45, x + r * 0.45, y - off + r * 0.45), fill=(180, 185, 205, 255))
    if glow > 0:
        front, back = outline_path(cx, gy, s)
        for pth in (front, back):
            d.line(sh(pth), fill=(255, 230, 120, int(255 * glow)), width=int(14 * s))
            d.line(sh(pth), fill=(255, 255, 230, int(255 * glow)), width=int(5 * s))
    img = L.done()
    fr.paste(img, (0, off), img)

def bolt(d, x_end, y_end, t, seed=3, alpha=1.0):
    rnd = random.Random(seed + int(t * 20))
    pts = [(x_end + rnd.uniform(-60, 60), 740)]
    n = 9
    for i in range(1, n + 1):
        f = i / n
        x = x_end + (pts[0][0] - x_end) * (1 - f) + (rnd.uniform(-45, 45) if i < n else 0)
        y = 740 + (y_end - 740) * f
        pts.append((x, y))
    c = int(255 * alpha)
    d.line(pts, fill=(c, c, int(200 * alpha) + 55), width=14, joint="curve")
    d.line(pts, fill=(255, 255, 255), width=5, joint="curve")

def flow_dots(d, t, t0, alpha=1.0, cx=CX0, gy=1235, s=1.0):
    front, back = outline_path(cx, gy, s)
    for pth in (front, back):
        for j in range(6):
            f = ((t - t0) * 0.55 + j / 6) % 1.0
            x, y = along(pth, f)
            r = 11
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 225, 90))

# ---------------- static assets ----------------
NEWS = pill("തുലാവർഷം · Kerala-ൽ thunderstorm alert", 32, fg=WHITE, bg=(80, 60, 160))
WRONG = pill("തെറ്റ്!", 44, fg=WHITE, bg=RED)
SRC = pill("Source: NOAA / US National Weather Service", 26, fg=WHITE, bg=(60, 70, 120))
E0 = boxed(text_img("E = 0", 64, max_w=300, color=GREEN), outline=(91, 228, 155, 200))
DEF_PILL = pill("ELECTROSTATIC SHIELDING", 40, bg=YELLOW)
DEF_H = text_img(BLOCKS["DEF"][2], 56, max_w=880, hl=YELLOW, lh=1.45)
DEF_CARD = card(960, DEF_H.height + 50)
GAUSS_P = pill("Gauss's theorem", 36, fg=WHITE, bg=(80, 60, 160))
GAUSS_EQ = text_img("∮ E⋅dS = q / ε₀", 72, max_w=900, color=CYAN)
SAFE_P = pill("SAFETY TIP", 40, fg=(9, 14, 38), bg=GREEN)
OK = text_img("✓", 110, max_w=200, color=GREEN)
NO = text_img("✗", 110, max_w=200, color=RED)
QUIZ = pill("QUIZ TIME", 44, fg=(9, 14, 38), bg=PINK)
EXAM = pill("Exam favourite · Gauss's theorem", 30, fg=WHITE, bg=(80, 60, 160))
OPT_A = card(460, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(460, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A)  q / 4πε₀r²", 44, max_w=440)
TB = text_img("B)  Zero", 44, max_w=440)

# ---------------- scenes ----------------
def s1(fr, t, d):
    sc = 0
    st = ev("STRIKE", sc)
    rain(d, t)
    ground(d)
    glow = 0.0
    if t >= st:
        glow = max(0.0, 1 - (t - st) / 2.2)
    draw_car(fr, glow=glow)
    if st <= t < st + 0.7:
        bolt(d, CX0 + 350, 1235 - 235, t, alpha=1.0)
    if st - 0.05 <= t < st + 0.35:  # flash
        a = 1 - prog(t, st, 0.35)
        fl = Image.new("RGB", (W, H), (235, 240, 255))
        fr.paste(Image.blend(fr, fl, 0.55 * a))
    if st <= t < st + 2.4:
        flow_dots(d, t, st)
    top_tag(fr, t, fade=True)
    say(fr, "HOOK", W / 2, 330, t, sc)
    appear(fr, NEWS, W / 2, 660, t, WT["HOOK"][-1] + 0.3)
    say(fr, "CAP1", W / 2, 1330, t, sc)

def s2(fr, t, d):
    sc = 1
    rain(d, t + 13, 0.6)
    ground(d)
    hl = 0.5 + 0.5 * math.sin(t * 6) if 0.6 < t < ev("X", sc) + 0.6 else 0.0
    draw_car(fr, tyre_hl=hl * 0.8, glow=0.0)
    top_tag(fr, t)
    say(fr, "MYTH", W / 2, 330, t, sc)
    xs = ev("X", sc)
    if t > xs:
        k = ease_out(prog(t, xs, 0.3)) * (1 - prog(t, ev("SRC", sc) + 2.5, 0.4))
        for wx in (CX0 + 150, CX0 + 520):
            r = 70 * k
            if r > 2:
                d.line((wx - r, 1190 - r, wx + r, 1190 + r), fill=RED, width=14)
                d.line((wx - r, 1190 + r, wx + r, 1190 - r), fill=RED, width=14)
        appear(fr, WRONG, W / 2, 600, t, xs, pop=True, out_at=ev("SRC", sc) - 0.6)
    say(fr, "FACT", W / 2, 580, t, sc)
    appear(fr, SRC, W / 2, 790, t, ev("SRC", sc))
    if t > WT["FLOW"][0] - S0[sc]:
        t0 = WT["FLOW"][0] - S0[sc]
        draw_car(fr, glow=0.55 + 0.25 * math.sin(t * 5))
        flow_dots(d, t, t0)
    say(fr, "FLOW", W / 2, 1330, t, sc)

def shell_diagram(fr, d, t, a_ch, a_lines, a_in):
    x0, y0, x1, y1 = 250, 760, 830, 1180
    cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2
    # field lines outside (from + charges, pointing away)
    pts = []
    for i in range(10): pts.append((x0 + (x1 - x0) * (i + 0.5) / 10, y0, 0, -1))
    for i in range(10): pts.append((x0 + (x1 - x0) * (i + 0.5) / 10, y1, 0, 1))
    for i in range(6): pts.append((x0, y0 + (y1 - y0) * (i + 0.5) / 6, -1, 0))
    for i in range(6): pts.append((x1, y0 + (y1 - y0) * (i + 0.5) / 6, 1, 0))
    if a_lines > 0:
        for (x, y, ux, uy) in pts[::2]:
            L = 80 * a_lines
            arrow(d, x + ux * 26, y + uy * 26, x + ux * (26 + L), y + uy * (26 + L), (255, 159, 67), 5, 18)
    L = SS(W, 520); dd = L.d
    dd.rounded_rectangle(L.s(x0, y0 - 700, x1, y1 - 700), radius=60, outline=(200, 215, 255, 255), width=28)
    dd.rounded_rectangle(L.s(x0 + 14, y0 - 686, x1 - 14, y1 - 714), radius=48, fill=(30, 50, 90, 200))
    img = L.done(); fr.paste(img, (0, 700), img)
    # passenger inside
    if a_in > 0 or True:
        d.ellipse((cxm - 34, cym - 90, cxm + 34, cym - 22), fill=(120, 90, 70))
        d.rounded_rectangle((cxm - 60, cym - 18, cxm + 60, cym + 110), radius=24, fill=(60, 80, 150))
    if a_ch > 0:
        f = font("sym", "bold", 40)
        n = int(len(pts) * a_ch)
        for (x, y, ux, uy) in pts[:n]:
            d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(255, 92, 92))
            d.text((x, y + 1), "+", font=f, fill=WHITE, anchor="mm")
    if a_in > 0:
        paste(fr, E0, cxm + 170, cym - 60, a_in)

def s3(fr, t, d):
    sc = 2
    top_tag(fr, t)
    say(fr, "WHY", W / 2, 330, t, sc)
    say(fr, "SURF", W / 2, 470, t, sc)
    a_ch = ease_out(prog(t, WT["SURF"][1] - S0[sc], 2.0))
    a_l = ease_out(prog(t, WT["SURF"][-1] - S0[sc], 0.8))
    a_in = ease_out(prog(t, ev("E0", sc), 0.5))
    shell_diagram(fr, d, t, a_ch, a_l, a_in)
    say(fr, "ZERO", W / 2, 1330, t, sc)

def s4(fr, t, d):
    sc = 3
    top_tag(fr, t)
    appear(fr, DEF_PILL, W / 2, 330, t, 0.1, pop=True)
    appear(fr, DEF_CARD, W / 2, 430, t, 0.3)
    say(fr, "DEF", W / 2, 455, t, sc)
    say(fr, "DEF_ML", W / 2, 455 + DEF_H.height + 90, t, sc)
    gs = ev("GAUSS", sc)
    appear(fr, GAUSS_P, W / 2, 1000, t, gs - 0.6, pop=True)
    appear(fr, GAUSS_EQ, W / 2, 1090, t, gs, pop=True)
    say(fr, "GAUSS_ML", W / 2, 1280, t, sc)

def s5(fr, t, d):
    sc = 4
    rain(d, t + 40, 0.5)
    top_tag(fr, t)
    appear(fr, SAFE_P, W / 2, 330, t, 0.1, pop=True)
    say(fr, "TIP1", W / 2, 440, t, sc)
    # small car (safe) and bike (not safe)
    ground(d, 1235)
    draw_car(fr, cx=60, s=0.62, glow=0.0)
    appear(fr, OK, 270, 800, t, WT["TIP1"][-1] - S0[sc], pop=True)
    if t > WT["TIP2"][0] - S0[sc] - 0.3:
        a = ease_out(prog(t, WT["TIP2"][0] - S0[sc] - 0.3, 0.5))
        # bike
        bx, gy = 760, 1235
        col = (int(255 * a), int(159 * a), int(67 * a))
        for wx in (bx - 110, bx + 110):
            d.ellipse((wx - 62, gy - 124, wx + 62, gy), outline=col, width=10)
        d.line((bx - 110, gy - 62, bx - 20, gy - 150, bx + 70, gy - 150, bx + 110, gy - 62), fill=col, width=12)
        d.line((bx - 20, gy - 150, bx, gy - 62, bx - 110, gy - 62), fill=col, width=10)
        rc = (int(60 * a), int(80 * a), int(150 * a))
        d.line((bx - 20, gy - 160, bx + 10, gy - 250), fill=rc, width=30)
        d.line((bx + 10, gy - 235, bx + 70, gy - 160), fill=rc, width=14)
        d.line((bx - 20, gy - 160, bx + 20, gy - 70), fill=rc, width=16)
        d.ellipse((bx - 10, gy - 315, bx + 46, gy - 259), fill=(int(140 * a), int(90 * a), int(60 * a)))
        appear(fr, NO, 760, 800, t, WT["TIP2"][0] - S0[sc] + 0.4, pop=True)
    say(fr, "TIP2", W / 2, 1330, t, sc)

def s6(fr, t, d):
    sc = 5
    appear(fr, QUIZ, W / 2, 290, t, 0.1, pop=True)
    appear(fr, EXAM, W / 2, 380, t, ev("EXAM", sc), pop=True)
    say(fr, "Q", W / 2, 470, t, sc)
    for i, (c, tx, cx, key) in enumerate(((OPT_A, TA, 290, "OPT_A"), (OPT_B, TB, 790, "OPT_B"))):
        st = ev(key, sc)
        pulse = 1 + 0.03 * math.sin((t - st) * 6 + i * 3) if t > st + 0.6 else 1
        appear(fr, c, cx, 860, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 900, ease_out(prog(t, st + 0.05, 0.3)), pulse)
    say(fr, "CMT", W / 2, 1110, t, sc)
    say(fr, "FOL", W / 2, 1270, t, sc)

SCENES = list(zip(D, (s1, s2, s3, s4, s5, s6)))

VOICE = "vo/lc_voice.wav"
SFX = [(0.0, "rain"), (4.5, "rain"), (0.15, "pop"), (EV["STRIKE"], "thunder"), (EV["STRIKE"] + 0.05, "zap"),
       (WT["CAP1"][0], "pop"), (S0[1] + 0.0, "rain")]
for s in S0[1:]:
    SFX += [(s, "whoosh"), (s + 0.15, "pop")]
SFX += [(EV["X"], "boing"), (WT["FACT"][0], "ding"), (WT["FLOW"][0], "zap"), (WT["SURF"][1], "pop"), (EV["E0"], "ding"),
        (S0[3] + 0.3, "pop"), (WT["DEF_ML"][0], "pop"), (EV["GAUSS"], "ding"), (WT["GAUSS_ML"][0], "pop"),
        (WT["TIP1"][-1], "pop"), (WT["TIP2"][0] + 0.4, "boing"), (EV["EXAM"], "pop"), (EV["OPT_A"], "pop"), (EV["OPT_B"], "pop"),
        (EV["OPT_B"] + 0.6, "ticks"), (WT["CMT"][0], "pop"), (WT["FOL"][0], "chime")]
SFX = [(max(0.0, s), k) for s, k in SFX if s < END - 0.3]
MUSIC = [(0.0, "cinematic"), (S0[1], "tension"), (S0[2], "electric"), (S0[3], "curious"), (S0[4], "ocean"),
         (S0[5], "tension"), (WT["FOL"][0] - 0.3, "uplift")]
MUSIC_SEED = 512
