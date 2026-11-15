"""Munnar chill (15 Nov 2026) with JMK's cloned AI voice (ElevenLabs eleven_v4), JMK asked 15:45 IST.
Word starts from eleven_scribe_v1 in munnar_words.json (110 words). Voice file tools/vo_munnar.wav is gitignored
(never commit it). Scenes, captions, cards and SFX are retimed to the spoken words."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import munnar_chill as mc
from captions import Captions
from reelkit import YELLOW, CYAN, ORANGE

HERE = os.path.dirname(os.path.abspath(__file__))
_W = json.load(open(os.path.join(HERE, "munnar_words.json")))
WS = _W["starts"]; END = _W["end"]
# spoken lines (first word index): hook q 0 · L0 5 · L1 18 · L2 25 · L3 35 · L4 44 · L5 55 · L6 63 · L7 72 · quiz 93
IDX = [5, 18, 25, 35, 44, 55, 63, 72, 93, 110]

B = [0.0, WS[25] - 0.15, WS[35] - 0.15, WS[44] - 0.15, WS[63] - 0.15, WS[72] - 0.15, WS[93] - 0.15, END + 1.2]
S = [round(B[i + 1] - B[i], 3) for i in range(7)]
ST = B[:]
def rel(i, k): return round(WS[i] - ST[k], 3)

DISPLAY = [
    ("Nov 14-ന് Idukki Kundala-യിൽ *7.9°C*, Munnar-ൽ *9.7°C.*", CYAN, [(9, 4), (4, 4)]),
    ("കാരണം: തെളിഞ്ഞ ആകാശം, കാറ്റില്ല. എന്താണ് ഇതിലെ *physics?*", YELLOW, []),
    ("പകൽ സൂര്യന്റെ *heat* ഭൂമിയിൽ എത്തുന്നത് *radiation* വഴി, ഒരു *medium* ഇല്ലാതെ.", YELLOW, []),
    ("രാത്രി ഭൂമി ഈ *heat* *radiation* ആയി തിരികെ ആകാശത്തേക്ക് വിടുന്നു.", ORANGE, []),
    ("മേഘം ഉണ്ടെങ്കിൽ അത് ഈ *heat* *absorb* ചെയ്ത് ഭൂമിയിലേക്ക് തിരിച്ചു *radiate* ചെയ്യും.", CYAN, []),
    ("തെളിഞ്ഞ ആകാശത്തിൽ *heat* നേരെ space-ലേക്ക്. ഭൂമി വേഗം തണുക്കുന്നു.", CYAN, []),
    ("കാറ്റില്ലെങ്കിൽ തണുത്ത, *density* കൂടിയ air താഴ്വരയിൽ കെട്ടിക്കിടക്കും. രാവിലെ മഞ്ഞും.", CYAN, []),
    ("ഏത് body-യും *heat* *radiate* ചെയ്യും. *H* *=* *eσAT⁴.* *T* കൂടുമ്പോൾ *H* വളരെ വേഗം കൂടും.", YELLOW, [(7, 8)]),
]
lines, words = [], []
for n, (text, hl, merges) in enumerate(DISPLAY):
    starts = WS[IDX[n]:IDX[n + 1]]
    for a, k in merges:                      # given high index first
        starts[a:a + k] = [starts[a]]
    assert len(starts) == len(text.split()), (n, len(starts), len(text.split()))
    lines.append((text, hl)); words += [{"start": s} for s in starts]
words.append({"start": WS[93]})              # last caption page ends when the quiz starts
CAP = Captions.from_words(lines, words, size=52, maxw=9)

EV = dict(mc.EV)
EV.update(split=rel(55, 3), q=rel(95, 6), optA=rel(101, 6), optB=rel(103, 6), cmt=rel(105, 6), fol=rel(108, 6),
          pyq=rel(94, 6), modes=(rel(87, 5), rel(87, 5) + 0.5, rel(87, 5) + 1.0))
mc.S, mc.ST, mc.CAP, mc.EV = S, ST, CAP, EV
SCENES = [(S[i], f) for i, f in enumerate((mc.s1, mc.s2, mc.s3, mc.s4, mc.s5, mc.s6, mc.s7))]
HANDLE = getattr(mc, "HANDLE", "")
VOICE = "vo_munnar.wav"
MUSIC = [(0.0, "hype"), (ST[1], "drive"), (ST[4], "hype"), (ST[5], "drive"), (ST[6], "hype")]
MUSIC_GAIN = 0.32
SFX = [(0.0, "whoosh"), (4.5, "ding")]
for s_ in ST[1:-1]: SFX.append((s_ - 0.05, "swoosh"))
SFX += [(ST[1] + 0.6, "chime"), (ST[3] + 0.4, "pop"), (ST[3] + EV['split'] - 0.3, "pop"), (ST[5] + 0.2, "pop"),
        (WS[77], "ding"), (ST[5] + EV['modes'][0], "pop"), (ST[5] + EV['modes'][1], "pop"), (ST[5] + EV['modes'][2], "pop"),
        (ST[6] + 0.05, "pop"), (ST[6] + EV['optA'], "pop"), (ST[6] + EV['optB'], "pop"), (ST[6] + EV['fol'], "chime")]
if __name__ == "__main__":
    print("S", S, "total", round(sum(S), 2)); print(EV)
