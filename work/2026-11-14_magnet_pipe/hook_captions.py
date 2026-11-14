"""Burn word-by-word captions (JMK's own wording) onto his experiment clip. Times: his list, linearly mapped onto the
real audio (anchors from the ElevenLabs transcript: his times run ~4% long): t = 0.9593*t_his - 0.275."""
import sys, os, subprocess
sys.path.insert(0, "/home/claude/jmk-reels/tools")
from reelkit import *
from captions import Captions
from PIL import ImageDraw
SRC, OUT = sys.argv[1], sys.argv[2]
# (display token, his start time)
T = [("ഇന്നൊരു",0.0),("കുട്ടി",0.45),("പരീക്ഷണമാണ്.",0.85),("രണ്ട്",1.65),("പൈപ്പുണ്ട്",2.05),("എന്റെ",2.45),("കയ്യിൽ,",2.7),
("ഒരു",3.0),("*plastic*-ന്റെ",3.25),("പൈപ്പും",3.85),("ഒരു",4.25),("*metal*-ന്റെ",4.45),("പൈപ്പും.",4.85),
("ഇതിനകത്തൂടെ",5.2),("ഞാൻ",5.75),("ഒരു",5.95),("*magnet*-നെ",6.1),("താഴത്തേക്ക്",6.55),("insert",6.95),("ചെയ്യുകയാണ്.",7.3),
("ഓക്കെ,",7.75),("ആദ്യം",8.0),("ഞാൻ",8.3),("ഈ",8.5),("*plastic*-ന്റെ",8.65),("പൈപ്പിനകത്തൂടെ",9.2),("*magnet*",9.75),("താഴോട്ട്",10.15),
("ഇടുന്നു,",10.5),("താഴത്തേക്ക്",10.85),("വന്നു.",11.35),
("ഇനി",11.75),("അതേപോലെ",12.05),("തന്നെ",12.6),("ഈ",12.9),("*metal*",13.05),("പൈപ്പിനകത്തൂടെയും",13.45),("ഞാൻ",14.15),("ഈ",14.35),
("*magnet*",14.5),("താഴോട്ട്",14.9),("ഇടുകയാണ്.",15.25),
("Yes,",15.75),("ഞാൻ",16.0),("താഴോട്ട്",16.2),("ഇടാൻ",16.5),("പോവുകയാണ്,",16.75),("ശ്രദ്ധിക്കുക,",17.2),("Yes.",17.65),
("കണ്ടോ?",17.95),
("ഈ",18.35),("*metal*",18.5),("പൈപ്പിനകത്ത്",18.9),("*magnet*",19.5),("താഴെ",19.95),("വരാൻ",20.25),("കുറച്ച്",20.55),("സമയം",20.9),("എടുത്തു,",21.3),("അല്ലേ?",21.65),
("ആ",21.95),("ഒരു",22.05),("*time",22.15),("delay*",22.4),("ഉണ്ടാകാൻ",22.65),("കാരണം",23.0),("എന്താണ്?",23.3),
("നമുക്ക്",23.65),("നോക്കിയാലോ?",23.95)]
words = [{"start": max(0.0, 0.9593 * t - 0.275)} for _, t in T]
toks = [w for w, _ in T]
# lines = sentence groups (pages split further at 8 words)
cuts = [3, 13, 20, 31, 42, 49, 50, 60, 67, 69]
lines, k = [], 0
for c in cuts:
    lines.append((" ".join(toks[k:c]), YELLOW)); k = c
CAP = Captions.from_words(lines, words, size=56, maxw=6)
dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",SRC]))
dec = subprocess.Popen(["ffmpeg","-v","error","-i",SRC,"-vf",f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1",
                        "-f","rawvideo","-pix_fmt","rgb24","-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","30","-i","-","-i",SRC,
                        "-map","0:v","-map","1:a","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest",OUT],
                       stdin=subprocess.PIPE)
n = 0; fs = W * H * 3
while True:
    b = dec.stdout.read(fs)
    if len(b) < fs: break
    fr = Image.frombytes("RGB", (W, H), b)
    # soft dark band behind the captions for legibility on live video
    band = Image.new("RGBA", (W, 240), (0, 0, 0, 110)); fr.paste(band, (0, 1320), band)
    CAP.draw(fr, n / 30, 1335)
    enc.stdin.write(fr.tobytes()); n += 1
    if len(sys.argv) > 3 and n in (int(x) for x in sys.argv[3].split(",")): fr.resize((360, 640)).save(f"{OUT}_{n}.png")
enc.stdin.close(); enc.wait(); print("wrote", OUT, n, "frames")
