"""Starship Flight 15 (16 Nov 2026 reel): the launch tower caught Starship (Ship 42) after ~14 orbits.
Story style for a common audience (JMK, 15 Nov 22:58): curiosity questions -> answers, laws explained simply.
News: 13 Nov 22:47 UTC liftoff (Starbase, Texas), ~275 km orbit, 26 Starlink V3 deployed, ~22.5 h flight,
reentry T+22:10, catch by the tower "chopsticks" at T+22:32:34 (14 Nov ~21:20 UTC) — first catch of a ship
returning from orbit. Booster 22 aborted its catch and came down in the Gulf.
Numbers from the SpaceX webcast HUD: 26,794 km/h at 85 km (T+22:10:27); 543 km/h at 10.4 km (T+22:30:52).
Physics: v = sqrt(GM/r) at r = 6371+275 km -> 7.74 km/s; T = 2*pi*r/v -> 90 min.
Footage: SpaceX webcast (JMK's screen recordings), frames extracted to SX_FRAMES (not committed) — see STATUS.md.
No voice by default: captions word by word at reading pace."""
import math, os, sys, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storykit import *
from captions import Captions

random.seed(5)
FR = os.environ.get("SX_FRAMES", "/home/claude/sx/frames")
RED2 = (235, 70, 80)
FIRE = (255, 150, 60)

# ---------- footage ----------
_n = {}
def cf(name, t, speed=1.0, f0=1, f1=None):
    d = os.path.join(FR, name)
    if name not in _n: _n[name] = sorted(os.listdir(d))
    fs = _n[name]; f1 = min(f1 or len(fs), len(fs))
    k = max(f0, min(f1, f0 + int(t * speed * 30)))
    return Image.open(os.path.join(d, fs[k - 1])).convert("RGB")

SHADE = Image.new("RGBA", (W, H), (0, 0, 0, 0))
_a = np.zeros(H)
_a[:560] = np.linspace(205, 0, 560)
_a[1120:] = np.linspace(0, 235, H - 1120)
SHADE.putalpha(Image.fromarray(np.repeat(_a.astype(np.uint8)[:, None], W, axis=1)))

def footage(fr, name, t, dur, speed=1.0, f0=1, f1=None, z0=1.0, z1=1.05, cy=0.5):
    im = cf(name, t, speed, f0, f1)
    fr.paste(push(im, t, dur, z0, z1, 0.5, cy), (0, 0))
    fr.paste(SHADE, (0, 0), SHADE)

def flash(fr, t, at=0.0, d=0.25):
    a = 1 - prog(t, at, d)
    if a > 0.01:
        ov = Image.new("RGBA", (W, H), (255, 255, 255, int(200 * a))); fr.paste(ov, (0, 0), ov)

SPACE = grad(W, H, [(0, (2, 4, 14)), (0.6, (6, 10, 30)), (1, (3, 5, 16))])
STARS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(1, 3), random.uniform(0, 6.3)) for _ in range(120)]
def space_bg(fr, t):
    fr.paste(SPACE, (0, 0)); d = ImageDraw.Draw(fr)
    for x, y, r, ph in STARS:
        b = int(140 + 100 * math.sin(t * 1.5 + ph)); d.ellipse((x - r, y - r, x + r, y + r), fill=(b, b, min(255, b + 30)))

