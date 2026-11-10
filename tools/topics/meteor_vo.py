"""Topic: Why shooting stars glow — kinetic energy, work-energy theorem, non-conservative force.
Plus One · Ch5 Work, Energy and Power. Hook: Northern Taurid meteor shower peaks ~12 Nov 2026.
Scene/text timings are filled from the voice-over (see TIMES below)."""
import math, sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import *

HANDLE = "@jmk.space"
TAG = pill("PLUS ONE PHYSICS · WORK, ENERGY AND POWER", 28, bg=CYAN)
def top_tag(fr, t, fade=False):
    paste(fr, TAG, W / 2, 250, ease_out(prog(t, 0.1, 0.4)) if fade else 1.0)

# ---- line start times on the trimmed voice timeline (seconds); set by sync step ----
T = [0.0] * 13   # T[1]..T[12] = start of narration line 1..12; T[0] unused
END = 60.0
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from meteor_times import T, END, WT   # written by the sync step
except Exception:
    pass

# scenes: S1 lines 1-2 · S2 lines 3-5 · S3 lines 6-8 · S4 line 9 · S5 lines 10-12
def bounds():
    b = [0.0, T[3] - 0.15, T[6] - 0.15, T[9] - 0.15, T[10] - 0.15, END]
    return b

# ---------------- sky + meteor drawing ----------------
random.seed(11)
SKY_STARS = [(random.uniform(0, W), random.uniform(330, 1500), random.uniform(1.2, 3.4), random.uniform(0, 6.3)) for _ in range(120)]
SHOWERS = [(random.uniform(0, 6), random.uniform(500, 1100), random.uniform(250, 700), random.uniform(0.6, 1.0)) for _ in range(9)]

def draw_sky(fr, t, horizon=1460, tint=1.0):
    L = SS(W, 1180); d = L.d; s = L.s
    for x, y, r, ph in SKY_STARS:
        b = int((150 + 90 * math.sin(t * 2.1 + ph)) * tint)
        d.ellipse(s(x - r, y - 330 - r, x + r, y - 330 + r), fill=(b, b, min(255, b + 30), 255))
    # hills / coconut palms silhouette
    hy = horizon - 330
    pts = [(0, hy)] + [(x, hy - 40 - 30 * math.sin(x / 140)) for x in range(0, W + 40, 40)] + [(W, 1180), (0, 1180)]
    d.polygon([p for xy in pts for p in s(*xy)], fill=(14, 18, 40, 255))
    for px in (150, 860, 980):
        base = hy - 40 - 30 * math.sin(px / 140)
        d.line(s(px, base, px + 20, base - 230), fill=(14, 18, 40, 255), width=14)
        for a in range(-2, 3):
            ang = -math.pi / 2 + a * 0.55
            d.line(s(px + 20, base - 230, px + 20 + 110 * math.cos(ang), base - 230 + 110 * math.sin(ang) + 40), fill=(14, 18, 40, 255), width=10)
    fr.paste(L.done(), (0, 330), L.done())

def meteor(d, x, y, ang, length, alpha=1.0, width=7):
    """Bright head with a fading tail pointing back along -ang."""
    for k in range(18):
        f = k / 18
        x1 = x - math.cos(ang) * length * f; y1 = y - math.sin(ang) * length * f
        x2 = x - math.cos(ang) * length * (f + 1 / 18); y2 = y - math.sin(ang) * length * (f + 1 / 18)
        c = int(255 * (1 - f) * alpha)
        if c > 25:
            d.line((x1, y1, x2, y2), fill=(min(255, 60 + c), min(255, 40 + int(c * 0.9)), min(255, 70 + int(c * 0.5))), width=max(1, int(width * (1 - f))))
    r = width + 3
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 250, 220))

def shower(d, t, start=0.0):
    for t0, y0, ln, sp in SHOWERS:
        tt = (t - start - t0) % 6.5
        if tt > 1.2:
            continue
        p = tt / 1.2
        x = -100 + p * (W + 300) * sp
        y = y0 + p * 380 * sp
        meteor(d, x, y, math.atan2(380, W + 300), ln * min(1, p * 3), 1 - max(0, p - 0.7) / 0.3)

