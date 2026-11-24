"""24 Nov 2026 · Why the roadside KSEB transformer hums — transformer, mutual induction, energy losses (Plus Two · Ch7 Alternating Current).
Syllabus topic (no strong news link in the last 72 h). Christmas-exam favourite: transformer losses / turns ratio 5 of 7 papers.
Why chain: 11000 V line → 230 V home = transformer. AC in primary → changing flux in the iron core → emf in secondary
(mutual induction, Faraday) → V_s/V_p = N_s/N_p. DC → flux does not change → no emf. 50 Hz AC → field direction reverses
100 times a second; the iron core shrinks a tiny bit whenever it is magnetised, whichever direction (magnetostriction)
→ core vibrates 100 times/s → 100 Hz hum. Vibration + heat = energy loss (copper I²R, eddy currents, hysteresis, flux leakage)
→ output power < input power → efficiency = output/input < 100 %; oil + fins carry the heat away.
Quiz: PYQ Plus Two Christmas Exam 2025 Q7 (True/False: efficiency of a transformer = output power / input power) → True.
No voice by default: captions word by word at reading pace."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import reelkit
from storykit import *
from captions import Captions
reelkit.SYMBOLS |= set("−ₚₛ")

HANDLE = "@jmk.space"
random.seed(24)
STEEL, STEEL_D, CU = (120, 135, 150), (80, 92, 108), (214, 130, 60)

LINES = [
    ("*11000 V* line-ലെ *current* നമ്മുടെ വീട്ടിലെത്തുമ്പോൾ *230 V*! ഇത് ചെയ്യുന്നത് ഈ *transformer* ആണ്.", YELLOW),
    ("*Primary coil*-ൽ *AC* ഒഴുകുമ്പോൾ iron *core*-ൽ *magnetic flux* ഉണ്ടാകുന്നു — അത് ഓരോ നിമിഷവും മാറുന്നു.", CYAN),
    ("മാറുന്ന *flux* *secondary coil*-ൽ *emf* ഉണ്ടാക്കുന്നു — ഇതാണ് *mutual induction*.", ORANGE),
    ("*DC* കൊടുത്താൽ *flux* മാറില്ല → *emf* ഇല്ല. അതുകൊണ്ട് *transformer* *AC*-ൽ മാത്രം.", PINK),
    ("*AC 50 Hz*: ഒരു സെക്കൻഡിൽ *100* തവണ *magnetic field*-ന്റെ ദിശ മാറുന്നു.", CYAN),
    ("*Magnetise* ആകുമ്പോഴെല്ലാം iron *core* വളരെ ചെറുതായി ചുരുങ്ങുന്നു — ദിശ ഏതായാലും! (*magnetostriction*)", ORANGE),
    ("അപ്പോൾ *core* സെക്കൻഡിൽ *100* തവണ വിറയ്ക്കുന്നു = *100 Hz sound* → അതാണ് ആ 'മ്മ്മ്മ്'!", YELLOW),
    ("ഈ വിറയലും ചൂടും *energy loss* ആണ്. *Output power* എപ്പോഴും *input power*-നേക്കാൾ അല്പം കുറവ്.", GREEN),
    ("ചൂട് കളയാനാണ് *oil*-ഉം *cooling fins*-ഉം. *High voltage* — അടുത്ത് പോകരുത്, തൊടരുത്!", RED),
]
PACE = 0.42
def _dur(i, extra): return len(LINES[i][0].split()) * PACE + extra

PLAN = [[0], [1, 2], [3], [4, 5, 6], [7, 8], []]
GAP = {0: 1.6, 1: 1.0, 2: 1.8, 3: 3.4, 4: 1.0, 5: 1.4, 6: 2.2, 7: 1.4, 8: 2.0}
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

TAG = pill("PLUS TWO PHYSICS · ALTERNATING CURRENT", 26, bg=CYAN)
BG_IMG = grad(W, H, [(0, (10, 14, 30)), (0.55, (22, 26, 56)), (1, (14, 18, 40))])

# ---------- the pole-mounted transformer ----------
def sound_arcs(d, cx, cy, t, k=1.0, side=1, col=(255, 209, 102)):
    for j in range(4):
        ph = ((t * 1.6 + j / 4) % 1.0)
        r = 60 + ph * 220
        a = int(230 * (1 - ph) * k)
        if a <= 5: continue
        box = (cx - r, cy - r, cx + r, cy + r)
        if side > 0: d.arc(box, -40, 40, fill=col + (a,) if len(col) == 3 else col, width=6)
        else: d.arc(box, 140, 220, fill=col + (a,) if len(col) == 3 else col, width=6)

def transformer(fr, d, cx, top, t, shake=1.0, s=1.0):
    jx = shake * 2.2 * math.sin(t * 2 * math.pi * 11)   # visual jitter (real vibration is microscopic)
    L = SS(W, 900); dd = L.d; ss = L.s
    oy = 0
    # poles + platform
    for px in (cx - 300 * s, cx + 300 * s):
        dd.rectangle(ss(px - 16, oy, px + 16, 900), fill=(150, 150, 160, 255))
    dd.rectangle(ss(cx - 340 * s, 560 * s, cx + 340 * s, 590 * s), fill=(110, 110, 120, 255))
    # overhead wires
    for k in range(3):
        dd.line(ss(0, 40 + k * 26, W, 52 + k * 26), fill=(40, 40, 50, 255), width=4)
    x0 = cx + jx
    # fins
    for k in range(-5, 6):
        fx = x0 + k * 40 * s
        dd.rounded_rectangle(ss(fx - 10 * s, 300 * s, fx + 10 * s, 550 * s), radius=6, fill=STEEL_D + (255,))
    # tank
    dd.rounded_rectangle(ss(x0 - 190 * s, 250 * s, x0 + 190 * s, 560 * s), radius=26, fill=STEEL + (255,))
    dd.rounded_rectangle(ss(x0 - 200 * s, 236 * s, x0 + 200 * s, 270 * s), radius=12, fill=STEEL_D + (255,))
    # bushings + leads to the line
    for k, bx in enumerate((-110, 0, 110)):
        bx = x0 + bx * s
        for j in range(4):
            dd.ellipse(ss(bx - 22 * s, (200 - j * 34) * s, bx + 22 * s, (226 - j * 34) * s), fill=(210, 140, 90, 255))
        dd.line(ss(bx, 100 * s, bx, 230 * s), fill=(200, 130, 80, 255), width=8)
        dd.line(ss(bx, 100 * s, bx - 40 + k * 40, 52 + k * 26), fill=(40, 40, 50, 255), width=4)
    # danger plate
    dd.rounded_rectangle(ss(x0 - 70 * s, 360 * s, x0 + 70 * s, 450 * s), radius=10, fill=(245, 210, 40, 255))
    dd.polygon([tuple(v * L.k for v in p) for p in [(x0, 372 * s), (x0 - 34 * s, 436 * s), (x0 + 34 * s, 436 * s)]], fill=(20, 20, 20, 255))
    dd.polygon([tuple(v * L.k for v in p) for p in [(x0 + 4, 385 * s), (x0 - 10, 410 * s), (x0 + 2, 410 * s), (x0 - 6, 430 * s), (x0 + 12, 402 * s), (x0, 402 * s)]], fill=(245, 210, 40, 255))
    # LT cable down to houses
    dd.line(ss(x0 + 190 * s, 480 * s, W, 640 * s), fill=(30, 30, 40, 255), width=7)
    img = L.done()
    fr.paste(img, (0, int(top)), img)

def house(d, x, ground, lit=1.0):
    d.polygon([(x - 90, ground - 140), (x, ground - 220), (x + 90, ground - 140)], fill=(170, 70, 60))
    d.rectangle((x - 75, ground - 140, x + 75, ground), fill=(225, 215, 190))
    c = (int(255 * lit + 60 * (1 - lit)), int(220 * lit + 60 * (1 - lit)), int(120 * lit + 70 * (1 - lit)))
    d.rectangle((x - 50, ground - 105, x - 10, ground - 65), fill=c)
    d.rectangle((x + 15, ground - 95, x + 50, ground), fill=(110, 70, 50))

HOOK = text_img("റോഡരികിലെ *KSEB transformer* എപ്പോഴും 'മ്മ്മ്മ്...' എന്ന് മൂളുന്നത് എന്തുകൊണ്ട്?", 62, max_w=980, hl=YELLOW)
H0 = headline("WHY THE *HUMMM?*", hl=YELLOW, size=96)
V11 = boxed(text_img("11000 V", 36, max_w=260, color=ORANGE), pad=12)
V230 = boxed(text_img("230 V", 36, max_w=220, color=GREEN), pad=12)
GROUND = 1270
def s0(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    d.rectangle((0, GROUND, W, GROUND + 50), fill=(30, 46, 40))
    transformer(fr, d, W / 2 - 60, 520, t, 1.0, 0.9)
    house(d, 930, GROUND, 0.6 + 0.4 * ease_out(prog(t, ls(0, 0) + 3, 0.6)))
    sound_arcs(d, W / 2 - 60, 900, t, 1.0, 1)
    sound_arcs(d, W / 2 - 60, 900, t, 1.0, -1)
    paste(fr, H0, W / 2, 140)
    paste(fr, HOOK, W / 2, 300, 1.0, 1 + 0.025 * math.sin(t * 4))
    paste(fr, TAG, W / 2, 248, ease_out(prog(t, 1.5, 0.4)))
    appear(fr, V11, 170, 600, t, ls(0, 0) + 0.6)
    appear(fr, V230, 930, 1000, t, ls(0, 0) + 2.6)
    caps(fr, 0, t)

# ---------- inside: core + coils ----------
CORE = (250, 520, 830, 1120)   # outer box of the core
CW = 90
def core_coils(fr, d, t, flux_k=1.0, ac=True, show_sec=1.0, shrink=0.0):
    x0, y0, x1, y1 = CORE
    sx = shrink * 10
    col = (110, 116, 140)
    d.rectangle((x0 + sx, y0 + sx, x1 - sx, y1 - sx), fill=col)
    d.rectangle((x0 + CW - sx, y0 + CW - sx, x1 - CW + sx, y1 - CW + sx), fill=BG_IMG.getpixel((540, 800)))
    for k in range(1, 6):   # lamination lines
        d.line((x0 + sx, y0 + k * 15, x1 - sx, y0 + k * 15), fill=(95, 100, 124), width=2)
    # primary (left, many turns) and secondary (right, few turns)
    for side, n, xc, a in ((0, 14, x0 + CW / 2, 1.0), (1, 6, x1 - CW / 2, show_sec)):
        if a <= 0: continue
        top, bot = y0 + CW + 20, y1 - CW - 20
        for k in range(n):
            yy = top + (bot - top) * (k + 0.5) / n
            d.rounded_rectangle((xc - 70, yy - 9, xc + 70, yy + 9), radius=9, fill=CU)
    # flux arrows around the core loop (direction follows sin)
    ph = math.sin(t * 2 * math.pi * 0.5) if ac else 1.0
    mag = abs(ph) * flux_k
    if mag > 0.08:
        dirn = 1 if ph > 0 else -1
        path = [(x0 + CW / 2, y1 - CW / 2), (x0 + CW / 2, y0 + CW / 2), (x1 - CW / 2, y0 + CW / 2), (x1 - CW / 2, y1 - CW / 2), (x0 + CW / 2, y1 - CW / 2)]
        if dirn < 0: path = path[::-1]
        c = (int(79 + 176 * (1 - mag)), 209, 255) if dirn > 0 else (255, 159, 67)
        for (ax, ay), (bx, by) in zip(path, path[1:]):
            if ax == bx and abs(ax - (x0 + CW / 2)) < 1: continue   # skip arrows hidden behind the primary coil
            if ax == bx and abs(ax - (x1 - CW / 2)) < 1: continue
            mx, my = (ax + bx) / 2, (ay + by) / 2
            ux, uy = (bx - ax), (by - ay); ln = math.hypot(ux, uy); ux, uy = ux / ln, uy / ln
            L2 = 70 * mag
            arrow(d, mx - ux * L2, my - uy * L2, mx + ux * L2, my + uy * L2, c, 9, 26)

NP = boxed(text_img("Primary  Nₚ", 32, max_w=300, color=ORANGE), pad=10)
NS = boxed(text_img("Secondary  Nₛ", 32, max_w=320, color=GREEN), pad=10)
FLX = boxed(text_img("changing *flux*", 32, max_w=320, hl=CYAN), pad=10)
H1 = headline("INSIDE THE *BOX*", hl=CYAN, size=90)
def s1(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    a2 = ease_out(prog(t, ls(2, 1), 0.5))
    core_coils(fr, d, t, 1.0, True, a2)
    # AC source wave on the left
    pts = [(60 + k * 2, 1200 + 40 * math.sin(k * 0.12 - t * 6)) for k in range(80)]
    d.line(pts, fill=ORANGE, width=5)
    d.line((60, 1200, 60, 760, CORE[0] + 20, 760), fill=CU, width=4); d.line((220, 1200, 220, 900, CORE[0] + 20, 900), fill=CU, width=4)
    paste(fr, NP, 290, 430)
    appear(fr, FLX, W / 2, 790, t, ls(1, 1) + 2.0)
    if a2 > 0:
        paste(fr, NS, 790, 430, a2)
        # bulb on the secondary glows with the induced emf
        glow = abs(math.sin(t * 2 * math.pi * 0.5)) * a2
        bx, by = 970, 830
        d.ellipse((bx - 40, by - 40, bx + 40, by + 40), fill=(int(120 + 135 * glow), int(110 + 110 * glow), int(60 + 40 * glow)))
        d.line((CORE[2] - 20, 760, bx - 30, by - 10), fill=CU, width=4); d.line((CORE[2] - 20, 900, bx - 30, by + 20), fill=CU, width=4)
    paste(fr, H1, W / 2, 170)
    caps(fr, 1, t)

# ---------- principle card + DC ----------
TP = pill("TRANSFORMER", 44, bg=YELLOW)
TPR = text_img("Works on the principle of *mutual induction*.", 46, max_w=880, hl=YELLOW, lh=1.45)
TEQ = text_img("Vₛ / Vₚ = Nₛ / Nₚ = Iₚ / Iₛ", 60, max_w=940, color=CYAN)
TSU = boxed(text_img("*Step-down*: Nₛ < Nₚ  →  Vₛ < Vₚ", 38, max_w=820, hl=GREEN), pad=14, outline=(91, 228, 155, 180))
TCARD = card(960, TPR.height + 140)
DCX = boxed(text_img("*DC* → flux constant → emf = 0", 38, max_w=820, hl=PINK), pad=14, outline=(255, 107, 157, 180))
def s2(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    appear(fr, TP, W / 2, 200, t, 0.1, pop=True)
    appear(fr, TCARD, W / 2, 300, t, 0.3)
    appear(fr, TPR, W / 2, 318, t, 0.4)
    appear(fr, TEQ, W / 2, 318 + TPR.height, t, 0.9, pop=True)
    appear(fr, TSU, W / 2, 560, t, 1.6)
    # mini core with DC: flux arrow steady, secondary bulb dark
    a = ease_out(prog(t, ls(3, 2), 0.5))
    if a > 0:
        cx, cy = W / 2, 900
        d.rectangle((cx - 230, cy - 150, cx + 230, cy + 150), fill=(110, 116, 140))
        d.rectangle((cx - 160, cy - 80, cx + 160, cy + 80), fill=BG_IMG.getpixel((540, 900)))
        arrow(d, cx - 60, cy - 115, cx + 60, cy - 115, (180, 190, 210), 8, 22)
        paste(fr, text_img("DC", 40, max_w=100, color=PINK), cx - 300, cy - 30)
        d.ellipse((cx + 270, cy - 30, cx + 330, cy + 30), fill=(70, 70, 80))
        x = ease_out(prog(t, ls(3, 2) + 1.5, 0.3))
        if x > 0:
            d.line((cx + 270, cy - 30, cx + 330, cy + 30), fill=RED, width=8); d.line((cx + 330, cy - 30, cx + 270, cy + 30), fill=RED, width=8)
    appear(fr, DCX, W / 2, 1110, t, ls(3, 2) + 2.0, pop=True)
    caps(fr, 2, t)

# ---------- the hum ----------
H3 = headline("THE *100 Hz* HUM", hl=YELLOW, size=90)
HZ = boxed(text_img("50 Hz → field reverses *100* times / s", 34, max_w=820, hl=CYAN), pad=12)
MS = boxed(text_img("N→S ആയാലും S→N ആയാലും *core* ചുരുങ്ങും", 34, max_w=820, hl=ORANGE), pad=12)
def s3(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    ph = math.sin(t * 2 * math.pi * 0.5)       # slowed-down AC for the eye
    shrink = abs(ph) * ease_out(prog(t, ls(5, 3), 0.5))
    core_coils(fr, d, t, 1.0, True, 1.0, shrink)
    # field direction meter
    paste(fr, HZ, W / 2, 400)
    a5 = ease_out(prog(t, ls(5, 3) + 1.0, 0.5))
    if a5 > 0:
        paste(fr, MS, W / 2, 470 - 0, a5)
    a6 = ease_out(prog(t, ls(6, 3), 0.5))
    if a6 > 0:
        sound_arcs(d, CORE[2] + 10, 820, t, a6, 1)
        sound_arcs(d, CORE[0] - 10, 820, t, a6, -1)
        # little waveform of the hum (|sin| -> twice the frequency)
        pts = [(170 + k * 3.7, 1220 - 50 * abs(math.sin(k * 0.09 - t * 4))) for k in range(200)]
        d.line(pts, fill=YELLOW, width=5)
    paste(fr, H3, W / 2, 180)
    caps(fr, 3, t)

# ---------- losses + safety ----------
H4 = headline("ENERGY *LOSSES*", hl=GREEN, size=90)
LOSS = [("Copper loss  I²R", "thick wires", ORANGE), ("Eddy currents", "laminated core", CYAN),
        ("Hysteresis", "soft iron core", PINK), ("Flux leakage", "coils close together", YELLOW)]
TILES = []
for a_, b_, c_ in LOSS:
    im = Image.new("RGBA", (460, 150), (0, 0, 0, 0))
    cd = card(460, 150, fill=c_ + (40,), outline=c_ + (200,)); im.paste(cd, (0, 0), cd)
    t1 = text_img(a_, 36, max_w=440, color=WHITE); im.paste(t1, (10, 8), t1)
    t2 = text_img(b_, 28, max_w=440, color=MUTED); im.paste(t2, (10, 72), t2)
    TILES.append(im)
EFF = boxed(text_img("Efficiency = *output power* / *input power*  < 100 %", 34, max_w=960, hl=GREEN), pad=14, outline=(91, 228, 155, 180))
def s4(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    for i, im in enumerate(TILES):
        appear(fr, im, 290 + (i % 2) * 500, 330 + (i // 2) * 180, t, 0.4 + i * 0.5, pop=True, out_at=ls(8, 4) - 0.2)
    appear(fr, EFF, W / 2, 720, t, ls(7, 4) + 3.0, pop=True, out_at=ls(8, 4) - 0.2)
    a8 = ease_out(prog(t, ls(8, 4) - 0.1, 0.5))
    if a8 > 0:
        d.rectangle((0, GROUND, W, GROUND + 50), fill=(30, 46, 40))
        transformer(fr, d, W / 2, 380, t, 0.6, 0.9)
        # heat shimmer from the fins
        for k in range(6):
            hx = W / 2 - 150 + k * 60
            yy = 640 - ((t * 60 + k * 37) % 220)
            d.arc((hx - 20, yy - 30, hx + 20, yy + 30), 270, 90, fill=(255, 120, 80), width=4)
        paste(fr, pill("HIGH VOLTAGE · KEEP AWAY", 34, fg=WHITE, bg=RED), W / 2, 1190, a8)
    paste(fr, H4, W / 2, 180)
    caps(fr, 4, t)

# ---------- quiz ----------
QUIZ = pill("QUIZ TIME", 46, fg=(9, 14, 38), bg=PINK)
PYQ = pill("PYQ · Plus Two Christmas Exam 2025", 32, fg=WHITE, bg=(80, 60, 160))
Q = text_img("*True* or *False*: Efficiency of a transformer = *output power* / *input power*", 56, max_w=920, hl=YELLOW)
OPT_A = card(460, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(460, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) True", 44, max_w=440)
TB = text_img("B) False", 44, max_w=440)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 58, max_w=900, hl=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 58, max_w=900, hl=YELLOW)
def s5(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    appear(fr, QUIZ, W / 2, 290, t, 0.1, pop=True)
    appear(fr, PYQ, W / 2, 390, t, 0.3)
    appear(fr, Q, W / 2, 500, t, 0.5)
    for i, (c, tx, cx) in enumerate(((OPT_A, TA, 290), (OPT_B, TB, 790))):
        st = 3.0 + i * 0.5
        pulse = 1 + 0.03 * math.sin((t - st) * 6 + i * 3) if t > st + 0.6 else 1
        appear(fr, c, cx, 870, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 910, ease_out(prog(t, st + 0.05, 0.3)), pulse)
    appear(fr, CMT, W / 2, 1110, t, 5.0, pop=True)
    appear(fr, FOL, W / 2, 1250, t, 6.5, pop=True)

SCENES = [(S[i], f) for i, f in enumerate((s0, s1, s2, s3, s4, s5))]
VOICE = None
MUSIC_GAIN = 0.4
MUSIC = [(0.0, "electric"), (ST[1], "curious"), (ST[2], "uplift"), (ST[3], "tension"), (ST[4], "drive"), (ST[5], "tension"), (ST[5] + 6.4, "uplift")]
MUSIC_SEED = 2411
SFX = [(0.0, "hum"), (0.0, "whoosh"), (3.8, "hum"), (starts[0] + 0.6, "zap"), (starts[0] + 2.6, "ding"),
       (ST[1] + 0.1, "swoosh"), (starts[1] + 2.0, "pop"), (starts[2], "zap"), (starts[2] + 0.4, "ding"),
       (ST[2] + 0.1, "pop"), (ST[2] + 0.9, "ding"), (ST[2] + 1.6, "pop"), (starts[3] + 1.5, "thud"), (starts[3] + 2.0, "pop"),
       (ST[3] + 0.1, "swoosh"), (starts[5], "pop"), (starts[6], "hum"), (starts[6] + 3.8, "hum"),
       (ST[4] + 0.4, "pop"), (ST[4] + 0.9, "pop"), (ST[4] + 1.4, "pop"), (ST[4] + 1.9, "pop"), (starts[7] + 3.0, "ding"),
       (starts[8], "zap"), (starts[8] + 0.2, "hum"),
       (ST[5] + 0.1, "pop"), (ST[5] + 3.0, "pop"), (ST[5] + 3.5, "pop"), (ST[5] + 4.2, "ticks"), (ST[5] + 6.5, "chime")]
if __name__ == "__main__": print("total", round(ST[-1], 1), [round(x, 1) for x in S])