# ---------- story (captions word by word) ----------
PACE = 0.40
SC = [  # (min scene seconds, lead-in, [(line, highlight)])
    (11.3, 5.4, [("ഇത് എങ്ങനെ സാധിച്ചു? ആദ്യം മുതൽ പറയാം…", YELLOW)]),
    (8.0, 0.4, [("നവംബർ 13. Texas-ൽ നിന്ന് ലോകത്തിലെ ഏറ്റവും വലിയ rocket, *Starship*, പൊങ്ങി.", YELLOW),
                ("താഴെയുള്ള *booster*-ൽ മാത്രം *33* engine-കൾ!", ORANGE)]),
    (10.0, 0.4, [("ഇത്രയും ഭാരമുള്ള ഒരു സാധനം എങ്ങനെ മുകളിലേക്ക് പോകുന്നു?", CYAN),
                 ("ഒരു *balloon* വീർപ്പിച്ച് വിട്ടാലോ? Air പുറകോട്ട്, balloon മുന്നോട്ട്!", YELLOW)]),
    (9.0, 0.4, [("Rocket-ഉം അതുപോലെ: ചൂടുള്ള *gas* താഴേക്ക് തള്ളുമ്പോൾ gas rocket-നെ *മുകളിലേക്ക്* തള്ളുന്നു.", ORANGE),
                ("ഇതാണ് Newton's *third* *law.*", YELLOW)]),
    (8.0, 0.4, [("മിനിറ്റുകൾക്കുള്ളിൽ ship *275* *km* ഉയരത്തിൽ, space-ൽ!", CYAN),
                ("അവിടെ അത് താഴെ വീഴാതെ ഭൂമിയെ ചുറ്റി. എന്തുകൊണ്ട് *വീഴുന്നില്ല?*", YELLOW)]),
    (15.0, 0.4, [("സത്യത്തിൽ അത് *വീണുകൊണ്ടിരിക്കുകയാണ്!*", YELLOW),
                 ("പക്ഷേ മുന്നോട്ട് അത്ര വേഗത്തിൽ പോകുന്നതുകൊണ്ട് ഭൂമിയുടെ വളവിനൊപ്പം വീഴുന്നു. ഒരിക്കലും *നിലത്ത്* തട്ടില്ല.", CYAN),
                 ("അതിന് വേണ്ട വേഗം: സെക്കൻഡിൽ *7.7* *km!* Kerala മുഴുവൻ *80* സെക്കൻഡിൽ കടക്കും.", YELLOW),
                 ("ഒരു round = *90* മിനിറ്റ്. 22 മണിക്കൂറിൽ *14* round!", ORANGE)]),
    (5.0, 0.3, [("ഇതിനിടയിൽ *26* *Starlink* internet satellite-കളെയും space-ൽ വിട്ടു.", CYAN)]),
    (16.0, 0.4, [("ഇനിയാണ് ശരിക്കുള്ള പരീക്ഷണം: *തിരിച്ചുവരവ്!*", YELLOW),
                 ("Atmosphere-ൽ കയറുമ്പോൾ വേഗം *26,794* *km/h!* ഈ *പിങ്ക്* വെളിച്ചം കണ്ടോ?", PINK),
                 ("Ship മുന്നിലെ air-നെ ശക്തിയായി ഞെരുക്കുന്നു. Air *1000°C*-ലേറെ ചൂടാകുന്നു. ഇതാണ് *plasma.*", ORANGE),
                 ("Ship-ന്റെ വയറിലെ *heat* *shield* tiles ആണ് അതിനെ കത്താതെ രക്ഷിക്കുന്നത്.", CYAN)]),
    (8.0, 0.4, [("പിന്നെ ship ഒരു *skydiver*-നെപ്പോലെ വയറ് താഴേക്ക് വെച്ച് വീഴുന്നു.", CYAN),
                ("വായുവിന്റെ തടസ്സം (*air* *resistance*) വേഗം *540* *km/h*-ലേക്ക് കുറയ്ക്കുന്നു.", YELLOW)]),
    (12.0, 0.4, [("പക്ഷേ ആ വേഗത്തിൽ tower-ൽ *ഇടിച്ചാൽ?*", RED2),
                 ("അവസാന നിമിഷം engine-കൾ കത്തിച്ച് ship *നിവർന്ന്* നിൽക്കുന്നു.", ORANGE),
                 ("Engine-ന്റെ തള്ളൽ (*thrust*) ship-ന്റെ ഭാരത്തേക്കാൾ കൂടുതൽ → വേഗം കുറഞ്ഞ് ഏകദേശം *പൂജ്യം.*", YELLOW)]),
    (10.0, 0.4, [("അങ്ങനെ tower-ന്റെ രണ്ട് കൈകൾ, *chopsticks*, ship-നെ വായുവിൽ വെച്ച് *പിടിച്ചു!*", YELLOW),
                 ("Space-ൽ നിന്ന് വന്ന ship-നെ ഇങ്ങനെ പിടിക്കുന്നത് ചരിത്രത്തിൽ *ആദ്യമായി!*", CYAN)]),
    (12.0, 0.4, [("എന്തിനാണ് ഈ പാട്? ഒരു വിമാനം ഒരു യാത്ര കഴിഞ്ഞ് *കളഞ്ഞാൽ* ticket-ന് എത്ര രൂപയാകും?", CYAN),
                 ("Rocket വീണ്ടും വീണ്ടും പറത്താൻ പറ്റിയാൽ space യാത്രയുടെ ചെലവ് *വൻതോതിൽ* കുറയും.", YELLOW),
                 ("(ഇത്തവണ താഴത്തെ booster-നെ പിടിക്കാൻ പറ്റിയില്ല, അത് കടലിൽ *വീണു.*)", RED2)]),
    (9.0, 0.0, []),
]
S, ST, CAPL = [], [0.0], []
for mn, lead, lines in SC:
    t = ST[-1] + lead
    for txt, hl in lines:
        CAPL.append((txt, t, None, hl)); t += len(txt.split()) * PACE + 1.1
    d = max(mn, t - ST[-1] + 0.4)
    S.append(round(d, 2)); ST.append(ST[-1] + d)
