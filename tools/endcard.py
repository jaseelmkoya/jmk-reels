"""Platform end-cards for JMK's reels (appended after the reel).

  Instagram version: profile card -> tap on a blue "Follow" button -> "Following", hearts pop.
  YouTube version:   channel card -> tap on red "SUBSCRIBE" -> "SUBSCRIBED" -> tap the bell -> bell rings.

Only the *button styles* of each app are imitated (colours/shapes); the apps' logos are NOT drawn.
Uses JMK's own profile pictures from brand/.

Usage:
  python3 endcard.py <final.mp4> <out_prefix>     -> <out_prefix>_ig.mp4 and <out_prefix>_yt.mp4
"""
import sys, os, math, subprocess, tempfile, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reelkit import (W, H, FPS, WHITE, YELLOW, make_bg, paint_bg, paste, text_img, font, ease_out, ease_in_out,
                     prog, clamp, footer, _avatar, BRAND, HERE)

DUR = 4.0
IG_BLUE = (0, 149, 246); GREY = (54, 56, 64); YT_RED = (255, 0, 0)

def _rr(w, h, r, fill, outline=None, ow=0):
    k = 3
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w * k - 1, h * k - 1), radius=r * k, fill=fill, outline=outline, width=ow * k)
    return im.resize((w, h), Image.LANCZOS)

def _button(label, bg, fg=WHITE, w=420, h=104, r=22, size=48, icon=None):
    b = _rr(w, h, r, bg + (255,))
    t = text_img(label, size, max_w=w, color=fg)
    bb = t.getbbox() or (0, 0, t.width, t.height)
    tw = bb[2] - bb[0]; th = bb[3] - bb[1]
    x = (w - tw) // 2 - bb[0]; y = (h - th) // 2 - bb[1]
    if icon == "check":
        vis_left = (w - tw) // 2 + 22          # text moves right to make room for the tick
        x += 22
        d = ImageDraw.Draw(b); cx, cy = vis_left - 34, h // 2
        d.line((cx - 14, cy, cx - 4, cy + 11, cx + 14, cy - 12), fill=fg, width=7, joint="curve")
    b.alpha_composite(t, (x, y)) if x >= 0 and y >= 0 else b.alpha_composite(t.crop((max(0, -x), max(0, -y), t.width, t.height)), (max(0, x), max(0, y)))
    return b

def _big_avatar(path, ring, size=260):
    return _avatar(path, ring, "JMK", size=size)

def _ig_ring_avatar(path, size=260):
    """Profile picture with a warm gradient ring (story-ring style, no logo)."""
    k = 3; S = size * k
    ring = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    y, x = np.mgrid[0:S, 0:S]
    ang = (np.arctan2(y - S / 2, x - S / 2) + math.pi) / (2 * math.pi)
    c1 = np.array([254, 218, 117]); c2 = np.array([250, 126, 30]); c3 = np.array([214, 41, 118]); c4 = np.array([150, 47, 191])
    t = ang[..., None]
    col = np.where(t < 1 / 3, c1 + (c2 - c1) * (t * 3), np.where(t < 2 / 3, c2 + (c3 - c2) * ((t - 1 / 3) * 3), c3 + (c4 - c3) * ((t - 2 / 3) * 3)))
    r = np.sqrt((x - S / 2) ** 2 + (y - S / 2) ** 2)
    a = ((r <= S / 2 - 1) & (r >= S / 2 - 9 * k)).astype(np.uint8) * 255
    ring = Image.fromarray(np.dstack([col.astype(np.uint8), a]), "RGBA")
    av = _avatar(path, (12, 16, 40), "JMK", size=S - 22 * k)
    ring.alpha_composite(av, (11 * k, 11 * k))
    return ring.resize((size, size), Image.LANCZOS)

def _bell(size=96, color=WHITE, ring=0.0, filled=False):
    """Generic bell icon. ring: rotation in degrees for the 'ringing' wiggle."""
    k = 4; S = size * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = S / 2; top = S * 0.16; bot = S * 0.72
    body = [(cx - S * 0.06, top), (cx + S * 0.06, top), (cx + S * 0.24, S * 0.38), (cx + S * 0.27, bot), (cx + S * 0.36, bot + S * 0.06),
            (cx - S * 0.36, bot + S * 0.06), (cx - S * 0.27, bot), (cx - S * 0.24, S * 0.38)]
    d.ellipse((cx - S * 0.25, top - S * 0.02, cx + S * 0.25, S * 0.5), fill=color if filled else None, outline=color, width=int(S * 0.06))
    if filled:
        d.polygon(body, fill=color)
    else:
        d.line(body + [body[0]], fill=color, width=int(S * 0.06), joint="curve")
    d.ellipse((cx - S * 0.08, bot + S * 0.07, cx + S * 0.08, bot + S * 0.2), fill=color)
    d.ellipse((cx - S * 0.04, top - S * 0.08, cx + S * 0.04, top + S * 0.0), fill=color)
    im = im.rotate(ring, resample=Image.BICUBIC, center=(cx, top))
    return im.resize((size, size), Image.LANCZOS)

