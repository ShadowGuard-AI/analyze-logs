#!/usr/bin/env python3
"""analyze-logs intro: the harbor floor alone, nothing that can be read. Sand rippled by current,
gull feathers and shells, the great bell resting on its sand bank, tarred barrels, a rope coil,
and the mooring chain rising out of the upper frame toward hull shadows and thinned surface light."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter
random.seed(518)
V1 = "--v1" in sys.argv
W, H = 1200, 520
IRON = (16, 22, 19); KELP = (52, 98, 68); SANDC = (216, 198, 158); RED = (178, 44, 36)
img = Image.new("RGB", (W, H), IRON); d = ImageDraw.Draw(img, "RGBA")
# green water, clouded higher up, a diffuse pale light from the surface that thins with depth
for y in range(0, H):
    t = y / H
    col = tuple(int((96 + (IRON[i] - 96) * t)) for i in range(3)) if False else None
    base = (104, 138, 104)
    col = tuple(int(base[i] + (IRON[i] - base[i]) * (t ** 1.3)) for i in range(3))
    d.line([(0, y), (W, y)], fill=col)
for _ in range(260):  # clouded upper water
    x, y = random.uniform(0, W), random.uniform(0, 190); r = random.uniform(8, 30)
    d.ellipse([x - r, y - r * .5, x + r, y + r * .5], fill=(190, 210, 180, 14))
# faint hull shadows overhead
for (x, y, w) in [(240, 26, 300), (760, 14, 360), (1060, 40, 200)]:
    d.ellipse([x - w / 2, y - 16, x + w / 2, y + 18], fill=(10, 16, 13, 120))
# harbor floor falling away into green darkness at the back
d.polygon([(0, 356), (W, 330), (W, H), (0, H)], fill=(104, 108, 74))
for y in range(356, H, 15):  # sand rippled by current
    pts = [(x, y + math.sin(x / 90 + y) * 4) for x in range(0, W + 40, 40)]
    d.line(pts, fill=(188, 172, 128), width=2)
for _ in range(700):
    x, y = random.uniform(0, W), random.uniform(360, H)
    d.point((x, y), fill=random.choice([(232, 216, 176), (168, 152, 108), (140, 138, 100)]))
# tarred barrels lying on their sides in the middle distance, to the left
def barrel(x, y, s):
    d.ellipse([x, y - 34 * s, x + 118 * s, y + 34 * s], fill=(96, 74, 48))
    d.ellipse([x + 84 * s, y - 34 * s, x + 118 * s, y + 34 * s], fill=(78, 58, 38))
    for hx in (14, 52, 92):
        d.line([(x + hx * s, y - 33 * s), (x + hx * s, y + 33 * s)], fill=(30, 28, 24), width=int(6 * s))
    for ly in range(-26, 27, 13):
        d.line([(x + 4, y + ly * s), (x + 112 * s, y + ly * s)], fill=(84, 62, 40), width=2)
barrel(120, 330, 1.0); barrel(268, 352, .82)
# flat coil of rope between bell and barrels, a spiral the current has not disturbed
cxr, cyr = 520, 404
for r in range(46, 6, -9):
    d.ellipse([cxr - r, cyr - r * .38, cxr + r, cyr + r * .38], outline=(150, 128, 88), width=4)
# the great bell resting on its sand bank, midground right
def bell(cx, cy, s, flat=False):
    # sand banked against one side of the rim
    d.polygon([(cx - 118 * s, cy + 62 * s), (cx + 40 * s, cy + 30 * s), (cx + 128 * s, cy + 66 * s), (cx - 60 * s, cy + 84 * s)], fill=(222, 204, 164))
    body = [(cx - 30 * s, cy - 128 * s), (cx + 30 * s, cy - 128 * s)]
    pts = [(cx - 34 * s, cy - 122 * s), (cx - 62 * s, cy - 84 * s), (cx - 76 * s, cy - 30 * s),
           (cx - 88 * s, cy + 26 * s), (cx - 108 * s, cy + 58 * s), (cx + 108 * s, cy + 58 * s),
           (cx + 88 * s, cy + 26 * s), (cx + 76 * s, cy - 30 * s), (cx + 62 * s, cy - 84 * s), (cx + 34 * s, cy - 122 * s)]
    d.polygon(pts, fill=(44, 84, 58))
    d.polygon([(cx + 10 * s, cy - 122 * s), (cx + 62 * s, cy - 84 * s), (cx + 76 * s, cy - 30 * s), (cx + 88 * s, cy + 26 * s), (cx + 108 * s, cy + 58 * s), (cx + 20 * s, cy + 58 * s)], fill=(22, 34, 27))
    for gx in range(-60, 60, 18):  # kelp growth at the crown
        d.line([(cx + gx * s, cy - 118 * s), (cx + gx * s + 6, cy - 96 * s)], fill=(86, 140, 84), width=3)
    d.line([(cx - 40 * s, cy - 88 * s), (cx - 18 * s, cy - 40 * s), (cx - 30 * s, cy + 4 * s)], fill=RED, width=2)
    if flat:  # v1 flaw: a flat rim and a plain mouth, a generic bell icon
        d.rectangle([cx - 108 * s, cy + 52 * s, cx + 108 * s, cy + 66 * s], fill=(30, 52, 40))
    else:  # mouth tipped toward the viewer: the hollow shows as a deeper black crescent
        d.ellipse([cx - 108 * s, cy + 40 * s, cx + 108 * s, cy + 78 * s], fill=(52, 96, 66))
        d.ellipse([cx - 88 * s, cy + 46 * s, cx + 88 * s, cy + 74 * s], fill=(6, 10, 8))
        d.arc([cx - 88 * s, cy + 40 * s, cx + 88 * s, cy + 70 * s], 10, 170, fill=(10, 14, 11), width=6)
bell(880, 330, 1.12, flat=V1)
# mooring chain rising from the bell crown out of the upper frame
x, y = 880, 196
while y > -20:
    d.ellipse([x - 11, y - 16, x + 11, y + 16], outline=(24, 30, 26), width=5)
    x += 7; y -= 30
# the lower rim of the great bell entering from the right edge, foreground
d.ellipse([1058, 420, 1330, 560], fill=(40, 78, 54))
d.ellipse([1084, 442, 1300, 548], fill=(8, 12, 10))
d.arc([1058, 420, 1330, 560], 90, 260, fill=(90, 146, 88), width=7)
# scattered gull feathers and small shells on the sand
def feather(x, y, s, ang):
    pts = []
    for t in range(0, 11):
        tt = t / 10; pts.append((x + math.cos(ang) * 34 * s * tt - math.sin(ang) * 7 * s * math.sin(tt * 3.1), y + math.sin(ang) * 34 * s * tt + math.cos(ang) * 7 * s * math.sin(tt * 3.1)))
    d.line(pts, fill=(232, 230, 220), width=int(5 * s))
    d.line([(x, y), (x + math.cos(ang) * 38 * s, y + math.sin(ang) * 38 * s)], fill=(196, 190, 178), width=1)
for (x, y, s, a) in [(150, 452, 1, .4), (330, 478, .8, -.3), (700, 462, .9, .9), (980, 486, .75, -.6), (560, 492, .6, .2)]:
    feather(x, y, s, a)
for _ in range(16):
    x, y = random.uniform(20, 1180), random.uniform(420, 508); r = random.uniform(4, 8)
    d.ellipse([x - r, y - r * .6, x + r, y + r * .6], fill=(226, 214, 190), outline=(180, 168, 142))
img = img.filter(ImageFilter.GaussianBlur(0.5))
out = "scratch/intro-v1.png" if V1 else "intro-banner.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
