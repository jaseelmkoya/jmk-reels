"""Science story reel (sample): C.V. Raman, 1921 — why is the sea blue?
Facts: Raman sailed to London in 1921 (SS Narkunda), watched the Mediterranean, used a Nicol prism
to cut the sky's reflected light and still saw deep blue; argued it is molecular scattering of light
by water (Nature 108, 367, 1921, "The colour of the sea"). This line of work led to the Raman effect,
announced 28 Feb 1928 (National Science Day); Nobel Prize in Physics 1930.
Modern note: water's absorption of red light also makes the sea blue."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storykit import *

HANDLE = "@jmk.space"
random.seed(4)
SRC = source(["NATURE (1921)", "NOBELPRIZE.ORG"])
BW, BH = int(W * 1.12), int(H * 1.12)

# ---------- S1 · the voyage (stylised map) ----------
def _land(d, pts, fill=(38, 52, 70, 255), edge=(80, 110, 140, 255)):
    d.polygon(pts, fill=fill, outline=edge)
MAP = grad(BW, BH, [(0, (6, 18, 38)), (1, (10, 34, 62))])
_md = ImageDraw.Draw(MAP)
for gx in range(0, BW, 60): _md.line((gx, 0, gx, BH), fill=(255, 255, 255, 10))
for gy in range(0, BH, 60): _md.line((0, gy, BW, gy), fill=(255, 255, 255, 10))
# Europe (top-left), Africa/Arabia (middle), India (bottom-right) — stylised blobs
_land(_md, [(0, 330), (200, 300), (330, 360), (470, 330), (600, 420), (640, 520), (520, 600), (380, 560), (250, 620), (120, 600), (0, 640)])
_land(_md, [(0, 760), (300, 700), (520, 720), (600, 800), (660, 960), (620, 1250), (520, 1500), (400, 1700), (250, 1760), (0, 1800)])
_land(_md, [(560, 700), (760, 720), (880, 860), (860, 1000), (720, 1040), (640, 900)])
_land(_md, [(860, 900), (1010, 860), (BW, 880), (BW, 1060), (1080, 1180), (1010, 1420), (960, 1340), (900, 1100)])
ROUTE = [(985, 1270), (840, 1180), (720, 1120), (640, 1010), (610, 860), (580, 700), (430, 640), (300, 600), (240, 520), (210, 430)]
_m2 = grad(BW, BH, [(0, (6, 18, 38)), (1, (10, 34, 62))]); _m2.paste(MAP, (0, -230)); MAP = _m2
_g2 = ImageDraw.Draw(MAP)
for gy in range(BH - 230, BH, 60): _g2.line((0, gy, BW, gy), fill=(255, 255, 255, 10))
for gx in range(0, BW, 60): _g2.line((gx, BH - 230, gx, BH), fill=(255, 255, 255, 10))
ROUTE = [(x, y - 230) for x, y in ROUTE]
def route_pts(n=200):
    out = []
    for i in range(n):
        u = i / (n - 1) * (len(ROUTE) - 1); k = min(int(u), len(ROUTE) - 2); f = u - k
        (x1, y1), (x2, y2) = ROUTE[k], ROUTE[k + 1]
        out.append((x1 + (x2 - x1) * f, y1 + (y2 - y1) * f))
    return out
RP = route_pts()
P_IN, P_MED, P_LON = pin_label("BOMBAY"), pin_label("MEDITERRANEAN SEA", dot=CYAN), pin_label("LONDON")
H1 = headline("A *VOYAGE* · 1921")
C1 = mono("SS NARKUNDA · BOMBAY → LONDON · ILLUSTRATION, NOT TO SCALE")
T1a = subtitle("1921-ൽ ഒരു കപ്പൽ യാത്ര. യാത്രക്കാരൻ: *C.V. Raman*.")
T1b = subtitle("കടന്നുപോയത് *Mediterranean* കടലിലൂടെ.", hl=CYAN)
def s1(fr, t, d):
    base = MAP.copy(); bd = ImageDraw.Draw(base)
    k = int(len(RP) * ease_in_out(prog(t, 0.6, 4.4)))
    for i in range(0, max(0, k - 1), 3):
        bd.line((*RP[i], *RP[i + 1]), fill=(255, 209, 102, 255), width=5)
    if k > 1:
        x, y = RP[k - 1]
        bd.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(255, 255, 255, 255))
    for img, (x, y), st in ((P_IN, ROUTE[0], 0.3), (P_MED, ROUTE[5], 2.8), (P_LON, ROUTE[-1], 4.4)):
        a = ease_out(prog(t, st, 0.4))
        if a > 0:
            bd.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(255, 209, 102, 255))
            paste(base, img, x, y + 18, a)
    fr.paste(push(base, t, 6.5, 1.0, 1.06, 0.6, 0.5), (0, 0))
    standard_overlay(fr, t, H1, T1a, SRC, C1, sub_at=0.6, sub2=T1b, sub2_at=3.2)

# ---------- S2/S3 · the blue sea ----------
SEA = grad(BW, BH, [(0, (120, 170, 220)), (0.36, (190, 215, 240)), (0.4, (12, 70, 140)), (1, (2, 20, 60))])
def sea_frame(t, dark=0.0):
    base = SEA.copy(); bd = ImageDraw.Draw(base)
    hy = int(BH * 0.4)
    for i in range(70):
        y = hy + 20 + (i ** 1.6) * 3.2
        if y > BH: break
        amp = 2 + i * 0.25
        pts = [(x, y + amp * math.sin(x / (30 + i * 2) + t * (1.2 + i * 0.03) + i)) for x in range(0, BW + 20, 20)]
        bd.line(pts, fill=(140, 200, 255, 30 + min(60, i)), width=2)
    # little ship on the horizon
    sxp = 300 + t * 14
    bd.polygon([(sxp, hy - 4), (sxp + 120, hy - 4), (sxp + 100, hy + 14), (sxp + 18, hy + 14)], fill=(20, 26, 40, 255))
    bd.rectangle((sxp + 45, hy - 34, sxp + 65, hy - 4), fill=(20, 26, 40, 255))
    if dark:
        ov = Image.new("RGBA", base.size, (0, 0, 0, int(255 * dark))); base.alpha_composite(ov)
    return base
H2 = headline("THE DEEP *BLUE* SEA", hl=CYAN)
T2a = subtitle("കടലിന്റെ ആ കടും നീല നിറം Raman-നെ ചിന്തിപ്പിച്ചു.", hl=CYAN)
T2b = subtitle("ഈ നീല എവിടെ നിന്ന് വരുന്നു?", hl=CYAN)
def s2(fr, t, d):
    fr.paste(push(sea_frame(t), t, 6.0, 1.0, 1.07, 0.5, 0.55), (0, 0))
    standard_overlay(fr, t, H2, T2a, SRC, None, sub_at=0.6, sub2=T2b, sub2_at=3.3)

H3 = headline("JUST A *REFLECTION?*", hl=ORANGE)
C3 = mono("THE OLD IDEA: THE SEA ONLY REFLECTS THE BLUE SKY")
T3a = subtitle("അന്നത്തെ വിശ്വാസം: കടൽ നീല ആകാശത്തിന്റെ *reflection* മാത്രം.", hl=ORANGE)
EYE = pin_label("OBSERVER", dot=WHITE)
def s3(fr, t, d):
    fr.paste(push(sea_frame(t + 6, 0.15), t, 5.0, 1.04, 1.08, 0.5, 0.5), (0, 0))
    p = ease_out(prog(t, 0.8, 0.9)); q = ease_out(prog(t, 1.6, 0.9))
    if p > 0: arrow(d, 300, 380, 300 + 260 * p, 380 + 420 * p, (190, 225, 255), 9, 30)
    if q > 0: arrow(d, 560, 800, 560 + 300 * q, 800 - 330 * q, ORANGE, 9, 30)
    appear(fr, EYE, 900, 410, t, 1.9, pop=True)
    standard_overlay(fr, t, H3, T3a, SRC, C3, sub_at=0.6)

# ---------- S4 · the pocket prism ----------
H4 = headline("A *POCKET* PRISM")
C4 = mono("A NICOL PRISM BLOCKS THE REFLECTED (POLARISED) SKYLIGHT")
T4a = subtitle("Raman കയ്യിലുള്ള *Nicol prism* വെച്ച് ആ *reflection* തടഞ്ഞു.")
T4b = subtitle("എന്നിട്ടും കടൽ *നീല* തന്നെ!", hl=CYAN)
PR = pin_label("NICOL PRISM")
def s4(fr, t, d):
    fr.paste(push(sea_frame(t + 11, 0.1), t, 6.0, 1.08, 1.12, 0.5, 0.5), (0, 0))
    # prism
    L = SS(W, H); ld = L.d
    cx, cy = 560, 820
    pts = [(cx - 70, cy - 150), (cx + 70, cy - 110), (cx + 70, cy + 150), (cx - 70, cy + 110)]
    ld.polygon([v for xy in pts for v in L.s(*xy)], fill=(200, 230, 255, 70), outline=(230, 245, 255, 220), width=6)
    fr.paste(L.done(), (0, 0), L.done())
    q = ease_out(prog(t, 0.9, 0.8))
    if q > 0:
        arrow(d, 860, 560, 860 - 230 * q, 560 + 250 * q, ORANGE, 9, 30)
    if t > 1.9:  # blocked
        a = ease_out(prog(t, 1.9, 0.3))
        d.line((600, 760, 680, 840), fill=RED, width=int(12 * a) or 1); d.line((680, 760, 600, 840), fill=RED, width=int(12 * a) or 1)
    appear(fr, PR, 560, 1010, t, 0.5, pop=True)
    standard_overlay(fr, t, H4, T4a, SRC, C4, sub_at=0.6, sub2=T4b, sub2_at=3.3)

# ---------- S5 · scattering ----------
MOLS = [(random.uniform(420, 980), random.uniform(560, 1080), random.uniform(0, 6.28)) for _ in range(9)]
H5 = headline("LIGHT *SCATTERS*", hl=CYAN)
C5 = mono("RAMAN'S ANSWER: MOLECULAR SCATTERING OF LIGHT BY WATER")
T5a = subtitle("Raman-ന്റെ ഉത്തരം: *water molecules* light-നെ *scatter* ചെയ്യുന്നു.", hl=CYAN)
T5b = subtitle("*Blue light* ആണ് കൂടുതൽ scatter ആകുന്നത്.", hl=CYAN)
DEEP = grad(BW, BH, [(0, (2, 22, 58)), (1, (1, 8, 26))])
def s5(fr, t, d):
    fr.paste(push(DEEP, t, 6.5, 1.0, 1.05), (0, 0))
    bx = 80 + 900 * ease_in_out(prog(t, 0.5, 1.6))
    d.line((0, 820, bx, 820), fill=(255, 250, 230), width=16)
    d.line((0, 820, bx, 820), fill=(255, 255, 255), width=6)
    for i, (mx, my, ph) in enumerate(MOLS):
        hit = bx > mx
        r = 26
        d.ellipse((mx - r, my - r, mx + r, my + r), fill=(240, 90, 90))
        for a in (ph, ph + 1.82):
            hx, hy = mx + 34 * math.cos(a), my + 34 * math.sin(a)
            d.ellipse((hx - 15, hy - 15, hx + 15, hy + 15), fill=(235, 240, 250))
        if hit:
            s = prog(t, 0.5 + 1.6 * (mx - 80) / 900, 1.2)
            for k in range(4):
                ang = ph + k * 1.57 + t * 0.3
                L2 = 20 + 80 * ease_out(s)
                arrow(d, mx + 40 * math.cos(ang), my + 40 * math.sin(ang), mx + (40 + L2) * math.cos(ang), my + (40 + L2) * math.sin(ang), CYAN, 6, 18)
    standard_overlay(fr, t, H5, T5a, SRC, C5, sub_at=0.6, sub2=T5b, sub2_at=3.4)

# ---------- S6 · what it led to ----------
H6 = headline("THE *RAMAN* EFFECT")
CARDS = [(pill("1928 · RAMAN EFFECT", 40, bg=YELLOW), 0.6), (pill("1930 · NOBEL PRIZE", 40, bg=CYAN), 1.6),
         (pill("FEB 28 · NATIONAL SCIENCE DAY", 38, fg=WHITE, bg=(80, 60, 160)), 2.6)]
T6a = subtitle("ഈ ചിന്ത *Raman effect* കണ്ടെത്തലിലേക്ക് നയിച്ചു.")
T6b = subtitle("ഇന്ന് അറിയാം: water *red light* absorb ചെയ്യുന്നതും ഒരു കാരണമാണ്.", hl=ORANGE)
def s6(fr, t, d):
    fr.paste(push(DEEP, t + 6.5, 6.5, 1.05, 1.1), (0, 0))
    for i, (c, st) in enumerate(CARDS):
        appear(fr, c, W / 2, 560 + i * 150, t, st, pop=True)
    standard_overlay(fr, t, H6, T6a, SRC, None, sub_at=0.6, sub2=T6b, sub2_at=3.6)

# ---------- S7 · end ----------
END1 = headline("FROM CURIOSITY TO *NOBEL*")
FOL = text_img("*Follow* ചെയ്യൂ", 70, max_w=900, hl=YELLOW)
def s7(fr, t, d):
    fr.paste(push(sea_frame(t + 20, 0.35), t, 4.0, 1.1, 1.14), (0, 0))
    fr.paste(VIG, (0, 0), VIG)
    appear(fr, END1, W / 2, 560, t, 0.2, pop=True)
    appear(fr, FOL, W / 2, 760, t, 1.0, pop=True)

SCENES = [(7.0, s1), (6.5, s2), (5.5, s3), (6.5, s4), (7.0, s5), (7.5, s6), (4.0, s7)]
_st = [0]
for dsc, _ in SCENES: _st.append(_st[-1] + dsc)
VOICE = None
SFX = [(0.0, "whoosh")]
for s in _st[1:-1]: SFX += [(s - 0.05, "swoosh")]
SFX += [(_st[0] + 0.3, "pop"), (_st[0] + 2.8, "pop"), (_st[0] + 4.4, "pop"), (_st[2] + 1.9, "pop"), (_st[3] + 1.9, "thud"),
        (_st[3] + 3.3, "ding"), (_st[5] + 0.6, "pop"), (_st[5] + 1.6, "pop"), (_st[5] + 2.6, "chime"), (_st[6] + 1.0, "ding")]
MUSIC = [(0.0, "cinematic"), (_st[1], "ocean"), (_st[3], "tension"), (_st[4], "curious"), (_st[5], "uplift")]
