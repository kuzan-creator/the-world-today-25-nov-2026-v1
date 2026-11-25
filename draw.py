#!/usr/bin/env python3
"""Draw "The World in One Day" -- Wednesday 25 November 2026.

A single cream newspaper page summing up the day's world news:
40 stories, 3 heroes, 12 illustrated cards, a list of 25, a world
map with numbered pins, a date check and a sources footer.

News chosen by virality: the lead and cards are the stories most
widely reported by the big wires on Wednesday 25 November 2026
itself (Houthi strike on Riyadh, Shenzhou-24, Chen Jining probe,
US tariffs, Huawei verdict, Cartagena standoff). Stories that
broke on 23-24 Nov are named in DATE CHECK as left out.

Everything is drawn from scratch with PIL shapes; no outside images.
Run:  python3 draw.py [output.png] [lead]   (lead = riyadh | space)
"""
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "entry.png"
LEAD = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("LEAD", "riyadh")

PAGE_W, PAGE_H = 1024, 1024
EDGE = 24
RIGHT = PAGE_W - EDGE

PAPER = (247, 240, 221)
CARD = (255, 253, 247)
INK = (26, 26, 26)
SOFT = (74, 74, 70)
NAVY = (18, 38, 74)
RED = (176, 32, 28)
SEA = (127, 179, 213)
LAND = (214, 208, 182)
LAND_LINE = (96, 96, 84)
RULE = (198, 192, 177)

REGION = {
    "EU":    ((46, 95, 163), "EUROPE", 6),
    "ME":    ((176, 32, 28), "MIDDLE EAST", 6),
    "AF":    ((120, 90, 40), "AFRICA", 1),
    "AP":    ((81, 160, 160), "ASIA", 9),
    "AM":    ((53, 129, 56), "AMERICAS", 9),
    "TECH":  ((108, 79, 161), "TECH", 4),
    "WORLD": ((90, 90, 90), "WORLD", 5),
}
BAR_ORDER = ["EU", "ME", "AF", "AP", "AM", "TECH", "WORLD"]
BAR_EDGES = [24, 164, 304, 374, 574, 774, 884, 1000]

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
LIB_DIR = Path("/usr/share/fonts/truetype/liberation")


def _load(d, name, size):
    return ImageFont.truetype(str(d / name), size)


def f_serif_b(s):
    return _load(FONT_DIR, "DejaVuSerif-Bold.ttf", s)


def f_sans_b(s):
    return _load(FONT_DIR, "DejaVuSans-Bold.ttf", s)


def f_sans(s):
    return _load(FONT_DIR, "DejaVuSans.ttf", s)


def f_lib_b(s):
    return _load(LIB_DIR, "LiberationSans-Bold.ttf", s)


def f_lib(s):
    return _load(LIB_DIR, "LiberationSans-Regular.ttf", s)


def f_lib_serif_b(s):
    return _load(LIB_DIR, "LiberationSerif-Bold.ttf", s)


def f_lib_serif_i(s):
    return _load(LIB_DIR, "LiberationSerif-Italic.ttf", s)


