"""17 Nov 2026 · Why aeroplanes fly — Bernoulli + Newton's third law (Plus One · Mechanical Properties of Fluids).
Myth: 'equal transit time' (air over the top and bottom must meet at the trailing edge) is false — air over the
top reaches the trailing edge FIRST (NASA Glenn 'Incorrect Lift Theory'). Lift = pressure difference
(faster flow on top → lower pressure, Bernoulli) + wing turns air downward (downwash) → air pushes wing up (Newton's 3rd).
A380 maximum take-off mass ≈ 575 t ("500 ടണ്ണിലേറെ").
Quiz: concept (no PYQ label): Bernoulli's principle is based on conservation of A) energy B) momentum → A.
No voice by default: captions word by word at reading pace."""
import math, sys, os, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storykit import *
from captions import Captions

random.seed(11)
BW, BH = int(W * 1.12), int(H * 1.12)
SKY = grad(BW, BH, [(0, (8, 18, 48)), (0.55, (24, 52, 104)), (1, (240, 150, 90))])
LAB = grad(BW, BH, [(0, (8, 12, 30)), (1, (14, 22, 50))])
RED = (235, 70, 80)

# ---------- airliner (side view) ----------
def plane(d, cx, cy, s, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    def P(x, y): return (cx + (x * ca - y * sa) * s, cy + (x * sa + y * ca) * s)
    def poly(pts, col): d.polygon([P(*p) for p in pts], fill=col)
    poly([(-330, -10), (-250, -150), (-200, -150), (-170, -10)], (40, 90, 170))            # tail fin
    body = [(-340, -40), (260, -45), (330, -20), (350, 10), (300, 40), (-330, 35), (-360, 0)]
    poly(body, (235, 240, 250))
    poly([(300, -30), (335, -12), (310, -12)], (40, 60, 90))                                  # cockpit window
    for k in range(14):
        x = -260 + k * 38
        cxw, cyw = P(x, -15)
        d.ellipse((cxw - 6 * s, cyw - 6 * s, cxw + 6 * s, cyw + 6 * s), fill=(60, 90, 140))
    poly([(-40, 10), (90, 10), (-60, 110), (-120, 110)], (200, 210, 225))                     # wing
    poly([(-30, 40), (40, 40), (40, 75), (-30, 75)], (150, 160, 180))                         # engine
    poly([(-330, 10), (-260, 10), (-300, 60), (-340, 60)], (200, 210, 225))                   # tailplane
    d.line([P(-340, 5), P(340, 5)], fill=(40, 90, 170), width=max(2, int(8 * s)))            # livery stripe

CLOUDS = [(random.uniform(0, W), random.uniform(450, 1300), random.uniform(0.6, 1.4)) for _ in range(9)]
def clouds(d, t, speed=260):
    for x, y, sc in CLOUDS:
        xx = (x - t * speed * sc) % (W + 400) - 200
        for dx, dy, r in ((0, 0, 60), (55, -20, 70), (115, 0, 55), (60, 15, 60)):
            rr = r * sc
            d.ellipse((xx + dx * sc - rr, y + dy * sc - rr, xx + dx * sc + rr, y + dy * sc + rr), fill=(225, 230, 245))

# ---------- wing section + streamlines ----------
CX0, CY0, CH = 230, 900, 620          # leading edge x, chord-line y, chord length (px)
def _naca(x):  # x in 0..1 → (upper y, lower y) in px (screen: up = negative)
    m, p, tt = 0.05, 0.4, 0.14
    yt = 5 * tt * (0.2969 * math.sqrt(x) - 0.126 * x - 0.3516 * x * x + 0.2843 * x ** 3 - 0.1036 * x ** 4)
    yc = m / p ** 2 * (2 * p * x - x * x) if x < p else m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x - x * x)
    return -(yc + yt) * CH, -(yc - yt) * CH
XS = np.linspace(0, 1, 80)
UP = [(CX0 + x * CH, CY0 + _naca(x)[0]) for x in XS]
LO = [(CX0 + x * CH, CY0 + _naca(x)[1]) for x in XS]
WING = UP + LO[::-1]
def wing(d, col=(225, 232, 245)):
    d.polygon(WING, fill=col, outline=(120, 140, 180))

def _surf(x, upper):
    if x <= CX0 or x >= CX0 + CH: return 0.0
    u, l = _naca((x - CX0) / CH)
    return (u if upper else l)

