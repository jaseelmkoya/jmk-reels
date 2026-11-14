"""Sunday story reel (15 Nov 2026): Kolkata–Sairang Express derailment, Digaru (Assam), 11 Nov 2026.
Loco pilot in the cab video: "BP pressure kam nahi ho raha" (brake pipe pressure is not dropping); NFR: pilot could not
control the speed, technical cause under investigation; no deaths, a few passengers with minor injuries.
Physics: Indian Railways twin-pipe air brake (brake pipe 5 kg/cm², feed pipe/aux reservoir 6 kg/cm², brake cylinder
355 mm dia, max 3.8 kg/cm² — IRIMEE 'Braking System Used in Indian Railways'): brakes apply when BP pressure is REDUCED.
Plus One Ch10 Mechanical properties of fluids: pressure P = F/A (normal force per unit area), Pascal's law, hydraulic brakes.
Quiz: PYQ March 2025 / 2024 / 2022 — hydraulic lift & brakes → Pascal's law.
No voice by default: captions word by word at reading pace."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storykit import *
from captions import Captions

random.seed(7)
SRC = source(["NFR", "BRUT", "IRIMEE · INDIAN RAILWAYS"])
BW, BH = int(W * 1.12), int(H * 1.12)
NIGHT = grad(BW, BH, [(0, (6, 10, 26)), (0.55, (14, 22, 44)), (1, (4, 6, 14))])
STEEL = grad(BW, BH, [(0, (10, 16, 30)), (1, (4, 8, 18))])
RED = (235, 70, 80)

# ---------- drawing helpers ----------
def gauge(d, cx, cy, r, val, label="BP", vmax=10, col=YELLOW):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(18, 22, 36), outline=(200, 205, 220), width=6)
    for k in range(vmax + 1):
        a = math.radians(225 - 270 * k / vmax)
        r1, r2 = r * 0.78, r * 0.92
        d.line((cx + r1 * math.cos(a), cy - r1 * math.sin(a), cx + r2 * math.cos(a), cy - r2 * math.sin(a)), fill=(200, 205, 220), width=4)
    a = math.radians(225 - 270 * val / vmax)
    d.line((cx, cy, cx + r * 0.72 * math.cos(a), cy - r * 0.72 * math.sin(a)), fill=col, width=8)
    d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=col)
    f = font("lat", "bold", int(r * 0.26))
    d.text((cx, cy + r * 0.42), label, font=f, fill=WHITE, anchor="mm")
    d.text((cx, cy + r * 1.22), f"{val:.1f} kg/cm²", font=font("lat", "bold", int(r * 0.24)), fill=col, anchor="mm")

def loco_front(d, cx, cy, s, glow=1.0):
    w, h = 300 * s, 360 * s
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=int(30 * s), fill=(60, 70, 96), outline=(20, 24, 36), width=6)
    d.rounded_rectangle((cx - w * 0.38, cy - h * 0.38, cx + w * 0.38, cy - h * 0.06), radius=int(14 * s), fill=(150, 200, 230))
    for sx in (-1, 1):
        x = cx + sx * w * 0.28; y = cy + h * 0.22
        rr = 26 * s
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 245, 200) if glow > 0.3 else (90, 90, 80))
    d.rectangle((cx - w * 0.45, cy + h * 0.38, cx + w * 0.45, cy + h * 0.46), fill=(240, 190, 60))

def coach(d, x, y, w=300, h=150, col=(70, 110, 170)):
    d.rounded_rectangle((x, y, x + w, y + h), radius=16, fill=col, outline=(20, 24, 36), width=5)
    for i in range(4):
        d.rounded_rectangle((x + 20 + i * 70, y + 22, x + 70 + i * 70, y + 70), radius=8, fill=(170, 210, 235))
    for wx in (50, w - 50):
        d.ellipse((x + wx - 28, y + h - 18, x + wx + 28, y + h + 38), fill=(30, 30, 36))

def wheel_brake(d, cx, cy, t, press, spin):
    """Wheel with a brake block pushed by a cylinder piston from the right. press 0..1."""
    R = 170
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(70, 74, 86), outline=(200, 205, 220), width=8)
    d.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), fill=(150, 150, 160))
    for k in range(6):
        a = spin + k * math.pi / 3
        d.line((cx + 45 * math.cos(a), cy + 45 * math.sin(a), cx + (R - 20) * math.cos(a), cy + (R - 20) * math.sin(a)), fill=(120, 124, 136), width=10)
    gap = 60 * (1 - press)
    bx = cx + R + 6 + gap
    d.rounded_rectangle((bx, cy - 90, bx + 40, cy + 90), radius=8, fill=(160, 110, 70), outline=(30, 20, 10), width=4)   # brake block
    d.rectangle((bx + 40, cy - 12, bx + 150, cy + 12), fill=(190, 195, 205))                                            # piston rod
    d.rounded_rectangle((cx + R + 150, cy - 70, cx + R + 330, cy + 70), radius=14, fill=(40, 46, 66), outline=(200, 205, 220), width=5)  # cylinder
    fill = int(170 * press)
    if fill > 4:
        d.rectangle((cx + R + 160, cy - 60, cx + R + 160 + fill, cy + 60), fill=(79, 209, 255))
    if press > 0.9:   # friction sparks
        for k in range(10):
            a = random.uniform(-0.9, 0.9); L = random.uniform(30, 90)
            sx, sy = cx + R, cy + random.uniform(-60, 60)
            d.line((sx, sy, sx + L * math.cos(a), sy + L * math.sin(a)), fill=(255, random.randint(170, 230), 80), width=4)

# ---------- text ----------
H1 = headline("BRAKE *FAILED?*", hl=RED)
C1 = mono("KOLKATA–SAIRANG EXPRESS · DIGARU, ASSAM · 11 NOV 2026")
QUOTE = boxed(text_img("\"BP pressure *കുറയുന്നില്ല!*\"", 60, max_w=900, hl=YELLOW), outline=(235, 70, 80, 200))
QUOTE_BY = text_img("— loco pilot, cab video", 34, max_w=700, color=(200, 205, 220))
SAFE = pill("ആരും മരിച്ചില്ല · കുറച്ചുപേർക്ക് ചെറിയ പരിക്ക്", 30, fg=WHITE, bg=(40, 120, 80))

H2 = headline("TRAIN = *AIR* BRAKE", hl=CYAN)
C2 = mono("BRAKE PIPE (BP) RUNS THROUGH EVERY COACH")
H3 = headline("PRESSURE *DROPS* = BRAKE ON", hl=YELLOW, size=80)
C3 = mono("DISTRIBUTOR VALVE → BRAKE CYLINDER → BRAKE BLOCK")
H4 = headline("*F* = P × A", hl=YELLOW, size=110)
DEF = text_img("*Pressure* is the normal force acting per unit area.", 50, max_w=880, hl=YELLOW, lh=1.4)
DEF_CARD = card(960, DEF.height + 50)
CALC = [text_img(s, 46, max_w=960, hl=CYAN) for s in (
    "P = 3.8 kg/cm²  ≈  3.7 × 10⁵ Pa",
    "A = π (17.75 cm)²  ≈  990 cm²",
    "*F ≈ 37,000 N*  — ഒരു cylinder-ൽ നിന്ന്!")]
H5 = headline("PRESSURE *STUCK*", hl=RED)
C5 = mono("TECHNICAL CAUSE: UNDER INVESTIGATION (NFR)")
H6 = headline("CAR = *HYDRAULIC* BRAKE", hl=ORANGE, size=84)
LAW = text_img("The pressure applied at any point on a continuous fluid in equilibrium is equally transmitted to all other points.", 44, max_w=880, hl=YELLOW, lh=1.4)
LAW_PILL = pill("PASCAL'S LAW", 40, bg=YELLOW)
LAW_CARD = card(960, LAW.height + 50)
QUIZ = pill("QUIZ TIME", 44, fg=(9, 14, 38), bg=PINK)
PYQ = pill("PYQ · Plus One Exam 2025, 2024, 2022", 30, fg=WHITE, bg=(80, 60, 160))
Q = text_img("*Hydraulic brakes* ഏത് law-ന്റെ application ആണ്?", 58, max_w=920, hl=YELLOW)
OPT_A = card(480, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(480, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) Pascal's law", 40, max_w=460)
TB = text_img("B) Newton's law", 40, max_w=460)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 56, max_w=900, hl=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 56, max_w=900, hl=YELLOW)

# ---------- narration (word by word, reading pace) ----------
LINES = [
    ("Nov 11, Assam: Kolkata–Sairang Express-ന്റെ engine-ഉം അഞ്ച് coach-ഉം പാളം തെറ്റി.", RED),
    ("Loco pilot പറഞ്ഞത്: \"BP pressure കുറയുന്നില്ല!\" എന്താണ് ഈ *BP*?", YELLOW),
    ("Train ഓടുമ്പോൾ *brake pipe*-ൽ 5 kg/cm² *pressure* നിറച്ചുവെക്കും.", CYAN),
    ("Brake ഇടാൻ driver ഈ *pressure* കുറയ്ക്കുന്നു. അപ്പോൾ *air* *brake cylinder*-ലേക്ക് കയറി *brake block* wheel-ൽ അമരുന്നു.", YELLOW),
    ("*Friction* വഴി *kinetic energy* *heat* ആയി മാറുന്നു. Train നിൽക്കുന്നു.", ORANGE),
    ("Brake block-നെ തള്ളുന്ന *force* എവിടെ നിന്ന്? *F = P × A*", YELLOW),
    ("ചെറിയ *pressure*, വലിയ *area* → വലിയ *force*.", CYAN),
    ("*BP pressure* കുറഞ്ഞില്ലെങ്കിൽ *brake cylinder*-ൽ *air* എത്തില്ല — brake വീഴില്ല. യഥാർത്ഥ കാരണം അന്വേഷണത്തിലാണ്.", RED),
    ("Car-ൽ *brake oil* വഴി *pressure* എല്ലാ wheel-ലേക്കും ഒരുപോലെ എത്തുന്നു — ഇതാണ് *Pascal's law*.", ORANGE),
]
PACE = 0.42
def _dur(text, extra): return len(text.split()) * PACE + extra
# scene layout: S1 lines 0-1, S2 line 2, S3 lines 3-4, S4 lines 5-6, S5 line 7, S6 line 8, S7 quiz
S = [max(7.0, _dur(LINES[0][0], 0.8) + _dur(LINES[1][0], 1.4)),
     max(5.5, _dur(LINES[2][0], 2.2)),
     max(9.0, _dur(LINES[3][0], 0.8) + _dur(LINES[4][0], 1.4)),
     max(9.0, _dur(LINES[5][0], 3.0) + _dur(LINES[6][0], 1.6)),
     max(6.0, _dur(LINES[7][0], 1.6)),
     max(8.0, _dur(LINES[8][0], 4.0)),
     8.5]
ST = [0.0]
for d_ in S: ST.append(ST[-1] + d_)
starts = [ST[0] + 0.3, ST[0] + 0.3 + _dur(LINES[0][0], 0.8), ST[1] + 0.4, ST[2] + 0.3, ST[2] + 0.3 + _dur(LINES[3][0], 0.8),
          ST[3] + 0.4, ST[3] + 0.4 + _dur(LINES[5][0], 3.0), ST[4] + 0.4, ST[5] + 0.4]
CAP = Captions([(txt, st, None, hl) for (txt, hl), st in zip(LINES, starts)], None, size=52, wpm_pace=PACE)

def caps(fr, s_idx, t, y=1330):
    CAP.draw(fr, ST[s_idx] + t, y)

# ---------- scenes ----------
def s1(fr, t, d):
    base = NIGHT.copy(); bd = ImageDraw.Draw(base)
    # rails converging
    for sx in (-1, 1):
        bd.line((BW / 2 + sx * 40, 700, BW / 2 + sx * 520, BH), fill=(140, 150, 170), width=10)
    for k in range(14):
        yy = 720 + k ** 1.7 * 9
        hw = 50 + (yy - 700) * 0.55
        bd.line((BW / 2 - hw, yy, BW / 2 + hw, yy), fill=(70, 60, 50), width=8)
    # red signal
    bd.rounded_rectangle((180, 520, 260, 700), radius=20, fill=(20, 20, 26))
    on = int(t * 3) % 2 == 0
    bd.ellipse((195, 540, 245, 590), fill=RED if on else (80, 20, 24))
    fr.paste(push(base, t, S[0], 1.0, 1.08), (0, 0))
    s = 0.7 + 0.9 * ease_in_out(clamp(t / S[0]))
    jolt = 10 * math.sin(t * 40) * prog(t, S[0] - 2.5, 0.5)
    loco_front(d, W / 2 + jolt, 900, s)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H1, W / 2, 230, 1.0)                                       # hook visible from frame 0
    paste(fr, C1, W / 2, 380, ease_out(prog(t, 0.6, 0.4)))
    appear(fr, QUOTE, W / 2, 470, t, starts[1] - ST[0], pop=True)
    appear(fr, QUOTE_BY, W / 2, 470 + QUOTE.height + 10, t, starts[1] - ST[0] + 0.4)
    appear(fr, SAFE, W / 2, 1200, t, 2.0)
    paste(fr, SRC, W / 2, 1265, ease_out(prog(t, 0.6, 0.4)))
    caps(fr, 0, t)

def _pipe_scene(fr, t, d, bp, show_gauge=True):
    fr.paste(push(STEEL, t, 8, 1.0, 1.04), (0, 0))
    y = 760
    x0 = 40 - (t * 30) % 330
    for i in range(5):
        coach(d, x0 + i * 330, y)
    d.line((0, y + 175, W, y + 175), fill=(255, 209, 102), width=10)       # brake pipe
    flow = (t * 200) % 60
    for xx in range(int(-60 + flow), W, 60):
        d.line((xx, y + 175, xx + 24, y + 175), fill=(255, 245, 200), width=4)
    paste(fr, text_img("BRAKE PIPE", 34, max_w=400, color=YELLOW), 170, y + 195, 1.0)
    if show_gauge:
        gauge(d, W / 2, 520, 130, bp)

def s2(fr, t, d):
    _pipe_scene(fr, t, d, 5.0)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H2, W / 2, 200, 1.0); paste(fr, C2, W / 2, 330, ease_out(prog(t, 0.3, 0.4)))
    caps(fr, 1, t)

def s3(fr, t, d):
    fr.paste(push(STEEL, t + 8, 10, 1.0, 1.04), (0, 0))
    k = ease_in_out(prog(t, 1.0, 2.0))
    bp = 5.0 - 1.5 * k
    gauge(d, 250, 520, 110, bp)
    press = ease_out(prog(t, 2.0, 1.2))
    spin = -t * (6 * (1 - 0.85 * press))
    wheel_brake(d, 330, 900, t, press, spin)
    paste(fr, pin_label("BRAKE CYLINDER", dot=CYAN), 740, 1000, ease_out(prog(t, 2.2, 0.4)))
    paste(fr, pin_label("BRAKE BLOCK", dot=ORANGE), 560, 700, ease_out(prog(t, 2.6, 0.4)))
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H3, W / 2, 200, 1.0); paste(fr, C3, W / 2, 320, ease_out(prog(t, 0.3, 0.4)))
    caps(fr, 2, t)

def s4(fr, t, d):
    fr.paste(push(STEEL, t + 18, 10, 1.04, 1.08), (0, 0))
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H4, W / 2, 190, 1.0)
    appear(fr, DEF_CARD, W / 2, 360, t, 0.3)
    appear(fr, DEF, W / 2, 385, t, 0.4)
    for i, c in enumerate(CALC):
        appear(fr, c, W / 2, 620 + i * 110, t, 2.6 + i * 1.3, pop=(i == 2))
    caps(fr, 3, t)

def s5(fr, t, d):
    _pipe_scene(fr, t * 0.6, d, 5.0 + 0.05 * math.sin(t * 9), show_gauge=False)
    gauge(d, W / 2, 520, 130, 5.0 + 0.05 * math.sin(t * 9), col=RED)
    a = ease_out(prog(t, 0.6, 0.3))
    if a > 0:
        d.line((W / 2 - 170, 380, W / 2 + 170, 680), fill=RED, width=int(12 * a) or 1)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H5, W / 2, 200, 1.0); paste(fr, C5, W / 2, 330, ease_out(prog(t, 0.3, 0.4)))
    caps(fr, 4, t)

def s6(fr, t, d):
    fr.paste(push(STEEL, t + 30, 10, 1.0, 1.05), (0, 0))
    # pedal → small piston (master cylinder) → oil pipe → big piston (wheel cylinder)
    p = ease_in_out(prog(t, 3.0, 1.0))
    y = 900
    d.rounded_rectangle((140, y - 40, 340, y + 40), radius=10, fill=(40, 46, 66), outline=(200, 205, 220), width=5)
    d.rectangle((150 + 80 * p, y - 30, 190 + 80 * p, y + 30), fill=(200, 205, 220))
    d.line((60, y - 160, 150 + 80 * p, y), fill=(160, 160, 170), width=14)       # pedal
    d.rectangle((340, y - 14, 760, y + 14), fill=(220, 150, 40))                    # brake oil line
    d.rounded_rectangle((760, y - 110, 960, y + 110), radius=14, fill=(40, 46, 66), outline=(200, 205, 220), width=5)
    d.rectangle((770, y - 100, 810 + 60 * p, y + 100), fill=(200, 205, 220))
    paste(fr, text_img("small A₁", 34, max_w=300, color=CYAN), 240, y + 60, 1.0)
    paste(fr, text_img("large A₂", 34, max_w=300, color=CYAN), 860, y + 130, 1.0)
    paste(fr, text_img("F₂ = F₁ A₂ / A₁", 46, max_w=600, color=YELLOW), W / 2, y + 220, ease_out(prog(t, 4.0, 0.5)))
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H6, W / 2, 190, 1.0)
    appear(fr, LAW_PILL, W / 2, 310, t, 0.3, pop=True)
    appear(fr, LAW_CARD, W / 2, 400, t, 0.5)
    appear(fr, LAW, W / 2, 425, t, 0.6)
    caps(fr, 5, t, y=1360)

def s7(fr, t, d):
    fr.paste(push(STEEL, t + 40, 8, 1.05, 1.08), (0, 0))
    fr.paste(VIG, (0, 0), VIG)
    appear(fr, QUIZ, W / 2, 290, t, 0.0, pop=True)
    appear(fr, PYQ, W / 2, 380, t, 0.6, pop=True)
    appear(fr, Q, W / 2, 470, t, 1.0)
    for i, (c, tx, cx) in enumerate(((OPT_A, TA, 280), (OPT_B, TB, 800))):
        st = 2.6 + i * 0.4
        appear(fr, c, cx, 860, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 905, ease_out(prog(t, st + 0.05, 0.3)))
    appear(fr, CMT, W / 2, 1110, t, 4.2, pop=True)
    appear(fr, FOL, W / 2, 1270, t, 5.6, pop=True)

SCENES = [(S[i], f) for i, f in enumerate((s1, s2, s3, s4, s5, s6, s7))]
VOICE = None
MUSIC = [(0.0, "tension"), (ST[1], "curious"), (ST[4], "tension"), (ST[5], "curious"), (ST[6], "uplift")]
SFX = [(0.0, "whoosh"), (starts[1], "pop"), (ST[0] + S[0] - 2.4, "brake"), (ST[0] + S[0] - 2.0, "thud")]
for s_ in ST[1:-1]: SFX.append((s_ - 0.05, "swoosh"))
SFX += [(ST[2] + 2.0, "brake"), (ST[3] + 2.6, "pop"), (ST[3] + 3.9, "pop"), (ST[3] + 5.2, "ding"), (ST[4] + 0.6, "thud"),
        (ST[5] + 0.3, "pop"), (ST[6] + 0.6, "pop"), (ST[6] + 2.6, "pop"), (ST[6] + 3.0, "pop"), (ST[6] + 1.0, "ticks"), (ST[6] + 5.6, "chime")]
print("total", round(ST[-1], 1), [round(x, 1) for x in S]) if __name__ == "__main__" else None
