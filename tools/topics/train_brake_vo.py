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

# ---------- clips from JMK (14 Nov): the derailment animation + NDTV cockpit footage ----------
# Frames are extracted (not committed) into CLIPDIR/<kind>/NNN.jpg, 1080x1920, 30 fps — see work/.../STATUS.md
from PIL import Image as _Im, ImageEnhance as _En
CLIPDIR = os.environ.get("TB_CLIPS", "/home/claude/clips")
ANIM = "ANIMATION · ILLUSTRATIVE (NOT REAL FOOTAGE)"
EV['slash'] = w(95, 4)                     # "Brake വീഴില്ല" — after the gauge clip
# (scene, start, end [scene time], frame dir, label, first frame, last frame, fade in, fade out)
CLIPS = [(0, 2.8, w(10, 0), "anim", ANIM, 0, 83, True, False),          # derailment · "…പാളം തെറ്റി"
         (0, w(10, 0), S[0], "cock", "COCKPIT FOOTAGE · NDTV", 0, 128, False, True),   # "Loco pilot പറഞ്ഞത്…"
         (2, w(45, 2), w(45, 2) + 2.1, "spark", ANIM, 5, 47, True, True),          # "Friction വഴി … heat"
         (4, 0.0, w(94, 4) + 0.5, "gauge", ANIM, 8, 57, False, True)]                     # "BP pressure കുറഞ്ഞില്ലെങ്കിൽ …"
_LAB = {}
SHOW_LABELS = False   # JMK (14 Nov): no on-screen ANIMATION / NDTV labels
def _lab(txt):
    if txt not in _LAB: _LAB[txt] = tb.mono(txt, size=24, color=(255, 230, 150))
    return _LAB[txt]
def _clip_frame(kind, u, f0, f1):
    fs = sorted(os.listdir(os.path.join(CLIPDIR, kind)))
    i = min(f1, f0 + int(u * (f1 - f0 + 1)))
    im = _Im.open(os.path.join(CLIPDIR, kind, fs[i])).convert("RGB")
    return _En.Brightness(im).enhance(0.72).convert("RGBA")

def _overlay(si, lay, t):
    if si == 0:
        tb.paste(lay, tb.H1, tb.W / 2, 230, 1.0); tb.paste(lay, tb.C1, tb.W / 2, 380, 1.0)
        tb.appear(lay, tb.QUOTE, tb.W / 2, 470, t, EV['quote'], pop=True)
        tb.appear(lay, tb.QUOTE_BY, tb.W / 2, 470 + tb.QUOTE.height + 10, t, EV['quote'] + 0.4)
        tb.appear(lay, tb.SAFE, tb.W / 2, 1200, t, 2.0); tb.paste(lay, tb.SRC, tb.W / 2, 1265, 1.0)
    elif si == 2:
        tb.paste(lay, tb.H3, tb.W / 2, 200, 1.0); tb.paste(lay, tb.C3, tb.W / 2, 320, 1.0)
    elif si == 4:
        tb.paste(lay, tb.H5, tb.W / 2, 200, 1.0); tb.paste(lay, tb.C5, tb.W / 2, 330, 1.0)
    tb.caps(lay, si, t)

def _with_clips(si, fn):
    mine = [c for c in CLIPS if c[0] == si]
    def g(fr, t, d):
        fn(fr, t, d)
        for _, a0, a1, kind, lab, f0, f1, fin, fout in mine:
            if a0 <= t < a1:
                al = min(1.0, (t - a0) / 0.2 if fin else 1.0, (a1 - t) / 0.2 if fout else 1.0)
                lay = _clip_frame(kind, (t - a0) / (a1 - a0), f0, f1)
                lay.alpha_composite(tb.VIG)
                if SHOW_LABELS: tb.paste(lay, _lab(lab), tb.W / 2, 1140 if si == 0 else 1250, 1.0)
                _overlay(si, lay, t)
                if al >= 1.0: fr.paste(lay.convert(fr.mode), (0, 0))
                else: fr.paste(_Im.blend(fr.convert("RGBA"), lay, al).convert(fr.mode), (0, 0))
    return g
SCENES = [(dd, _with_clips(i, fn)) for i, (dd, fn) in enumerate(SCENES)]
SFX = [x for x in SFX if x[1] != "thud" or x[0] < ST[4]] + [(ST[4] + EV['slash'], "thud"), (ST[2] + w(45, 2), "brake")]
