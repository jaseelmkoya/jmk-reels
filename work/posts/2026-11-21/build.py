import asyncio, os
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))

CSS = """
@font-face{font-family:Anek;src:url(AnekMalayalam-Bold.ttf)}
@font-face{font-family:AnekX;src:url(AnekMalayalam-ExtraBold.ttf)}
@font-face{font-family:AnekS;src:url(AnekMalayalam-SemiBold.ttf)}
@font-face{font-family:Comic;src:url(comic-neue-latin-700-normal.ttf)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:%dpx;background:linear-gradient(170deg,#05060f 0%%,#1a0f3a 100%%);
 color:#fff;font-family:Comic,Anek,sans-serif;position:relative;overflow:hidden}
.ml{font-family:Comic,Anek}
.wrap{position:absolute;left:70px;right:70px;top:%dpx;bottom:%dpx;display:flex;flex-direction:column}
.tag{align-self:flex-start;font:28px Comic;letter-spacing:2px;color:#ffd166;border:3px solid #ffd166;border-radius:30px;padding:8px 24px}
.num{position:absolute;right:70px;font:30px Comic;color:#8a90b8}
h1{font-family:Comic,AnekX;font-size:84px;line-height:1.28;margin-top:36px}
h2{font-family:Comic,AnekX;font-size:72px;line-height:1.3;margin-top:30px}
.y{color:#ffd166}.c{color:#4fd1ff}.g{color:#5be49b}.o{color:#ff9f43}.p{color:#ff6b9d}
.sub{font-family:Comic,AnekS;font-size:44px;line-height:1.5;color:#dfe3ff;margin-top:24px}
.step{display:flex;gap:26px;align-items:flex-start;margin-top:44px}
.main{flex:1;display:flex;flex-direction:column;justify-content:center}
.dot{flex:none;width:72px;height:72px;border-radius:50%%;background:#4fd1ff;color:#090e26;font:44px Comic;display:flex;align-items:center;justify-content:center}
.st{font-family:Comic,AnekS;font-size:50px;line-height:1.45}
.eq{font:60px Comic;color:#ffd166;background:rgba(255,209,102,.1);border:3px dashed #ffd166;border-radius:22px;padding:16px 30px;margin-top:30px;align-self:center}
.card{background:rgba(255,255,255,.06);border:3px solid rgba(79,209,255,.45);border-radius:28px;padding:26px 32px;margin-top:30px}
.q{font-family:Comic,AnekX;font-size:52px;color:#ff9f43;line-height:1.35}
.a{font-family:Comic,AnekS;font-size:47px;line-height:1.45;margin-top:10px}
.brand{position:absolute;left:0;right:0;bottom:%dpx;display:flex;justify-content:center;gap:30px}
.brand span{display:flex;align-items:center;border:3px solid;border-radius:30px;padding:8px 24px;font:32px Comic}
.ico{display:inline-block;width:34px;height:34px;background:currentColor;-webkit-mask-size:contain;-webkit-mask-repeat:no-repeat;-webkit-mask-position:center;margin-right:12px}
.ig{color:#ff9fc4}.yt{color:#ff8a7a}
"""
FOOT = """<div class="brand"><span class="ig"><i class="ico" style="-webkit-mask-image:url(icons/instagram-white.png)"></i>@jmk.space</span>
<span class="yt"><i class="ico" style="-webkit-mask-image:url(icons/youtube-white.png)"></i>@jaseelmkoyajmk</span></div>"""

TAG = '<div class="tag">PLUS ONE PHYSICS · GRAVITATION</div>'

