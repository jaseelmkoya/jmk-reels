"""JMK's experiment clip with animated overlays: hook banner, pop-in word captions (his wording/timing),
keyword chips, DROP bursts, TIME DELAY clock burst, PLASTIC/METAL labels on the split screen, WHY? pulse,
progress bar and gentle punch-in zooms. Usage: python3 hook_fx.py <clip.mp4> <out.mp4> [stillframes]"""
import sys, os, math, subprocess, importlib.util
sys.path.insert(0, "/home/claude/jmk-reels/tools"); sys.path.insert(0, "/home/claude/jmk-reels/tools/topics")
from reelkit import *
from captions import Captions
from PIL import ImageDraw
SRC, OUT = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("hc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "hook_captions_data.py"))
hc = importlib.util.module_from_spec(spec); spec.loader.exec_module(hc)
_ms = importlib.util.spec_from_file_location("mp", "/home/claude/jmk-reels/tools/topics/magnet_pipe.py")
mp = importlib.util.module_from_spec(_ms); _ms.loader.exec_module(mp)

CAP = Captions.from_words(hc.LINES, hc.WORDS, size=60, maxw=5)
CAP.items = [it for it in CAP.items if it[3] < 7.4 or it[3] >= 21.1]

# events (seconds in the clip, from the real audio/video)
CUTS = [0.0, 17.8]                      # split screen starts at 17.8
DROP1, DROP2, KANDO, SPLIT, WHY = 9.35, 16.7, 16.96, 17.8, 21.9
DUR = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",SRC]))

HOOK = boxed(text_img("*Plastic* vs *Metal* pipe — ഏതിൽ *magnet* പതുക്കെ വീഴും?", 60, max_w=940, hl=YELLOW), pad=26,
             fill=(9, 14, 38, 225), outline=(255, 209, 102, 230))
C_PL = pill("PLASTIC PIPE", 40, fg=(9, 14, 38), bg=(235, 240, 250))
C_MT = pill("METAL PIPE", 40, fg=(9, 14, 38), bg=(190, 198, 214))
C_MG = pill("MAGNET", 40, fg=WHITE, bg=(235, 70, 70))
DROP = pill("DROP!", 54, fg=(9, 14, 38), bg=YELLOW)
FAST = pill("വേഗം താഴെ എത്തി!", 40, fg=(9, 14, 38), bg=ORANGE)
TD = pill("TIME DELAY!", 64, fg=(9, 14, 38), bg=CYAN)
L_PL = pill("PLASTIC", 40, fg=(9, 14, 38), bg=(235, 240, 250))
L_MT = pill("METAL", 40, fg=(9, 14, 38), bg=(190, 198, 214))
WHYB = text_img("WHY?", 110, max_w=400, color=YELLOW)
SW_START = 19.3            # magnet leaves the top of the metal pipe on the split screen
T_PL = 0.302               # plastic: free fall through ~45 cm, t = sqrt(2h/g)
APPROX = boxed(text_img("≈ estimate|(plastic: free fall)", 26, max_w=340, color=MUTED, lh=1.3), pad=12)
from PIL import ImageFont
MONO = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 44)
MONO_S = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)

def stopwatch_dev(fr, cx, y, secs, alpha, stopped):
    """Handheld digital stopwatch with a microsecond readout (s.µs)."""
    Wd, Hd = 330, 250
    L = SS(Wd, Hd); dd = L.d; k = L.s
    dd.rounded_rectangle(k(140, 0, 190, 26), radius=8, fill=(200, 205, 215, 255))          # start button
    dd.rounded_rectangle(k(40, 16, 80, 34), radius=6, fill=(255, 92, 92, 255) if stopped else (150, 155, 170, 255))
    dd.rounded_rectangle(k(6, 24, Wd - 6, Hd - 6), radius=46, fill=(40, 44, 58, 255), outline=(150, 156, 175, 255), width=6)
    dd.rounded_rectangle(k(30, 70, Wd - 30, 170), radius=14, fill=(178, 196, 160, 255), outline=(90, 100, 80, 255), width=3)
    img = L.done(); d2 = ImageDraw.Draw(img)
    us = int(round(secs * 1e6)) + (0 if stopped or secs == 0 else (int(secs * 7919e3) % 977))   # live µs digits
    txt = f"{us // 1000000:02d}.{us % 1000000:06d}"
    d2.text((Wd / 2, 122), txt, font=MONO, fill=(25, 32, 22), anchor="mm")
    d2.text((Wd / 2, 200), "STOP" if stopped else ("RUN" if secs > 0 else "READY"), font=MONO_S, fill=(255, 92, 92) if stopped else (91, 228, 155), anchor="mm")
    d2.text((Wd - 52, 88), "s", font=MONO_S, fill=(25, 32, 22), anchor="mm") if False else None
    paste(fr, img, cx, y, alpha, 0.85)

