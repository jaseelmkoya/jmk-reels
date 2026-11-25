"""25 Nov 2026 · Why you spin faster on a revolving chair when you fold your arms — conservation of angular momentum
(Plus One · Ch6 System of Particles and Rotational Motion). Syllabus topic (no news story with a clear physics link in the last 72 h).
Why chain: no external torque about the chair's axis (τ = 0) → τ = dL/dt → L stays constant → L = Iω, so if I falls ω must rise
→ I = Σmr² depends on r² (mass far from the axis) → arms in: r small → I small → ω large (I₁ω₁ = I₂ω₂).
Extra KE: K = ½Iω² = L²/2I → I falls → K rises; the energy comes from the work our muscles do pulling the arms in.
Quiz: PYQ · Plus One March 2022 — duration of a day if Earth shrinks to 1/64 of its volume (R → R/4, I → I/16, ω ×16 → 1.5 h).
No voice by default: captions word by word at reading pace."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import reelkit
from storykit import *
from captions import Captions
reelkit.SYMBOLS |= set("−₁₂ωτΣ⇒⅖")

HANDLE = "@jmk.space"
random.seed(25)

LINES = [
    ("കൈ നീട്ടി പതുക്കെ കറങ്ങുന്നു... കൈ മടക്കിയതും *spin* മൂന്നിരട്ടി വേഗത്തിൽ! ആരും തള്ളിയില്ല!", YELLOW),
    ("കസേരയുടെ *axis*-ന് ചുറ്റും പുറത്തുനിന്ന് ഒരു *torque*-ഉം ഇല്ല: *external torque = 0*.", CYAN),
    ("*τ = dL/dt* — *torque* ഇല്ലെങ്കിൽ *angular momentum L* മാറില്ല. നോക്കൂ, *L* ബാർ അനങ്ങുന്നില്ല!", ORANGE),
    ("*L = Iω* മാറാതെ നിൽക്കണം. അപ്പോൾ *I* കുറഞ്ഞാൽ *ω* കൂടിയേ പറ്റൂ.", YELLOW),
    ("ഇനി *I* എന്തിന് കുറയുന്നു? *Moment of inertia* *I = Σmr²* — *mass* *axis*-ൽ നിന്ന് എത്ര ദൂരെ എന്നതാണ് പ്രധാനം.", CYAN),
    ("*r²* ആണ്! കയ്യിലെ *mass*-ന്റെ *r* പകുതിയായാൽ ആ ഭാഗത്തിന്റെ *I* നാലിലൊന്നാകും.", ORANGE),
    ("*I* കുറഞ്ഞു → *ω* കൂടി. *Ice skater*-ഉം *diver*-ഉം ചെയ്യുന്നത് ഇതേ trick തന്നെ!", PINK),
    ("അപ്പോൾ കൂടിയ *kinetic energy* എവിടെ നിന്ന്? *K = ½Iω² = L²/2I* — കൈ ഉള്ളിലേക്ക് വലിക്കുമ്പോൾ നമ്മുടെ പേശികൾ ചെയ്യുന്ന *work*-ൽ നിന്ന്!", GREEN),
]
PACE = 0.42
def _dur(i, extra): return len(LINES[i][0].split()) * PACE + extra

PLAN = [[0], [1, 2], [3], [4, 5, 6], [7], []]
GAP = {0: 2.4, 1: 1.0, 2: 1.8, 3: 1.8, 4: 1.0, 5: 1.6, 6: 1.6, 7: 2.0}
S, ST, starts = [], [0.0], []
for k, idx in enumerate(PLAN):
    t = 0.3 if k else 0.6
    for i in idx:
        starts.append(ST[-1] + t); t += _dur(i, GAP[i])
    S.append(t if idx else 9.5)
    ST.append(ST[-1] + S[-1])
CAP = Captions([(txt, st, None, hl) for (txt, hl), st in zip(LINES, starts)], None, size=52, wpm_pace=PACE)
def caps(fr, s_idx, t, y=1335): CAP.draw(fr, ST[s_idx] + t, y)
def ls(i, sc): return starts[i] - ST[sc]

TAG = pill("PLUS ONE PHYSICS · ROTATIONAL MOTION", 26, bg=CYAN)
BG_IMG = grad(W, H, [(0, (10, 14, 34)), (0.55, (26, 20, 60)), (1, (14, 16, 40))])

# ---------- physics of the spinning person (top view) ----------
I0 = 40000.0
def hand_local(f):            # f = 0 arms out, 1 folded
    return (1 - f) * 330 + f * 50, f * 80
def I_of(f):
    x, y = hand_local(f); return I0 + x * x + y * y
I_OUT, I_IN = I_of(0), I_of(1)
W_OUT = 1.25                   # rad/s with arms out
LMOM = W_OUT * I_OUT
def omega(f): return LMOM / I_of(f)

def fold_once(t0, d=0.6):
    return lambda t: ease_in_out(prog(t, t0, d))
def fold_cycle(start_in=True, out_t=1.8, in_t=1.8, mv=0.6, t0=0.0):
    per = out_t + in_t + 2 * mv
    def f(t):
        if t < t0: return 1.0 if start_in else 0.0
        u = (t - t0) % per
        if start_in:
            if u < in_t: return 1.0
            if u < in_t + mv: return 1 - ease_in_out((u - in_t) / mv)
            if u < in_t + mv + out_t: return 0.0
            return ease_in_out((u - in_t - mv - out_t) / mv)
        if u < out_t: return 0.0
        if u < out_t + mv: return ease_in_out((u - out_t) / mv)
        if u < out_t + mv + in_t: return 1.0
        return 1 - ease_in_out((u - out_t - mv - in_t) / mv)
    return f

class Spinner:
    """Precomputes angle θ(t) = ∫ω dt for a fold function over a scene."""
    def __init__(self, ffn, dur, th0=0.0):
        self.f = ffn; n = int(dur * 30) + 3; self.th = [th0]
        for k in range(n):
            self.th.append(self.th[-1] + omega(ffn(k / 30)) / 30)
    def at(self, t):
        k = min(len(self.th) - 1, int(t * 30)); return self.th[k], self.f(t)

def rot(x, y, th): c, s = math.cos(th), math.sin(th); return x * c - y * s, x * s + y * c

def person(fr, cx, cy, th, f, s=1.0, trail=True, rlabel=None):
    L = SS(W, 900); d = L.d; k = L.k
    oy = cy - 450
    P = lambda x, y: ((cx + x) * k, (450 + y) * k)
    # chair base (static star) + seat
    for j in range(5):
        a = j * 2 * math.pi / 5 + 0.3
        d.line(P(0, 0) + P(200 * s * math.cos(a), 200 * s * math.sin(a)), fill=(70, 74, 100, 255), width=int(16 * k))
        ex, ey = 200 * s * math.cos(a), 200 * s * math.sin(a)
        d.ellipse(P(ex - 16 * s, ey - 16 * s) + P(ex + 16 * s, ey + 16 * s), fill=(40, 40, 52, 255))
    d.ellipse(P(-150 * s, -150 * s) + P(150 * s, 150 * s), fill=(60, 66, 120, 255))
    w_ = omega(f)
    hx, hy = hand_local(f)
    # speed trails behind the hands
    if trail:
        ln = 0.35 * w_
        for side in (1, -1):
            r_ = math.hypot(hx, hy) * s
            a0 = math.atan2(side * hy, side * hx) + th
            pts = []
            for q in range(14):
                a = a0 - ln * q / 13
                pts.append(P(r_ * math.cos(a), r_ * math.sin(a)))
            for q in range(13):
                al = int(200 * (1 - q / 13))
                d.line(pts[q] + pts[q + 1], fill=(255, 209, 102, al), width=int(10 * k * (1 - q / 15)))
    # body: shoulders ellipse rotated
    sh = [rot(120 * s * math.cos(a), 62 * s * math.sin(a), th) for a in [i * 2 * math.pi / 40 for i in range(40)]]
    shirt = (255, 120, 90, 255)
    for side in (1, -1):
        sx, sy = rot(side * 100 * s, 0, th)
        ex, ey = rot(side * hx * s, hy * s, th)
        mx, my = rot(side * (100 + (hx - 100) * 0.5 + 40 * f) * s, (hy * 0.5 + 40 * f) * s, th)
        d.line(P(sx, sy) + P(mx, my), fill=(225, 170, 130, 255), width=int(34 * s * k))
        d.line(P(mx, my) + P(ex, ey), fill=(225, 170, 130, 255), width=int(30 * s * k))
        d.ellipse(P(mx - 16 * s, my - 16 * s) + P(mx + 16 * s, my + 16 * s), fill=(225, 170, 130, 255))
        # dumbbell in the hand
        d.ellipse(P(ex - 34 * s, ey - 34 * s) + P(ex + 34 * s, ey + 34 * s), fill=(91, 228, 155, 255), outline=(20, 60, 40, 255), width=int(4 * k))
    d.polygon([P(x, y) for x, y in sh], fill=shirt)
    hxh, hyh = rot(0, 18 * s, th)
    d.ellipse(P(hxh - 52 * s, hyh - 52 * s) + P(hxh + 52 * s, hyh + 52 * s), fill=(40, 30, 30, 255))
    nx, ny = rot(0, 64 * s, th)
    d.ellipse(P(nx - 12 * s, ny - 12 * s) + P(nx + 12 * s, ny + 12 * s), fill=(225, 170, 130, 255))
    d.ellipse(P(-12 * s, -12 * s) + P(12 * s, 12 * s), outline=(255, 255, 255, 120), width=int(3 * k))
    img = L.done()
    fr.paste(img, (0, int(oy)), img)
    if rlabel is not None:   # radius line from the axis to one hand
        ex, ey = rot(hx * s, hy * s, th)
        d2 = ImageDraw.Draw(fr)
        d2.line((cx, cy, cx + ex, cy + ey), fill=CYAN, width=5)

def meters(fr, d, f, y0=1030, a=1.0, show_L=True):
    if a <= 0.01: return
    I = I_of(f); w_ = omega(f)
    rows = [("I", I / I_OUT, PINK), ("ω", w_ / omega(1.0), YELLOW)]
    if show_L: rows.append(("L = Iω", 0.62, GREEN))
    for j, (lab, v, col) in enumerate(rows):
        y = y0 + j * 78
        tl = METER_LBL[lab]
        paste(fr, tl, 190, y - 6, a)
        d.rounded_rectangle((330, y, 330 + 600, y + 46), radius=23, fill=(40, 44, 80))
        d.rounded_rectangle((330, y, 330 + max(46, int(600 * v)), y + 46), radius=23, fill=col)
METER_LBL = {k: text_img(k, 40, max_w=260, color=WHITE) for k in ("I", "ω", "L = Iω")}

# ---------- S0 hook ----------
HOOK = text_img("കറങ്ങുന്ന കസേരയിൽ കൈ മടക്കിയാൽ *വേഗം* കൂടുന്നത് എന്തുകൊണ്ട്?", 64, max_w=980, hl=YELLOW)
H0 = headline("WHY *FASTER?*", hl=YELLOW, size=100)
TOPV = boxed(text_img("TOP VIEW", 30, max_w=220, color=MUTED), pad=10)
FOLD_T = ls(0, 0) + 3.2
SP0 = Spinner(fold_once(FOLD_T), S[0] + 0.5)
X3 = boxed(text_img("ω × 3!", 54, max_w=300, color=YELLOW), pad=14, outline=(255, 209, 102, 200))
def s0(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    th, f = SP0.at(t)
    person(fr, W / 2, 860, th, f, 1.0)
    paste(fr, H0, W / 2, 130)
    paste(fr, HOOK, W / 2, 290, 1.0, 1 + 0.02 * math.sin(t * 4))
    paste(fr, TAG, W / 2, 245, ease_out(prog(t, 1.5, 0.4)))
    paste(fr, TOPV, 150, 1220, ease_out(prog(t, 1.0, 0.4)))
    appear(fr, X3, 880, 640, t, FOLD_T + 0.7, pop=True)
    caps(fr, 0, t)

# ---------- S1 no external torque, meters ----------
H1 = headline("NO *TORQUE*", hl=CYAN, size=96)
TZ = boxed(text_img("*external torque* τ = 0", 40, max_w=700, hl=CYAN), pad=14, outline=(79, 209, 255, 180))
TDL = boxed(text_img("τ = dL/dt  →  L = *constant*", 40, max_w=800, hl=GREEN), pad=14, outline=(91, 228, 155, 180))
SP1 = Spinner(fold_cycle(True, 1.6, 1.6, 0.6), S[1] + 0.5, SP0.th[-1])
def s1(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    th, f = SP1.at(t)
    person(fr, W / 2, 720, th, f, 0.75)
    paste(fr, H1, W / 2, 150)
    appear(fr, TZ, W / 2, 285, t, ls(1, 1) + 1.0, pop=True)
    appear(fr, TDL, W / 2, 370, t, ls(2, 1) + 0.6, pop=True)
    meters(fr, d, f, 1010, ease_out(prog(t, ls(2, 1) + 1.5, 0.5)))
    caps(fr, 1, t)

# ---------- S2 law card ----------
LP = pill("CONSERVATION OF ANGULAR MOMENTUM", 32, bg=YELLOW)
LAW = text_img("If external torque is zero, the angular momentum *L = Iω* is constant.", 46, max_w=880, hl=YELLOW, lh=1.45)
LEQ = text_img("I₁ω₁ = I₂ω₂", 76, max_w=900, color=CYAN)
LCARD = card(960, LAW.height + 150)
SA = Spinner(lambda t: 0.0, S[2] + 0.5); SB = Spinner(lambda t: 1.0, S[2] + 0.5)
LA = text_img("*I* വലുത് → *ω* ചെറുത്", 36, max_w=440, hl=PINK)
LB = text_img("*I* ചെറുത് → *ω* വലുത്", 36, max_w=440, hl=YELLOW)
def s2(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    appear(fr, LP, W / 2, 200, t, 0.1, pop=True)
    appear(fr, LCARD, W / 2, 300, t, 0.3)
    appear(fr, LAW, W / 2, 318, t, 0.4)
    appear(fr, LEQ, W / 2, 318 + LAW.height, t, 1.0, pop=True)
    a = ease_out(prog(t, 1.6, 0.5))
    if a > 0:
        tha, fa = SA.at(t); thb, fb = SB.at(t)
        person(fr, 290, 900, tha, fa, 0.6)
        person(fr, 790, 900, thb, fb, 0.6)
        paste(fr, LA, 290, 1140, a); paste(fr, LB, 790, 1140, a)
    caps(fr, 2, t)

# ---------- S3 I = Σmr² ----------
H3 = headline("MOMENT OF *INERTIA*", hl=CYAN, size=90)
IEQ = text_img("I = Σmr²", 72, max_w=600, color=CYAN)
RL_OUT = boxed(text_img("r", 44, max_w=80, color=CYAN), pad=10)
RQ = boxed(text_img("r → r/2   ⇒   r² → r²/4", 42, max_w=760, hl=ORANGE, color=ORANGE), pad=14, outline=(255, 159, 67, 180))
SK = boxed(text_img("*Ice skater* · *diver* · *dancer*", 40, max_w=820, hl=PINK), pad=14, outline=(255, 107, 157, 180))
SP3 = Spinner(fold_cycle(False, 2.2, 2.0, 0.8, 0.3), S[3] + 0.5, SP1.th[-1])
def s3(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    th, f = SP3.at(t)
    person(fr, W / 2, 800, th, f, 0.8, rlabel=True)
    hx, hy = hand_local(f); ex, ey = rot(hx * 0.8, hy * 0.8, th)
    paste(fr, RL_OUT, W / 2 + ex * 0.6, 800 + ey * 0.6 - 40)
    paste(fr, H3, W / 2, 140)
    paste(fr, IEQ, W / 2, 250)
    appear(fr, RQ, W / 2, 370, t, ls(5, 3) + 0.8, pop=True)
    meters(fr, d, f, 1090, ease_out(prog(t, ls(4, 3) + 2.0, 0.5)), show_L=False)
    appear(fr, SK, W / 2, 460, t, ls(6, 3) + 1.5, pop=True)
    caps(fr, 3, t)

# ---------- S4 energy ----------
H4 = headline("EXTRA *ENERGY?*", hl=GREEN, size=96)
KE = text_img("K = ½Iω² = L² / 2I", 64, max_w=960, color=GREEN)
KI = boxed(text_img("*I* ↓  →  *K* ↑", 46, max_w=600, hl=YELLOW), pad=14, outline=(255, 209, 102, 180))
WK = boxed(text_img("*Work* by our muscles", 38, max_w=700, hl=ORANGE), pad=12, outline=(255, 159, 67, 180))
SP4 = Spinner(fold_cycle(False, 1.6, 1.8, 0.9, 0.2), S[4] + 0.5, SP3.th[-1])
def s4(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    th, f = SP4.at(t)
    person(fr, W / 2, 820, th, f, 0.85)
    # inward pull arrows while folding
    u = (t - 0.2) % (1.6 + 1.8 + 1.8)
    if 1.6 <= u < 2.5:
        for side in (1, -1):
            hx, hy = hand_local(f); ex, ey = rot(side * hx * 0.85, hy * 0.85, th)
            n = math.hypot(ex, ey) or 1
            arrow(d, W / 2 + ex * 1.35, 820 + ey * 1.35, W / 2 + ex * 1.05, 820 + ey * 1.05, ORANGE, 10, 30)
    paste(fr, H4, W / 2, 150)
    appear(fr, KE, W / 2, 300, t, ls(7, 4) + 2.5, pop=True)
    appear(fr, KI, W / 2, 420, t, ls(7, 4) + 4.0, pop=True)
    appear(fr, WK, W / 2, 1210, t, ls(7, 4) + 7.0, pop=True)
    caps(fr, 4, t)

# ---------- S5 quiz ----------
QUIZ = pill("QUIZ TIME", 46, fg=(9, 14, 38), bg=PINK)
PYQ = pill("PYQ · Plus One March 2022", 32, fg=WHITE, bg=(80, 60, 160))
Q = text_img("ഭൂമി ചുരുങ്ങി *volume* ഇപ്പോഴത്തേതിന്റെ *1/64* ആയാൽ ഒരു ദിവസം എത്ര മണിക്കൂർ?", 54, max_w=940, hl=YELLOW)
HINT = text_img("(*L = Iω* constant · *I = ⅖MR²*)", 36, max_w=900, hl=CYAN, color=MUTED)
OPT_A = card(460, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(460, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) 1.5 hours", 44, max_w=440)
TB = text_img("B) 24 hours", 44, max_w=440)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 58, max_w=900, hl=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 58, max_w=900, hl=YELLOW)
def s5(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    appear(fr, QUIZ, W / 2, 270, t, 0.1, pop=True)
    appear(fr, PYQ, W / 2, 370, t, 0.3)
    appear(fr, Q, W / 2, 470, t, 0.5)
    appear(fr, HINT, W / 2, 470 + Q.height + 10, t, 1.8)
    for i, (c, tx, cx) in enumerate(((OPT_A, TA, 290), (OPT_B, TB, 790))):
        st = 3.2 + i * 0.5
        pulse = 1 + 0.03 * math.sin((t - st) * 6 + i * 3) if t > st + 0.6 else 1
        appear(fr, c, cx, 910, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 950, ease_out(prog(t, st + 0.05, 0.3)), pulse)
    appear(fr, CMT, W / 2, 1130, t, 5.0, pop=True)
    appear(fr, FOL, W / 2, 1270, t, 6.5, pop=True)

SCENES = [(S[i], f) for i, f in enumerate((s0, s1, s2, s3, s4, s5))]
VOICE = None
MUSIC_GAIN = 0.4
MUSIC = [(0.0, "curious"), (ST[1], "tension"), (ST[2], "uplift"), (ST[3], "drive"), (ST[4], "curious"), (ST[5], "tension"), (ST[5] + 6.4, "uplift")]
MUSIC_SEED = 2511
SFX = [(0.0, "whoosh"), (FOLD_T, "swoosh"), (FOLD_T + 0.7, "pop"), (FOLD_T + 0.75, "ding"),
       (ST[1] + 0.1, "swoosh"), (starts[1] + 1.0, "pop"), (starts[2], "pop"), (starts[2] + 3.0, "ding"),
       (ST[2] + 0.1, "pop"), (ST[2] + 1.0, "ding"), (ST[2] + 1.6, "whoosh"),
       (ST[3] + 0.1, "swoosh"), (starts[5] + 0.8, "pop"), (starts[6], "ding"),
       (ST[4] + 0.1, "swoosh"), (starts[7] + 2.5, "pop"), (starts[7] + 4.0, "ding"), (starts[7] + 7.0, "pop"),
       (ST[5] + 0.1, "pop"), (ST[5] + 3.2, "pop"), (ST[5] + 3.7, "pop"), (ST[5] + 4.3, "ticks"), (ST[5] + 6.5, "chime")]
if __name__ == "__main__": print("total", round(ST[-1], 1), [round(x, 1) for x in S])
