"""17 Nov 2026 · Why aeroplanes fly — Bernoulli + Newton's third law (Plus One · Mechanical Properties of Fluids).
Myth: 'equal transit time' (air over the top and bottom must meet at the trailing edge) is false — air over the
top reaches the trailing edge FIRST (NASA Glenn 'Incorrect Lift Theory'). Lift = pressure difference
(faster flow on top → lower pressure, Bernoulli) + wing turns air downward (downwash) → air pushes wing up (Newton's 3rd).
A380 maximum take-off mass ≈ 575 t ("500 ടണ്ണിലേറെ").
Quiz: PYQ Plus One Model Exam 2020 ('Bernoulli's theorem is based on …' → conservation of energy): Bernoulli's principle is based on conservation of A) energy B) momentum → A.
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
    k = math.exp(-max(0, dist - 20) / (110 if upper else 170))
    pts, sp = [], []
    for x in np.linspace(-40, W + 40, 220):
        y = y0 + _surf(x, upper) * k * (1.6 if upper else 0.9)
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
LAW_CARD = card(960, LAW.height + 40, fill=(9, 14, 38, 210), outline=(255, 209, 102, 120))
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
PYQ = pill("PYQ · Plus One Model Exam 2020", 32, fg=WHITE, bg=(80, 60, 160))
Q = text_img("*Bernoulli's principle* ഏത് *conservation*-ൽ നിന്നാണ്?", 58, max_w=920, hl=YELLOW)
OPT_A = card(480, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(480, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) Energy", 44, max_w=460)
TB = text_img("B) Momentum", 44, max_w=460)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 56, max_w=900, hl=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 56, max_w=900, hl=YELLOW)

H_WHY = headline("WHY *FASTER* ON TOP?", hl=YELLOW, size=88)
H_CONT = headline("NARROW PATH = *FAST*", hl=CYAN, size=90)
H_CURVE = headline("CURVE NEEDS *LOW P*", hl=PINK, size=90)
CONT_PILL = pill("EQUATION OF CONTINUITY", 36, bg=CYAN)
CONT = text_img("*A₁v₁ = A₂v₂*   (Av = constant)", 54, max_w=920, hl=YELLOW)
A1L = boxed(text_img("*A₁* വലുത് → *v₁* കുറവ്", 36, max_w=500, hl=ORANGE), outline=(255, 159, 67, 200))
A2L = boxed(text_img("*A₂* ചെറുത് → *v₂* കൂടുതൽ", 36, max_w=520, hl=CYAN), outline=(79, 209, 255, 200))
HPL = boxed(text_img("*HIGH P*", 40, max_w=300, hl=ORANGE), outline=(255, 159, 67, 200))
LPL = boxed(text_img("*LOW P*", 40, max_w=300, hl=CYAN), outline=(79, 209, 255, 200))
FL = boxed(text_img("*net force* ↓", 36, max_w=400, hl=PINK), outline=(255, 107, 157, 200))
def sl_y(si, x):
    pts = SLS[si][0]
    return float(np.interp(x, pts[:, 0], pts[:, 1]))
def bracket(d, x, y1, y2, col):
    d.line((x, y1, x, y2), fill=col, width=6)
    d.line((x - 14, y1, x + 14, y1), fill=col, width=6); d.line((x - 14, y2, x + 14, y2), fill=col, width=6)


# ---------- JMK's Google Flow clips (17 Nov): frames pre-extracted at 30 fps into clips/<name>/ ----------
CLIPS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "clips")
CLIP_T0 = {"c1": 1.5, "c2": 1.0, "c8": 1.0, "c10": 3.0, "c11": 3.0, "c5": 0.0}   # clip time of frame 0001
_cache = {}
def clip_frame(name, ct):
    n = len(os.listdir(os.path.join(CLIPS, name)))
    i = min(max(int(round((ct - CLIP_T0[name]) * 30)), 0), n - 1) + 1
    key = (name, i)
    if key not in _cache:
        if len(_cache) > 40: _cache.clear()
        _cache[key] = Image.open(os.path.join(CLIPS, name, f"{i:04d}.jpg")).convert("RGB")
    return _cache[key]
def show_clip(fr, name, ct, z=1.0, c=(540, 960), dark=0.0):
    im = clip_frame(name, ct)
    if z > 1.001:
        cx, cy = c; w, h = W / z, H / z
        x0 = min(max(cx - cx / z, 0), W - w); y0 = min(max(cy - cy / z, 0), H - h)
        im = im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BICUBIC)
    if dark > 0: im = Image.blend(im, Image.new("RGB", (W, H), (0, 0, 0)), dark)
    fr.paste(im, (0, 0))
def zp(x, y, z, c):  # where point (x, y) of the clip lands after zoom z about c
    return c[0] + (x - c[0]) * z, c[1] + (y - c[1]) * z
def _shade():
    a = np.zeros((H, W), np.uint8)
    for y in range(H):
        v = 0
        if y < 560: v = 170 * (1 - y / 560)
        if y > 1250: v = max(v, 190 * min(1, (y - 1250) / 200))
        a[y, :] = int(v)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); im.putalpha(Image.fromarray(a)); return im
SHADE = _shade()
WEIGHT = text_img("*WEIGHT*", 56, max_w=320, hl=ORANGE)
RING_A = boxed(text_img("Thumb: *A* കുറഞ്ഞു", 38, max_w=520, hl=CYAN), outline=(79, 209, 255, 200))
JET_V = boxed(text_img("*v* കൂടി! വെള്ളം ദൂരെ", 38, max_w=520, hl=YELLOW), outline=(255, 209, 102, 200))
PROOF = boxed(text_img("ഈ *mist* = *low pressure*-ന്റെ തെളിവ്: air തണുത്ത് *vapour* മേഘമാകുന്നു", 34, max_w=900, hl=CYAN, lh=1.4), outline=(79, 209, 255, 200))
LOWP2 = boxed(text_img("*LOW P* · fast air", 38, max_w=500, hl=CYAN), outline=(79, 209, 255, 200))
HIGHP2 = boxed(text_img("*HIGH P*", 38, max_w=300, hl=ORANGE), outline=(255, 159, 67, 200))
TROUGH = boxed(text_img("Air താഴേക്ക് — മേഘം അമർന്നു", 34, max_w=600, hl=ORANGE), outline=(255, 159, 67, 200))

# ---------- narration (word by word, reading pace) ----------
LINES = [
    ("500 ടണ്ണിലേറെ ഭാരമുള്ള *Airbus A380* വായുവിൽ നിൽക്കുന്നത് എങ്ങനെ?", YELLOW),
    ("പഠിച്ച കഥ: മുകളിലെയും താഴത്തെയും *air* ഒരേ സമയം പിന്നിൽ എത്തണം.", WHITE),
    ("ഇത് *myth* ആണ്! മുകളിലെ *air* ആദ്യം എത്തും — അത്ര വേഗത്തിലാണ് ഒഴുക്ക്.", RED),
    ("അപ്പോൾ മുകളിൽ *velocity* എന്തുകൊണ്ട് കൂടുന്നു? രണ്ട് കാരണം.", YELLOW),
    ("Wing-ന്റെ വളഞ്ഞ മുകൾഭാഗവും ചെരിവും (*angle of attack*) മുകളിലെ *streamlines*-നെ അടുപ്പിക്കുന്നു.", CYAN),
    ("ഒഴുകാനുള്ള *area* കുറഞ്ഞാൽ *velocity* കൂടും — *equation of continuity*. Hose pipe അമർത്തുമ്പോൾ വെള്ളം ദൂരെ പോകുന്നത് പോലെ!", YELLOW),
    ("പിന്നെ, air വളഞ്ഞ wing-നൊപ്പം താഴേക്ക് തിരിയുന്നു. നേരെ പോയാൽ wing-നടുത്ത് *vacuum* വരും — ചുറ്റുമുള്ള air അതിനെ wing-ലേക്ക് അമർത്തുന്നു.", PINK),
    ("വളഞ്ഞ വഴിയിൽ പോകാൻ centre-ലേക്ക് ഒരു *centripetal force* വേണം. കല്ല് ചരടിൽ കെട്ടി കറക്കുമ്പോൾ ചരടിന്റെ *tension* പോലെ.", YELLOW),
    ("Air-ന് ചരടില്ല — തള്ളാൻ *pressure* മാത്രം! മുകളിൽ നിന്ന് *atmospheric pressure* താഴേക്ക് തള്ളുന്നു. *Net force* താഴേക്ക് കിട്ടാൻ wing-നടുത്തെ *pressure* അതിലും കുറവായിരിക്കണം.", ORANGE),
    ("മുന്നിലെ *high pressure* air-നെ ഈ *low pressure*-ലേക്ക് തള്ളുന്നു — അങ്ങനെ *speed* കൂടുന്നു!", CYAN),
    ("ചുരുക്കത്തിൽ: മുകളിൽ *velocity* കൂടുതൽ, *pressure* കുറവ്. താഴെ *pressure* കൂടുതൽ.", CYAN),
    ("ഈ *pressure difference* wing-നെ മുകളിലേക്ക് തള്ളുന്നു — ഇതാണ് *lift*.", GREEN),
    ("ഒപ്പം wing *air*-നെ താഴേക്ക് തള്ളുന്നു — *action*.", ORANGE),
    ("*Air* wing-നെ മുകളിലേക്ക് തള്ളുന്നു — *reaction*!", GREEN),
]
PACE = 0.42
def _dur(text, extra): return len(text.split()) * PACE + extra
S = [7.0,
     _dur(LINES[1][0], 0.6) + _dur(LINES[2][0], 1.6),
     _dur(LINES[3][0], 0.6) + _dur(LINES[4][0], 0.8) + _dur(LINES[5][0], 1.8),
     _dur(LINES[6][0], 0.8) + _dur(LINES[7][0], 1.8),
     _dur(LINES[8][0], 1.0) + _dur(LINES[9][0], 1.8),
     max(10.5, _dur(LINES[10][0], 1.0) + _dur(LINES[11][0], 2.2)),
     _dur(LINES[12][0], 0.8) + _dur(LINES[13][0], 2.0),
     8.5]
ST = [0.0]
for d_ in S: ST.append(ST[-1] + d_)
starts = [ST[0] + 0.5, ST[1] + 0.3, ST[1] + 0.3 + _dur(LINES[1][0], 0.6),
          ST[2] + 0.3, ST[2] + 0.3 + _dur(LINES[3][0], 0.6), ST[2] + 0.3 + _dur(LINES[3][0], 0.6) + _dur(LINES[4][0], 0.8),
          ST[3] + 0.3, ST[3] + 0.3 + _dur(LINES[6][0], 0.8),
          ST[4] + 0.3, ST[4] + 0.3 + _dur(LINES[8][0], 1.0),
          ST[5] + 0.4, ST[5] + 0.4 + _dur(LINES[10][0], 1.0),
          ST[6] + 0.3, ST[6] + 0.3 + _dur(LINES[12][0], 0.8)]
CAP = Captions([(txt, st, None, hl) for (txt, hl), st in zip(LINES, starts)], None, size=52, wpm_pace=PACE)
def caps(fr, s_idx, t, y=1340): CAP.draw(fr, ST[s_idx] + t, y)

# ---------- scenes ----------
def s1(fr, t, d):
    ct = 1.5 + min(t, 4.0) * 1.25                   # take-off plays, freezes at clip 6.5 s
    fz = ease_out(prog(t, 4.0, 0.6)); c = (470, 900); z = 1 + 0.05 * fz
    show_clip(fr, "c1", ct, z, c, dark=0.25 * fz)
    a = ease_out(prog(t, 4.3, 0.5))
    if a > 0:
        x, y = zp(470, 860, z, c)
        arrow(d, x, y, x, y - 340 * a - 10, GREEN, 16, 46)
        paste(fr, LIFT, x + 140, y - 330 * a - 20, a)
        x2, y2 = zp(470, 960, z, c)
        arrow(d, x2, y2, x2, y2 + 340 * a + 10, ORANGE, 16, 46)
        paste(fr, WEIGHT, x2 + 170, y2 + 280 * a - 30, a)
    fr.paste(SHADE, (0, 0), SHADE)
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
    ct = 1.2 + min(t, 4.6) * 0.5                    # JMK's clip: mist forms above the wing (slow motion), freeze 3.5 s
    fz = ease_out(prog(t, 4.6, 0.6)); c = (600, 900); z = 1 + 0.04 * fz
    show_clip(fr, "c8", ct, z, c, dark=0.15 * fz)
    appear(fr, LOWP2, 330, 610, t, 4.8)
    appear(fr, HIGHP2, 840, 1050, t, 5.3)
    a = ease_out(prog(t, starts[11] - ST[5], 0.6))
    if a > 0:
        x, y = zp(600, 930, z, c)
        arrow(d, x, y, x, y - 260 * a - 10, GREEN, 16, 46)
        paste(fr, LIFT, x + 150, y - 260 * a - 20, a)
    appear(fr, PROOF, W / 2, 1180, t, 2.2, out_at=starts[11] - ST[5] - 0.4)
    fr.paste(SHADE, (0, 0), SHADE)
    paste(fr, H3, W / 2, 190, 1.0)
    appear(fr, LAW_PILL, W / 2, 310, t, 0.2, pop=True)
    appear(fr, LAW_CARD, W / 2, 390, t, 0.4)
    appear(fr, LAW, W / 2, 410, t, 0.5)
    caps(fr, 5, t)

def s4(fr, t, d):
    t13 = starts[13] - ST[6]
    if t < t13:                                      # JMK's wind-tunnel clip: air turned DOWN behind the wing (action)
        ct = 3.0 + min(t, 3.4) * 1.2
        fz = ease_out(prog(t, 3.4, 0.5)); c = (540, 900); z = 1 + 0.04 * fz
        show_clip(fr, "c10", ct, z, c, dark=0.1 * fz)
        a = ease_out(prog(t, 1.2, 0.6))
        if a > 0:
            for k, x in enumerate((900, 980, 1040)):
                x1, y1 = zp(x, 1020 + k * 30, z, c)
                arrow(d, x1, y1, x1 + 10, y1 + 230 * a + 10, ORANGE, 12, 36)
        appear(fr, ACT, 340, 1170, t, 1.4)
    else:                                            # JMK's cloud clip: air pushed down, wing pushed up (reaction)
        u = t - t13
        ct = 3.5 + min(u, 2.9) * 1.2
        fz = ease_out(prog(u, 2.9, 0.5)); c = (540, 950); z = 1 + 0.04 * fz
        show_clip(fr, "c11", ct, z, c, dark=0.1 * fz)
        a = ease_out(prog(u, 0.3, 0.6))
        if a > 0:
            for x in (470, 610):
                x1, y1 = zp(x, 1080, z, c)
                arrow(d, x1, y1, x1, y1 + 200 * a + 10, ORANGE, 12, 36)
        b = ease_out(prog(u, 0.8, 0.6))
        if b > 0:
            x, y = zp(540, 900, z, c)
            arrow(d, x, y, x, y - 280 * b - 10, GREEN, 16, 46)
        appear(fr, REACT, W / 2, 470, t, t13 + 0.9)
        appear(fr, TROUGH, W / 2, 1180, t, t13 + 0.4)
    fr.paste(SHADE, (0, 0), SHADE)
    paste(fr, H4, W / 2, 190, 1.0)
    appear(fr, N3, W / 2, 330, t, 0.2, pop=True)
    caps(fr, 6, t)

def s5(fr, t, d):
    show_clip(fr, "c5", min(t, 9.8), dark=0.55)     # JMK's sunset-cruise clip behind the quiz
    fr.paste(VIG, (0, 0), VIG)
    appear(fr, QUIZ, W / 2, 290, t, 0.0, pop=True)
    appear(fr, PYQ, W / 2, 385, t, 0.3, pop=True)
    appear(fr, Q, W / 2, 480, t, 0.6)
    for i, (c, tx, cx) in enumerate(((OPT_A, TA, 280), (OPT_B, TB, 800))):
        st = 2.4 + 0.4 * i
        appear(fr, c, cx, 860, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 902, ease_out(prog(t, st + 0.05, 0.3)))
    appear(fr, CMT, W / 2, 1110, t, 4.0, pop=True)
    appear(fr, FOL, W / 2, 1270, t, 5.4, pop=True)

def s_cont(fr, t, d):
    t5 = starts[5] - ST[2]
    if t < t5:
        fr.paste(push(LAB, t + 4, S[2], 1.0, 1.04), (0, 0))
        L = SS(W, H, 1); flow(L.d, t)
        fr.paste(L.done(), (0, 0), L.done())
        wing(d)
        a = ease_out(prog(t, starts[4] - ST[2], 0.5))
        if a > 0:
            xa, xb = 110, CX0 + CH * 0.32
            y1, y2 = sl_y(1, xa), sl_y(3, xa)
            y3, y4 = sl_y(1, xb), sl_y(3, xb)
            L2 = SS(W, H, 1)
            L2.d.polygon([(xa, y1), (xb, y3), (xb, y4), (xa, y2)], fill=(255, 209, 102, int(60 * a)))
            fr.paste(L2.done(), (0, 0), L2.done())
            bracket(d, xa, y1, y2, ORANGE); bracket(d, xb, y3, y4, CYAN)
            appear(fr, A1L, 250, 470, t, starts[4] - ST[2] + 0.3)
            appear(fr, A2L, 770, 470, t, starts[4] - ST[2] + 0.8)
        fr.paste(VIG, (0, 0), VIG)
    else:                                            # JMK's hose clip: gentle flow → thumb → fast jet, freeze
        u = t - t5
        ct = 1.0 + min(u, 5.0) * 1.5
        fz = ease_out(prog(u, 5.0, 0.6)); c = (620, 1000); z = 1 + 0.05 * fz
        show_clip(fr, "c2", ct, z, c, dark=0.2 * fz)
        a = ease_out(prog(u, 5.2, 0.4))
        if a > 0:
            x, y = zp(608, 1000, z, c)
            d.ellipse((x - 62, y - 62, x + 62, y + 62), outline=CYAN, width=7)
            paste(fr, RING_A, x - 120, y - 210, a)
            b = ease_out(prog(u, 5.8, 0.5))
            if b > 0:
                x1, y1 = zp(680, 960, z, c); x2, y2 = zp(1030, 870, z, c)
                arrow(d, x1, y1 - 40, x1 + (x2 - x1) * b, y1 - 40 + (y2 - y1) * b, YELLOW, 14, 42)
                paste(fr, JET_V, 760, 1150, b)
        fr.paste(SHADE, (0, 0), SHADE)
    paste(fr, H_WHY if t < starts[4] - ST[2] else H_CONT, W / 2, 190, 1.0)
    appear(fr, CONT_PILL, W / 2, 300, t, t5, pop=True)
    appear(fr, CONT, W / 2, 375, t, t5 + 0.2, pop=True)
    caps(fr, 2, t)

H_TURN = headline("WHY DOES AIR *TURN?*", hl=PINK, size=88)
VAC = boxed(text_img("*vacuum?*", 40, max_w=300, hl=RED), outline=(235, 70, 80, 220))
CPL = text_img("*centripetal force*|a = v²/r", 36, max_w=330, hl=PINK, lh=1.4)
INSET = card(560, 250, fill=(9, 14, 38, 235), outline=(255, 107, 157, 160))
P0L = boxed(text_img("*atmospheric pressure* ↓", 38, max_w=600, hl=ORANGE), outline=(255, 159, 67, 200))
PLL = boxed(text_img("Wing-നടുത്ത് *pressure കുറവ്* ↑", 36, max_w=640, hl=CYAN), outline=(79, 209, 255, 200))
XP = CX0 + CH * 0.42

def _curve_base(fr, t, d, k):
    fr.paste(push(LAB, t + 12 + k, 16, 1.0, 1.04), (0, 0))
    L = SS(W, H, 1); flow(L.d, t, dots=False, alpha=150)
    L.d.line([tuple(p) for p in SLS[3][0]], fill=(255, 107, 157, 255), width=7)
    fr.paste(L.done(), (0, 0), L.done())
    wing(d)

def _rider(d, t, speed=0.8):
    x = (t * V0 * speed) % (CX0 + CH + 200) - 40
    y = sl_y(3, x)
    d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=PINK, outline=WHITE, width=4)
    return x, y

def s_curve(fr, t, d):
    _curve_base(fr, t, d, 0)
    ev = starts[7] - ST[3]
    x, y = _rider(d, t)
    # "what if it went straight?" — dashed straight path + gap next to the wing
    a = ease_out(prog(t, 2.6, 0.5)) * (1 - prog(t, ev - 0.3, 0.4))
    if a > 0.02:
        ya = sl_y(3, XP)
        L2 = SS(W, H, 1)
        poly = [(XP, ya)] + [(xx, sl_y(3, xx)) for xx in range(int(XP), W + 20, 20)][::-1] + []
        poly = [(XP, ya), (W, ya)] + [(xx, sl_y(3, xx)) for xx in range(W, int(XP), -20)]
        L2.d.polygon(poly, fill=(235, 70, 80, int(90 * a)))
        fr.paste(L2.done(), (0, 0), L2.done())
        for xx in range(int(XP), W, 44):
            d.line((xx, ya, xx + 24, ya), fill=WHITE, width=5)
        paste(fr, VAC, 900, ya + 30, a)
    if t > ev:
        if CX0 + CH * 0.2 < x < CX0 + CH * 0.95:
            arrow(d, x, y + 26, x, y + 110, PINK, 10, 30)
        b = ease_out(prog(t, ev + 0.2, 0.4))
        paste(fr, INSET, W / 2, 1020, b)
        if b > 0.5:
            cx, cy, r = 400, 1145, 80
            d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(120, 130, 190), width=3)
            an = t * 4
            sx, sy = cx + r * math.cos(an), cy + r * math.sin(an)
            d.line((cx, cy, sx, sy), fill=WHITE, width=4)
            arrow(d, sx, sy, cx + r * 0.35 * math.cos(an), cy + r * 0.35 * math.sin(an), PINK, 8, 24)
            d.ellipse((sx - 16, sy - 16, sx + 16, sy + 16), fill=ORANGE)
            d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=WHITE)
            paste(fr, CPL, 660, 1085, b)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H_TURN, W / 2, 190, 1.0)
    caps(fr, 3, t)

def s_press(fr, t, d):
    _curve_base(fr, t, d, 16)
    ev = starts[9] - ST[4]
    yp = sl_y(3, XP)
    if t < ev:
        d.rounded_rectangle((XP - 26, yp - 26, XP + 26, yp + 26), radius=8, fill=PINK, outline=WHITE, width=4)
        a = ease_out(prog(t, 3.0, 0.5))
        if a > 0:
            arrow(d, XP, yp - 40 - 190 * a, XP, yp - 34, ORANGE, 18, 46)
        appear(fr, P0L, XP, yp - 330, t, 3.0)
        b = ease_out(prog(t, 6.6, 0.5))
        if b > 0:
            arrow(d, XP, yp + 34 + 50 * b, XP, yp + 30, (30, 90, 200), 8, 22)
        appear(fr, PLL, W / 2, 1010, t, 6.6)
        appear(fr, FL, XP + 230, yp - 150, t, 5.2)
    else:
        _rider(d, t - ev, 1.1)
        appear(fr, LPL, XP, yp - 150, t, ev)
        appear(fr, HPL, 150, 960, t, ev)
        b = ease_out(prog(t, ev + 0.6, 0.6))
        if b > 0:
            arrow(d, 150, 930, 150 + (CX0 + CH * 0.3 - 150) * b, 930 - 230 * b, ORANGE, 12, 38)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H_CURVE, W / 2, 190, 1.0)
    caps(fr, 4, t)

SCENES = [(S[i], f) for i, f in enumerate((s1, s2, s_cont, s_curve, s_press, s3, s4, s5))]
VOICE = None
MUSIC_GAIN = 0.4
MUSIC = [(0.0, "hype"), (ST[1], "tension"), (ST[2], "curious"), (ST[3], "space"), (ST[4], "tension"), (ST[5], "curious"), (ST[6], "drive"), (ST[7], "uplift")]
SFX = [(0.0, "whoosh"), (0.4, "engine"), (4.0, "thud"), (4.3, "pop"), (ST[1] + 0.6, "swoosh"), (starts[2], "thud"),
       (starts[3], "boing"), (starts[4], "pop"), (starts[5], "ding"), (ST[3] + 2.6, "thud"), (starts[7], "pop"),
       (ST[4] + 3.0, "whoosh"), (ST[4] + 5.2, "pop"), (ST[4] + 6.6, "pop"), (starts[9], "whoosh"),
       (ST[5] + 0.2, "pop"), (ST[5] + 1.2, "pop"), (ST[5] + 1.8, "pop"), (starts[11], "ding"), (ST[6] + 0.6, "whoosh"), (starts[13], "ding"),
       (ST[7] + 0.0, "pop"), (ST[7] + 1.0, "ticks"), (ST[7] + 2.4, "pop"), (ST[7] + 2.8, "pop"), (ST[7] + 5.4, "chime")]
for s_ in ST[1:-1]: SFX.append((s_ - 0.05, "swoosh"))
if __name__ == "__main__": print("total", round(ST[-1], 1), [round(x, 1) for x in S])
