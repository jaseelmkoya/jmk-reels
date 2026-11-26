import asyncio, os
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
# Rebuild: copy tools/fonts (AnekMalayalam Bold/ExtraBold/SemiBold, comic-neue-latin-700) next to this file, run it (renders to out/).

CSS = """
@font-face{font-family:Anek;src:url(AnekMalayalam-Bold.ttf)}
@font-face{font-family:AnekX;src:url(AnekMalayalam-ExtraBold.ttf)}
@font-face{font-family:AnekS;src:url(AnekMalayalam-SemiBold.ttf)}
@font-face{font-family:Comic;src:url(comic-neue-latin-700-normal.ttf)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:%dpx;background:linear-gradient(170deg,#05060f 0%%,#1a0f3a 100%%);
 color:#fff;font-family:Comic,Anek,sans-serif;position:relative;overflow:hidden}
.wrap{position:absolute;left:70px;right:70px;top:%dpx;bottom:%dpx;display:flex;flex-direction:column}
.tag{align-self:flex-start;font:28px Comic;letter-spacing:2px;color:#ffd166;border:3px solid #ffd166;border-radius:30px;padding:8px 24px}
.num{position:absolute;right:0;top:12px;font:30px Comic;color:#8a90b8}
h1{font-family:Comic,AnekX;font-size:76px;line-height:1.28;margin-top:30px}
h2{font-family:Comic,AnekX;font-size:60px;line-height:1.3;margin-top:26px}
.y{color:#ffd166}.c{color:#4fd1ff}.g{color:#5be49b}.o{color:#ff9f43}.p{color:#ff6b9d}
.sub{font-family:Comic,AnekS;font-size:42px;line-height:1.5;color:#dfe3ff;margin-top:20px}
.mno{align-self:flex-start;margin-top:26px;font:34px Comic;color:#090e26;background:#ffd166;border-radius:30px;padding:8px 26px}
.bad,.good{display:flex;gap:22px;align-items:flex-start;border-radius:26px;padding:24px 28px;margin-top:22px}
.bad{background:rgba(255,92,92,.12);border:3px solid #ff5c5c}
.good{background:rgba(91,228,155,.12);border:3px solid #5be49b}
.mk{flex:none;width:70px;height:70px;border-radius:50%%;font:48px Comic;display:flex;align-items:center;justify-content:center;color:#090e26}
.bad .mk{background:#ff5c5c}.good .mk{background:#5be49b}
.t{font-family:Comic,AnekS;font-size:46px;line-height:1.42}
.bad .t{color:#ffc9c9}
.eq{font:52px Comic;color:#ffd166;background:rgba(255,209,102,.1);border:3px dashed #ffd166;border-radius:22px;padding:12px 30px;margin-top:22px;align-self:center}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:16px}
.brand{position:absolute;left:0;right:0;bottom:%dpx;display:flex;justify-content:center;gap:30px}
.brand span{display:flex;align-items:center;border:3px solid;border-radius:30px;padding:8px 24px;font:32px Comic}
.ico{display:inline-block;width:34px;height:34px;background:currentColor;-webkit-mask-size:contain;-webkit-mask-repeat:no-repeat;-webkit-mask-position:center;margin-right:12px}
.ig{color:#ff9fc4}.yt{color:#ff8a7a}
.rl{display:flex;gap:20px;align-items:flex-start;margin-top:30px}
.rl .mk{width:62px;height:62px;font-size:40px;background:#5be49b}
"""
FOOT = """<div class="brand"><span class="ig"><i class="ico" style="-webkit-mask-image:url(icons/instagram-white.png)"></i>@jmk.space</span>
<span class="yt"><i class="ico" style="-webkit-mask-image:url(icons/youtube-white.png)"></i>JMK Space</span></div>"""

TAG = '<div class="tag">PLUS ONE PHYSICS · LAWS OF MOTION</div>'

def blocks(w=860):
    # A pushes B to the right. Force on B by A (F_BA) -> right, drawn on B.
    # Force on A by B (F_AB) -> left, drawn on A. Equal length = equal magnitude.
    return f"""<svg width="{w}" height="{int(250*w/860)}" viewBox="0 0 860 250" style="align-self:center;margin-top:18px">
<defs><marker id="ah" markerUnits="userSpaceOnUse" markerWidth="34" markerHeight="34" refX="20" refY="17" orient="auto"><path d="M0,0 L34,17 L0,34 z" fill="#ffd166"/></marker></defs>
<line x1="60" y1="235" x2="800" y2="235" stroke="#8a90b8" stroke-width="4"/>
<rect x="250" y="125" width="180" height="110" rx="10" fill="rgba(79,209,255,.18)" stroke="#4fd1ff" stroke-width="5"/>
<rect x="430" y="125" width="180" height="110" rx="10" fill="rgba(255,107,157,.18)" stroke="#ff6b9d" stroke-width="5"/>
<text x="340" y="198" text-anchor="middle" font-family="Comic" font-size="52" fill="#4fd1ff">A</text>
<text x="520" y="198" text-anchor="middle" font-family="Comic" font-size="52" fill="#ff6b9d">B</text>
<line x1="400" y1="90" x2="250" y2="90" stroke="#ffd166" stroke-width="7" marker-end="url(#ah)"/>
<line x1="460" y1="90" x2="610" y2="90" stroke="#ffd166" stroke-width="7" marker-end="url(#ah)"/>
<text x="315" y="60" text-anchor="middle" font-family="Comic" font-size="36" fill="#4fd1ff">Force on A</text>
<text x="545" y="60" text-anchor="middle" font-family="Comic" font-size="36" fill="#ff6b9d">Force on B</text>
</svg>"""

