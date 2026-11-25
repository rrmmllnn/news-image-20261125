#!/usr/bin/env python3
"""Render the round-3 news poster for 25 November 2026.

Layout: a 24-hour news wire. A navy masthead names the day, three large
drawn panels lead with the day's biggest stories, and below them a two-column
wire lists the rest of the day in order. Everything is drawn with Pillow from
fixed coordinates, so the output is byte-identical on every run.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (25, 25, 35)
NAVY = (20, 38, 63)
NAVY_SOFT = (38, 62, 96)
RED = (179, 38, 30)
TEAL = (14, 107, 107)
GOLD = (176, 124, 18)
MUTED = (90, 90, 102)
WHITE = (255, 255, 255)
PANEL = (255, 255, 255)
RULE = (196, 188, 172)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)     # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)            # noqa: E731


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- scenes
def scene_tanker(d, x, y, w, h):
    """Burning tanker in a strait at dusk."""
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 74))
    d.ellipse([x + w - 52, y + 10, x + w - 18, y + 44], fill=(232, 214, 160))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(39, 75, 99))
    for i in range(5):
        wx = x + 12 + i * 62
        d.arc([wx, y + h - 26, wx + 44, y + h - 8], 180, 360, fill=(255, 255, 255))
    # hull
    d.rectangle([x + 28, y + h * 0.58, x + w - 28, y + h * 0.80], fill=(32, 32, 40))
    d.rectangle([x + 28, y + h * 0.58, x + w - 28, y + h * 0.63], fill=(179, 38, 30))
    # containers
    for i, c in enumerate([(196, 90, 30), (38, 110, 140), (176, 124, 18)]):
        cx = x + 48 + i * 62
        d.rectangle([cx, y + h * 0.40, cx + 54, y + h * 0.58], fill=c)
    # bridge
    d.rectangle([x + w - 78, y + h * 0.34, x + w - 44, y + h * 0.58], fill=(240, 240, 235))
    # flames above the deck
    d.polygon([(x + 96, y + h * 0.58), (x + 116, y + h * 0.18),
               (x + 138, y + h * 0.58)], fill=(232, 110, 20))
    d.polygon([(x + 150, y + h * 0.58), (x + 168, y + h * 0.30),
               (x + 186, y + h * 0.58)], fill=(240, 180, 40))
    d.polygon([(x + 196, y + h * 0.58), (x + 212, y + h * 0.22),
               (x + 228, y + h * 0.58)], fill=(232, 110, 20))
    # smoke
    for cx, cy, r in [(120, 26, 12), (150, 14, 15), (186, 24, 11), (214, 12, 13)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(120, 120, 128))


def scene_market(d, x, y, w, h):
    """A market board: the line falls off a cliff."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for gy in range(4):
        yy = y + 18 + gy * 26
        d.line([x + 12, yy, x + w - 12, yy], fill=(228, 228, 228))
    # falling line with an arrowhead
    pts = [(x + 16, y + 22), (x + 70, y + 30), (x + 120, y + 26),
           (x + 168, y + 52), (x + 214, y + 66), (x + 258, y + 96),
           (x + w - 16, y + h - 18)]
    d.line(pts, fill=(179, 38, 30), width=5, joint="curve")
    d.polygon([(x + w - 16, y + h - 18), (x + w - 34, y + h - 30),
               (x + w - 30, y + h - 10)], fill=(179, 38, 30))
    # red bars sinking
    for i, bh in enumerate([66, 52, 40, 26]):
        bx = x + 30 + i * 64
        d.rectangle([bx, y + h - 12 - bh, bx + 34, y + h - 12],
                    fill=(196, 60, 48))
    d.text((x + 14, y + 6), "KOSPI", font=F_SANS_B(13), fill=(90, 90, 102))
    d.text((x + w - 118, y + 8), "-6.16%", font=F_SANS_B(30), fill=(179, 38, 30))


