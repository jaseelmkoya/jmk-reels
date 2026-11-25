"""25 Nov 2026 · spin chair (conservation of angular momentum) — VOICED version, full re-render timed to JMK's recording.
Voice: JMK's file angular_mementum.mp3 (sent in chat 25 Nov), kept OUTSIDE the repo (VO_DIR env, default scratchpad).
Word times: JMK's own word list (sent with the file), corrected against the recording's pauses (silencedetect -35 dB)
with a piecewise-linear map (ANCHORS: list time -> real time). No ElevenLabs used.
PLAT=yt → YouTube cut keeps the closing 'സബ്സ്ക്രൈബ് ചെയ്യൂ' and shows 'Subscribe ചെയ്യൂ'; IG cut ends after 'ഫോളോ ചെയ്യൂ'."""
import math, sys, os, bisect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import importlib.util
_spec = importlib.util.spec_from_file_location("spin_base", os.path.join(os.path.dirname(os.path.abspath(__file__)), "spin_chair.py"))
B = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(B)
from storykit import *
from reelkit import text_img, pill, boxed, card, paste, appear, prog, ease_out, arrow, W, H
from captions import Captions

HANDLE = "@jmk.space"
YT = os.environ.get("PLAT") == "yt"
VO_DIR = os.environ.get("VO_DIR", "/tmp/claude-0/-home-claude-jmk-reels/248bc511-40f2-50fc-a693-a417f3d46d85/scratchpad/vo")

# --- JMK's word list (start times as sent) ---
DOC = [0.000, 0.550, 1.100, 1.350, 1.850, 2.200, 2.680,          # hook (7)
       3.600, 3.850, 4.220, 4.700, 5.650, 5.900, 6.520, 6.850, 7.500, 8.350, 8.750,
       9.800, 10.420, 10.950, 11.350, 11.980, 12.220, 13.300, 13.850, 14.220,
       15.250, 15.550, 16.050, 16.450, 17.300, 17.650, 18.180, 18.700, 19.250, 19.500, 20.500, 21.020, 21.320, 21.650,
       22.750, 22.980, 23.520, 23.900, 24.080, 24.750, 24.920, 25.420, 25.980, 26.250, 26.580, 26.780, 27.200, 27.380,
       28.350, 28.850, 29.500, 29.950, 30.420,
       31.500, 31.720, 32.220, 33.050, 33.320, 33.980, 34.520, 35.000,
       36.600, 36.920, 37.150, 37.620, 38.500, 38.920, 39.100, 39.620, 39.850, 40.320, 40.750, 40.980, 41.180,
       41.850, 42.280, 42.880, 43.300, 43.580, 43.950, 44.420,
       45.150, 45.420, 45.900, 46.550, 46.980, 47.580, 47.850, 48.800, 49.020, 49.720, 50.000,
       51.150, 51.420, 52.180, 52.700, 53.900, 54.220, 54.880, 55.450, 56.020, 56.350, 56.680,
       58.200, 58.620, 58.950, 59.480, 59.950, 60.380, 61.080, 61.350, 61.720, 62.050, 62.280, 62.680, 63.250, 63.620, 63.850, 64.220, 64.450,
       65.600, 65.880, 66.400, 67.050, 67.380, 67.800, 68.180, 68.550,
       69.650]                                                     # 'ഇനി' (quiz) — end of captions
# list time -> real time (pauses in the recording, silencedetect)
ANCHORS = [(0, 0.31), (3.25, 3.40), (3.60, 4.11), (5.40, 5.45), (5.65, 5.86), (8.15, 8.00), (8.35, 8.26),
           (12.95, 12.21), (13.30, 12.63), (14.85, 14.11), (15.25, 14.66), (17.00, 16.65), (17.30, 17.09),
           (20.15, 19.69), (20.50, 20.06), (22.45, 21.83), (22.75, 22.22), (27.95, 27.74), (28.35, 28.55),
           (31.20, 31.20), (31.50, 31.61), (35.42, 34.81), (36.60, 36.44), (38.25, 37.94), (38.50, 38.22),
           (41.65, 41.16), (41.85, 41.56), (44.95, 44.18), (45.15, 44.62), (46.28, 45.44), (46.55, 45.78),
           (50.92, 50.20), (51.15, 50.62), (53.18, 52.35), (53.90, 53.36), (57.10, 56.12), (58.20, 57.26),
           (60.82, 59.08), (61.08, 59.64), (64.98, 64.02), (65.60, 65.10), (68.90, 68.11), (69.65, 69.04),
           (71.05, 70.16), (71.35, 70.52), (78.60, 77.68), (79.70, 79.17), (81.45, 80.58), (81.70, 80.87),
           (83.12, 82.06), (83.32, 82.37), (84.55, 83.58), (84.65, 83.88), (85.50, 84.58), (86.05, 86.06), (87.0, 86.92)]
