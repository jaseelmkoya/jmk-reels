"""Topic: Inertia of motion — why we fall forward when a bus brakes. (Plus One · Laws of Motion)"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import *

HANDLE = "@jmk.space"

TAG = pill("PLUS ONE PHYSICS · LAWS OF MOTION", 30, bg=CYAN)
def top_tag(fr, t, fade=False):
    paste(fr, TAG, W / 2, 250, ease_out(prog(t, 0.1, 0.4)) if fade else 1.0)

# ---------- bus world ----------
AY = 760            # top of animation region
AW, AH = W, 620
FLOOR = 1160 - AY   # floor y inside region
FEET_X = 560

BRAKE_T, BRAKE_D = 6.3, 0.7
def speed(t):  # 1 = cruising
    if t < BRAKE_T: return 1.0
    return max(0.0, 1 - (t - BRAKE_T) / BRAKE_D)

# lean simulation (theta>0 = leaning forward / right)
def _sim():
    dt, th, om = 1 / FPS / 4, 0.0, 0.0
    w, z, A = 6.0, 0.32, 10.5
    vals = []
    for k in range(int(12 * FPS * 4)):
        t = k * dt
        acc = A if BRAKE_T <= t < BRAKE_T + BRAKE_D else 0.0
        al = acc - w * w * th - 2 * z * w * om
        om += al * dt; th += om * dt
        if k % 4 == 0: vals.append(th)
    return vals
LEAN = _sim()
LEAN_MAX = max(LEAN)
def lean_at(t): return LEAN[min(len(LEAN) - 1, int(t * FPS))]

def dist(t):  # integrated road scroll in px
    s, k = 0.0, 0
    n = int(t * FPS)
    for k in range(n):
        s += speed(k / FPS) * 26
    return s

def body_pt(r, th, fx=FEET_X, fy=FLOOR):
    return fx + r * math.sin(th), fy - r * math.cos(th)

def draw_world(fr, t, th, scroll, braking=False, moving=True):
    L = SS(AW, AH); d = L.d; s = L.s
    # road + scenery
    road_y = 1235 - AY
    d.rectangle(s(0, road_y, AW, AH), fill=(24, 26, 52, 255))
    d.line(s(0, road_y, AW, road_y), fill=(120, 130, 190, 255), width=6)
    off = scroll % 160
    for x in range(-160, AW + 160, 160):
        xx = x - off
        d.rounded_rectangle(s(xx, road_y + 60, xx + 90, road_y + 72), radius=10, fill=(200, 205, 240, 255))
    poff = (scroll * 0.6) % 420
    for x in range(-420, AW + 420, 420):
        xx = x - poff
        d.rectangle(s(xx, road_y - 330, xx + 10, road_y), fill=(70, 78, 130, 255))
        d.ellipse(s(xx - 22, road_y - 352, xx + 32, road_y - 318), fill=(70, 78, 130, 255))
    # speed lines behind bus
    if moving and speed(t) > 0.05:
        for i, yy in enumerate((170, 250, 330)):
            ln = 120 * speed(t)
            x0 = 150 - ((scroll * 1.5 + i * 60) % 90)
            d.line(s(x0 - ln, yy, x0, yy), fill=(160, 220, 255, 140), width=6)
    # bus body (cut-away so the passenger is visible)
    bx0, bx1, by0, by1 = 210, 870, 900 - AY, 1185 - AY
    d.rounded_rectangle(s(bx0, by0, bx1, by1), radius=40, fill=(255, 159, 67, 255))
    d.rounded_rectangle(s(bx0 + 22, by0 + 22, bx1 - 22, by1 - 40), radius=22, fill=(255, 236, 210, 255))
    d.rectangle(s(bx0 + 22, FLOOR, bx1 - 22, FLOOR + 10), fill=(120, 80, 40, 255))
    # windshield on front (right)
    d.rounded_rectangle(s(bx1 - 22, by0 + 22, bx1 - 4, by0 + 120), radius=8, fill=(130, 210, 255, 255))
    # headlight + brake light
    d.ellipse(s(bx1 - 26, by1 - 70, bx1 - 4, by1 - 48), fill=(255, 245, 200, 255))
    d.rounded_rectangle(s(bx0 - 2, by1 - 80, bx0 + 16, by1 - 40), radius=6, fill=(255, 60, 60, 255) if braking else (140, 40, 40, 255))
    if braking:
        d.ellipse(s(bx0 - 40, by1 - 100, bx0 + 20, by1 - 20), outline=(255, 80, 80, 160), width=5)
    # handrail
    d.line(s(bx0 + 40, by0 + 50, bx1 - 40, by0 + 50), fill=(150, 150, 160, 255), width=6)
    # wheels
    ang = scroll / 50
    for wx in (330, 750):
        wy = 1190 - AY
        d.ellipse(s(wx - 52, wy - 52, wx + 52, wy + 52), fill=(30, 30, 40, 255))
        d.ellipse(s(wx - 24, wy - 24, wx + 24, wy + 24), fill=(180, 185, 200, 255))
        for k in range(3):
            a = ang + k * 2.094
            d.line(s(wx, wy, wx + 44 * math.cos(a), wy + 44 * math.sin(a)), fill=(90, 95, 110, 255), width=5)
    # passenger (pivot at feet)
    col = (40, 50, 110, 255)
    hip = body_pt(85, th); sh = body_pt(160, th); head = body_pt(196, th)
    for dx in (-16, 16):
        d.line(s(FEET_X + dx, FLOOR, *hip), fill=col, width=14)
    d.line(s(*hip, *sh), fill=col, width=18)
    hx, hy = head
    d.ellipse(s(hx - 24, hy - 24, hx + 24, hy + 24), fill=(140, 90, 60, 255))
    # arm reaching for the rail
    hand = (sh[0] + 30 + 40 * math.sin(th), by0 + 58)
    d.line(s(*sh, *hand), fill=col, width=12)
    fr.paste(L.done(), (0, AY), L.done())
    return hip, sh, head

# ---------- scenes ----------
# Timing rule: every text block stays on screen long enough to read it aloud
# (~0.5 s per word + 1 s), so JMK can record a voice-over on top. See VO script.
S1_D, S2_D, S3_D, S4_D, S5_D = 11.0, 14.0, 16.0, 10.5, 10.5

HOOK = text_img("ബസ് പെട്ടെന്ന് *brake* ഇടുമ്പോൾ നമ്മൾ *മുന്നോട്ട്* വീഴുന്നത് എന്തുകൊണ്ട്?", 66, max_w=900)
CAP1 = text_img("ബസ് നിന്നു... പക്ഷെ നമ്മൾ *മുന്നോട്ട്!*", 54, max_w=900, hl=ORANGE)
BRAKE = pill("BRAKE!", 40, fg=WHITE, bg=RED)

def s1(fr, t, d):
    top_tag(fr, t, fade=True)
    appear(fr, HOOK, W / 2, 330, t, 0.25, pop=True)
    br = BRAKE_T <= t < BRAKE_T + 1.2
    draw_world(fr, t, lean_at(t), dist(t), braking=br)
    if br:
        paste(fr, BRAKE, 300, 790, 1 - prog(t, BRAKE_T + 0.9, 0.3), 0.7 + 0.3 * ease_back(prog(t, BRAKE_T, 0.3)))
    appear(fr, CAP1, W / 2, 1385, t, 7.4)

WHY = text_img("കാരണം: *Inertia of Motion*", 60, max_w=1000, hl=CYAN)
LBL_UP = boxed(text_img("ശരീരത്തിന്റെ മുകൾഭാഗം *motion* തുടരുന്നു", 40, max_w=560, hl=ORANGE, lh=1.45), outline=(255, 159, 67, 180))
LBL_FEET = boxed(text_img("*Friction* കാരണം കാലുകൾ ബസിനൊപ്പം നിൽക്കുന്നു", 40, max_w=900, hl=GREEN, lh=1.45), outline=(91, 228, 155, 180))
CAP2 = text_img("*Inertia of motion*: *motion*-ലുള്ള body-ക്ക് *motion*-ൽ തന്നെ തുടരാനുള്ള *tendency*", 46, max_w=1000, hl=CYAN)

def s2(fr, t, d):
    top_tag(fr, t)
    appear(fr, WHY, W / 2, 360, t, 0.1, pop=True)
    th = LEAN_MAX * ease_out(prog(t, 0.0, 0.6))
    hip, sh, head = draw_world(fr, 11.5, th, dist(S1_D), moving=False)
    a1 = ease_out(prog(t, 1.8, 0.6))
    if a1 > 0:
        sx, sy = sh[0] + 30, sh[1] + AY
        arrow(d, sx, sy, sx + 150 * a1 + 10, sy, ORANGE, 12, 36)
    appear(fr, LBL_UP, 700, 700, t, 2.0)
    a2 = ease_out(prog(t, 4.8, 0.6))
    if a2 > 0:
        fx, fy = FEET_X - 30, FLOOR + AY - 8
        arrow(d, fx, fy, fx - 150 * a2 - 10, fy, GREEN, 12, 36)
    appear(fr, LBL_FEET, W / 2, 1262, t, 5.0, out_at=7.8)
    appear(fr, CAP2, W / 2, 1380, t, 8.2)

LAW_PILL = pill("NEWTON'S FIRST LAW (Law of Inertia)", 34, bg=YELLOW)
LAW = text_img("Every body continues to be in its state of *rest* or of *uniform motion in a straight line* unless compelled by some *external force* to change that state.", 44, max_w=880, hl=YELLOW, lh=1.45)
LAW_CARD = card(960, LAW.height + 40)
LAW_ML = text_img("*External force* ഇല്ലെങ്കിൽ *rest*-ൽ ഉള്ളത് *rest*-ൽ തന്നെ, *uniform motion*-ൽ ഉള്ളത് അങ്ങനെ തന്നെ തുടരും.", 42, max_w=940, hl=CYAN, color=WHITE)
F0 = text_img("F = 0  →  a = 0  →  v = constant", 52, max_w=960, color=CYAN)

def s3(fr, t, d):
    top_tag(fr, t)
    appear(fr, LAW_PILL, W / 2, 330, t, 0.1, pop=True)
    appear(fr, LAW_CARD, W / 2, 430, t, 0.3)
    appear(fr, LAW, W / 2, 445, t, 0.5)
    appear(fr, LAW_ML, W / 2, 470 + LAW.height + 60, t, 8.5)
    a = ease_out(prog(t, 12.5, 0.5))
    if a > 0:
        L = SS(W, 230); dd = L.d; s = L.s
        dd.line(s(80, 190, W - 80, 190), fill=(150, 160, 220, int(255 * a)), width=6)
        x = 120 + ((t - 12.5) * 230) % (W - 240)
        dd.ellipse(s(x - 45, 100, x + 45, 190), fill=(79, 209, 255, int(255 * a)))
        for k in range(3):
            dd.line(s(x - 75 - k * 30, 125 + k * 20, x - 55 - k * 30, 125 + k * 20), fill=(79, 209, 255, int(140 * a)), width=5)
        fr.paste(L.done(), (0, 1120), L.done())
    appear(fr, F0, W / 2, 1380, t, 12.8)

MASS_T = text_img("Mass = measure of *Inertia*", 76, max_w=1000, color=WHITE, hl=CYAN)
MASS_TXT = text_img("*Mass* കൂടുന്തോറും *inertia* കൂടും. ഒരേ *force* കൊടുത്താൽ *mass* കൂടിയ body-ക്ക് *acceleration* കുറവ്.", 48, max_w=920, hl=YELLOW)
AFM = text_img("a = F / m", 60, max_w=600, color=PINK)
LM = text_img("m", 60, max_w=120, color=(9, 14, 38))
LBM = text_img("M", 90, max_w=160, color=(9, 14, 38))
LF = text_img("F", 50, max_w=80, color=PINK)

def s4(fr, t, d):
    top_tag(fr, t)
    appear(fr, MASS_T, W / 2, 330, t, 0.1, pop=True)
    appear(fr, MASS_TXT, W / 2, 470, t, 0.8)
    a = ease_out(prog(t, 3.0, 0.4))
    if a > 0:
        tt = max(0.0, t - 4.0)
        for (y, size, m, lab) in ((900, 120, 1.0, LM), (1130, 200, 4.0, LBM)):
            x = min(230 + 0.5 * (36 / m) * tt * tt, 900 - size)   # same F, a = F/m
            ground = y + 210
            d.line((80, ground, W - 80, ground), fill=(110, 120, 180), width=4)
            L = SS(size + 4, size + 4); L.d.rounded_rectangle(L.s(2, 2, size, size), radius=18, fill=(91, 228, 155, int(255 * a)) if m == 1 else (255, 159, 67, int(255 * a)))
            fr.paste(L.done(), (int(x), ground - size), L.done())
            paste(fr, lab, x + size / 2, ground - size / 2 - lab.height / 2 + 8, a)
            if t > 3.4:
                arrow(d, x - 130, ground - size / 2, x - 12, ground - size / 2, PINK, 10, 30)
                paste(fr, LF, x - 150, ground - size / 2 - 80, a)
    appear(fr, AFM, W / 2, 1390, t, 4.5)

QUIZ = pill("QUIZ TIME", 44, fg=(9, 14, 38), bg=PINK)
PYQ = pill("PYQ · Plus One Exam 2023", 30, fg=WHITE, bg=(80, 60, 160))
Q = text_img("ബസ് പെട്ടെന്ന് *start* ചെയ്യുമ്പോൾ യാത്രക്കാർ പിന്നോട്ട് വീഴുന്നത് ഏത് *inertia* കാരണം?", 58, max_w=920, hl=YELLOW)
OPT_A = card(440, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(440, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) Inertia of rest", 42, max_w=420)
TB = text_img("B) Inertia of motion", 42, max_w=420)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 56, max_w=900, hl=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 52, max_w=900, hl=YELLOW, color=WHITE)

def s5(fr, t, d):
    appear(fr, QUIZ, W / 2, 290, t, 0.1, pop=True)
    appear(fr, PYQ, W / 2, 380, t, 0.3)
    appear(fr, Q, W / 2, 470, t, 0.5)
    for i, (c, tx, cx) in enumerate(((OPT_A, TA, 290), (OPT_B, TB, 790))):
        pulse = 1 + 0.03 * math.sin((t - 4) * 6 + i * 3) if t > 4.5 else 1
        appear(fr, c, cx, 860, t, 4.0 + i * 0.4, pop=True)
        if t > 4.3 + i * 0.4:
            paste(fr, tx, cx, 900, ease_out(prog(t, 4.2 + i * 0.4, 0.4)), pulse)
    appear(fr, CMT, W / 2, 1110, t, 6.8, pop=True)
    appear(fr, FOL, W / 2, 1270, t, 8.2)

SCENES = [(S1_D, s1), (S2_D, s2), (S3_D, s3), (S4_D, s4), (S5_D, s5)]
