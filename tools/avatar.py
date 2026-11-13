"""JMK's cartoon avatar that 'talks' with the voice (for the weekly explainer format).
Frames: brand/avatar_closed.png, avatar_talk.png (mouth patch), avatar_blink.png (eye patch) — made once
from JMK's photo with ElevenLabs gpt-image-2 (flow ucZ6EMwp8Y3OJwPypDEr). No credits per video.
Mouth opens when the voice is loud (RMS envelope with hysteresis), blinks every 2.5–4.5 s,
small head bob while speaking.
    av = Avatar("vo/x.wav"); av.draw(fr, t, cx=830, bottom=1600, height=640)
"""
import os, wave, random
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30

class Avatar:
    def __init__(self, voice_wav=None, seed=3):
        b = os.path.join(HERE, "brand")
        self.img = {k: Image.open(os.path.join(b, f"avatar_{k}.png")).convert("RGBA") for k in ("closed", "talk", "blink")}
        self.talk = np.zeros(1, bool)
        if voice_wav and os.path.exists(voice_wav):
            w = wave.open(voice_wav); sr = w.getframerate(); ch = w.getnchannels()
            x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
            if ch == 2: x = x.reshape(-1, 2).mean(1)
            hop = sr // FPS; n = len(x) // hop
            rms = np.sqrt(np.array([np.mean(x[i * hop:(i + 1) * hop] ** 2) for i in range(n)]) + 1e-12)
            on, off = np.percentile(rms, 70) * 0.55, np.percentile(rms, 70) * 0.35
            st, out, hold = False, [], 0
            for i, r in enumerate(rms):
                if hold > 0: hold -= 1
                elif not st and r > on: st, hold = True, 1
                elif st and r < off: st, hold = False, 1
                out.append(st)
            # flap: alternate open/closed every 2–3 frames while talking so it looks like speech
            out = np.array(out); flap = np.zeros_like(out)
            k = 0
            for i in range(len(out)):
                if out[i]: k += 1; flap[i] = (k // 3) % 2 == 0
                else: k = 0
            self.talk = flap
            self.env = rms / (rms.max() + 1e-9)
        else:
            self.env = np.zeros(1)
        rnd = random.Random(seed); t, self.blinks = 1.2, []
        while t < 600: self.blinks.append(t); t += rnd.uniform(2.5, 4.5)
        self._cache = {}

    def state(self, t):
        i = int(t * FPS)
        if any(b <= t < b + 0.13 for b in self.blinks if b - 1 < t < b + 1): return "blink"
        if i < len(self.talk) and self.talk[i]: return "talk"
        return "closed"

    def draw(self, fr, t, cx, bottom, height=640, alpha=1.0):
        s = self.state(t)
        i = int(t * FPS); e = float(self.env[i]) if i < len(self.env) else 0.0
        bob = 6 * np.sin(t * 2.1) + 8 * e
        key = (s, height)
        if key not in self._cache:
            im = self.img[s]; w = int(im.width * height / im.height)
            self._cache[key] = im.resize((w, height), Image.LANCZOS)
        im = self._cache[key]
        if alpha < 1:
            im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
        x = int(cx - im.width / 2); y = int(bottom - im.height + bob)
        fr.paste(im, (x, y), im)
