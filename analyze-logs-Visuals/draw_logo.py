#!/usr/bin/env python3
"""analyze-logs logo: a church bell resting on a harbor floor, in profile, kelp green darkened
to iron black at the shaded side, mouth tipped toward the viewer, one signal red seam line,
a chain trailing out of the upper frame, sand banked at the rim, the name chalked in Coming Soon."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
V1 = "--v1" in sys.argv
W, H = 900, 560
IRON = (16, 22, 19); KELP = (52, 98, 68); SANDC = (216, 198, 158); RED = (178, 44, 36)
img = Image.new("RGB", (W, H), IRON); d = ImageDraw.Draw(img, "RGBA")
for y in range(0, 430):
    t = y / 430
    base = (70, 104, 74)
    d.line([(0, y), (W, y)], fill=tuple(int(base[i] + (IRON[i] - base[i]) * t) for i in range(3)))
d.rectangle([0, 424, W, H], fill=(96, 100, 70))
cx, cy, s = 450, 268, 1.55
# anchor chain leaves the crown and trails out of the upper frame
x, y = cx + 6, cy - 200
while y > -24:
    d.ellipse([x - 12, y - 17, x + 12, y + 17], outline=(30, 38, 32), width=6)
    x += 16; y -= 33
# crown loop
d.ellipse([cx - 26, cy - 216, cx + 26, cy - 168], outline=(40, 78, 54), width=10)
# sand banked against one side of the rim
d.polygon([(cx - 168 * s * .62, cy + 66), (cx + 30, cy + 38), (cx + 176, cy + 72), (cx - 70, cy + 96)], fill=(224, 206, 166))
# bell body in profile
pts = [(cx - 52, cy - 168), (cx - 96, cy - 118), (cx - 118, cy - 44), (cx - 136, cy + 40), (cx - 168, cy + 88),
       (cx + 168, cy + 88), (cx + 136, cy + 40), (cx + 118, cy - 44), (cx + 96, cy - 118), (cx + 52, cy - 168)]
d.polygon(pts, fill=KELP)
# shaded side darkened to iron black
d.polygon([(cx + 18, cy - 168), (cx + 96, cy - 118), (cx + 118, cy - 44), (cx + 136, cy + 40), (cx + 168, cy + 88), (cx + 30, cy + 88)], fill=(20, 30, 25))
# kelp film at the crown
for gx in range(-84, 88, 16):
    top = cy - 168 + abs(gx) // 3
    d.line([(cx + gx, top), (cx + gx + 5, top + 26)], fill=(92, 148, 88), width=4)
# one signal red line along the shoulder, damage history rather than decoration
d.line([(cx - 62, cy - 122), (cx - 28, cy - 58), (cx - 44, cy + 2)], fill=RED, width=3)
if V1:  # v1 flaw: flat rim, plain mouth, a generic bell icon
    d.rectangle([cx - 168, cy + 80, cx + 168, cy + 98], fill=(34, 62, 46))
else:  # mouth tipped a few degrees toward the viewer: hollow inside as a deeper black crescent
    d.ellipse([cx - 168, cy + 62, cx + 168, cy + 116], fill=(58, 104, 70))
    d.ellipse([cx - 138, cy + 72, cx + 138, cy + 108], fill=(5, 9, 7))
    d.arc([cx - 138, cy + 60, cx + 138, cy + 102], 8, 172, fill=(8, 12, 10), width=8)
try:
    f = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/ComingSoon.ttf", 54)
except Exception:
    f = ImageFont.load_default()
d.text((450, 500), "analyze-logs", font=f, fill=SANDC, anchor="mm")
img = img.filter(ImageFilter.GaussianBlur(0.3))
out = "scratch/logo-v1.png" if V1 else "logo.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out)
if not V1:
    img.resize((64, 64)).save(__file__.rsplit("/", 1)[0] + "/scratch/logo64-ship.png")
print("saved", out)
