"""28 Nov 2026 (Sat, free slot) · Brazil nut effect — shake a mixture packet and the big peanuts come to the top.
Off-syllabus little-known everyday phenomenon (backlog item). No quiz → comment question.
Why chain: heavier things "should" sink (gravity) → but the pile is being SHAKEN → each shake every grain hops, small gaps open
under the big nut → small grains slip into those gaps, the big nut cannot fit into a small gap → it lands a little higher each time
(ratchet, "percolation") → plus granular convection: grains rise in the middle and go down in a thin layer along the walls, too thin
for the big nut, so it stays on top. Twist: Rosato et al. 1987, Phys. Rev. Lett. "Why the Brazil nuts are on top"; studied for
asteroids (Matsumura et al. 2014, MNRAS: "The Brazil-nut effect and its application to asteroids"); a reverse effect also exists.
No voice by default: captions word by word at reading pace."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import reelkit
from storykit import *
from captions import Captions
reelkit.SYMBOLS |= set("✓✗↻")

HANDLE = "@jmk.space"
random.seed(28)

LINES = [
    ("കുലുക്കും തോറും വലിയ *കപ്പലണ്ടി* മുകളിലേക്ക് കയറി വരുന്നു. ഇതിന് ഒരു പേരുണ്ട്: *Brazil nut effect*!", YELLOW),
    ("*Mass* കൂടിയതിനെ *gravity* താഴേക്കല്ലേ വലിക്കേണ്ടത്? ഇവിടെ കളി *gravity* മാത്രമല്ല — *shaking* ആണ്.", CYAN),
    ("ഓരോ കുലുക്കത്തിലും എല്ലാം ഒന്ന് ചാടുന്നു. വലിയ കപ്പലണ്ടിയുടെ അടിയിൽ ഒരു ചെറിയ *gap* തുറക്കുന്നു.", ORANGE),
    ("ചെറിയ കഷണങ്ങൾ ആ *gap*-ലേക്ക് ഊർന്നിറങ്ങും. വലിയതിന് ചെറിയ *gap*-ൽ കയറാൻ പറ്റില്ല!", YELLOW),
    ("താഴെ ഇടം നിറഞ്ഞു — അതുകൊണ്ട് ഓരോ കുലുക്കത്തിലും വലിയത് ഒരു പടി മുകളിൽ. ഒരു *ratchet* പോലെ!", GREEN),
    ("ഇനി രണ്ടാമത്തെ കാരണം: *granular convection*. നടുവിലൂടെ *grains* മുകളിലേക്ക്, ഭിത്തിയോട് ചേർന്ന് നേർത്ത വഴിയിലൂടെ താഴേക്ക്.", CYAN),
    ("ആ നേർത്ത വഴിയിൽ വലിയത് കയറില്ല — അതുകൊണ്ട് അത് മുകളിൽ തന്നെ കുടുങ്ങുന്നു.", PINK),
    ("1987-ൽ *Physical Review Letters*-ൽ ഇതിനെക്കുറിച്ച് ഒരു *paper* വന്നു: *Why the Brazil nuts are on top*.", YELLOW),
    ("Twist: *asteroid*-കളിലെ വലിയ പാറകൾ മുകളിൽ വരുന്നതിനും ഇതേ *effect* ആണോ എന്ന് scientists പഠിക്കുന്നു!", ORANGE),
]
PACE = 0.42
def _dur(i, extra): return len(LINES[i][0].split()) * PACE + extra

PLAN = [[0], [1], [2, 3, 4], [5, 6], [7, 8], []]
GAP = {0: 1.6, 1: 1.4, 2: 1.4, 3: 1.4, 4: 1.6, 5: 1.4, 6: 1.6, 7: 1.4, 8: 1.8}
HOOK_T = 3.0      # hook read time before the first caption line
S, ST, starts = [], [0.0], []
for k, idx in enumerate(PLAN):
    t = HOOK_T if k == 0 else 0.3
    for i in idx:
        starts.append(ST[-1] + t); t += _dur(i, GAP[i])
    S.append(t if idx else 8.5)
    ST.append(ST[-1] + S[-1])
CAP = Captions([(txt, st, None, hl) for (txt, hl), st in zip(LINES, starts)], None, size=52, wpm_pace=PACE)
def caps(fr, s_idx, t, y=1335): CAP.draw(fr, ST[s_idx] + t, y)
def ls(i, sc): return starts[i] - ST[sc]


BG_IMG = grad(W, H, [(0, (12, 14, 34)), (0.55, (34, 22, 54)), (1, (14, 16, 40))])

# ---------- grains & jar ----------
MIX = [(236, 170, 70), (214, 120, 50), (250, 205, 110), (190, 90, 40), (240, 150, 60)]   # sev / boondi colours
NUT = (196, 130, 80)
def peanut(d, k, cx, cy, R, col=NUT):
    """A peanut-ish blob: two overlapping circles + a crease line."""
    r2 = R * 0.72
    for dx in (-R * 0.38, R * 0.38):
        d.ellipse(((cx + dx - r2) * k, (cy - r2) * k, (cx + dx + r2) * k, (cy + r2) * k), fill=col + (255,))
    d.ellipse(((cx - R * 0.3) * k, (cy - R * 0.45) * k, (cx + R * 0.05) * k, (cy - R * 0.15) * k), fill=(232, 180, 130, 180))
    for j in range(5):
        x = cx - R * 0.8 + j * R * 0.4
        d.line(((x) * k, (cy - R * 0.25) * k, (x + 4) * k, (cy + R * 0.25) * k), fill=(150, 95, 55, 200), width=int(3 * k))

class Jar:
    def __init__(self, x0, x1, y0, y1, r=15, fill=0.86):
        self.x0, self.x1, self.y0, self.y1, self.r = x0, x1, y0, y1, r
        self.top = y1 - (y1 - y0) * fill
        self.g = []
        rng = random.Random(5); dy = r * 1.75
        row = 0; y = y1 - r - 4
        while y > self.top:
            off = r if row % 2 else 0
            x = x0 + r + 6 + off
            while x < x1 - r - 4:
                self.g.append([x + rng.uniform(-3, 3), y + rng.uniform(-2, 2), rng.choice(MIX), rng.uniform(0, 6.3)])
                x += 2 * r + 1
            y -= dy; row += 1
    def draw(self, fr, nut_y, R, shake=0.0, t=0.0, extra=None):
        L = SS(W, H); d = L.d; k = L.k
        oy = -shake
        # glass
        d.rounded_rectangle(((self.x0 - 14) * k, (self.y0 - 30 + oy) * k, (self.x1 + 14) * k, (self.y1 + 14 + oy) * k), radius=40 * k,
                            fill=(120, 170, 255, 34), outline=(190, 215, 255, 200), width=int(6 * k))
        cx = (self.x0 + self.x1) / 2
        for gx, gy, col, ph in self.g:
            jx = math.sin(t * 31 + ph) * 3 * (shake > 1)
            jy = math.cos(t * 27 + ph) * 3 * (shake > 1)
            # grains overlapping the nut are pushed out of the way (not drawn)
            if math.hypot((gx - cx) / 1.25, gy - nut_y) < R + self.r * 0.3: continue
            if extra and extra(gx, gy): continue
            r = self.r
            d.ellipse(((gx + jx - r) * k, (gy + jy - r + oy) * k, (gx + jx + r) * k, (gy + jy + r + oy) * k), fill=col + (255,))
        peanut(d, k, cx, nut_y + oy, R)
        img = L.done(); fr.paste(img, (0, 0), img)

def shake_amp(t, t0, t1, per=0.26, amp=16):
    if t < t0 or t > t1: return 0.0
    return amp * abs(math.sin(math.pi * (t - t0) / per))

def stair(t, t0, t1, y_start, y_end, per=0.26):
    """nut height: rises one small step per shake (ratchet)."""
    if t <= t0: return y_start
    n_tot = max(1, int((t1 - t0) / per)); n = min(n_tot, int((t - t0) / per))
    frac = ease_out(clamp(((t - t0) % per) / per)) if n < n_tot else 0
    return y_start + (y_end - y_start) * min(1, (n + frac) / n_tot)

# ---------- S0 hook ----------
H0 = headline("BIG ONES ON *TOP?*", hl=YELLOW, size=96)
HOOK = text_img("*Mixture* packet കുലുക്കിയാൽ വലിയ *കപ്പലണ്ടി* മുകളിൽ! ഭാരം കൂടിയത് താഴെ പോകേണ്ടേ?", 60, max_w=980, hl=YELLOW)
JAR0 = Jar(300, 780, 640, 1240, r=15)
NUT_R = 54
SH0, SH1 = 0.2, S[0] - 1.0
def s0(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    sh = shake_amp(t, SH0, SH1)
    ny = stair(t, SH0, SH1, JAR0.y1 - NUT_R - 10, JAR0.top - 6)
    JAR0.draw(fr, ny, NUT_R, sh, t)
    paste(fr, H0, W / 2, 120)
    paste(fr, HOOK, W / 2, 270, 1.0, 1 + 0.015 * math.sin(t * 4))

    caps(fr, 0, t)

# ---------- S1 paradox: gravity vs shaking ----------
H1 = headline("GRAVITY *vs* SHAKING", hl=CYAN, size=90)
G_LBL = boxed(text_img("*mg* ↓", 46, max_w=260, hl=CYAN), pad=12, outline=(79, 209, 255, 180))
Q_LBL = boxed(text_img("എന്നിട്ടും മുകളിലേക്ക്?", 42, max_w=600, hl=YELLOW, color=YELLOW), pad=12, outline=(255, 209, 102, 180))
def s1(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    sh = shake_amp(t, 0.0, S[1], per=0.3, amp=10)
    ny = JAR0.top - 6
    JAR0.draw(fr, ny, NUT_R, sh, t)
    cx = W / 2
    a = ease_out(prog(t, 1.0, 0.5))
    if a > 0:
        arrow(d, cx, ny + 10, cx, ny + 10 + 170 * a, CYAN, 12, 36)
        paste(fr, G_LBL, cx + 170, ny + 80, a)
    appear(fr, Q_LBL, W / 2, 470, t, ls(1, 1) + 2.0, pop=True)
    paste(fr, H1, W / 2, 140)
    caps(fr, 1, t)

# ---------- S2 percolation zoom ----------
H2 = headline("WHY? *GAPS!*", hl=ORANGE, size=96)
ZB_R, Zr = 130, 38
ZX, ZFLOOR = W / 2, 1180
SIDE = []
for row in range(6):
    y = ZFLOOR - Zr - row * (Zr * 1.75)
    off = Zr if row % 2 else 0
    x = 90 + off
    while x < W - 90:
        if abs(x - ZX) > ZB_R + Zr * 0.9: SIDE.append((x, y, MIX[(row * 7 + int(x)) % 5]))
        x += 2 * Zr + 2
CYC = 2.4
GAP_LBL = boxed(text_img("*gap*", 40, max_w=160, hl=ORANGE), pad=10, outline=(255, 159, 67, 200))
OK_LBL = boxed(text_img("ചെറുത് ✓", 38, max_w=260, color=GREEN), pad=10, outline=(91, 228, 155, 200))
NO_LBL = boxed(text_img("വലുത് ✗", 38, max_w=260, color=RED), pad=10, outline=(255, 92, 92, 200))
RAT = boxed(text_img("*ratchet* ↑", 44, max_w=360, hl=GREEN), pad=12, outline=(91, 228, 155, 200))
def s2(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    paste(fr, H2, W / 2, 140)
    t0 = 0.4
    n = 0 if t < t0 else int((t - t0) / CYC)
    u = 0 if t < t0 else ((t - t0) % CYC) / CYC
    n = min(n, 5)
    stack_h = n * Zr * 1.75
    lift = 70 * math.sin(math.pi * clamp(u / 0.45)) if u < 0.45 else 0
    by = ZFLOOR - stack_h - ZB_R + 10 - lift
    L = SS(W, H); dd = L.d; k = L.k
    dd.line((60 * k, (ZFLOOR + 4) * k, (W - 60) * k, (ZFLOOR + 4) * k), fill=(140, 150, 200, 255), width=int(6 * k))
    side_lift = lift * 0.5
    for x, y, col in SIDE:
        if y < by - ZB_R - 40: continue
        dd.ellipse(((x - Zr) * k, (y - Zr - side_lift) * k, (x + Zr) * k, (y + Zr - side_lift) * k), fill=col + (255,))
    # grains already under the nut (the stack)
    for j in range(n):
        y = ZFLOOR - Zr - j * Zr * 1.75
        dd.ellipse(((ZX - Zr) * k, (y - Zr) * k, (ZX + Zr) * k, (y + Zr) * k), fill=MIX[j % 5] + (255,))
    # the grain that slides into the gap during this cycle
    gy = ZFLOOR - Zr - n * Zr * 1.75
    if t >= t0 and n < 5:
        m = ease_in_out(clamp((u - 0.15) / 0.35))
        gx = ZX - (ZB_R + Zr + 10) * (1 - m)
        gyy = gy - 60 * (1 - m) - side_lift * (1 - m)
        dd.ellipse(((gx - Zr) * k, (gyy - Zr) * k, (gx + Zr) * k, (gyy + Zr) * k), fill=(255, 220, 140, 255), outline=(91, 228, 155, 255), width=int(5 * k))
    # gap outline under the lifted nut
    if lift > 15:
        dd.rounded_rectangle(((ZX - Zr - 8) * k, (by + ZB_R - 6) * k, (ZX + Zr + 8) * k, (by + ZB_R + lift + 4) * k), radius=14 * k,
                             outline=(255, 159, 67, 230), width=int(4 * k))
    # big nut (peanut, scaled)
    peanut(dd, k, ZX, by, ZB_R * 0.95)
    img = L.done(); fr.paste(img, (0, 0), img)
    if lift > 15: paste(fr, GAP_LBL, ZX + 200, by + ZB_R - 20)
    appear(fr, OK_LBL, 230, 470, t, ls(3, 2) + 1.0, pop=True)
    appear(fr, NO_LBL, 850, 470, t, ls(3, 2) + 3.0, pop=True)
    appear(fr, RAT, W / 2, 570, t, ls(4, 2) + 3.0, pop=True)
    caps(fr, 2, t)

# ---------- S3 granular convection ----------
H3 = headline("GRANULAR *CONVECTION*", hl=CYAN, size=86)
JX0, JX1, JY0, JY1 = 250, 830, 560, 1200
LANE = 34
NP = 70
PATH_SEED = [random.random() for _ in range(NP)]
def loop_pt(s, side):
    """Closed loop for one half: up the middle, out along the top, down the wall lane, in along the bottom."""
    cx = W / 2; xi = cx + side * 40; xo = (JX1 - LANE / 2) if side > 0 else (JX0 + LANE / 2)
    ytop, ybot = JY0 + 90, JY1 - 30
    segs = [((xi, ybot), (xi, ytop)), ((xi, ytop), (xo, ytop)), ((xo, ytop), (xo, ybot)), ((xo, ybot), (xi, ybot))]
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]
    tot = sum(lens); s = (s % 1) * tot
    for (a, b), l in zip(segs, lens):
        if s <= l:
            f = s / l; return a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
        s -= l
    return segs[-1][1]
FILL = Jar(JX0, JX1, JY0, JY1, r=14, fill=0.92)
BLK = boxed(text_img("✗", 44, max_w=60, color=RED), pad=6, outline=(255, 92, 92, 200))
def s3(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    paste(fr, H3, W / 2, 140)
    cx = W / 2
    ny = FILL.top + 10 + 6 * math.sin(t * 7)
    # dim background grains
    FILL.draw(fr, ny, NUT_R, 6.0, t)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rectangle((JX0, JY0 - 20, JX1, JY1 + 10), fill=(10, 12, 30, 120))
    a = ease_out(prog(t, ls(5, 3) + 2.0, 0.6))
    # wall lanes
    for x in (JX0, JX1 - LANE):
        od.rectangle((x, JY0 + 60, x + LANE, JY1), fill=(79, 209, 255, int(70 * a)))
    fr.paste(ov, (0, 0), ov)
    if a > 0:
        L = SS(W, H); dd = L.d; k = L.k
        for side in (1, -1):
            for i, s0_ in enumerate(PATH_SEED[: NP // 2] if side > 0 else PATH_SEED[NP // 2:]):
                x, y = loop_pt(s0_ + t * 0.07, side)
                dd.ellipse(((x - 11) * k, (y - 11) * k, (x + 11) * k, (y + 11) * k), fill=MIX[i % 5] + (int(255 * a),))
        img = L.done(); fr.paste(img, (0, 0), img)
        arrow(d, cx, JY1 - 80, cx, JY0 + 160, YELLOW, 10, 34)
        for side in (1, -1):
            xo = (JX1 - LANE / 2) if side > 0 else (JX0 + LANE / 2)
            arrow(d, xo, JY0 + 160, xo, JY1 - 90, CYAN, 8, 28)
        L = SS(W, H); dd = L.d; k = L.k
        peanut(dd, k, cx, ny, NUT_R)
        img = L.done(); fr.paste(img, (0, 0), img)
    b = prog(t, ls(6, 3) + 1.0, 0.5)
    if b > 0:
        # the nut tries to go towards the wall lane and is blocked
        for side in (1, -1):
            xo = (JX1 - LANE / 2) if side > 0 else (JX0 + LANE / 2)
            paste(fr, BLK, xo, JY0 + 100, ease_out(b), 0.7 + 0.3 * ease_back(b))
    caps(fr, 3, t)

# ---------- S4 history + asteroid twist ----------
H4 = headline("1987 · *PRL*", hl=YELLOW, size=96)
PAPER = card(900, 300, fill=(255, 255, 255, 230), outline=(255, 209, 102, 255))
PT1 = text_img("PHYSICAL REVIEW LETTERS · 1987", 34, max_w=840, color=(60, 60, 90))
PT2 = text_img("“Why the Brazil Nuts Are on Top”", 54, max_w=840, color=(20, 20, 40))
PT3 = text_img("Rosato · Strandburg · Prinz · Swendsen", 32, max_w=840, color=(90, 90, 120))
H4B = headline("TWIST: *ASTEROIDS!*", hl=ORANGE, size=90)
random.seed(4)
ROCKS = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(10, 30)) for _ in range(40)]
def asteroid(fr, cx, cy, t, a):
    L = SS(W, 700); dd = L.d; k = L.k; oy = 350
    ang = t * 0.25
    pts = []
    for j in range(60):
        th = j / 60 * 2 * math.pi
        r = 230 + 60 * math.cos(2 * th) + 14 * math.sin(5 * th + 1)
        x, y = r * math.cos(th) * 1.25, r * math.sin(th) * 0.62
        xr, yr = x * math.cos(ang * 0.3) - y * math.sin(ang * 0.3), x * math.sin(ang * 0.3) + y * math.cos(ang * 0.3)
        pts.append(((cx + xr) * k, (oy + yr) * k))
    dd.polygon(pts, fill=(120, 116, 112, int(255 * a)))
    for rx, ry, rr in ROCKS:
        x, y = rx * 220 * 1.1, ry * 120
        if (x / 300) ** 2 + (y / 150) ** 2 > 1: continue
        xr, yr = x * math.cos(ang * 0.3) - y * math.sin(ang * 0.3), x * math.sin(ang * 0.3) + y * math.cos(ang * 0.3)
        dd.ellipse(((cx + xr - rr) * k, (oy + yr - rr * 0.7) * k, (cx + xr + rr) * k, (oy + yr + rr * 0.7) * k), fill=(170, 165, 155, int(255 * a)))
    img = L.done(); fr.paste(img, (0, int(cy - 350)), img)
def s4(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    tb = ls(8, 4) - 0.3
    if t < tb:
        paste(fr, H4, W / 2, 140)
        appear(fr, PAPER, W / 2, 520, t, 0.3, pop=True)
        appear(fr, PT1, W / 2, 545, t, 0.6)
        appear(fr, PT2, W / 2, 610, t, 0.9)
        appear(fr, PT3, W / 2, 730, t, 1.2)
        # small jar with nut on top
        JAR_S.draw(fr, JAR_S.top - 4, 34, 0.0, t)
    else:
        a = ease_out(prog(t, tb, 0.6))
        paste(fr, H4B, W / 2, 140, a)
        asteroid(fr, W / 2, 800, t, a)
    caps(fr, 4, t)
JAR_S = Jar(400, 680, 880, 1200, r=11)

# ---------- S5 comment question ----------
CQ = headline("YOUR *TURN!*", hl=PINK, size=100)
Q = text_img("*Mixture*, *cornflakes*, *chips* packet... നിങ്ങൾ ഇത് എവിടെ കണ്ടിട്ടുണ്ട്?", 56, max_w=940, hl=YELLOW)
TRY = text_img("ഒരു *jar*-ൽ അരിയും ഒരു ചെറിയ പന്തും ഇട്ട് കുലുക്കി നോക്കൂ!", 46, max_w=920, hl=CYAN, color=WHITE)
CMT = text_img("കമന്റിൽ പറയൂ 👇".replace(" 👇", ""), 60, max_w=900, hl=CYAN, color=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 58, max_w=900, hl=YELLOW)
JAR5 = Jar(380, 700, 930, 1180, r=10, fill=0.8)
def s5(fr, t, d):
    fr.paste(BG_IMG, (0, 0))
    appear(fr, CQ, W / 2, 160, t, 0.1, pop=True)
    appear(fr, Q, W / 2, 340, t, 0.4)
    appear(fr, TRY, W / 2, 340 + Q.height + 30, t, 2.4)
    sh = shake_amp(t, 2.6, 7.0, per=0.24, amp=10)
    JAR5.draw(fr, stair(t, 2.6, 6.5, JAR5.y1 - 40, JAR5.top - 4), 32, sh, t)
    appear(fr, CMT, W / 2, 1250, t, 5.0, pop=True)
    appear(fr, FOL, W / 2, 1360, t, 6.2, pop=True)

SCENES = [(S[i], f) for i, f in enumerate((s0, s1, s2, s3, s4, s5))]
VOICE = None
MUSIC_GAIN = 0.42
MUSIC = [(0.0, "curious"), (ST[1], "tension"), (ST[2], "drive"), (ST[3], "curious"), (ST[4], "cinematic"), (ST[4] + ls(8, 4), "space"), (ST[5], "uplift")]
MUSIC_SEED = 2811
SFX = [(0.0, "whoosh"), (0.3, "ticks"), (ST[0] + HOOK_T, "pop"),
       (ST[1] + 0.1, "swoosh"), (ST[1] + 1.0, "pop"), (starts[1] + 2.0, "ding"),
       (ST[2] + 0.1, "swoosh"), (starts[3] + 1.0, "pop"), (starts[3] + 3.0, "pop"), (starts[4] + 3.0, "ding"),
       (ST[3] + 0.1, "swoosh"), (starts[5] + 2.0, "whoosh"), (starts[6] + 1.0, "pop"),
       (ST[4] + 0.1, "swoosh"), (ST[4] + 0.3, "pop"), (starts[8] - 0.3, "whoosh"), (starts[8] + 0.5, "ding"),
       (ST[5] + 0.1, "pop"), (ST[5] + 2.6, "ticks"), (ST[5] + 5.0, "pop"), (ST[5] + 6.2, "chime")]
if __name__ == "__main__": print("total", round(ST[-1], 1), [round(x, 1) for x in S])