CAP = Captions(CAPL, None, size=52, wpm_pace=PACE)
def caps(fr, i, t, y=1330): CAP.draw(fr, ST[i] + t, y)
def line_at(i, k):                      # start of the k-th caption line of scene i (scene time)
    return [c[1] for c in CAPL if ST[i] <= c[1] < ST[i + 1]][k] - ST[i]

# ---------- text layers ----------
H1 = text_img("Rocket-നെ tower *പിടിച്ചു!*", 84, max_w=1000, hl=YELLOW)
HOOK = text_img("ഭൂമിയെ *14* തവണ ചുറ്റിവന്ന rocket-നെ ഒരു tower *കൈകൊണ്ട്* പിടിച്ചു!", 62, max_w=960, hl=YELLOW)
TAG = pill("STARSHIP · 14 NOV 2026", 30, bg=CYAN)
H2 = headline("STARSHIP · *FLIGHT 15*", hl=ORANGE)
P33 = pill("33 ENGINES", 40, bg=ORANGE)
H3 = text_img("എങ്ങനെ *പൊങ്ങുന്നു?*", 84, max_w=1000, hl=CYAN)
H4 = headline("ACTION = *REACTION*", hl=ORANGE)
LAW_PILL = pill("NEWTON'S THIRD LAW", 36, bg=YELLOW)
LAW = text_img("To every action, there is an equal and *opposite* reaction.", 46, max_w=900, hl=YELLOW, lh=1.35)
LAW_CARD = card(960, LAW.height + 50, fill=(9, 14, 38, 190))
L_GAS = pill("GAS ↓  (action)", 34, bg=FIRE)
L_UP = pill("ROCKET ↑  (reaction)", 34, bg=CYAN)
H5 = headline("WELCOME TO *SPACE*", hl=CYAN)
H6 = text_img("എന്തുകൊണ്ട് *വീഴുന്നില്ല?*", 80, max_w=1000, hl=YELLOW)
FORM = text_img("*v = √(GM/r)* ≈ 7.7 km/s", 56, max_w=900, hl=YELLOW)
FORM_CARD = card(760, 120, fill=(9, 14, 38, 200))
P90 = pill("1 ROUND ≈ 90 MIN", 36, bg=ORANGE)
H7 = headline("26 *STARLINK*", hl=CYAN)
H8 = headline("26,794 *KM/H*", hl=PINK, size=100)
KE = pill("KINETIC ENERGY → HEAT", 36, bg=PINK)
H9 = headline("SKYDIVER *MODE*", hl=CYAN)
P540 = pill("10 KM ഉയരം · 540 KM/H", 34, bg=CYAN)
H10 = headline("THRUST > *WEIGHT*", hl=ORANGE)
L_T = pill("THRUST ↑", 36, bg=FIRE)
L_W = pill("WEIGHT ↓", 36, bg=(200, 210, 230))
FMA = text_img("Net force ↑  →  *speed ↓*   (F = ma)", 44, max_w=950, hl=YELLOW)
FMA_CARD = card(960, 100, fill=(9, 14, 38, 200))
H11 = headline("MECHAZILLA *CATCH!*", hl=YELLOW)
FIRST = pill("WORLD FIRST", 40, bg=YELLOW)
H12 = headline("REUSE = *CHEAP* SPACE", hl=YELLOW, size=88)
QUIZ = pill("QUIZ TIME", 44, fg=(9, 14, 38), bg=PINK)
TOPIC = pill("Plus One · Laws of Motion", 30, fg=WHITE, bg=(80, 60, 160))
Q = text_img("Rocket മുകളിലേക്ക് പൊങ്ങുന്നത് ഏത് *law* അനുസരിച്ചാണ്?", 58, max_w=920, hl=YELLOW)
OPT_A = card(480, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(480, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) Newton's first law", 38, max_w=440)
TB = text_img("B) Newton's third law", 38, max_w=440)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 56, max_w=900, hl=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 56, max_w=900, hl=YELLOW)

