"""Cinematic 'science story' reel style: big uppercase headline with one coloured word,
small mono caption, SOURCE strip, Malayalam subtitle, location pins, slow camera push.
Built on reelkit (same watermark/footer, size, fps)."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reelkit import *

POP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "comic-neue-latin-700-normal.ttf")  # Chalkboard-style English
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
_f = {}
def F(path, size):
    k = (path, size)
    if k not in _f: _f[k] = ImageFont.truetype(path, size)
    return _f[k]

def headline(words, size=92, hl=YELLOW, max_w=1000):
    """words: 'A SMALL *CHURCH*' – starred words in colour. Auto-shrinks to one line."""
    toks = words.split()
    while True:
        f = F(POP, size); sp = f.getlength(" ")
        w = sum(f.getlength(t.strip("*")) for t in toks) + sp * (len(toks) - 1)
        if w <= max_w or size < 50: break
        size -= 4
    h = int(size * 1.35)
    img = Image.new("RGBA", (int(w) + 40, h + 30), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d, ds = ImageDraw.Draw(img), ImageDraw.Draw(sh)
    x = 20
    for t in toks:
        c = hl if t.startswith("*") else WHITE
        t = t.strip("*")
        ds.text((x + 3, 12 + 5), t, font=f, fill=(0, 0, 0, 200))
        d.text((x, 12), t, font=f, fill=c)
        x += f.getlength(t) + sp
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    sh.alpha_composite(img)
    return sh

def mono(text, size=22, color=(220, 225, 240)):
    f = F(MONO, size)
    w = int(f.getlength(text)) + 30
    img = Image.new("RGBA", (w, size + 18), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, size + 17), radius=6, fill=(0, 0, 0, 150))
    d.text((15, 8), text, font=f, fill=color)
    return img

def source(items, size=24):
    f = F(MONO, size)
    lab = "SOURCE  "
    txt = "  ·  ".join(items)
    w = int(f.getlength(lab + txt)) + 36
    img = Image.new("RGBA", (w, size + 22), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, size + 21), radius=8, fill=(8, 10, 20, 210), outline=(255, 255, 255, 70), width=2)
    d.text((18, 10), lab, font=f, fill=YELLOW)
    d.text((18 + f.getlength(lab), 10), txt, font=f, fill=WHITE)
    return img

def subtitle(text, size=52, hl=YELLOW):
    t = text_img(text, size, max_w=980, hl=hl, lh=1.45)
    bb = t.getbbox()
    t = t.crop((0, 0, t.width, bb[3] + 6)) if bb else t
    sh = Image.new("RGBA", t.size, (0, 0, 0, 0))
    a = t.getchannel("A").point(lambda v: int(v * 0.9))
    sh.paste((0, 0, 0, 255), (0, 0), a)
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    out = Image.new("RGBA", (t.width, t.height + 6), (0, 0, 0, 0))
    out.alpha_composite(sh, (0, 4)); out.alpha_composite(sh, (0, 4)); out.alpha_composite(t, (0, 0))
    return out

def pin_label(text, size=26, dot=YELLOW):
    f = F(POP, size)
    w = int(f.getlength(text)) + 70
    h = size + 26
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=(8, 10, 20, 225))
    d.ellipse((18, h / 2 - 8, 34, h / 2 + 8), fill=dot)
    d.text((46, h / 2), text, font=f, fill=WHITE, anchor="lm")
    return img

def push(base, t, dur, z0=1.0, z1=1.08, cx=0.5, cy=0.5):
    """Slow camera push on a pre-drawn background (base is >= W x H)."""
    p = ease_in_out(clamp(t / dur))
    z = z0 + (z1 - z0) * p
    w, h = int(W / z * base.width / W), int(H / z * base.height / H)
    w = int(base.width / z); h = int(base.height / z)
    x0 = int((base.width - w) * cx); y0 = int((base.height - h) * cy)
    return base.crop((x0, y0, x0 + w, y0 + h)).resize((W, H), Image.BILINEAR)

def vignette():
    y, x = np.mgrid[0:H, 0:W]
    r = np.sqrt(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H / 2) / (H * 0.62)) ** 2)
    a = (np.clip(r - 0.55, 0, 1) * 300).clip(0, 190).astype(np.uint8)
    v = Image.new("RGBA", (W, H), (0, 0, 0, 0)); v.putalpha(Image.fromarray(a))
    return v
VIG = vignette()

def grad(w, h, stops):
    """vertical gradient: stops = [(pos0..1, (r,g,b)), ...]"""
    ys = np.linspace(0, 1, h)
    cols = np.zeros((h, 3))
    for c in range(3):
        cols[:, c] = np.interp(ys, [s[0] for s in stops], [s[1][c] for s in stops])
    arr = np.repeat(cols[:, None, :], w, axis=1).astype(np.uint8)
    return Image.fromarray(arr, "RGB").convert("RGBA")

def standard_overlay(fr, t, head, sub, src=None, cap=None, sub_at=0.5, head_at=0.15, sub2=None, sub2_at=None):
    """Headline at top, caption + source + Malayalam subtitle in the lower third."""
    fr.paste(VIG, (0, 0), VIG)
    p = ease_out(prog(t, head_at, 0.5))
    paste(fr, head, W / 2, 230 + (1 - p) * 30, p)
    y = 1180
    if cap is not None:
        paste(fr, cap, W / 2, y, ease_out(prog(t, head_at + 0.4, 0.5))); y += cap.height + 14
    if src is not None:
        paste(fr, src, W / 2, y, ease_out(prog(t, head_at + 0.5, 0.5))); y += src.height + 24
    else:
        y += 10
    if sub is None:
        return y
    if sub2 is not None and sub2_at is not None and t >= sub2_at:
        appear(fr, sub2, W / 2, y, t, sub2_at)
    else:
        appear(fr, sub, W / 2, y, t, sub_at, out_at=(sub2_at - 0.35) if sub2_at else None)
