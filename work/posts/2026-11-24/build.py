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
.wrap{position:absolute;left:56px;right:56px;top:%dpx;bottom:%dpx;display:flex;flex-direction:column}
.tag{align-self:flex-start;font:26px Comic;letter-spacing:2px;color:#ffd166;border:3px solid #ffd166;border-radius:30px;padding:7px 22px}
h1{font-family:Comic,AnekX;font-size:56px;line-height:1.2;margin-top:16px}
.y{color:#ffd166}.c{color:#4fd1ff}.g{color:#5be49b}.o{color:#ff9f43}.p{color:#ff6b9d}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:18px}
.card{background:rgba(255,255,255,.06);border:3px solid rgba(79,209,255,.4);border-radius:24px;padding:9px 22px}
.card.w{grid-column:1 / span 2}
.k{font-family:Comic,AnekS;font-size:28px;color:#ff9f43;line-height:1.25}
.f{font:38px Comic;color:#ffd166;margin-top:2px;line-height:1.25}
.n{font-family:Comic,AnekS;font-size:27px;color:#dfe3ff;line-height:1.35;margin-top:4px}
.fav{margin-top:14px;background:rgba(91,228,155,.14);border:3px dashed #5be49b;border-radius:22px;padding:8px 20px;font-family:Comic,AnekS;font-size:28px;line-height:1.4}
.save{text-align:center;font-family:Comic,AnekX;font-size:36px;margin-top:12px}
.brand{position:absolute;left:0;right:0;bottom:%dpx;display:flex;justify-content:center;gap:30px}
.brand span{display:flex;align-items:center;border:3px solid;border-radius:30px;padding:8px 24px;font:32px Comic}
.ico{display:inline-block;width:34px;height:34px;background:currentColor;-webkit-mask-size:contain;-webkit-mask-repeat:no-repeat;-webkit-mask-position:center;margin-right:12px}
.ig{color:#ff9fc4}.yt{color:#ff8a7a}
"""
FOOT = """<div class="brand"><span class="ig"><i class="ico" style="-webkit-mask-image:url(icons/instagram-white.png)"></i>@jmk.space</span>
<span class="yt"><i class="ico" style="-webkit-mask-image:url(icons/youtube-white.png)"></i>@jaseelmkoyajmk</span></div>"""

TAG = '<div class="tag">PLUS ONE PHYSICS · WORK, ENERGY AND POWER</div>'

P1 = f"""{TAG}
<h1>Work, Energy &amp; Power — <span class="y">എല്ലാ formulas</span> ഒറ്റ നോട്ടത്തിൽ 📌</h1>
<div class="grid">
<div class="card"><div class="k">Work (constant force)</div><div class="f">W = F d cosθ</div><div class="n">θ = 90° → W = 0 · unit: J</div></div>
<div class="card"><div class="k">Work (variable force)</div><div class="f">W = ∫ F dx</div><div class="n">= F–x graph-ന് താഴെയുള്ള area</div></div>
<div class="card"><div class="k">Kinetic energy</div><div class="f">K = ½mv² = p²/2m</div></div>
<div class="card"><div class="k">Work–energy theorem</div><div class="f">W<sub>net</sub> = K<sub>f</sub> − K<sub>i</sub></div></div>
<div class="card"><div class="k">Potential energy</div><div class="f">U = mgh</div><div class="n">Spring: U = ½kx², F = −kx</div></div>
<div class="card"><div class="k">Conservation of energy</div><div class="f">K + U = constant</div><div class="n">(conservative forces മാത്രം)</div></div>
<div class="card"><div class="k">Power</div><div class="f">P = W/t = F·v</div><div class="n">1 hp = 746 W</div></div>
<div class="card"><div class="k">Commercial unit</div><div class="f">1 kWh = 3.6×10⁶ J</div><div class="n">current bill-ലെ "unit" ഇതാണ്</div></div>
<div class="card w"><div class="k">Collisions</div><div class="n" style="font-size:29px"><span class="g">Elastic:</span> momentum ✓ KE ✓ &nbsp;·&nbsp; <span class="p">Inelastic:</span> momentum ✓ KE ✗<br><span class="c">Perfectly inelastic:</span> ഒട്ടിച്ചേരും → v = (m₁u₁ + m₂u₂)/(m₁ + m₂)</div></div>
</div>
<div class="fav">⭐ Spring PE (½kx²) derivation: Plus One Christmas Exam <span class="y">2018, 2019, 2024</span></div>
<div class="save">Save ചെയ്തു വെച്ചോ 📌 exam-ന് മുമ്പ് ഒന്ന് നോക്കാം</div>"""

STB = """<div class="tag">PLUS ONE PHYSICS · WORK, ENERGY AND POWER</div>
<h1 style="font-size:78px;margin-top:30px">ഇന്നലത്തെ post <span class="y">miss</span> ചെയ്തോ? 👀</h1>
<img src="out/post1.png" style="width:560px;align-self:center;margin-top:30px;border-radius:26px;border:5px solid #ffd166;box-shadow:0 0 50px rgba(255,209,102,.35)">
<div class="save" style="font-size:52px;margin-top:34px"><span class="y">Full formula card</span> 📌</div>
<div class="save" style="font-size:42px;margin-top:14px;color:#dfe3ff">Profile-ൽ പോയി save ചെയ്യൂ!</div>"""

def page(body, h, top, bot, fb):
    return f"<html><head><meta charset='utf-8'><style>{CSS % (h, top, bot, fb)}</style></head><body><div class='wrap'>{body}</div>{FOOT}</body></html>"

JOBS = [("post1", P1, 1350, 44, 110, 34), ("storyB", STB, 1920, 250, 300, 270)]

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