def wrap(text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if fnt.getlength(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def number_disc(d, cx, cy, r, num, fill=RED):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)
    d.text((cx, cy), str(num), font=f_sans_b(11 if r <= 9 else 12),
           fill=(255, 255, 255), anchor="mm")


# ------------------------------------------------------------------ top

def draw_masthead(d):
    d.rectangle((0, 0, PAGE_W, 26), fill=NAVY)
    d.text((EDGE, 6), "THE WORLD IN ONE DAY",
           font=f_sans_b(13), fill=(255, 255, 255))
    right = ("40 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED "
             "WEDNESDAY 25 NOVEMBER 2026")
    d.text((RIGHT, 7), right, font=f_sans_b(11),
           fill=(255, 255, 255), anchor="ra")


def draw_headline(d):
    d.text((PAGE_W // 2, 33), "Wednesday 25 November 2026",
           font=f_lib_serif_b(56), fill=INK, anchor="ma")
    if LEAD == "space":
        sub = ("Shenzhou-24 carries Pakistan's first astronaut \u00b7 "
               "Houthi drone hits Riyadh tower \u00b7 China probes "
               "Politburo member")
    else:
        sub = ("Houthi drone hits Riyadh tower \u00b7 Shenzhou-24 carries "
               "Pakistan's first astronaut \u00b7 China probes "
               "Politburo member")
    d.text((PAGE_W // 2, 98), sub, font=f_lib_serif_i(16), fill=RED,
           anchor="ma")
    d.line((EDGE, 122, RIGHT, 122), fill=RULE, width=1)


NUMBERS = [
    ("11", "hurt in Riyadh tower strike"),
    ("1st", "Pakistani in orbit"),
    ("4th", "Politburo member probed"),
    ("16", "partners face new US tariffs"),
    ("25", "hostages held in Cartagena"),
    ("204", "runs off 53 balls, aged 15"),
]


def draw_numbers(d):
    top, bottom = 125, 164
    cell = (RIGHT - EDGE) / len(NUMBERS)
    for i, (figure, label) in enumerate(NUMBERS):
        cx = EDGE + cell * (i + 0.5)
        d.text((cx, top + 1), figure, font=f_lib_serif_b(23), fill=RED,
               anchor="ma")
        d.text((cx, top + 23), label, font=f_lib(10), fill=SOFT,
               anchor="ma")
        if i:
            x = EDGE + cell * i
            d.line((x, top + 4, x, bottom - 4), fill=RULE, width=1)
    d.line((EDGE, bottom, RIGHT, bottom), fill=RULE, width=1)


def draw_region_bar(d):
    top, bottom = 168, 190
    for key, x0, x1 in zip(BAR_ORDER, BAR_EDGES, BAR_EDGES[1:]):
        colour, label, count = REGION[key]
        d.rectangle((x0, top, x1, bottom), fill=colour)
        d.text(((x0 + x1) // 2, top + 4), f"{label} {count}",
               font=f_lib_b(12), fill=(255, 255, 255), anchor="ma")


# ------------------------------------------------------------ hero scenes

def scene_tower(d, x0, y0, x1, y1):
    """Riyadh tower at dusk: pale sky, glass tower, drone, smoke."""
    w, h = x1 - x0, y1 - y0
    for i, col in enumerate([(250, 214, 150), (244, 190, 130),
                             (232, 160, 120), (214, 140, 130)]):
        d.rectangle((x0, y0 + i * h // 4, x1, y0 + (i + 1) * h // 4),
                    fill=col)
    d.ellipse((x0 + w * 0.78, y0 + 8, x0 + w * 0.78 + 30, y0 + 36),
              fill=(255, 240, 170))
    for cx, cy, r in [(0.12, 0.14, 15), (0.24, 0.09, 19), (0.38, 0.16, 12)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r // 2,
                   x0 + w * cx + r, y0 + h * cy + r // 2),
                  fill=(245, 240, 230))
    # skyline base
    for bx, bw, bh in [(0.02, 0.10, 0.30), (0.14, 0.08, 0.38),
                       (0.66, 0.09, 0.34), (0.78, 0.10, 0.28),
                       (0.90, 0.08, 0.36)]:
        d.rectangle((x0 + w * bx, y1 - h * bh, x0 + w * (bx + bw), y1),
                    fill=(90, 80, 95))
    # the tower: pale glass slab, dark top, lit windows
    tx0, tx1 = x0 + int(w * 0.40), x0 + int(w * 0.60)
    d.rectangle((tx0, y0 + 26, tx1, y1), fill=(200, 215, 225))
    d.rectangle((tx0, y0 + 26, tx1, y0 + 44), fill=(40, 48, 66))
    for r in range(5):
        for c in range(3):
            wx = tx0 + 10 + c * 20
            wy = y0 + 52 + r * 13
            lit = (r * 3 + c) % 3 != 2
            d.rectangle((wx, wy, wx + 12, wy + 8),
                        fill=(255, 205, 90) if lit else (120, 135, 150))
    # blast glow near the top, smoke curling up
    d.ellipse((tx0 + 8, y0 + 30, tx0 + 52, y0 + 58), fill=(255, 120, 30))
    d.ellipse((tx0 + 16, y0 + 36, tx0 + 44, y0 + 54), fill=(255, 205, 60))
    for cx, cy, r in [(0.50, 0.10, 13), (0.55, 0.04, 10), (0.45, 0.05, 9)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r,
                   x0 + w * cx + r, y0 + h * cy + r),
                  fill=(110, 105, 110))
    # small drone, upper left
    dx, dy = x0 + int(w * 0.16), y0 + int(h * 0.30)
    d.ellipse((dx - 12, dy - 3, dx + 12, dy + 3), fill=(30, 30, 36))
    d.ellipse((dx - 16, dy - 6, dx - 10, dy), fill=(60, 60, 66))
    d.ellipse((dx + 10, dy - 6, dx + 16, dy), fill=(60, 60, 66))
    # street with two tiny cars
    d.rectangle((x0, y1 - 10, x1, y1), fill=(70, 66, 72))
    for cx, col in [(0.10, (220, 60, 50)), (0.82, (60, 120, 200))]:
        px = x0 + int(w * cx)
        d.rectangle((px, y1 - 18, px + 22, y1 - 10), fill=col)


def scene_rocket(d, x0, y0, x1, y1):
    """Shenzhou-24 launch: bright blue sky, white rocket, flame."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y1), fill=(146, 196, 235))
    for cx, cy, r in [(0.10, 0.12, 16), (0.22, 0.08, 20), (0.82, 0.14, 15),
                      (0.70, 0.07, 12)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r // 2,
                   x0 + w * cx + r, y0 + h * cy + r // 2),
                  fill=(250, 250, 245))
    d.ellipse((x0 + w * 0.86, y0 + 6, x0 + w * 0.86 + 26, y0 + 32),
              fill=(255, 240, 170))
    # green ground
    d.rectangle((x0, y1 - 22, x1, y1), fill=(86, 148, 84))
    # launch tower, left
    d.rectangle((x0 + 22, y0 + 34, x0 + 40, y1 - 22), fill=(120, 120, 118))
    for r in range(4):
        d.line((x0 + 22, y0 + 44 + r * 16, x0 + 40, y0 + 54 + r * 16),
               fill=(90, 90, 88), width=2)
    # rocket body centre-right
    rx0, rx1 = x0 + int(w * 0.52), x0 + int(w * 0.66)
    d.rectangle((rx0, y0 + 30, rx1, y1 - 46), fill=(245, 245, 240))
    d.polygon([(rx0, y0 + 30), (rx1, y0 + 30),
               ((rx0 + rx1) // 2, y0 + 8)], fill=(200, 40, 36))
    d.rectangle((rx0, y0 + 62, rx1, y0 + 74), fill=(200, 40, 36))
    d.rectangle((rx0 + 8, y0 + 88, rx1 - 8, y0 + 100), fill=(60, 110, 180))
    # fins
    d.polygon([(rx0, y1 - 46), (rx0 - 14, y1 - 30), (rx0, y1 - 28)],
              fill=(200, 40, 36))
    d.polygon([(rx1, y1 - 46), (rx1 + 14, y1 - 30), (rx1, y1 - 28)],
              fill=(200, 40, 36))
    # flame and smoke
    fx = (rx0 + rx1) // 2
    d.polygon([(fx - 14, y1 - 44), (fx, y1 - 8), (fx + 14, y1 - 44)],
              fill=(255, 120, 20))
    d.polygon([(fx - 7, y1 - 44), (fx, y1 - 20), (fx + 7, y1 - 44)],
              fill=(255, 205, 60))
    for cx, cy, r in [(0.42, 0.86, 14), (0.62, 0.90, 17), (0.76, 0.86, 12)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r,
                   x0 + w * cx + r, y0 + h * cy + r),
                  fill=(235, 232, 225))


def scene_skyline(d, x0, y0, x1, y1):
    """Shanghai by day: pale sky, towers, river, red flag."""
    w, h = x1 - x0, y1 - y0
    d.rectangle((x0, y0, x1, y1), fill=(178, 208, 228))
    for cx, cy, r in [(0.10, 0.10, 14), (0.30, 0.07, 18), (0.72, 0.12, 13)]:
        d.ellipse((x0 + w * cx - r, y0 + h * cy - r // 2,
                   x0 + w * cx + r, y0 + h * cy + r // 2),
                  fill=(248, 248, 243))
    d.ellipse((x0 + w * 0.84, y0 + 8, x0 + w * 0.84 + 26, y0 + 34),
              fill=(255, 240, 170))
    # river at the base
    d.rectangle((x0, y1 - 24, x1, y1), fill=(90, 140, 190))
    d.arc((x0 + 30, y1 - 18, x0 + 90, y1 - 6), 200, 340,
          fill=(200, 225, 240), width=2)
    # towers, tallest centre with a pink sphere (needle tower)
    for bx, bw, bh, col in [(0.04, 0.14, 0.42, (120, 125, 135)),
                            (0.22, 0.12, 0.55, (150, 155, 165)),
                            (0.58, 0.13, 0.48, (110, 118, 130)),
                            (0.74, 0.14, 0.38, (140, 145, 155)),
                            (0.90, 0.08, 0.30, (120, 125, 135))]:
        d.rectangle((x0 + w * bx, y1 - 24 - h * bh,
                     x0 + w * (bx + bw), y1 - 24), fill=col)
    cx = x0 + int(w * 0.44)
    d.rectangle((cx - 3, y0 + 18, cx + 3, y1 - 24), fill=(140, 140, 145))
    d.ellipse((cx - 14, y0 + 44, cx + 14, y0 + 72), fill=(230, 120, 150))
    d.ellipse((cx - 10, y0 + 86, cx + 10, y0 + 106), fill=(230, 120, 150))
    # lit windows on the two main blocks
    for bx, bw in [(0.22, 0.12), (0.58, 0.13)]:
        for r in range(4):
            for c in range(2):
                wx = x0 + w * bx + 8 + c * 16
                wy = y1 - 24 - h * 0.50 + r * 14
                d.rectangle((wx, wy, wx + 9, wy + 7),
                            fill=(255, 215, 110) if (r + c) % 3 else (90, 100, 110))
    # small red flag on the tallest block
    fx = x0 + int(w * 0.28)
    d.line((fx, y1 - 24 - h * 0.55, fx, y1 - 24 - h * 0.55 - 18),
           fill=(60, 60, 60), width=2)
    d.polygon([(fx, y1 - 24 - h * 0.55 - 18), (fx + 16, y1 - 24 - h * 0.55 - 14),
               (fx, y1 - 24 - h * 0.55 - 10)], fill=(200, 40, 36))


HERO_TOP, HERO_PIC_BOT, HERO_CAP_BOT, HERO_BOT = 196, 300, 322, 416
HERO_X = [(24, 337), (356, 668), (687, 999)]

HERO_DEFS = [
    dict(key="riyadh", num=1, scene=scene_tower,
         caption="RIYADH, SAUDI ARABIA \u00b7 25 NOV",
         kicker="WAR \u00b7 MIDDLE EAST",
         title="Houthi drone hits Riyadh tower, 11 hurt",
         deck=("Second strike on the PIF Tower in five days; the "
               "coalition hits Hodeidah in reply. (Al Jazeera)"),
         pin=(46.7, 24.6, "ME", -8, 6)),
    dict(key="space", num=2, scene=scene_rocket,
         caption="JIUQUAN, CHINA \u00b7 00:18 UTC",
         kicker="SPACE \u00b7 ASIA-PACIFIC",
         title="Shenzhou-24 lifts off with Pakistan's first astronaut",
         deck=("Long March 2F launches at 00:18 UTC; Zeeshan Ali is the "
               "first foreign visitor to Tiangong. (Reuters)"),
         pin=(98.5, 39.7, "AP", 0, 0)),
    dict(key="purge", num=3, scene=scene_skyline,
         caption="SHANGHAI, CHINA \u00b7 25 NOV",
         kicker="POLITICS \u00b7 ASIA-PACIFIC",
         title="China probes Politburo member Chen Jining",
         deck=("Shanghai party chief under investigation; the fourth top "
               "leader probed since 2025. (Reuters)"),
         pin=(121.5, 31.2, "AP", 7, 5)),
]


def hero_order():
    """Variant A (riyadh lead) or B (space lead); renumber 1-3."""
    keys = ["riyadh", "space", "purge"] if LEAD != "space" \
        else ["space", "riyadh", "purge"]
    by_key = {h["key"]: h for h in HERO_DEFS}
    out = []
    for i, k in enumerate(keys, 1):
        h = dict(by_key[k])
        h["num"] = i
        out.append(h)
    return out


def draw_hero(d, hero, x0, x1):
    d.rectangle((x0, HERO_TOP, x1, HERO_BOT), fill=CARD,
                outline=INK, width=1)
    hero["scene"](d, x0 + 1, HERO_TOP + 1, x1 - 1, HERO_PIC_BOT)
    d.rectangle((x0 + 1, HERO_PIC_BOT + 1, x1 - 1, HERO_CAP_BOT),
                fill=INK)
    d.text((x0 + 10, HERO_PIC_BOT + 4), hero["caption"],
           font=f_sans(11), fill=(255, 255, 255))
    if hero["num"] == 1:
        tag = "TOP STORY"
        tw = int(f_sans_b(10).getlength(tag)) + 12
        d.rectangle((x1 - tw - 2, HERO_TOP + 2, x1 - 2, HERO_TOP + 18),
                    fill=RED)
        d.text((x1 - tw // 2 - 2, HERO_TOP + 4), tag, font=f_sans_b(10),
               fill=(255, 255, 255), anchor="ma")
    pad = 10
    d.text((x0 + pad, HERO_CAP_BOT + 6), hero["kicker"],
           font=f_sans_b(11), fill=RED)
    number_disc(d, x1 - 14, HERO_CAP_BOT + 15, 10, hero["num"])
    title_lines = wrap(hero["title"], f_sans_b(19), (x1 - x0) - 2 * pad)
    text_block(d, x0 + pad, HERO_CAP_BOT + 22, title_lines,
               f_sans_b(19), INK, 22)
    deck_lines = wrap(hero["deck"], f_sans(10), (x1 - x0) - 2 * pad)
    text_block(d, x0 + pad, HERO_BOT - 24, deck_lines,
               f_sans(10), SOFT, 12)


# ------------------------------------------------------------ card scenes

def _sky(d, x0, y0, x1, y1, col):
    d.rectangle((x0, y0, x1, y1), fill=col)


def scene_ship(d, x0, y0, x1, y1):
    """Tariffs: container ship on a blue sea."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (150, 198, 232))
    d.rectangle((x0, y0 + int(h * 0.55), x1, y1), fill=(24, 68, 110))
    d.polygon([(x0 + 14, y0 + int(h * 0.55)), (x0 + w - 10, y0 + int(h * 0.55)),
               (x0 + w - 26, y0 + int(h * 0.78)), (x0 + 30, y0 + int(h * 0.78))],
              fill=(28, 28, 32))
    for i, col in enumerate([(200, 60, 40), (60, 110, 160), (200, 160, 60)]):
        d.rectangle((x0 + 34 + i * 26, y0 + int(h * 0.28),
                     x0 + 56 + i * 26, y0 + int(h * 0.52)), fill=col)
    d.rectangle((x0 + w - 34, y0 + int(h * 0.30), x0 + w - 18,
                 y0 + int(h * 0.52)), fill=(240, 240, 235))


def scene_chip(d, x0, y0, x1, y1):
    """Huawei verdict: a chip on a dark bench."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (40, 48, 66))
    cx, cy = x0 + w // 2, y0 + h // 2
    d.rectangle((cx - 26, cy - 20, cx + 26, cy + 20), fill=(20, 20, 24),
                outline=(150, 150, 150))
    d.rectangle((cx - 14, cy - 10, cx + 14, cy + 10), fill=(60, 110, 180))
    for i in range(4):
        d.line((cx - 20 + i * 13, cy - 20, cx - 20 + i * 13, cy - 28),
               fill=(180, 180, 180), width=2)
        d.line((cx - 20 + i * 13, cy + 20, cx - 20 + i * 13, cy + 28),
               fill=(180, 180, 180), width=2)
    d.text((x0 + 6, y0 + 4), "GUILTY", font=f_sans_b(10), fill=(255, 120, 90))


def scene_shop(d, x0, y0, x1, y1):
    """Cartagena: yellow supermarket front, police tape."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (170, 205, 230))
    d.rectangle((x0 + 12, y0 + 14, x1 - 12, y1 - 12), fill=(245, 205, 60))
    d.rectangle((x0 + 20, y0 + 26, x1 - 20, y0 + 38), fill=(200, 40, 36))
    d.rectangle((x0 + 24, y0 + 44, x0 + 66, y1 - 18), fill=(150, 200, 230))
    d.rectangle((x0 + 74, y0 + 44, x1 - 24, y1 - 18), fill=(150, 200, 230))
    d.line((x0, y1 - 12, x1, y1 - 18), fill=(255, 255, 255), width=3)
    d.text((x0 + 6, y1 - 11), "POLICE", font=f_sans_b(8), fill=(20, 20, 20))


def scene_street(d, x0, y0, x1, y1):
    """Gaza street in daylight: pale blocks, ambulance."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (184, 210, 224))
    for bx, bw, bh in [(0.06, 0.20, 0.55), (0.30, 0.18, 0.68),
                       (0.52, 0.20, 0.48), (0.76, 0.18, 0.60)]:
        d.rectangle((x0 + w * bx, y1 - h * bh, x0 + w * (bx + bw), y1 - 12),
                    fill=(225, 218, 200))
    d.rectangle((x0 + 14, y1 - 26, x0 + 52, y1 - 12), fill=(255, 255, 255))
    d.rectangle((x0 + 14, y1 - 26, x0 + 52, y1 - 20), fill=(200, 40, 36))
    d.ellipse((x0 + 20, y1 - 11, x0 + 26, y1 - 5), fill=(30, 30, 30))
    d.ellipse((x0 + 40, y1 - 11, x0 + 46, y1 - 5), fill=(30, 30, 30))


def scene_satellite(d, x0, y0, x1, y1):
    """NATO space: satellite over a dark sky."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (22, 32, 58))
    for sx, sy in [(0.10, 0.18), (0.25, 0.10), (0.45, 0.22), (0.70, 0.12),
                   (0.88, 0.20), (0.60, 0.30)]:
        d.ellipse((x0 + w * sx - 2, y0 + h * sy - 2,
                   x0 + w * sx + 2, y0 + h * sy + 2), fill=(230, 230, 200))
    cx, cy = x0 + int(w * 0.50), y0 + int(h * 0.55)
    d.rectangle((cx - 22, cy - 6, cx - 6, cy + 6), fill=(60, 110, 180))
    d.rectangle((cx + 6, cy - 6, cx + 22, cy + 6), fill=(60, 110, 180))
    d.rectangle((cx - 6, cy - 10, cx + 6, cy + 10), fill=(200, 200, 200))
    d.ellipse((cx + 12, cy - 16, cx + 22, cy - 6), fill=(240, 240, 230))


def scene_chart(d, x0, y0, x1, y1):
    """Nvidia slide: red line falling on white."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (250, 250, 245))
    for i in range(3):
        d.line((x0 + 8, y0 + 14 + i * 16, x1 - 8, y0 + 14 + i * 16),
               fill=(225, 225, 220), width=1)
    pts = [(0.08, 0.25), (0.28, 0.35), (0.48, 0.30), (0.68, 0.62),
           (0.86, 0.78)]
    for (fx, fy), (tx, ty) in zip(pts, pts[1:]):
        d.line((x0 + w * fx, y0 + h * fy, x0 + w * tx, y0 + h * ty),
               fill=(200, 40, 36), width=3)
    d.text((x0 + 8, y0 + 4), "-6%", font=f_sans_b(13), fill=(200, 40, 36))


def scene_screen(d, x0, y0, x1, y1):
    """Microsoft outage: dark screen, red warning triangle."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (240, 240, 235))
    d.rectangle((x0 + 18, y0 + 8, x1 - 18, y1 - 12), fill=(30, 34, 44))
    cx, cy = x0 + w // 2, y0 + h // 2 - 4
    d.polygon([(cx, cy - 14), (cx + 14, cy + 10), (cx - 14, cy + 10)],
              fill=(255, 180, 30))
    d.text((cx, cy - 2), "!", font=f_sans_b(12), fill=(30, 30, 30),
           anchor="mm")
    d.rectangle((x0 + int(w * 0.42), y1 - 12, x0 + int(w * 0.58), y1 - 6),
                fill=(120, 120, 118))


def scene_quake(d, x0, y0, x1, y1):
    """Nepal quake: mountains, crack, shaking house."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (178, 208, 228))
    d.polygon([(x0, y1), (x0 + int(w * 0.30), y0 + 10),
               (x0 + int(w * 0.55), y1)], fill=(120, 125, 135))
    d.polygon([(x0 + int(w * 0.40), y1), (x0 + int(w * 0.68), y0 + 18),
               (x1, y1)], fill=(95, 100, 110))
    d.polygon([(x0 + int(w * 0.30) - 8, y0 + 10),
               (x0 + int(w * 0.30) + 8, y0 + 10),
               (x0 + int(w * 0.30), y0 + 24)], fill=(250, 250, 245))
    d.rectangle((x0 + int(w * 0.62), y1 - 26, x0 + int(w * 0.82), y1 - 8),
                fill=(200, 120, 60))
    d.polygon([(x0 + int(w * 0.60), y1 - 26), (x0 + int(w * 0.72), y1 - 38),
               (x0 + int(w * 0.84), y1 - 26)], fill=(160, 40, 36))
    d.line((x0 + int(w * 0.50), y1 - 8, x0 + int(w * 0.52), y1 - 22,
            x0 + int(w * 0.48), y1 - 30), fill=(60, 55, 50), width=2)


def scene_podium(d, x0, y0, x1, y1):
    """Seoul resignation: podium, flag, microphone."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (200, 215, 225))
    d.rectangle((x0 + 14, y0 + 10, x0 + 34, y0 + 34), fill=(255, 255, 255))
    d.ellipse((x0 + 19, y0 + 15, x0 + 29, y0 + 25), fill=(200, 40, 36))
    d.rectangle((x0 + int(w * 0.55), y1 - 34, x0 + int(w * 0.80), y1 - 8),
                fill=(90, 70, 60))
    d.line((x0 + int(w * 0.62), y1 - 34, x0 + int(w * 0.55), y1 - 46),
           fill=(40, 40, 40), width=2)
    d.ellipse((x0 + int(w * 0.53) - 3, y1 - 50, x0 + int(w * 0.53) + 3,
               y1 - 44), fill=(40, 40, 40))


def scene_court(d, x0, y0, x1, y1):
    """Sarkozy trial: courthouse columns."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (228, 222, 205))
    d.rectangle((x0 + 12, y0 + 8, x1 - 12, y0 + 20), fill=(180, 170, 150))
    d.polygon([(x0 + 8, y0 + 8), (x0 + w // 2, y0 - 2),
               (x1 - 8, y0 + 8)], fill=(160, 150, 130))
    for i in range(4):
        cx = x0 + 26 + i * 30
        d.rectangle((cx, y0 + 22, cx + 10, y1 - 10), fill=(210, 200, 180))
    d.rectangle((x0 + 12, y1 - 10, x1 - 12, y1 - 4), fill=(160, 150, 130))


def scene_cricket(d, x0, y0, x1, y1):
    """Suryavanshi 204: bat, ball, stumps on green."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (150, 198, 232))
    d.rectangle((x0, y1 - 18, x1, y1), fill=(86, 148, 84))
    d.rectangle((x0 + int(w * 0.30), y1 - 34, x0 + int(w * 0.34), y1 - 18),
                fill=(230, 210, 140))
    d.rectangle((x0 + int(w * 0.36), y1 - 34, x0 + int(w * 0.40), y1 - 18),
                fill=(230, 210, 140))
    d.rectangle((x0 + int(w * 0.42), y1 - 34, x0 + int(w * 0.46), y1 - 18),
                fill=(230, 210, 140))
    d.line((x0 + int(w * 0.62), y0 + 14, x0 + int(w * 0.78), y1 - 26),
           fill=(210, 170, 110), width=5)
    d.ellipse((x0 + int(w * 0.84) - 5, y0 + 12, x0 + int(w * 0.84) + 5,
               y0 + 22), fill=(200, 40, 36))


def scene_crown(d, x0, y0, x1, y1):
    """Miss Universe: gold crown on deep purple."""
    w, h = x1 - x0, y1 - y0
    _sky(d, x0, y0, x1, y1, (72, 52, 110))
    for sx, sy in [(0.12, 0.16), (0.85, 0.12), (0.70, 0.30), (0.25, 0.32)]:
        d.ellipse((x0 + w * sx - 2, y0 + h * sy - 2,
                   x0 + w * sx + 2, y0 + h * sy + 2), fill=(255, 230, 150))
    cx, cy = x0 + w // 2, y0 + h // 2 + 4
    d.polygon([(cx - 30, cy + 12), (cx - 30, cy - 8), (cx - 15, cy + 2),
               (cx, cy - 14), (cx + 15, cy + 2), (cx + 30, cy - 8),
               (cx + 30, cy + 12)], fill=(255, 205, 60))
    d.rectangle((cx - 30, cy + 12, cx + 30, cy + 18), fill=(220, 160, 40))
    for px, py in [(-15, 2), (0, -14), (15, 2)]:
        d.ellipse((cx + px - 3, cy + py - 3, cx + px + 3, cy + py + 3),
                  fill=(255, 90, 120))


CARDS = [
    dict(num=4, region="AM", tag="TARIFFS",
         head="Trump set to unveil new tariffs on 16 partners",
         place="WASHINGTON, US", scene=scene_ship),
    dict(num=5, region="TECH", tag="GUILTY",
         head="Huawei guilty of stealing trade secrets in US trial",
         place="NEW YORK, US", scene=scene_chip),
    dict(num=6, region="AM", tag="SIEGE",
         head="Gunmen hold 25 hostages in Cartagena shop",
         place="CARTAGENA, COLOMBIA", scene=scene_shop),
    dict(num=7, region="ME", tag="GAZA",
         head="Israeli strike kills Hamas security chief",
         place="GAZA", scene=scene_street),
    dict(num=8, region="EU", tag="SPACE THREAT",
         head="NATO vows space defence after nuclear satellite reports",
         place="BERLIN", scene=scene_satellite),
    dict(num=9, region="TECH", tag="SHARES -6%",
         head="Nvidia shares slide 6% as Wall Street bounce fades",
         place="SANTA CLARA, US", scene=scene_chart),
    dict(num=10, region="TECH", tag="OUTAGE",
         head="Microsoft declares \u2018Code Red\u2019 after historic outage",
         place="REDMOND, US", scene=scene_screen),
    dict(num=11, region="AP", tag="QUAKE M5.3",
         head="5.3 quake shakes Nepal; tremors felt in India",
         place="KATHMANDU", scene=scene_quake),
    dict(num=12, region="AP", tag="RESIGNS",
         head="South Korea education minister quits over exam scandal",
         place="SEOUL", scene=scene_podium),
    dict(num=13, region="EU", tag="TRIAL",
         head="Sarkozy and wife ordered to stand trial",
         place="PARIS", scene=scene_court),
    dict(num=14, region="AP", tag="204 OFF 53",
         head="Suryavanshi, 15, smashes 204 off 53 balls",
         place="DOHA", scene=scene_cricket),
    dict(num=15, region="AM", tag="75TH CROWN",
         head="Miss Universe crowns its 75th winner",
         place="SAN JUAN, PUERTO RICO", scene=scene_crown),
]
CARD_X = [24, 187, 350, 513, 676, 839]
CARD_W = 157
CARD_ROWS = [424, 552]
CARD_H = 122
PIC_H = 64


def draw_card(d, card, x0, y0):
    x1, y1 = x0 + CARD_W, y0 + CARD_H
    d.rectangle((x0, y0, x1, y1), fill=CARD, outline=INK, width=1)
    card["scene"](d, x0 + 1, y0 + 1, x1 - 1, y0 + PIC_H)
    d.rectangle((x0 + 1, y0 + PIC_H + 1, x1 - 1, y1 - 1), fill=CARD)
    tw = int(f_sans_b(9).getlength(card["tag"])) + 10
    d.rectangle((x0 + 1, y0 + 1, x0 + 1 + tw, y0 + 14), fill=RED)
    d.text((x0 + 6, y0 + 3), card["tag"], font=f_sans_b(9),
           fill=(255, 255, 255))
    lines = wrap(card["head"], f_lib_b(12), CARD_W - 16)
    text_block(d, x0 + 8, y0 + PIC_H + 6, lines, f_lib_b(12), INK, 13)
    d.text((x0 + 8, y1 - 12), card["place"],
           font=f_sans_b(9), fill=REGION[card["region"]][0])
    number_disc(d, x1 - 11, y1 - 11, 9, card["num"])


# ---------------------------------------------------------------- bottom half

MAP_BOX = (24, 706, 340, 918)
SEA_BOTTOM = 912


def _mx(lon):
    return MAP_BOX[0] + 2 + (lon + 170) / 360 * (MAP_BOX[2] - MAP_BOX[0] - 4)


def _my(lat):
    return MAP_BOX[1] + (78 - lat) / 138 * (MAP_BOX[3] - MAP_BOX[1])


# Simplified continent outlines, hand-drawn for this page.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-100, 68), (-85, 66), (-75, 62),
     (-65, 58), (-55, 52), (-60, 46), (-68, 44), (-74, 39), (-76, 35),
     (-81, 28), (-85, 30), (-90, 29), (-97, 26), (-105, 22), (-112, 27),
     (-118, 33), (-123, 40), (-124, 48), (-132, 56), (-148, 60),
     (-160, 58), (-168, 66)],
    [(-58, 62), (-45, 60), (-38, 65), (-28, 70), (-32, 74), (-48, 76),
     (-58, 72), (-58, 62)],
    [(-79, 9), (-70, 12), (-60, 8), (-52, 4), (-46, -2), (-38, -6),
     (-40, -16), (-46, -26), (-54, -33), (-62, -38), (-68, -48),
     (-72, -54), (-70, -44), (-71, -30), (-70, -18), (-76, -12),
     (-80, -4), (-79, 9)],
    [(-6, 35), (5, 37), (15, 33), (25, 32), (32, 30), (34, 26), (38, 18),
     (44, 12), (50, 11), (46, 4), (41, -4), (39, -14), (34, -24),
     (28, -32), (20, -35), (16, -30), (13, -18), (11, -4), (8, 4),
     (0, 6), (-8, 4), (-14, 10), (-17, 16), (-16, 24), (-10, 31), (-6, 35)],
    [(-10, 36), (-9, 43), (-4, 44), (-2, 48), (2, 51), (6, 54), (8, 57),
     (13, 56), (19, 55), (24, 58), (28, 62), (28, 66), (22, 70),
     (16, 69), (12, 64), (6, 60), (4, 57), (0, 54), (-3, 49), (-6, 44),
     (-10, 36)],
    [(30, 62), (40, 68), (55, 69), (70, 72), (85, 73), (100, 76),
     (115, 74), (130, 72), (145, 71), (158, 66), (160, 58), (150, 48),
     (142, 40), (137, 35), (130, 33), (126, 38), (122, 39), (119, 31),
     (114, 23), (109, 15), (105, 9), (100, 7), (96, 12), (92, 21),
     (88, 22), (83, 17), (80, 9), (76, 10), (72, 19), (67, 24), (60, 25),
     (54, 27), (50, 30), (44, 29), (39, 30), (35, 36), (30, 40), (28, 48),
     (28, 58), (30, 62)],
    [(113, -22), (116, -32), (122, -34), (130, -32), (137, -35),
     (143, -38), (149, -37), (153, -30), (150, -23), (145, -15),
     (141, -11), (134, -12), (126, -14), (119, -19), (113, -22)],
    [(130, 31), (134, 34), (138, 37), (141, 41), (143, 44), (140, 41),
     (136, 36), (132, 33), (130, 31)],
    [(95, 5), (100, 2), (105, -2), (110, -6), (116, -9), (122, -8),
     (128, -5), (128, -1), (122, -3), (114, -7), (106, -5), (100, 0),
     (95, 5)],
]

# story number -> (lon, lat, region, dx, dy). dx/dy nudge pins apart;
# check_map_layout() asserts every pair is >= 15 px apart.
CARD_PINS = [
    (4, -77.0, 38.9, "AM", -9, 7),
    (5, -74.0, 40.7, "TECH", 9, -7),
    (6, -75.5, 10.4, "AM", -6, 5),
    (7, 34.5, 31.5, "ME", 0, 0),
    (8, 13.4, 52.5, "EU", 5, -5),
    (9, -122.0, 37.3, "TECH", -7, 3),
    (10, -122.1, 47.7, "TECH", 7, -4),
    (11, 85.3, 27.7, "AP", 0, 0),
    (12, 127.0, 37.5, "AP", -7, -5),
    (13, 2.3, 48.9, "EU", -7, 6),
    (14, 51.5, 25.3, "AP", 8, -6),
    (15, -66.1, 18.5, "AM", 6, -5),
]


def all_pins(heroes):
    pins = [(h["num"],) + h["pin"] for h in heroes]
    return pins + CARD_PINS


def _pin_xy(pin):
    _num, lon, lat, _region, dx, dy = pin
    return _mx(lon) + dx, _my(lat) + dy


def check_map_layout(heroes):
    import math
    probe = ImageDraw.Draw(Image.new("RGB", (PAGE_W, PAGE_H), PAPER))
    sub = probe.textbbox((EDGE, 690), "pins match story numbers",
                         font=f_sans(9))
    gap = MAP_BOX[1] - sub[3]
    print(f"map caption ink bottom y={sub[3]}, box top y={MAP_BOX[1]}, "
          f"gap {gap}px")
    assert gap >= 2, ("map caption clipped: ink bottom "
                      f"{sub[3]} only {gap}px above box top {MAP_BOX[1]}")
    centres = {pin[0]: _pin_xy(pin) for pin in all_pins(heroes)}
    worst = (999, None, None)
    for a in centres:
        for b in centres:
            if a < b:
                dist = math.dist(centres[a], centres[b])
                if dist < worst[0]:
                    worst = (dist, a, b)
    print(f"closest pin pair: {worst[1]}-{worst[2]} at {worst[0]:.1f}px")
    assert worst[0] >= 15, (f"pins {worst[1]} and {worst[2]} only "
                            f"{worst[0]:.1f}px apart (need >= 15)")


def draw_map(d, heroes):
    x0, y0, x1, y1 = MAP_BOX
    d.rectangle((x0 + 1, y0 + 1, x1 - 1, SEA_BOTTOM), fill=SEA)
    d.rectangle((x0 + 1, SEA_BOTTOM + 1, x1 - 1, y1 - 1), fill=CARD)
    for poly in CONTINENTS:
        pts = [(_mx(lon), _my(lat)) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for pin in all_pins(heroes):
        num, _lon, _lat, region = pin[:4]
        cx, cy = _pin_xy(pin)
        col = REGION[region][0]
        d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=col,
                  outline=(255, 255, 255), width=1)
        d.text((cx, cy), str(num), font=f_sans_b(8),
               fill=(255, 255, 255), anchor="mm")
    d.rectangle((x0, y0, x1, y1), outline=INK, width=1)


LIST_ITEMS = [
    (16, "AM", "CIA says its unclassified system was breached (NYT)"),
    (17, "EU", "Real Madrid rout PSV 5-1 (Reuters)"),
    (18, "AP", "Gukesh holds Sindarov at world chess final (Hindu)"),
    (19, "AP", "Bangladesh garment strike halts ~500 factories (AP)"),
    (20, "AP", "Solomon Islands picks Australia as top partner (AP)"),
    (21, "AF", "DR Congo military plane missing, rebels claim (AP)"),
    (22, "ME", "Iranian singer gets 74 lashes after YouTube show (AP)"),
    (23, "ME", "Iraq cracks down on oil smuggling networks (Reuters)"),
    (24, "EU", "EU caps Chinese hybrid EVs (Reuters)"),
    (25, "EU", "EU budget fight puts Ukraine aid at risk (Reuters)"),
    (26, "ME", "Gaza death toll reaches 74,746, WAFA says (WAFA)"),
    (27, "WORLD", "WFP: 266m people face acute food insecurity (WFP)"),
    (28, "AM", "Fort Hood survivors barred from execution (AP)"),
    (29, "AM", "Plane crashes in Gulf of Mexico; six missing (AP)"),
    (30, "AM", "Thomas Markle charged in US court (AP)"),
    (31, "TECH", "Shein to pay $100m in FTC settlement (FTC)"),
    (32, "AM", "Radar fault delays flights into O'Hare (FAA)"),
    (33, "EU", "Sweden ends months without a government (AP)"),
    (34, "ME", "Eisenkot clinches first coalition deal (Reuters)"),
    (35, "WORLD", "Fourteen nations affirm ICJ Myanmar ruling (AP)"),
    (36, "WORLD", "TikTok tops list for online abuse of women (Report)"),
    (37, "WORLD", "UN: five women killed each hour by relatives (UN)"),
    (38, "AM", "Trump pardons Thanksgiving turkeys (AP)"),
    (39, "WORLD", "WHO chief urges US to lift Cuba oil blockade (WHO)"),
    (40, "AP", "Delhi: three held after cafe gang-rape (Hindu)"),
]


def draw_bottom_headers(d):
    d.text((EDGE, 678), "WHERE IT HAPPENED", font=f_sans_b(14), fill=INK)
    d.text((EDGE, 690), "pins match story numbers", font=f_sans(9),
           fill=SOFT)
    d.text((352, 678), "ALSO ON WEDNESDAY 25 NOVEMBER",
           font=f_sans_b(14), fill=INK)


def draw_list(d):
    num_fnt, txt_fnt = f_sans_b(11), f_sans(11)
    for i, (num, region, text) in enumerate(LIST_ITEMS):
        col = 0 if i < 13 else 1
        row = i % 13
        nx = 352 if col == 0 else 682
        tx = nx + 22
        y = 700 + row * 16
        d.text((nx, y), str(num), font=num_fnt, fill=REGION[region][0])
        d.text((tx, y), text, font=txt_fnt, fill=INK)


DATE_CHECK = [
    "Wires read up to 02:00 UTC, Wednesday 25 November 2026. Every story "
    "here happened, or was first reported, on 25 November 2026 \u2014 in "
    "any time zone worldwide.",
    "Left out \u2014 COP31 collapse (Sun 22 Nov); Hormuz tanker mine "
    "claims (23\u201324 Nov); Indonesia candy-factory fire, 24 killed "
    "(Sat 21 Nov); Amtrak derails (Sun 22 Nov); ",
    "Ukraine sinks Russian warship (Mon 23 Nov); US sanctions on Iran "
    "banks (Mon 23 Nov); Cartagena siege began Tue 24 Nov \u2014 "
    "standoff and releases are Wed 25 Nov;",
]


def draw_date_check(d):
    x0, y0, x1, y1 = EDGE, 926, RIGHT, 988
    d.rectangle((x0, y0, x1, y1), fill=CARD, outline=RED, width=2)
    d.rectangle((x0, y0, 139, y1), fill=RED)
    d.text((82, 957), "DATE CHECK", font=f_lib_b(12),
           fill=(255, 255, 255), anchor="mm")
    body_fnt = f_sans(10)
    for i, line in enumerate(DATE_CHECK):
        d.text((150, y0 + 8 + i * 18), line, font=body_fnt, fill=INK)


def draw_footer(d):
    left = ("Sources: Reuters, AP, BBC, Al Jazeera, Xinhua, The Hindu, "
            "NYT, WAFA, WFP, FTC \u2014 25 Nov 2026")
    right = ("THE WORLD IN ONE DAY \u2014 WEDNESDAY 25 NOVEMBER 2026 "
             "\u00b7 ONE PAGE")
    for size in (11, 10, 9):
        if (f_sans(size).getlength(left)
                + f_sans_b(size).getlength(right) + 16 <= RIGHT - EDGE):
            break
    d.text((EDGE, 996), left, font=f_sans(size), fill=INK)
    d.text((RIGHT, 996), right, font=f_sans_b(size), fill=INK,
           anchor="ra")


# ---------------------------------------------------------------- assembly

def build():
    heroes = hero_order()
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_headline(d)
    draw_numbers(d)
    draw_region_bar(d)
    for hero, (x0, x1) in zip(heroes, HERO_X):
        draw_hero(d, hero, x0, x1)
    for i, card in enumerate(CARDS):
        draw_card(d, card, CARD_X[i % 6], CARD_ROWS[i // 6])
    draw_bottom_headers(d)
    draw_map(d, heroes)
    draw_list(d)
    draw_date_check(d)
    draw_footer(d)
    return img


def report_layout(heroes):
    for hero in heroes:
        t = wrap(hero["title"], f_sans_b(19), 313 - 20)
        dk = wrap(hero["deck"], f_sans(10), 313 - 20)
        print(f"hero {hero['num']} ({hero['key']}): title {len(t)} lines, "
              f"deck {len(dk)} lines")
    for card in CARDS:
        lines = wrap(card["head"], f_lib_b(12), CARD_W - 16)
        print(f"card {card['num']}: headline {len(lines)} lines, "
              f"place {f_sans_b(9).getlength(card['place']):.0f}px")
    for i, line in enumerate(DATE_CHECK, 1):
        print(f"datecheck L{i}: {f_sans(10).getlength(line):.1f}px")
    for num, _reg, text in LIST_ITEMS:
        w = f_sans(11).getlength(text)
        flag = "  <-- TOO LONG" if w > 300 else ""
        print(f"list {num}: {w:.1f}px{flag}")


if __name__ == "__main__":
    heroes = hero_order()
    report_layout(heroes)
    check_map_layout(heroes)
    page = build()
    page.save(OUT)
    print("saved", OUT, page.size, OUT.stat().st_size, "bytes",
          "lead =", LEAD)