def burst(d, cx, cy, p, col, n=12, r0=60, r1=170):
    if p <= 0 or p >= 1: return
    for i in range(n):
        a = i * 2 * math.pi / n
        ra, rb = r0 + (r1 - r0) * p, r0 + (r1 - r0) * min(1, p + 0.25)
        d.line((cx + ra * math.cos(a), cy + ra * math.sin(a), cx + rb * math.cos(a), cy + rb * math.sin(a)), fill=col, width=8)

def clock(fr, cx, cy, t, r=70):
    L = SS(2 * r + 20, 2 * r + 20); dd = L.d; k = L.s; c = r + 10
    dd.ellipse(k(10, 10, 2 * r + 10, 2 * r + 10), fill=(9, 14, 38, 235), outline=CYAN + (255,), width=10)
    for h in range(12):
        a = h * math.pi / 6
        dd.line(k(c + (r - 18) * math.sin(a), c - (r - 18) * math.cos(a), c + (r - 8) * math.sin(a), c - (r - 8) * math.cos(a)), fill=(200, 220, 255, 255), width=5)
    a = t * 2 * math.pi * 1.2
    dd.line(k(c, c, c + (r - 22) * math.sin(a), c - (r - 22) * math.cos(a)), fill=YELLOW + (255,), width=8)
    dd.line(k(c, c, c + (r - 40) * math.sin(a / 12), c - (r - 40) * math.cos(a / 12)), fill=WHITE + (255,), width=10)
    img = L.done(); fr.paste(img, (int(cx - c), int(cy - c)), img)

def pop(fr, layer, cx, y, t, t0, t1, wob=False):
    if not (t0 <= t < t1 + 0.3): return
    p = prog(t, t0, 0.35); a = ease_out(p) * (1 - prog(t, t1, 0.3))
    s = (0.5 + 0.5 * ease_back(p)) if p < 1 else 1.0
    if wob: s *= 1 + 0.04 * math.sin((t - t0) * 7)
    paste(fr, layer, cx, y, a, s)

def zoom_of(t):
    # gentle punch-ins between cuts: wide -> slow push, punch on key moments
    if t < 7.4: return 1.0 + 0.04 * t / 7.4
    if t < 11.6: return 1.10 + 0.03 * (t - 7.4) / 4.2
    if t < SPLIT: return 1.04 + 0.05 * (t - 11.6) / (SPLIT - 11.6)
    return 1.0

def CY(T): return 1330 if T < SPLIT else 1400   # below the pipe bottoms on the split screen

def draw_caption(fr, T):
    for words, hl, times, p0, p1 in CAP.items:
        if p0 - 0.05 <= T < p1:
            n = sum(1 for x in times if x <= T)
            if n == 0: return
            a = min(1.0, (T - times[n - 1]) / 0.1)
            img = CAP._img(words, hl, n, a)
            full = CAP._img(words, hl, len(words), 1.0)
            bb = full.getbbox()
            pp = prog(T, p0, 0.25); s = (0.8 + 0.2 * ease_back(pp)) if pp < 1 else 1.0
            out_a = 1 - prog(T, p1 - 0.1, 0.1)
            if bb:
                box = card(bb[2] - bb[0] + 60, bb[3] - bb[1] + 40, fill=(9, 14, 38, 200), outline=(255, 209, 102, 160), r=30)
                bx = W / 2 - full.width / 2 + (bb[0] + bb[2]) / 2
                paste(fr, box, bx, CY(T) + bb[1] - 20, out_a, s)
            paste(fr, img, W / 2, CY(T), out_a, s)
            return

