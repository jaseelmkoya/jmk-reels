import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from storykit import *
import importlib.util
spec = importlib.util.spec_from_file_location("tp", os.path.join(os.path.dirname(os.path.abspath(__file__)), "topics", "train_brake.py"))
tp = importlib.util.module_from_spec(spec); spec.loader.exec_module(tp)
fr = Image.new("RGB", (W, H)); fr.paste(push(tp.NIGHT, 3.0, 10, 1.0, 1.0), (0, 0)); d = ImageDraw.Draw(fr)
for sx in (-1, 1):
    d.line((W / 2 + sx * 40, 760, W / 2 + sx * 560, H), fill=(140, 150, 170), width=12)
tp.loco_front(d, W / 2, 1050, 1.5)
L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse((W / 2 - 330, 1160, W / 2 + 330, 1330), fill=(255, 240, 180, 60))
fr.paste(L.filter(ImageFilter.GaussianBlur(30)), (0, 0), L.filter(ImageFilter.GaussianBlur(30)))
tp.gauge(d, 880, 760, 105, 5.0, col=tp.RED)
fr.paste(VIG, (0, 0), VIG)
paste(fr, headline("BRAKE *FAILED?*", hl=tp.RED, size=130), W / 2, 230)
paste(fr, text_img("Train-ന്റെ *brake* എങ്ങനെ work ചെയ്യുന്നു?", 66, max_w=980, hl=YELLOW), W / 2, 430)
paste(fr, pill("Pascal's law · F = P × A · Plus One", 36, bg=YELLOW), W / 2, 1450)
footer(fr, ImageDraw.Draw(fr), "")
fr.save(sys.argv[1], quality=92)
