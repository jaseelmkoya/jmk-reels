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

TAG = '<div class="tag">PLUS ONE PHYSICS · MOTION IN A PLANE</div>'
PYQ = '<div class="pyq">PYQ · Plus One Christmas Exam 2025 · Q16 (3 marks)</div>'

def art(q=True):
    # true proportions: u=20 m/s, R=35.3 m, H30=5.1 m, H60=15.3 m at 16 px/m
    x0,y0,R=150,330,565
    return f"""<svg width="860" height="370" viewBox="0 0 860 370" style="align-self:center;margin-top:18px">
<line x1="60" y1="{y0}" x2="800" y2="{y0}" stroke="#8a90b8" stroke-width="4"/>
<path d="M{x0} {y0} Q {x0+R/2} {y0-2*245} {x0+R} {y0}" fill="none" stroke="#ff6b9d" stroke-width="7" stroke-dasharray="16 10"/>
<path d="M{x0} {y0} Q {x0+R/2} {y0-2*82} {x0+R} {y0}" fill="none" stroke="#4fd1ff" stroke-width="7" stroke-dasharray="16 10"/>
<circle cx="{x0}" cy="{y0}" r="14" fill="#ffd166"/>
<circle cx="{x0+R}" cy="{y0}" r="14" fill="#5be49b"/>
<text x="{x0+R/2}" y="{y0-262}" text-anchor="middle" font-family="Comic" font-size="38" fill="#ff6b9d">60°</text>
<text x="{x0+R/2}" y="{y0-98}" text-anchor="middle" font-family="Comic" font-size="38" fill="#4fd1ff">30°</text>
{'<text x="'+str(x0+R+30)+'" y="'+str(y0-24)+'" font-family="Comic" font-size="44" fill="#5be49b">?</text>' if q else ''}
</svg>"""

CSS2 = """.pyq{align-self:flex-start;margin-top:18px;font:30px Comic;color:#090e26;background:#5be49b;border-radius:30px;padding:8px 24px}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:26px}
.opt{background:rgba(255,255,255,.07);border:3px solid rgba(79,209,255,.5);border-radius:24px;padding:18px 24px;font:46px Comic;display:flex;align-items:center;gap:18px}
.opt b{flex:none;width:58px;height:58px;border-radius:50%;background:#ffd166;color:#090e26;display:flex;align-items:center;justify-content:center;font:38px Comic}
.opt.ok{border-color:#5be49b;background:rgba(91,228,155,.18)}"""

S1 = f"""{TAG}{PYQ}
<h1 style="font-size:70px;margin-top:26px">Christmas exam-ൽ <span class="y">7-ൽ 6</span> തവണയും projectile! 🎯</h1>
<div class="sub" style="font-size:46px;margin-top:18px;color:#fff">ഒരേ speed-ൽ <span class="c">30°</span>-ലും <span class="p">60°</span>-ലും എറിഞ്ഞാൽ horizontal range?</div>
{art()}
<div class="opts">
<div class="opt"><b>A</b>R₃₀ &gt; R₆₀</div><div class="opt"><b>B</b>R₃₀ &lt; R₆₀</div>
<div class="opt"><b>C</b>R₃₀ = R₆₀</div><div class="opt"><b>D</b>R₆₀ = 2R₃₀</div></div>
<div class="sub" style="text-align:center;margin-top:30px;font-size:44px">Comment ചെയ്യൂ 👇 ഉത്തരം നാളെ രാവിലെ <span class="y">story</span>-യിൽ</div>"""

STB = f"""{TAG}{PYQ}
<h1 style="margin-top:30px;font-size:80px">ഇന്നലത്തെ quiz-ന്റെ <span class="y">ഉത്തരം</span> ✅</h1>
<div class="opt ok" style="margin-top:36px;font-size:60px;align-self:center;padding:22px 44px"><b style="width:76px;height:76px;font-size:48px">C</b>R₃₀ = R₆₀</div>
{art(False)}
<div class="eq">R = u² sin2θ / g</div>
<div class="sub" style="text-align:center;font-size:48px">sin 60° = sin 120° → range <span class="g">same</span>!<br>θ-ക്കും (90° − θ)-ക്കും ഒരേ range. <span class="p">60°</span> കൂടുതൽ ഉയരത്തിൽ പോകും.</div>"""

def page(body, h, top, bot, fb):
    return f"<html><head><meta charset='utf-8'><style>{CSS % (h, top, bot, fb)}{CSS2}</style></head><body><div class='wrap'>{body}</div>{FOOT}</body></html>"

JOBS = [("post1", S1, 1350, 60, 130, 45), ("storyB", STB, 1920, 250, 300, 270)]

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