def _tap(fr, x, y, t, t_tap):
    """Finger-tap cursor: dot moves in, presses (shrinks), ripple expands."""
    if t < t_tap - 0.55 or t > t_tap + 0.6: return
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    p = ease_out(prog(t, t_tap - 0.55, 0.45))
    cx = x + 140 * (1 - p); cy = y + 180 * (1 - p)
    press = 1 - 0.25 * math.exp(-((t - t_tap) / 0.07) ** 2)
    r = 30 * press
    a = int(230 * (1 - prog(t, t_tap + 0.3, 0.3)))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, a // 2), outline=(255, 255, 255, a), width=4)
    if t > t_tap:
        q = prog(t, t_tap, 0.5); rr = 30 + 90 * ease_out(q)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(255, 255, 255, int(200 * (1 - q))), width=5)
    fr.paste(L, (0, 0), L)

def _hearts(fr, x, y, t, t0):
    if t < t0 or t > t0 + 1.4: return
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(7):
        q = prog(t, t0 + i * 0.05, 1.0)
        if q <= 0 or q >= 1: continue
        ang = -math.pi / 2 + (i - 3) * 0.32
        hx = x + math.cos(ang) * 260 * ease_out(q); hy = y + math.sin(ang) * 260 * ease_out(q)
        s = 22 * (1 - 0.4 * q); a = int(255 * (1 - q))
        col = (255, 48, 108, a)
        d.ellipse((hx - s, hy - s, hx, hy), fill=col); d.ellipse((hx, hy - s, hx + s, hy), fill=col)
        d.polygon([(hx - s, hy - s * 0.45), (hx + s, hy - s * 0.45), (hx, hy + s)], fill=col)
    fr.paste(L, (0, 0), L)

def _card_bg():
    return _rr(860, 780, 48, (14, 18, 44, 235), (255, 255, 255, 40), 2)

_CACHE = {}
def _c(key, fn):
    if key not in _CACHE: _CACHE[key] = fn()
    return _CACHE[key]

def frame_ig(fr, t):
    a = ease_out(prog(t, 0.0, 0.4)); dy = (1 - a) * 80
    paste(fr, _c("card", _card_bg), W / 2, 360 + dy, a)
    paste(fr, _c("igav", lambda: _ig_ring_avatar(BRAND[0][2], 280)), W / 2, 430 + dy, a)
    paste(fr, _c("ighandle", lambda: text_img(BRAND[0][1], 60, max_w=800)), W / 2, 740 + dy, a)
    paste(fr, _c("igsub", lambda: text_img("Physics · Plus One & Plus Two · Malayalam", 34, max_w=800, color=(190, 196, 220))), W / 2, 830 + dy, a)
    T_TAP = 1.5
    if t < T_TAP:
        btn = _c("follow", lambda: _button("Follow", IG_BLUE, w=520))
    else:
        btn = _c("following", lambda: _button("Following", GREY, w=520, icon="check"))
    pop = 1 + 0.08 * math.exp(-((t - T_TAP) / 0.12) ** 2) if t > T_TAP - 0.2 else 1
    paste(fr, btn, W / 2, 960 + dy, a, pop)
    _tap(fr, W / 2 + 60, 1012, t, T_TAP)
    _hearts(fr, W / 2, 1000, t, T_TAP + 0.05)
    paste(fr, _c("igcta", lambda: text_img("*Follow* ചെയ്യൂ!", 66, max_w=900, hl=(255, 120, 170))), W / 2, 1200, ease_out(prog(t, T_TAP + 0.3, 0.4)))

