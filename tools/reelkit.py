"""reelkit — tiny engine for 1080x1920 animated physics reels (Malayalam + English).

A topic file defines SCENES = [(duration_s, draw_fn), ...] where draw_fn(fr, t, d) draws
on frame `fr` (RGB PIL Image, background already painted) at scene time t (seconds).
Run: python3 reelkit.py topic_file.py out.mp4
"""
import os, sys, math, random, subprocess, wave, importlib.util, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts")
FONT_FILES = {
    ("ml", "bold"): f"{FD}/NotoSansMalayalam-Bold.ttf",
    ("ml", "reg"): f"{FD}/NotoSansMalayalam-Regular.ttf",
    ("lat", "bold"): "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    ("lat", "reg"): "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
    ("sym", "bold"): "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ("sym", "reg"): "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}
for k, p in list(FONT_FILES.items()):
    if not os.path.exists(p):  # fall back to DejaVu if Inter missing
        FONT_FILES[k] = FONT_FILES[("sym", k[1])]

# palette
BG1, BG2 = (9, 14, 38), (30, 18, 70)
WHITE, MUTED = (245, 247, 255), (169, 177, 214)
CYAN, ORANGE, YELLOW, GREEN, PINK, RED = (79, 209, 255), (255, 159, 67), (255, 209, 102), (91, 228, 155), (255, 107, 157), (255, 92, 92)

_fc = {}
def font(kind, weight, size):
    key = (kind, weight, size)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(FONT_FILES[(kind, weight)], size, layout_engine=ImageFont.Layout.RAQM)
    return _fc[key]

SYMBOLS = set("∝×÷→←↑↓≈≠≤≥√πθλΔΣΩμ°±∞·²³½")
def script_of(c):
    if "ഀ" <= c <= "ൿ" or c in "‌‍":
        return "ml"
    if c in SYMBOLS:
        return "sym"
    return "lat"

def runs(word):
    out, cur, kind = [], "", None
    for c in word:
        k = script_of(c)
        if kind is None or k == kind:
            cur += c; kind = k
        else:
            out.append((kind, cur)); cur, kind = c, k
    if cur:
        out.append((kind, cur))
    return out

