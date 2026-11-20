"""20 Nov 2026 · How a maglev train floats — Faraday's law + Lenz's law (Plus Two · Ch6 Electromagnetic Induction).
Facts (Wikipedia 'SCMaglev', checked 20 Nov 2026): Japan's SCMaglev (L0 series) set the world rail speed record of
603 km/h on 21 Apr 2015 (Yamanashi test line); it levitates about 10 cm; it runs on rubber wheels until about
150 km/h; the levitation/guidance coils in the guideway walls are passive (no power supply) — the moving
superconducting magnets induce the currents (electrodynamic suspension, EDS).
Why chain: magnet moves past coil → flux through the coil changes → induced emf (Faraday, ε = −N dφ/dt) → induced
current → by Lenz's law the current opposes the change → coil becomes a magnet that pushes the train's magnet away →
lift. emf ∝ dφ/dt, and dφ/dt ∝ speed → slow = weak lift → wheels until ~150 km/h.
Quiz: PYQ Plus Two Christmas 2019 Q2 ('Time rate of change of magnetic flux is ___' → induced emf).
No voice by default: captions word by word at reading pace."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import reelkit
from storykit import *
from captions import Captions
reelkit.SYMBOLS |= set("εφ−⋅↔")

HANDLE = "@jmk.space"
random.seed(20)
STEEL, STEEL_D = (150, 160, 182), (88, 96, 120)
COPPER, COPPER_L = (214, 128, 60), (255, 190, 120)
NRED, SBLUE = (232, 72, 80), (70, 120, 235)

LINES = [
    ("ജപ്പാനിലെ ഈ ട്രെയിൻ *track* തൊടാതെ ഏകദേശം *10 cm* ഉയർന്നാണ് ഓടുന്നത് — *603 km/h*, world record!", YELLOW),
    ("പക്ഷേ ഒരു *twist*: start ചെയ്യുമ്പോൾ ഇത് സാധാരണ *wheels*-ൽ ആണ് ഓടുന്നത്!", WHITE),
    ("ഏകദേശം *150 km/h* കഴിഞ്ഞാൽ മാത്രമേ ഇത് ഉയരൂ. എന്തുകൊണ്ട്?", ORANGE),
    ("ട്രെയിനിൽ ശക്തമായ *superconducting magnets*. Track-ൽ വെറും *coils* — ഉയർത്താനുള്ള ഇവയ്ക്ക് *power supply* ഇല്ല!", CYAN),
    ("*Magnet* മുകളിലൂടെ പായുമ്പോൾ *coil*-ലൂടെയുള്ള *magnetic flux* മാറുന്നു.", YELLOW),
    ("*Flux* മാറിയാൽ *induced emf* ഉണ്ടാകും — *Faraday's law*. അപ്പോൾ *coil*-ൽ *induced current* ഒഴുകുന്നു.", CYAN),
    ("ഈ *current* ഏത് ദിശയിൽ? *Lenz's law*: *flux*-ലെ മാറ്റത്തെ എതിർക്കുന്ന ദിശയിൽ.", YELLOW),
    ("അങ്ങനെ *coil* തന്നെ ഒരു *magnet* ആകുന്നു — *N*-ന് നേരെ *N*! *Magnet*-നെ മുകളിലേക്ക് തള്ളുന്നു. ട്രെയിൻ ഉയരുന്നു!", GREEN),
    ("ഇനി *speed*: *induced emf* = *flux* മാറുന്ന *rate*. പതുക്കെ പോയാൽ *flux* പതുക്കെ മാറും — *emf* ചെറുത്, തള്ളൽ കുറവ്.", ORANGE),
    ("വേഗം കൂടുമ്പോൾ *emf*, *current*, തള്ളൽ എല്ലാം കൂടും. അതുകൊണ്ടാണ് *150 km/h* വരെ *wheels*!", GREEN),
    ("ഇതെല്ലാം *Plus Two*-വിലെ *Electromagnetic Induction* chapter-ലെ രണ്ട് നിയമങ്ങൾ!", CYAN),
]
PACE = 0.42
def _dur(i, extra): return len(LINES[i][0].split()) * PACE + extra

# line start times are relative to their scene start; scenes = list of line indices
PLAN = [[0], [1, 2], [3, 4, 5], [6, 7], [8, 9], [10], []]
GAP = {0: 1.4, 1: 0.7, 2: 1.8, 3: 0.8, 4: 1.0, 5: 0.9, 6: 0.9, 7: 2.0, 8: 1.0, 9: 2.0, 10: 3.2}
S, ST, starts = [], [0.0], []
for k, idx in enumerate(PLAN):
    t = 0.3 if k else 0.6
    for i in idx:
        starts.append(ST[-1] + t); t += _dur(i, GAP[i])
    S.append(t if idx else 10.0)
    ST.append(ST[-1] + S[-1])
CAP = Captions([(txt, st, None, hl) for (txt, hl), st in zip(LINES, starts)], None, size=52, wpm_pace=PACE)
def caps(fr, s_idx, t, y=1335): CAP.draw(fr, ST[s_idx] + t, y)
def ls(i, sc): return starts[i] - ST[sc]          # line start, scene-relative

TAG = pill("PLUS TWO PHYSICS · ELECTROMAGNETIC INDUCTION", 26, bg=CYAN)
BG_IMG = grad(W, H, [(0, (6, 10, 30)), (0.6, (16, 22, 58)), (1, (30, 18, 60))])

# ---------- side view: guideway + train ----------
BEAM_Y = 1060
def pillars(d, scroll, y=BEAM_Y):
    d.rectangle((0, y, W, y + 46), fill=STEEL_D)
    d.line((0, y, W, y), fill=(200, 210, 235), width=4)
    off = scroll % 300
    for x in range(-300, W + 300, 300):
        xx = x - off
        d.polygon([(xx - 40, y + 46), (xx + 40, y + 46), (xx + 26, 1260), (xx - 26, 1260)], fill=(60, 66, 96))
    off2 = scroll % 120
    for x in range(-120, W + 120, 120):
        xx = x - off2
        d.rectangle((xx, y + 14, xx + 50, y + 22), fill=(130, 140, 170))

def train(fr, d, x0, ybot, wheels=1.0, glow=0.0, t=0.0):
    L = SS(980, 300); dd = L.d; s = L.s
    by = 260                                  # body bottom inside layer
    body = [(10, by), (10, by - 150), (560, by - 150), (700, by - 135), (840, by - 90), (950, by - 25), (960, by)]
    if glow > 0:
        for k in range(6):
            a = int(60 * glow * (1 - k / 6))
            dd.rounded_rectangle(s(20 - k * 4, by - 4 - k * 3, 940 + k * 4, by + 12 + k * 3), radius=12 * L.k, fill=(79, 209, 255, a))
    dd.polygon([tuple(v * L.k for v in p) for p in body], fill=(240, 244, 252, 255))
    dd.line(s(10, by - 52, 930, by - 52), fill=(30, 90, 190, 255), width=9 * L.k)
    dd.polygon([tuple(v * L.k for v in p) for p in [(600, by - 140), (700, by - 128), (790, by - 96), (640, by - 96)]], fill=(30, 50, 90, 255))
    for k in range(9):
        x = 40 + k * 58
        dd.rounded_rectangle(s(x, by - 125, x + 38, by - 92), radius=8 * L.k, fill=(40, 70, 120, 255))
    # magnet boxes under the body (red)
    for mx in (120, 480):
        dd.rectangle(s(mx, by - 6, mx + 120, by + 8), fill=NRED + (255,))
    if wheels > 0.02:
        r = 22 * wheels
        for wx in (90, 300, 640, 860):
            dd.ellipse(s(wx - r, by + 18 - r + 22 * (1 - wheels), wx + r, by + 18 + r + 22 * (1 - wheels)), fill=(30, 30, 40, 255))
            dd.ellipse(s(wx - r * 0.45, by + 18 - r * 0.45 + 22 * (1 - wheels), wx + r * 0.45, by + 18 + r * 0.45 + 22 * (1 - wheels)), fill=(170, 175, 190, 255))
    img = L.done()
    fr.paste(img, (int(x0), int(ybot - 260)), img)

def speed_lines(d, t, k=1.0):
    if k <= 0.05: return
    for i, yy in enumerate((860, 920, 990, 1030)):
        x0 = (900 - (t * 1600 + i * 300) % 1400)
        d.line((x0, yy, x0 + 160 * k, yy), fill=(150, 210, 255), width=4)

HOOK = text_img("ഈ ട്രെയിൻ *track* തൊടുന്നേയില്ല!", 74, max_w=1000, hl=CYAN)
H0 = headline("FLYING TRAIN? *603 KM/H*", hl=YELLOW, size=86)
GAPL = boxed(text_img("≈ 10 cm", 34, max_w=240, color=CYAN), pad=12)
SRC = source(["Wikipedia: SCMaglev, Japan"], 20)

def gauge(fr, d, cx, cy, v, vmax=600, label=True):
    r = 92
    d.arc((cx - r, cy - r, cx + r, cy + r), 150, 390, fill=(70, 80, 120), width=14)
    a1 = 150 + 240 * min(1, v / vmax)
    d.arc((cx - r, cy - r, cx + r, cy + r), 150, a1, fill=ORANGE if v < 150 else GREEN, width=14)
    tx = text_img(f"{int(v)}", 54, max_w=220, color=WHITE)
    paste(fr, tx, cx, cy - 46)
    if label: paste(fr, text_img("km/h", 28, max_w=160, color=MUTED), cx, cy + 14)

def s0(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    scroll = t * 1500
    speed_lines(d, t)
    pillars(d, scroll)
    bob = 3 * math.sin(t * 5)
    train(fr, d, 50, BEAM_Y - 80 + bob, wheels=0.0, glow=0.8 + 0.2 * math.sin(t * 9))
    paste(fr, GAPL, 900, BEAM_Y + 70)
    d.line((975, BEAM_Y - 80 + bob, 975, BEAM_Y), fill=CYAN, width=4)
    gauge(fr, d, 150, 760, min(603, 540 + t * 40))
    paste(fr, H0, W / 2, 150)
    paste(fr, HOOK, W / 2, 380, 1.0, 1 + 0.03 * math.sin(t * 4))
    paste(fr, TAG, W / 2, 290, ease_out(prog(t, 1.5, 0.4)))
    paste(fr, SRC, W / 2, 1275, ease_out(prog(t, 2.0, 0.4)) * 0.9)
    caps(fr, 0, t)

# ---------- scene 1: wheels until 150 km/h ----------
H1 = headline("WHY *WHEELS* FIRST?", hl=ORANGE, size=90)
LIFT = pill("LIFT!  150 km/h", 40, fg=(9, 14, 38), bg=GREEN)
S1V = lambda t: min(220.0, 6 + 16 * t)       # km/h, reaches 150 at t = 9 s
def s1(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    v = S1V(t)
    tl = (150 - 6) / 16.0
    up = ease_out(prog(t, tl, 0.9))
    pos = sum(S1V(k / 10) for k in range(int(t * 10))) / 10 * 4.0
    speed_lines(d, t, max(0, (v - 80) / 140))
    pillars(d, pos)
    train(fr, d, 50, BEAM_Y - 40 - 40 * up + 2 * math.sin(t * 20) * (1 - up), wheels=1 - up, glow=up)
    gauge(fr, d, W / 2, 620, v, vmax=300)
    if up > 0:
        paste(fr, LIFT, W / 2, 760, up, 0.7 + 0.3 * ease_back(prog(t, tl, 0.4)))
    paste(fr, H1, W / 2, 190)
    caps(fr, 1, t)

# ---------- close-up: magnet over coils ----------
COIL_Y = 1080
COIL_X = [140, 400, 660, 920]
NLAB = text_img("N", 46, max_w=80, color=WHITE)
SLAB = text_img("S", 46, max_w=80, color=WHITE)
def magnet(fr, d, cx, cy, w=230, h=130):
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy), radius=14, fill=SBLUE)
    d.rounded_rectangle((cx - w / 2, cy, cx + w / 2, cy + h / 2), radius=14, fill=NRED)
    d.line((cx - w / 2, cy, cx + w / 2, cy), fill=WHITE, width=3)
    paste(fr, SLAB, cx, cy - h / 2 + 2); paste(fr, NLAB, cx, cy - 6)

def coil(d, cx, cy, I=0.0, t=0.0, rw=105, rh=34):
    for k in range(3):
        o = k * 9
        d.ellipse((cx - rw, cy - rh + o, cx + rw, cy + rh + o), outline=COPPER if abs(I) < 0.15 else COPPER_L, width=7)
    if abs(I) > 0.08:
        n = 10
        for j in range(n):
            a = 2 * math.pi * j / n + t * 7 * (1 if I > 0 else -1) * min(1, abs(I))
            x, y = cx + rw * math.cos(a), cy + 9 + rh * math.sin(a)
            r = 5 + 6 * min(1, abs(I))
            d.ellipse((x - r, y - r, x + r, y + r), fill=YELLOW)

def flux(d, cx, top, bot, a=1.0, n=5):
    if a <= 0: return
    for j in range(n):
        x = cx + (j - (n - 1) / 2) * 42
        spread = (j - (n - 1) / 2) * 28
        pts = [(x + spread * (u ** 2), top + (bot - top) * u) for u in [k / 12 for k in range(13)]]
        for k in range(0, 12, 2):
            d.line((pts[k], pts[k + 1]), fill=(255, 140, 150, int(200 * a)) if False else (255, 140, 150), width=4)
        x2, y2 = pts[-1]
        arrow(d, pts[-2][0], pts[-2][1], x2, y2, (255, 140, 150), 4, 16)

def mag_x(t, v=260, x0=-120):
    return (x0 + t * v) % (W + 300) - 150

def coil_I(cx, mx, v):
    """induced current ~ dφ/dt: φ(x) gaussian around the magnet; positive while approaching."""
    dx = (cx - mx) / 120.0
    return v / 260.0 * 1.6 * dx * math.exp(-dx * dx)

H2 = headline("MAGNET + *COIL*", hl=CYAN, size=92)
PSL = boxed(text_img("*Power supply* ഇല്ല!", 36, max_w=420, hl=ORANGE), pad=14, outline=(255, 159, 67, 180))
FAR = boxed(text_img("ε = −N dφ/dt", 46, max_w=420, color=YELLOW), pad=16, outline=(255, 209, 102, 200))
ICUR = boxed(text_img("*induced current*", 34, max_w=360, hl=YELLOW), pad=12)
def closeup(fr, d, t, v=260, my=830, lenz=0.0, show_flux=1.0, show_I=1.0):
    mx = mag_x(t, v)
    near = min(COIL_X, key=lambda c: abs(c - mx))
    for cx in COIL_X:
        I = coil_I(cx, mx, v) * show_I
        if lenz > 0 and cx == near: I = max(abs(I), 0.9)
        coil(d, cx, COIL_Y, I, t)
        if lenz > 0 and cx == near and abs(cx - mx) < 200:
            d.rounded_rectangle((cx - 36, COIL_Y - 30, cx + 36, COIL_Y + 30), radius=12, fill=NRED + (int(255 * lenz),) if False else NRED)
            paste(fr, NLAB, cx, COIL_Y - 32, lenz)
    lift = 26 * lenz
    flux(d, mx, my + 70 - lift, COIL_Y - 40, show_flux)
    magnet(fr, d, mx, my - lift)
    if lenz > 0:
        arrow(d, mx, my - 80 - lift, mx, my - 80 - lift - 130 * lenz, GREEN, 14, 40)
    return mx

def s2(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    a_flux = ease_out(prog(t, ls(4, 2), 0.6))
    a_I = ease_out(prog(t, ls(5, 2) + 1.5, 0.6))
    mx = closeup(fr, d, t, show_flux=a_flux, show_I=a_I)
    appear(fr, PSL, W / 2, 1180, t, ls(3, 2) + 3.5, out_at=ls(4, 2))
    appear(fr, FAR, W / 2, 470, t, ls(5, 2) + 1.0, pop=True)
    if a_I > 0: paste(fr, ICUR, W / 2, 1185, a_I)
    paste(fr, H2, W / 2, 190)
    caps(fr, 2, t)

H3 = headline("LENZ'S *LAW*", hl=YELLOW, size=96)
REP = pill("N  ↔  N  :  REPEL", 40, fg=WHITE, bg=(200, 60, 80))
UP = boxed(text_img("*LIFT*", 40, max_w=200, hl=GREEN), pad=12)
def s3(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    lz = ease_out(prog(t, ls(7, 3), 0.8))
    mx = closeup(fr, d, t, lenz=lz)
    appear(fr, REP, W / 2, 470, t, ls(7, 3) + 1.5, pop=True)
    paste(fr, H3, W / 2, 190)
    caps(fr, 3, t)

# ---------- scene 4: slow vs fast ----------
H4 = headline("WHY *SPEED?*", hl=ORANGE, size=96)
SLOW = pill("SLOW · 30 km/h", 30, bg=ORANGE)
FAST = pill("FAST · 500 km/h", 30, bg=GREEN)
EMF = text_img("emf", 30, max_w=100, color=MUTED)
def lane(fr, d, t, y, v, lab, gain, rise):
    mx = (t * v) % (W + 260) - 130
    for cx in (180, 540, 900):
        I = coil_I(cx, mx, v) * 0.9
        coil(d, cx, y + 150, I, t, rw=80, rh=24)
    m_y = y + 40 - rise
    d.rounded_rectangle((mx - 80, m_y - 36, mx + 80, m_y), radius=10, fill=SBLUE)
    d.rounded_rectangle((mx - 80, m_y, mx + 80, m_y + 36), radius=10, fill=NRED)
    if rise < 10:
        for wx in (mx - 50, mx + 50):
            d.ellipse((wx - 14, m_y + 36, wx + 14, m_y + 64), fill=(30, 30, 40), outline=(170, 175, 190), width=3)
    else:
        arrow(d, mx, m_y - 46, mx, m_y - 46 - 70, GREEN, 10, 30)
    paste(fr, lab, 150 + lab.width / 2 - 60, y - 70)
    # emf meter
    paste(fr, EMF, 640, y - 66)
    d.rounded_rectangle((700, y - 58, 1020, y - 30), radius=12, outline=(110, 120, 170), width=3)
    val = min(1.0, abs(coil_I(540, mx, v)) * 0.9) * gain
    d.rounded_rectangle((704, y - 54, 704 + 312 * val, y - 34), radius=10, fill=lab.getpixel((lab.width // 2, 6))[:3])

EQS = boxed(text_img("ε ∝ dφ/dt   →   *speed* ↑  *emf* ↑", 42, max_w=900, hl=YELLOW), pad=18, outline=(255, 209, 102, 180))
def s4(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    lane(fr, d, t, 520, 70, SLOW, 0.25, 0)
    b = ease_out(prog(t, ls(9, 4) - 0.4, 0.6))
    lane(fr, d, t, 900, 900, FAST, 1.0, 40 * max(b, 0.3))
    appear(fr, EQS, W / 2, 1200, t, ls(8, 4) + 2.0, out_at=ls(9, 4) + 4.5)
    paste(fr, H4, W / 2, 190)
    caps(fr, 4, t)

# ---------- scene 5: law card ----------
FL_P = pill("FARADAY'S LAW", 40, bg=YELLOW)
FL = text_img("The magnitude of the *induced emf* equals the *time rate of change of magnetic flux*.", 46, max_w=880, hl=YELLOW, lh=1.45)
EQ = text_img("ε = −N dφ/dt", 64, max_w=700, color=CYAN)
LZ_P = pill("LENZ'S LAW", 40, bg=GREEN)
LZ = text_img("The *induced current* opposes the change in flux that produces it.", 46, max_w=880, hl=GREEN, lh=1.45)
CARD1 = card(960, FL.height + 140)
CARD2 = card(960, LZ.height + 40)
def s5(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    appear(fr, FL_P, W / 2, 230, t, 0.1, pop=True)
    appear(fr, CARD1, W / 2, 320, t, 0.3)
    appear(fr, FL, W / 2, 335, t, 0.5)
    appear(fr, EQ, W / 2, 335 + FL.height + 10, t, 1.5, pop=True)
    y2 = 320 + CARD1.height + 50
    appear(fr, LZ_P, W / 2, y2, t, 2.5, pop=True)
    appear(fr, CARD2, W / 2, y2 + 95, t, 2.7)
    appear(fr, LZ, W / 2, y2 + 110, t, 2.9)
    caps(fr, 5, t)

# ---------- scene 6: quiz ----------
QUIZ = pill("QUIZ TIME", 46, fg=(9, 14, 38), bg=PINK)
PYQ = pill("PYQ · Plus Two Christmas Exam 2019", 32, fg=WHITE, bg=(80, 60, 160))
Q = text_img("Time rate of change of *magnetic flux* is ______", 60, max_w=920, hl=YELLOW)
OPT_A = card(460, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(460, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) Induced emf", 44, max_w=440)
TB = text_img("B) Induced current", 44, max_w=440)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 58, max_w=900, hl=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 58, max_w=900, hl=YELLOW)
def s6(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    appear(fr, QUIZ, W / 2, 290, t, 0.1, pop=True)
    appear(fr, PYQ, W / 2, 390, t, 0.3)
    appear(fr, Q, W / 2, 500, t, 0.5)
    for i, (c, tx, cx) in enumerate(((OPT_A, TA, 290), (OPT_B, TB, 790))):
        st = 3.0 + i * 0.5
        pulse = 1 + 0.03 * math.sin((t - st) * 6 + i * 3) if t > st + 0.6 else 1
        appear(fr, c, cx, 820, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 860, ease_out(prog(t, st + 0.05, 0.3)), pulse)
    appear(fr, CMT, W / 2, 1080, t, 5.0, pop=True)
    appear(fr, FOL, W / 2, 1230, t, 6.5, pop=True)

SCENES = [(S[i], f) for i, f in enumerate((s0, s1, s2, s3, s4, s5, s6))]
VOICE = None
MUSIC_GAIN = 0.4
MUSIC = [(0.0, "hype"), (ST[1], "tension"), (ST[2], "electric"), (ST[3], "curious"), (ST[4], "drive"), (ST[5], "uplift"), (ST[6], "tension"), (ST[6] + 6.4, "uplift")]
MUSIC_SEED = 2011
SFX = [(0.0, "whoosh"), (0.2, "zap"), (ST[1] + 0.1, "swoosh"), (ST[1] + (150 - 6) / 16.0, "whoosh"), (ST[1] + (150 - 6) / 16.0 + 0.1, "ding"),
       (ST[2] + 0.1, "swoosh"), (starts[4] + 0.2, "pop"), (starts[5] + 1.0, "pop"), (starts[5] + 1.5, "zap"),
       (ST[3] + 0.1, "swoosh"), (starts[7], "boing"), (starts[7] + 1.5, "pop"),
       (ST[4] + 0.1, "swoosh"), (starts[8] + 2.0, "pop"), (starts[9] - 0.4, "whoosh"),
       (ST[5] + 0.1, "pop"), (ST[5] + 1.5, "ding"), (ST[5] + 2.5, "pop"),
       (ST[6] + 0.1, "pop"), (ST[6] + 3.0, "pop"), (ST[6] + 3.5, "pop"), (ST[6] + 4.2, "ticks"), (ST[6] + 6.5, "chime")]
if __name__ == "__main__": print("total", round(ST[-1], 1), [round(x, 1) for x in S])
