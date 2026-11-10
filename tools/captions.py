"""Word-by-word captions synced to the voice (karaoke-style reveal).

Usage in a topic file:
    from captions import Captions
    CAP = Captions([(text, start_s, end_s, hl_colour), ...], voice_wav=VOICE)   # voiced
    CAP = Captions([(text, start_s, None, hl), ...])                              # no voice: reading pace
    ... in every scene:  CAP.draw(fr, global_time, y)

Words are timed by spreading each line's words over the actual speech inside [start, end]
(pauses found with ffmpeg silencedetect), weighted by word length. Lines are split into pages
(sentence ends, max ~8 words) that replace each other. '*' marks highlighted words as in text_img.
Malayalam is revealed per WORD (not per letter) so conjuncts never break.
"""
import re, subprocess, os
from PIL import Image, ImageFilter
from reelkit import text_img, YELLOW, W, paste, ease_out, prog

def speech_chunks(wav, noise="-35dB", d=0.12):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", wav, "-af", f"silencedetect=noise={noise}:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ss = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
    se = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav],
                               capture_output=True, text=True).stdout)
    chunks, cur = [], 0.0
    for a, b in zip(ss, se + [dur] * (len(ss) - len(se))):
        if a > cur + 0.05: chunks.append((cur, a))
        cur = b
    if cur < dur - 0.05: chunks.append((cur, dur))
    return chunks

def _weight(w):
    return len(re.sub(r"[*.,!?:;]", "", w)) + 2

def _pages(words, maxw=8):
    pages, cur = [], []
    for w in words:
        cur.append(w)
        bare = w.strip("*")
        abbrev = re.fullmatch(r"([A-Z]\.)+", bare) or (bare.endswith(".") and len(bare) <= 3)  # C.V. / സി. വി.
        if (re.search(r"[.?!]\*?$", w) and not abbrev) or len(cur) >= maxw:
            pages.append(cur); cur = []
    if cur: pages.append(cur)
    # avoid a lonely last word
    if len(pages) > 1 and len(pages[-1]) == 1:
        last = pages.pop(); pages[-1] = pages[-1] + last
    return pages

class Captions:
    @classmethod
    def from_words(cls, lines, words, size=54, maxw=8, tail=1.5):
        """Exact sync from a transcript (ElevenLabs creative_transcribe_audio 'words': start per word).
        lines: (display_text, hl) — display tokens must match the spoken words one-to-one, in order
        (markup like *..* and -suffixes are fine). Spoken words after the last line are ignored."""
        self = cls.__new__(cls); self.size, self.items, self._cache = size, [], {}
        k = 0; allw = [w["start"] for w in words]
        for text, hl in lines:
            toks = text.split(); n = len(toks)
            times = allw[k:k + n]; k += n
            nxt = allw[k] if k < len(allw) else times[-1] + tail
            j = 0
            for p in _pages(toks, maxw):
                pt = times[j:j + len(p)]; j += len(p)
                p_end = times[j] if j < n else nxt
                self.items.append((p, hl, pt, pt[0], p_end))
        return self

    def __init__(self, lines, voice_wav=None, size=54, wpm_pace=0.42, maxw=8):
        """lines: (text, start, end_or_None, hl). wpm_pace: seconds per word when there is no voice."""
        self.size, self.items = size, []   # items: (page_text_words, hl, [word_times], page_start, page_end)
        chunks = speech_chunks(voice_wav) if voice_wav and os.path.exists(voice_wav) else None
        for i, (text, st, en, hl) in enumerate(lines):
            words = text.split()
            if en is None:
                en = st + len(words) * wpm_pace + 0.6
            times = []
            if chunks:
                sp = [(max(a, st), min(b, en)) for a, b in chunks if b > st and a < en]
                tot = sum(b - a for a, b in sp) or (en - st)
                ws = [_weight(w) for w in words]; S = sum(ws); acc = 0.0
                for w in ws:
                    target = acc / S * tot; acc += w
                    # map speech-time -> real time
                    rem = target; tt = st
                    for a, b in sp:
                        if rem <= b - a: tt = a + rem; break
                        rem -= b - a; tt = b
                    times.append(tt)
            else:
                times = [st + k * (en - st - 0.6) / max(1, len(words)) for k in range(len(words))]
            k = 0
            pg = _pages(words, maxw)
            for j, p in enumerate(pg):
                pt = times[k:k + len(p)]
                p_end = times[k + len(p)] if k + len(p) < len(words) else (lines[i + 1][1] if i + 1 < len(lines) else en + 1.5)
                self.items.append((p, hl, pt, pt[0], p_end))
                k += len(p)
        self._cache = {}

    def _img(self, words, hl, n, a):
        key = (tuple(words), hl, n, round(a, 1))
        if key not in self._cache:
            t = text_img(" ".join(words), self.size, max_w=980, hl=hl, lh=1.45, reveal=(n, a))
            bb = t.getbbox()
            sh = Image.new("RGBA", t.size, (0, 0, 0, 0))
            sh.paste((0, 0, 0, 255), (0, 0), t.getchannel("A"))
            sh = sh.filter(ImageFilter.GaussianBlur(6))
            out = Image.new("RGBA", t.size, (0, 0, 0, 0))
            out.alpha_composite(sh, (0, 4)); out.alpha_composite(sh, (0, 4)); out.alpha_composite(t)
            if len(self._cache) > 400: self._cache.clear()
            self._cache[key] = out
        return self._cache[key]

    def draw(self, fr, T, y):
        for words, hl, times, p0, p1 in self.items:
            if p0 - 0.05 <= T < p1:
                n = sum(1 for x in times if x <= T)          # fully started words
                if n == 0: return
                a = min(1.0, (T - times[n - 1]) / 0.12)       # newest word fades in quickly
                out_a = 1 - prog(T, p1 - 0.12, 0.12)
                img = self._img(words, hl, n, a)
                paste(fr, img, W / 2, y, out_a)
                return
