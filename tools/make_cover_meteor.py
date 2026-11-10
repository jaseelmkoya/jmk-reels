import sys, os, math, importlib.util
from reelkit import *
spec = importlib.util.spec_from_file_location("topic", sys.argv[1]); tp = importlib.util.module_from_spec(spec); spec.loader.exec_module(tp)
bg = make_bg(); fr = paint_bg(bg, 3.0); d = ImageDraw.Draw(fr)
tp.draw_sky(fr, 2.0)
# a few big glowing meteors
for x, y, ln, w in ((820, 1030, 520, 10), (420, 860, 300, 6), (250, 1150, 220, 5)):
    from PIL import ImageFilter
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse((x - 45, y - 45, x + 45, y + 45), fill=(255, 190, 90, 150))
    g = g.filter(ImageFilter.GaussianBlur(40))
    fr.paste(g, (0, 0), g)
    tp.meteor(d, x, y, math.atan2(420, 760), ln, 1.0, w)
paste(fr, pill("PLUS ONE PHYSICS", 40, bg=CYAN), W/2, 300)
paste(fr, text_img("SHOOTING STARS", 130, color=YELLOW, max_w=1040), W/2, 370)
paste(fr, text_img("എന്തുകൊണ്ട് *കത്തുന്നു*?", 64, max_w=1000, hl=ORANGE), W/2, 790)
paste(fr, pill("K = ½ m v²  ·  Work-Energy Theorem", 40, fg=(9,14,38), bg=YELLOW), W/2, 1340)
paste(fr, pill("Taurid meteor shower · Nov 12", 34, fg=WHITE, bg=(80, 60, 160)), W/2, 1440)
footer(fr, d, "")
fr.convert("RGB").save(sys.argv[2], quality=92)
