"""Maglev reel · cinematic v2 + JMK's cloned AI voice (ElevenLabs eleven_v4, voice D6wSSgA3oM61Ljd71fAY), JMK asked 20 Nov ~16:00 IST.
Word starts from eleven_scribe_v1 in maglev_words.json. Every scene, caption, card and quiz beat is retimed to the spoken words
(full re-render, never a voice laid over the old video). Voice wavs (vo_maglev_ig/yt.wav) are never committed.
PLAT=yt → YouTube cut: the spoken 'Follow ചെയ്യൂ!' is cut out and 'Subscribe ചെയ്യൂ!' follows the quiz."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import maglev_cine as mc
from captions import Captions, _pages
from reelkit import text_img

YT = os.environ.get("PLAT") == "yt"
_W = json.load(open(os.path.join(HERE, "maglev_words.json")))
WT = [w["text"] for w in _W]; WS = [w["start"] for w in _W]; WE = [w["end"] for w in _W]

SPOKEN = [
    ("X", "[excited]"),
    ("H", "ഈ ട്രെയിൻ track തൊടുന്നേയില്ല!"),
    ("L0", "ജപ്പാനിലെ ഈ ട്രെയിൻ track തൊടാതെ ഏകദേശം പത്ത് സെന്റിമീറ്റർ ഉയർന്നാണ് ഓടുന്നത്. സ്പീഡ്, മണിക്കൂറിൽ അറുനൂറ്റി മൂന്ന് കിലോമീറ്റർ! World record!"),
    ("L1", "പക്ഷേ ഒരു twist: start ചെയ്യുമ്പോൾ ഇത് സാധാരണ wheels-ൽ ആണ് ഓടുന്നത്!"),
    ("L2", "ഏകദേശം മണിക്കൂറിൽ നൂറ്റമ്പത് കിലോമീറ്റർ കഴിഞ്ഞാൽ മാത്രമേ ഇത് ഉയരൂ. എന്തുകൊണ്ട്?"),
    ("L3", "ട്രെയിനിൽ ശക്തമായ superconducting magnets ഉണ്ട്. Track-ൽ വെറും coils. ഉയർത്താനുള്ള ഈ coils-ന് power supply ഇല്ല!"),
    ("L4", "Magnet മുകളിലൂടെ പായുമ്പോൾ coil-ലൂടെയുള്ള magnetic flux മാറുന്നു."),
    ("L5", "Flux മാറിയാൽ induced emf ഉണ്ടാകും. ഇതാണ് Faraday's law. അപ്പോൾ coil-ൽ induced current ഒഴുകുന്നു."),
    ("L6", "ഈ current ഏത് ദിശയിൽ? Lenz's law പറയുന്നു: flux-ലെ മാറ്റത്തെ എതിർക്കുന്ന ദിശയിൽ."),
    ("L7", "അങ്ങനെ coil തന്നെ ഒരു magnet ആകുന്നു. N-ന് നേരെ N! അത് magnet-നെ മുകളിലേക്ക് തള്ളുന്നു. ട്രെയിൻ ഉയരുന്നു!"),
    ("L8", "ഇനി speed. Induced emf, flux മാറുന്ന rate-ന് തുല്യമാണ്. പതുക്കെ പോയാൽ flux പതുക്കെ മാറും. emf ചെറുത്, തള്ളൽ കുറവ്."),
    ("L9", "വേഗം കൂടുമ്പോൾ emf-ഉം current-ഉം തള്ളലും എല്ലാം കൂടും. അതുകൊണ്ടാണ് നൂറ്റമ്പത് കിലോമീറ്റർ വരെ wheels!"),
    ("L11", "ആയിരത്തി എണ്ണൂറ്റി മുപ്പത്തൊന്നിൽ ലണ്ടനിൽ മൈക്കൽ ഫാരഡേ ഇത് ആദ്യം കണ്ടു: magnet നീക്കുമ്പോൾ മാത്രം galvanometer സൂചി അനങ്ങി!"),
    ("LAW", "Faraday's law: The magnitude of the induced emf equals the time rate of change of magnetic flux. Lenz's law: The induced current opposes the change in flux that produces it."),
    ("L10", "ഇതെല്ലാം Plus Two-വിലെ Electromagnetic Induction chapter-ലെ രണ്ട് നിയമങ്ങൾ!"),
    ("QZ", "Quiz time! Plus Two Christmas Exam രണ്ടായിരത്തി പത്തൊമ്പതിൽ വന്ന ചോദ്യം: Time rate of change of magnetic flux is? A, Induced emf. B, Induced current. ഉത്തരം comment ചെയ്യൂ!"),
    ("FOL", "Follow ചെയ്യൂ!"),
    ("SUB", "Subscribe ചെയ്യൂ!"),
]
IDX, k = {}, 0
for key, text in SPOKEN:
    toks = text.split()
    assert [w for w in WT[k:k + len(toks)]] == toks, (key, WT[k:k + len(toks)], toks)
    IDX[key] = (k, k + len(toks)); k += len(toks)
assert k == len(WT)
KEYS = [key for key, _ in SPOKEN]

# YouTube cut: drop 'Follow ചെയ്യൂ!' from the audio, everything after it moves earlier by CUT_D
F0, F1 = IDX["FOL"]
CUT_A, CUT_B = WS[F0] - 0.06, WS[F1] - 0.04          # [CUT_A, CUT_B) removed in the yt voice
CUT_D = CUT_B - CUT_A
def T(i):  # time of word i in this platform's voice
    t = WS[i]
    return t - CUT_D if (YT and t >= CUT_B) else t
def t0(key): return T(IDX[key][0])
def span(key): a, b = IDX[key]; return [T(i) for i in range(a, b)]
END_KEY = "SUB" if YT else "FOL"
VOICE_END = (WE[IDX["SUB"][1] - 1] - CUT_D) if YT else WE[IDX["FOL"][1] - 1]

# scenes: s0 [H, L0] · s1 [L1, L2] · s2 [L3, L4, L5] · s3 [L6, L7] · s4 [L8, L9] · hist [L11] · law [LAW, L10] · quiz [QZ, FOL/SUB]
B = [0.0] + [t0(k_) - 0.15 for k_ in ("L1", "L3", "L6", "L8", "L11", "LAW", "QZ")] + [VOICE_END + 1.3]
S = [round(B[i + 1] - B[i], 3) for i in range(8)]
mc.S, mc.ST = S, B[:]

# display line i ↔ spoken key; line start times for ls()
DKEY = {0: "L0", 1: "L1", 2: "L2", 3: "L3", 4: "L4", 5: "L5", 6: "L6", 7: "L7", 8: "L8", 9: "L9", 10: "L10", 11: "L11"}
mc.starts = [t0(DKEY[i]) for i in range(len(mc.LINES))]

# captions: display tokens spread over the line's spoken words; a line's last page ends at the next spoken key
def next_key_start(key):
    i = KEYS.index(key)
    return t0(KEYS[i + 1]) if i + 1 < len(KEYS) else VOICE_END + 1.0
CAP = Captions.__new__(Captions); CAP.size, CAP.items, CAP._cache = 52, [], {}
order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 10]
for li in order:
    txt, hl = mc.LINES[li]; key = DKEY[li]
    sp = span(key); n = len(sp); toks = txt.split(); nd = len(toks)
    times = []
    for i in range(nd):
        f = i * (n - 1) / (nd - 1) if nd > 1 else 0.0
        a = int(f); fr = f - a
        times.append(sp[a] if a + 1 >= n else sp[a] + fr * (sp[a + 1] - sp[a]))
    j = 0; pages = _pages(toks, 8)
    for p in pages:
        pt = times[j:j + len(p)]; j += len(p)
        p_end = times[j] if j < nd else min(next_key_start(key), sp[-1] + 2.5)
        CAP.items.append((p, hl, pt, pt[0], p_end))
mc.CAP = CAP

# scene-internal beats from word times
w = lambda key, n: T(IDX[key][0] + n)                      # n-th word of a spoken key
mc.TL = w("L2", 7) - B[1]                                   # lift on 'ഉയരൂ'
mc.C2_D = mc.TL - 2.8
mc.C4_END = w("L3", 5) - B[2]                               # 'Track-ൽ' → guideway coils clip
mc.C5_END = t0("L4") - B[2] - 0.2                           # 'Magnet …' → animation
mc.LZ_AT = w("LAW", 17) - B[6]                              # 'Lenz's law:'
mc.Q_A, mc.Q_B = w("QZ", 18) - B[7], w("QZ", 21) - B[7]     # 'A,' 'B,'
mc.Q_CMT = w("QZ", 24) - B[7]
mc.Q_FOL = (t0("SUB") if YT else t0("FOL")) - B[7]
if YT: mc.FOL = text_img("*Subscribe* ചെയ്യൂ", 58, max_w=900, hl=mc.YELLOW)
assert WT[IDX["L2"][0] + 7].startswith("ഉയരൂ") and WT[IDX["L3"][0] + 5] == "Track-ൽ" and WT[IDX["LAW"][0] + 17] == "Lenz's"
assert WT[IDX["QZ"][0] + 18] == "A," and WT[IDX["QZ"][0] + 21] == "B," and WT[IDX["QZ"][0] + 24] == "ഉത്തരം"

SCENES = [(S[i], f) for i, (_, f) in enumerate(mc.SCENES)]
HANDLE = mc.HANDLE
VOICE = "vo_maglev_yt.wav" if YT else "vo_maglev_ig.wav"
MUSIC_SEED = mc.MUSIC_SEED
MUSIC = [(0.0, "hype"), (B[1], "tension"), (B[2], "electric"), (B[3], "curious"), (B[4], "drive"), (B[5], "cinematic"), (B[6], "uplift"), (B[7], "tension"), (B[7] + mc.Q_FOL - 0.3, "uplift")]
SFX = [(0.0, "whoosh"), (2.2, "whoosh"), (B[1] + 0.1, "swoosh"), (B[1] + mc.C2_D, "swoosh"), (B[1] + mc.TL, "whoosh"), (B[1] + mc.TL + 0.1, "ding"),
       (B[2] + 0.1, "swoosh"), (B[2] + mc.C4_END, "swoosh"), (B[2] + mc.C4_END + 1.0, "zap"), (B[2] + mc.C5_END, "whoosh"),
       (w("L5", 3), "pop"), (w("L5", 9), "zap"),
       (B[3] + 0.1, "swoosh"), (t0("L7"), "boing"), (w("L7", 6), "pop"),
       (B[4] + 0.1, "swoosh"), (w("L8", 6), "pop"), (B[5] - 4.5, "whoosh"),
       (B[5] + 0.1, "swoosh"), (w("L11", 8), "zap"),
       (B[6] + 0.1, "pop"), (B[6] + 1.5, "ding"), (B[6] + mc.LZ_AT, "pop"),
       (B[7] + 0.1, "pop"), (B[7] + mc.Q_A, "pop"), (B[7] + mc.Q_B, "pop"), (B[7] + mc.Q_B + 1.4, "ticks"), (B[7] + mc.Q_FOL, "chime")]
MUSIC_GAIN = 0.4
if __name__ == "__main__":
    print("total", round(B[-1], 2), S, "TL", round(mc.TL, 2), "C4", round(mc.C4_END, 2), "C5", round(mc.C5_END, 2), "LZ", round(mc.LZ_AT, 2), "Q", mc.Q_A, mc.Q_B, mc.Q_CMT, mc.Q_FOL)