# frame windows (30 fps) inside each extracted clip, avoiding app UI / split screens
CD = (4, 433)      # catch_desc: ship coming down with engines lit (T+22:32:14 → 22:32:28)
LC = (10, 213)     # lift_close
LS = (1, 310)      # lift_sky
PA = (17, 736)     # plasma_a
SL = (25, 124)     # starlink

# ---------- scenes ----------
HKB = 1.4
QT = dict(q=1.0, a=2.6, b=3.0, cmt=4.2, fol=5.6)
HK = 2.8                                            # 2.8 s cold-open hook before the title card
HOOKA = boxed(text_img("ഇത് *സിനിമയല്ല!*", 112, max_w=1000, hl=YELLOW), 26, (9, 14, 38, 200))
HOOKA2 = pill("REAL FOOTAGE · SPACEX", 36, bg=CYAN)
HOOKB = boxed(text_img("*26,794 km/h*-ൽ space-ൽ നിന്ന് വീഴുന്ന rocket…", 70, max_w=940, hl=YELLOW), 26, (9, 14, 38, 200))
def hook(fr, t):
    if t < HKB:
        footage(fr, "catch_desc", t, HKB, 1.2, 370, CD[1], 1.1, 1.0)
        paste(fr, HOOKA, W / 2, 230, 1.0, 1.08 - 0.08 * ease_out(prog(t, 0, 0.25)))
        appear(fr, HOOKA2, W / 2, 450, t, 0.35, pop=True)
    else:
        footage(fr, "plasma_b", t - HKB, HK - HKB, 2.2, 400, None, 1.1, 1.0)
        flash(fr, t, HKB, 0.15)
        paste(fr, HOOKB, W / 2, 680, 1.0, 1.15 - 0.15 * ease_out(prog(t, HKB, 0.25)))

def s0(fr, t, d):                                   # HOOK, then the catch
    if t < HK:
        hook(fr, t); return
    t -= HK
    if t < 3.6:
        footage(fr, "catch_hold", t, 3.6, 0.6, 1, None, 1.0, 1.06)
    else:
        footage(fr, "catch_close", t - 3.6, S[0] - 3.6, 0.9, 1, None, 1.0, 1.05)
        flash(fr, t, 3.6, 0.2)
    flash(fr, t, 0.0, 0.2)
    paste(fr, H1, W / 2, 170, 1.0)
    paste(fr, HOOK, W / 2, 320, 1.0)
    appear(fr, TAG, W / 2, 1180, t, 1.0, pop=True)
    caps(fr, 0, t + HK)