def streamline(y0, down=1.0):
    """Polyline (x, y) and local speed for a streamline starting far left at height y0."""
    upper = y0 < CY0
    dist = abs(y0 - CY0)
    k = math.exp(-max(0, dist - 20) / 170)
    pts, sp = [], []
    for x in np.linspace(-40, W + 40, 220):
        y = y0 + _surf(x, upper) * k * (1.0 if upper else 0.9)
        up = 26 * k * math.exp(-((x - CX0 + 40) / 110) ** 2)                 # upwash ahead of the wing
        dw = 90 * down * (0.4 + 0.6 * k) / (1 + math.exp(-(x - CX0 - CH) / 70))   # downwash behind
        y = y - up + dw
        over = 1.0 if CX0 - 60 < x < CX0 + CH + 30 else math.exp(-min(abs(x - CX0 + 60), abs(x - CX0 - CH - 30)) / 120)
        v = 1 + (0.85 * k * over if upper else -0.3 * k * over)
        pts.append((x, y)); sp.append(v)
    pts = np.array(pts); sp = np.array(sp)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    tau = np.concatenate([[0], np.cumsum(seg / ((sp[1:] + sp[:-1]) / 2))])
    return pts, tau
SL_Y = [640, 700, 760, 820, 990, 1050, 1110, 1170]
SLS = [streamline(y) for y in SL_Y]
V0 = 230.0  # px/s base speed

def flow(d, t, alpha=255, dots=True, down=1.0):
    for (pts, tau), y0 in zip(SLS, SL_Y):
        upper = y0 < CY0
        col = (79, 209, 255) if upper else (255, 159, 67)
        d.line([tuple(p) for p in pts], fill=col + (int(alpha * 0.45),) if len(col) == 3 else col, width=3)
        if dots:
            T = tau[-1]
            for k in range(9):
                q = ((t * V0 + k * T / 9 * 1.0) % T)
                i = int(np.searchsorted(tau, q))
                i = min(max(i, 1), len(pts) - 1)
                x, y = pts[i]
                d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=col)

def parcel_pos(si, t):
    pts, tau = SLS[si]
    i0 = int(np.searchsorted(pts[:, 0], CX0 - 120))
    i1 = int(np.searchsorted(pts[:, 0], CX0 + CH))
    q = min(tau[i0] + t * V0, tau[i1])
    i = min(int(np.searchsorted(tau, q)), i1)
    return pts[i], i >= i1

# ---------- text ----------
H1 = headline("500 TONNE *FLYING?*", hl=YELLOW, size=96)
H2 = headline("SCHOOL STORY = *MYTH*", hl=RED, size=86)
H3 = headline("FAST AIR = *LOW P*", hl=CYAN, size=92)
H4 = headline("AIR *DOWN* = WING *UP*", hl=GREEN, size=88)
LAW_PILL = pill("BERNOULLI'S PRINCIPLE", 38, bg=YELLOW)
LAW = text_img("Non-viscous, incompressible fluid · streamline flow|*P + ½ρv² + ρgh = constant*", 38, max_w=920, hl=YELLOW, lh=1.45)
LAW_CARD = card(960, LAW.height + 40)
LOWP = boxed(text_img("*LOW P* · fast air", 40, max_w=500, hl=CYAN), outline=(79, 209, 255, 200))
HIGHP = boxed(text_img("*HIGH P* · slow air", 40, max_w=500, hl=ORANGE), outline=(255, 159, 67, 200))
LIFT = text_img("*LIFT*", 64, max_w=300, hl=GREEN)
FIRST = boxed(text_img("*1st!*", 46, max_w=200, hl=CYAN), outline=(79, 209, 255, 200))
WAIT = boxed(text_img("ഇനിയും *എത്തിയില്ല*", 36, max_w=500, hl=ORANGE), outline=(255, 159, 67, 200))
ACT = boxed(text_img("*Action*: wing → air ↓", 40, max_w=600, hl=ORANGE), outline=(255, 159, 67, 200))
REACT = boxed(text_img("*Reaction*: air → wing ↑", 40, max_w=600, hl=GREEN), outline=(91, 228, 155, 200))
N3 = pill("NEWTON'S THIRD LAW", 36, bg=GREEN)
TAG = pill("PLUS ONE PHYSICS · FLUIDS", 26, bg=CYAN)

QUIZ = pill("QUIZ TIME", 44, fg=(9, 14, 38), bg=PINK)
Q = text_img("*Bernoulli's principle* ഏത് *conservation*-ൽ നിന്നാണ്?", 58, max_w=920, hl=YELLOW)
OPT_A = card(480, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(480, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) Energy", 44, max_w=460)
TB = text_img("B) Momentum", 44, max_w=460)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 56, max_w=900, hl=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 56, max_w=900, hl=YELLOW)