dec = subprocess.Popen(["ffmpeg","-v","error","-i",SRC,"-vf",f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1",
                        "-f","rawvideo","-pix_fmt","rgb24","-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","30","-i","-","-i",SRC,
                        "-map","0:v","-map","1:a","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest",OUT],
                       stdin=subprocess.PIPE)
stills = set(int(x) for x in sys.argv[3].split(",")) if len(sys.argv) > 3 else set()
n = 0; fs = W * H * 3
while True:
    b = dec.stdout.read(fs)
    if len(b) < fs: break
    t = n / 30
    fr = Image.frombytes("RGB", (W, H), b)
    z = zoom_of(t)
    if z > 1.001:
        cw, ch = W / z, H / z; cx = W / 2; cy = max(ch / 2, min(H - ch / 2, H * 0.45))
        fr = fr.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BICUBIC)
    d = ImageDraw.Draw(fr)
    # progress bar
    d.rectangle((0, 0, int(W * t / DUR), 10), fill=(255, 176, 32))
    # hook banner (frame 0)
    if t < 4.6:
        paste(fr, HOOK, W / 2, 290, 1 - prog(t, 4.2, 0.4), 1 + 0.02 * math.sin(t * 5))
    pop(fr, C_PL, 300, 560, t, 2.6, 4.3)
    pop(fr, C_MT, 780, 700, t, 3.55, 5.0)
    if 5.0 <= t < 7.5:
        pop(fr, C_MG, W / 2, 420, t, 5.0, 7.3)
        a = ease_out(prog(t, 5.0, 0.3)) * (1 - prog(t, 7.2, 0.3))
        if a > 0.05:
            L = Image.new("RGBA", (200, 240), (0, 0, 0, 0)); mp.magnet(ImageDraw.Draw(L), 100, 120, 80, 130)
            L.putalpha(L.getchannel("A").point(lambda v: int(v * a)))
            fr.paste(L, (W // 2 - 100, 520 + int(14 * math.sin(t * 6))), L)
    # drop 1 (plastic)
    if DROP1 - 0.05 <= t < DROP1 + 1.6:
        burst(d, 820, 520, prog(t, DROP1, 0.5), YELLOW)
        pop(fr, DROP, 820, 480, t, DROP1, DROP1 + 1.0)
        pop(fr, FAST, W / 2, 640, t, DROP1 + 0.6, DROP1 + 2.2)
        if t < DROP1 + 1.0:
            arrow(d, 820, 600, 820, 600 + 200 * ease_out(prog(t, DROP1, 0.4)), YELLOW, 14, 40)
    # drop 2 (metal) + TIME DELAY
    if DROP2 - 0.05 <= t < KANDO + 0.4:
        pop(fr, DROP, 820, 480, t, DROP2, KANDO + 0.2)
    if KANDO <= t < SPLIT + 0.4:
        burst(d, W / 2, 560, prog(t, KANDO, 0.6), CYAN, 16, 120, 300)
        clock(fr, W / 2, 470, t)
        pop(fr, TD, W / 2, 580, t, KANDO, SPLIT + 0.2, wob=True)
    # split screen labels
    if t >= SPLIT:
        pop(fr, L_PL, 500, 300, t, SPLIT, DUR)
        pop(fr, L_MT, 922, 300, t, SPLIT + 0.2, DUR)
        if t >= SW_START - 0.6:
            a = ease_out(prog(t, SW_START - 0.6, 0.4))
            el = max(0.0, t - SW_START)
            stopwatch_dev(fr, 500, 470, min(el, T_PL), a, el >= T_PL)
            stopwatch_dev(fr, 922, 470, el, a, False)
            paste(fr, APPROX, 500, 1240, a * 0.9)
    if t >= WHY:
        p = prog(t, WHY, 0.35)
        paste(fr, WHYB, 922, 800, ease_out(p), (0.5 + 0.5 * ease_back(p) if p < 1 else 1) * (1 + 0.05 * math.sin((t - WHY) * 8)))
    draw_caption(fr, t)
    footer(fr, d, "") if False else None
    enc.stdin.write(fr.tobytes()); n += 1
    if n in stills: fr.resize((360, 640)).save(f"{OUT}_{n}.png")
enc.stdin.close(); enc.wait(); print("wrote", OUT, n, "frames")
