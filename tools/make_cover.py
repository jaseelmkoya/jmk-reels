import sys, importlib.util
from reelkit import *
spec = importlib.util.spec_from_file_location("topic", sys.argv[1]); tp = importlib.util.module_from_spec(spec); spec.loader.exec_module(tp)
bg = make_bg(); fr = paint_bg(bg, 3.0); d = ImageDraw.Draw(fr)
# Instagram grid shows the centre 3:4 (y 240-1680): keep everything there
paste(fr, pill("PLUS ONE PHYSICS", 40, bg=CYAN), W/2, 300)
big = text_img("INERTIA", 170, color=YELLOW, max_w=1040)
paste(fr, big, W/2, 360)
sub = text_img("ബസ് *brake* ഇടുമ്പോൾ നമ്മൾ *മുന്നോട്ട്* വീഴുന്നത് എന്തിന്?", 56, max_w=1000, hl=ORANGE)
paste(fr, sub, W/2, 610)
tp.draw_world(fr, 9.0, tp.LEAN_MAX, 400, braking=True, moving=False)
arrow(d, 690, 1010, 820, 1010, ORANGE, 14, 40)
paste(fr, pill("Newton's First Law", 44, fg=(9,14,38), bg=YELLOW), W/2, 1420)
footer(fr, d, "")
fr.save(sys.argv[2], quality=92)
