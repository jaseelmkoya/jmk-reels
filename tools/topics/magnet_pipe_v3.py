"""Magnet in a metal pipe — v3: animated explanation synced to JMK's OWN voice (vo_magnet_v3.wav, silences trimmed),
word times from ElevenLabs scribe (magnet_pipe_v3_words.py, 113 words). Follows his experiment clip.
Each display token maps to a transcript word index (IDX), so captions are exactly on his words.
Plus Two · Ch6 Electromagnetic Induction."""
import math, sys, os, importlib.util
TOP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(TOP)); sys.path.insert(0, TOP)
import reelkit
from reelkit import *
reelkit.SYMBOLS |= set("εφ−⋅✓✗")
from magnet_pipe_v3_words import STARTS as WS

_spec = importlib.util.spec_from_file_location("mp", os.path.join(TOP, "magnet_pipe.py"))
mp = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(mp)
mp.COPPER, mp.COPPER_D, mp.COPPER_L = (168, 176, 192), (110, 118, 136), (230, 236, 248)   # shiny metal pipe

HANDLE = "@jmk.space"
TAG = pill("PLUS TWO PHYSICS · ELECTROMAGNETIC INDUCTION", 26, bg=CYAN)
def top_tag(fr, t): paste(fr, TAG, W / 2, 250)

w = lambda i: WS[i]
# scene boundaries in voice time (just before the first word of each part)
S0 = [0.0, w(27) - 0.12, w(47) - 0.15, w(92) - 0.15]
END = WS[-1] + 1.9
D = [S0[1] - S0[0], S0[2] - S0[1], S0[3] - S0[2], END - S0[3]]

# key: (scene, text, [transcript index per display token], style)
BLOCKS = {
    "WHY":  (0, "കാരണം: *Electromagnetic Induction*", [0, 1, 3], dict(size=58, max_w=1000, hl=CYAN)),
    "SUB":  (0, "*Magnet* വീഴുമ്പോൾ *metal pipe*-ലെ ഓരോ *ring*-ലും *magnetic flux* മാറുന്നു.", [4, 5, 6, 7, 9, 10, 12, 13, 14], dict(size=48, max_w=960, hl=YELLOW)),
    "CAP2": (0, "അപ്പോൾ *induced current* അഥവാ *eddy currents* ഉണ്ടാകുന്നു — അത് *magnet*-നെ മുകളിലേക്ക് തള്ളുന്നു!",
             [15, 16, 17, 18, 19, 20, 21, 21, 22, 23, 25, 26], dict(size=48, max_w=960, hl=GREEN)),
    "PL":   (1, "*Plastic* ഒരു *insulator* ആണ് — *current* ഉണ്ടാകില്ല, അതുകൊണ്ട് *magnet* വേഗം വീഴുന്നു.",
             [27, 28, 29, 30, 30, 31, 32, 33, 34, 35, 36], dict(size=44, max_w=980, hl=ORANGE, lh=1.4)),
    "MT":   (1, "*Metal* ഒരു *conductor* ആണ് — *eddy currents* എതിർക്കുന്നു, അതുകൊണ്ട് *time delay!*",
             [37, 38, 39, 40, 40, 41, 42, 43, 44, 45, 46], dict(size=44, max_w=980, hl=CYAN, lh=1.4)),
    "LAW":  (2, "The *induced current* opposes the change in *magnetic flux* that produces it.", list(range(49, 61)),
             dict(size=54, max_w=880, hl=YELLOW, lh=1.45)),
    "LAW_ML": (2, "*Flux*-ലെ മാറ്റത്തെ എതിർക്കുന്ന ദിശയിലാണ് *induced current*. അതുകൊണ്ട് *magnet* പതുക്കെ വീഴുന്നു.",
             [61, 63, 64, 65, 66, 67, 68, 69, 70, 71], dict(size=48, max_w=940, hl=CYAN)),
    "Q":    (3, "*Lenz's law* ഏത് *conservation law*-ന് അനുസൃതമാണ്?", [94, 95, 96, 97, 98, 99], dict(size=58, max_w=920, hl=YELLOW)),
    "CMT":  (3, "ഉത്തരം *comment* ചെയ്യൂ!", [108, 109, 110], dict(size=56, max_w=900, hl=CYAN)),
    "FOL":  (3, "*Follow* ചെയ്യൂ", [111, 112], dict(size=56, max_w=900, hl=YELLOW)),
}
for k, (sc, txt, idx, _) in BLOCKS.items():
    assert len(txt.split()) == len(idx), k
