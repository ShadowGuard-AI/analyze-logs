#!/usr/bin/env python3
"""analyze-logs wordmark banner: below the surface of a harbor at dusk, looking along the floor
toward the sunken bell. The name is chalked in Coming Soon on one slate hung from the chain at
the bell crown, its edges softened by the water. No other writing in the picture."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(764)
V1 = "--v1" in sys.argv
W, H = 1200, 520
IRON = (16, 22, 19); KELP = (52, 98, 68); SANDC = (216, 198, 158); RED = (178, 44, 36)
img = Image.new("RGB", (W, H), IRON); d = ImageDraw.Draw(img, "RGBA")
for y in range(0, H):
    t = y / H
    base = (110, 144, 108)
    d.line([(0, y), (W, y)], fill=tuple(int(base[i] + (IRON[i] - base[i]) * (t ** 1.25)) for i in range(3)))
# wash of pale surface light and the undersides of hulls far above
d.ellipse([240, -70, 960, 90], fill=(226, 234, 200, 60))
for (x, y, w) in [(300, 22, 320), (820, 10, 380)]:
    d.ellipse([x - w / 2, y - 15, x + w / 2, y + 17], fill=(10, 16, 13, 130))
d.polygon([(0, 348), (W, 326), (W, H), (0, H)], fill=(104, 108, 74))
for y in range(352, H, 15):
    pts = [(x, y + math.sin(x / 90 + y) * 4) for x in range(0, W + 40, 40)]
    d.line(pts, fill=(188, 172, 128), width=2)
for _ in range(600):
    x, y = random.uniform(0, W), random.uniform(356, H)
    d.point((x, y), fill=random.choice([(232, 216, 176), (168, 152, 108)]))
def barrel(x, y, s):
    d.ellipse([x, y - 36 * s, x + 124 * s, y + 36 * s], fill=(96, 74, 48))
    d.ellipse([x + 88 * s, y - 36 * s, x + 124 * s, y + 36 * s], fill=(78, 58, 38))
    for hx in (14, 54, 96):
        d.line([(x + hx * s, y - 35 * s), (x + hx * s, y + 35 * s)], fill=(30, 28, 24), width=int(6 * s))
    for ly in range(-26, 27, 13):
        d.line([(x + 4, y + ly * s), (x + 118 * s, y + ly * s)], fill=(84, 62, 40), width=2)
    if V1:  # v1 flaw: chalk-like strokes on a barrel read as a second piece of writing
        for k in range(3):
            d.line([(x + 30 + k * 13, y - 10), (x + 38 + k * 13, y + 8)], fill=(230, 226, 214), width=3)
barrel(90, 322, 1.05); barrel(250, 348, .86)
cxr, cyr = 452, 398
for r in range(48, 6, -9):
    d.ellipse([cxr - r, cyr - r * .38, cxr + r, cyr + r * .38], outline=(150, 128, 88), width=4)
# the bell, right foreground, large, rim half sunk in sand
cx, cy, s = 905, 306, 1.5
d.polygon([(cx - 158, cy + 96), (cx + 40, cy + 52), (cx + 190, cy + 100), (cx - 80, cy + 128)], fill=(224, 206, 166))
pts = [(cx - 50, cy - 162), (cx - 92, cy - 114), (cx - 112, cy - 42), (cx - 130, cy + 38), (cx - 160, cy + 84),
       (cx + 160, cy + 84), (cx + 130, cy + 38), (cx + 112, cy - 42), (cx + 92, cy - 114), (cx + 50, cy - 162)]
d.polygon(pts, fill=KELP)
d.polygon([(cx + 16, cy - 162), (cx + 92, cy - 114), (cx + 112, cy - 42), (cx + 130, cy + 38), (cx + 160, cy + 84), (cx + 28, cy + 84)], fill=(20, 30, 25))
for gx in range(-80, 84, 15):
    top = cy - 162 + abs(gx) // 3
    d.line([(cx + gx, top), (cx + gx + 5, top + 24)], fill=(92, 148, 88), width=4)
d.line([(cx - 58, cy - 118), (cx - 26, cy - 54), (cx - 40, cy + 2)], fill=RED, width=3)
d.ellipse([cx - 160, cy + 58, cx + 160, cy + 110], fill=(58, 104, 70))
d.ellipse([cx - 130, cy + 68, cx + 130, cy + 102], fill=(5, 9, 7))
# mooring chain in a long catenary from the crown toward the light
prev = None
for i in range(26):
    t = i / 25
    x = cx - 4 - t * 300; y = (cy - 186) - math.sin(t * math.pi) * 60 - t * 130
    d.ellipse([x - 10, y - 14, x + 10, y + 14], outline=(24, 30, 26), width=5)
# gull feathers scattered on the sand near the bell, white going grey in the depth
def feather(x, y, s, ang):
    pts = [(x + math.cos(ang) * 32 * s * (t / 10) - math.sin(ang) * 6 * s * math.sin(t / 10 * 3.1),
            y + math.sin(ang) * 32 * s * (t / 10) + math.cos(ang) * 6 * s * math.sin(t / 10 * 3.1)) for t in range(11)]
    d.line(pts, fill=(224, 222, 212), width=int(5 * s))
for (x, y, s, a) in [(690, 448, 1, .4), (790, 474, .8, -.4), (620, 478, .7, .9)]:
    feather(x, y, s, a)
# the slate hung from the chain at the bell crown, the one inscription in the picture
sx0, sy0, sx1, sy1 = 596, 108, 856, 176
d.line([(cx - 120, cy - 218), (sx0 + 30, sy0)], fill=(24, 30, 26), width=4)
d.line([(cx - 40, cy - 224), (sx1 - 30, sy0)], fill=(24, 30, 26), width=4)
slate = Image.new("RGBA", (sx1 - sx0, sy1 - sy0), (14, 20, 17, 255))
sd = ImageDraw.Draw(slate)
sd.rectangle([0, 0, sx1 - sx0, sy1 - sy0], outline=(86, 140, 84), width=3)
try:
    f = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/ComingSoon.ttf", 40)
except Exception:
    f = ImageFont.load_default()
sd.text(((sx1 - sx0) / 2, (sy1 - sy0) / 2), "analyze-logs", font=f, fill=SANDC, anchor="mm")
if not V1:  # the water softens the chalk edges; v1 left them hard and dry, and too crisp to be underwater
    slate = slate.filter(ImageFilter.GaussianBlur(1.1))
img.paste(slate, (sx0, sy0), slate)
img = img.filter(ImageFilter.GaussianBlur(0.4))
out = "scratch/banner-v1.png" if V1 else "banner.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
