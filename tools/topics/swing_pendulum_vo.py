"""Voiced version of swing_pendulum.py (JMK cloned AI voice, 13 Nov 2026).
Word times from ElevenLabs scribe (topics/pendulum_words.json, 125 spoken words, one-to-one with SPOKEN below).
Silence GAPS are inserted into the voice at scene changes (vo/pendulum_voice.wav); captions use the shifted times.
Display tokens of each block are mapped onto that block's spoken words by linear interpolation."""
import os, json
_HERE = os.path.dirname(os.path.abspath(__file__))
SPOKEN_COUNTS = [("H0", 7), ("T0", 4), ("HOOK", 10), ("TEASE", 3), ("CAP1", 5), ("WHY", 3), ("DEFP", 7), ("SHM", 8),
                 ("DEF", 17), ("DEF_ML", 7), ("LEN", 4), ("BOT", 7), ("F1", 13), ("F2", 9), ("F3", 7), ("Q", 9), ("CMT", 3), ("FOL", 2)]
GAPS = [(5.86, 0.5), (16.12, 0.8), (25.08, 0.6), (35.52, 3.4), (37.48, 1.0), (40.60, 0.8), (56.76, 1.0)]  # (cut time in raw voice, silence s)
TAIL = 2.5
_W = json.load(open(os.path.join(_HERE, "pendulum_words.json")))
def shift(t): return t + sum(g for c, g in GAPS if c <= t)
_ST = [shift(x) for x in _W["starts"]]
VOICE_END = shift(_W["end"])

def _retime(g):
    BL = g["BLOCKS"]; k = 0; wt = {}
    for key, n in SPOKEN_COUNTS:
        sp = _ST[k:k + n]; k += n
        nd = len(BL[key][2].split())
        out = []
        for i in range(nd):
            f = i * (n - 1) / (nd - 1) if nd > 1 else 0.0
            j = int(f); fr = f - j
            out.append(sp[j] if j + 1 >= n else sp[j] + fr * (sp[j + 1] - sp[j]))
        wt[key] = out
    assert k == len(_ST)
    first = {1: "HOOK", 2: "WHY", 3: "DEF", 4: "LEN", 5: "F1", 6: "Q"}
    S0 = [0.0] + [wt[first[i]][0] - 0.35 for i in range(1, 7)]
    END = VOICE_END + TAIL
    D = [S0[i + 1] - S0[i] for i in range(6)] + [END - S0[6]]
    g.update(D=D, S0=S0, END=END, WT=wt)

def _events(g):
    WT, S0 = g["WT"], g["S0"]
    q = WT["Q"]
    g["EV"] = dict(MASS=S0[1] + 0.6, LBL=S0[2] + 2.4, FORM=WT["DEF_ML"][-1] + 0.8, NOM=WT["DEF_ML"][-1] + 1.6,
                   PROP=WT["LEN"][-1] + 0.6, EXAM=S0[6] + 0.4, OPT_A=q[-3] - 0.1, OPT_B=q[-1] - 0.1, SRC=S0[5] + 3.0)

_src = open(os.path.join(_HERE, "swing_pendulum.py")).read()
_m1 = next(l for l in _src.splitlines(True) if l.startswith('WT["H0"]'))
_m2 = "          EXAM=S0[6] + 0.4, OPT_A=S0[6] + 5.0, OPT_B=S0[6] + 5.4, SRC=S0[5] + 3.0)\n"
assert _m1 in _src and _m2 in _src
_src = _src.replace(_m1, _m1 + "_retime(globals())\n").replace(_m2, _m2 + "_events(globals())\n")
_src = _src.replace("VOICE = None", 'VOICE = "vo/pendulum_voice.wav"')
exec(compile(_src, os.path.join(_HERE, "swing_pendulum.py"), "exec"), globals())