def text_img(s, size=64, weight="bold", color=WHITE, max_w=900, align="center", hl=YELLOW, lh=1.5):
    """Render mixed-script text to an RGBA image. Wrap *words* in asterisks to colour them `hl`.
    Use '|' for a forced line break."""
    space = font("lat", weight, size).getlength(" ")
    lines, line, lw = [], [], 0
    on = False  # '*' toggles highlight; a span may cover several words ("*uniform motion*-ൽ")
    for para in s.split("|"):
        for raw in para.split():
            rs = []
            for i, seg in enumerate(raw.split("*")):
                if i > 0: on = not on
                if seg:
                    rs += [(k, t, font(k, weight, size), hl if on else color) for k, t in runs(seg)]
            if not rs: continue
            ww = sum(f.getlength(t) for _, t, f, _ in rs)
            add = ww + (space if line else 0)
            if line and lw + add > max_w:
                lines.append((line, lw)); line, lw = [], 0; add = ww
            line.append((rs, ww)); lw += add
        lines.append((line, lw)); line, lw = [], 0
    lhp = int(size * lh)
    img = Image.new("RGBA", (max_w, lhp * len(lines) + int(size * 0.3)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for i, (ln, w) in enumerate(lines):
        x = (max_w - w) / 2 if align == "center" else 0
        base = i * lhp + int(size * 1.05)
        for rs, ww in ln:
            for k, t, f, col in rs:
                d.text((x, base), t, font=f, fill=col, anchor="ls")
                x += f.getlength(t)
            x += space
    return img

# ---------- easing / helpers ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, start, dur): return clamp((t - start) / dur) if dur > 0 else float(t >= start)
def ease_out(x): return 1 - (1 - x) ** 3
def ease_in_out(x): return 3 * x * x - 2 * x * x * x
def ease_back(x, s=1.7):
    x -= 1
    return x * x * ((s + 1) * x + s) + 1

def paste(fr, layer, cx, y, alpha=1.0, scale=1.0, dy=0):
    """Paste RGBA layer centred horizontally at cx, top at y."""
    if alpha <= 0.01 or scale <= 0.01:
        return
    oh = layer.height
    if abs(scale - 1) > 0.01:
        layer = layer.resize((max(1, int(layer.width * scale)), max(1, int(layer.height * scale))), Image.BICUBIC)
    if alpha < 0.999:
        a = layer.getchannel("A").point(lambda v: int(v * alpha))
        layer = layer.copy(); layer.putalpha(a)
    top = y + dy + (oh - layer.height) / 2
    fr.paste(layer, (int(cx - layer.width / 2), int(top)), layer)

def appear(fr, layer, cx, y, t, start, out_at=None, pop=False):
    """Fade/slide (or pop) a layer in at `start`, optional fade out at `out_at`."""
    p = prog(t, start, 0.45)
    a = ease_out(p)
    if out_at is not None:
        a *= 1 - prog(t, out_at, 0.35)
    if pop:
        paste(fr, layer, cx, y, a, 0.6 + 0.4 * ease_back(p) if p < 1 else 1.0)
    else:
        paste(fr, layer, cx, y, a, 1.0, dy=(1 - ease_out(p)) * 40)

def pill(text, size=34, fg=(9, 14, 38), bg=CYAN, pad=(28, 14)):
    t = text_img(text, size, "bold", fg, max_w=1000, lh=1.35)
    bbox = t.getbbox() or (0, 0, 10, 10)
    t = t.crop((bbox[0], 0, bbox[2], t.height))
    w, h = t.width + pad[0] * 2, int(size * 1.6) + pad[1]
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=bg)
    img.paste(t, (pad[0], (h - t.height) // 2 + int(size * 0.08)), t)
    return img

def boxed(layer, pad=22, fill=(9, 14, 38, 215), outline=None):
    """Put a text layer on a dark rounded box (for labels over busy drawings)."""
    bb = layer.getbbox() or (0, 0, layer.width, layer.height)
    t = layer.crop(bb)
    img = Image.new("RGBA", (t.width + pad * 2, t.height + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=24, fill=fill, outline=outline, width=3)
    img.paste(t, (pad, pad), t)
    return img

def card(w, h, fill=(255, 255, 255, 18), outline=(255, 255, 255, 50), r=36):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=fill, outline=outline, width=3)
    return img

def arrow(d, x1, y1, x2, y2, col, w=10, head=34):
    d.line((x1, y1, x2, y2), fill=col, width=w)
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - head * math.cos(a - 0.45), y2 - head * math.sin(a - 0.45))
    p2 = (x2 - head * math.cos(a + 0.45), y2 - head * math.sin(a + 0.45))
    d.polygon([(x2 + 6 * math.cos(a), y2 + 6 * math.sin(a)), p1, p2], fill=col)

class SS:
    """Supersampled drawing layer for smooth (anti-aliased) shapes in a region."""
    def __init__(self, w, h, k=2):
        self.w, self.h, self.k = w, h, k
        self.img = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)
    def s(self, *v): return [x * self.k for x in v]
    def done(self): return self.img.resize((self.w, self.h), Image.LANCZOS)

# ---------- background ----------
def make_bg():
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(-1, 1, W)[None, :]
    g = np.zeros((H, W, 3))
    for i in range(3):
        g[..., i] = BG1[i] * (1 - y) + BG2[i] * y
    glow = np.exp(-((x - 0.3) ** 2 * 2.2 + (y - 0.35) ** 2 * 5)) * 28
    g[..., 2] += glow; g[..., 1] += glow * 0.4
    vig = 1 - 0.35 * (x ** 2 + (y * 2 - 1) ** 2) / 2
    g *= vig[..., None]
    img = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    for gx in range(0, W, 90):
        d.line((gx, 0, gx, H), fill=(255, 255, 255, 0) if False else (40, 44, 90), width=1)
    for gy in range(0, H, 90):
        d.line((0, gy, W, gy), fill=(40, 44, 90), width=1)
    # soften grid
    return Image.blend(Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)), img, 0.35)

random.seed(7)
STARS = [(random.uniform(0, W), random.uniform(0, H), random.uniform(1, 3.2), random.uniform(0, 6.28), random.uniform(4, 14)) for _ in range(70)]

def paint_bg(bg, T):
    fr = bg.copy()
    d = ImageDraw.Draw(fr)
    for x, y, r, ph, sp in STARS:
        yy = (y - T * sp) % H
        b = int(110 + 90 * math.sin(T * 1.7 + ph))
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=(b, b, min(255, b + 40)))
    return fr