# ---------------- text assets ----------------
HOOK = text_img("ഈ ആഴ്ച രാത്രി ആകാശത്ത് *shooting stars!*", 64, max_w=940, hl=YELLOW)
NEWS = pill("Northern Taurid meteor shower · peak ~ Nov 12", 30, fg=WHITE, bg=(80, 60, 160))
WHY = text_img("അവ *കത്തുന്നത്* എന്തുകൊണ്ട്?", 66, max_w=940, hl=ORANGE)

M1 = text_img("*Meteors* = ബഹിരാകാശത്ത് നിന്നുള്ള ചെറിയ കല്ലുകളും പൊടിയും", 46, max_w=940, hl=CYAN)
KE = text_img("K = ½ m v²", 96, max_w=900, color=YELLOW)
KE_ML = text_img("*Velocity* കൂടുമ്പോൾ *kinetic energy* വളരെ കൂടും", 46, max_w=940, hl=YELLOW)
AIR = boxed(text_img("*Air resistance*: *kinetic energy* → *heat* + *light*", 42, max_w=900, hl=ORANGE, lh=1.4), outline=(255, 159, 67, 180))

THM_PILL = pill("WORK-ENERGY THEOREM", 38, bg=YELLOW)
THM = text_img("The change in *kinetic energy* of a particle is equal to the *work done* on it by the *net force*.", 50, max_w=880, hl=YELLOW, lh=1.45)
THM_CARD = card(960, THM.height + 44)
THM_EQ = text_img("ΔK = W", 92, max_w=600, color=CYAN)
NEG = text_img("*Air resistance* → *negative work* → *K* കുറയുന്നു", 46, max_w=960, hl=PINK)

NC_T = text_img("*Non-conservative forces*", 68, max_w=1000, hl=PINK)
NC_L = text_img("*Friction*, *air resistance*, *viscous force*", 46, max_w=960, hl=ORANGE)
NC_ML = text_img("*Energy* നഷ്ടപ്പെടുന്നില്ല — *heat*-ഉം *light*-ഉം ആയി മാറുന്നു", 46, max_w=960, hl=GREEN)
BAR_LBL = [text_img(s, 36, max_w=300, color=c) for s, c in (("KE", YELLOW), ("Heat", ORANGE), ("Light", CYAN))]

QUIZ = pill("QUIZ TIME", 44, fg=(9, 14, 38), bg=PINK)
PYQ = pill("PYQ · Plus One Exam 2024", 30, fg=WHITE, bg=(80, 60, 160))
Q = text_img("*Frictional force* conservative ആണോ, non-conservative ആണോ?", 58, max_w=920, hl=YELLOW)
OPT_A = card(480, 150, fill=(79, 209, 255, 40), outline=(79, 209, 255, 200))
OPT_B = card(480, 150, fill=(255, 159, 67, 40), outline=(255, 159, 67, 200))
TA = text_img("A) Conservative", 38, max_w=460)
TB = text_img("B) Non-conservative", 38, max_w=460)
CMT = text_img("ഉത്തരം *comment* ചെയ്യൂ!", 56, max_w=900, hl=CYAN)
FOL = text_img("*Follow* ചെയ്യൂ", 52, max_w=900, hl=YELLOW, color=WHITE)

# ---------------- word-by-word reveal (times from the voice transcript) ----------------
SPEC = dict(
    HOOK=("ഈ ആഴ്ച രാത്രി ആകാശത്ത് *shooting stars!*", dict(size=64, max_w=940, hl=YELLOW)),
    WHY=("അവ *കത്തുന്നത്* എന്തുകൊണ്ട്?", dict(size=66, max_w=940, hl=ORANGE)),
    M1=("*Meteors* = ബഹിരാകാശത്ത് നിന്നുള്ള ചെറിയ കല്ലുകളും പൊടിയും", dict(size=46, max_w=940, hl=CYAN)),
    KE_ML=("*Velocity* കൂടുമ്പോൾ *kinetic energy* വളരെ കൂടും", dict(size=46, max_w=940, hl=YELLOW)),
    THM=("The change in *kinetic energy* of a particle is equal to the *work done* on it by the *net force*.", dict(size=50, max_w=880, hl=YELLOW, lh=1.45)),
    NEG=("*Air resistance* → *negative work* → *K* കുറയുന്നു", dict(size=46, max_w=960, hl=PINK)),
    NC_L=("*Friction*, *air resistance*, *viscous force*", dict(size=46, max_w=960, hl=ORANGE)),
    NC_ML=("*Energy* നഷ്ടപ്പെടുന്നില്ല — *heat*-ഉം *light*-ഉം ആയി മാറുന്നു", dict(size=46, max_w=960, hl=GREEN)),
    Q=("*Frictional force* conservative ആണോ, non-conservative ആണോ?", dict(size=58, max_w=920, hl=YELLOW)),
    CMT=("ഉത്തരം *comment* ചെയ്യൂ!", dict(size=56, max_w=900, hl=CYAN)),
    FOL=("*Follow* ചെയ്യൂ", dict(size=52, max_w=900, hl=YELLOW, color=WHITE)),
)
for _k, (_s, _kw) in SPEC.items():
    assert len(_s.split()) == len(WT[_k]), _k