WT = {k: [WS[i] for i in idx] for k, (sc, txt, idx, _) in BLOCKS.items()}
EV = dict(RINGS=w(16) - 0.2, FORCE=w(25) - 0.3, LAWP=w(47), FAR=w(72), EQ=w(75), EQN=w(86), QUIZ=w(92),
          EXAM=w(94), OPT_A=w(100), OPT_B=w(104), DROP=S0[1] + 0.25, MTR=w(41))

_RC = {}
def say(fr, key, x, y, t, sc, out_at=None):
    times = [g - S0[sc] for g in WT[key]]
    n = sum(1 for v in times if v <= t)
    if n == 0: return
    a = min(1.0, (t - times[n - 1]) / 0.12)
    oa = 1.0 if out_at is None else 1 - prog(t, out_at, 0.3)
    if oa <= 0: return
    ck = (key, n, round(a, 1))
    if ck not in _RC:
        _, s, _, kw = BLOCKS[key]; kw = dict(kw); size = kw.pop("size")
        _RC[ck] = text_img(s, size, reveal=(n, a), **kw)
    paste(fr, _RC[ck], x, y, oa)

def ev(k, sc): return EV[k] - S0[sc]

# ---------- scene 1: induction ----------
def s1(fr, t, d):
    sc = 0
    top_tag(fr, t)
    say(fr, "WHY", W / 2, 320, t, sc)
    say(fr, "SUB", W / 2, 420, t, sc)
    a_r = ease_out(prog(t, ev("RINGS", sc), 0.6))
    a_f = ease_out(prog(t, ev("FORCE", sc), 0.6))
    mp.zoom_pipe(fr, d, t, a_r, a_f)
    say(fr, "CAP2", W / 2, 1300, t, sc)

# ---------- scene 2: plastic vs metal race with millisecond stopwatches ----------
PL_LAB = pill("PLASTIC · insulator", 30, fg=(9, 14, 38), bg=(200, 215, 240))
MT_LAB = pill("METAL · conductor", 30, fg=(9, 14, 38), bg=(190, 198, 214))
SIM = text_img("(animation)", 26, max_w=300, color=MUTED)
T_PL = 0.32                      # free fall through ~0.5 m: t = √(2h/g) ≈ 0.32 s
V_MT = 92.0                      # px/s terminal speed in the metal pipe
Y0, YEXIT = 720, 1262
T_MT = (YEXIT - Y0) / V_MT + 0.3

def stopwatch(fr, cx, y, secs, running, col):
    L = SS(300, 120); dd = L.d; k = L.s
    dd.rounded_rectangle(k(4, 14, 296, 116), radius=26, fill=(9, 14, 38, 230), outline=col + (255,), width=5)
    dd.rounded_rectangle(k(132, 0, 168, 18), radius=6, fill=col + (255,))
    img = L.done()
    paste(fr, img, cx, y)
    s = f"{int(secs):02d}.{int((secs % 1) * 1000):03d} s"
    tx = text_img(s, 46, max_w=300, color=WHITE if running else col)
    paste(fr, tx, cx, y + 26)