def frame_yt(fr, t):
    a = ease_out(prog(t, 0.0, 0.4)); dy = (1 - a) * 80
    paste(fr, _c("card", _card_bg), W / 2, 360 + dy, a)
    paste(fr, _c("ytav", lambda: _big_avatar(BRAND[1][2], (255, 255, 255), 280)), W / 2, 430 + dy, a)
    paste(fr, _c("ytname", lambda: text_img(BRAND[1][1], 64, max_w=800)), W / 2, 740 + dy, a)
    paste(fr, _c("ytsub", lambda: text_img("@jaseelmkoyajmk · Physics in Malayalam", 34, max_w=800, color=(190, 196, 220))), W / 2, 830 + dy, a)
    T1, T2 = 1.3, 2.4
    if t < T1:
        btn = _c("sub", lambda: _button("SUBSCRIBE", YT_RED, w=470))
    else:
        btn = _c("subd", lambda: _button("SUBSCRIBED", GREY, fg=(225, 225, 230), w=470))
    pop = 1 + 0.08 * math.exp(-((t - T1) / 0.12) ** 2) if t > T1 - 0.2 else 1
    bx = W / 2 - 80
    paste(fr, btn, bx, 960 + dy, a, pop)
    # bell button appears after subscribing
    if t > T1 + 0.15:
        ba = ease_out(prog(t, T1 + 0.15, 0.3))
        ringing = t > T2
        wig = 22 * math.sin((t - T2) * 34) * math.exp(-(t - T2) * 2.2) if ringing else 0
        circ = _c("bellbg", lambda: _rr(110, 104, 22, GREY + (255,)))
        paste(fr, circ, bx + 306, 960 + dy, ba)
        bell = _bell(76, WHITE, wig, filled=ringing)
        paste(fr, bell, bx + 306, 974 + dy, ba)
        if ringing and t < T2 + 0.9:  # little sound rays
            L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            q = prog(t, T2, 0.9); cx, cy = bx + 306, 1012 + dy
            for s in (-1, 1):
                for j in range(2):
                    rr = 62 + j * 18 + 10 * q
                    d.arc((cx - rr, cy - rr, cx + rr, cy + rr), 200 if s < 0 else -20, 250 if s < 0 else 30, fill=(255, 255, 255, int(220 * (1 - q))), width=5)
            fr.paste(L, (0, 0), L)
    _tap(fr, bx + 40, 1012, t, T1)
    _tap(fr, bx + 306, 1012, t, T2)
    paste(fr, _c("ytcta1", lambda: text_img("*Subscribe* ചെയ്യൂ", 64, max_w=900, hl=(255, 90, 90))), W / 2, 1200, ease_out(prog(t, T1 + 0.2, 0.4)))
    paste(fr, _c("ytcta2", lambda: text_img("*bell icon* അമർത്തൂ", 54, max_w=900, hl=YELLOW)), W / 2, 1300, ease_out(prog(t, T2 + 0.2, 0.4)))

def _sfx_track(kind, sr=48000):
    import mix_voice as mv
    n = int(DUR * sr); y = np.zeros(n)
    def add(t0, s):
        i = int(t0 * sr); j = min(n, i + len(s)); y[i:j] += s[:j - i]
    add(0.0, mv.sfx("swoosh"))
    if kind == "ig":
        add(1.5, mv.sfx("pop")); add(1.55, mv.sfx("chime"))
    else:
        add(1.3, mv.sfx("pop")); add(2.4, mv.sfx("pop")); add(2.45, mv.sfx("ding"))
    # soft uplifting tail
    import music
    m = music.build(DUR + 1.0, [(0.0, "uplift")], seed=11)[:n]
    y += m * 0.22 * np.minimum(1, np.arange(n) / sr / 0.3)
    y /= max(1.0, np.abs(y).max() / 0.95)
    return y

def render_outro(kind, out):
    tmp = tempfile.mkdtemp()
    vid = os.path.join(tmp, "v.mp4"); wav = os.path.join(tmp, "a.wav")
    bg = make_bg()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", vid], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        t = i / FPS
        fr = paint_bg(bg, 100 + t)
        (frame_ig if kind == "ig" else frame_yt)(fr, t)
        footer(fr, ImageDraw.Draw(fr), "")
        p.stdin.write(fr.convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    y = _sfx_track(kind)
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000); w.writeframes((y * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", wav, "-c:v", "copy", "-af", "loudnorm=I=-15:TP=-1.0", "-ar", "48000",
                    "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-shortest", out], check=True)

def attach(final, outro, out):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", final, "-i", outro, "-filter_complex",
                    "[0:v]fps=30,format=yuv420p[v0];[1:v]fps=30,format=yuv420p[v1];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];"
                    "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]",
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", out], check=True)

if __name__ == "__main__":
    final, prefix = sys.argv[1], sys.argv[2]
    d = tempfile.mkdtemp()
    for kind in ("ig", "yt"):
        o = os.path.join(d, f"outro_{kind}.mp4")
        render_outro(kind, o)
        attach(final, o, f"{prefix}_{kind}.mp4")
        print("wrote", f"{prefix}_{kind}.mp4")
