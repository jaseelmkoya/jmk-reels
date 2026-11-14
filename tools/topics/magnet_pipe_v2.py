"""Magnet in a metal pipe — v2: animated EXPLANATION that follows JMK's own experiment clip (plastic pipe vs metal pipe).
His clip ends with "...time delay ഉണ്ടാകാൻ കാരണമെന്താണ് നമുക്ക് നോക്കിയാലോ" → this animation starts directly with the reason.
Plus Two · Ch6 Electromagnetic Induction. No-voice: words at reading pace. For his voice: replace WT with transcript word times
(display tokens are one-to-one with the VO script in magnet_pipe_v2_script.txt)."""
import math, sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import reelkit
from reelkit import *
reelkit.SYMBOLS |= set("εφ−⋅✓✗")

_spec = importlib.util.spec_from_file_location("mp", os.path.join(os.path.dirname(os.path.abspath(__file__)), "magnet_pipe.py"))
mp = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(mp)
# JMK's pipe is a shiny metal (not copper) -> silver colours
mp.COPPER, mp.COPPER_D, mp.COPPER_L = (168, 176, 192), (110, 118, 136), (230, 236, 248)

HANDLE = "@jmk.space"
TAG = pill("PLUS TWO PHYSICS · ELECTROMAGNETIC INDUCTION", 26, bg=CYAN)
def top_tag(fr, t):
    paste(fr, TAG, W / 2, 250)

PACE = 0.40
D = [12.0, 9.0, 13.5, 10.5]
S0 = [sum(D[:i]) for i in range(len(D))]
END = sum(D)

BLOCKS = {
    "WHY":   (0, 0.2, "കാരണം: *Electromagnetic Induction*", dict(size=58, max_w=1000, hl=CYAN)),
    "SUB":   (0, 1.8, "*Magnet* വീഴുമ്പോൾ *metal pipe*-ലെ ഓരോ *ring*-ലും *magnetic flux* മാറുന്നു.", dict(size=48, max_w=960, hl=YELLOW)),
    "CAP2":  (0, 6.0, "അപ്പോൾ *induced current* (*eddy currents*) ഉണ്ടാകുന്നു — അത് *magnet*-നെ മുകളിലേക്ക് തള്ളുന്നു!", dict(size=48, max_w=960, hl=GREEN)),
    "PL":    (1, 0.3, "*Plastic* ഒരു *insulator* ആണ് — *current* ഉണ്ടാകില്ല, അതുകൊണ്ട് *magnet* വേഗം വീഴുന്നു.", dict(size=44, max_w=980, hl=ORANGE, lh=1.4)),
    "MT":    (1, 4.3, "*Metal* ഒരു *conductor* — *eddy currents* എതിർക്കുന്നു, അതുകൊണ്ട് *time delay!*", dict(size=44, max_w=980, hl=CYAN, lh=1.4)),
    "LAW":   (2, 0.7, "The *induced current* opposes the change in *flux* that produces it.", dict(size=56, max_w=880, hl=YELLOW, lh=1.45)),
    "LAW_ML": (2, 5.6, "*Flux*-ലെ മാറ്റത്തെ എതിർക്കുന്ന ദിശയിലാണ് *induced current*. അതുകൊണ്ട് *magnet* പതുക്കെ വീഴുന്നു.", dict(size=48, max_w=940, hl=CYAN)),
    "Q":     (3, 0.9, "*Lenz's law* ഏത് *conservation law*-ന് അനുസൃതമാണ്?", dict(size=58, max_w=920, hl=YELLOW)),
    "CMT":   (3, 6.3, "ഉത്തരം *comment* ചെയ്യൂ!", dict(size=56, max_w=900, hl=CYAN)),
    "FOL":   (3, 8.2, "*Follow* ചെയ്യൂ", dict(size=56, max_w=900, hl=YELLOW)),
}
WT = {k: [S0[sc] + st + i * PACE for i in range(len(txt.split()))] for k, (sc, st, txt, _) in BLOCKS.items()}
EV = dict(RINGS=S0[0] + 4.6, FORCE=S0[0] + 8.6, EQ=S0[2] + 10.4, EXAM=S0[3] + 0.4, OPT_A=S0[3] + 4.1, OPT_B=S0[3] + 4.5)

_RC = {}
def say(fr, key, x, y, t, sc, out_at=None):
    times = [g - S0[sc] for g in WT[key]]
    n = sum(1 for v in times if v <= t)
    if n == 0: return
    a = min(1.0, (t - times[n - 1]) / 0.15)
    oa = 1.0 if out_at is None else 1 - prog(t, out_at, 0.3)
    if oa <= 0: return
    ck = (key, n, round(a, 1))
    if ck not in _RC:
        _, _, s, kw = BLOCKS[key]; kw = dict(kw); size = kw.pop("size")
        _RC[ck] = text_img(s, size, reveal=(n, a), **kw)
    paste(fr, _RC[ck], x, y, oa)

