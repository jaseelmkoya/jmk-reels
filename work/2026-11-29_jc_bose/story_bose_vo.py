"""J.C. Bose story with the ElevenLabs voice-over (JMK's cloned voice, 15 Nov). All timing from
story_bose_words.json (eleven_scribe_v1 word starts). Voice file tools/vo_bose.wav is gitignored."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import story_bose as sb
from captions import Captions
from reelkit import YELLOW, CYAN

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = json.load(open(os.path.join(HERE, "story_bose_words.json")))
WS = [w["start"] for w in WORDS]
END = 74.56
def first(line): return next(i for i, w in enumerate(WORDS) if w["line"] == line)
L = [WS[first(n)] for n in range(11)]          # line starts: 0 hook … 10 quiz
def at(text, after=0.0):                        # start time of the first word containing text after `after`
    return next(w["start"] for w in WORDS if text in w["text"] and w["start"] >= after)

# scenes: s0 hook = line 0, s1..s9 = lines 1..9, s10 = quiz (line 10)
B = [0.0] + [L[n] - 0.15 for n in range(1, 11)] + [END + 0.9]
S0 = round(B[1] - B[0], 3)
S = [round(B[i + 1] - B[i], 3) for i in range(1, 11)]
ST = B[1:]                                      # ST[k] = start of scene s(k+1), as in story_bose

def rel(t, k): return round(t - ST[k], 3)       # k = 0..9 for s1..s10
TM = dict(hook2=at("എന്നിട്ടും"), hook3=at("നിങ്ങളുടെ"),
          name=rel(at("ജഗദീഷ്"), 1), gun=rel(at("gunpowder"), 3),
          eq1=rel(at("അഞ്ച്", L[6]), 5), eq2=rel(at("equals"), 5) - 0.2, eq3=rel(at("അറുപത്"), 5),
          mw=rel(at("Microwaves!"), 5), pills=rel(at("5G-യും"), 5),
          q=rel(at("RADAR"), 9), optA=rel(at("A,"), 9), optB=rel(at("B,"), 9),
          cmt=rel(at("ഉത്തരം"), 9), fol=rel(at("Follow"), 9))

# captions: display tokens one-to-one with spoken tokens after merging number words etc.
DISPLAY = {
    1: ("*1895.* Marconi radio കണ്ടുപിടിക്കുന്നതിന് രണ്ട് വർഷം മുമ്പ്…", YELLOW, [(0, 4)]),
    2: ("Kolkata-യിലെ Presidency College-ൽ ഒരു ഇന്ത്യൻ ശാസ്ത്രജ്ഞൻ ഒരു *spark* *transmitter* ഓൺ ചെയ്തു. *ജഗദീഷ്* *ചന്ദ്ര* *ബോസ്.*", YELLOW, []),
    3: ("*23* *metre* അകലെ, *രണ്ട്* *ചുവരുകൾക്കപ്പുറം…*", CYAN, []),
    4: ("ഒരു *മണി* തനിയെ മുഴങ്ങി! ഒരു ചെറിയ *gunpowder* പൊട്ടിത്തെറിച്ചു!", sb.RED, []),
    5: ("ആരും ഒന്നും തൊട്ടില്ല. ചുവരുകൾ കടന്നത് കണ്ണിന് കാണാനാവാത്ത *electromagnetic* *waves* ആയിരുന്നു.", CYAN, []),
    6: ("Wavelength വെറും *5* *mm.* *c=fλ* വെച്ച് നോക്കിയാൽ frequency ഏകദേശം *60* *GHz.* *Microwaves!* ഇന്ന് *5G*-യും *car* *radar*-ഉം ഉപയോഗിക്കുന്ന അതേ waves!", YELLOW, [(4, 4)]),
    7: ("പക്ഷേ ബോസ് *patent* എടുത്തില്ല. അറിവ് *എല്ലാവർക്കുമുള്ളതാണ്* എന്നായിരുന്നു അദ്ദേഹത്തിന്റെ വിശ്വാസം.", sb.RED, []),
    8: ("1897-ൽ London-ലെ Royal Institution-ൽ പോലും അദ്ദേഹം ഇത് കാണിച്ചു. പക്ഷേ radio-യുടെ ക്രെഡിറ്റ് *Marconi*-ക്ക് പോയി.", YELLOW, [(0, 4)]),
    9: ("2012-ൽ *IEEE* ബോസിന്റെ പരീക്ഷണത്തെ ലോകത്തിലെ ആദ്യ *millimetre-wave* *communication* ആയി അംഗീകരിച്ചു.", YELLOW, [(0, 2), (2, 3)]),
}
lines, words = [], []
for n in range(1, 10):
    text, hl, merges = DISPLAY[n]
    sp = [w for w in WORDS if w["line"] == n]
    starts = [w["start"] for w in sp]
    for a, k in sorted(merges, reverse=True):
        starts[a:a + k] = [starts[a]]
    assert len(starts) == len(text.split()), (n, len(starts), len(text.split()))
    lines.append((text, hl)); words += [{"start": s} for s in starts]
words.append({"start": L[10]})                 # last page ends when the quiz starts
CAP = Captions.from_words(lines, words, size=54, maxw=9)

sb.S0, sb.S, sb.ST, sb.CAP = S0, S, ST, CAP
sb.TM.update(TM)
SCENES = [(S0, sb.s0)] + [(S[i], f) for i, f in enumerate((sb.s1, sb.s2, sb.s3, sb.s4, sb.s5, sb.s6, sb.s7, sb.s8, sb.s9, sb.s10))]
HANDLE = getattr(sb, "HANDLE", "")
VOICE = "vo_bose.wav"
MUSIC = [(0.0, "tension"), (ST[0], "cinematic"), (ST[2], "tension"), (ST[5], "electric"), (ST[6], "cinematic"), (ST[8], "uplift")]
SFX = [(ST[0] - 0.05, "whoosh"), (ST[2] - 0.05, "swoosh"), (ST[3] + TM["gun"], "pop"),
       (ST[4] - 0.05, "swoosh"), (ST[5] - 0.05, "whoosh"), (ST[5] + TM["eq3"], "ding"), (ST[5] + TM["mw"], "pop"),
       (ST[6] - 0.05, "swoosh"), (ST[7] - 0.05, "swoosh"), (ST[8] + 0.2, "chime"),
       (ST[9], "pop"), (ST[9] + TM["optA"], "pop"), (ST[9] + TM["optB"], "pop"), (ST[9] + TM["fol"], "chime")]
if __name__ == "__main__":
    print("S0", S0, "S", S, "total", round(ST[-1] if False else B[-1], 2)); print(TM)