_RC = {}
def say(fr, key, x, y, t, s0, out_at=None):
    """Reveal block `key` word by word; t is scene time, s0 the scene start (global)."""
    times = [g - s0 for g in WT[key]]
    n = sum(1 for v in times if v <= t)
    if n == 0: return
    a = min(1.0, (t - times[n - 1]) / 0.12)
    oa = 1.0 if out_at is None else 1 - prog(t, out_at, 0.25)
    if oa <= 0: return
    ck = (key, n, round(a, 1))
    if ck not in _RC:
        s, kw = SPEC[key]; kw = dict(kw); size = kw.pop("size")
        _RC[ck] = text_img(s, size, reveal=(n, a), **kw)
    paste(fr, _RC[ck], x, y, oa)

def g(key, s0):  # global event time -> scene time
    return WT[key] - s0

# ---------------- scenes (t = time inside scene; a(i) = line i start inside scene) ----------------
def mk(scene_idx):
    b = bounds()
    s0 = b[scene_idx]
    return lambda i: T[i] - s0

def s1(fr, t, d):
    a = mk(0); s0 = bounds()[0]
    draw_sky(fr, t)
    shower(d, t)
    top_tag(fr, t, fade=True)
    say(fr, "HOOK", W / 2, 330, t, s0)
    appear(fr, NEWS, W / 2, 545, t, 3.6)
    say(fr, "WHY", W / 2, 1300, t, s0)

def s2(fr, t, d):
    a = mk(1); s0 = bounds()[1]
    draw_sky(fr, t + 20, tint=0.8)
    top_tag(fr, t)
    say(fr, "M1", W / 2, 340, t, s0)
    p = clamp((t - 0.3) / max(1.0, (a(5) + 3.0)))
    x = 120 + p * 760; y = 640 + p * 420
    glow = 0.3 + 0.7 * ease_in_out(prog(t, a(5), 1.2))
    if p < 0.995:
        L = SS(W, 1100); dd = L.d
        if glow > 0.35:
            for r in (90, 60, 35):
                dd.ellipse(L.s(x - r * glow, y - 330 - r * glow, x + r * glow, y - 330 + r * glow), fill=(255, 190, 90, int(70 * glow)))
        fr.paste(L.done(), (0, 330), L.done())
        meteor(d, x, y, math.atan2(420, 760), 160 + 260 * glow, 1.0, int(6 + 6 * glow))
    d.line((0, 760, W, 760), fill=(79, 209, 255), width=3)
    paste(fr, text_img("atmosphere", 30, max_w=300, color=CYAN), 920, 715, 0.9)
    appear(fr, KE, W / 2, 1180, t, g("K", s0), pop=True, out_at=g("AIR", s0) - 0.1)
    say(fr, "KE_ML", W / 2, 1320, t, s0, out_at=g("AIR", s0) - 0.1)
    appear(fr, AIR, W / 2, 1250, t, g("AIR", s0) + 0.1)