_AX = [a for a, _ in ANCHORS]; _AY = [b for _, b in ANCHORS]
def R(x):
    i = max(1, min(len(_AX) - 1, bisect.bisect_left(_AX, x)))
    x0, x1, y0, y1 = _AX[i - 1], _AX[i], _AY[i - 1], _AY[i]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
WORDS = [{"start": R(t)} for t in DOC]

LINES = [
    ("കൈ നീട്ടി പതുക്കെ കറങ്ങുന്നു. കൈ മടക്കിയതും *spin* മൂന്നിരട്ടി വേഗതയിൽ. ആരും തള്ളിയില്ല.", YELLOW),
    ("കസേരയുടെ *axis*-ന് ചുറ്റും പുറത്തുനിന്നും ഒരു *torque*-ഉമില്ല. *External* *torque* *zero.*", CYAN),
    ("*τ* = *dL* */dt.* *Torque* ഇല്ലെങ്കിൽ *angular* *momentum* *L* മാറില്ല. നോക്കൂ, *L* ബാർ അനങ്ങുന്നില്ല.", ORANGE),
    ("If external torque is zero, the angular momentum *L* = *I* *ω* is constant. *I₁* *ω₁* = *I₂* *ω₂.*", YELLOW),
    ("*L* മാറാതെ നിൽക്കണം. *I* കുറഞ്ഞാൽ *ω* കൂടിയേ പറ്റൂ.", PINK),
    ("ഇനി *I* എന്തിന് കുറയുന്നു? *Moment* *of* *inertia* *I* = *Σ* *m* *r* *square.* *Mass* *axis*-ൽ നിന്നും എത്ര ദൂരെ എന്നതാണ് പ്രധാനം.", CYAN),
    ("*r* *square* ആണ്. കയ്യിലെ *mass*-ന്റെ *r* പകുതിയായാൽ ആ ഭാഗത്തിന്റെ *I* നാലിലൊന്നാകും.", ORANGE),
    ("*I* കുറഞ്ഞു, *ω* കൂടി. *Ice* *skaters*-ഉം *diver*-ഉം ചെയ്യുന്നത് ഇതേ *trick* തന്നെ.", PINK),
    ("അപ്പോൾ കൂടിയ *kinetic* *energy* എവിടെ നിന്ന്? *K* = ½ *I* *ω* ² = *L* ² / *2I.* കൈ ഉള്ളിലേക്ക് വലിക്കുമ്പോൾ നമ്മുടെ പേശികൾ ചെയ്യുന്ന *work*-ൽ നിന്ന്.", GREEN),
]
assert sum(len(t.split()) for t, _ in LINES) == len(DOC) - 8, (sum(len(t.split()) for t, _ in LINES), len(DOC) - 8)
CAP = Captions.from_words(LINES, WORDS[7:], size=52, maxw=8)

def w(i): return WORDS[i]["start"]          # real start of word i (index in DOC)
def r(t): return R(t)                        # real time of a list time
# scene starts (just before the first word of each part)
ST = [0.0, r(9.80) - 0.25, r(22.75) - 0.25, r(36.60) - 0.3, r(58.20) - 0.3, r(69.65) - 0.3]
END = (r(87.0) + 0.45) if YT else 85.0
ST.append(END)
S = [ST[i + 1] - ST[i] for i in range(6)]
def caps(fr, si, t, y=1335): CAP.draw(fr, ST[si] + t, y)
def at(list_t, si): return r(list_t) - ST[si]   # scene-local time of a list time

