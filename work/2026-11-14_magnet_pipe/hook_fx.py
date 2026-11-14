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
WHYB = text_img("WHY?", 150, max_w=700, color=YELLOW)

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
    return 1.0 + 0.05 * (t - SPLIT) / (DUR - SPLIT)

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
                paste(fr, box, bx, 1330 + bb[1] - 20, out_a, s)
            paste(fr, img, W / 2, 1330, out_a, s)
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
        pop(fr, L_PL, 270, 300, t, SPLIT, DUR)
        pop(fr, L_MT, 810, 300, t, SPLIT + 0.2, DUR)
        if 19.4 <= t < WHY:
            clock(fr, W / 2, 520, t, 60)
    if t >= WHY:
        p = prog(t, WHY, 0.35)
        paste(fr, WHYB, W / 2, 560, ease_out(p), (0.5 + 0.5 * ease_back(p) if p < 1 else 1) * (1 + 0.05 * math.sin((t - WHY) * 8)))
    draw_caption(fr, t)
    footer(fr, d, "") if False else None
    enc.stdin.write(fr.tobytes()); n += 1
    if n in stills: fr.resize((360, 640)).save(f"{OUT}_{n}.png")
enc.stdin.close(); enc.wait(); print("wrote", OUT, n, "frames")
