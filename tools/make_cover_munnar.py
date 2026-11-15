import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from storykit import *
import importlib.util
spec = importlib.util.spec_from_file_location("tp", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topics", "munnar_chill.py"))
tp = importlib.util.module_from_spec(spec); spec.loader.exec_module(tp)
fr = Image.new("RGB", (W, H)); fr.paste(push(tp.night_base(2.0), 3.0, 10, 1.0, 1.0), (0, 0)); d = ImageDraw.Draw(fr)
tp.fog(fr, 3.0, 1.0)
for i in range(5):
    x = 140 + i * 150
    tp.wavy(d, x, 1150, x, 760, tp.HEAT, ph=i)
tp.thermo(d, 900, 820, 7.9)
fr.paste(VIG, (0, 0), VIG)
paste(fr, headline("KERALA *7.9°C!*", hl=CYAN, size=140), W / 2, 260)
paste(fr, text_img("മേഘമില്ലാത്ത രാത്രി കൂടുതൽ *തണുക്കുന്നത്* എന്തുകൊണ്ട്?", 64, max_w=980, hl=CYAN), W / 2, 460)
paste(fr, pill("Radiation · H = eσAT⁴ · Plus One", 36, bg=YELLOW), W / 2, 1450)
footer(fr, ImageDraw.Draw(fr), "")
fr.save(sys.argv[1], quality=92)