# ---------- S0 hook ----------
FOLD_T = at(5.90, 0) + 0.1
SP0 = B.Spinner(B.fold_once(FOLD_T), S[0] + 0.5)
def s0(fr, t, d):
    fr.paste(B.BG_IMG, (0, 0))
    th, f = SP0.at(t)
    B.person(fr, W / 2, 860, th, f, 1.0)
    paste(fr, B.H0, W / 2, 130)
    paste(fr, B.HOOK, W / 2, 290, 1.0, 1 + 0.02 * math.sin(t * 4))
    paste(fr, B.TAG, W / 2, 245, ease_out(prog(t, 1.5, 0.4)))
    paste(fr, B.TOPV, 150, 1220, ease_out(prog(t, 1.0, 0.4)))
    appear(fr, B.X3, 880, 640, t, at(6.85, 0), pop=True)
    if t > at(3.60, 0) - 0.1: caps(fr, 0, t)

# ---------- S1 no torque ----------
SP1 = B.Spinner(B.fold_cycle(True, 1.6, 1.6, 0.6), S[1] + 0.5, SP0.th[-1])
def s1(fr, t, d):
    fr.paste(B.BG_IMG, (0, 0))
    th, f = SP1.at(t)
    B.person(fr, W / 2, 720, th, f, 0.75)
    paste(fr, B.H1, W / 2, 150)
    appear(fr, B.TZ, W / 2, 285, t, at(13.30, 1), pop=True)
    appear(fr, B.TDL, W / 2, 370, t, at(15.25, 1), pop=True)
    B.meters(fr, d, f, 1010, ease_out(prog(t, at(17.30, 1), 0.5)))
    caps(fr, 1, t)

# ---------- S2 law ----------
SA = B.Spinner(lambda t: 0.0, S[2] + 0.5); SB = B.Spinner(lambda t: 1.0, S[2] + 0.5)
def s2(fr, t, d):
    fr.paste(B.BG_IMG, (0, 0))
    appear(fr, B.LP, W / 2, 200, t, 0.1, pop=True)
    appear(fr, B.LCARD, W / 2, 300, t, 0.2)
    appear(fr, B.LAW, W / 2, 318, t, 0.3)
    appear(fr, B.LEQ, W / 2, 318 + B.LAW.height, t, at(28.35, 2), pop=True)
    a = ease_out(prog(t, at(31.50, 2), 0.5))
    if a > 0:
        tha, fa = SA.at(t); thb, fb = SB.at(t)
        B.person(fr, 290, 900, tha, fa, 0.6)
        B.person(fr, 790, 900, thb, fb, 0.6)
        paste(fr, B.LA, 290, 1140, a); paste(fr, B.LB, 790, 1140, a)
    caps(fr, 2, t)

# ---------- S3 I = Σmr² ----------
SP3 = B.Spinner(B.fold_cycle(False, 2.2, 2.0, 0.8, 0.3), S[3] + 0.5, SP1.th[-1])
def s3(fr, t, d):
    fr.paste(B.BG_IMG, (0, 0))
    th, f = SP3.at(t)
    B.person(fr, W / 2, 800, th, f, 0.8, rlabel=True)
    hx, hy = B.hand_local(f); ex, ey = B.rot(hx * 0.8, hy * 0.8, th)
    paste(fr, B.RL_OUT, W / 2 + ex * 0.6, 800 + ey * 0.6 - 40)
    paste(fr, B.H3, W / 2, 140)
    appear(fr, B.IEQ, W / 2, 250, t, at(38.50, 3), pop=True)
    appear(fr, B.RQ, W / 2, 370, t, at(46.55, 3), pop=True)
    appear(fr, B.SK, W / 2, 460, t, at(53.90, 3), pop=True)
    B.meters(fr, d, f, 1090, ease_out(prog(t, at(45.15, 3), 0.5)), show_L=False)
    caps(fr, 3, t)

