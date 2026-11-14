"""Train-brake story (15 Nov 2026) with the ElevenLabs voice-over (JMK's cloned voice).
Everything is timed from the transcript word starts in train_brake_words.json (eleven_scribe_v1).
Voice file tools/vo_train_brake.wav is gitignored (never commit it)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import train_brake as tb
from reelkit import YELLOW, CYAN, ORANGE
from captions import Captions

RED = tb.RED
WORDS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "train_brake_words.json")))
WS = [w["start"] for w in WORDS]
END = 63.12
LINE_START = [0, 10, 19, 30, 45, 54, 74, 88, 100, 112]          # word index of each spoken line
L = [WS[i] for i in LINE_START]

# scenes: S1 lines 1-2 · S2 line 3 · S3 lines 4-5 · S4 lines 6-7 · S5 line 8 · S6 line 9 · S7 quiz (line 10)
B = [0.0, L[2] - 0.15, L[3] - 0.15, L[5] - 0.15, L[7] - 0.15, L[8] - 0.15, L[9] - 0.15, END + 1.0]
S = [round(B[i + 1] - B[i], 3) for i in range(7)]
ST = B[:]

CAP = Captions.from_words([
    ("നവംബർ 11-ന് അസമിൽ *കൊൽക്കത്ത–സൈരംഗ്* Express-ന്റെ engine-ഉം അഞ്ച് coach-ഉം *പാളം* *തെറ്റി.*", RED),
    ("Loco pilot പറഞ്ഞത്: *BP* *pressure* *കുറയുന്നില്ല!* എന്താണ് ഈ *BP?*", YELLOW),
    ("Train ഓടുമ്പോൾ *brake* *pipe*-ൽ *5* *kg* per *sq.* *cm* *pressure* നിറച്ചുവെക്കും.", CYAN),
    ("Brake ഇടാൻ driver ഈ *pressure* കുറയ്ക്കുന്നു. അപ്പോൾ *air* *brake* *cylinder*-ലേക്ക് കയറി *brake* *block* wheel-ൽ അമരുന്നു.", YELLOW),
    ("*Friction* വഴി *kinetic* *energy* *heat* ആയി മാറുന്നു. Train നിൽക്കുന്നു.", ORANGE),
    ("Brake block-നെ തള്ളുന്ന *force* എവിടെ നിന്ന്? *F* *=* *P* *×* *A.* *Pressure* is the normal *force* acting per unit *area.*", YELLOW),
    ("ചെറിയ *pressure,* വലിയ *area,* വലിയ *force.* ഒരു brake cylinder ഏകദേശം *37,000* *newton* force ഉണ്ടാക്കുന്നു!", CYAN),
    ("*BP* *pressure* കുറഞ്ഞില്ലെങ്കിൽ *brake* *cylinder*-ൽ *air* എത്തില്ല. Brake വീഴില്ല. യഥാർത്ഥ കാരണം *അന്വേഷണത്തിലാണ്.*", RED),
    ("Car-ൽ *brake* *oil* വഴി *pressure* എല്ലാ wheel-ലേക്കും *ഒരുപോലെ* എത്തുന്നു. ഇതാണ് *Pascal's* *law.*", ORANGE),
], WORDS, size=52, maxw=9)

def w(i, scene):            # time of word i relative to the start of a scene
    return round(WS[i] - ST[scene], 3)

EV = dict(quote=w(13, 0),            # "BP pressure കുറയുന്നില്ല!"
          bp_drop=w(35, 2),          # "കുറയ്ക്കുന്നു"
          press=w(37, 2),            # "air"
          block=w(41, 2),            # "brake block"
          defn=w(65, 3),             # "Pressure is the normal force…"
          calc=(w(74, 3), w(76, 3), w(81, 3)),   # ചെറിയ pressure · വലിയ area · ഒരു brake cylinder
          slash=w(90, 4),            # "കുറഞ്ഞില്ലെങ്കിൽ"
          pedal=w(101, 5),           # "brake oil"
          f2=w(107, 5),              # "ഒരുപോലെ"
          pyq=w(114, 6),             # "Plus One exam"
          q=w(120, 6), optA=w(126, 6), optB=w(129, 6), cmt=w(132, 6), fol=w(135, 6))

tb.S, tb.ST, tb.CAP, tb.EV = S, ST, CAP, EV
tb.starts = [L[0], L[1], L[2], L[3], L[4], L[5], L[6], L[7], L[8]]
HANDLE = getattr(tb, "HANDLE", "")
SCENES = [(S[i], f) for i, f in enumerate((tb.s1, tb.s2, tb.s3, tb.s4, tb.s5, tb.s6, tb.s7))]
VOICE = "vo_train_brake.wav"
MUSIC = [(0.0, "tension"), (ST[1], "curious"), (ST[4], "tension"), (ST[5], "curious"), (ST[6], "uplift")]
SFX = [(0.0, "whoosh"), (WS[13], "pop"), (S[0] - 2.4, "brake"), (S[0] - 2.0, "thud")]
for s_ in ST[1:-1]: SFX.append((s_ - 0.05, "swoosh"))
SFX += [(ST[2] + EV['press'], "brake"), (ST[3] + EV['calc'][0], "pop"), (ST[3] + EV['calc'][1], "pop"), (ST[3] + EV['calc'][2], "ding"),
        (ST[4] + EV['slash'], "thud"), (ST[5] + 0.3, "pop"), (ST[6] + 0.05, "pop"), (ST[6] + EV['pyq'], "pop"),
        (ST[6] + EV['q'], "ticks"), (ST[6] + EV['optA'], "pop"), (ST[6] + EV['optB'], "pop"), (ST[6] + EV['fol'], "chime")]
if __name__ == "__main__":
    print("S", S, "total", round(sum(S), 2)); print("EV", EV)

# ---------- real clips JMK sent (14 Nov): animation of the derailment + NDTV cockpit footage ----------
# Frames pre-extracted (not committed) by make step in work/2026-11-15_train_brake/clips.md
from PIL import Image as _Im, ImageEnhance as _En
CLIPDIR = os.environ.get("TB_CLIPS", "/home/claude/clips")
CLIPS = [(2.8, WS[10], "anim", "ANIMATION · ILLUSTRATIVE (NOT REAL FOOTAGE)"),
         (WS[10], ST[1], "cock", "COCKPIT FOOTAGE · NDTV")]
_LAB = {k: tb.mono(lab, size=24, color=(255, 230, 150)) for _, _, k, lab in CLIPS}
def _clip_frame(kind, t):
    fs = sorted(os.listdir(os.path.join(CLIPDIR, kind)))
    i = min(len(fs) - 1, int(t * 30))
    if kind == "anim":   # stretch 50.0–52.8 s of the source over the window (avoid its press-release dissolve)
        i = min(83, int(t / (WS[10] - 2.8) * 84))
    im = _Im.open(os.path.join(CLIPDIR, kind, fs[i])).convert("RGB")
    return _En.Brightness(im).enhance(0.72).convert("RGBA")
def s1_clips(fr, t, d):
    tb.s1(fr, t, d)
    for a0, a1, kind, _ in CLIPS:
        if a0 <= t < a1:
            al = min(1.0, (t - a0) / 0.2) if kind == "anim" else min(1.0, (a1 - t) / 0.2)
            lay = _clip_frame(kind, t - a0)
            lay.alpha_composite(tb.VIG)
            from PIL import ImageDraw as _D
            ld = _D.Draw(lay)
            tb.paste(lay, tb.H1, tb.W / 2, 230, 1.0)
            tb.paste(lay, tb.C1, tb.W / 2, 380, 1.0)
            q0 = EV['quote']
            tb.appear(lay, tb.QUOTE, tb.W / 2, 470, t, q0, pop=True)
            tb.appear(lay, tb.QUOTE_BY, tb.W / 2, 470 + tb.QUOTE.height + 10, t, q0 + 0.4)
            tb.paste(lay, _LAB[kind], tb.W / 2, 1140, 1.0)
            tb.appear(lay, tb.SAFE, tb.W / 2, 1200, t, 2.0)
            tb.paste(lay, tb.SRC, tb.W / 2, 1265, 1.0)
            tb.caps(lay, 0, t)
            if al >= 1.0:
                fr.paste(lay.convert(fr.mode), (0, 0))
            else:
                fr.paste(_Im.blend(fr.convert("RGBA"), lay, al).convert(fr.mode), (0, 0))
SCENES[0] = (S[0], s1_clips)
