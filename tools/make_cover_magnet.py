import sys, importlib.util
from reelkit import *
spec = importlib.util.spec_from_file_location("topic", sys.argv[1]); tp = importlib.util.module_from_spec(spec); spec.loader.exec_module(tp)
bg = make_bg(); fr = paint_bg(bg, 3.0); d = ImageDraw.Draw(fr)
paste(fr, pill("PLUS TWO PHYSICS", 40, bg=CYAN), W/2, 300)
paste(fr, text_img("MAGNET vs COPPER", 104, color=YELLOW, max_w=1060), W/2, 370)
paste(fr, text_img("*Magnet* എന്തുകൊണ്ട് ഇത്ര *പതുക്കെ* വീഴുന്നു?", 56, max_w=1000, hl=ORANGE), W/2, 515)
tp._mag(fr, 330, 1100); tp.pipe(fr, 330, False)
tp._mag(fr, 750, 900); tp.pipe(fr, 750, True)
paste(fr, tp.PL_LAB, 330, 1300); paste(fr, tp.CU_LAB, 750, 1300)
paste(fr, pill("Lenz's Law  ·  Eddy currents", 42, fg=(9,14,38), bg=YELLOW), W/2, 1420)
footer(fr, d, "")
fr.convert("RGB").save(sys.argv[2], quality=92)