def s1(fr, t, d):                                   # liftoff
    if t < 5.5: footage(fr, "lift_close", t, 5.5, 1.0, LC[0], LC[1], 1.0, 1.04)
    else: footage(fr, "lift_aerial", t - 5.5, S[1] - 5.5, 1.0, 1, None, 1.0, 1.04)
    paste(fr, H2, W / 2, 170, 1.0)
    appear(fr, P33, W / 2, 1180, t, line_at(1, 1) + 0.6, pop=True)
    caps(fr, 1, t)

def balloon(d, cx, cy, t, k):
    """Animated balloon moving right while air rushes out left (third law)."""
    x = cx + 260 * ease_in_out(clamp(k))
    d.ellipse((x - 120, cy - 90, x + 120, cy + 90), fill=(235, 70, 80), outline=(255, 160, 160), width=6)
    d.polygon([(x - 120, cy), (x - 150, cy - 18), (x - 150, cy + 18)], fill=(200, 50, 60))
    for i in range(6):
        ph = (t * 3 + i * 0.37) % 1
        xx = x - 160 - ph * 260; a = int(255 * (1 - ph))
        d.line((xx, cy - 30 + i * 12, xx - 50, cy - 30 + i * 12), fill=(150, 220, 255, a), width=6)
    arrow(d, x + 140, cy, x + 280, cy, YELLOW, 12, 36)
    arrow(d, x - 170, cy + 130, x - 330, cy + 130, CYAN, 12, 36)

L_AIR = pill("AIR ←", 32, bg=CYAN)
L_BAL = pill("BALLOON →", 32, bg=YELLOW)
def s2(fr, t, d):                                   # question + balloon animation
    t2 = line_at(2, 1) - 0.3
    if t < t2:
        footage(fr, "lift_aerial", t, t2, 0.7, 60, None, 1.02, 1.08)
    else:
        space_bg(fr, t); d = ImageDraw.Draw(fr)
        k = prog(t, t2 + 0.6, 3.0)
        balloon(d, 300, 820, t, k)
        appear(fr, L_AIR, 300, 1010, t, t2 + 1.0, pop=True)
        appear(fr, L_BAL, 760, 640, t, t2 + 1.4, pop=True)
        flash(fr, t, t2, 0.2)
    paste(fr, H3, W / 2, 170, 1.0)
    caps(fr, 2, t)

def s3(fr, t, d):                                   # third law over the climbing rocket
    footage(fr, "lift_sky", t, S[3], 0.8, LS[0], LS[1], 1.0, 1.04)
    d = ImageDraw.Draw(fr)
    paste(fr, H4, W / 2, 170, 1.0)
    p = ease_out(prog(t, 0.6, 0.8))
    if p > 0:
        arrow(d, 150, 760, 150, 760 + 300 * p, FIRE, 14, 40)
        arrow(d, W - 150, 1060, W - 150, 1060 - 300 * p, CYAN, 14, 40)
    appear(fr, L_GAS, 260, 1090, t, 0.8, pop=True)
    appear(fr, L_UP, W - 270, 690, t, 1.2, pop=True)
    la = line_at(3, 1) - 0.2
    appear(fr, LAW_PILL, W / 2, 330, t, la, pop=True)
    appear(fr, LAW_CARD, W / 2, 410, t, la + 0.2)
    appear(fr, LAW, W / 2, 432, t, la + 0.3)
    caps(fr, 3, t)

def s4(fr, t, d):                                   # in space (onboard view)
    footage(fr, "earth_flap", t, S[4], 0.75, 1, None, 1.0, 1.06)
    paste(fr, H5, W / 2, 170, 1.0)
    caps(fr, 4, t)

