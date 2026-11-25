#!/usr/bin/env python3
"""Draw the 25 November 2026 front page and save it as entry.png.

A flat newspaper front page, 1024 by 1024, built with Pillow only.
Everything on the page is drawn here: masthead, lead story with a
small sea-scene illustration, six story boxes and an also-today strip.
The file this writes is the image the entry ships; main.py never
redraws it, it only hands out an exact copy.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 28

PAPER = (246, 241, 230)
INK = (26, 26, 26)
NAVY = (20, 38, 63)
GOLD = (200, 147, 42)
RED = (164, 31, 31)
TEAL = (21, 94, 99)
GREY = (90, 90, 90)
RULE = (180, 170, 150)
SKY = (188, 214, 230)
SEA = (28, 77, 107)
ORANGE = (232, 116, 30)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width, word by word."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def para(draw, xy, text, fnt, width, fill=INK, spacing=5):
    """Draw wrapped text, return the y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def headline(draw, xy, text, fnt, width, fill=INK, spacing=3):
    return para(draw, xy, text, fnt, width, fill=fill, spacing=spacing)


def sea_scene(draw, x0, y0, x1, y1):
    """Flat drawing: a cargo ship ablaze at sea, a drone overhead."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # sun
    draw.ellipse([x1 - 72, y0 + 14, x1 - 28, y0 + 58], fill=(240, 196, 90))
    # sea
    horizon = y0 + (y1 - y0) * 2 // 5
    draw.rectangle([x0, horizon, x1, y1], fill=SEA)
    # wave crests
    for wx in range(x0 + 8, x1 - 20, 46):
        draw.arc([wx, y1 - 46, wx + 34, y1 - 18], 180, 360, fill=(220, 235, 242), width=3)
    for wx in range(x0 + 26, x1 - 20, 52):
        draw.arc([wx, horizon + 26, wx + 34, horizon + 48], 180, 360, fill=(160, 195, 212), width=3)
    # hull
    hx0, hx1 = x0 + 26, x1 - 60
    hy = y1 - 96
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 22, hy + 42), (hx0 + 16, hy + 42)], fill=(58, 58, 58))
    draw.rectangle([hx0 + 6, hy - 34, hx0 + 108, hy], fill=(120, 40, 36))
    draw.rectangle([hx0 + 116, hy - 26, hx0 + 168, hy], fill=(60, 90, 110))
    draw.rectangle([hx0 + 176, hy - 18, hx0 + 214, hy], fill=(120, 40, 36))
    # funnel + mast
    draw.rectangle([hx0 + 130, hy - 58, hx0 + 150, hy - 26], fill=(40, 40, 40))
    draw.line([hx0 + 196, hy - 18, hx0 + 196, hy - 66], fill=(40, 40, 40), width=4)
    # blast at the bow
    bx, by = hx1 - 8, hy - 26
    spikes = [(0, -34), (12, -12), (34, -20), (18, 2), (32, 18),
              (8, 14), (0, 36), (-10, 12), (-32, 20), (-18, 0),
              (-34, -16), (-12, -12)]
    draw.polygon([(bx + dx, by + dy) for dx, dy in spikes], fill=ORANGE)
    draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(250, 210, 90))
    # drone
    dx, dy = x1 - 96, y0 + 78
    draw.line([dx - 22, dy - 10, dx + 22, dy + 10], fill=(30, 30, 30), width=3)
    draw.line([dx - 22, dy + 10, dx + 22, dy - 10], fill=(30, 30, 30), width=3)
    draw.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=(30, 30, 30))
    for cx, cy in [(dx - 22, dy - 10), (dx + 22, dy + 10),
                   (dx - 22, dy + 10), (dx + 22, dy - 10)]:
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=(30, 30, 30), width=2)


def story_box(draw, x0, y0, x1, y1, kicker, kcolor, title, body, body_size=16):
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=2)
    draw.rectangle([x0, y0, x1, y0 + 30], fill=kcolor)
    draw.text((x0 + 12, y0 + 6), kicker, font=font(SANS_B, 16), fill=(255, 255, 255))
    headline(draw, (x0 + 12, y0 + 42), title, font(SERIF_B, 22),
             x1 - x0 - 24)
    para(draw, (x0 + 12, y0 + 118), body, font(SANS, body_size),
         x1 - x0 - 24, spacing=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 132], fill=NAVY)
    d.text((MARGIN, 18), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 56), fill=(250, 246, 236))
    d.text((MARGIN, 92), "WEDNESDAY, 25 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE PAGE",
           font=font(SANS_B, 21), fill=GOLD)
    d.line([0, 132, W, 132], fill=GOLD, width=4)

    # ---- lead story ----
    lx, lw = MARGIN, 612
    d.text((lx, 150), "UKRAINE'S WAR AT SEA", font=font(SANS_B, 19), fill=RED)
    headline(d, (lx, 178),
             "Zelenskyy: we hit the Sparta II — and sank a Russian warship off Libya",
             font(SERIF_B, 30), lw)
    para(d, (lx, 292),
         "Ukraine's president confirms Kyiv's drone strike on the Russian "
         "cargo ship Sparta II in the Gulf of Finland on Saturday, calling "
         "the weapons-carrying vessel a legitimate target: \u201cWe did "
         "everything right.\u201d Kyiv also says it sank a Russian warship "
         "in Benghazi harbour. Norway, a staunch ally, urges caution — and "
         "Putin warns retaliation is inevitable as Ukraine keeps hitting "
         "Russian oil refineries.",
         font(SANS, 17), lw, spacing=5)
    sea_scene(d, 668, 150, 996, 400)
    d.text((668, 406), "The Sparta II, ablaze in the Gulf of Finland.",
           font=font(SANS, 14), fill=GREY)

    d.line([MARGIN, 436, W - MARGIN, 436], fill=RULE, width=2)

    # ---- first row of stories ----
    row1 = [
        ("TECH TRIAL", NAVY,
         "Huawei convicted in US trial over Iran business",
         "A US jury finds China's Huawei guilty of trade-secrets "
         "conspiracy and fraud over its Iran business — acquitting it of "
         "racketeering — in a sprawling criminal trial."),
        ("MIDDLE EAST", RED,
         "Houthis hit Riyadh's tallest tower; 11 wounded",
         "Saudi civil defence says a Houthi strike hit Riyadh's tallest "
         "tower, wounding 11. The Houthis have pushed to within 60 km of "
         "Aden, but Yemeni forces say they will not take the city."),
        ("FRANCE", TEAL,
         "Sarkozy and Bruni ordered to trial in Libya case",
         "French officials order former president Nicolas Sarkozy and his "
         "wife Carla Bruni to trial over the Libya corruption case, with a "
         "first pre-trial hearing set for 1 April 2027."),
    ]
    xs = [MARGIN, 356, 680]
    for (kicker, kc, title, body), x0 in zip(row1, xs):
        story_box(d, x0, 452, x0 + 316, 696, kicker, kc, title, body)

    # ---- second row of stories ----
    row2 = [
        ("UKRAINE", RED,
         "Kyiv rescuers pull 11 dead from rubble",
         "Rescuers pull 11 dead from a Kyiv apartment block hit by "
         "drones. Leaked Russian records put the war dead at 720,000."),
        ("MARKETS", NAVY,
         "Nvidia roars back 31.5% as Huang returns",
         "Nvidia gains nearly $1 trillion in a day; shares close 31.5% "
         "higher. Huang, back as CEO, recoups nearly $34 billion."),
        ("DISASTER", TEAL,
         "Five die in Turkish crash; 175 migrants missing",
         "Turkish helicopter crashes on a training flight, killing "
         "five. 175 migrants missing after a boat from Senegal vanishes."),
    ]
    for (kicker, kc, title, body), x0 in zip(row2, xs):
        story_box(d, x0, 712, x0 + 316, 916, kicker, kc, title, body,
                  body_size=15)

    # ---- also-today strip ----
    d.rectangle([0, 926, W, 1004], fill=NAVY)
    d.text((MARGIN, 932), "ALSO TODAY", font=font(SANS_B, 17), fill=GOLD)
    para(d, (MARGIN, 954),
         "DR Congo rebels pull back from Bunia  •  England beat Australia "
         "by 8 wickets in the 2nd T20I  •  Real Madrid sink PSV 5–1  •  "
         "Trump spares turkeys Freedom and Feathers  •  Fort Hood gunman "
         "seeks a stay  •  Iran rations electricity  •  Iraq moves on "
         "Kurdish oilfields  •  NATO jets for Poland  •  Colombia car "
         "bomb injures 23",
         font(SANS, 13), W - 2 * MARGIN, fill=(232, 228, 218), spacing=3)

    d.text((MARGIN, 1008),
           "All stories reported Wednesday 25 November 2026  •  Reuters  •  RFE/RL  •  Bloomberg  •  WireMinute",
           font=font(SANS, 13), fill=GREY)
    return img


if __name__ == "__main__":
    page = build()
    page.save("entry.png", optimize=True)
    print("wrote entry.png", page.size)
