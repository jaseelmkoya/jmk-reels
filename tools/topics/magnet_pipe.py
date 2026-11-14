"""Topic: Why does a magnet fall SLOWLY through a copper pipe? — Electromagnetic induction, eddy currents, Lenz's law.
Plus Two · Ch6 Electromagnetic Induction. No-voice version: words appear at reading pace (PACE s/word).
For a voiced version, replace WT with transcript word times — display tokens are one-to-one with the VO script words."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import reelkit
from reelkit import *
reelkit.SYMBOLS |= set("εφ−⋅✓✗")

HANDLE = "@jmk.space"
TAG = pill("PLUS TWO PHYSICS · ELECTROMAGNETIC INDUCTION", 26, bg=CYAN)
def top_tag(fr, t, start=1.5):
    paste(fr, TAG, W / 2, 250, ease_out(prog(t, start, 0.4)))

PACE = 0.42
D = [10.0, 11.5, 13.5, 10.5]
S0 = [sum(D[:i]) for i in range(len(D))]
END = sum(D)

BLOCKS = {
    "HOOK":  (0, -5.0, "*Copper pipe*-ൽ ഇട്ട *magnet* എന്തുകൊണ്ട് ഇത്ര പതുക്കെ വീഴുന്നു?", dict(size=68, max_w=960, hl=YELLOW)),
    "CAP1":  (0, 5.2, "*Copper*-നെ *magnet* ആകർഷിക്കില്ല! പിന്നെ ആരാണ് തടയുന്നത്?", dict(size=52, max_w=960, hl=ORANGE)),
    "WHY":   (1, 0.2, "കാരണം: *Electromagnetic Induction*", dict(size=58, max_w=1000, hl=CYAN)),
    "SUB":   (1, 1.6, "*Magnet* വീഴുമ്പോൾ *pipe*-ലെ ഓരോ *ring*-ലും *magnetic flux* മാറുന്നു.", dict(size=48, max_w=960, hl=YELLOW)),
    "CAP2":  (1, 5.6, "*Induced current* (*eddy currents*) ഉണ്ടാകുന്നു — അത് *magnet*-നെ മുകളിലേക്ക് തള്ളുന്നു!", dict(size=48, max_w=960, hl=GREEN)),
    "LAW":   (2, 0.7, "The *induced current* opposes the change in *flux* that produces it.", dict(size=56, max_w=880, hl=YELLOW, lh=1.45)),
    "LAW_ML": (2, 5.6, "*Flux*-ലെ മാറ്റത്തെ എതിർക്കുന്ന ദിശയിലാണ് *induced current*. അതുകൊണ്ട് *magnet* പതുക്കെ വീഴുന്നു.", dict(size=48, max_w=940, hl=CYAN)),
    "Q":     (3, 0.9, "*Lenz's law* ഏത് *conservation law*-ന് അനുസൃതമാണ്?", dict(size=58, max_w=920, hl=YELLOW)),
    "CMT":   (3, 6.3, "ഉത്തരം *comment* ചെയ്യൂ!", dict(size=56, max_w=900, hl=CYAN)),
    "FOL":   (3, 8.2, "*Follow* ചെയ്യൂ", dict(size=56, max_w=900, hl=YELLOW)),
}
WT = {k: [S0[sc] + st + i * PACE for i in range(len(txt.split()))] for k, (sc, st, txt, _) in BLOCKS.items()}
EV = dict(RINGS=S0[1] + 4.6, FORCE=S0[1] + 7.6, EQ=S0[2] + 10.4, EXAM=S0[3] + 0.4, OPT_A=S0[3] + 4.1, OPT_B=S0[3] + 4.5)

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
COPPER, COPPER_D, COPPER_L = (214, 120, 62), (150, 78, 40), (255, 190, 140)

def magnet(d, cx, cy, w=74, h=110, lab=True):
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy), radius=10, fill=(235, 70, 70))
    d.rounded_rectangle((cx - w / 2, cy, cx + w / 2, cy + h / 2), radius=10, fill=(70, 120, 235))
    d.rectangle((cx - w / 2, cy - 8, cx + w / 2, cy + 8), fill=(70, 120, 235))
    d.rectangle((cx - w / 2, cy - 8, cx + w / 2, cy), fill=(235, 70, 70))
    if lab:
        f = font("lat", "bold", int(h * 0.32))
        d.text((cx, cy - h / 4), "N", font=f, fill=WHITE, anchor="mm")
        d.text((cx, cy + h / 4), "S", font=f, fill=WHITE, anchor="mm")

PTOP, PBOT, PW = 720, 1230, 120
def pipe(fr, cx, copper):
    L = SS(W, 620); dd = L.d; k = L.s; off = PTOP - 50
    x0, x1 = cx - PW / 2, cx + PW / 2
    if copper:
        dd.rectangle(k(x0, PTOP - off, x1, PBOT - off), fill=COPPER + (215,))
        dd.rectangle(k(x0 + 12, PTOP - off, x0 + 30, PBOT - off), fill=COPPER_L + (150,))
        dd.rectangle(k(x1 - 26, PTOP - off, x1, PBOT - off), fill=COPPER_D + (170,))
    else:
        dd.rectangle(k(x0, PTOP - off, x1, PBOT - off), fill=(220, 235, 255, 60), outline=(220, 235, 255, 200), width=8)
        dd.rectangle(k(x0 + 14, PTOP - off, x0 + 26, PBOT - off), fill=(255, 255, 255, 90))
    dd.ellipse(k(x0, PTOP - 18 - off, x1, PTOP + 18 - off), fill=(20, 24, 50, 255), outline=(COPPER_L if copper else (220, 235, 255)) + (255,), width=8)
    img = L.done(); fr.paste(img, (0, off), img)

def fast_y(t):
    tt = (t + 0.25) % 1.9           # free fall: plastic pipe does not oppose the motion
    return 720 + 0.5 * 1650 * tt * tt if tt < 0.86 else None

def slow_y(t):
    tt = (t + 2.2) % 7.0            # quickly reaches a small constant (terminal) speed
    return 720 + 95 * tt - 95 * 0.35 * (1 - math.exp(-tt / 0.35)) if 720 + 95 * tt < 1330 else None

def ground(d, y=1300):
    d.line((120, y, W - 120, y), fill=(110, 120, 180), width=5)

def _mag(fr, cx, y):
    if y is None or y > 1290: return
    a = 1 - clamp((y - 1230) / 60)
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); magnet(ImageDraw.Draw(L), cx, y)
    if a < 1: L.putalpha(L.getchannel("A").point(lambda v: int(v * a)))
    fr.paste(L, (0, 0), L)

def s1_visual(fr, d, t):
    _mag(fr, 330, fast_y(t))
    pipe(fr, 330, False)
    _mag(fr, 750, slow_y(t))
    pipe(fr, 750, True)

PL_LAB = pill("PLASTIC", 32, fg=(9, 14, 38), bg=(200, 215, 240))
CU_LAB = pill("COPPER", 32, fg=WHITE, bg=COPPER_D)
FAST = boxed(text_img("വേഗം!", 40, max_w=300, color=WHITE))
SLOW = boxed(text_img("പതുക്കെ...", 40, max_w=300, color=COPPER_L))

def s1(fr, t, d):
    sc = 0
    s1_visual(fr, d, t)
    paste(fr, PL_LAB, 330, 1300)
    paste(fr, CU_LAB, 750, 1300)
    appear(fr, FAST, 330, 1395, t, 0.0, out_at=4.8)
    appear(fr, SLOW, 750, 1395, t, 0.0, out_at=4.8)
    top_tag(fr, t)
    pulse = 1 + 0.025 * math.sin(t * 4.0)
    _ = say(fr, "HOOK", W / 2, 320, t, sc)
    say(fr, "CAP1", W / 2, 1400, t, sc)

# zoomed copper pipe section (cut-away) with induced current loops
def loop_ring(fr, cx, cy, rx, ry, col, phase, cw, alpha=1.0, back=False):
    L = SS(W, 2 * ry + 60); dd = L.d; k = L.s; off = cy - ry - 30
    a = int(255 * alpha)
    rng = (180, 360) if back else (0, 180)
    dd.arc(k(cx - rx, cy - ry - off, cx + rx, cy + ry - off), rng[0], rng[1], fill=col + (a,), width=14)
    img = L.done(); fr.paste(img, (0, int(off)), img)
    if not back:  # moving charge dots on the front half show the direction
        d = ImageDraw.Draw(fr)
        for j in range(5):
            u = ((phase if cw else -phase) + j / 5) % 1.0
            ang = math.pi * u                          # 0..pi along front arc (right -> left)
            x, y = cx + rx * math.cos(ang), cy + ry * math.sin(ang)
            d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(255, 255, 255))

ZX, ZT, ZB, ZR = 540, 700, 1260, 210
I_LAB = boxed(text_img("*Induced current*", 38, max_w=420, hl=ORANGE), outline=(255, 159, 67, 180))
F_LAB = boxed(text_img("*F* ↑ (opposes)", 38, max_w=420, hl=GREEN), outline=(91, 228, 155, 180))
G_LAB = text_img("mg ↓", 38, max_w=200, color=PINK)

def zoom_pipe(fr, d, t, a_r, a_f):
    my = 985 + 10 * math.sin(t * 1.2) + (t * 6)
    my = 960 + ((t * 18) % 60)
    L = SS(W, ZB - ZT + 40); dd = L.d; k = L.s; off = ZT - 20
    dd.rectangle(k(ZX - ZR, ZT - off, ZX + ZR, ZB - off), fill=(60, 34, 24, 255))
    dd.rectangle(k(ZX - ZR, ZT - off, ZX - ZR + 34, ZB - off), fill=COPPER + (255,))
    dd.rectangle(k(ZX + ZR - 34, ZT - off, ZX + ZR, ZB - off), fill=COPPER_D + (255,))
    for yy in range(ZT + 40, ZB, 70):  # imaginary rings of the pipe wall
        dd.arc(k(ZX - ZR, yy - 26 - off, ZX + ZR, yy + 26 - off), 0, 180, fill=(COPPER_L) + (70,), width=4)
    img = L.done(); fr.paste(img, (0, off), img)
    if a_r > 0:
        ph = t * 0.6
        loop_ring(fr, ZX, my - 150, ZR - 10, 36, ORANGE, ph, True, a_r, back=True)
        loop_ring(fr, ZX, my + 150, ZR - 10, 36, CYAN, ph, False, a_r, back=True)
    magnet(d, ZX, my, 90, 160)
    if a_r > 0:
        loop_ring(fr, ZX, my - 150, ZR - 10, 36, ORANGE, ph, True, a_r)
        loop_ring(fr, ZX, my + 150, ZR - 10, 36, CYAN, ph, False, a_r)
        paste(fr, I_LAB, ZX + 320, my + 175, a_r)
    if a_f > 0:
        arrow(d, ZX - 330, my + 60, ZX - 330, my + 60 - 190 * a_f, GREEN, 14, 40)
        paste(fr, F_LAB, ZX - 330, my - 210, a_f)
        arrow(d, ZX, my + 85, ZX, my + 85 + 110 * a_f, PINK, 10, 30)
        paste(fr, G_LAB, ZX + 90, my + 120, a_f)

def s2(fr, t, d):
    sc = 1
    top_tag(fr, t, 0.0)
    say(fr, "WHY", W / 2, 320, t, sc)
    say(fr, "SUB", W / 2, 420, t, sc, out_at=ev("RINGS", sc) - 0.1 if False else None)
    a_r = ease_out(prog(t, ev("RINGS", sc), 0.6))
    a_f = ease_out(prog(t, ev("FORCE", sc), 0.6))
    zoom_pipe(fr, d, t, a_r, a_f)
    say(fr, "CAP2", W / 2, 1300, t, sc)

LAW_PILL = pill("LENZ'S LAW", 44, bg=YELLOW)
LAW_H = text_img(BLOCKS["LAW"][2], 56, max_w=880, hl=YELLOW, lh=1.45)
LAW_CARD = card(960, LAW_H.height + 50)
FAR_P = pill("Faraday's law", 34, fg=WHITE, bg=(80, 60, 160))
EQ = text_img("ε = − N dφ/dt", 76, max_w=900, color=CYAN)
EQ_N = text_img("( − sign  →  *Lenz's law* )", 42, max_w=900, color=MUTED, hl=YELLOW)

def s3(fr, t, d):
    sc = 2
    top_tag(fr, t, 0.0)
    appear(fr, LAW_PILL, W / 2, 320, t, 0.1, pop=True)
    appear(fr, LAW_CARD, W / 2, 430, t, 0.3)
    say(fr, "LAW", W / 2, 455, t, sc)
    say(fr, "LAW_ML", W / 2, 455 + LAW_H.height + 90, t, sc)
    es = ev("EQ", sc)
    appear(fr, FAR_P, W / 2, 1150, t, es - 0.5, pop=True)
    appear(fr, EQ, W / 2, 1235, t, es, pop=True)
    appear(fr, EQ_N, W / 2, 1385, t, es + 0.8)

QUIZ = pill("QUIZ TIME", 44, fg=(9, 14, 38), bg=PINK)
EXAM = pill("Exam favourite · Lenz's law", 30, fg=WHITE, bg=(80, 60, 160))
OPT_A = card(470, 170, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(470, 170, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) Conservation|of charge", 42, max_w=450, lh=1.3)
TB = text_img("B) Conservation|of energy", 42, max_w=450, lh=1.3)

def s4(fr, t, d):
    sc = 3
    appear(fr, QUIZ, W / 2, 290, t, 0.1, pop=True)
    appear(fr, EXAM, W / 2, 380, t, ev("EXAM", sc), pop=True)
    say(fr, "Q", W / 2, 470, t, sc)
    for i, (c, tx, cx, key) in enumerate(((OPT_A, TA, 285, "OPT_A"), (OPT_B, TB, 795, "OPT_B"))):
        st = ev(key, sc)
        pulse = 1 + 0.03 * math.sin((t - st) * 6 + i * 3) if t > st + 0.6 else 1
        appear(fr, c, cx, 820, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 845, ease_out(prog(t, st + 0.05, 0.3)), pulse)
    say(fr, "CMT", W / 2, 1090, t, sc)
    say(fr, "FOL", W / 2, 1250, t, sc)

SCENES = list(zip(D, (s1, s2, s3, s4)))

VOICE = None
SFX = [(0.0, "whoosh")] + [(0.56 + 1.9 * k, "thud") for k in range(5)] + [
       (WT["CAP1"][0], "boing")]
for s in S0[1:]:
    SFX += [(s, "whoosh"), (s + 0.15, "pop")]
SFX += [(WT["SUB"][0], "pop"), (EV["RINGS"], "zap"), (WT["CAP2"][0], "pop"), (EV["FORCE"], "ding"),
        (S0[2] + 0.3, "pop"), (WT["LAW_ML"][0], "pop"), (EV["EQ"], "ding"),
        (EV["EXAM"], "pop"), (EV["OPT_A"], "pop"), (EV["OPT_B"], "pop"), (EV["OPT_B"] + 0.6, "ticks"),
        (WT["CMT"][0], "pop"), (WT["FOL"][0], "chime")]
SFX = [(max(0.0, s), k) for s, k in SFX if s < END - 0.3]
MUSIC = [(0.0, "tension"), (S0[1], "electric"), (S0[2], "curious"), (S0[3], "tension"), (WT["FOL"][0] - 0.3, "uplift")]
MUSIC_SEED = 614