# ---------- narration (word by word, reading pace) ----------
LINES = [
    ("500 ടണ്ണിലേറെ ഭാരമുള്ള *Airbus A380* വായുവിൽ നിൽക്കുന്നത് എങ്ങനെ?", YELLOW),
    ("പഠിച്ച കഥ: മുകളിലെയും താഴത്തെയും *air* ഒരേ സമയം പിന്നിൽ എത്തണം.", WHITE),
    ("ഇത് *myth* ആണ്! മുകളിലെ *air* ആദ്യം എത്തും — അത്ര വേഗത്തിലാണ് ഒഴുക്ക്.", RED),
    ("മുകളിൽ *velocity* കൂടുതൽ → *pressure* കുറവ്. താഴെ *pressure* കൂടുതൽ.", CYAN),
    ("ഈ *pressure difference* wing-നെ മുകളിലേക്ക് തള്ളുന്നു — ഇതാണ് *lift*.", GREEN),
    ("ഒപ്പം wing *air*-നെ താഴേക്ക് തള്ളുന്നു — *action*.", ORANGE),
    ("*Air* wing-നെ മുകളിലേക്ക് തള്ളുന്നു — *reaction*!", GREEN),
]
PACE = 0.42
def _dur(text, extra): return len(text.split()) * PACE + extra
S = [max(6.0, _dur(LINES[0][0], 1.6)),
     _dur(LINES[1][0], 0.6) + _dur(LINES[2][0], 1.6),
     max(10.5, _dur(LINES[3][0], 1.0) + _dur(LINES[4][0], 2.2)),
     _dur(LINES[5][0], 0.8) + _dur(LINES[6][0], 2.0),
     8.5]
ST = [0.0]
for d_ in S: ST.append(ST[-1] + d_)
starts = [ST[0] + 0.5, ST[1] + 0.3, ST[1] + 0.3 + _dur(LINES[1][0], 0.6), ST[2] + 0.4, ST[2] + 0.4 + _dur(LINES[3][0], 1.0),
          ST[3] + 0.3, ST[3] + 0.3 + _dur(LINES[5][0], 0.8)]
CAP = Captions([(txt, st, None, hl) for (txt, hl), st in zip(LINES, starts)], None, size=52, wpm_pace=PACE)
def caps(fr, s_idx, t, y=1340): CAP.draw(fr, ST[s_idx] + t, y)

# ---------- scenes ----------
def s1(fr, t, d):
    base = SKY.copy(); bd = ImageDraw.Draw(base)
    bd.rectangle((0, 1390, BW, BH), fill=(40, 44, 60))
    for k in range(12):
        x = (k * 180 - t * 900) % (BW + 200) - 100
        bd.rectangle((x, 1440, x + 90, 1452), fill=(240, 240, 240))
    fr.paste(push(base, t, S[0], 1.0, 1.06), (0, 0))
    clouds(d, t)
    lift = ease_in_out(prog(t, 0.3, S[0] - 0.3))
    ang = -0.22 * ease_out(prog(t, 0.2, 1.2))
    plane(d, W / 2 - 40 + 60 * lift, 1250 - 420 * lift, 1.15, ang)
    # lift arrow on the wing
    a = ease_out(prog(t, 2.2, 0.5))
    if a > 0:
        wx, wy = W / 2 - 40 + 60 * lift - 20, 1250 - 420 * lift + 40
        arrow(d, wx, wy, wx, wy - 260 * a - 10, GREEN, 14, 44)
        paste(fr, LIFT, wx + 120, wy - 250 * a - 40, a)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H1, W / 2, 220, 1.0)                                    # hook from frame 0
    paste(fr, TAG, W / 2, 365, ease_out(prog(t, 1.5, 0.4)))
    caps(fr, 0, t)

def s2(fr, t, d):
    fr.paste(push(LAB, t, S[1], 1.0, 1.04), (0, 0))
    L = SS(W, H, 1); flow(L.d, t, dots=False, down=0.0)
    fr.paste(L.done(), (0, 0), L.done())
    wing(d)
    # two parcels leave the leading edge together, repeat every 4 s
    tt = (t - 0.6) % 4.2
    if t > 0.6:
        for si, col, lab_off in ((3, CYAN, -90), (4, ORANGE, 90)):
            (x, y), done = parcel_pos(si, tt)
            d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=col, outline=WHITE, width=4)
        (xu, yu), du = parcel_pos(3, tt)
        (xl, yl), dl = parcel_pos(4, tt)
        if du and not dl:
            paste(fr, FIRST, xu - 40, yu - 140, 1.0)
            paste(fr, WAIT, min(xl, 760), yl + 50, 1.0)
    # equal-time claim crossed out
    a = ease_out(prog(t, starts[2] - ST[1], 0.3))
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H2, W / 2, 200, 1.0)
    clm = text_img("\"Equal transit time\"", 48, max_w=800, color=WHITE)
    paste(fr, clm, W / 2, 360, 1.0)
    if a > 0:
        d.line((W / 2 - 260, 400, W / 2 - 260 + 520 * a, 420), fill=RED, width=10)
    caps(fr, 1, t)

