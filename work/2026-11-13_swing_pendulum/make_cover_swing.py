import sys, importlib.util
from reelkit import *
spec = importlib.util.spec_from_file_location("topic", sys.argv[1]); tp = importlib.util.module_from_spec(spec); spec.loader.exec_module(tp)
bg = make_bg(); fr = paint_bg(bg, 3.0); d = ImageDraw.Draw(fr)
paste(fr, pill("PLUS ONE PHYSICS", 40, bg=CYAN), W/2, 290)
paste(fr, text_img("PENDULUM", 150, color=YELLOW, max_w=1060), W/2, 340)
paste(fr, text_img("ഒരു *pendulum* കൊണ്ട് ഭൂമി കറങ്ങുന്നത് കാണാമോ?", 58, max_w=1000, hl=ORANGE), W/2, 540)
tp.foucault_view(fr, 1.2, 1.0, 22.0, 0.0, fc=(540, 1050))
paste(fr, pill("Simple Pendulum  ·  T = 2π√(L/g)", 42, fg=(9,14,38), bg=YELLOW), W/2, 1400)
paste(fr, pill("PYQ 2022", 34, fg=WHITE, bg=(80, 60, 160)), W/2, 1510)
footer(fr, d, "")
fr.convert("RGB").save(sys.argv[2], quality=92)
