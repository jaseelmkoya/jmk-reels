"""Sunday story reel (15 Nov 2026): early winter chill in Kerala's hills.
News: NewsBytes (15 Nov 2026): Idukki dipped to 7.9 °C at Kundala Dam, Munnar 9.7 °C on 14 Nov; reasons given:
weaker winds and clear, stable skies; foggy mornings.
Physics (Plus One Ch10 Thermal Properties of Matter — heat transfer): radiation needs no medium; at night the ground
radiates heat to the sky; clouds absorb it and radiate part back (blanket); clear sky -> heat escapes -> colder night.
No wind -> cold, denser air settles in the valleys (no mixing by convection). Stefan–Boltzmann H = e σ A T⁴.
Quiz (exam favourite, Heat transfer = 14 PYQs): Sun's heat reaches Earth by? A) Convection B) Radiation -> B.
No voice by default: captions word by word at reading pace."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storykit import *
from captions import Captions

random.seed(11)
SRC = source(["NEWSBYTES", "15 NOV 2026"])
BW, BH = int(W * 1.12), int(H * 1.12)
NIGHT = grad(BW, BH, [(0, (4, 8, 26)), (0.5, (12, 22, 52)), (1, (6, 10, 22))])
DAY = grad(BW, BH, [(0, (70, 140, 210)), (0.5, (150, 200, 235)), (1, (60, 110, 80))])
DEEP = grad(BW, BH, [(0, (8, 12, 30)), (1, (3, 6, 16))])
RED2 = (235, 70, 80)
HEAT = (255, 120, 80)
STARS = [(random.uniform(0, BW), random.uniform(0, BH * 0.45), random.uniform(1.5, 3.5), random.uniform(0, 6.3)) for _ in range(90)]
FOG = [(random.uniform(-200, BW), random.uniform(1000, 1250), random.uniform(160, 320)) for _ in range(9)]

def hills(bd, night=True, y0=900):
    cols = [(24, 40, 52), (16, 30, 38), (10, 20, 26)] if night else [(70, 130, 90), (50, 110, 70), (36, 90, 56)]
    for i, (amp, per, ph) in enumerate(((140, 420, 0.3), (110, 330, 1.7), (90, 260, 3.1))):
        yb = y0 + i * 120
        pts = [(x, yb - amp * (0.5 + 0.5 * math.sin(x / per * math.pi + ph))) for x in range(0, BW + 40, 40)]
        bd.polygon(pts + [(BW, BH), (0, BH)], fill=cols[i])
        # tea-garden rows
        for k in range(0, BW, 70):
            yy = yb - amp * (0.5 + 0.5 * math.sin(k / per * math.pi + ph)) + 30
            bd.line((k, yy, k + 40, yy + 10), fill=tuple(c + 14 for c in cols[i]), width=4)

def night_base(t, stars=True, clouds=0.0):
    base = NIGHT.copy(); bd = ImageDraw.Draw(base)
    if stars:
        for x, y, r, ph in STARS:
            b = int(150 + 100 * math.sin(t * 2 + ph))
            bd.ellipse((x - r, y - r, x + r, y + r), fill=(b, b, min(255, b + 30)))
    hills(bd, True)
    return base

def fog(fr, t, a=0.5):
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
    for x, y, r in FOG:
        xx = (x + t * 25) % (W + 400) - 200
        ld.ellipse((xx - r * 1.6, y - r * 0.35, xx + r * 1.6, y + r * 0.35), fill=(200, 210, 230, int(40 * a)))
    fr.paste(L, (0, 0), L)

def thermo(d, cx, top, val, vmin=0, vmax=25, col=CYAN):
    h = 420
    d.rounded_rectangle((cx - 26, top, cx + 26, top + h), radius=26, fill=(20, 26, 44), outline=(220, 225, 240), width=5)
    d.ellipse((cx - 50, top + h - 30, cx + 50, top + h + 70), fill=col, outline=(220, 225, 240), width=5)
    lvl = top + h - (val - vmin) / (vmax - vmin) * (h - 30)
    d.rectangle((cx - 12, lvl, cx + 12, top + h), fill=col)
    for k in range(vmin, vmax + 1, 5):
        yy = top + h - (k - vmin) / (vmax - vmin) * (h - 30)
        d.line((cx + 30, yy, cx + 50, yy), fill=(220, 225, 240), width=3)
    d.text((cx, top - 50), f"{val:.1f}°C", font=font("lat", "bold", 52), fill=col, anchor="mm")

def wavy(d, x1, y1, x2, y2, col, w=7, ph=0.0, amp=12, head=26):
    n = 28; L = math.hypot(x2 - x1, y2 - y1)
    if L < 5: return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L; nx, ny = -uy, ux
    pts = []
    for i in range(n + 1):
        s = i / n
        o = amp * math.sin(s * 6 * math.pi + ph) * min(1, (1 - s) * 4)
        pts.append((x1 + ux * L * s + nx * o, y1 + uy * L * s + ny * o))
    d.line(pts, fill=col, width=w, joint="curve")
    a = math.atan2(uy, ux)
    d.polygon([(x2 + 6 * ux, y2 + 6 * uy), (x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45)),
               (x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45))], fill=col)

def cloud(d, cx, cy, s=1.0, col=(150, 160, 185)):
    for dx, dy, r in ((-90, 10, 60), (-30, -20, 80), (50, -5, 70), (110, 15, 50)):
        d.ellipse((cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s), fill=col)


# ---------- real footage (JMK's clips; frames extracted to CLIPS dir, not committed) ----------
CLIPS = os.environ.get("MC_CLIPS", "/home/claude/clips_mc")
_clip_n = {}
def clip_frame(name, t, speed=1.0):
    d = os.path.join(CLIPS, name)
    if name not in _clip_n: _clip_n[name] = len(os.listdir(d))
    k = min(_clip_n[name], max(1, int(t * speed * 30) + 1))
    return Image.open(os.path.join(d, f"{k:04d}.jpg")).convert("RGB")
TOPSHADE = grad(W, H, [(0, (0, 0, 0)), (1, (0, 0, 0))])
_ta = np.clip(np.concatenate([np.linspace(200, 0, 620), np.zeros(H - 620 - 760), np.linspace(0, 210, 760)]), 0, 255).astype(np.uint8)
TOPSHADE.putalpha(Image.fromarray(np.repeat(_ta[:, None], W, axis=1)))
def night_grade(img, k=0.5):
    a = np.asarray(img).astype(np.float32)
    a = a * np.array([0.45, 0.6, 0.95]) * k * 1.6
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
P_MUN = pin_label("MUNNAR", dot=YELLOW)
P_KUN = pin_label("KUNDALA DAM, IDUKKI", dot=CYAN)

# ---------- text ----------
H1 = headline("KERALA *7.9°C!*", hl=CYAN, size=110)
HOOK = text_img("മേഘമില്ലാത്ത രാത്രി കൂടുതൽ *തണുക്കുന്നത്* എന്തുകൊണ്ട്?", 64, max_w=960, hl=CYAN)
C1 = mono("KUNDALA DAM, IDUKKI 7.9°C · MUNNAR 9.7°C · 14 NOV")
H2 = headline("DAY: SUN *HEATS* US", hl=YELLOW)
C2 = mono("RADIATION NEEDS NO MEDIUM — 15 CRORE KM OF EMPTY SPACE")
H3 = headline("NIGHT: EARTH *RADIATES*", hl=HEAT, size=84)
C3 = mono("THE GROUND LOSES HEAT AS INFRARED RADIATION")
H4 = headline("CLOUDS = *BLANKET*", hl=CYAN)
L_CLOUD = pin_label("CLOUDY", dot=(150, 160, 185))
L_CLEAR = pin_label("CLEAR SKY", dot=CYAN)
H5 = headline("NO WIND = *COLD* VALLEY", hl=CYAN, size=84)
C5 = mono("COLD AIR IS DENSER — IT SINKS AND SETTLES")
H6 = headline("HOTTER = *MORE* RADIATION", hl=YELLOW, size=80)
FORM = text_img("*H = eσAT⁴*", 84, max_w=900, hl=YELLOW)
LAW_PILL = pill("STEFAN–BOLTZMANN LAW", 38, bg=YELLOW)
LAW = text_img("Every body radiates heat. Energy radiated per second is proportional to *T⁴* (absolute temperature).", 46, max_w=880, hl=YELLOW, lh=1.4)
LAW_CARD = card(960, LAW.height + 50)
MODES = [pill("CONDUCTION · needs a medium", 34, bg=(120, 130, 160), fg=WHITE),
         pill("CONVECTION · needs a fluid", 34, bg=(120, 130, 160), fg=WHITE),
         pill("RADIATION · no medium needed", 38, bg=CYAN)]
QUIZ = pill("QUIZ TIME", 44, fg=(9, 14, 38), bg=PINK)
PYQ = pill("Exam favourite · Heat Transfer", 30, fg=WHITE, bg=(80, 60, 160))
Q = text_img("സൂര്യന്റെ *heat* ഭൂമിയിൽ എത്തുന്നത് ഏത് രീതിയിൽ?", 58, max_w=920, hl=YELLOW)
OPT_A = card(480, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(480, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) Convection", 42, max_w=460)
TB = text_img("B) Radiation", 42, max_w=460)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 56, max_w=900, hl=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 56, max_w=900, hl=YELLOW)

# ---------- narration (word by word, reading pace) ----------
LINES = [
    ("Nov 14: Idukki Kundala-യിൽ *7.9°C*, Munnar-ൽ *9.7°C*.", CYAN),
    ("കാരണം: തെളിഞ്ഞ ആകാശം, കാറ്റില്ല. എന്താണ് ഇതിലെ physics?", YELLOW),
    ("പകൽ സൂര്യന്റെ *heat* ഭൂമിയിൽ എത്തുന്നത് *radiation* വഴി — ഒരു *medium* ഇല്ലാതെ.", YELLOW),
    ("രാത്രി ഭൂമി ഈ *heat* *radiation* ആയി തിരികെ ആകാശത്തേക്ക് വിടുന്നു.", ORANGE),
    ("മേഘം ഉണ്ടെങ്കിൽ അത് ഈ *heat* *absorb* ചെയ്ത് ഭൂമിയിലേക്ക് തിരിച്ചു *radiate* ചെയ്യും.", CYAN),
    ("തെളിഞ്ഞ ആകാശത്തിൽ *heat* നേരെ space-ലേക്ക് — ഭൂമി വേഗം തണുക്കുന്നു.", CYAN),
    ("കാറ്റില്ലെങ്കിൽ തണുത്ത, *density* കൂടിയ air താഴ്വരയിൽ കെട്ടിക്കിടക്കും. രാവിലെ മഞ്ഞും.", CYAN),
    ("ഏത് body-യും *heat* *radiate* ചെയ്യും. *T* കൂടുമ്പോൾ *H* വളരെ വേഗം കൂടും (*T⁴*).", YELLOW),
]
PACE = 0.42
def _dur(text, extra): return len(text.split()) * PACE + extra
S = [max(7.5, _dur(LINES[0][0], 1.0) + _dur(LINES[1][0], 1.4)),
     max(6.0, _dur(LINES[2][0], 1.8)),
     max(5.5, _dur(LINES[3][0], 1.6)),
     max(9.0, _dur(LINES[4][0], 0.8) + _dur(LINES[5][0], 1.6)),
     max(6.0, _dur(LINES[6][0], 1.6)),
     max(8.0, _dur(LINES[7][0], 3.5)),
     8.0]
ST = [0.0]
for d_ in S: ST.append(ST[-1] + d_)
starts = [ST[0] + 0.4, ST[0] + 0.4 + _dur(LINES[0][0], 1.0), ST[1] + 0.4, ST[2] + 0.4, ST[3] + 0.3,
          ST[3] + 0.3 + _dur(LINES[4][0], 0.8), ST[4] + 0.4, ST[5] + 0.4]
CAP = Captions([(txt, st, None, hl) for (txt, hl), st in zip(LINES, starts)], None, size=52, wpm_pace=PACE)

def caps(fr, s_idx, t, y=1330):
    CAP.draw(fr, ST[s_idx] + t, y)

EV = dict(cool=0.0, rays=0.6, emit=0.4, split=starts[5] - ST[3], sink=0.8, modes=(4.2, 4.9, 5.6),
          q=1.0, optA=2.6, optB=3.0, cmt=4.2, fol=5.6, pyq=0.6)

# ---------- scenes ----------
SW1 = 3.4   # switch Munnar hills -> Kundala dam
def s1(fr, t, d):
    if t < SW1:
        fr.paste(clip_frame("b_hook", t), (0, 0))
    else:
        cur = clip_frame("a_lake", t - SW1)
        a = prog(t, SW1, 0.35)
        if a < 1: cur = Image.blend(clip_frame("b_hook", t), cur, a)
        fr.paste(cur, (0, 0))
    fr.paste(TOPSHADE, (0, 0), TOPSHADE)
    val = 20 - (20 - 7.9) * ease_in_out(prog(t, EV['cool'], 4.5))
    thermo(d, 900, 720, val)
    if t < SW1: paste(fr, P_MUN, 300, 1080, ease_out(prog(t, 0.5, 0.4)) * (1 - prog(t, SW1 - 0.3, 0.3)))
    else: appear(fr, P_KUN, 380, 1080, t, SW1 + 0.2, pop=True)
    paste(fr, H1, W / 2, 200, 1.0)                                 # hook visible from frame 0
    paste(fr, HOOK, W / 2, 360, 1.0)
    paste(fr, C1, W / 2, 1200, ease_out(prog(t, 0.6, 0.4)))
    paste(fr, SRC, W / 2, 1255, ease_out(prog(t, 0.8, 0.4)))
    caps(fr, 0, t)

def s2(fr, t, d):
    base = DAY.copy(); bd = ImageDraw.Draw(base); hills(bd, False)
    fr.paste(push(base, t, S[1], 1.0, 1.05), (0, 0))
    sx, sy = 230, 560
    for k in range(12):
        a = k * math.pi / 6 + t * 0.4
        d.line((sx + 95 * math.cos(a), sy + 95 * math.sin(a), sx + 130 * math.cos(a), sy + 130 * math.sin(a)), fill=(255, 220, 90), width=8)
    d.ellipse((sx - 80, sy - 80, sx + 80, sy + 80), fill=(255, 210, 80))
    for i in range(4):
        p = ease_out(prog(t, EV['rays'] + i * 0.25, 0.8))
        if p > 0:
            x1, y1 = sx + 90, sy + 60 + i * 20
            x2, y2 = 420 + i * 160, 950 + i * 25
            wavy(d, x1, y1, x1 + (x2 - x1) * p, y1 + (y2 - y1) * p, (255, 200, 60), ph=-t * 8)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H2, W / 2, 200, 1.0); paste(fr, C2, W / 2, 340, ease_out(prog(t, 0.3, 0.4)))
    caps(fr, 1, t)

def s3(fr, t, d):
    fr.paste(push(night_base(t + 8), t, S[2], 1.02, 1.07, 0.5, 0.7), (0, 0))
    for i in range(6):
        p = ease_out(prog(t, EV['emit'] + i * 0.2, 1.2))
        if p > 0:
            x = 120 + i * 170; y1 = 1000 + 40 * math.sin(i)
            wavy(d, x, y1, x, y1 - 520 * p, HEAT, ph=-t * 8 + i)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H3, W / 2, 200, 1.0); paste(fr, C3, W / 2, 330, ease_out(prog(t, 0.3, 0.4)))
    caps(fr, 2, t)

def s4(fr, t, d):
    fr.paste(push(night_base(t + 14, stars=True), t, S[3], 1.0, 1.03), (0, 0))
    # split: left cloudy, right clear
    cf = night_grade(clip_frame("b_cloud", t), 0.75).crop((270, 330, 270 + W // 2, 330 + 800))
    fr.paste(cf, (0, 380))
    d.line((W / 2, 380, W / 2, 1180), fill=(220, 225, 240), width=4)
    for i in range(3):
        x = 110 + i * 110
        p = ease_out(prog(t, 0.6 + i * 0.2, 0.9))
        if p > 0:
            wavy(d, x, 1080, x, 1080 - 420 * p, HEAT, ph=-t * 8 + i)
        q = ease_out(prog(t, 1.6 + i * 0.2, 0.9))
        if q > 0:
            wavy(d, x + 40, 640, x + 40, 640 + 380 * q, (255, 170, 110), ph=-t * 8 + i, w=6)
    st = EV['split']
    for i in range(3):
        x = 660 + i * 130
        p = ease_out(prog(t, st + i * 0.2, 1.4))
        if p > 0:
            wavy(d, x, 1080, x, 1080 - 640 * p, HEAT, ph=-t * 8 + i)
    appear(fr, L_CLOUD, 270, 420, t, 0.4, pop=True)
    appear(fr, L_CLEAR, 810, 420, t, st - 0.3, pop=True)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H4, W / 2, 200, 1.0)
    caps(fr, 3, t)

L_COLD = pin_label("COLD AIR SINKS", dot=(150, 210, 255))
def s5(fr, t, d):
    fr.paste(night_grade(clip_frame("a_dam", t), 0.6), (0, 0))
    fr.paste(TOPSHADE, (0, 0), TOPSHADE)
    for i in range(6):
        p = ease_in_out(prog(t, EV['sink'] + (i % 3) * 0.35, 2.4))
        left = i < 3
        sx = 90 + (i % 3) * 120 if left else W - 90 - (i % 3) * 120
        sy = 640 + (i % 3) * 40
        ex, ey = W / 2 + (-120 + (i % 3) * 60) * (1 if left else -1), 1060
        x, y = sx + (ex - sx) * p, sy + (ey - sy) * p
        dx, dy = ex - sx, ey - sy; L = math.hypot(dx, dy)
        if p > 0.02:
            arrow(d, x - dx / L * 110, y - dy / L * 110, x, y, (150, 210, 255), 10, 32)
    appear(fr, L_COLD, W / 2, 1110, t, 2.4, pop=True)
    fog(fr, t * 1.5, 0.35 * ease_out(prog(t, 1.5, 2.0)) + 0.1)
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H5, W / 2, 200, 1.0); paste(fr, C5, W / 2, 330, ease_out(prog(t, 0.3, 0.4)))
    caps(fr, 4, t)

def s6(fr, t, d):
    fr.paste(push(DEEP, t, S[5], 1.0, 1.05), (0, 0))
    fr.paste(VIG, (0, 0), VIG)
    paste(fr, H6, W / 2, 190, 1.0)
    appear(fr, LAW_PILL, W / 2, 360, t, 0.2, pop=True)
    appear(fr, LAW_CARD, W / 2, 450, t, 0.4)
    appear(fr, LAW, W / 2, 475, t, 0.5)
    appear(fr, FORM, W / 2, 470 + LAW.height + 70, t, 1.2, pop=True)
    for i, m in enumerate(MODES):
        appear(fr, m, W / 2, 920 + i * 110, t, EV['modes'][i], pop=(i == 2))
    caps(fr, 5, t, y=1330)

def s7(fr, t, d):
    fr.paste(push(night_base(t + 40), t, 8, 1.05, 1.08), (0, 0))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 120)); fr.paste(ov, (0, 0), ov)
    fr.paste(VIG, (0, 0), VIG)
    appear(fr, QUIZ, W / 2, 290, t, 0.0, pop=True)
    appear(fr, PYQ, W / 2, 380, t, EV['pyq'], pop=True)
    appear(fr, Q, W / 2, 470, t, EV['q'])
    for i, (c, tx, cx) in enumerate(((OPT_A, TA, 280), (OPT_B, TB, 800))):
        st = (EV['optA'], EV['optB'])[i]
        appear(fr, c, cx, 860, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 905, ease_out(prog(t, st + 0.05, 0.3)))
    appear(fr, CMT, W / 2, 1110, t, EV['cmt'], pop=True)
    appear(fr, FOL, W / 2, 1270, t, EV['fol'], pop=True)

SCENES = [(S[i], f) for i, f in enumerate((s1, s2, s3, s4, s5, s6, s7))]
VOICE = None
MUSIC = [(0.0, "space"), (ST[1], "uplift"), (ST[2], "curious"), (ST[4], "ocean"), (ST[5], "curious"), (ST[6], "tension")]
SFX = [(0.0, "whoosh"), (ST[0] + 4.5, "ding")]
for s_ in ST[1:-1]: SFX.append((s_ - 0.05, "swoosh"))
SFX += [(ST[1] + 0.6, "chime"), (ST[2] + 0.4, "whoosh"), (ST[3] + 0.4, "pop"), (ST[3] + EV['split'] - 0.3, "pop"),
        (ST[4] + 0.8, "whoosh"), (ST[5] + 0.2, "pop"), (ST[5] + 4.2, "pop"), (ST[5] + 4.9, "pop"), (ST[5] + 5.6, "ding"),
        (ST[6] + 0.6, "pop"), (ST[6] + 1.0, "ticks"), (ST[6] + 2.6, "pop"), (ST[6] + 3.0, "pop"), (ST[6] + 5.6, "chime")]
if __name__ == "__main__":
    print("total", round(ST[-1], 1), [round(x, 1) for x in S])