def scene_rocket(d, x, y, w, h):
    """A crew rocket climbing into a starry sky."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    stars = [(30, 18), (70, 44), (120, 14), (170, 38), (220, 16),
             (262, 48), (52, 84), (250, 84), (140, 70), (200, 96)]
    for sx, sy in stars:
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                  fill=(255, 255, 255))
    # ground
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(60, 58, 66))
    # flame
    cx = x + w // 2
    d.polygon([(cx - 12, y + 74), (cx, y + 118), (cx + 12, y + 74)],
              fill=(240, 140, 20))
    d.polygon([(cx - 6, y + 74), (cx, y + 100), (cx + 6, y + 74)],
              fill=(250, 210, 80))
    # body
    d.rounded_rectangle([cx - 16, y + 12, cx + 16, y + 76], radius=14,
                        fill=(240, 240, 235))
    d.polygon([(cx - 16, y + 22), (cx, y + 2), (cx + 16, y + 22)],
              fill=(179, 38, 30))
    d.polygon([(cx - 16, y + 56), (cx - 32, y + 78), (cx - 16, y + 76)],
              fill=(179, 38, 30))
    d.polygon([(cx + 16, y + 56), (cx + 32, y + 78), (cx + 16, y + 76)],
              fill=(179, 38, 30))
    d.ellipse([cx - 7, y + 30, cx + 7, y + 44], fill=(38, 62, 96))
    # smoke puffs
    for sx, sy, r in [(cx - 46, y + h - 30, 12), (cx + 44, y + h - 26, 14),
                      (cx - 24, y + h - 22, 10), (cx + 22, y + h - 20, 9)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 150, 158))


# ---------------------------------------------------------------- content
LEADS = [
    ("MIDDLE EAST", RED, scene_tanker,
     "Tankers burn in the Strait of Hormuz",
     "Iran says tankers struck mines and caught fire; Tehran says their "
     "route was unauthorised."),
    ("EAST ASIA", TEAL, scene_market,
     "Asia's chip shares plunge",
     "Seoul's Kospi falls 6.16% \u2014 Samsung \u22129.9%, SK Hynix \u221211.1% "
     "\u2014 as the AI rally unwinds."),
    ("SPACE", NAVY_SOFT, scene_rocket,
     "Pakistan reaches orbit",
     "Shenzhou-24 lifts off at 00:18 GMT; Muhammad Zeeshan Ali, 40, is the "
     "first Pakistani in space."),
]

# (region, colour, headline) -- every headline is dated 25 November 2026.
WIRE = [
    ("EAST ASIA", TEAL,
     "Shenzhou-24 docks with Tiangong at 03:56 GMT, three and a half hours "
     "after lift-off."),
    ("EAST ASIA", TEAL,
     "Tang Hongbo boards Tiangong for a third time, a first for any "
     "astronaut."),
    ("EAST ASIA", TEAL,
     "Taiwan's Taiex slides about 5% as the chip sell-off spreads across "
     "Asia."),
    ("EAST ASIA", TEAL,
     "SoftBank tumbles 14.8% in Tokyo, leading Japanese shares lower."),
    ("PACIFIC", (31, 111, 178),
     "Australia and Solomon Islands sign a treaty in Canberra barring "
     "foreign bases on the islands."),
    ("EUROPE", (46, 94, 140),
     "Ukrainian drones set two Rosneft refineries ablaze in Samara; one "
     "person is killed."),
    ("EUROPE", (46, 94, 140),
     "A Russian strike on Odesa kills two and injures three, including a "
     "child."),
    ("EUROPE", (46, 94, 140),
     "Kyiv reports a fire in a tower block after overnight strikes; two "
     "people are hurt."),
    ("MIDDLE EAST", RED,
     "Houthis say they struck Saudi Arabia's Ras Tanura refinery; fires are "
     "reported."),
    ("NORTH AMERICA", (138, 90, 0),
     "Washington proposes new tariffs on 14 partners at 20\u201340%; nothing "
     "before a 25 January hearing."),
    ("EUROPE", (46, 94, 140),
     "Zelensky says Ukraine needs \u20ac115bn in foreign aid for 2027."),
    ("EUROPE", (46, 94, 140),
     "Poland presses for a permanent US troop presence after two airspace "
     "incursions in four days."),
    ("EUROPE", (46, 94, 140),
     "Eurozone inflation rises to 4.0%, Eurostat reports."),
    ("PACIFIC", (31, 111, 178),
     "Australian inflation climbs to 4.9%, driven by fuel prices."),
    ("MIDDLE EAST", RED,
     "Israel kills Hamas colonel Mohammad Abuelouf in Gaza; his wife and two "
     "children also die."),
    ("AFRICA", (62, 122, 58),
     "Sudanese paramilitary drone strikes kill 19 civilians and wound 20 in "
     "two cities."),
    ("LATIN AMERICA", (194, 94, 0),
     "Colombian troops free every hostage in a Cartagena supermarket siege; "
     "one captor is killed."),
    ("EUROPE", (46, 94, 140),
     "Pope Leo XIV speaks out over the COP31 talks' failure to reach a "
     "deal."),
    ("WORLD", MUTED,
     "The UN warns funding cuts put decades of progress against HIV at "
     "risk."),
    ("EUROPE", (46, 94, 140),
     "Kyiv says its drones sank a Russian warship off the Libyan coast."),
    ("NORTH AMERICA", (138, 90, 0),
     "Kilmar Abrego Garcia leaves the US for Spain after a 20-month legal "
     "fight."),
    ("NORTH AMERICA", (138, 90, 0),
     "The US Army destroys about five tons of degraded explosive in a "
     "controlled Iowa blast."),
    ("AFRICA", (62, 122, 58),
     "Senegal are restored as Africa Cup of Nations champions by sport's "
     "highest court."),
]


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- masthead
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.rectangle([0, 100, W, 104], fill=GOLD)
    d.text((24, 14), "THE DAY IN 24 HOURS", font=F_SERIF_B(42), fill=WHITE)
    d.text((24, 66), "One day of world news, hour by hour",
           font=F_SANS(15), fill=(200, 208, 222))
    d.text((1000, 12), "WEDNESDAY", font=F_SANS_B(16),
           fill=(200, 208, 222), anchor="ra")
    d.text((1000, 34), "25 NOVEMBER 2026", font=F_SANS_B(30),
           fill=WHITE, anchor="ra")
    d.text((1000, 70), "26 stories \u00b7 8 regions \u00b7 all times UTC",
           font=F_SANS(13), fill=(200, 208, 222), anchor="ra")

    # ---------------------------------------------------------- lead panels
    px = [24, 352, 680]
    for i, (region, colour, scene, head, detail) in enumerate(LEADS):
        x = px[i]
        d.rectangle([x, 116, x + 320, 336], fill=PANEL, outline=RULE, width=1)
        d.rectangle([x, 116, x + 320, 122], fill=colour)
        d.text((x + 12, 128), region, font=F_SANS_B(12), fill=colour)
        scene(d, x + 12, 148, 296, 108)
        lines = wrap(d, head, F_SANS_B(16), 296)
        text_block(d, (x + 12, 262), lines[:2], F_SANS_B(16), INK, 19)
        dlines = wrap(d, detail, F_SANS(12), 296)
        text_block(d, (x + 12, 262 + len(lines[:2]) * 19 + 4),
                   dlines[:2], F_SANS(12), MUTED, 14)

    # ---------------------------------------------------------- wire header
    d.text((24, 348), "THE WIRE", font=F_SANS_B(17), fill=NAVY)
    d.text((150, 351),
           "the rest of the day, in order \u2014 every story dated 25 November 2026",
           font=F_SANS(13), fill=MUTED)
    d.line([24, 374, 1000, 374], fill=RULE, width=1)

    # ---------------------------------------------------------- wire columns
    col_x = [24, 528]
    col_w = 472
    rows = 12
    top, bottom = 382, 920
    row_h = (bottom - top) / rows
    left = WIRE[:12]
    right = WIRE[12:]
    d.line([512, top, 512, bottom], fill=RULE, width=1)
    for col, stories in enumerate((left, right)):
        for r, (region, colour, head) in enumerate(stories):
            x = col_x[col]
            y = top + r * row_h
            d.text((x, y), region, font=F_SANS_B(11), fill=colour)
            lines = wrap(d, head, F_SANS(13), col_w)
            text_block(d, (x, y + 13), lines[:2], F_SANS(13), INK, 15)

    # date-check box in the spare cell of the right column
    bx, by = col_x[1], top + 11 * row_h
    d.rounded_rectangle([bx, by + 2, bx + col_w, by + row_h - 4], radius=6,
                        outline=NAVY_SOFT, width=1, fill=(232, 238, 246))
    d.text((bx + 10, by + 6), "DATE CHECK", font=F_SANS_B(11),
           fill=NAVY_SOFT)
    d.text((bx + 10, by + 22),
           "Every story is dated Wednesday 25 November 2026.",
           font=F_SANS(12), fill=INK)

    # ---------------------------------------------------------- footer
    d.line([24, 932, 1000, 932], fill=RULE, width=1)
    numbers = ("KOSPI \u22126.16%  \u00b7  NIKKEI \u22122.78%  \u00b7  "
               "SOFTBANK \u221214.8%  \u00b7  \u20ac115BN AID ASK  \u00b7  "
               "14 TARIFF PARTNERS  \u00b7  5 TONS DESTROYED")
    nsize = 14
    while d.textlength(numbers, font=F_SANS_B(nsize)) > 960 and nsize > 10:
        nsize -= 1
    d.text((512, 944), numbers, font=F_SANS_B(nsize), fill=NAVY, anchor="ma")
    d.text((512, 970),
           "Sources: Reuters \u00b7 AP \u00b7 Nature \u00b7 Just Security "
           "\u00b7 Xinhua \u00b7 Eurostat",
           font=F_SANS(12), fill=MUTED, anchor="ma")
    d.text((512, 992),
           "Drawn and checked 26 November 2026 \u00b7 All events of "
           "Wednesday 25 November 2026",
           font=F_SANS(11), fill=MUTED, anchor="ma")
    return img


if __name__ == "__main__":
    render().save("entry.png", optimize=True)
    print("wrote entry.png")