# ---------- watermark (Instagram + YouTube, with profile pictures) ----------
BRAND = [  # (platform label, handle, profile picture file, ring colour)
    ("Instagram", "@jmk.space", f"{HERE}/brand/ig.jpg", (225, 48, 108)),
    ("YouTube", "@jaseelmkoyajmk", f"{HERE}/brand/yt.jpg", (255, 0, 0)),
]
_wm = None
def _avatar(path, ring, initials, size=64):
    k = 4; S = size * k
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.ellipse((0, 0, S - 1, S - 1), fill=ring + (255,))
    inner = S - 6 * k
    if os.path.exists(path):
        ph = Image.open(path).convert("RGB")
        m = min(ph.size); ph = ph.crop(((ph.width - m) // 2, (ph.height - m) // 2, (ph.width + m) // 2, (ph.height + m) // 2)).resize((inner, inner), Image.LANCZOS)
        mask = Image.new("L", (inner, inner), 0); ImageDraw.Draw(mask).ellipse((0, 0, inner - 1, inner - 1), fill=255)
        img.paste(ph, (3 * k, 3 * k), mask)
    else:  # placeholder until the real picture is added to brand/
        d.ellipse((3 * k, 3 * k, S - 3 * k, S - 3 * k), fill=(30, 34, 70, 255))
        f = font("lat", "bold", int(S * 0.36))
        d.text((S / 2, S / 2), initials, font=f, fill=WHITE, anchor="mm")
    return img.resize((size, size), Image.LANCZOS)

def watermark():
    global _wm
    if _wm is None:
        parts = []
        for label, handle, path, ring in BRAND:
            av = _avatar(path, ring, "JMK")
            lab = font("lat", "bold", 20); hf = font("lat", "bold", 28)
            tw = int(max(lab.getlength(label), hf.getlength(handle)))
            part = Image.new("RGBA", (64 + 14 + tw, 64), (0, 0, 0, 0)); pd = ImageDraw.Draw(part)
            part.paste(av, (0, 0), av)
            pd.text((78, 4), label, font=lab, fill=ring if label == "YouTube" else (255, 120, 170))
            pd.text((78, 28), handle, font=hf, fill=WHITE)
            parts.append(part)
        gap, pad = 36, 14
        w = sum(p.width for p in parts) + gap * (len(parts) - 1) + pad * 2 + 16
        img = Image.new("RGBA", (w, 64 + pad * 2), (0, 0, 0, 0))
        ImageDraw.Draw(img).rounded_rectangle((0, 0, w - 1, img.height - 1), radius=img.height // 2, fill=(9, 14, 38, 150), outline=(255, 255, 255, 40), width=2)
        x = pad + 8
        for p in parts:
            img.paste(p, (x, pad), p); x += p.width + gap
        _wm = img
    return _wm

WM_Y = 1620  # JMK wants the watermark at the bottom (keep slide content above y≈1590)
def footer(fr, d, handle):
    paste(fr, watermark(), W / 2, WM_Y, 0.92)

# ---------- music ----------
def make_music(path, dur, sr=44100):
    n = int(dur * sr); t = np.arange(n) / sr
    chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
    out = np.zeros(n)
    seg = 4.0
    for i in range(int(math.ceil(dur / seg))):
        a, b = int(i * seg * sr), min(n, int((i + 1) * seg * sr + 0.8 * sr))
        tt = t[a:b] - i * seg
        env = np.minimum(1, tt / 0.9) * np.exp(-np.maximum(0, tt - seg) * 3)
        for m in chords[i % 4]:
            f = 440 * 2 ** ((m - 69) / 12)
            out[a:b] += env * (np.sin(2 * np.pi * f * tt) * 0.5 + np.sin(2 * np.pi * f * 2.001 * tt) * 0.12)
        fb = 440 * 2 ** ((chords[i % 4][0] - 12 - 69) / 12)
        out[a:b] += env * np.sin(2 * np.pi * fb * tt) * 0.5
        # soft pulse on beats
        for k in range(8):
            s0 = a + int(k * 0.5 * sr)
            if s0 >= n: break
            L = min(int(0.25 * sr), n - s0)
            tk = np.arange(L) / sr
            out[s0:s0 + L] += np.sin(2 * np.pi * 2 * fb * tk) * np.exp(-tk * 14) * 0.35
    out *= np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 1.5)
    out = out / (np.abs(out).max() + 1e-9) * 0.28
    pcm = (out * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())

# ---------- render ----------
def render(topic_path, out_path, only=None, stills=None):
    spec = importlib.util.spec_from_file_location("topic", topic_path)
    topic = importlib.util.module_from_spec(spec); spec.loader.exec_module(topic)
    scenes = topic.SCENES
    handle = getattr(topic, "HANDLE", "")
    bg = make_bg()
    work = os.path.join(os.path.dirname(os.path.abspath(out_path)), "_work")
    os.makedirs(work, exist_ok=True)
    T0 = 0.0
    if stills:  # list of (scene_index, t) -> PNGs for checking
        starts = np.cumsum([0] + [s[0] for s in scenes])
        for si, t in stills:
            fr = paint_bg(bg, starts[si] + t); d = ImageDraw.Draw(fr)
            scenes[si][1](fr, t, d); footer(fr, d, handle)
            fr.save(os.path.join(work, f"still_{si}_{t:.1f}.png"))
        return
    files = []
    for i, (dur, fn) in enumerate(scenes):
        f = os.path.join(work, f"scene_{i:02d}.mp4"); files.append(f)
        if only is not None and i not in only and os.path.exists(f):
            T0 += dur; continue
        tmp = f[:-4] + ".tmp.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                              "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
        nf = int(round(dur * FPS))
        for k in range(nf):
            t = k / FPS
            fr = paint_bg(bg, T0 + t); d = ImageDraw.Draw(fr)
            fn(fr, t, d); footer(fr, d, handle)
            p.stdin.write(fr.tobytes())
        p.stdin.close()
        if p.wait() != 0:
            raise SystemExit(f"ffmpeg failed on scene {i}")
        os.replace(tmp, f)
        T0 += dur
        print(f"scene {i} done", flush=True)
    total = sum(s[0] for s in scenes)
    lst = os.path.join(work, "list.txt")
    with open(lst, "w") as fh:
        fh.writelines(f"file '{x}'\n" for x in files)
    silent = os.path.join(work, "video.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
    mus = os.path.join(work, "music.wav"); make_music(mus, total)
    tmp = out_path[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", mus, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out_path)
    print("wrote", out_path)

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
