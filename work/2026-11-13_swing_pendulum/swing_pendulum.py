"""Topic: Swing (ഊഞ്ഞാൽ) — does a heavier person swing slower? Simple pendulum period is independent of mass.
Plus One · Ch13 Oscillations. T = 2π√(L/g). Quiz: PYQ March 2022 (True/False: period depends on mass of bob → False).
No-voice version: words appear at reading pace (PACE s/word). For a voiced version replace WT with transcript
word times (see meteor_vo.py) — display tokens below are one-to-one with the VO script words."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import reelkit
from reelkit import *
reelkit.SYMBOLS |= set("✓✗")

HANDLE = "@jmk.space"
TAG = pill("PLUS ONE PHYSICS · OSCILLATIONS", 30, bg=CYAN)
def top_tag(fr, t, fade=False):
    paste(fr, TAG, W / 2, 250, ease_out(prog(t, 0.1, 0.4)) if fade else 1.0)

PACE = 0.42
D = [13.0, 14.0, 17.0, 13.5, 16.0, 12.5]
S0 = [sum(D[:i]) for i in range(len(D))]
END = sum(D)

BLOCKS = {
    "HOOK": (0, 0.1, "*75 kg* അച്ഛനോ *25 kg* കുട്ടിയോ — ആരുടെ ഊഞ്ഞാൽ വേഗം ആടും?", dict(size=66, max_w=940, hl=YELLOW)),
    "TEASE": (0, 4.0, "നിങ്ങൾക്ക് ഉത്തരം അറിയാമോ?", dict(size=58, max_w=940, hl=PINK)),
    "CAP1": (0, 8.0, "രണ്ടും ഒരേ താളത്തിൽ! *Period* ഒന്നുതന്നെ.", dict(size=56, max_w=940, hl=GREEN)),
    "WHY":  (1, 0.2, "കാരണം: *Simple pendulum*", dict(size=60, max_w=1000, hl=CYAN)),
    "DEFP": (1, 1.8, "*Period* (T) = ഒരു പൂർണ്ണ *oscillation*-ന് എടുക്കുന്ന സമയം", dict(size=48, max_w=960, hl=YELLOW)),
    "SHM":  (1, 7.2, "ചെറിയ *angle*-ൽ ഊഞ്ഞാലിന്റെ ആട്ടം *simple harmonic motion* (SHM) ആണ്.", dict(size=50, max_w=960, hl=GREEN)),
    "DEF":  (2, 0.7, "For small amplitudes, the *period* of a *simple pendulum* is independent of the *mass of the bob*.", dict(size=52, max_w=880, hl=YELLOW, lh=1.45)),
    "DEF_ML": (2, 8.0, "*Period*, *length* (L)-നെയും *g*-യെയും മാത്രം ആശ്രയിക്കുന്നു — *mass*-നെ അല്ല!", dict(size=48, max_w=940, hl=CYAN)),
    "LEN":  (3, 0.3, "*Length* കൂടിയാൽ *period* കൂടും", dict(size=60, max_w=1000, hl=ORANGE)),
    "BOT":  (3, 7.0, "*Length* 4 മടങ്ങ് ആക്കിയാൽ *period* 2 മടങ്ങ്!", dict(size=52, max_w=1000, hl=YELLOW)),
    "F1":   (4, 0.5, "1851-ൽ *Paris*-ൽ 67 m നീളമുള്ള ഒരു *pendulum* ഭൂമി കറങ്ങുന്നത് നേരിട്ട് കാണിച്ചുതന്നു!", dict(size=52, max_w=960, hl=YELLOW)),
    "F2":   (4, 6.6, "*Pendulum* ആടുന്ന ദിശ പതുക്കെ തിരിയുന്നു. ശരിക്കും തിരിയുന്നത് താഴെയുള്ള ഭൂമിയാണ്!", dict(size=50, max_w=960, hl=CYAN)),
    "F3":   (4, 11.6, "*Kerala*-യിൽ ഒരു റൗണ്ട് തിരിയാൻ ഏകദേശം 6 ദിവസം!", dict(size=54, max_w=960, hl=GREEN)),
    "Q":    (5, 0.9, "*Simple pendulum*-ന്റെ *period* *bob*-ന്റെ *mass*-നെ ആശ്രയിക്കുന്നു. *True* or *False*?", dict(size=56, max_w=920, hl=YELLOW)),
    "CMT":  (5, 7.6, "ഉത്തരം *comment* ചെയ്യൂ!", dict(size=56, max_w=900, hl=CYAN)),
    "FOL":  (5, 9.4, "*Follow* ചെയ്യൂ", dict(size=56, max_w=900, hl=YELLOW)),
}
WT = {k: [S0[sc] + st + i * PACE for i in range(len(txt.split()))] for k, (sc, st, txt, _) in BLOCKS.items()}
WT["HOOK"] = [0.1 + i * 0.3 for i in range(len(BLOCKS["HOOK"][2].split()))]   # fast hook: whole question visible by ~3.3 s
EV = dict(MASS=S0[0] + 0.6, LBL=S0[1] + 2.4, FORM=S0[2] + 12.6, NOM=S0[2] + 13.8, PROP=S0[3] + 4.6,
          EXAM=S0[5] + 0.4, OPT_A=S0[5] + 5.0, OPT_B=S0[5] + 5.4, SRC=S0[4] + 3.0)

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
ROPE = (200, 185, 150, 255)
def theta(T, period, amp, t0=0.0):
    return amp * math.sin(2 * math.pi * (T - t0) / period)

def frame_beam(d, x0, x1, y, gy):
    """Swing frame: top beam + two slanted legs to the ground."""
    col = (120, 90, 60)
    d.line((x0 - 40, y, x1 + 40, y), fill=col, width=22)
    for x in (x0 - 20, x1 + 20):
        d.line((x, y, x - 70, gy), fill=col, width=16)
        d.line((x, y, x + 70, gy), fill=col, width=16)

def swing(fr, px, py, Lr, th, who="kid", y0=600, h=760, alpha=1.0):
    """Side view swing with a seated person. who: 'kid', 'adult' or None (empty seat)."""
    L = SS(W, h); d = L.d; k = L.s
    ux, uy = math.sin(th), math.cos(th)          # along rope, pivot -> seat
    fx, fy = math.cos(th), -math.sin(th)          # 'forward' (perpendicular)
    sx, sy = px + Lr * ux, py + Lr * uy
    P = lambda x, y: k(x, y - y0)
    a = int(255 * alpha)
    d.line(P(px, py) + P(sx, sy), fill=ROPE[:3] + (a,), width=10)
    # seat plank
    d.line(P(sx - 48 * fx, sy - 48 * fy) + P(sx + 48 * fx, sy + 48 * fy), fill=(150, 95, 50, a), width=26)
    if who:
        s = 0.72 if who == "kid" else 1.0
        body = (255, 159, 67, a) if who == "kid" else (79, 140, 230, a)
        skin = (150, 100, 70, a)
        hip = (sx - 10 * fx - 14 * uy * 0, sy - 14)
        hip = (sx - 14 * ux, sy - 14 * uy)
        sh = (hip[0] - 120 * s * ux, hip[1] - 120 * s * uy)
        hd = (sh[0] - 36 * s * ux, sh[1] - 36 * s * uy)
        knee = (hip[0] + 92 * s * fx, hip[1] + 92 * s * fy)
        foot = (knee[0] + 85 * s * ux, knee[1] + 85 * s * uy)
        leg = (90, 105, 190, a)
        d.line(P(*hip) + P(*knee), fill=leg, width=int(26 * s * 2))
        d.line(P(*knee) + P(*foot), fill=leg, width=int(22 * s * 2))
        d.line(P(*hip) + P(*sh), fill=body, width=int(40 * s * 2))
        hand = (px + (Lr - 120 * s) * ux, py + (Lr - 120 * s) * uy)
        d.line(P(*sh) + P(*hand), fill=body, width=int(14 * s * 2))
        r = 30 * s
        d.ellipse(P(hd[0] - r, hd[1] - r) + P(hd[0] + r, hd[1] + r), fill=skin)
    img = L.done()
    fr.paste(img, (0, y0), img)
    return sx, sy

def pendulum(fr, d, px, py, Lr, th, r=38, col=(255, 209, 102), y0=500, h=900):
    L = SS(W, h); dd = L.d; k = L.s
    bx, by = px + Lr * math.sin(th), py + Lr * math.cos(th)
    P = lambda x, y: k(x, y - y0)
    dd.line(P(px, py) + P(bx, by), fill=(220, 225, 245, 255), width=8)
    dd.ellipse(P(px - 10, py - 10) + P(px + 10, py + 10), fill=(200, 205, 230, 255))
    dd.ellipse(P(bx - r, by - r) + P(bx + r, by + r), fill=col + (255,))
    img = L.done(); fr.paste(img, (0, y0), img)
    return bx, by

def dashed_arc(d, px, py, Lr, amp, col=(150, 160, 220)):
    n = 26
    for i in range(n):
        if i % 2: continue
        a1 = -amp + 2 * amp * i / n; a2 = -amp + 2 * amp * (i + 1) / n
        d.line((px + Lr * math.sin(a1), py + Lr * math.cos(a1), px + Lr * math.sin(a2), py + Lr * math.cos(a2)), fill=col, width=4)

def ground(d, y=1250):
    d.rectangle((0, y, W, y + 60), fill=(26, 40, 46))
    d.line((0, y, W, y), fill=(91, 160, 120), width=5)

# ---------------- static assets ----------------
KID = pill("കുട്ടി · 25 kg", 32, fg=(9, 14, 38), bg=ORANGE)
ADULT = pill("അച്ഛൻ · 75 kg", 32, fg=WHITE, bg=(60, 110, 210))
LB_L = boxed(text_img("L", 46, max_w=80, color=CYAN), pad=12)
LB_TH = text_img("θ", 40, max_w=80, color=YELLOW)
LB_M = text_img("m", 40, max_w=80, color=(9, 14, 38))
LB_MG = text_img("mg", 42, max_w=120, color=PINK)
DEF_PILL = pill("SIMPLE PENDULUM", 40, bg=YELLOW)
DEF_H = text_img(BLOCKS["DEF"][2], 52, max_w=880, hl=YELLOW, lh=1.45)
DEF_CARD = card(960, DEF_H.height + 50)
FORM = text_img("T = 2π √(L / g)", 92, max_w=960, color=CYAN)
NOM = pill("ഇതിൽ mass (m) ഇല്ല!", 42, fg=WHITE, bg=RED)
LB_SL = boxed(text_img("L", 40, max_w=80, color=CYAN), pad=10)
LB_LL = boxed(text_img("4L", 40, max_w=100, color=ORANGE), pad=10)
T1 = pill("T", 38, fg=(9, 14, 38), bg=CYAN)
T2 = pill("2T", 38, fg=(9, 14, 38), bg=ORANGE)
PROP = pill("T ∝ √L", 46, fg=(9, 14, 38), bg=YELLOW)
QUIZ = pill("QUIZ TIME", 44, fg=(9, 14, 38), bg=PINK)
EXAM = pill("PYQ · Plus One Exam 2022", 30, fg=WHITE, bg=(80, 60, 160))
OPT_A = card(440, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(440, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A)  True", 46, max_w=420)
TB = text_img("B)  False", 46, max_w=420)

# ---------------- scenes ----------------
SW_T, SW_A = 2.4, 0.42   # swing period (s, on screen) and amplitude (rad)
def s1(fr, t, d):
    sc = 0
    ground(d)
    frame_beam(d, 150, 930, 800, 1250)
    th = theta(t, SW_T, SW_A) * ease_out(prog(t, 0.0, 1.2))
    swing(fr, 350, 800, 340, th, "kid")
    swing(fr, 730, 800, 340, th, "adult")
    top_tag(fr, t, fade=True)
    say(fr, "HOOK", W / 2, 330, t, sc)
    appear(fr, KID, 350, 712, t, ev("MASS", sc), pop=True)
    appear(fr, ADULT, 730, 712, t, ev("MASS", sc) + 0.3, pop=True)
    say(fr, "TEASE", W / 2, 1340, t, sc, out_at=7.6)
    say(fr, "CAP1", W / 2, 1330, t, sc)

PV = (540, 700); PL = 420; PA = 0.42; PT = 2.6
def s2(fr, t, d):
    sc = 1
    top_tag(fr, t)
    say(fr, "WHY", W / 2, 340, t, sc)
    say(fr, "DEFP", W / 2, 460, t, sc)
    d.line((PV[0] - 140, PV[1], PV[0] + 140, PV[1]), fill=(120, 90, 60), width=14)
    dashed_arc(d, PV[0], PV[1], PL, PA)
    la = ease_out(prog(t, ev("LBL", sc), 0.5))
    if la > 0:  # vertical reference line + angle
        for yy in range(PV[1], PV[1] + PL, 24):
            d.line((PV[0], yy, PV[0], yy + 12), fill=(110, 120, 170), width=3)
    th = theta(t, PT, PA)
    bx, by = pendulum(fr, d, PV[0], PV[1], PL, th)
    if la > 0:
        paste(fr, LB_L, PV[0] + PL * 0.5 * math.sin(th) + 60, PV[1] + PL * 0.5 * math.cos(th) - 40, la)
        paste(fr, LB_TH, PV[0] + (40 if th >= 0 else -40) * 1.0, PV[1] + 80, la * min(1, abs(th) / 0.15))
        paste(fr, LB_M, bx, by - 30, la)
        arrow(d, bx, by + 40, bx, by + 40 + 90 * la, PINK, 8, 26)
        paste(fr, LB_MG, bx + 60, by + 60, la)
    say(fr, "SHM", W / 2, 1330, t, sc)

def s3(fr, t, d):
    sc = 2
    top_tag(fr, t)
    appear(fr, DEF_PILL, W / 2, 330, t, 0.1, pop=True)
    appear(fr, DEF_CARD, W / 2, 430, t, 0.3)
    say(fr, "DEF", W / 2, 455, t, sc)
    say(fr, "DEF_ML", W / 2, 455 + DEF_H.height + 80, t, sc)
    appear(fr, FORM, W / 2, 1060, t, ev("FORM", sc), pop=True)
    appear(fr, NOM, W / 2, 1260, t, ev("NOM", sc), pop=True)

SA, SB = (300, 560, 140), (760, 560, 560)
def s4(fr, t, d):
    sc = 3
    top_tag(fr, t)
    say(fr, "LEN", W / 2, 330, t, sc)
    d.line((140, 560, 940, 560), fill=(120, 90, 60), width=14)
    a = ease_out(prog(t, 1.4, 0.6))
    T0 = 1.2
    th1 = theta(t, T0, 0.45, 1.4) * a
    th2 = theta(t, 2 * T0, 0.45, 1.4) * a
    b1 = pendulum(fr, d, SA[0], SA[1], SA[2], th1, r=34, col=(79, 209, 255))
    b2 = pendulum(fr, d, SB[0], SB[1], SB[2], th2, r=40, col=(255, 159, 67))
    if a > 0:
        paste(fr, LB_SL, SA[0] + 70 * math.sin(th1) - 50, SA[1] + 70 * math.cos(th1) - 35, a)
        paste(fr, LB_LL, SB[0] + 280 * math.sin(th2) - 60, SB[1] + 280 * math.cos(th2) - 35, a)
    appear(fr, T1, SA[0], 760, t, 3.2, pop=True)
    appear(fr, T2, SB[0], 1200, t, 3.6, pop=True)
    appear(fr, PROP, SA[0], 940, t, ev("PROP", sc), pop=True)
    say(fr, "BOT", W / 2, 1330, t, sc)

FACT_P = pill("നിങ്ങൾക്കറിയാമോ?", 44, fg=(9, 14, 38), bg=PINK)
FOUC = pill("Foucault Pendulum", 32, fg=WHITE, bg=(80, 60, 160))
SRC_P = pill("Source: Encyclopaedia Britannica", 26, fg=WHITE, bg=(60, 70, 120))
TL = pill("time-lapse · മുകളിൽ നിന്നുള്ള കാഴ്ച", 26, fg=(9, 14, 38), bg=MUTED)
FC = (540, 950); FR = 215
def s_fact(fr, t, d):
    sc = 4
    top_tag(fr, t)
    appear(fr, FACT_P, W / 2, 310, t, 0.1, pop=True)
    say(fr, "F1", W / 2, 410, t, sc)
    a = ease_out(prog(t, 2.2, 0.6))
    if a > 0:
        L = SS(W, 520); dd = L.d; k = L.s; oy = FC[1] - 260
        cx, cy = FC[0], FC[1] - oy
        dd.ellipse(k(cx - FR - 20, cy - FR - 20, cx + FR + 20, cy + FR + 20), fill=(30, 36, 80, int(230 * a)), outline=(150, 160, 220, int(255 * a)), width=6)
        for i in range(36):  # pins around the floor circle
            ang = i * math.pi / 18
            x, y = cx + FR * math.cos(ang), cy + FR * math.sin(ang)
            dd.ellipse(k(x - 6, y - 6, x + 6, y + 6), fill=(255, 209, 102, int(255 * a)))
        phi = math.radians(20) + math.radians(9) * max(0.0, t - 3.0)   # sped-up turning of the swing plane
        ux, uy = math.cos(phi), math.sin(phi)
        dd.line(k(cx - FR * ux, cy - FR * uy, cx + FR * ux, cy + FR * uy), fill=(79, 209, 255, int(120 * a)), width=4)
        for j in range(1, 6):  # faint old swing lines (trail)
            p2 = phi - math.radians(6) * j
            dd.line(k(cx - FR * math.cos(p2), cy - FR * math.sin(p2), cx + FR * math.cos(p2), cy + FR * math.sin(p2)), fill=(79, 209, 255, int(45 * a / j)), width=3)
        r = FR * 0.85 * math.sin(2 * math.pi * t / 1.6)
        bx, by = cx + r * ux, cy + r * uy
        dd.ellipse(k(bx - 30, by - 30, bx + 30, by + 30), fill=(255, 159, 67, int(255 * a)))
        dd.ellipse(k(cx - 8, cy - 8, cx + 8, cy + 8), fill=(220, 225, 245, int(255 * a)))
        img = L.done(); fr.paste(img, (0, oy), img)
        paste(fr, TL, W / 2, FC[1] - FR - 95, a)
        paste(fr, FOUC, W / 2, FC[1] + FR + 30, a)
    say(fr, "F2", W / 2, 1255, t, sc, out_at=WT["F3"][0] - S0[sc] - 0.35)
    say(fr, "F3", W / 2, 1290, t, sc)
    appear(fr, SRC_P, W / 2, 1505, t, ev("SRC", sc))

def s5(fr, t, d):
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

SCENES = list(zip(D, (s1, s2, s3, s4, s_fact, s5)))

VOICE = None
SFX = [(0.15, "pop")]
# soft swoosh each time the swings pass the lowest point (scene 1)
k = 1
while k * SW_T / 2 < D[0] - 0.3:
    SFX.append((k * SW_T / 2 - 0.15, "swoosh")); k += 1
for s in S0[1:]:
    SFX += [(s, "whoosh"), (s + 0.15, "pop")]
SFX += [(WT["TEASE"][0], "boing"), (EV["MASS"], "pop"), (EV["MASS"] + 0.3, "pop"), (WT["CAP1"][0], "ding"), (EV["LBL"], "pop"), (WT["SHM"][0], "pop"),
        (S0[2] + 0.3, "pop"), (WT["DEF_ML"][0], "pop"), (EV["FORM"], "ding"), (EV["NOM"], "boing"),
        (S0[3] + 3.2, "pop"), (S0[3] + 3.6, "pop"), (EV["PROP"], "ding"), (WT["BOT"][0], "pop"),
        (S0[4] + 0.1, "chime"), (S0[4] + 2.2, "whoosh"), (EV["SRC"], "pop"), (WT["F2"][0], "pop"), (WT["F3"][0], "ding"),
        (EV["EXAM"], "pop"), (EV["OPT_A"], "pop"), (EV["OPT_B"], "pop"), (EV["OPT_B"] + 0.6, "ticks"),
        (WT["CMT"][0], "pop"), (WT["FOL"][0], "chime")]
SFX = [(max(0.0, s), k_) for s, k_ in SFX if s < END - 0.3]
MUSIC = [(0.0, "ocean"), (WT["CAP1"][0] - 0.2, "uplift"), (S0[1], "tension"), (S0[2], "cinematic"), (S0[3], "curious"),
         (S0[4], "space"), (S0[5], "tension"), (WT["FOL"][0] - 0.3, "uplift")]
MUSIC_SEED = 713
