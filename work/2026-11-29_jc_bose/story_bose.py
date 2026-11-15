"""Sunday story (29 Nov 2026, day before J.C. Bose's birthday): 1895, Presidency College Calcutta — Bose sends
60 GHz (λ = 5 mm) EM waves over 23 m through two walls, rings a bell and fires gunpowder. ~2 years before Marconi.
No patent (knowledge should be free). IEEE Milestone 2012. Plus Two Ch8 EM waves: c = fλ, microwaves → RADAR.
Cinematic: Google Flow (Omni 1.2 Flash) clips as backgrounds (frames in CLIPDIR/f1..f7, not committed),
exact text drawn by us. Bose never shown face-on. No voice by default: captions word by word at reading pace."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storykit import *
from captions import Captions
from PIL import ImageEnhance

CLIPDIR = os.environ.get("BOSE_CLIPS", "/home/claude/bose/clips")
# f1 lecture hall London · f2 notebooks+candle · f3 silhouettes · f4 bell · f5 corridor through walls · f6 hands+transmitter · f7 lab sparks
_files = {}
def clip(fr, k, t, d, z0=1.0, z1=1.07, speed=1.0, dim=0.82, start=0.0):
    if k not in _files:
        _files[k] = sorted(os.listdir(os.path.join(CLIPDIR, f"f{k}")))
    fs = _files[k]
    i = min(len(fs) - 1, int((start + t * speed) * 30))
    im = Image.open(os.path.join(CLIPDIR, f"f{k}", fs[i])).convert("RGB")
    p = ease_in_out(clamp(t / d)); z = z0 + (z1 - z0) * p
    if z > 1.001:
        w, h = int(W / z), int(H / z)
        im = im.crop(((W - w) // 2, (H - h) // 2, (W - w) // 2 + w, (H - h) // 2 + h)).resize((W, H), Image.BILINEAR)
    if dim < 1: im = ImageEnhance.Brightness(im).enhance(dim)
    fr.paste(im, (0, 0))
    fr.paste(SHADE, (0, 0), SHADE)

# dark gradient behind top headline and bottom captions
import numpy as np
_a = np.zeros((H, 1), np.float32)
ys = np.arange(H)
_a[:, 0] = np.clip(np.maximum((420 - ys) / 420 * 170, (ys - 1080) / 560 * 215), 0, 215)
SHADE = Image.new("RGBA", (W, H), (0, 0, 0, 0)); SHADE.putalpha(Image.fromarray(np.repeat(_a, W, 1).astype(np.uint8)))

RED = (235, 70, 80)
H1 = headline("BEFORE *MARCONI*", 96, hl=YELLOW)
C1 = mono("KOLKATA · 1895 · PRESIDENCY COLLEGE")
H3 = headline("23 m · *2 WALLS*", 92, hl=CYAN)
H4 = headline("*NO* WIRES!", 100, hl=RED)
H5 = headline("INVISIBLE *WAVES*", 92, hl=CYAN)
H6 = text_img("c = f *λ*", 100, hl=YELLOW)
H7 = headline("NO *PATENT*", 100, hl=RED)
H8 = headline("IEEE *MILESTONE*", 92, hl=YELLOW)
C8 = mono("FIRST MILLIMETRE-WAVE COMMUNICATION · 2012")
SRC = source(["IEEE MILESTONE", "ETHW", "THEPRINT"])
NAME = text_img("ജഗദീഷ് ചന്ദ്ര ബോസ്", 74, color=YELLOW)
YEARS = mono("30 NOV 1858 – 23 NOV 1937")

LINES = [
    ("1895. Marconi radio കണ്ടുപിടിക്കുന്നതിന് രണ്ട് വർഷം മുമ്പ്…", YELLOW),
    ("Kolkata-യിലെ Presidency College-ൽ ഒരു ഇന്ത്യൻ ശാസ്ത്രജ്ഞൻ ഒരു *spark* *transmitter* ഓൺ ചെയ്തു.", YELLOW),
    ("*23* *metre* അകലെ, *രണ്ട്* *ചുവരുകൾക്കപ്പുറം…*", CYAN),
    ("ഒരു *മണി* തനിയെ മുഴങ്ങി! ഒരു ചെറിയ *gunpowder* പൊട്ടിത്തെറിച്ചു!", RED),
    ("ആരും ഒന്നും തൊട്ടില്ല. ചുവരുകൾ കടന്നത് കണ്ണിന് കാണാനാവാത്ത *electromagnetic* *waves.*", CYAN),
    ("Wavelength വെറും *5* *mm.* Frequency ഏകദേശം *60* *GHz* — *microwaves!* ഇന്ന് *5G*-യും *car* *radar*-ഉം ഉപയോഗിക്കുന്ന അതേ waves!", YELLOW),
    ("പക്ഷേ ബോസ് *patent* എടുത്തില്ല. അറിവ് *എല്ലാവർക്കുമുള്ളതാണ്* എന്നായിരുന്നു അദ്ദേഹത്തിന്റെ വിശ്വാസം.", RED),
    ("1897-ൽ London-ലെ Royal Institution-ൽ പോലും അദ്ദേഹം ഇത് കാണിച്ചു. പക്ഷേ radio-യുടെ ക്രെഡിറ്റ് *Marconi*-ക്ക് പോയി.", YELLOW),
    ("2012-ൽ *IEEE* ബോസിന്റെ പരീക്ഷണത്തെ ലോകത്തിലെ ആദ്യ *millimetre-wave* *communication* ആയി അംഗീകരിച്ചു.", YELLOW),
]
PACE = 0.42
def _dur(text, extra): return len(text.split()) * PACE + extra
S = [max(5.6, _dur(LINES[0][0], 2.2)),   # s1 lab sparks
     max(6.6, _dur(LINES[1][0], 2.6)),   # s2 hands + name
     max(4.6, _dur(LINES[2][0], 2.4)),   # s3 corridor through walls
     max(5.0, _dur(LINES[3][0], 1.8)),   # s4 bell
     max(6.0, _dur(LINES[4][0], 1.6)),   # s5 silhouettes
     max(11.0, _dur(LINES[5][0], 4.4)),  # s6 physics card
     max(6.8, _dur(LINES[6][0], 1.6)),   # s7 notebooks
     max(7.6, _dur(LINES[7][0], 1.4)),   # s8 London lecture
     max(7.0, _dur(LINES[8][0], 2.2)),   # s9 milestone
     8.5]                                # s10 quiz
ST = [0.0]
for d_ in S: ST.append(ST[-1] + d_)
starts = [ST[0] + 0.5, ST[1] + 0.3, ST[2] + 0.3, ST[3] + 0.2, ST[4] + 0.3, ST[5] + 0.6, ST[6] + 0.3, ST[7] + 0.3, ST[8] + 0.4]
CAP = Captions([(txt, st, None, hl) for (txt, hl), st in zip(LINES, starts)], None, size=54, wpm_pace=PACE)
def caps(fr, s_idx, t, y=1300):
    CAP.draw(fr, ST[s_idx] + t, y)

def top(fr, h, t, at=0.1, sub=None):
    p = ease_out(prog(t, at, 0.5))
    paste(fr, h, W / 2, 200 + (1 - p) * 30, p)
    if sub is not None: paste(fr, sub, W / 2, 350, ease_out(prog(t, at + 0.35, 0.5)))

# ---------- scenes ----------
def s1(fr, t, d):
    clip(fr, 7, t, S[0], 1.0, 1.10)
    paste(fr, H1, W / 2, 200, 1.0)                     # hook visible on frame 0
    paste(fr, C1, W / 2, 350, ease_out(prog(t, 0.3, 0.5)))
    caps(fr, 0, t)

def s2(fr, t, d):
    clip(fr, 6, t, S[1], 1.04, 1.12, speed=0.95)
    appear(fr, NAME, W / 2, 230, t, 2.4)
    appear(fr, YEARS, W / 2, 360, t, 2.8)
    caps(fr, 1, t)

def s3(fr, t, d):
    clip(fr, 5, t, S[2], 1.0, 1.0, speed=8.0 / S[2] * 0.95)  # whole fly-through inside the scene
    top(fr, H3, t)
    caps(fr, 2, t)

def s4(fr, t, d):
    clip(fr, 4, t, S[3], 1.0, 1.12, start=1.0)
    top(fr, H4, t, 0.6)
    if 1.2 < t < 1.6:                                  # tiny gunpowder flash
        a = 1 - abs(t - 1.4) / 0.2
        fl = Image.new("RGBA", (W, H), (255, 230, 170, int(90 * a))); fr.paste(fl, (0, 0), fl)
    caps(fr, 3, t)

def s5(fr, t, d):
    clip(fr, 3, t, S[4], 1.0, 1.08)
    top(fr, H5, t)
    caps(fr, 4, t)

WAVEBG = grad(W, H, [(0, (6, 10, 26)), (0.6, (12, 18, 40)), (1, (4, 6, 14))])
EQ1 = text_img("λ = 5 mm = 5 × 10⁻³ m", 64, color=WHITE)
EQ2 = text_img("f = c / λ = (3 × 10⁸) / (5 × 10⁻³)", 58, color=WHITE)
EQ3 = text_img("f = 6 × 10¹⁰ Hz ≈ *60 GHz*", 66, hl=YELLOW)
MW = pill("MICROWAVES", 44, bg=YELLOW)
P5G = pill("5G", 40, bg=CYAN); PRAD = pill("CAR RADAR", 40, bg=CYAN); PRDR = pill("RADAR", 40, bg=CYAN)
def s6(fr, t, d):
    fr.paste(WAVEBG, (0, 0))
    dd = ImageDraw.Draw(fr)
    # travelling EM wave: E (yellow) and B (cyan), lambda bracket
    lam = 260; y0 = 560; ph = t * 2.2 * math.pi
    for k in range(0, W, 6):
        x = k; e = math.sin(2 * math.pi * x / lam - ph)
        dd.ellipse((x - 3, y0 - 120 * e - 3, x + 3, y0 - 120 * e + 3), fill=YELLOW)
        dd.ellipse((x - 2, y0 + 50 * e * 0.6 - 2, x + 2, y0 + 50 * e * 0.6 + 2), fill=CYAN)
    dd.line((0, y0, W, y0), fill=(120, 130, 160), width=2)
    a = ease_out(prog(t, 0.6, 0.5))
    if a > 0:
        x1 = (ph / (2 * math.pi) * lam) % lam + 100
        dd.line((x1, y0 + 170, x1 + lam, y0 + 170), fill=(255, 255, 255, int(255 * a)), width=4)
        for xx in (x1, x1 + lam): dd.line((xx, y0 + 150, xx, y0 + 190), fill=WHITE, width=4)
        dd.text((x1 + lam / 2, y0 + 215), "λ", font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52), fill=WHITE, anchor="mm")
    top(fr, H6, t, 0.0)
    appear(fr, EQ1, W / 2, 840, t, 1.0)
    appear(fr, EQ2, W / 2, 940, t, 2.4)
    appear(fr, EQ3, W / 2, 1040, t, 3.8, pop=True)
    appear(fr, MW, W / 2, 1160, t, 4.6, pop=True)
    for i, (pl, x) in enumerate(((P5G, 250), (PRAD, 540), (PRDR, 830))):
        appear(fr, pl, x, 1240, t, 6.2 + i * 0.3, pop=True)
    caps(fr, 5, t, y=1340)

def s7(fr, t, d):
    clip(fr, 2, t, S[6], 1.0, 1.10)
    top(fr, H7, t, 0.4)
    caps(fr, 6, t)

def s8(fr, t, d):
    clip(fr, 1, t, S[7], 1.0, 1.08)
    paste(fr, mono("LONDON · ROYAL INSTITUTION · 1897"), W / 2, 220, ease_out(prog(t, 0.2, 0.5)))
    caps(fr, 7, t)

def s9(fr, t, d):
    clip(fr, 6, t, S[8], 1.12, 1.18, speed=0.4, dim=0.5, start=3.0)
    top(fr, H8, t, 0.1, C8)
    paste(fr, SRC, W / 2, 470, ease_out(prog(t, 0.8, 0.5)))
    caps(fr, 8, t)

STEEL = grad(int(W * 1.12), int(H * 1.12), [(0, (10, 16, 30)), (1, (4, 8, 18))])
QUIZ = pill("QUIZ", 44, bg=YELLOW)
PYQ = pill("Plus Two exam favourite · EM Waves", 32, bg=CYAN)
Q = text_img("*RADAR*-ൽ ഉപയോഗിക്കുന്ന electromagnetic wave ഏതാണ്?", 60, max_w=940)
OPT_A = card(420, 150); OPT_B = card(420, 150)
TA = text_img("A) Microwaves", 54); TB = text_img("B) Gamma rays", 54)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 56)
FOL = pill("Follow ചെയ്യൂ", 52, bg=YELLOW)
def s10(fr, t, d):
    fr.paste(push(STEEL, t + 40, 8, 1.05, 1.08), (0, 0))
    fr.paste(VIG, (0, 0), VIG)
    appear(fr, QUIZ, W / 2, 290, t, 0.0, pop=True)
    appear(fr, PYQ, W / 2, 380, t, 0.5, pop=True)
    appear(fr, Q, W / 2, 480, t, 1.0)
    for i, (c, tx, cx) in enumerate(((OPT_A, TA, 280), (OPT_B, TB, 800))):
        st = (2.6, 3.0)[i]
        appear(fr, c, cx, 860, t, st, pop=True)
        if t > st + 0.1: paste(fr, tx, cx, 905, ease_out(prog(t, st + 0.05, 0.3)))
    appear(fr, CMT, W / 2, 1110, t, 4.2, pop=True)
    appear(fr, FOL, W / 2, 1270, t, 5.6, pop=True)

SCENES = [(S[i], f) for i, f in enumerate((s1, s2, s3, s4, s5, s6, s7, s8, s9, s10))]
VOICE = None
MUSIC = [(0.0, "cinematic"), (ST[2], "tension"), (ST[5], "electric"), (ST[6], "cinematic"), (ST[8], "uplift")]
# Flow clips carry their own sound (sparks, bell, whooshes, room tone) — mixed in by the post step, so no synthetic zaps/bells here
FLOW_AUDIO = True
SFX = [(0.0, "whoosh"), (ST[2] - 0.05, "swoosh"), (ST[3] + 1.4, "pop"),
       (ST[4] - 0.05, "swoosh"), (ST[5] - 0.05, "whoosh"), (ST[5] + 3.8, "ding"), (ST[5] + 4.6, "pop"),
       (ST[6] - 0.05, "swoosh"), (ST[6] + 0.4, "thud"), (ST[7] - 0.05, "swoosh"), (ST[8] + 0.2, "chime"),
       (ST[9], "pop"), (ST[9] + 1.0, "ticks"), (ST[9] + 2.6, "pop"), (ST[9] + 3.0, "pop"), (ST[9] + 5.6, "chime")]
if __name__ == "__main__":
    print("total", round(ST[-1], 1), [round(x, 1) for x in S])
