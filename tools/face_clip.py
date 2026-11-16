"""JMK's own phone clip (intro/outro) -> 1080x1920 30 fps segment with word-by-word captions + watermark.
iPhone HDR (HLG) is tone-mapped to SDR. Voice: highpass + denoise + loudnorm (no ElevenLabs).

  from face_clip import render
  render(src, out, a, b, lines, words)   # a/b = trim (s, source time); words = [{"start": source_s}, ...]
lines: (display_text, hl) as Captions.from_words; word starts are SOURCE times (shifted by -a here).
"""
import os, sys, subprocess
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reelkit import W, H, FPS, watermark, paste, WM_Y
from captions import Captions

TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")

def is_hdr(src):
    t = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=color_transfer",
                        "-of", "csv=p=0", src], capture_output=True, text=True).stdout
    return any(k in t for k in ("arib-std-b67", "smpte2084"))

def render(src, out, a, b, lines, words, cap_y=1300, size=58):
    dur = b - a
    cap = Captions.from_words(lines, [{"start": w["start"] - a} for w in words], size=size, maxw=6, tail=0.6)
    vf = (TONEMAP + "," if is_hdr(src) else "") + f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=rgb24"
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-ss", str(a), "-t", str(dur), "-i", src, "-vf", vf,
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    tmpv = out + ".v.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                            "-pix_fmt", "yuv420p", tmpv], stdin=subprocess.PIPE)
    wm, n = watermark(), 0
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        fr = Image.frombytes("RGB", (W, H), buf)
        cap.draw(fr, n / FPS, cap_y)
        paste(fr, wm, W / 2, WM_Y, 0.92)
        enc.stdin.write(fr.tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    fade = f"afade=t=in:d=0.05,afade=t=out:st={dur - 0.12:.3f}:d=0.12"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmpv, "-ss", str(a), "-t", str(dur), "-i", src,
                    "-map", "0:v", "-map", "1:a", "-af", f"highpass=f=80,afftdn=nf=-30,acompressor,{fade},loudnorm=I=-15:TP=-1.5",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", out], check=True)
    os.remove(tmpv)
    print("wrote", out, f"{n} frames")