def s3(fr, t, d):
    a = mk(2); s0 = bounds()[2]
    top_tag(fr, t)
    appear(fr, THM_PILL, W / 2, 330, t, 0.1, pop=True)
    appear(fr, THM_CARD, W / 2, 440, t, a(7) - 0.3)
    say(fr, "THM", W / 2, 462, t, s0)
    appear(fr, THM_EQ, W / 2, 470 + THM.height + 70, t, g("THM_EQ", s0), pop=True)
    say(fr, "NEG", W / 2, 1250, t, s0)
    if t > a(8):
        k = ease_out(prog(t, a(8), 0.6))
        y0 = 1060
        arrow(d, 300, y0, 300 + 220 * k, y0, YELLOW, 10, 30)
        arrow(d, 780, y0 + 50, 780 - 220 * k, y0 + 50, PINK, 10, 30)
        paste(fr, text_img("v", 40, max_w=60, color=YELLOW), 300 + 240 * k, y0 - 30, k)
        paste(fr, text_img("F (air)", 34, max_w=200, color=PINK), 780 - 240 * k, y0 + 70, k)
        d.ellipse((520, y0, 560, y0 + 40), fill=(255, 240, 200))

def s4(fr, t, d):
    a = mk(3); s0 = bounds()[3]
    top_tag(fr, t)
    appear(fr, NC_T, W / 2, 330, t, max(0.1, g("NC_T", s0)), pop=True)
    say(fr, "NC_L", W / 2, 460, t, s0)
    k = ease_in_out(prog(t, g("BARS", s0), 2.6))
    vals = (1 - k, 0.7 * k, 0.3 * k)
    base, H, bw = 1230, 520, 170
    for i, (v, col) in enumerate(zip(vals, (YELLOW, ORANGE, CYAN))):
        x = 230 + i * 260
        d.rectangle((x, base - H, x + bw, base), outline=(90, 96, 150), width=3)
        if (H - 8) * v > 6:
            d.rectangle((x + 4, base - int((H - 8) * v), x + bw - 4, base - 4), fill=col)
        paste(fr, BAR_LBL[i], x + bw / 2, base + 14, 1.0)
    paste(fr, text_img("Total energy = constant", 38, max_w=700, color=GREEN), W / 2, base + 80, ease_out(prog(t, g("BARS", s0) + 0.5, 0.5)))
    say(fr, "NC_ML", W / 2, 1400, t, s0)

def s5(fr, t, d):
    a = mk(4); s0 = bounds()[4]
    appear(fr, QUIZ, W / 2, 290, t, max(0.1, g("QUIZ", s0)), pop=True)
    appear(fr, PYQ, W / 2, 380, t, g("PYQ", s0), pop=True)
    say(fr, "Q", W / 2, 470, t, s0)
    for i, (c, tx, cx, key) in enumerate(((OPT_A, TA, 280, "OPT_A"), (OPT_B, TB, 800, "OPT_B"))):
        st = g(key, s0)
        pulse = 1 + 0.03 * math.sin((t - st) * 6 + i * 3) if t > st + 0.6 else 1
        appear(fr, c, cx, 860, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 900, ease_out(prog(t, st + 0.05, 0.3)), pulse)
    say(fr, "CMT", W / 2, 1110, t, s0)
    say(fr, "FOL", W / 2, 1270, t, s0)

_b = bounds()
SCENES = [(_b[i + 1] - _b[i], f) for i, f in enumerate((s1, s2, s3, s4, s5))]

VOICE = "vo/meteor_voice.wav"
SFX = [(0.0, "whoosh"), (0.15, "pop"), (0.9, "pop"), (T[2] + 0.6, "boing")]
for i, s0 in enumerate(_b[1:5]):
    SFX += [(s0, "whoosh"), (s0 + 0.1, "pop")]
SFX += [(WT["K"], "ding"), (WT["AIR"] + 0.1, "swoosh"), (T[7], "ding"), (WT["THM_EQ"], "pop"), (T[8], "pop"),
        (WT["BARS"], "pop"), (WT["PYQ"], "pop"), (T[11], "pop"), (WT["OPT_A"], "pop"), (WT["OPT_B"], "pop"), (T[11] + 1.0, "ticks"),
        (WT["CMT"][0], "pop"), (WT["FOL"][0], "chime")]
SFX = [(max(0.0, s), k) for s, k in SFX if s < END - 0.3]
MUSIC = [(0.0, "space"), (_b[2], "curious"), (_b[4], "tension"), (T[12] + 1.0, "uplift")]
