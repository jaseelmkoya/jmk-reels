"""16 Nov: JMK's own intro (IMG_1763) + outro (IMG_1764) around the AI-voice Bose reel.
Word times = JMK's transcript, re-fitted per phrase to the real speech found by silencedetect
(his transcript ran ~0.4-0.6 s late). Outro goes after the quiz, before the end-card."""
import sys, os, subprocess
T = "/home/claude/jmk-reels/tools"; sys.path.insert(0, T)
from face_clip import render
from reelkit import YELLOW, CYAN
UP = "/mnt/user-data/uploads"; HERE = os.path.dirname(os.path.abspath(__file__)); OUT = "/home/claude/oi"

def fit(user, segs):
    res = []
    for u in user:
        for u0, u1, r0, r1 in segs:
            if u0 <= u < u1 or (u == u1 and (u0, u1, r0, r1) == segs[-1]):
                res.append({"start": round(r0 + (u - u0) * (r1 - r0) / (u1 - u0), 3)}); break
        else: raise ValueError(u)
    return res

intro_w = fit([0.8, 1.3, 1.6, 1.9, 2.6, 2.9, 3.6, 4.2, 4.6, 4.9, 5.4, 5.6, 6.0, 6.4],
              [(0.8, 3.4, 0.41, 2.56), (3.6, 5.4, 3.05, 4.88), (5.4, 5.6, 5.24, 5.50), (5.6, 7.2, 5.66, 6.59)])
intro_l = [("ചരിത്രം നമ്മളിൽ നിന്ന് മറച്ചുവെച്ച ഒരു *സത്യമുണ്ട്.*", YELLOW),
           ("യഥാർത്ഥത്തിൽ radio-യുടെ പിതാവ് *Marconi* *അല്ല,* അതൊരു *ഇന്ത്യൻ* *ശാസ്ത്രജ്ഞനാണ്.*", YELLOW)]
outro_w = fit([0.5, 1.0, 1.5, 2.0, 2.3, 2.7, 3.0, 3.2, 3.6, 3.8, 4.1, 4.4, 4.7, 5.0, 5.2, 5.8],
              [(0.5, 3.2, 0.71, 3.29), (3.2, 4.1, 3.49, 4.17), (4.1, 5.2, 4.31, 5.58), (5.2, 6.5, 6.05, 6.69)])
outro_l = [("അപ്പോൾ നിങ്ങളുടെ അഭിപ്രായത്തിൽ radio-യുടെ *യഥാർത്ഥ* *പിതാവ്* ആരാണ്?", YELLOW),
           ("*Marconi* ആണോ അതോ *Jagadish* *Chandra* *Bose* ആണോ?", CYAN),
           ("*കമന്റിൽ* രേഖപ്പെടുത്തൂ.", YELLOW)]

if __name__ == "__main__":
    render(f"{UP}/d9661876-IMG_1763.mov", f"{OUT}/intro.mp4", 0.30, 6.84, intro_l, intro_w)
    render(f"{UP}/IMG_1764.mov", f"{OUT}/outro.mp4", 0.60, 6.94, outro_l, outro_w)
    BODY = 79.567 - 4.0                       # end-card = last 4.0 s (endcard.DUR)
    for p in ("ig", "yt"):
        src = f"{HERE}/story_bose_aivoice_{p}.mp4"; out = f"{OUT}/story_bose_face_{p}.mp4"
        fc = ("[1:v]trim=0:{b},setpts=PTS-STARTPTS[rb];[1:a]atrim=0:{b},asetpts=PTS-STARTPTS[ra];"
              "[1:v]trim={b},setpts=PTS-STARTPTS[eb];[1:a]atrim={b},asetpts=PTS-STARTPTS[ea];"
              "[0:v][0:a][rb][ra][2:v][2:a][eb][ea]concat=n=4:v=1:a=1[v][a]").format(b=BODY)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{OUT}/intro.mp4", "-i", src, "-i", f"{OUT}/outro.mp4",
                        "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
        print("wrote", out)
