import asyncio, os, math, shutil
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
# Rebuild: run this file (copies fonts from tools/fonts, renders to out/).
FONTS = os.path.join(D, "../../../tools/fonts")
for f in ["AnekMalayalam-Bold.ttf", "AnekMalayalam-ExtraBold.ttf", "AnekMalayalam-SemiBold.ttf", "comic-neue-latin-700-normal.ttf"]:
    if not os.path.exists(f"{D}/{f}"): shutil.copy(f"{FONTS}/{f}", D)

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
h1{font-family:Comic,AnekX;font-size:80px;line-height:1.28;margin-top:30px}
h2{font-family:Comic,AnekX;font-size:62px;line-height:1.3;margin-top:26px}
.y{color:#ffd166}.c{color:#4fd1ff}.g{color:#5be49b}.o{color:#ff9f43}.p{color:#ff6b9d}
.sub{font-family:Comic,AnekS;font-size:44px;line-height:1.5;color:#dfe3ff;margin-top:20px}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:16px}
.card{border-radius:26px;padding:24px 30px;margin-top:24px;display:flex;align-items:center;gap:26px}
.card .em{font-size:76px;flex:none}
.card .t{font-family:Comic,AnekS;font-size:44px;line-height:1.4}
.card .big{font:58px Comic}
.cold{background:rgba(79,209,255,.12);border:3px solid #4fd1ff}
.hot{background:rgba(255,159,67,.14);border:3px solid #ff9f43}
.eq{font-family:Comic,AnekS;font-size:46px;color:#ffd166;background:rgba(255,209,102,.1);border:3px dashed #ffd166;border-radius:22px;padding:14px 30px;margin-top:30px;align-self:center;text-align:center;line-height:1.4}
.ans{background:rgba(91,228,155,.12);border:3px solid #5be49b;border-radius:26px;padding:26px 30px;margin-top:26px;font-family:Comic,AnekS;font-size:44px;line-height:1.45}
.exam{align-self:center;margin-top:26px;font:30px Comic;color:#090e26;background:#ffd166;border-radius:30px;padding:10px 26px}
.brand{position:absolute;left:0;right:0;bottom:%dpx;display:flex;justify-content:center;gap:30px}
.brand span{display:flex;align-items:center;border:3px solid;border-radius:30px;padding:8px 24px;font:32px Comic}
.ico{display:inline-block;width:34px;height:34px;background:currentColor;-webkit-mask-size:contain;-webkit-mask-repeat:no-repeat;-webkit-mask-position:center;margin-right:12px}
sup{font-size:.6em;vertical-align:.7em;line-height:0}
.ig{color:#ff9fc4}.yt{color:#ff8a7a}
"""
FOOT = """<div class="brand"><span class="ig"><i class="ico" style="-webkit-mask-image:url(icons/instagram-white.png)"></i>@jmk.space</span>
<span class="yt"><i class="ico" style="-webkit-mask-image:url(icons/youtube-white.png)"></i>JMK Space</span></div>"""
TAG = '<div class="tag">PLUS ONE PHYSICS · UNITS AND MEASUREMENTS</div>'

def diagram():
    W, H = 940, 330
    sx, ex, y = 150, 830, 150
    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="align-self:center;margin-top:6px">',
         '<defs><radialGradient id="sun"><stop offset="0" stop-color="#fff3b0"/><stop offset=".6" stop-color="#ffd166"/><stop offset="1" stop-color="#ff9f43"/></radialGradient>',
         '<marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#ffd166"/></marker></defs>',
         f'<circle cx="{sx}" cy="{y}" r="105" fill="url(#sun)"/>',
         f'<circle cx="{ex}" cy="{y}" r="42" fill="#3b82f6"/><path d="M{ex-25},{y-18} q18,-10 30,4 q-6,16 -22,12 z M{ex+4},{y+12} q14,2 18,14 q-14,4 -20,-6 z" fill="#5be49b"/>',
         f'<line x1="{sx+115}" y1="{y}" x2="{ex-56}" y2="{y}" stroke="#ffd166" stroke-width="6" stroke-dasharray="22 14" marker-end="url(#ar)"/>',
         f'<text x="{(sx+ex)/2}" y="{y-26}" text-anchor="middle" font-family="Comic" font-size="34" fill="#ffd166">light · c = 3 × 10<tspan dy="-14" font-size="24">8</tspan><tspan dy="14"> m/s</tspan></text>',
         f'<text x="{(sx+ex)/2}" y="{y+62}" text-anchor="middle" font-family="Comic" font-size="34" fill="#4fd1ff">d ≈ 1.5 × 10<tspan dy="-14" font-size="24">11</tspan><tspan dy="14"> m</tspan></text>',
         f'<text x="{sx}" y="{y+150}" text-anchor="middle" font-family="Comic" font-size="32" fill="#dfe3ff">Sun</text>',
         f'<text x="{ex}" y="{y+150}" text-anchor="middle" font-family="Comic" font-size="32" fill="#dfe3ff">Earth</text>',
         f'<text x="{(sx+ex)/2}" y="{y+150}" text-anchor="middle" font-family="Comic" font-size="24" fill="#8a90b8">(not to scale)</text>',
         '</svg>']
    return "".join(s)

S1 = f"""{TAG}<div class="num">1/2</div>
<h1>ഇപ്പോൾ കാണുന്ന സൂര്യൻ <span class="y">8 മിനിറ്റ് പഴയതാണ്!</span> ☀️</h1>
<div class="main">{diagram()}
<div class="eq" style="font-size:44px">t = d / c = (1.5 × 10<sup>11</sup>) / (3 × 10<sup>8</sup>)<br>= <span class="g">500 s ≈ 8 min 20 s</span></div>
<div class="sub" style="text-align:center;margin-top:26px">8 മിനിറ്റ് മുമ്പ് പുറപ്പെട്ട light ആണ് നമ്മൾ കാണുന്നത് 👉</div></div>"""

S2 = f"""{TAG}<div class="num">2/2</div>
<h2>ആകാശത്തേക്ക് നോക്കുന്നത് = <span class="y">past-ലേക്ക്</span> നോക്കുന്നത് 🔭</h2>
<div class="main">
<div class="card cold" style="margin-top:14px;padding:16px 30px"><div class="em" style="font-size:62px">🌙</div><div class="t">Moon<br><span class="big c">1.3 s</span></div></div>
<div class="card hot" style="margin-top:14px;padding:16px 30px"><div class="em" style="font-size:62px">☀️</div><div class="t">Sun<br><span class="big o">8 min 20 s</span></div></div>
<div class="card cold" style="margin-top:14px;padding:16px 30px"><div class="em" style="font-size:62px">⭐</div><div class="t">Proxima Centauri<br><span class="big c">4.2 വർഷം</span></div></div>
<div class="card hot" style="margin-top:14px;padding:16px 30px"><div class="em" style="font-size:62px">🌌</div><div class="t">Andromeda galaxy<br><span class="big p">25 ലക്ഷം വർഷം!</span></div></div>
<div class="eq" style="font-size:38px;margin-top:22px">1 light year = ദൂരത്തിന്റെ unit ആണ് (time അല്ല)<br>= 9.46 × 10<sup>15</sup> m</div></div>"""

STB = f"""{TAG}
<h1 style="font-size:78px;margin-top:30px">ഇന്നലത്തെ post <span class="y">miss</span> ചെയ്തോ? 👀</h1>
<img src="out/post1.png" style="width:560px;align-self:center;margin-top:30px;border-radius:26px;border:5px solid #ffd166;box-shadow:0 0 50px rgba(255,209,102,.35)">
<div class="sub" style="font-size:50px;text-align:center;margin-top:34px">സൂര്യൻ <span class="y">8 മിനിറ്റ് പഴയത്</span> ☀️</div>
<div class="sub" style="font-size:42px;text-align:center;margin-top:10px">Profile-ൽ പോയി save ചെയ്യൂ 📌</div>"""

def page(body, h, top, bot, fb):
    return f"<html><head><meta charset='utf-8'><style>{CSS % (h, top, bot, fb)}</style></head><body><div class='wrap'>{body}</div>{FOOT}</body></html>"

F = (1350, 60, 130, 45)
JOBS = [("post1", S1, *F), ("post2", S2, *F),
        ("storyB", STB, 1920, 250, 300, 270)]

async def main():
    os.makedirs(f"{D}/out", exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--allow-file-access-from-files"])
        for name, body, h, top, bot, fb in JOBS:
            pg = await b.new_page(viewport={"width": 1080, "height": h})
            open(f"{D}/{name}.html", "w").write(page(body, h, top, bot, fb))
            await pg.goto(f"file://{D}/{name}.html"); await pg.wait_for_timeout(800)
            await pg.screenshot(path=f"{D}/out/{name}.png"); await pg.close()
        await b.close()
    from PIL import Image
    for name, *_ in JOBS:
        Image.open(f"{D}/out/{name}.png").convert("RGB").save(f"{D}/{name}.jpg", quality=92)
asyncio.run(main())