# ---------- S4 energy ----------
SP4 = B.Spinner(B.fold_cycle(False, 1.6, 1.8, 0.9, 0.2), S[4] + 0.5, SP3.th[-1])
def s4(fr, t, d):
    fr.paste(B.BG_IMG, (0, 0))
    th, f = SP4.at(t)
    B.person(fr, W / 2, 820, th, f, 0.85)
    u = (t - 0.2) % (1.6 + 1.8 + 1.8)
    if 1.6 <= u < 2.5:
        for side in (1, -1):
            hx, hy = B.hand_local(f); ex, ey = B.rot(side * hx * 0.85, hy * 0.85, th)
            arrow(d, W / 2 + ex * 1.35, 820 + ey * 1.35, W / 2 + ex * 1.05, 820 + ey * 1.05, ORANGE, 10, 30)
    paste(fr, B.H4, W / 2, 150)
    appear(fr, B.KE, W / 2, 300, t, at(61.08, 4), pop=True)
    appear(fr, B.KI, W / 2, 420, t, at(64.45, 4), pop=True)
    appear(fr, B.WK, W / 2, 1210, t, at(65.60, 4), pop=True)
    caps(fr, 4, t)

# ---------- S5 quiz (voice reads it; no captions) ----------
SUB = text_img("*Subscribe* ചെയ്യൂ", 58, max_w=900, hl=RED)
def s5(fr, t, d):
    fr.paste(B.BG_IMG, (0, 0))
    appear(fr, B.QUIZ, W / 2, 270, t, 0.1, pop=True)
    appear(fr, B.PYQ, W / 2, 370, t, at(71.35, 5) - 0.1, pop=True)
    appear(fr, B.Q, W / 2, 470, t, at(73.55, 5))
    appear(fr, B.HINT, W / 2, 470 + B.Q.height + 10, t, at(78.60, 5))
    for i, (c, tx, cx, lt) in enumerate(((B.OPT_A, B.TA, 290, 79.70), (B.OPT_B, B.TB, 790, 81.70))):
        st = at(lt, 5) - 0.1
        pulse = 1 + 0.03 * math.sin((t - st) * 6 + i * 3) if t > st + 0.6 else 1
        appear(fr, c, cx, 910, t, st, pop=True)
        if t > st + 0.1:
            paste(fr, tx, cx, 950, ease_out(prog(t, st + 0.05, 0.3)), pulse)
    appear(fr, B.CMT, W / 2, 1130, t, at(83.32, 5), pop=True)
    appear(fr, B.FOL, W / 2, 1270, t, at(84.65, 5), pop=True)
    if YT: appear(fr, SUB, W / 2, 1390, t, at(86.05, 5), pop=True)

SCENES = [(S[i], f) for i, f in enumerate((s0, s1, s2, s3, s4, s5))]
VOICE = os.path.join(VO_DIR, "vo_full.wav" if YT else "vo_ig.wav")
MUSIC_GAIN = 0.32
MUSIC = [(0.0, "curious"), (ST[1], "tension"), (ST[2], "uplift"), (ST[3], "drive"), (ST[4], "curious"), (ST[5], "tension")]
MUSIC_SEED = 2511
SFX = [(0.0, "whoosh"), (FOLD_T, "swoosh"), (ST[0] + at(6.85, 0), "pop"), (ST[0] + at(6.85, 0) + 0.05, "ding"),
       (ST[1] + 0.05, "swoosh"), (r(13.30), "pop"), (r(15.25), "pop"), (r(21.02), "ding"),
       (ST[2] + 0.1, "pop"), (r(28.35), "ding"), (r(31.50), "whoosh"),
       (ST[3] + 0.05, "swoosh"), (r(38.50), "pop"), (r(46.55), "pop"), (r(53.90), "ding"),
       (ST[4] + 0.05, "swoosh"), (r(61.08), "pop"), (r(64.45), "ding"), (r(65.60), "pop"),
       (ST[5] + 0.1, "pop"), (r(79.70) - 0.1, "pop"), (r(81.70) - 0.1, "pop"), (r(78.60), "ticks"), (r(84.65), "chime")]
if YT: SFX.append((r(86.05), "ding"))
if __name__ == "__main__": print("total", round(ST[-1], 2), [round(x, 2) for x in S], "fold", round(FOLD_T, 2))
