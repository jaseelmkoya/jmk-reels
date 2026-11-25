import asyncio, os, math
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
.wrap{position:absolute;left:70px;right:70px;top:%dpx;bottom:%dpx;display:flex;flex-direction:column}
.tag{align-self:flex-start;font:28px Comic;letter-spacing:2px;color:#ffd166;border:3px solid #ffd166;border-radius:30px;padding:8px 24px}
.num{position:absolute;right:0;top:12px;font:30px Comic;color:#8a90b8}
h1{font-family:Comic,AnekX;font-size:84px;line-height:1.28;margin-top:36px}
h2{font-family:Comic,AnekX;font-size:64px;line-height:1.3;margin-top:28px}
.y{color:#ffd166}.c{color:#4fd1ff}.g{color:#5be49b}.o{color:#ff9f43}.p{color:#ff6b9d}
.sub{font-family:Comic,AnekS;font-size:44px;line-height:1.5;color:#dfe3ff;margin-top:24px}
.step{display:flex;gap:24px;align-items:flex-start;margin-top:30px}
.dot{flex:none;width:66px;height:66px;border-radius:50%%;background:#4fd1ff;color:#090e26;font:40px Comic;display:flex;align-items:center;justify-content:center}
.st{font-family:Comic,AnekS;font-size:48px;line-height:1.42}
.eq{font:58px Comic;color:#ffd166;background:rgba(255,209,102,.1);border:3px dashed #ffd166;border-radius:22px;padding:14px 30px;margin-top:18px;align-self:flex-start}
.big{font-size:64px;align-self:center;padding:22px 40px}
.pyq{align-self:flex-start;margin-top:18px;font:30px Comic;color:#090e26;background:#5be49b;border-radius:30px;padding:8px 24px}
.years{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}
.years b{font:34px Comic;padding:6px 15px;border-radius:18px;background:rgba(91,228,155,.18);border:3px solid #5be49b;color:#5be49b}
.years b.x{background:none;border-color:#555a80;color:#555a80;text-decoration:line-through}
.card{background:rgba(255,255,255,.06);border:3px solid rgba(79,209,255,.45);border-radius:28px;padding:24px 32px;margin-top:26px}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:20px}
.brand{position:absolute;left:0;right:0;bottom:%dpx;display:flex;justify-content:center;gap:30px}
.brand span{display:flex;align-items:center;border:3px solid;border-radius:30px;padding:8px 24px;font:32px Comic}
.ico{display:inline-block;width:34px;height:34px;background:currentColor;-webkit-mask-size:contain;-webkit-mask-repeat:no-repeat;-webkit-mask-position:center;margin-right:12px}
.ig{color:#ff9fc4}.yt{color:#ff8a7a}
"""
FOOT = """<div class="brand"><span class="ig"><i class="ico" style="-webkit-mask-image:url(icons/instagram-white.png)"></i>@jmk.space</span>
<span class="yt"><i class="ico" style="-webkit-mask-image:url(icons/youtube-white.png)"></i>@jaseelmkoyajmk</span></div>"""

TAG = '<div class="tag">PLUS TWO PHYSICS · RAY OPTICS</div>'
PYQ = '<div class="pyq">PYQ · Plus Two Christmas Exam 2019 · Q24 (4 marks)</div>'

def prism(w=900, labels=True, scale=1.0):
    # Equilateral prism A=60°, n=1.5, minimum deviation: ray inside parallel to base.
    # i = e = asin(1.5*sin30°) = 48.6°, D = 37.2° (true geometry)
    ax, ay, L, R, by = 450, 20, 230, 670, 401
    yr = 225
    t = (yr - ay) / (by - ay)
    x1, x2 = ax - t * (ax - L), ax + t * (R - ax)
    i = math.radians(48.59); d = (math.cos(math.radians(30) - i), math.sin(math.radians(30) - i))
    p0 = (x1 - 210 * d[0], yr - 210 * d[1])
    p3 = (x2 + 210 * d[0], yr - 210 * -d[1])
    ext = (x1 + 260 * d[0], yr + 260 * -d[1] * -1)
    ext = (x1 + 300 * d[0], yr + 300 * d[1])
    nl = 130; nx, ny = math.cos(math.radians(30)), math.sin(math.radians(30))
    s = f"""<svg width="{w}" height="{int(430*w/900)}" viewBox="0 0 900 430" style="align-self:center;margin-top:14px">
<polygon points="{ax},{ay} {L},{by} {R},{by}" fill="rgba(79,209,255,.13)" stroke="#4fd1ff" stroke-width="5"/>
<line x1="{x1-nl*nx}" y1="{yr-nl*ny}" x2="{x1+nl*nx}" y2="{yr+nl*ny}" stroke="#8a90b8" stroke-width="3" stroke-dasharray="8 8"/>
<line x1="{x2+nl*nx}" y1="{yr-nl*ny}" x2="{x2-nl*nx}" y2="{yr+nl*ny}" stroke="#8a90b8" stroke-width="3" stroke-dasharray="8 8"/>
<line x1="{x1}" y1="{yr}" x2="{ext[0]}" y2="{ext[1]}" stroke="#ff9f43" stroke-width="3" stroke-dasharray="10 8"/>
<polyline points="{p0[0]},{p0[1]} {x1},{yr} {x2},{yr} {p3[0]},{p3[1]}" fill="none" stroke="#ffd166" stroke-width="7" stroke-linejoin="round"/>
<polygon points="{(p0[0]+x1)/2+14*d[0]},{(p0[1]+yr)/2+14*d[1]} {(p0[0]+x1)/2-12*d[0]-9*d[1]},{(p0[1]+yr)/2-12*d[1]+9*d[0]} {(p0[0]+x1)/2-12*d[0]+9*d[1]},{(p0[1]+yr)/2-12*d[1]-9*d[0]}" fill="#ffd166"/>
<polygon points="{(x1+x2)/2+16},{yr} {(x1+x2)/2-10},{yr-11} {(x1+x2)/2-10},{yr+11}" fill="#ffd166"/>
"""
    if labels:
        s += f"""<text x="{ax}" y="{ay+80}" text-anchor="middle" font-family="Comic" font-size="40" fill="#ff6b9d">A</text>
<text x="{x1-95}" y="{yr-8}" font-family="Comic" font-size="38" fill="#5be49b">i</text>
<text x="{x1+30}" y="{yr+50}" font-family="Comic" font-size="34" fill="#5be49b">r₁</text>
<text x="{x2-70}" y="{yr+50}" font-family="Comic" font-size="34" fill="#5be49b">r₂</text>
<text x="{x2+80}" y="{yr-8}" font-family="Comic" font-size="38" fill="#5be49b">e</text>
<text x="{ext[0]-20}" y="{ext[1]+10}" font-family="Comic" font-size="38" fill="#ff9f43">δ</text>"""
    return s + "</svg>"

S1 = f"""{TAG}<div class="num">1/5</div>
<h1 style="font-size:76px">Plus Two Christmas exam-ൽ <span class="y">7-ൽ 6</span> തവണ വന്ന derivation! 🔺</h1>
{prism(820, labels=False)}
<div class="years"><b>2017</b><b>2018</b><b>2019</b><b class="x">2022</b><b>2023</b><b>2024</b><b>2025</b></div>
<div class="sub" style="font-size:48px;color:#fff">Prism-ന്റെ <span class="c">refractive index</span> — ഈ വർഷവും expect ചെയ്യാം 👉</div>"""

S2 = f"""{TAG}<div class="num">2/5</div>{PYQ}
<h2>Derive: prism-ന്റെ <span class="c">refractive index</span></h2>
<div class="eq big">n = sin[(A + D)/2] / sin(A/2)</div>
{prism(940)}
<div class="sub" style="margin-top:36px">A = angle of prism, D = <span class="o">angle of minimum deviation</span></div>"""

S3 = f"""{TAG}<div class="num">3/5</div>
<h2><span class="y">Step 1–2</span>: രണ്ട് angle relations</h2>
<div class="main"><div class="step"><div class="dot">1</div><div class="st">Geometry-യിൽ നിന്ന് (normals ചേരുന്ന quadrilateral):</div></div>
<div class="eq" style="margin-left:90px">r₁ + r₂ = A</div>
<div class="step"><div class="dot">2</div><div class="st">Deviation = <span style="white-space:nowrap">(i − r₁) + (e − r₂)</span></div></div>
<div class="eq" style="margin-left:90px">δ = i + e − A</div>
<div class="card" style="margin-top:34px"><div class="st">അതായത് <span class="g">A + δ = i + e</span> ✅<br><span style="color:#dfe3ff;font-size:40px">(Christmas 2017-ൽ ഇത് മാത്രം ചോദിച്ചു)</span></div></div></div>"""

S4 = f"""{TAG}<div class="num">4/5</div>
<h2><span class="y">Step 3–4</span>: Minimum deviation</h2>
<div class="main"><div class="step"><div class="dot">3</div><div class="st">δ = D ആകുമ്പോൾ <span class="g">i = e</span>, <span class="g">r₁ = r₂ = r</span> (ray base-ന് parallel)</div></div>
<div class="eq" style="margin-left:90px">2r = A → r = A/2</div>
<div class="eq" style="margin-left:90px">2i = A + D → i = (A + D)/2</div>
<div class="step"><div class="dot">4</div><div class="st">Snell's law: n = sin i / sin r</div></div>
<div class="eq big" style="margin-top:40px">n = sin[(A + D)/2] / sin(A/2)</div></div>"""

S5 = f"""{TAG}<div class="num">5/5</div>
<h2>Quick check ✍️</h2>
<div class="main" style="justify-content:space-evenly"><div class="card" style="margin-top:0"><div class="st">A = 60°, D = 30° ആണെങ്കിൽ<br>n = sin 45° / sin 30° = <span class="y">√2 ≈ 1.41</span></div></div>
<div class="sub" style="font-size:46px;color:#fff;margin-top:34px">Diagram + 4 steps = <span class="g">full 4 marks</span> നേടാം! 💯</div>
<div style="display:flex;flex-direction:column;gap:22px;align-items:center">
<div class="eq" style="align-self:center;font-size:56px">📌 Save &nbsp; 📤 Share &nbsp; 🔔 Follow</div>
<div class="sub" style="text-align:center;font-size:44px;margin-top:6px">Christmas exam-ന് പഠിക്കുന്ന friends-ന് അയച്ചു കൊടുക്കൂ</div></div></div>"""

STB = f"""{TAG}
<div class="pyq">Plus Two Christmas Exam · 7-ൽ 6 തവണ</div>
<h1 style="font-size:76px">ഇന്നലത്തെ PYQ <span class="y">recap</span>🔺</h1>
{prism(900)}
<div class="eq" style="align-self:center;font-size:50px">r₁ + r₂ = A &nbsp;·&nbsp; δ = i + e − A</div>
<div class="sub" style="text-align:center;font-size:46px;color:#fff">Minimum deviation: i = e, r = A/2</div>
<div class="eq big">n = sin[(A + D)/2] / sin(A/2)</div>
<div class="sub" style="text-align:center;font-size:44px">Full steps — ഇന്നലത്തെ post-ൽ 📌</div>"""

def page(body, h, top, bot, fb):
    return f"<html><head><meta charset='utf-8'><style>{CSS % (h, top, bot, fb)}</style></head><body><div class='wrap'>{body}</div>{FOOT}</body></html>"

F = (1350, 60, 130, 45)
JOBS = [("post1", S1, *F), ("post2", S2, *F), ("post3", S3, *F), ("post4", S4, *F), ("post5", S5, *F),
        ("storyB", STB, 1920, 250, 300, 270)]

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
