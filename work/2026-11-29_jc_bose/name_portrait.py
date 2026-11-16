"""16 Nov: JMK's AI portrait of Bose shown when the AI voice says 'ജഗദീഷ് ചന്ദ്ര ബോസ്' (reel 18.10–19.53 s),
whole picture visible, name title word by word, 'AI recreation' tag. Then the final pair:
intro_fx + reel(with portrait) + outro + end-card."""
import sys, os, subprocess, json
from PIL import Image
import intro_fx as fx
from reelkit import W, H, FPS, text_img, paste, watermark, WM_Y, ease_back, prog, YELLOW
OUT = fx.OUT; HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = json.load(open(os.path.join(HERE, "story_bose_words.json")))
NAME = [w["start"] for w in WORDS if w["line"] == 2][-3:]          # ജഗദീഷ് ചന്ദ്ര ബോസ്
T0, T1 = NAME[0] - 0.14, next(w["start"] for w in WORDS if w["line"] == 3) - 0.15
BODY = 79.567 - 4.0
TOKS = ["ജഗദീഷ്", "ചന്ദ്ര", "ബോസ്"]

def seg(path):
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    wm = watermark(); n = 0
    while n / FPS < T1 - T0:
        T = T0 + n / FPS
        fr = fx.bose_frame(T, T0).convert("RGBA")
        if T < T0 + 0.22:
            fr.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(235 * (1 - (T - T0) / 0.22) ** 2))))
        k = sum(1 for x in NAME if x <= T)
        if k:
            nm = text_img(" ".join(TOKS[:k]), 84, color=YELLOW, max_w=1000)
            paste(fr, fx.TOPG.transpose(Image.FLIP_TOP_BOTTOM), W / 2, H - 520 - 300, 1.0)
            paste(fr, nm, W / 2, 1330, 1.0, scale=0.9 + 0.1 * ease_back(prog(T, NAME[k - 1], 0.25)))
        paste(fr, text_img("AI recreation", 26, color=(230, 230, 230)), W - 130, 1560, 0.7)
        paste(fr, wm, W / 2, WM_Y, 0.92)
        enc.stdin.write(fr.convert("RGB").tobytes()); n += 1
    enc.stdin.close(); enc.wait()

if __name__ == "__main__":
    sp = f"{OUT}/name_portrait.mp4"; seg(sp)
    for p in ("ig", "yt"):
        fc = (f"[3:v]setpts=PTS-STARTPTS+{T0}/TB[pv];[1:v][pv]overlay=eof_action=pass:enable='between(t,{T0},{T1 - 0.001})'[rv];"
              "[rv]split[r1][r2];[r1]trim=0:{b},setpts=PTS-STARTPTS[rb];[1:a]atrim=0:{b},asetpts=PTS-STARTPTS[ra];"
              "[r2]trim={b},setpts=PTS-STARTPTS[eb];[1:a]atrim={b},asetpts=PTS-STARTPTS[ea];"
              "[0:v][0:a][rb][ra][2:v][2:a][eb][ea]concat=n=4:v=1:a=1[v][a]").replace("{b}", str(BODY))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/intro_fx.mp4", "-i", f"{HERE}/story_bose_aivoice_{p}.mp4",
                        "-i", f"{OUT}/outro.mp4", "-i", sp, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{HERE}/story_bose_fx_{p}.mp4"], check=True)
        print("wrote", p)
