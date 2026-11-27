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
.ig{color:#ff9fc4}.yt{color:#ff8a7a}
"""
FOOT = """<div class="brand"><span class="ig"><i class="ico" style="-webkit-mask-image:url(icons/instagram-white.png)"></i>@jmk.space</span>
<span class="yt"><i class="ico" style="-webkit-mask-image:url(icons/youtube-white.png)"></i>JMK Space</span></div>"""
TAG = '<div class="tag">PLUS ONE PHYSICS · THERMAL PROPERTIES OF MATTER</div>'

def bp(p_atm):
    """Boiling point of water (deg C) from Antoine equation, pressure in atm."""
    mm = p_atm * 760
    A, B, C = (8.07131, 1730.63, 233.426) if mm < 760.5 else (8.14019, 1810.94, 244.485)
    return B / (A - math.log10(mm)) - C

def graph():
    W, H = 900, 560; L, R, T, Bm = 110, 40, 30, 90
    x0, x1, y0, y1 = 0.6, 2.2, 85, 125
    X = lambda p: L + (p - x0) / (x1 - x0) * (W - L - R)
    Y = lambda t: T + (y1 - t) / (y1 - y0) * (H - T - Bm)
    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="align-self:center;margin-top:10px">']
    for t in range(85, 126, 10):  # grid + y labels
        s.append(f'<line x1="{L}" y1="{Y(t):.1f}" x2="{W-R}" y2="{Y(t):.1f}" stroke="#2c2f55" stroke-width="2"/>')
        s.append(f'<text x="{L-14}" y="{Y(t)+11:.1f}" text-anchor="end" font-family="Comic" font-size="30" fill="#b9bee6">{t}</text>')
    for p in [0.6, 1.0, 1.4, 1.8, 2.2]:
        s.append(f'<text x="{X(p):.1f}" y="{H-Bm+40}" text-anchor="middle" font-family="Comic" font-size="30" fill="#b9bee6">{p:g}</text>')
    s.append(f'<line x1="{L}" y1="{H-Bm}" x2="{W-R}" y2="{H-Bm}" stroke="#dfe3ff" stroke-width="4"/>')
    s.append(f'<line x1="{L}" y1="{H-Bm}" x2="{L}" y2="{T}" stroke="#dfe3ff" stroke-width="4"/>')
    s.append(f'<text x="{(L+W-R)/2}" y="{H-8}" text-anchor="middle" font-family="Comic" font-size="32" fill="#dfe3ff">Pressure (atm)</text>')
    s.append(f'<text x="34" y="{(T+H-Bm)/2}" text-anchor="middle" font-family="Comic" font-size="32" fill="#dfe3ff" transform="rotate(-90 34 {(T+H-Bm)/2})">Boiling point (°C)</text>')
    pts = " ".join(f"{X(p):.1f},{Y(bp(p)):.1f}" for p in [0.6 + i * 0.02 for i in range(81)])
    s.append(f'<polyline points="{pts}" fill="none" stroke="#ffd166" stroke-width="7" stroke-linecap="round"/>')
    # marked points: (pressure atm, colour, label, label dx, dy)
    for p, col, lab, dx, dy, anc in [(0.83, "#4fd1ff", "Munnar ≈ 95 °C", 22, 52, "start"),
                                     (1.0, "#5be49b", "Open pot 100 °C", 22, 50, "start"),
                                     (2.0, "#ff9f43", "Cooker ≈ 120 °C", 20, 150, "end")]:
        cx, cy = X(p), Y(bp(p))
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="15" fill="{col}" stroke="#090e26" stroke-width="4"/>')
        s.append(f'<text x="{cx+dx:.1f}" y="{cy+dy:.1f}" text-anchor="{anc}" font-family="Comic" font-size="34" fill="{col}">{lab}</text>')
    s.append('</svg>')
    return "".join(s)

S1 = f"""{TAG}<div class="num">1/4</div>
<h1>Pressure cooker-ൽ ചോറ് <span class="y">വേഗം വേവുന്നത്</span> എന്തുകൊണ്ട്? 🍚</h1>
<div class="main">
<div class="card cold"><div class="em">🥘</div><div class="t">സാധാരണ പാത്രം: ചോറ് വേവാൻ <span class="c">ഏറെ സമയം</span></div></div>
<div class="card hot"><div class="em">♨️</div><div class="t">Pressure cooker: <span class="o">ഏറെ കുറവ് സമയം</span></div></div>
<div class="sub" style="text-align:center;margin-top:44px">ഉത്തരം: <span class="y">Physics</span> 👉 Swipe ചെയ്യൂ</div></div>"""

S2 = f"""{TAG}<div class="num">2/4</div>
<h2>Pressure കൂടിയാൽ <span class="y">boiling point</span> കൂടും 🔥</h2>
<div class="main">
<div class="card cold"><div class="em">🥘</div><div class="t">Open pot<br><span class="big c">1 atm → 100 °C</span></div></div>
<div class="card hot"><div class="em">♨️</div><div class="t">Pressure cooker<br><span class="big o">≈ 2 atm → ≈ 120 °C</span></div></div>
<div class="eq">കൂടിയ temperature-ൽ വെള്ളം boil ചെയ്യും<br>→ ചോറ് <span class="g">വേഗം വേവും</span> ⏱️</div></div>"""

S3 = f"""{TAG}<div class="num">3/4</div>
<h2>Hill station-ൽ <span class="c">നേരെ തിരിച്ച്</span> 🏔️</h2>
<div class="sub" style="font-size:40px">Munnar-ൽ air pressure കുറവ് → വെള്ളം <span style="white-space:nowrap">≈ 95 °C-ൽ</span> boil ചെയ്യും → cooking <span class="c">slow</span></div>
<div class="main">{graph()}</div>"""

S4 = f"""{TAG}<div class="num">4/4</div>
<h2>Whistle വന്ന ശേഷം <span class="y">flame കൂട്ടിയാൽ</span> temperature കൂടുമോ? 🤔</h2>
<div class="main">
<div class="ans"><span class="g">ഇല്ല!</span> Weight valve pressure ഏകദേശം constant ആക്കി നിർത്തും → temperature ≈ 120 °C തന്നെ. Extra heat <span class="y">steam</span> ആയി പുറത്തു പോകും 💨 (gas waste)</div>
<div class="exam">Exam-ലും: Plus One Christmas Exam 2024 · Q9 (2 marks)</div>
<div class="eq" style="margin-top:34px;font:52px Comic">📌 Save &nbsp; 📤 Share &nbsp; 🔔 Follow</div></div>"""

STB = f"""{TAG}
<h1 style="font-size:78px;margin-top:30px">ഇന്നലത്തെ post <span class="y">miss</span> ചെയ്തോ? 👀</h1>
<img src="out/post1.png" style="width:560px;align-self:center;margin-top:30px;border-radius:26px;border:5px solid #ffd166;box-shadow:0 0 50px rgba(255,209,102,.35)">
<div class="sub" style="font-size:50px;text-align:center;margin-top:34px"><span class="y">Pressure cooker</span>-ന്റെ physics 🍚</div>
<div class="sub" style="font-size:42px;text-align:center;margin-top:10px">Profile-ൽ പോയി save ചെയ്യൂ 📌</div>"""

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
            await pg.goto(f"file://{D}/{name}.html"); await pg.wait_for_timeout(800)
            await pg.screenshot(path=f"{D}/out/{name}.png"); await pg.close()
        await b.close()
    from PIL import Image
    for name, *_ in JOBS:
        Image.open(f"{D}/out/{name}.png").convert("RGB").save(f"{D}/{name}.jpg", quality=92)
asyncio.run(main())
