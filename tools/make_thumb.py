"""JMK thumbnail style (learned from JMK's own SpaceX thumbnail, 16 Nov 2026). Use this for every reel cover / thumbnail.

The look:
  * 1080x1920, one dramatic REAL photo/frame of the subject filling the frame (subject on one side, usually left/centre),
    graded cinematic: darker, higher contrast, cool blue/teal shadows, warm highlights, dark vignette,
    red/orange glow creeping in from the edges and a few flying embers/sparks.
  * TOP: a huge Malayalam claim in bright YELLOW, very heavy font, thick dark outline + red outer glow
    (e.g. "ചരിത്രം കുറിച്ച്"), then a short English punch word in big WHITE condensed caps ("SPACE X!").
  * MIDDLE (beside the subject): 2–3 short Malayalam lines in the same yellow style that say what happened
    ("റോക്കറ്റിനെ / കൈകൊണ്ട് / പിടിച്ച് ടവർ!").
  * BOTTOM-RIGHT: JMK's shocked reaction cut-out (hands on head), large, overlapping the frame edge.
  * Few words, all CAPS-energy, no small text, no logos, no watermark clutter. The first line is the curiosity hook.

Usage:
  python3 make_thumb.py BG.jpg OUT.jpg --top "ചരിത്രം കുറിച്ച്" --en "SPACE X!" --mid "റോക്കറ്റിനെ|കൈകൊണ്ട്|പിടിച്ച് ടവർ!" \
         [--face brand/faces/jmk_shock.png] [--focus 0.35] [--side right]
"""
import argparse, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
ML = os.path.join(HERE, "fonts", "AnekMalayalam-ExtraBold.ttf")
EN = os.path.join(HERE, "fonts", "BebasNeue-Regular.ttf")
YEL = (255, 232, 20)

def font(path, size): return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)

def fit_font(text, path, max_w, start, lo=60):
    s = start
    while s > lo:
        f = font(path, s)
        if f.getbbox(text)[2] - f.getbbox(text)[0] <= max_w: return f
        s -= 4
    return font(path, lo)

def grade(bg, focus):
    """cover-fit + cinematic grade"""
    r = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * r) + 1, int(bg.height * r) + 1), Image.LANCZOS)
    x = int((bg.width - W) * focus); y = (bg.height - H) // 2
    bg = bg.crop((x, y, x + W, y + H)).convert("RGB")
    bg = ImageOps.autocontrast(bg, cutoff=2)
    bg = bg.point(lambda v: int(255 * (v / 255) ** 1.15))
    bg = bg.filter(ImageFilter.UnsharpMask(radius=3, percent=120, threshold=2))
    bg = ImageEnhance.Contrast(bg).enhance(1.35)
    bg = ImageEnhance.Color(bg).enhance(1.25)
    # cool shadows / warm highlights (teal-orange)
    r_, g_, b_ = bg.split()
    r_ = r_.point(lambda v: int(min(255, (v / 255) ** 1.12 * 255 * 1.04)))
    g_ = g_.point(lambda v: int((v / 255) ** 1.08 * 255))
    b_ = b_.point(lambda v: int(min(255, 255 * ((v / 255) ** 0.92) + 10)))
    bg = Image.merge("RGB", (r_, g_, b_))
    bg = ImageEnhance.Brightness(bg).enhance(0.9)
    # dark top for the headline + vignette
    ov = Image.new("L", (W, H), 0); d = ImageDraw.Draw(ov)
    for i in range(H):
        a = 0
        if i < 700: a = int(120 * (1 - i / 700) ** 1.4)
        d.line((0, i, W, i), fill=a)
    bg = Image.composite(Image.new("RGB", (W, H), (5, 10, 25)), bg, ov)
    vig = Image.new("L", (W, H), 0); dv = ImageDraw.Draw(vig)
    dv.ellipse((-W * 0.35, -H * 0.2, W * 1.35, H * 1.2), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(160))
    bg = Image.composite(bg, Image.new("RGB", (W, H), (0, 0, 0)), vig)
    return bg

def edge_glow(img):
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(g)
    for (box, col) in [((-260, 200, 90, H + 200), (255, 40, 20, 150)), ((W - 70, 900, W + 260, H + 200), (255, 60, 20, 120)),
                       ((-200, H - 220, W + 200, H + 300), (255, 90, 20, 150))]:
        d.ellipse(box, fill=col)
    g = g.filter(ImageFilter.GaussianBlur(90))
    img.alpha_composite(g)
    rnd = random.Random(7); sp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sp)
    for _ in range(40):
        x = rnd.choice([rnd.uniform(0, 200), rnd.uniform(0, 200), rnd.uniform(W - 160, W), rnd.uniform(0, W * 0.5)])
        y = rnd.uniform(H * 0.3, H)
        r = rnd.uniform(1.5, 4); a = rnd.randint(140, 240); ang = rnd.uniform(-0.6, 0.6)
        ds.line((x, y, x + ang * 18, y - r * 6), fill=(255, rnd.randint(70, 150), 30, a), width=int(r))
    img.alpha_composite(sp.filter(ImageFilter.GaussianBlur(1.2)))
    img.alpha_composite(sp.filter(ImageFilter.GaussianBlur(6)))