def s5(fr, t, d):                                   # Newton's cannon / orbit animation
    space_bg(fr, t); d = ImageDraw.Draw(fr)
    cx, cy, R = W / 2, 900, 250
    # earth
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(30, 90, 170), outline=(120, 200, 255), width=5)
    for ax, ay, ar in ((-80, -60, 90), (60, 70, 70), (-20, 120, 50), (110, -110, 55)):
        d.ellipse((cx + ax - ar, cy + ay - ar * 0.7, cx + ax + ar, cy + ay + ar * 0.7), fill=(60, 150, 80))
    top = (cx, cy - R - 10)
    l1, l2, l3 = (line_at(5, k) for k in range(3))
    # Newton's cannon: slow throws fall back to the ground, the fast one never lands
    for i, (phi, col) in enumerate(((0.45, (200, 210, 230)), (0.95, (255, 200, 120)))):
        p = prog(t, 0.5 + i * 1.4, 1.2)
        if p > 0:
            pts = []
            for k in range(41):
                a = phi * p * k / 40
                r = R + 70 * (1 - (a / phi) ** 2)
                pts.append((cx + r * math.sin(a), cy - r * math.cos(a)))
            d.line(pts, fill=col, width=6)
            if p >= 1:
                x, y = pts[-1]; d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=RED2)
    d.rectangle((cx - 10, cy - R - 70, cx + 10, cy - R), fill=(200, 200, 210))
    # orbit (fast) — ship goes round and round
    po = prog(t, l1 - 0.2, 0.01)
    if po > 0:
        orb = R + 120
        d.ellipse((cx - orb, cy - orb, cx + orb, cy + orb), outline=(120, 200, 255, 120), width=3)
        ang = (t - l1) * 1.4
        sx, sy = cx + orb * math.sin(ang), cy - orb * math.cos(ang)
        d.ellipse((sx - 16, sy - 16, sx + 16, sy + 16), fill=YELLOW)
        # velocity arrow (tangent) and gravity arrow (to centre)
        tx, ty = math.cos(ang), math.sin(ang)
        arrow(d, sx, sy, sx + tx * 120, sy + ty * 120, YELLOW, 8, 26)
        arrow(d, sx, sy, sx + (cx - sx) * 0.3, sy + (cy - sy) * 0.3, CYAN, 8, 26)
        n = min(14, 1 + int(max(0, t - l3) / 0.25)) if t > l3 else 1
        rnd = text_img(f"ROUND *{n}*", 52, max_w=500, hl=YELLOW)
        paste(fr, rnd, W / 2, cy - 30, 1.0)
    paste(fr, H6, W / 2, 170, 1.0)
    appear(fr, FORM_CARD, W / 2, 330, t, l2 - 0.2)
    appear(fr, FORM, W / 2, 350, t, l2)
    appear(fr, P90, W / 2, 470, t, l3, pop=True)
    caps(fr, 5, t)

def s6(fr, t, d):                                   # Starlink
    footage(fr, "starlink", t, S[6], 0.65, SL[0], SL[1], 1.0, 1.05)
    paste(fr, H7, W / 2, 170, 1.0)
    caps(fr, 6, t)

def s7(fr, t, d):                                   # reentry plasma
    k = 0.9
    if t < 8.0: footage(fr, "plasma_a", t, 8.0, k, PA[0], PA[1], 1.0, 1.05)
    else: footage(fr, "plasma_b", t - 8.0, S[7] - 8.0, k, 1, None, 1.0, 1.05)
    paste(fr, H8, W / 2, 170, 1.0)
    appear(fr, KE, W / 2, 330, t, line_at(7, 2), pop=True)
    caps(fr, 7, t)

def s8(fr, t, d):                                   # belly flop
    footage(fr, "belly", t, S[8], 100 / 30 / S[8], 1, None, 1.0, 1.08)
    paste(fr, H9, W / 2, 170, 1.0)
    appear(fr, P540, W / 2, 330, t, line_at(8, 1) + 0.5, pop=True)
    caps(fr, 8, t)