def ev(k, sc): return EV[k] - S0[sc]

def s1(fr, t, d):
    sc = 0
    top_tag(fr, t)
    say(fr, "WHY", W / 2, 320, t, sc)
    say(fr, "SUB", W / 2, 420, t, sc)
    a_r = ease_out(prog(t, ev("RINGS", sc), 0.6))
    a_f = ease_out(prog(t, ev("FORCE", sc), 0.6))
    mp.zoom_pipe(fr, d, t, a_r, a_f)
    say(fr, "CAP2", W / 2, 1300, t, sc)

PL_LAB = pill("PLASTIC · insulator", 30, fg=(9, 14, 38), bg=(200, 215, 240))
MT_LAB = pill("METAL · conductor", 30, fg=(9, 14, 38), bg=(190, 198, 214))
FAST = boxed(text_img("വേഗം!", 40, max_w=300, color=WHITE))
SLOW = boxed(text_img("*time delay*", 40, max_w=360, hl=CYAN))

def s2(fr, t, d):
    sc = 1
    top_tag(fr, t)
    say(fr, "PL", W / 2, 320, t, sc)
    mp.s1_visual(fr, d, t + 1.0)
    # induced-current rings drawn on the metal pipe only
    y = mp.slow_y(t + 1.0)
    if y is not None and y < 1240 and t > WT["MT"][0] - S0[sc]:
        a = ease_out(prog(t, WT["MT"][0] - S0[sc], 0.5))
        for dy, col in ((-80, ORANGE), (80, CYAN)):
            d.ellipse((750 - 72, y + dy - 16, 750 + 72, y + dy + 16), outline=tuple(int(c * a) for c in col), width=6)
    paste(fr, PL_LAB, 330, 1300)
    paste(fr, MT_LAB, 750, 1300)
    appear(fr, FAST, 330, 1385, t, 1.5)
    appear(fr, SLOW, 750, 1385, t, WT["MT"][0] - S0[sc] + 1.5)
    say(fr, "MT", W / 2, 505, t, sc)

LAW_PILL = pill("LENZ'S LAW", 44, bg=YELLOW)
LAW_H = text_img(BLOCKS["LAW"][2], 56, max_w=880, hl=YELLOW, lh=1.45)
LAW_CARD = card(960, LAW_H.height + 50)

def s3(fr, t, d):
    sc = 2
    top_tag(fr, t)
    appear(fr, LAW_PILL, W / 2, 320, t, 0.1, pop=True)
    appear(fr, LAW_CARD, W / 2, 430, t, 0.3)
    say(fr, "LAW", W / 2, 455, t, sc)
    say(fr, "LAW_ML", W / 2, 455 + LAW_H.height + 90, t, sc)
    es = ev("EQ", sc)
    appear(fr, mp.FAR_P, W / 2, 1150, t, es - 0.5, pop=True)
    appear(fr, mp.EQ, W / 2, 1235, t, es, pop=True)
    appear(fr, mp.EQ_N, W / 2, 1385, t, es + 0.8)

def s4(fr, t, d):
    sc = 3
    appear(fr, mp.QUIZ, W / 2, 290, t, 0.1, pop=True)
    appear(fr, mp.EXAM, W / 2, 380, t, ev("EXAM", sc), pop=True)
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

VOICE = None
SFX = [(0.0, "whoosh"), (0.15, "pop"), (WT["SUB"][0], "pop"), (EV["RINGS"], "zap"), (WT["CAP2"][0], "pop"), (EV["FORCE"], "ding")]
for s in S0[1:]:
    SFX += [(s, "whoosh"), (s + 0.15, "pop")]
SFX += [(S0[1] + 1.5, "boing"), (WT["MT"][0], "zap"), (WT["MT"][0] + 1.5, "ding"),
        (S0[2] + 0.3, "pop"), (WT["LAW_ML"][0], "pop"), (EV["EQ"], "ding"),
        (EV["EXAM"], "pop"), (EV["OPT_A"], "pop"), (EV["OPT_B"], "pop"), (EV["OPT_B"] + 0.6, "ticks"),
        (WT["CMT"][0], "pop"), (WT["FOL"][0], "chime")]
SFX = [(max(0.0, s), k) for s, k in SFX if s < END - 0.3]
MUSIC = [(0.0, "electric"), (S0[1], "curious"), (S0[2], "ocean"), (S0[3], "tension"), (WT["FOL"][0] - 0.3, "uplift")]
MUSIC_SEED = 733