LAT = os.path.join(HERE, "fonts", "BebasNeue-Regular.ttf")
def _is_ml(ch): return "\u0d00" <= ch <= "\u0d7f" or ch in "\u200c\u200d"
def runs(text, f):
    """split mixed Malayalam/Latin text: Malayalam glyphs in the Malayalam font, the rest (Latin, digits, ! ?) in Bebas"""
    if f.path != ML: return [(text, f)]
    lat = font(LAT, int(f.size * 1.08)); out = []
    for ch in text:
        ff = f if (_is_ml(ch) or (ch == " " and out and out[-1][1] is f)) else lat
        if out and out[-1][1] is ff: out[-1] = (out[-1][0] + ch, ff)
        else: out.append((ch, ff))
    return out
def text_w(text, f): return sum(ff.getlength(t) for t, ff in runs(text, f))

def glow_text(img, text, f, x, y, fill, stroke_col=(60, 0, 0), stroke=14, glow=(255, 30, 0), anchor="ls"):
    """y is the baseline; anchor[0] in l/m/r"""
    rs = runs(text, f); tw = sum(ff.getlength(t) for t, ff in rs)
    x0 = x - tw if anchor[0] == "r" else (x - tw / 2 if anchor[0] == "m" else x)
    def draw(d, dx, dy, fl, sw, sf):
        xx = x0 + dx
        for t, ff in rs:
            d.text((xx, y + dy), t, font=ff, fill=fl, stroke_width=sw, stroke_fill=sf, anchor="ls"); xx += ff.getlength(t)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw(ImageDraw.Draw(lay), 0, 0, glow + (255,), stroke + 14, glow + (255,))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(22)))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw(ImageDraw.Draw(sh), 6, 8, (0, 0, 0, 200), stroke, (0, 0, 0, 200))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    draw(ImageDraw.Draw(img), 0, 0, fill, stroke, stroke_col)

def fit_ml(text, max_w, start, lo=70):
    s = start
    while s > lo and text_w(text, font(ML, s)) > max_w: s -= 4
    return font(ML, s)

def make(bg_path, out, top, en, mid, face=None, focus=0.35, side="right"):
    img = grade(Image.open(bg_path), focus).convert("RGBA")
    edge_glow(img)
    # TOP: Malayalam claim (yellow) + English punch (white)
    ft = fit_ml(top, W - 110, 180)
    tl = [top]
    if ft.size < 112 and " " in top:
        ws = top.split(" "); best = None
        for i in range(1, len(ws)):
            a_, b_ = " ".join(ws[:i]), " ".join(ws[i:]); m = max(text_w(a_, font(ML, 100)), text_w(b_, font(ML, 100)))
            if best is None or m < best[0]: best = (m, [a_, b_])
        tl = best[1]; ft = min((fit_ml(l, W - 110, 170) for l in tl), key=lambda f_: f_.size)
    ty = 330 if len(tl) == 1 else 250
    for l in tl:
        glow_text(img, l, ft, W // 2, ty, YEL, anchor="ms"); ty += int(ft.size * 1.0)
    en_y = max(640, ty + 150)
    if en:
        fe = fit_font(en, EN, int(W * 0.62), 300)
        ex = W - 50 if side == "right" else 50
        glow_text(img, en, fe, ex, en_y, (255, 255, 255), stroke_col=(20, 20, 30), stroke=6, glow=(0, 0, 0),
                  anchor="rs" if side == "right" else "ls")
    # MIDDLE: what happened, beside the subject
    lines = [l for l in mid.split("|") if l] if mid else []
    if lines:
        fm = min((fit_ml(l, int(W * 0.6), 160) for l in lines), key=lambda f: f.size)
        y = max(1050, en_y + 330)
        for l in lines:
            mx = W - 50 if side == "right" else 50
            glow_text(img, l, fm, mx, y, YEL, anchor="rs" if side == "right" else "ls")
            y += int(fm.size * 1.05)
    # JMK reaction bottom corner
    if face and os.path.exists(face):
        fc = Image.open(face).convert("RGBA"); bb = fc.getbbox(); fc = fc.crop(bb)
        s = (W * 0.6) / fc.width; fc = fc.resize((int(fc.width * s), int(fc.height * s)), Image.LANCZOS)
        if side != "right": fc = ImageOps.mirror(fc)
        fx = W - fc.width + 20 if side == "right" else -20
        shadow = Image.new("RGBA", fc.size, (0, 0, 0, 0)); shadow.putalpha(fc.split()[3].point(lambda v: int(v * 0.6)))
        img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(18)), (fx - 18, H - fc.height + 10))
        img.alpha_composite(fc, (fx, H - fc.height))
    img.convert("RGB").save(out, quality=93)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("bg"); ap.add_argument("out")
    ap.add_argument("--top", required=True); ap.add_argument("--en", default="")
    ap.add_argument("--mid", default=""); ap.add_argument("--face", default=os.path.join(HERE, "brand", "faces", "jmk_shock.png"))
    ap.add_argument("--focus", type=float, default=0.35); ap.add_argument("--side", default="right")
    a = ap.parse_args()
    print(make(a.bg, a.out, a.top, a.en, a.mid, a.face, a.focus, a.side))