def s9(fr, t, d):                                   # flip + landing burn
    sp = (CD[1] - CD[0]) / 30 / S[9]
    footage(fr, "catch_desc", t, S[9], sp, CD[0], CD[1], 1.0, 1.05)
    d = ImageDraw.Draw(fr)
    paste(fr, H10, W / 2, 170, 1.0)
    l3 = line_at(9, 2)
    p = ease_out(prog(t, l3, 0.8))
    if p > 0:
        arrow(d, 170, 1000, 170, 1000 - 280 * p, FIRE, 16, 44)
        arrow(d, W - 170, 720, W - 170, 720 + 160 * p, (200, 210, 230), 12, 36)
    appear(fr, L_T, 230, 1030, t, l3 + 0.2, pop=True)
    appear(fr, L_W, W - 230, 640, t, l3 + 0.4, pop=True)
    appear(fr, FMA_CARD, W / 2, 330, t, l3 + 1.5)
    appear(fr, FMA, W / 2, 352, t, l3 + 1.6)
    caps(fr, 9, t)

def s10(fr, t, d):                                  # the catch
    if t < 5.0: footage(fr, "catch_close", t, 5.0, 165 / 30 / 5.0, 1, None, 1.0, 1.04)
    else: footage(fr, "catch_hold", t - 5.0, S[10] - 5.0, 0.8, 1, None, 1.0, 1.05)
    flash(fr, t, 5.0, 0.15)
    paste(fr, H11, W / 2, 170, 1.0)
    appear(fr, FIRST, W / 2, 330, t, line_at(10, 1), pop=True)
    caps(fr, 10, t)

def s11(fr, t, d):                                  # why it matters
    l2 = line_at(11, 1) - 0.3
    if t < l2: footage(fr, "catch_hold", t, l2, 0.55, 1, None, 1.02, 1.10, cy=0.4)
    else:
        footage(fr, "lift_close", t - l2, S[11] - l2, 0.6, LC[0], LC[1], 1.0, 1.05)
        flash(fr, t, l2, 0.2)
    paste(fr, H12, W / 2, 170, 1.0)
    caps(fr, 11, t)

def s12(fr, t, d):                                  # quiz
    footage(fr, "lift_sky", t, S[12], 0.5, 120, LS[1], 1.05, 1.1)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 150)); fr.paste(ov, (0, 0), ov)
    appear(fr, QUIZ, W / 2, 290, t, 0.0, pop=True)
    appear(fr, TOPIC, W / 2, 380, t, 0.5, pop=True)
    appear(fr, Q, W / 2, 470, t, QT["q"])
    for i, (c, tx, cx) in enumerate(((OPT_A, TA, 280), (OPT_B, TB, 800))):
        st = (QT["a"], QT["b"])[i]
        appear(fr, c, cx, 860, t, st, pop=True)
        if t > st + 0.1: paste(fr, tx, cx, 905, ease_out(prog(t, st + 0.05, 0.3)))
    appear(fr, CMT, W / 2, 1110, t, QT["cmt"], pop=True)
    appear(fr, FOL, W / 2, 1270, t, QT["fol"], pop=True)

FNS = (s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12)
SCENES = [(S[i], f) for i, f in enumerate(FNS)]
VOICE = None
MUSIC = [(0.0, "hype"), (ST[1], "cinematic"), (ST[4], "space"), (ST[7], "tension"), (ST[9], "hype"), (ST[11], "uplift")]
MUSIC_GAIN = 0.45
SFX = [(0.0, "thud"), (0.05, "whoosh"), (HKB, "whoosh"), (HK, "ding"), (HK + 3.6, "pop")]
for s_ in ST[1:-1]: SFX.append((s_ - 0.05, "swoosh"))
SFX += [(ST[1] + line_at(1, 1) + 0.6, "pop"), (ST[3] + 0.8, "pop"), (ST[3] + 1.2, "pop"), (ST[5] + line_at(5, 2), "ding"),
        (ST[7] + line_at(7, 2), "pop"), (ST[9] + line_at(9, 2), "pop"), (ST[10] + 0.2, "chime"), (ST[10] + line_at(10, 1), "ding"),
        (ST[12] + 0.05, "pop"), (ST[12] + 1.0, "ticks"), (ST[12] + 2.6, "pop"), (ST[12] + 3.0, "pop"), (ST[12] + 5.6, "chime")]
if __name__ == "__main__":
    print("total", round(ST[-1], 1), [round(x, 1) for x in S])
