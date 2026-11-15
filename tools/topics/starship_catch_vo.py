"""Starship catch reel with JMK's cloned AI voice (ElevenLabs eleven_v4), JMK asked 15 Nov 23:24.
Word starts from eleven_scribe_v1 in starship_words.json; spoken lines in work/2026-11-16_starship_catch/starship_voice_lines.py.
Every scene, caption, card and quiz beat is retimed to the spoken words (full re-render, never a voice laid over the old video).
Voice file tools/vo_starship.wav is gitignored (never commit it)."""
import sys, os, json, re, difflib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(HERE, "..", "..", "work", "2026-11-16_starship_catch"))
import starship_catch as mc
from starship_voice_lines import SPOKEN
from captions import Captions

_W = json.load(open(os.path.join(HERE, "starship_words.json")))
WT = [w["text"] for w in _W["words"]]; WS = [w["start"] for w in _W["words"]]; END = _W["end"]

def _norm(s): return re.sub(r"[^\wഀ-ൿ]", "", s.lower())
# align each spoken line to its first transcript word (greedy, tolerant to small tokenisation differences)
START = {}; k = 0
for i, (key, text) in enumerate(SPOKEN):
    first = _norm(text.split()[0]); best = None
    for j in range(max(0, k - 3), min(len(WT), k + 8)):
        r = difflib.SequenceMatcher(None, first, _norm(WT[j])).ratio()
        if best is None or r > best[0] + 0.05 or (abs(r - best[0]) <= 0.05 and abs(j - k) < abs(best[1] - k)):
            if r >= 0.5 and (best is None or r >= best[0] - 0.05): best = (r, j)
    j = best[1] if best else k
    START[key] = j; k = j + len(text.split())
KEYS = [key for key, _ in SPOKEN]
def t0(key): return WS[START[key]]
def span(key):
    i = KEYS.index(key); a = START[key]
    b = START[KEYS[i + 1]] if i + 1 < len(KEYS) else len(WS)
    return WS[a:b]

# scenes
SC_KEYS = [["L0"], ["L1", "L2"], ["L3", "L4"], ["L5", "L6"], ["L7", "L8"], ["L9", "L10", "L11", "L12"], ["L13"],
           ["L14", "L15", "L16", "L17"], ["L18", "L19"], ["L20", "L21", "L22"], ["L23", "L24"], ["L25", "L26", "L27"], []]
B = [0.0] + [t0(ks[0]) - 0.15 for ks in SC_KEYS[1:-1]] + [t0("QZ") - 0.15, END + 1.2]
S = [round(B[i + 1] - B[i], 3) for i in range(13)]
ST = B[:]

# captions: the reel's display lines, word times interpolated over each line's spoken words
DISP = [ln for _, _, lines in mc.SC for ln in lines]
LKEYS = [k for ks in SC_KEYS for k in ks]
assert len(DISP) == len(LKEYS) == 28
lines, words, CAPL = [], [], []
for (txt, hl), key in zip(DISP, LKEYS):
    sp = span(key); nd = len(txt.split()); n = len(sp)
    for i in range(nd):
        f = i * (n - 1) / (nd - 1) if nd > 1 else 0.0
        a = int(f); fr = f - a
        words.append({"start": sp[a] if a + 1 >= n else sp[a] + fr * (sp[a + 1] - sp[a])})
    lines.append((txt, hl)); CAPL.append((txt, sp[0], None, hl))
words.append({"start": t0("LAW")})          # placeholder end for L6 page (fixed below)
# from_words: the page after the last word of a line ends at the next line's first word
CAP = Captions.from_words(lines, words[:-1] + [{"start": t0("QZ")}], size=52, maxw=9)

mc.S, mc.ST, mc.CAP, mc.CAPL = S, ST, CAP, CAPL
mc.HKB = t0("HB") - 0.1
mc.HK = t0("HC") - 0.1
q0 = ST[12]
mc.QT = dict(q=t0("QQ") - q0, a=t0("QA") - q0, b=t0("QB") - q0, cmt=t0("QC") - q0, fol=t0("QF") - q0)
SCENES = [(S[i], f) for i, f in enumerate(mc.FNS)]
HANDLE = getattr(mc, "HANDLE", "")
VOICE = "vo_starship.wav"
MUSIC = [(0.0, "hype"), (ST[1], "cinematic"), (ST[4], "space"), (ST[7], "tension"), (ST[9], "hype"), (ST[11], "uplift")]
MUSIC_GAIN = 0.32
la = mc.line_at
HK = mc.HK
SFX = [(0.0, "thud"), (0.05, "whoosh"), (mc.HKB, "whoosh"), (HK, "ding"), (HK + 3.6, "pop")]
for s_ in ST[1:-1]: SFX.append((s_ - 0.05, "swoosh"))
SFX += [(ST[1] + la(1, 1) + 0.6, "pop"), (ST[3] + 0.8, "pop"), (ST[3] + 1.2, "pop"), (ST[5] + la(5, 2), "ding"),
        (ST[7] + la(7, 2), "pop"), (ST[9] + la(9, 2), "pop"), (ST[10] + 0.2, "chime"), (ST[10] + la(10, 1), "ding"),
        (ST[12] + 0.05, "pop"), (q0 + mc.QT["a"], "pop"), (q0 + mc.QT["b"], "pop"), (q0 + mc.QT["fol"], "chime")]
if __name__ == "__main__":
    print("S", S, "total", round(B[-1], 2)); print("HKB", round(mc.HKB, 2), "HK", round(mc.HK, 2), mc.QT)
    for key in KEYS: print(key, START[key], WT[START[key]], round(t0(key), 2))