S1 = f"""{TAG}<div class="num">1/4</div>
<h1>Laws of Motion: students സ്ഥിരം ചെയ്യുന്ന <span class="y">4 തെറ്റുകൾ</span> ⚠️</h1>
<div class="main"><div class="mno">തെറ്റ് #1</div>
<div class="bad"><div class="mk">✗</div><div class="t">Action-ഉം reaction-ഉം പരസ്പരം cancel ചെയ്യും</div></div>
<div class="good"><div class="mk">✓</div><div class="t">രണ്ടും <span class="g">വ്യത്യസ്ത bodies-ൽ</span> ആണ് — cancel ആകില്ല</div></div>
{blocks()}</div>"""

S2 = f"""{TAG}<div class="num">2/4</div>
<h2>Net force <span class="y">zero</span> ആയാൽ body നിൽക്കുമോ? 🤔</h2>
<div class="main"><div class="mno">തെറ്റ് #2</div>
<div class="bad"><div class="mk">✗</div><div class="t">Net force zero ആണെങ്കിൽ body rest-ൽ മാത്രം</div></div>
<div class="good"><div class="mk">✓</div><div class="t">Rest-ൽ, <span class="g">അല്ലെങ്കിൽ uniform velocity-യിൽ</span> നേർരേഖയിൽ തുടരും (First law)</div></div>
<div class="sub" style="margin-top:40px">ഉദാ: ഒരേ speed-ൽ നേരെ പോകുന്ന car → <span class="y">net force = 0</span></div></div>"""

S3 = f"""{TAG}<div class="num">3/4</div>
<h2>Moon-ൽ പോയാൽ നിങ്ങളുടെ <span class="y">mass</span> കുറയുമോ? 🌙</h2>
<div class="main"><div class="mno">തെറ്റ് #3</div>
<div class="bad"><div class="mk">✗</div><div class="t">Mass-ഉം weight-ഉം ഒന്നുതന്നെ</div></div>
<div class="good"><div class="mk">✓</div><div class="t"><span class="c">Mass</span> (kg) മാറില്ല. <span class="o">Weight W = mg</span> (N) — g മാറിയാൽ മാറും</div></div>
<div class="eq">60 kg → Earth: 588 N · Moon: ≈ 97 N</div></div>"""

S4 = f"""{TAG}<div class="num">4/4</div>
<h2><span class="y">Impulse</span>-ന്റെ unit — N/s ആണോ? 🧐</h2>
<div class="main"><div class="mno">തെറ്റ് #4</div>
<div class="bad"><div class="mk">✗</div><div class="t">Impulse-ന്റെ unit N/s</div></div>
<div class="good"><div class="mk">✓</div><div class="t">Impulse = F × Δt = Δp → unit <span class="g">N s</span> <span style="white-space:nowrap">(= kg m s⁻¹)</span></div></div>
<div class="eq" style="margin-top:50px;font-size:54px">📌 Save &nbsp; 📤 Share &nbsp; 🔔 Follow</div>
<div class="sub" style="text-align:center">ഏത് തെറ്റ് നിങ്ങൾ ചെയ്തിട്ടുണ്ട്? Comment ചെയ്യൂ 👇</div></div>"""

STB = f"""{TAG}
<h1 style="font-size:72px">ഇന്നലത്തെ <span class="y">4 തെറ്റുകൾ</span> — ശരി ഇതാ ✅</h1>
<div class="main" style="justify-content:flex-start;margin-top:70px">
<div class="rl"><div class="mk">✓</div><div class="t">Action, reaction: വ്യത്യസ്ത bodies-ൽ → cancel ഇല്ല</div></div>
<div class="rl"><div class="mk">✓</div><div class="t">Net force 0 → rest അല്ലെങ്കിൽ uniform velocity</div></div>
<div class="rl"><div class="mk">✓</div><div class="t">Weight W = mg (N); mass (kg) മാറില്ല</div></div>
<div class="rl"><div class="mk">✓</div><div class="t">Impulse unit: N s</div></div>
<div class="sub" style="text-align:center;margin-top:50px">Full post — profile-ൽ 📌</div></div>"""

def page(body, h, top, bot, fb):
    return f"<html><head><meta charset='utf-8'><style>{CSS % (h, top, bot, fb)}</style></head><body><div class='wrap'>{body}</div>{FOOT}</body></html>"

F = (1350, 60, 130, 45)
JOBS = [("post1", S1, *F), ("post2", S2, *F), ("post3", S3, *F), ("post4", S4, *F),
        ("storyB", STB, 1920, 250, 300, 270)]

async def main():
    os.makedirs(f"{D}/out", exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--allow-file-access-from-files"])
        for name, body, h, top, bot, fb in JOBS:
            pg = await b.new_page(viewport={"width": 1080, "height": h})
            open(f"{D}/{name}.html", "w").write(page(body, h, top, bot, fb))
            await pg.goto(f"file://{D}/{name}.html"); await pg.wait_for_timeout(700)
            await pg.screenshot(path=f"{D}/out/{name}.png"); await pg.close()
        await b.close()
asyncio.run(main())
