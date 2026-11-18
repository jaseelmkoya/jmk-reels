"""Aeroplane-lift reel with JMK's cloned AI voice (ElevenLabs eleven_v4, 18 Nov; JMK asked "ഓഡിയോ ElevenLabs-ൽ നിന്ന് എടുത്തോളൂ").
'vacuum' was misread as 'വക്കം' → that sentence regenerated as 'വാക്വം' and spliced in at 35.02 s (+0.83 s; vo/ splice notes in STATUS.md).
Word starts from eleven_scribe_v1 (below, original timeline; sh() applies the splice shift).
Every scene, caption and quiz beat is retimed to the spoken words (full re-render, never a voice laid over the old video).
Voice files vo_airplane*.wav are gitignored (never commit them). PLAT=yt → YouTube cut ("Subscribe ചെയ്യൂ")."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import airplane_lift as mc
from captions import Captions

YT = os.environ.get("PLAT") == "yt"
CUT, D = 35.02, 0.83
def sh(t): return t if t < CUT else t + D
Y, W_, C, O, P, G, R = mc.YELLOW, mc.WHITE, mc.CYAN, mc.ORANGE, mc.PINK, mc.GREEN, mc.RED

# (display line, highlight, spoken word starts on the original take — one start per display token)
L = [
 ("അഞ്ഞൂറ് ടണ്ണിലേറെ ഭാരമുള്ള *Airbus* *A380*… വായുവിൽ നിൽക്കുന്നത് എങ്ങനെ?", Y, [0.08, 0.64, 1.227, 1.92, 2.48, 3.68, 4.08, 4.48]),
 ("School-ൽ പഠിച്ച കഥ: മുകളിലെയും താഴത്തെയും *air* ഒരേ സമയം പിന്നിൽ എത്തണം.", W_, [5.456, 5.68, 5.92, 6.56, 7.2, 7.92, 8.32, 8.56, 8.92, 9.16]),
 ("പക്ഷേ… ഇത് *myth* ആണ്! മുകളിലെ *air* ആദ്യം എത്തും. അത്ര വേഗത്തിലാണ് ഒഴുക്ക്.", R, [9.98, 10.8, 11.12, 11.44, 12.08, 12.56, 12.96, 13.2, 13.76, 14.12, 14.64]),
 ("അപ്പോൾ മുകളിൽ *velocity* എന്തുകൊണ്ട് കൂടുന്നു? രണ്ട് കാരണം.", Y, [15.36, 15.88, 16.48, 16.76, 17.16, 17.92, 18.24]),
 ("Wing-ന്റെ വളഞ്ഞ മുകൾഭാഗവും ചെരിവും, *angle* *of* *attack*, മുകളിലെ *streamlines*-നെ അടുപ്പിക്കുന്നു.", C, [18.96, 19.44, 19.88, 20.6, 21.36, 21.6, 21.84, 22.32, 22.8, 23.52]),
 ("ഒഴുകാനുള്ള *area* കുറഞ്ഞാൽ *velocity* കൂടും. ഇതാണ് *equation* *of* *continuity*. Hose pipe അമർത്തുമ്പോൾ വെള്ളം ദൂരെ പോകുന്നത് പോലെ!", Y,
  [24.4, 25.04, 25.36, 26.08, 26.36, 26.92, 27.44, 27.92, 28.12, 28.96, 29.32, 29.48, 30.12, 30.48, 30.8, 31.2]),
 ("പിന്നെ, air വളഞ്ഞ wing-നൊപ്പം താഴേക്ക് തിരിയുന്നു. നേരെ പോയാൽ wing-നടുത്ത് *vacuum* വരും. ചുറ്റുമുള്ള air അതിനെ wing-ലേക്ക് അമർത്തുന്നു.", P,
  [31.913, 32.64, 32.88, 33.2, 33.92, 34.32] + [CUT - 0.15 + x for x in (0.16, 0.56, 1.32, 2.24, 2.68)] + [37.333, 37.92, 38.2, 38.48, 38.96]),
 ("വളഞ്ഞ വഴിയിൽ പോകാൻ centre-ലേക്ക് ഒരു *centripetal* *force* വേണം. കല്ല് ചരടിൽ കെട്ടി കറക്കുമ്പോൾ ചരടിന്റെ *tension* പോലെ.", Y,
  [39.76, 40.16, 40.48, 40.92, 41.627, 41.84, 42.48, 42.76, 43.387, 43.68, 44.04, 44.28, 44.96, 45.44, 45.84]),
 ("പക്ഷേ… air-ന് ചരടില്ല! തള്ളാൻ *pressure* മാത്രമേ ഉള്ളൂ. മുകളിൽ നിന്ന് *atmospheric* *pressure* താഴേക്ക് തള്ളുന്നു. *Net* *force* താഴേക്ക് കിട്ടാൻ wing-നടുത്തെ *pressure* അതിലും കുറവായിരിക്കണം.", O,
  [46.4, 47.2, 47.6, 48.56, 49.08, 49.4, 49.76, 50.32, 50.66, 50.96, 51.72, 52.0, 52.4, 53.04, 53.4, 53.6, 54.04, 54.56, 55.32, 55.6, 55.96]),
 ("മുന്നിലെ *high* *pressure* air-നെ ഈ *low* *pressure*-ലേക്ക് തള്ളുന്നു. അങ്ങനെ *speed* കൂടുന്നു!", C,
  [56.88, 57.4, 57.68, 57.92, 58.48, 58.56, 58.8, 59.36, 60.08, 60.48, 60.8]),
 ("*Bernoulli's* *principle:* P + ½ρv² + ρgh = *constant*", Y, [61.84, 62.28, 63.68, 63.92, 64.08, 65.44, 66.16, 66.64, 67.28]),
 ("ചുരുക്കത്തിൽ: മുകളിൽ *velocity* കൂടുതൽ, *pressure* കുറവ്. താഴെ *pressure* കൂടുതൽ.", C, [67.84, 68.64, 69.28, 69.6, 70.293, 70.48, 71.147, 71.68, 71.92]),
 ("ഈ *pressure* *difference* wing-നെ മുകളിലേക്ക് തള്ളുന്നു. ഇതാണ് *lift*!", G, [72.64, 72.72, 73.04, 73.52, 73.96, 74.48, 75.2, 75.92]),
 ("ഒപ്പം wing *air*-നെ താഴേക്ക് തള്ളുന്നു. ഇതാണ് *action*.", O, [76.4, 77.04, 77.2, 77.6, 78.0, 78.56, 79.12]),
 ("*Air* wing-നെ മുകളിലേക്ക് തള്ളുന്നു. ഇതാണ് *reaction*!", G, [79.84, 80.08, 80.48, 80.96, 81.6, 82.08]),
]
for txt, _, ts in L: assert len(txt.split()) == len(ts), (txt, len(txt.split()), len(ts))
LS = [[sh(x) for x in ts] for _, _, ts in L]
Q0 = sh(83.04)                                   # "ഇനി quiz!"
IG_END = 95.45
YT_SUB = 94.787                                  # "Subscribe ചെയ്യൂ" in vo_airplane_yt.wav
END = (YT_SUB + 1.15) if YT else IG_END

# scenes: s1 L0 | s2 L1-2 | s_cont L3-5 | s_curve L6-7 | s_press L8-9 | s3 L10-12 (Bernoulli) | s4 L13-14 | s5 quiz
first = [0, 1, 3, 6, 8, 10, 13]
B = [0.0] + [LS[i][0] - 0.15 for i in first[1:]] + [Q0 - 0.15, END + 1.0]
S = [round(B[i + 1] - B[i], 3) for i in range(8)]
ST = B[:]
# original line indices (mc.starts) → new line starts (mc LINES 0..13 ↔ L 0,1,2,3,4,5,6,7,8,9,11,12,13,14)
MAP = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]
starts = [LS[k][0] for k in MAP]

words, lines = [], []
for (txt, hl, _), ts in zip(L, LS):
    lines.append((txt, hl)); words += [{"start": x} for x in ts]
CAP = Captions.from_words(lines, words + [{"start": Q0}], size=52, maxw=8)

mc.S, mc.ST, mc.starts, mc.CAP = S, ST, starts, CAP

# s_press: atmospheric / net-force / low-P beats were at fixed times → warp to the spoken words
_press = mc.s_press
def s_press(fr, t, d):
    ev = starts[9] - ST[4]
    kx = [0, sh(50.96) - ST[4], sh(53.04) - ST[4], sh(54.56) - ST[4], ev]
    ky = [0, 3.0, 5.2, 6.6, ev]
    if t < ev:
        for i in range(4):
            if t <= kx[i + 1]:
                t = ky[i] + (t - kx[i]) * (ky[i + 1] - ky[i]) / (kx[i + 1] - kx[i]); break
    _press(fr, t, d)
mc.s_press = s_press
_caps = mc.caps
def s_press_c(fr, t, d):                         # captions must use real time
    mc.caps = lambda *a, **k: None
    s_press(fr, t, d)
    mc.caps = _caps
    CAP.draw(fr, ST[4] + t, 1340)

# quiz on the voice
qt = dict(pyq=sh(84.16) - Q0, q=sh(86.912) - Q0, a=sh(90.0) - Q0, b=sh(91.44) - Q0, cmt=sh(92.48) - Q0,
          fol=(YT_SUB if YT else sh(93.893)) - Q0)
FOL = mc.text_img("*Subscribe* ചെയ്യൂ" if YT else "*Follow* ചെയ്യൂ", 56, max_w=900, hl=Y)
def s5(fr, t, d):
    mc.show_clip(fr, "c5", min(t, 9.8), dark=0.55)
    fr.paste(mc.VIG, (0, 0), mc.VIG)
    mc.appear(fr, mc.QUIZ, mc.W / 2, 290, t, 0.0, pop=True)
    mc.appear(fr, mc.PYQ, mc.W / 2, 385, t, qt["pyq"], pop=True)
    mc.appear(fr, mc.Q, mc.W / 2, 480, t, qt["q"] - 0.1)
    for (c, tx, cx), st in zip(((mc.OPT_A, mc.TA, 280), (mc.OPT_B, mc.TB, 800)), (qt["a"], qt["b"])):
        mc.appear(fr, c, cx, 860, t, st - 0.1, pop=True)
        if t > st:
            mc.paste(fr, tx, cx, 902, mc.ease_out(mc.prog(t, st - 0.05, 0.3)))
    mc.appear(fr, mc.CMT, mc.W / 2, 1110, t, qt["cmt"], pop=True)
    mc.appear(fr, FOL, mc.W / 2, 1270, t, qt["fol"], pop=True)

SCENES = [(S[i], f) for i, f in enumerate((mc.s1, mc.s2, mc.s_cont, mc.s_curve, s_press_c, mc.s3, mc.s4, s5))]
HANDLE = getattr(mc, "HANDLE", "")
VOICE = "vo_airplane_yt.wav" if YT else "vo_airplane.wav"
MUSIC_GAIN = 0.3
MUSIC = [(0.0, "hype"), (ST[1], "tension"), (ST[2], "curious"), (ST[3], "space"), (ST[4], "tension"), (ST[5], "curious"), (ST[6], "drive"), (ST[7], "uplift")]
SFX = [(0.0, "whoosh"), (0.4, "engine"), (4.0, "thud"), (4.3, "pop"), (LS[2][2], "thud"),
       (starts[3], "boing"), (starts[5], "ding"), (LS[6][9], "thud"), (starts[7], "pop"),
       (sh(50.96), "whoosh"), (starts[9], "whoosh"),
       (ST[5] + 0.2, "pop"), (LS[12][7], "ding"), (LS[13][6], "whoosh"), (LS[14][5], "ding"),
       (ST[7] + 0.0, "pop"), (ST[7] + qt["a"], "pop"), (ST[7] + qt["b"], "pop"), (ST[7] + qt["fol"], "chime")]
for s_ in ST[1:-1]: SFX.append((s_ - 0.05, "swoosh"))
if __name__ == "__main__":
    print("S", S, "total", round(B[-1], 2)); print("starts", [round(x, 2) for x in starts]); print(qt)
