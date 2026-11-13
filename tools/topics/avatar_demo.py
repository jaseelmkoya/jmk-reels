"""Demo of the weekly 'avatar explainer' format (maroon theme, JMK cartoon avatar talking bottom-right)."""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from reelkit import *
from avatar import Avatar
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = "vo_demo_avatar.wav"
AV = Avatar(os.path.join(HERE, VOICE))
DUR = 9.9

def _bg():
    y, x = np.mgrid[0:H, 0:W]
    r = np.sqrt(((x - W * 0.5) / W) ** 2 + ((y - H * 0.42) / H) ** 2)
    k = np.clip(1 - r * 1.6, 0, 1)[..., None]
    c0 = np.array([22, 6, 10]); c1 = np.array([74, 20, 30])
    return Image.fromarray((c0 + (c1 - c0) * k).astype(np.uint8), "RGB")
BG = _bg()

def chip(top, main):
    f1 = font("lat", "bold", 30); f2 = font("lat", "bold", 44)
    w = int(max(f1.getlength(top) + 40, f2.getlength(main))) + 60
    im = Image.new("RGBA", (w, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, 139), radius=18, fill=(20, 8, 12, 230), outline=(255, 255, 255, 60), width=2)
    d.ellipse((28, 32, 46, 50), fill=(235, 70, 80)); d.text((58, 26), top, font=f1, fill=(235, 90, 100))
    d.text((28, 70), main, font=f2, fill=WHITE)
    return im
CHIP = chip("PLUS ONE PHYSICS", "INERTIA OF MOTION")
HOOK = text_img("ബസ് പെട്ടെന്ന് *brake* ഇടുമ്പോൾ നമ്മൾ *മുന്നോട്ട്* വീഴുന്നത് എന്തുകൊണ്ട്?", 64, max_w=960, hl=YELLOW)
Q = text_img("?", 120, max_w=200, color=(30, 20, 10))

def bus(d, x, y, s=1.0, col=(240, 190, 60)):
    d.rounded_rectangle((x, y, x + 420 * s, y + 200 * s), radius=int(30 * s), fill=col, outline=(30, 20, 10), width=6)
    for i in range(4):
        d.rounded_rectangle((x + (30 + i * 95) * s, y + 30 * s, x + (105 + i * 95) * s, y + 95 * s), radius=10, fill=(150, 210, 240))
    for wx in (90, 330):
        d.ellipse((x + (wx - 40) * s, y + 160 * s, x + (wx + 40) * s, y + 240 * s), fill=(30, 30, 34))
        d.ellipse((x + (wx - 16) * s, y + 184 * s, x + (wx + 16) * s, y + 216 * s), fill=(150, 150, 160))

def scene(fr, t, d):
    fr.paste(BG, (0, 0))
    # glow ring behind the icon
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
    for r, a in ((330, 40), (280, 60)):
        rr = r + 10 * math.sin(t * 2)
        ld.ellipse((W / 2 - rr, 860 - rr, W / 2 + rr, 860 + rr), outline=(255, 120, 120, a), width=4)
    fr.paste(L, (0, 0), L)
    # bus drives in and brakes hard at t=4.6 (matches the voice)
    p = min(1, t / 4.6); x = -420 + (W / 2 - 210 + 420) * (1 - (1 - p) ** 2)
    jolt = 14 * math.exp(-max(0, t - 4.6) * 6) * math.sin(max(0, t - 4.6) * 30) if t > 4.6 else 0
    bus(d, x + jolt, 760)
    if t < 4.6:
        for k in range(3):
            d.line((x - 40 - k * 30, 800 + k * 50, x - 140 - k * 30, 800 + k * 50), fill=(255, 220, 160), width=6)
    if t > 4.6:
        a = ease_out(prog(t, 4.6, 0.3))
        d.ellipse((W / 2 + 160, 640, W / 2 + 260, 740), fill=(255, 209, 102))
        paste(fr, Q, W / 2 + 210, 620, a)
    paste(fr, HOOK, W / 2, 230, 1.0)                     # hook visible from frame 0
    paste(fr, CHIP, 300, 1330, ease_out(prog(t, 1.2, 0.4)))
    AV.draw(fr, t, cx=W - 190, bottom=1640, height=660)

SCENES = [(DUR, scene)]
SFX = [(0.0, "whoosh"), (4.6, "brake"), (4.7, "thud"), (1.2, "pop")]
MUSIC = [(0.0, "curious")]