def s3(fr, t, d):
    fr.paste(push(LAB, t + 8, S[2], 1.02, 1.06), (0, 0))
    L = SS(W, H, 1); flow(L.d, t)
    fr.paste(L.done(), (0, 0), L.done())
    wing(d)
    appear(fr, LOWP, 300, 585, t, 1.2)
    appear(fr, HIGHP, 520, 1190, t, 1.8)
    a = ease_out(prog(t, starts[4] - ST[2], 0.6))
    if a > 0:
        arrow(d, CX0 + CH * 0.35, CY0 + 30, CX0 + CH * 0.35, CY0 - 30 - 240 * a, GREEN, 16, 46)
        paste(fr, LIFT, CX0 + CH * 0.35 + 130, CY0 - 250 * a - 30, a)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H3, W / 2, 190, 1.0)
    appear(fr, LAW_PILL, W / 2, 310, t, 0.2, pop=True)
    appear(fr, LAW_CARD, W / 2, 390, t, 0.4)
    appear(fr, LAW, W / 2, 410, t, 0.5)
    caps(fr, 2, t)

def s4(fr, t, d):
    fr.paste(push(LAB, t + 20, S[3], 1.0, 1.04), (0, 0))
    L = SS(W, H, 1); flow(L.d, t, down=1.6)
    fr.paste(L.done(), (0, 0), L.done())
    wing(d)
    a = ease_out(prog(t, 0.5, 0.6))
    if a > 0:
        for k in range(3):
            x = CX0 + CH + 30 + k * 70
            arrow(d, x, 1010, x + 20, 1010 + 170 * a + 10, ORANGE, 12, 36)
    appear(fr, ACT, 760, 1230, t, 0.6)
    b = ease_out(prog(t, starts[6] - ST[3], 0.6))
    if b > 0:
        arrow(d, CX0 + CH * 0.4, CY0 - 20, CX0 + CH * 0.4, CY0 - 40 - 220 * b, GREEN, 16, 46)
    appear(fr, REACT, W / 2, 500, t, starts[6] - ST[3] + 0.1)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H4, W / 2, 190, 1.0)
    appear(fr, N3, W / 2, 330, t, 0.2, pop=True)
    caps(fr, 3, t)

def s5(fr, t, d):
    fr.paste(push(LAB, t + 30, 8, 1.05, 1.08), (0, 0))
    fr.paste(VIG, (0, 0), VIG)
    appear(fr, QUIZ, W / 2, 290, t, 0.0, pop=True)
    appear(fr, Q, W / 2, 420, t, 0.4)
    for i, (c, tx, cx) in enumerate(((OPT_A, TA, 280), (OPT_B, TB, 800))):
        st = 2.4 + 0.4 * i
        appear(fr, c, cx, 820, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 862, ease_out(prog(t, st + 0.05, 0.3)))
    appear(fr, CMT, W / 2, 1080, t, 4.0, pop=True)
    appear(fr, FOL, W / 2, 1240, t, 5.4, pop=True)

SCENES = [(S[i], f) for i, f in enumerate((s1, s2, s3, s4, s5))]
VOICE = None
MUSIC_GAIN = 0.4
MUSIC = [(0.0, "hype"), (ST[1], "tension"), (ST[2], "curious"), (ST[3], "drive"), (ST[4], "uplift")]
SFX = [(0.0, "whoosh"), (0.4, "engine"), (2.2, "pop"), (ST[1] + 0.6, "swoosh"), (starts[2], "thud"), (ST[2] + 0.2, "pop"),
       (ST[2] + 1.2, "pop"), (ST[2] + 1.8, "pop"), (starts[4], "ding"), (ST[3] + 0.6, "whoosh"), (starts[6], "ding"),
       (ST[4] + 0.0, "pop"), (ST[4] + 1.0, "ticks"), (ST[4] + 2.4, "pop"), (ST[4] + 2.8, "pop"), (ST[4] + 5.4, "chime")]
for s_ in ST[1:-1]: SFX.append((s_ - 0.05, "swoosh"))
if __name__ == "__main__": print("total", round(ST[-1], 1), [round(x, 1) for x in S])
