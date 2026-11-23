"""23 Nov 2026 · Why a raindrop from 2 km doesn't hit like a bullet — terminal velocity (Plus One · Ch9 Mechanical Properties of Fluids).
News hook: Kerala heavy rain / thunderstorm yellow alerts this week (IMD, till 26 Nov; newkerala.com).
Why chain: no air → v² = u² + 2as → v = √(2gh) ≈ 198 m/s (~700 km/h) from 2 km. Real drops ≤ ~9 m/s (big drops, Gunn & Kinzer 1949).
Air is a fluid → viscous force opposes motion. Faster drop → air layers around it must slide faster (bigger velocity gradient)
→ bigger viscous force (Stokes' law F = 6πηav for small spheres). Weight constant; drag + buoyancy grow until they equal weight →
net force 0 → a = 0 (F = ma) → constant velocity = terminal velocity, vₜ = 2a²(ρ − σ)g/9η → vₜ ∝ a² (big drops faster).
Note: real raindrops (mm size) are beyond Stokes' regime; the reel says Stokes' law is for small drops.
Quiz: PYQ Plus One Model Exam 2024 (Ch9: rain drops reach a constant velocity → name → terminal velocity).
No voice by default: captions word by word at reading pace."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import reelkit
from storykit import *
from captions import Captions
reelkit.SYMBOLS |= set("ₜη−")

HANDLE = "@jmk.space"
random.seed(23)
DROP, DROP_L = (90, 170, 255), (190, 225, 255)

LINES = [
    ("ഏകദേശം *2 km* ഉയരത്തിലെ മേഘത്തിൽ നിന്നാണ് മഴത്തുള്ളി വീഴുന്നത്!", YELLOW),
    ("*Air* ഇല്ലായിരുന്നെങ്കിൽ *v² = u² + 2as* പ്രകാരം *v ≈ 200 m/s* — ഏകദേശം *700 km/h*! വെടിയുണ്ട പോലെ!", ORANGE),
    ("പക്ഷേ ശരിക്കും വലിയ തുള്ളി പോലും *9 m/s* (*32 km/h*) വരെയേ എത്തൂ. എന്തുകൊണ്ട്?", CYAN),
    ("*Air* ഒരു *fluid* ആണ്. വീഴുന്ന തുള്ളിയെ *air* എതിർക്കുന്നു — *viscous force* (*drag*).", CYAN),
    ("*Speed* കൂടുമ്പോൾ തുള്ളിക്ക് ചുറ്റുമുള്ള *air layers* കൂടുതൽ വേഗത്തിൽ തെന്നിമാറണം — അതുകൊണ്ട് *viscous force* കൂടുന്നു.", YELLOW),
    ("താഴേക്ക് *weight* (*mg*) മാറുന്നില്ല. മുകളിലേക്ക് *drag* + *buoyancy* കൂടിക്കൂടി വരുന്നു.", ORANGE),
    ("രണ്ടും തുല്യമാകുമ്പോൾ *net force = 0* → *acceleration = 0* (*F = ma*). പിന്നെ *velocity* മാറില്ല!", GREEN),
    ("ഈ *constant* വേഗമാണ് *terminal velocity*. വലിയ തുള്ളി കൂടുതൽ വേഗത്തിൽ, ചെറിയ ചാറ്റൽമഴത്തുള്ളി പതുക്കെ.", CYAN),
]
PACE = 0.42
def _dur(i, extra): return len(LINES[i][0].split()) * PACE + extra

PLAN = [[0], [1, 2], [3, 4], [5, 6], [7], []]
GAP = {0: 1.6, 1: 1.2, 2: 1.6, 3: 0.9, 4: 1.6, 5: 0.9, 6: 2.0, 7: 3.4}
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

TAG = pill("PLUS ONE PHYSICS · MECHANICAL PROPERTIES OF FLUIDS", 24, bg=CYAN)
BG_IMG = grad(W, H, [(0, (10, 14, 30)), (0.55, (20, 30, 58)), (1, (14, 22, 40))])

# ---------- rain + cloud ----------
RAIN = [(random.uniform(0, W), random.uniform(0, H), random.uniform(28, 60), random.uniform(900, 1400)) for _ in range(90)]
def rain(d, t, k=1.0, y0=0, y1=1300, col=(150, 180, 230)):
    if k <= 0: return
    for x, y, ln, sp in RAIN:
        yy = y0 + (y + t * sp) % (y1 - y0)
        d.line((x, yy, x - 4, yy + ln * k), fill=col, width=3)

def cloud(d, cx, cy, s=1.0, col=(120, 130, 160)):
    for dx, dy, r in ((-210, 20, 95), (-90, -35, 130), (60, -50, 140), (200, 5, 105), (0, 40, 120), (-150, 50, 90), (150, 55, 95)):
        d.ellipse((cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s), fill=col)

def drop(fr, cx, cy, r=26, glow=0.0):
    L = SS(int(r * 4), int(r * 5)); dd = L.d; s = L.s
    c = r * 2
    if glow > 0:
        for k in range(5):
            a = int(50 * glow * (1 - k / 5)); rr = r + 6 + k * 5
            dd.ellipse(s(c - rr, c * 1.25 - rr, c + rr, c * 1.25 + rr), fill=(120, 200, 255, a))
    dd.ellipse(s(c - r, c * 1.25 - r, c + r, c * 1.25 + r), fill=DROP + (255,))
    dd.polygon([tuple(v * L.k for v in p) for p in [(c - r * 0.72, c * 1.25 - r * 0.7), (c, c * 1.25 - r * 2.0), (c + r * 0.72, c * 1.25 - r * 0.7)]], fill=DROP + (255,))
    dd.ellipse(s(c - r * 0.5, c * 1.25 - r * 0.55, c - r * 0.1, c * 1.25 - r * 0.15), fill=DROP_L + (255,))
    img = L.done()
    fr.paste(img, (int(cx - img.width / 2), int(cy - c * 1.25)), img)

def person(d, x, ground):
    col = (40, 50, 90)
    d.ellipse((x - 18, ground - 150, x + 18, ground - 114), fill=(150, 100, 70))
    d.line((x, ground - 114, x, ground - 50), fill=col, width=16)
    for dx in (-14, 14): d.line((x, ground - 52, x + dx, ground), fill=col, width=12)
    d.line((x, ground - 100, x + 30, ground - 150), fill=col, width=9)
    d.line((x + 30, ground - 150, x + 30, ground - 205), fill=(200, 200, 210), width=5)
    d.pieslice((x - 70, ground - 255, x + 130, ground - 155), 180, 360, fill=(230, 70, 90))

HOOK = text_img("2 km മുകളിൽ നിന്ന് വീണിട്ടും മഴത്തുള്ളി *വെടിയുണ്ട* പോലെ കൊള്ളാത്തത് എന്തുകൊണ്ട്?", 64, max_w=980, hl=ORANGE)
H0 = headline("RAIN = *BULLET?*", hl=CYAN, size=96)
KM2 = boxed(text_img("≈ 2 km", 36, max_w=220, color=YELLOW), pad=12)
SRC = source(["IMD: Kerala rain alert till 26 Nov"], 20)
GROUND = 1240
def s0(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    rain(d, t, 1.0, 640, GROUND)
    cloud(d, W / 2, 690, 1.1)
    d.rectangle((0, GROUND, W, GROUND + 40), fill=(30, 50, 40))
    person(d, 760, GROUND)
    # highlighted drop falling cloud -> ground, repeats
    p = ((t + 0.9) % 2.2) / 2.2
    drop(fr, 470, 790 + (GROUND - 840) * p * p, 30, glow=0.8)
    d.line((120, 760, 120, GROUND), fill=YELLOW, width=4)
    for yy in (760, GROUND): d.line((100, yy, 140, yy), fill=YELLOW, width=4)
    paste(fr, KM2, 150, 980)
    paste(fr, H0, W / 2, 140)
    paste(fr, HOOK, W / 2, 300, 1.0, 1 + 0.025 * math.sin(t * 4))
    paste(fr, TAG, W / 2, 248, ease_out(prog(t, 1.5, 0.4)))
    paste(fr, SRC, W / 2, 1290, ease_out(prog(t, 2.0, 0.4)) * 0.9)
    caps(fr, 0, t)

# ---------- scene 1: no air vs air ----------
def gauge(fr, d, cx, cy, v, vmax, col):
    r = 100
    d.arc((cx - r, cy - r, cx + r, cy + r), 150, 390, fill=(70, 80, 120), width=16)
    d.arc((cx - r, cy - r, cx + r, cy + r), 150, 150 + 240 * min(1, v / vmax), fill=col, width=16)
    paste(fr, text_img(f"{int(v)}", 56, max_w=240, color=WHITE), cx, cy - 48)
    paste(fr, text_img("km/h", 28, max_w=160, color=MUTED), cx, cy + 14)

H1 = headline("NO AIR *vs* AIR", hl=ORANGE, size=92)
VAC = pill("AIR ഇല്ലെങ്കിൽ", 32, bg=ORANGE)
AIR = pill("ശരിക്കും (AIR)", 32, bg=CYAN)
EQ1 = boxed(text_img("v = √(2gh) = √(2 × 9.8 × 2000) ≈ *198 m/s*", 38, max_w=900, hl=ORANGE), pad=16, outline=(255, 159, 67, 180))
def s1(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    paste(fr, H1, W / 2, 170)
    a2 = ease_out(prog(t, ls(2, 1), 0.5))
    # left lane: vacuum, accelerating
    d.line((W / 4, 560, W / 4, 1220), fill=(60, 70, 110), width=2)
    pv = (t % 1.6) / 1.6
    yv = 560 + 640 * pv * pv
    for k in range(4):
        d.line((W / 4 - 30 + k * 20, yv - 40 - 90 * pv, W / 4 - 30 + k * 20, yv - 40), fill=(255, 190, 120), width=3)
    drop(fr, W / 4, yv, 24, glow=0.6)
    paste(fr, VAC, W / 4, 300)
    gauge(fr, d, W / 4, 470, min(713, t * 260), 720, ORANGE)
    # right lane: real, steady ~32 km/h
    if a2 > 0:
        d.line((3 * W / 4, 560, 3 * W / 4, 1220), fill=(60, 70, 110), width=2)
        pa = ((t * 0.55) % 1.0)
        drop(fr, 3 * W / 4, 560 + 640 * pa, 24, glow=0.3)
        paste(fr, AIR, 3 * W / 4, 300, a2)
        gauge(fr, d, 3 * W / 4, 470, min(32, (t - ls(2, 1)) * 40), 720, CYAN)
    appear(fr, EQ1, W / 2, 1210, t, ls(1, 1) + 1.5, out_at=ls(2, 1) + 1.0)
    caps(fr, 1, t)

# ---------- close-up: drop + air streamlines ----------
CX, CY, R = W / 2, 720, 95
def big_drop(fr, d, cy=CY):
    d.ellipse((CX - R, cy - R, CX + R, cy + R), fill=DROP)
    d.ellipse((CX - R * 0.55, cy - R * 0.6, CX - R * 0.15, cy - R * 0.2), fill=DROP_L)

def streams(d, t, v, cy=CY, n=8):
    """air flowing upward past the drop (drop's frame); dash speed ~ v"""
    for j in range(n):
        x0 = CX + (j - (n - 1) / 2) * 62
        off = x0 - CX
        for k in range(14):
            y = (cy + 330) - ((k * 60 + t * 120 * (0.3 + v)) % 840)
            dy = (y - cy) / (R * 1.6)
            push_ = 0 if abs(off) > R * 1.9 else (R * 1.15 - abs(off) * 0.4) * math.exp(-dy * dy) * (1 if off >= 0 else -1)
            x = x0 + push_
            d.line((x, y, x, y - 26), fill=(170, 200, 240), width=4)

H2 = headline("AIR *FIGHTS BACK*", hl=CYAN, size=88)
DRAG = boxed(text_img("*viscous force* (drag)", 34, max_w=420, hl=GREEN), pad=12)
STK = boxed(text_img("*Stokes' law*  F = 6πηav", 40, max_w=600, hl=YELLOW), pad=14, outline=(255, 209, 102, 180))
STK2 = text_img("(ചെറിയ തുള്ളികൾക്ക്)  F ∝ v", 32, max_w=600, color=MUTED)
SPD = text_img("speed", 30, max_w=120, color=MUTED)
def s2(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    v = min(1.0, t / (S[2] * 0.85))
    streams(d, t, v)
    big_drop(fr, d)
    la = ease_out(prog(t, ls(3, 2) + 2.0, 0.5))
    if la > 0:
        L = 60 + 170 * v
        arrow(d, CX, CY - R - 10, CX, CY - R - 10 - L * la, GREEN, 14, 38)
        paste(fr, DRAG, CX + 250, CY - R - 120, la)
    # speed bar
    paste(fr, SPD, 110, 470)
    d.rounded_rectangle((90, 520, 130, 1000), radius=16, outline=(110, 120, 170), width=3)
    d.rounded_rectangle((96, 994 - 468 * v, 124, 994), radius=12, fill=ORANGE)
    appear(fr, STK, W / 2, 1110, t, ls(4, 2) + 3.0, pop=True)
    appear(fr, STK2, W / 2, 1200, t, ls(4, 2) + 3.4)
    paste(fr, H2, W / 2, 190)
    caps(fr, 2, t)

# ---------- scene 3: balance + v-t graph ----------
H3 = headline("FORCES *BALANCE*", hl=GREEN, size=88)
MG = boxed(text_img("*weight* mg", 40, max_w=360, hl=ORANGE), pad=10)
DR = boxed(text_img("*drag*", 40, max_w=200, hl=GREEN), pad=10)
BU = boxed(text_img("*buoyancy*", 40, max_w=300, hl=CYAN), pad=10)
NET = pill("NET FORCE = 0  →  a = 0", 36, fg=(9, 14, 38), bg=GREEN)
VT = text_img("vₜ", 40, max_w=80, color=GREEN)
AXV = text_img("v", 32, max_w=60, color=MUTED); AXT = text_img("t", 32, max_w=60, color=MUTED)
DCY = 600; DR_ = 70
def vfun(x): return 1 - math.exp(-4 * x)
def s3(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    T_eq = ls(6, 3)
    g = min(1.0, t / max(0.1, T_eq))               # 0 -> 1 as drag grows to match weight
    dragL = 200 * vfun(g * 1.2) / vfun(1.2)
    d.ellipse((CX - DR_, DCY - DR_, CX + DR_, DCY + DR_), fill=DROP)
    arrow(d, CX, DCY + DR_ + 6, CX, DCY + DR_ + 6 + 220, ORANGE, 14, 38)            # weight
    paste(fr, MG, CX + 170, DCY + DR_ + 120)
    arrow(d, CX - 30, DCY - DR_ - 6, CX - 30, DCY - DR_ - 6 - 20 - dragL, GREEN, 14, 38)  # drag
    paste(fr, DR, CX - 170, DCY - DR_ - 120)
    arrow(d, CX + 30, DCY - DR_ - 6, CX + 30, DCY - DR_ - 6 - 24, CYAN, 10, 22)   # buoyancy (small)
    paste(fr, BU, CX + 170, DCY - DR_ - 70)
    # v-t graph
    gx0, gy0, gw, gh = 170, 1250, 760, 300
    ga = ease_out(prog(t, 0.6, 0.5))
    if ga > 0:
        d.line((gx0, gy0, gx0 + gw, gy0), fill=(150, 160, 210), width=4)
        d.line((gx0, gy0, gx0, gy0 - gh - 20), fill=(150, 160, 210), width=4)
        paste(fr, AXV, gx0 - 30, gy0 - gh - 40); paste(fr, AXT, gx0 + gw + 20, gy0 - 30)
        n = int(60 * g) + 1
        pts = [(gx0 + gw * k / 60, gy0 - gh * 0.9 * vfun(k / 60 * 1.2) / vfun(1.2)) for k in range(n)]
        if len(pts) > 1: d.line(pts, fill=CYAN, width=7)
        if g >= 1:
            for x in range(gx0, gx0 + gw, 30):
                d.line((x, gy0 - gh * 0.9, x + 16, gy0 - gh * 0.9), fill=GREEN, width=3)
            paste(fr, VT, gx0 + gw + 30, gy0 - gh * 0.9 - 30)
    appear(fr, NET, W / 2, 870, t, T_eq + 0.6, pop=True)
    paste(fr, H3, W / 2, 190)
    caps(fr, 3, t, y=1350)

# ---------- scene 4: definition card + big vs small ----------
TV_P = pill("TERMINAL VELOCITY", 42, bg=YELLOW)
TV = text_img("The constant maximum *velocity* of a body falling through a *viscous fluid*.", 46, max_w=880, hl=YELLOW, lh=1.45)
EQ = text_img("vₜ = 2a²(ρ − σ)g / 9η", 62, max_w=900, color=CYAN)
PROP = boxed(text_img("vₜ ∝ a²  →  വലിയ തുള്ളി *വേഗം*", 38, max_w=800, hl=GREEN), pad=14, outline=(91, 228, 155, 180))
CARD = card(960, TV.height + 150)
def s4(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    appear(fr, TV_P, W / 2, 210, t, 0.1, pop=True)
    appear(fr, CARD, W / 2, 310, t, 0.3)
    appear(fr, TV, W / 2, 325, t, 0.5)
    appear(fr, EQ, W / 2, 325 + TV.height + 10, t, 1.6, pop=True)
    a = ease_out(prog(t, 3.0, 0.5))
    if a > 0:
        tt = t - 3.0
        for x, r, sp in ((360, 30, 0.75), (720, 12, 0.32)):
            y = 820 + (tt * sp * 380) % 330
            drop(fr, x, y, r, glow=0.4)
    appear(fr, PROP, W / 2, 1185, t, 4.0, pop=True)
    caps(fr, 4, t, y=1335)

# ---------- scene 5: quiz ----------
QUIZ = pill("QUIZ TIME", 46, fg=(9, 14, 38), bg=PINK)
PYQ = pill("PYQ · Plus One Model Exam 2024", 32, fg=WHITE, bg=(80, 60, 160))
Q = text_img("മഴത്തുള്ളി ഒടുവിൽ ഒരു *constant velocity*-യിൽ വീഴുന്നു. ആ *velocity*-യുടെ പേര്?", 58, max_w=920, hl=YELLOW)
OPT_A = card(460, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(460, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) Terminal velocity", 40, max_w=440)
TB = text_img("B) Escape velocity", 40, max_w=440)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 58, max_w=900, hl=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 58, max_w=900, hl=YELLOW)
def s5(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    rain(d, t, 0.5, 0, 1500, col=(60, 80, 120))
    appear(fr, QUIZ, W / 2, 290, t, 0.1, pop=True)
    appear(fr, PYQ, W / 2, 390, t, 0.3)
    appear(fr, Q, W / 2, 500, t, 0.5)
    for i, (c, tx, cx) in enumerate(((OPT_A, TA, 290), (OPT_B, TB, 790))):
        st = 3.0 + i * 0.5
        pulse = 1 + 0.03 * math.sin((t - st) * 6 + i * 3) if t > st + 0.6 else 1
        appear(fr, c, cx, 870, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 912, ease_out(prog(t, st + 0.05, 0.3)), pulse)
    appear(fr, CMT, W / 2, 1110, t, 5.0, pop=True)
    appear(fr, FOL, W / 2, 1250, t, 6.5, pop=True)

SCENES = [(S[i], f) for i, f in enumerate((s0, s1, s2, s3, s4, s5))]
VOICE = None
MUSIC_GAIN = 0.4
MUSIC = [(0.0, "cinematic"), (ST[1], "tension"), (ST[2], "curious"), (ST[3], "drive"), (ST[4], "uplift"), (ST[5], "tension"), (ST[5] + 6.4, "uplift")]
MUSIC_SEED = 2311
SFX = [(0.0, "rain"), (0.0, "whoosh"), (1.2, "thunder"), (6.0, "rain"),
       (ST[1] + 0.1, "swoosh"), (starts[1] + 1.5, "pop"), (starts[2], "whoosh"), (starts[2] + 0.3, "ding"),
       (ST[2] + 0.1, "swoosh"), (starts[3] + 2.0, "pop"), (starts[4] + 3.0, "pop"),
       (ST[3] + 0.1, "swoosh"), (starts[6] + 0.6, "boing"), (starts[6] + 1.0, "ding"),
       (ST[4] + 0.1, "pop"), (ST[4] + 1.6, "ding"), (ST[4] + 4.0, "pop"),
       (ST[5] + 0.1, "pop"), (ST[5] + 3.0, "pop"), (ST[5] + 3.5, "pop"), (ST[5] + 4.2, "ticks"), (ST[5] + 6.5, "chime")]
if __name__ == "__main__": print("total", round(ST[-1], 1), [round(x, 1) for x in S])
