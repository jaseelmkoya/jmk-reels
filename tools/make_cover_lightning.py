import sys, importlib.util
from reelkit import *
spec = importlib.util.spec_from_file_location("topic", sys.argv[1]); tp = importlib.util.module_from_spec(spec); spec.loader.exec_module(tp)
bg = make_bg(); fr = paint_bg(bg, 3.0); d = ImageDraw.Draw(fr)
tp.rain(d, 2.0, 0.7)
tp.ground(d)
tp.draw_car(fr, glow=0.9)
import random
tp.bolt(d, tp.CX0 + 350, 1235 - 235, 0.33)
tp.flow_dots(d, 1.0, 0.0)
paste(fr, pill("PLUS TWO PHYSICS", 40, bg=CYAN), W/2, 300)
paste(fr, text_img("LIGHTNING", 150, color=YELLOW, max_w=1040), W/2, 360)
paste(fr, text_img("*car*-നുള്ളിൽ നമ്മൾ *safe* ആണോ?", 64, max_w=1000, hl=ORANGE), W/2, 580)
paste(fr, pill("Electrostatic Shielding  ·  E = 0", 42, fg=(9,14,38), bg=YELLOW), W/2, 1350)
paste(fr, pill("Gauss's theorem", 34, fg=WHITE, bg=(80, 60, 160)), W/2, 1460)
footer(fr, d, "")
fr.convert("RGB").save(sys.argv[2], quality=92)
