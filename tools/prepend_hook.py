"""Put JMK's own 3–8 s phone clip (face + hook question) at the very start of a reel.
Usage: python3 prepend_hook.py <hook_clip> <reel.mp4> <out.mp4>
- Crops/scales the phone clip to 1080x1920 @30 fps (portrait or landscape), cleans the voice
  (highpass + denoise + loudnorm), adds the watermark, then joins it in front of the reel.
- Trim silence at the start/end of the clip first (silencedetect) so the hook starts instantly.
"""
import sys, os, subprocess, re, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reelkit import watermark, W, H, WM_Y

def speech_bounds(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "silencedetect=noise=-35dB:d=0.25", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()[2]) + 60 * int(re.search(r"Duration: (\d+):(\d+)", err).group(2))
    ss = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    se = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    start = se[0] if ss and ss[0] < 0.05 and se else 0.0
    end = ss[-1] if ss and (not se or ss[-1] > se[-1]) else dur
    return max(0, start - 0.08), min(dur, end + 0.15)

def main(hook, reel, out):
    tmp = tempfile.mkdtemp()
    wm = os.path.join(tmp, "wm.png")
    img = watermark(); img.save(wm)
    a, b = speech_bounds(hook)
    x = (W - img.width) // 2; y = int(WM_Y)
    vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1[v0];"
          f"[v0][1:v]overlay={x}:{y}:format=auto,format=yuv420p[v]")
    hookv = os.path.join(tmp, "hook.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a), "-to", str(b), "-i", hook, "-i", wm,
                    "-filter_complex", vf, "-map", "[v]", "-map", "0:a",
                    "-af", "highpass=f=80,afftdn=nf=-30,acompressor,loudnorm=I=-15:TP=-1.0",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", hookv], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", hookv, "-i", reel, "-filter_complex",
                    "[0:v]fps=30,format=yuv420p[v0];[1:v]fps=30,format=yuv420p[v1];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];"
                    "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print("wrote", out, f"(hook {b - a:.1f}s)")

if __name__ == "__main__":
    main(*sys.argv[1:4])
