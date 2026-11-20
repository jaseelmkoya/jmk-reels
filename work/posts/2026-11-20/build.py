import asyncio, os
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))

CSS = """
@font-face{font-family:Anek;src:url(AnekMalayalam-Bold.ttf)}
@font-face{font-family:AnekX;src:url(AnekMalayalam-ExtraBold.ttf)}
@font-face{font-family:AnekS;src:url(AnekMalayalam-SemiBold.ttf)}
@font-face{font-family:Comic;src:url(comic-neue-latin-700-normal.ttf)}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:%dpx;background:linear-gradient(170deg,#090e26 0%%,#1e1246 100%%);
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
TAG = '<div class="tag">PLUS TWO PHYSICS · ELECTROMAGNETIC INDUCTION</div>'

def art(scale=1.0):
    # charging pad + phone with coils and field lines
    return f"""<svg width="{int(760*scale)}" height="{int(510*scale)}" viewBox="0 0 760 510" style="align-self:center;margin-top:20px">
<defs><linearGradient id="ph" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#3a3f6b"/><stop offset="1" stop-color="#22264a"/></linearGradient></defs>
<g fill="none" stroke="#4fd1ff" stroke-width="5" stroke-dasharray="14 12" opacity=".85">
<path d="M300 360 C 160 300, 160 150, 300 95"/><path d="M460 360 C 600 300, 600 150, 460 95"/>
<path d="M330 360 C 240 300, 240 160, 330 110"/><path d="M430 360 C 520 300, 520 160, 430 110"/>
<path d="M380 360 L380 100"/></g>
<rect x="190" y="40" width="380" height="120" rx="30" fill="url(#ph)" stroke="#8a90b8" stroke-width="4"/>
<g fill="none" stroke="#ff9f43" stroke-width="6"><ellipse cx="380" cy="100" rx="120" ry="28"/><ellipse cx="380" cy="100" rx="85" ry="18"/><ellipse cx="380" cy="100" rx="50" ry="9"/></g>
<text x="590" y="110" font-family="Comic" font-size="34" fill="#ff9f43">Phone coil</text>
<ellipse cx="380" cy="400" rx="230" ry="55" fill="#2a2f57" stroke="#8a90b8" stroke-width="4"/>
<g fill="none" stroke="#5be49b" stroke-width="6"><ellipse cx="380" cy="390" rx="140" ry="30"/><ellipse cx="380" cy="390" rx="100" ry="20"/><ellipse cx="380" cy="390" rx="60" ry="11"/></g>
<text x="380" y="500" text-anchor="middle" font-family="Comic" font-size="34" fill="#5be49b">Charger coil (AC)</text>
<g fill="#ffd166"><path d="M380 235 l-22 34 h16 l-10 30 30-42 h-16 l12-22z"/></g>
</svg>"""

S1 = f"""{TAG}<div class="num" style="top:0">1/4</div>
<h1>Wire ഇല്ലാതെ phone <span class="y">charge</span> ആകുന്നത് എങ്ങനെ? 🤔</h1>
{art()}
<div class="sub" style="text-align:center;margin-top:30px">ഉത്തരം: <span class="c">Mutual Induction</span> ⚡<br>Swipe ചെയ്യൂ 👉</div>"""

S2 = f"""{TAG}<div class="num" style="top:0">2/4</div><div class="main">
<h2>എങ്ങനെ <span class="c">work</span> ചെയ്യുന്നു?</h2>
<div class="step"><div class="dot">1</div><div class="st">Charger coil-ൽ <span class="g">AC current</span> → മാറുന്ന <span class="c">magnetic field</span></div></div>
<div class="step"><div class="dot">2</div><div class="st">Phone coil-ലൂടെ <span class="c">magnetic flux</span> മാറുന്നു → <span class="y">induced emf</span></div></div>
<div class="step"><div class="dot">3</div><div class="st">Phone-ലെ circuit ഇത് <span class="o">DC</span> ആക്കി battery charge ചെയ്യുന്നു 🔋</div></div>
<div class="eq">ε₂ = −M dI₁/dt</div>
<div class="sub" style="text-align:center">ഒരു coil-ലെ current മാറുമ്പോൾ അടുത്ത coil-ൽ emf = <span class="c">Mutual induction</span></div></div>"""

S3 = f"""{TAG}<div class="num" style="top:0">3/4</div><div class="main">
<h2>2 <span class="o">WHY</span> ചോദ്യങ്ങൾ 🧠</h2>
<div class="card"><div class="q">Charger coil-ൽ steady DC ആണെങ്കിൽ?</div>
<div class="a">Flux മാറില്ല → <span class="y">emf = 0</span> → charging ഇല്ല!</div></div>
<div class="card"><div class="q">Phone അല്പം മാറ്റി വെച്ചാൽ?</div>
<div class="a">Phone coil-ലൂടെയുള്ള flux കുറയും → <span class="c">M</span> കുറയും → charging slow 🐢</div></div>
<div class="sub" style="font-size:48px;margin-top:40px">💡 <span class="g">Transformer</span>-ഉം ഇതേ principle!</div></div>"""

S4 = f"""{TAG}<div class="num" style="top:0">4/4</div><div class="main">
<h2>Exam-ന് <span class="y">ഓർക്കാൻ</span> 📌</h2>
<div class="card"><div class="a"><span class="y">Mutual inductance (M):</span> total flux linked with a coil when one ampere flows in the neighbouring coil.</div>
<div class="a" style="margin-top:16px">Unit: <span class="c">henry (H)</span> · <span class="c">φ₂ = M I₁</span></div></div>
<h2 style="text-align:center;font-size:62px;margin-top:90px">💾 Save · 📤 Share · 🔔 <span class="y">Follow</span></h2></div>"""

STA = f"""{TAG}
<h1 style="margin-top:120px;font-size:96px">ഇന്ന് <span class="y">6:30</span>-ന് പുതിയ reel 🔔</h1>
<div class="card" style="margin-top:80px;padding:40px"><div class="q" style="font-size:60px;line-height:1.4">ട്രെയിൻ track തൊടാതെ <span class="y">603 km/h</span>-ൽ പറക്കുന്നത് എങ്ങനെ? 🚄</div></div>
<div class="sub" style="text-align:center;margin-top:70px;font-size:50px">Physics ഉത്തരം reel-ൽ 👀<br>മിസ്സ് ആക്കല്ലേ!</div>"""

STB = f"""{TAG}
<h1 style="margin-top:20px;font-size:84px">ഇന്നലത്തെ post <span class="y">miss</span> ചെയ്തോ? 👀</h1>
<div style="align-self:center;margin-top:50px;border:6px solid #4fd1ff;border-radius:30px;overflow:hidden;width:528px;height:660px;box-shadow:0 0 60px rgba(79,209,255,.35)"><img src="out/post1.png" style="width:528px;height:660px"></div>
<div class="sub" style="text-align:center;margin-top:36px;font-size:46px">Wireless charging-ന്റെ physics 📱⚡<br><span class="c">@jmk.space</span> profile-ൽ കാണൂ</div>"""

def page(body, h, top, bot, fb):
    return f"<html><head><meta charset='utf-8'><style>{CSS % (h, top, bot, fb)}</style></head><body><div class='wrap'>{body}</div>{FOOT}</body></html>"

JOBS = [("post1", S1, 1350, 70, 150, 50), ("post2", S2, 1350, 70, 150, 50), ("post3", S3, 1350, 70, 150, 50),
        ("post4", S4, 1350, 70, 150, 50), ("storyA", STA, 1920, 260, 330, 300), ("storyB", STB, 1920, 260, 330, 300)]

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
