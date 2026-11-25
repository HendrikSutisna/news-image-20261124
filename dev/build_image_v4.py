#!/usr/bin/env python3
"""Build the 24 Nov 2026 newspaper front page v4 (1024x1024) for the
make.fun news-image-20261124 entry. Build-time tooling only; the entry
program (main.ts) just copies the generated entry.png.

v4 = v2 story set restored (Banten panel back, US panel out) + craft polish
(see v4/BUILD_NOTES.md):
- Full-day story selection: Hormuz lead updated to the 4th tanker
  (IRGC claim, unverified); Gaza, Zaporizhzhia, Indonesia factory fire
  and Shenzhou-24 replace the Asia-heavy v1 grid.
- Lead pictogram and panel icons redrawn for clarity: a naval mine in
  the water, a second tanker silhouette, cleaner flames and smoke;
  each grid icon is now a small scene (building+blast, flats+blast,
  factory+flames, rocket+orbit) instead of an abstract pictogram.
- All text still set in real fonts (DejaVu via PIL); no AI text.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (248, 245, 236)
INK = (17, 17, 17)
WHITE = (255, 253, 246)
RED = (179, 32, 44)
NAVY = (31, 58, 95)
SLATE = (52, 68, 88)
GREY = (120, 120, 115)
LIGHT = (238, 234, 222)
ORANGE = (255, 140, 30)
YELLOW = (255, 210, 80)
SMOKE = (150, 150, 148)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def star(d, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def flame(d, cx, cy, s):
    """Simple fire puff: orange outer ellipse, yellow inner ellipse."""
    d.ellipse([cx - s, cy - s * 1.3, cx + s, cy + s], fill=ORANGE)
    d.ellipse([cx - s * 0.45, cy - s * 0.5, cx + s * 0.45, cy + s * 0.8],
              fill=YELLOW)


def smoke(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], fill=(180, 180, 178))


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# outer frame
d.rectangle([8, 8, 1015, 1015], outline=INK, width=3)

# masthead band
d.rectangle([11, 11, 1012, 108], fill=INK)
mast = font(F_SERIF_B, 72)
d.text((512, 16), "WORLD NEWS", font=mast, fill=WHITE, anchor="ma")
# red rule under masthead
d.rectangle([11, 108, 1012, 114], fill=RED)

# dateline
date_f = font(F_SANS_B, 26)
dateline = "T U E S D A Y   2 4   N O V E M B E R   2 0 2 6"
d.text((512, 124), dateline, font=date_f, fill=INK, anchor="ma")
d.line([28, 160, 996, 160], fill=INK, width=2)

# ---------- lead panel: Hormuz, 4th tanker ----------
LY0, LY1 = 172, 420
d.rectangle([28, LY0, 996, LY1], outline=INK, width=2)
d.rectangle([28, LY0, 996, LY0 + 6], fill=RED)
kick_f = font(F_SANS_B, 20)
d.text((44, LY0 + 18), "STRAIT OF HORMUZ", font=kick_f, fill=RED)
head_f = font(F_SANS_B, 44)
lead_head = wrap(d, "IRGC: 4TH TANKER HIT BY MINE IN HORMUZ", head_f, 600)
y = draw_text_block(d, 44, LY0 + 52, lead_head, head_f, INK, 52)
sum_f = font(F_SANS, 24)
lead_sum = wrap(
    d,
    "Iran's Guards say a fourth oil tanker exploded after "
    "hitting a mine; the claim is unverified.",
    sum_f, 600)
draw_text_block(d, 44, y + 8, lead_sum, sum_f, (60, 60, 60), 31)
assert y + 8 + 31 * len(lead_sum) <= LY1 - 6, "lead summary overflows"

# lead pictogram: tanker ablaze, mine in the water, second tanker behind
PX0, PY0, PX1, PY1 = 668, 196, 980, 404
d.rectangle([PX0, PY0, PX1, PY1], fill=SLATE)
d.rectangle([PX0, PY0, PX1, PY1], outline=INK, width=2)
# distant tanker silhouette (grey, upper left)
d.polygon([(690, 252), (800, 252), (788, 272), (702, 272)], fill=(140, 155, 175))
d.rectangle([742, 232, 772, 252], fill=(140, 155, 175))
# sea
d.rectangle([PX0, 330, PX1, PY1], fill=(38, 52, 70))
for wx in range(PX0 + 12, PX1 - 12, 34):
    d.arc([wx, 336, wx + 30, 356], 0, 180, fill=(150, 180, 210), width=3)
# main tanker hull
d.polygon([(700, 300), (948, 300), (928, 336), (720, 336)], fill=(200, 60, 50))
d.rectangle([700, 292, 948, 302], fill=(140, 30, 25))
# containers
d.rectangle([716, 262, 772, 292], fill=(240, 200, 60))
d.rectangle([780, 262, 836, 292], fill=(90, 180, 120))
d.rectangle([844, 262, 900, 292], fill=(220, 220, 220))
# bridge tower
d.rectangle([908, 238, 940, 292], fill=(230, 230, 230))
d.rectangle([912, 246, 936, 262], fill=(40, 80, 120))
# flames above the deck (ellipse puffs, clear of the label)
flame(d, 800, 252, 15)
flame(d, 862, 246, 18)
flame(d, 916, 254, 13)
# naval mine in the foreground water (spiky black circle)
mx, my, mr = 724, 372, 15
for ang in range(0, 360, 45):
    a = math.radians(ang)
    x1, y1 = mx + mr * math.cos(a), my + mr * math.sin(a)
    x2, y2 = mx + (mr + 9) * math.cos(a), my + (mr + 9) * math.sin(a)
    d.line([x1, y1, x2, y2], fill=INK, width=4)
d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=INK)
d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(90, 90, 90))
d.text((PX0 + 12, PY0 + 8), "FOURTH TANKER ABLAZE", font=font(F_SANS_B, 17),
       fill=(255, 255, 255))

# ---------- 2x2 grid ----------
GX0, GX1 = 28, 996
GY = [432, 672, 922]
PW = 478
panels = [
    # (kicker, kicker_color, headline, summary, icon)
    ("GAZA", RED,
     "ISRAEL KILLS HAMAS SECURITY CHIEF",
     "Hamas security chief Naeem Abu Nahel killed in Gaza City; six others also died.",
     "blast"),
    ("UKRAINE", NAVY,
     "RUSSIAN STRIKE KILLS 2, WOUNDS 40",
     "Overnight attack hits flats in Zaporizhzhia; four children hurt, governor says.",
     "flats"),
    ("INDONESIA", (140, 60, 20),
     "FACTORY FIRE TOLL REACHES 26",
     "Death toll confirmed in the Banten candy factory fire; dozens still missing.",
     "factory"),
    ("SPACE", (20, 110, 60),
     "PAKISTAN'S FIRST MAN IN SPACE",
     "China unveils Shenzhou-24 crew; Zeeshan Ali will be the first foreigner on Tiangong.",
     "rocket"),
]


def draw_icon(d, x0, y0, s, kind):
    d.rectangle([x0, y0, x0 + s, y0 + s], fill=LIGHT, outline=GREY, width=1)
    pad = 10
    if kind == "blast":
        # dark building with a broken top, blast star above it
        d.rectangle([x0 + pad + 6, y0 + pad + 22, x0 + s - pad - 6, y0 + s - pad - 4],
                    fill=(70, 70, 78))
        d.polygon([(x0 + pad + 6, y0 + pad + 22), (x0 + pad + 16, y0 + pad + 12),
                   (x0 + pad + 26, y0 + pad + 22), (x0 + pad + 36, y0 + pad + 14),
                   (x0 + s - pad - 6, y0 + pad + 22)], fill=(70, 70, 78))
        for wy in (y0 + pad + 30, y0 + pad + 40):
            for wx in (x0 + pad + 12, x0 + s // 2 - 4, x0 + s - pad - 20):
                d.rectangle([wx, wy, wx + 7, wy + 7], fill=(220, 220, 210))
        star(d, x0 + s - 18, y0 + 18, 13, 6, 8, ORANGE)
        star(d, x0 + s - 18, y0 + 18, 7, 3, 8, YELLOW)
    elif kind == "flats":
        # apartment block with window grid, blast star on the broken corner
        d.rectangle([x0 + pad + 4, y0 + pad + 8, x0 + s - pad - 4, y0 + s - pad - 4],
                    fill=(150, 160, 175))
        d.rectangle([x0 + pad + 4, y0 + pad + 8, x0 + s - pad - 4, y0 + pad + 16],
                    fill=(110, 120, 138))
        for r in range(3):
            for c in range(4):
                wx = x0 + pad + 10 + c * 12
                wy = y0 + pad + 22 + r * 11
                d.rectangle([wx, wy, wx + 7, wy + 7], fill=(40, 55, 75))
        # broken top-right corner: dark triangle + star
        d.polygon([(x0 + s - pad - 4, y0 + pad + 8), (x0 + s - pad - 4, y0 + pad + 24),
                   (x0 + s - pad - 20, y0 + pad + 8)], fill=INK)
        star(d, x0 + s - 16, y0 + 16, 11, 5, 8, ORANGE)
    elif kind == "factory":
        # factory with sawtooth roof, flames on the roof, smoke
        d.rectangle([x0 + pad + 4, y0 + pad + 26, x0 + s - pad - 4, y0 + s - pad - 4],
                    fill=(120, 110, 100))
        for i, tx in enumerate(range(x0 + pad + 4, x0 + s - pad - 4, 14)):
            d.polygon([(tx, y0 + pad + 26), (tx + 7, y0 + pad + 14),
                       (tx + 14, y0 + pad + 26)], fill=(120, 110, 100))
        d.rectangle([x0 + pad + 10, y0 + s - pad - 18, x0 + pad + 20, y0 + s - pad - 8],
                    fill=(60, 60, 60))
        d.rectangle([x0 + s - pad - 20, y0 + s - pad - 18, x0 + s - pad - 10,
                     y0 + s - pad - 8], fill=(60, 60, 60))
        flame(d, x0 + s // 2 - 8, y0 + pad + 12, 9)
        flame(d, x0 + s // 2 + 8, y0 + pad + 14, 7)
        smoke(d, x0 + s - 14, y0 + pad + 2, 6)
    elif kind == "rocket":
        # rocket with orbit ring and station dot
        d.ellipse([x0 + pad - 2, y0 + pad + 2, x0 + s - pad + 2, y0 + s - pad - 2],
                  outline=(90, 130, 180), width=2)
        d.ellipse([x0 + s - 16, y0 + pad + 8, x0 + s - 8, y0 + pad + 16],
                  fill=NAVY)
        # rocket body, tilted slightly: draw upright for clarity
        cx = x0 + s // 2 - 2
        d.polygon([(cx - 7, y0 + pad + 30), (cx, y0 + pad + 12),
                   (cx + 7, y0 + pad + 30)], fill=RED)
        d.rounded_rectangle([cx - 7, y0 + pad + 28, cx + 7, y0 + s - pad - 16],
                            radius=3, fill=(230, 230, 225))
        d.rectangle([cx - 7, y0 + pad + 34, cx + 7, y0 + pad + 38], fill=NAVY)
        d.polygon([(cx - 7, y0 + s - pad - 16), (cx - 14, y0 + s - pad - 6),
                   (cx - 7, y0 + s - pad - 10)], fill=RED)
        d.polygon([(cx + 7, y0 + s - pad - 16), (cx + 14, y0 + s - pad - 6),
                   (cx + 7, y0 + s - pad - 10)], fill=RED)
        flame(d, cx, y0 + s - pad - 6, 6)
        for sx, sy in [(x0 + pad + 4, y0 + pad + 6), (x0 + pad + 16, y0 + s - pad - 8),
                       (x0 + s - pad - 6, y0 + s // 2)]:
            star(d, sx, sy, 3, 1.5, 4, INK)


for i, (kicker, kcol, headline, summary, icon) in enumerate(panels):
    row, col = divmod(i, 2)
    x0 = GX0 + col * (PW + 12)
    y0 = GY[row]
    y1 = GY[row + 1] - 10
    d.rectangle([x0, y0, x0 + PW, y1], fill=WHITE, outline=INK, width=2)
    d.rectangle([x0, y0, x0 + PW, y0 + 6], fill=kcol)
    d.text((x0 + 16, y0 + 16), kicker, font=font(F_SANS_B, 18), fill=kcol)
    draw_icon(d, x0 + PW - 86, y0 + 14, 70, icon)
    hf = font(F_SANS_B, 29)
    hl = wrap(d, headline, hf, PW - 32 - 90)
    y = draw_text_block(d, x0 + 16, y0 + 46, hl, hf, INK, 35)
    sf = font(F_SANS, 20)
    sl = wrap(d, summary, sf, PW - 32)
    draw_text_block(d, x0 + 16, y + 6, sl, sf, (60, 60, 60), 25)
    assert len(hl) <= 2 and len(sl) <= 2, \
        f"panel {kicker} overflows: headline {len(hl)} lines, summary {len(sl)} lines"
    assert y + 6 + 25 * len(sl) <= y1 - 6, f"panel {kicker} overflows bottom"

# ---------- bottom strip ----------
SY0, SY1 = 932, 1012
d.rectangle([28, SY0, 996, SY1], fill=NAVY)
strip_f = font(F_SANS, 21)
strip_b = font(F_SANS_B, 21)
d.text((44, SY0 + 8), "ALSO:", font=strip_b, fill=(255, 220, 90))
d.text((128, SY0 + 8), "Quake of 5.6 shakes Nepal's far east; no casualties reported.",
       font=strip_f, fill=WHITE)
d.text((44, SY0 + 42), "Kyiv: Germany first to get Ukraine's Delta war software.",
       font=strip_f, fill=WHITE)

img.save("/home/hatch/workspace/makefun-news-image-24/v4/entry/entry.png")
print("saved v4/entry.png")