def s2(fr, t, d):
    sc = 1
    top_tag(fr, t)
    say(fr, "PL", W / 2, 320, t, sc)
    say(fr, "MT", W / 2, 505, t, sc)
    td = t - ev("DROP", sc)
    # plastic: free fall (scaled to the pipe length on screen)
    if td < 0:
        yp = Y0
    else:
        yp = Y0 + (YEXIT - Y0 + 60) * (td / T_PL) ** 2
    mp._mag(fr, 330, yp if yp < 1300 else None)
    mp.pipe(fr, 330, False)
    # metal: quickly reaches a small constant (terminal) speed
    ym = Y0 if td < 0 else Y0 + V_MT * td - V_MT * 0.3 * (1 - math.exp(-td / 0.3))
    mp._mag(fr, 750, ym if ym < 1300 else None)
    mp.pipe(fr, 750, True)
    if td > 0 and ym < YEXIT and t > ev("MTR", sc):
        a = ease_out(prog(t, ev("MTR", sc), 0.4))
        for dy, col in ((-80, ORANGE), (80, CYAN)):
            d.ellipse((750 - 72, ym + dy - 16, 750 + 72, ym + dy + 16), outline=tuple(int(c * a) for c in col), width=6)
    paste(fr, PL_LAB, 330, 1290)
    paste(fr, MT_LAB, 750, 1290)
    sp = min(max(td, 0), T_PL); sm = min(max(td, 0), T_MT)
    stopwatch(fr, 330, 1375, sp, 0 < td < T_PL, ORANGE)
    stopwatch(fr, 750, 1375, sm, 0 < td < T_MT, CYAN)
    paste(fr, SIM, W / 2, 1540, 0.8)

# ---------- scene 3: Lenz's law ----------
LAW_PILL = pill("LENZ'S LAW", 44, bg=YELLOW)
LAW_H = text_img(BLOCKS["LAW"][1], 54, max_w=880, hl=YELLOW, lh=1.45)
LAW_CARD = card(960, LAW_H.height + 50)

def s3(fr, t, d):
    sc = 2
    top_tag(fr, t)
    appear(fr, LAW_PILL, W / 2, 320, t, ev("LAWP", sc), pop=True)
    appear(fr, LAW_CARD, W / 2, 430, t, ev("LAWP", sc) + 0.2)
    say(fr, "LAW", W / 2, 455, t, sc)
    say(fr, "LAW_ML", W / 2, 455 + LAW_H.height + 90, t, sc)
    appear(fr, mp.FAR_P, W / 2, 1150, t, ev("FAR", sc), pop=True)
    appear(fr, mp.EQ, W / 2, 1235, t, ev("EQ", sc), pop=True)
    appear(fr, mp.EQ_N, W / 2, 1385, t, ev("EQN", sc))

# ---------- scene 4: quiz ----------
def s4(fr, t, d):
    sc = 3
    appear(fr, mp.QUIZ, W / 2, 290, t, ev("QUIZ", sc), pop=True)
    appear(fr, mp.EXAM, W / 2, 380, t, ev("EXAM", sc) - 0.2, pop=True)
    say(fr, "Q", W / 2, 470, t, sc)
    for i, (c, tx, cx, key) in enumerate(((mp.OPT_A, mp.TA, 285, "OPT_A"), (mp.OPT_B, mp.TB, 795, "OPT_B"))):
        st = ev(key, sc)
        pulse = 1 + 0.03 * math.sin((t - st) * 6 + i * 3) if t > st + 0.6 else 1
        appear(fr, c, cx, 820, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 845, ease_out(prog(t, st + 0.05, 0.3)), pulse)
    say(fr, "CMT", W / 2, 1090, t, sc)
    say(fr, "FOL", W / 2, 1250, t, sc)

SCENES = list(zip(D, (s1, s2, s3, s4)))

VOICE = "vo_magnet_v3.wav"
SFX = [(0.0, "whoosh"), (EV["RINGS"], "zap"), (EV["FORCE"], "ding")]
for s in S0[1:]:
    SFX += [(s, "whoosh")]
SFX += [(EV["DROP"], "pop"), (EV["DROP"] + T_PL, "thud"), (EV["MTR"], "zap"), (EV["DROP"] + T_MT, "ding"),
        (EV["LAWP"], "pop"), (EV["EQ"], "ding"), (EV["QUIZ"], "pop"), (EV["OPT_A"], "pop"), (EV["OPT_B"], "pop"),
        (EV["OPT_B"] + 1.2, "ticks"), (w(111), "chime")]
SFX = [(max(0.0, s), k) for s, k in SFX if s < END - 0.3]
MUSIC = [(0.0, "electric"), (S0[1], "curious"), (S0[2], "ocean"), (S0[3], "tension"), (w(111) - 0.3, "uplift")]
MUSIC_SEED = 733