def art():
    return """<svg width="900" height="470" viewBox="0 0 900 470" style="align-self:center;margin-top:24px">
<defs><radialGradient id="e" cx=".38" cy=".35" r=".7"><stop offset="0" stop-color="#7fd3ff"/><stop offset=".55" stop-color="#2b6fd6"/><stop offset="1" stop-color="#0b2a6b"/></radialGradient>
<radialGradient id="bh" cx=".5" cy=".5" r=".5"><stop offset=".55" stop-color="#000"/><stop offset=".72" stop-color="#ff9f43"/><stop offset=".85" stop-color="#ffd166" stop-opacity=".6"/><stop offset="1" stop-color="#ff6b9d" stop-opacity="0"/></radialGradient></defs>
<g fill="#fff" opacity=".6"><circle cx="40" cy="30" r="2"/><circle cx="860" cy="60" r="2.5"/><circle cx="470" cy="20" r="1.8"/><circle cx="820" cy="420" r="2"/><circle cx="60" cy="440" r="2.2"/><circle cx="560" cy="440" r="1.6"/></g>
<circle cx="200" cy="215" r="170" fill="url(#e)"/>
<path d="M120 150 q40 -30 80 0 q20 40 -20 60 q-50 10 -60 -60z M230 260 q40 -20 70 10 q-10 50 -60 40z" fill="#5be49b" opacity=".75"/>
<text x="200" y="440" text-anchor="middle" font-family="Comic" font-size="34" fill="#4fd1ff">R = 6371 km</text>
<path d="M410 215 h150" stroke="#ffd166" stroke-width="8" stroke-dasharray="18 12"/><path d="M560 190 l40 25 -40 25z" fill="#ffd166"/>
<text x="490" y="180" text-anchor="middle" font-family="Comic" font-size="30" fill="#ffd166">compress</text>
<circle cx="740" cy="215" r="105" fill="url(#bh)"/>
<circle cx="740" cy="215" r="9" fill="#2b6fd6" stroke="#fff" stroke-width="2"/>
<text x="740" y="400" text-anchor="middle" font-family="Comic" font-size="34" fill="#ff9f43">R ≈ 9 mm</text>
<text x="740" y="440" text-anchor="middle" font-family="Comic" font-size="26" fill="#8a90b8">(not to scale)</text>
</svg>"""

S1 = f"""{TAG}<div class="num" style="top:0">1/2</div>
<h1>ഭൂമിയെ ഒരു <span class="y">ഗോലി</span>യുടെ size-ലേക്ക് ഞെക്കിയാൽ?</h1>
{art()}
<div class="sub" style="text-align:center;margin-top:20px;font-size:50px">Earth ഒരു <span class="p">Black Hole</span> ആയി മാറും! 🤯</div>
<div class="sub" style="text-align:center;margin-top:10px">Sun ആണെങ്കിൽ? Radius വെറും <span class="y">3 km</span> 👉</div>"""

S2 = f"""{TAG}<div class="num" style="top:0">2/2</div><div class="main">
<h2>എന്താണ് <span class="c">physics</span>? 🧠</h2>
<div class="step"><div class="dot">1</div><div class="st"><span class="g">Escape speed</span> &nbsp;v<sub>e</sub> = √(2GM/R) <br>Earth-ന് ഇപ്പോൾ ≈ <span class="y">11.2 km/s</span></div></div>
<div class="step"><div class="dot">2</div><div class="st">R കുറയും തോറും v<sub>e</sub> കൂടും. v<sub>e</sub> = <span class="o">c</span> (light speed) ആയാൽ light-നും രക്ഷയില്ല!</div></div>
<div class="eq">R<sub>s</sub> = 2GM / c²</div>
<div class="sub" style="text-align:center">Earth → <span class="y">8.9 mm</span> &nbsp;·&nbsp; Sun → <span class="y">2.95 km</span><br><span style="font-size:36px;color:#8a90b8">(Schwarzschild radius · GR-ലും ഇതേ formula)</span></div>
<h2 style="text-align:center;font-size:56px;margin-top:40px">💾 Save · 📤 Share · 🔔 <span class="y">Follow</span></h2></div>"""

STB = f"""{TAG}
<h1 style="margin-top:20px;font-size:84px">ഇന്നലത്തെ post <span class="y">miss</span> ചെയ്തോ? 👀</h1>
<div style="align-self:center;margin-top:50px;border:6px solid #4fd1ff;border-radius:30px;overflow:hidden;width:528px;height:660px;box-shadow:0 0 60px rgba(79,209,255,.35)"><img src="out/post1.png" style="width:528px;height:660px"></div>
<div class="sub" style="text-align:center;margin-top:36px;font-size:46px">Earth → Black Hole 🕳️ എത്ര ചെറുതാകണം?<br><span class="c">@jmk.space</span> profile-ൽ കാണൂ</div>"""

def page(body, h, top, bot, fb):
    return f"<html><head><meta charset='utf-8'><style>{CSS % (h, top, bot, fb)}</style></head><body><div class='wrap'>{body}</div>{FOOT}</body></html>"

JOBS = [("post1", S1, 1350, 70, 150, 50), ("post2", S2, 1350, 70, 150, 50), ("storyB", STB, 1920, 260, 330, 300)]

async def main():
    os.makedirs(f"{D}/out", exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--allow-file-access-from-files"])
        for name, body, h, top, bot, fb in JOBS:
            pg = await b.new_page(viewport={"width": 1080, "height": h})
            open(f"{D}/{name}.html", "w").write(page(body, h, top, bot, fb))
            await pg.goto(f"file://{D}/{name}.html"); await pg.wait_for_timeout(600)
            await pg.screenshot(path=f"{D}/out/{name}.png"); await pg.close()
        await b.close()
asyncio.run(main())
