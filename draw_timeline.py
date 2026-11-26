#!/usr/bin/env python3
"""Draw the round-3 poster: one day of world news as a 24-hour wire.

A navy masthead names the day, three big hand-drawn panels carry the
largest stories, and a two-column wire underneath lists the rest of the
day in order. All geometry is fixed and every picture is painted with
Pillow, so repeated runs produce byte-identical PNG output.
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


def load_font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


_FONT_FILES = {
    "serif_bold": "DejaVuSerif-Bold.ttf",
    "sans_bold": "DejaVuSans-Bold.ttf",
    "sans": "DejaVuSans.ttf",
}


def _font_factory(kind):
    def make(size):
        return load_font(_FONT_FILES[kind], size)
    return make


serif_bold = _font_factory("serif_bold")
sans_bold = _font_factory("sans_bold")
sans = _font_factory("sans")


def wrap_text(draw, text, fnt, width):
    """Split text into lines that fit `width`, measured with the real font."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text_lines(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- scenes
def paint_tanker(d, x, y, w, h):
    """A tanker on fire in a strait at dusk."""
    d.rectangle([x, y, x + w, y + h], fill=(27, 42, 74))
    d.ellipse([x + w - 52, y + 10, x + w - 18, y + 44], fill=(232, 214, 160))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(39, 75, 99))
    for k in range(5):
        wave_x = x + 12 + k * 62
        d.arc([wave_x, y + h - 26, wave_x + 44, y + h - 8], 180, 360,
              fill=(255, 255, 255))
    # the hull, with its red waterline stripe
    d.rectangle([x + 28, y + h * 0.58, x + w - 28, y + h * 0.80], fill=(32, 32, 40))
    d.rectangle([x + 28, y + h * 0.58, x + w - 28, y + h * 0.63], fill=(179, 38, 30))
    # stacked containers on deck
    for slot, shade in enumerate([(196, 90, 30), (38, 110, 140), (176, 124, 18)]):
        box_x = x + 48 + slot * 62
        d.rectangle([box_x, y + h * 0.40, box_x + 54, y + h * 0.58], fill=shade)
    # the bridge tower
    d.rectangle([x + w - 78, y + h * 0.34, x + w - 44, y + h * 0.58], fill=(240, 240, 235))
    # flames rising above the deck
    d.polygon([(x + 96, y + h * 0.58), (x + 116, y + h * 0.18),
               (x + 138, y + h * 0.58)], fill=(232, 110, 20))
    d.polygon([(x + 150, y + h * 0.58), (x + 168, y + h * 0.30),
               (x + 186, y + h * 0.58)], fill=(240, 180, 40))
    d.polygon([(x + 196, y + h * 0.58), (x + 212, y + h * 0.22),
               (x + 228, y + h * 0.58)], fill=(232, 110, 20))
    # drifting smoke
    for puff_x, puff_y, puff_r in [(120, 26, 12), (150, 14, 15), (186, 24, 11), (214, 12, 13)]:
        d.ellipse([x + puff_x - puff_r, y + puff_y - puff_r,
                   x + puff_x + puff_r, y + puff_y + puff_r],
                  fill=(120, 120, 128))


def paint_market(d, x, y, w, h):
    """A market board where the line falls off a cliff."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for row in range(4):
        grid_y = y + 18 + row * 26
        d.line([x + 12, grid_y, x + w - 12, grid_y], fill=(228, 228, 228))
    # the falling line, with an arrowhead at its end
    path = [(x + 16, y + 22), (x + 70, y + 30), (x + 120, y + 26),
            (x + 168, y + 52), (x + 214, y + 66), (x + 258, y + 96),
            (x + w - 16, y + h - 18)]
    d.line(path, fill=(179, 38, 30), width=5, joint="curve")
    d.polygon([(x + w - 16, y + h - 18), (x + w - 34, y + h - 30),
               (x + w - 30, y + h - 10)], fill=(179, 38, 30))
    # red bars sinking toward the bottom
    for slot, bar_h in enumerate([66, 52, 40, 26]):
        bar_x = x + 30 + slot * 64
        d.rectangle([bar_x, y + h - 12 - bar_h, bar_x + 34, y + h - 12],
                    fill=(196, 60, 48))
    d.text((x + 14, y + 6), "KOSPI", font=sans_bold(13), fill=(90, 90, 102))
    d.text((x + w - 118, y + 8), "-6.16%", font=sans_bold(30), fill=(179, 38, 30))


def paint_rocket(d, x, y, w, h):
    """A crewed rocket climbing away into a starry sky."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    stars = [(30, 18), (70, 44), (120, 14), (170, 38), (220, 16),
             (262, 48), (52, 84), (250, 84), (140, 70), (200, 96)]
    for star_x, star_y in stars:
        d.ellipse([x + star_x - 2, y + star_y - 2, x + star_x + 2, y + star_y + 2],
                  fill=(255, 255, 255))
    # the launch pad ground
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(60, 58, 66))
    # the exhaust flame
    centre = x + w // 2
    d.polygon([(centre - 12, y + 74), (centre, y + 118), (centre + 12, y + 74)],
              fill=(240, 140, 20))
    d.polygon([(centre - 6, y + 74), (centre, y + 100), (centre + 6, y + 74)],
              fill=(250, 210, 80))
    # the rocket body
    d.rounded_rectangle([centre - 16, y + 12, centre + 16, y + 76], radius=14,
                        fill=(240, 240, 235))
    d.polygon([(centre - 16, y + 22), (centre, y + 2), (centre + 16, y + 22)],
              fill=(179, 38, 30))
    d.polygon([(centre - 16, y + 56), (centre - 32, y + 78), (centre - 16, y + 76)],
              fill=(179, 38, 30))
    d.polygon([(centre + 16, y + 56), (centre + 32, y + 78), (centre + 16, y + 76)],
              fill=(179, 38, 30))
    d.ellipse([centre - 7, y + 30, centre + 7, y + 44], fill=(38, 62, 96))
    # smoke puffs around the pad
    for puff_x, puff_y, puff_r in [(centre - 46, y + h - 30, 12), (centre + 44, y + h - 26, 14),
                      (centre - 24, y + h - 22, 10), (centre + 22, y + h - 20, 9)]:
        d.ellipse([puff_x - puff_r, puff_y - puff_r, puff_x + puff_r, puff_y + puff_r], fill=(150, 150, 158))


# ---------------------------------------------------------------- content
LEADS = [
    ("MIDDLE EAST", RED, paint_tanker,
     "Tankers burn in the Strait of Hormuz",
     "Iran says tankers struck mines and caught fire; Tehran says their "
     "route was unauthorised."),
    ("EAST ASIA", TEAL, paint_market,
     "Asia's chip shares plunge",
     "Seoul's Kospi falls 6.16% \u2014 Samsung \u22129.9%, SK Hynix \u221211.1% "
     "\u2014 as the AI rally unwinds."),
    ("SPACE", NAVY_SOFT, paint_rocket,
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
    d.text((24, 14), "THE DAY IN 24 HOURS", font=serif_bold(42), fill=WHITE)
    d.text((24, 66), "One day of world news, hour by hour",
           font=sans(15), fill=(200, 208, 222))
    d.text((1000, 12), "WEDNESDAY", font=sans_bold(16),
           fill=(200, 208, 222), anchor="ra")
    d.text((1000, 34), "25 NOVEMBER 2026", font=sans_bold(30),
           fill=WHITE, anchor="ra")
    d.text((1000, 70), "26 stories \u00b7 8 regions \u00b7 all times UTC",
           font=sans(13), fill=(200, 208, 222), anchor="ra")

    # ---------------------------------------------------------- lead panels
    panel_x = [24, 352, 680]
    for slot, (region, colour, scene, head, detail) in enumerate(LEADS):
        x = panel_x[slot]
        d.rectangle([x, 116, x + 320, 336], fill=PANEL, outline=RULE, width=1)
        d.rectangle([x, 116, x + 320, 122], fill=colour)
        d.text((x + 12, 128), region, font=sans_bold(12), fill=colour)
        scene(d, x + 12, 148, 296, 108)
        head_lines = wrap_text(d, head, sans_bold(16), 296)
        draw_text_lines(d, (x + 12, 262), head_lines[:2], sans_bold(16), INK, 19)
        detail_lines = wrap_text(d, detail, sans(12), 296)
        draw_text_lines(d, (x + 12, 262 + len(head_lines[:2]) * 19 + 4),
                        detail_lines[:2], sans(12), MUTED, 14)

    # ---------------------------------------------------------- wire header
    d.text((24, 348), "THE WIRE", font=sans_bold(17), fill=NAVY)
    d.text((150, 351),
           "the rest of the day, in order \u2014 every story dated 25 November 2026",
           font=sans(13), fill=MUTED)
    d.line([24, 374, 1000, 374], fill=RULE, width=1)

    # ---------------------------------------------------------- wire columns
    column_x = [24, 528]
    column_w = 472
    row_count = 12
    wire_top, wire_bottom = 382, 920
    row_height = (wire_bottom - wire_top) / row_count
    left_col = WIRE[:12]
    right_col = WIRE[12:]
    d.line([512, wire_top, 512, wire_bottom], fill=RULE, width=1)
    for x, stories in zip(column_x, (left_col, right_col)):
        for row, (region, colour, head) in enumerate(stories):
            y = wire_top + row * row_height
            d.text((x, y), region, font=sans_bold(11), fill=colour)
            lines = wrap_text(d, head, sans(13), column_w)
            draw_text_lines(d, (x, y + 13), lines[:2], sans(13), INK, 15)

    # date-check box in the spare cell of the right column
    box_x, box_y = column_x[1], wire_top + 11 * row_height
    d.rounded_rectangle([box_x, box_y + 2, box_x + column_w, box_y + row_height - 4], radius=6,
                        outline=NAVY_SOFT, width=1, fill=(232, 238, 246))
    d.text((box_x + 10, box_y + 6), "DATE CHECK", font=sans_bold(11),
           fill=NAVY_SOFT)
    d.text((box_x + 10, box_y + 22),
           "Every story is dated Wednesday 25 November 2026.",
           font=sans(12), fill=INK)

    # ---------------------------------------------------------- footer
    d.line([24, 932, 1000, 932], fill=RULE, width=1)
    ticker = ("KOSPI \u22126.16%  \u00b7  NIKKEI \u22122.78%  \u00b7  "
              "SOFTBANK \u221214.8%  \u00b7  \u20ac115BN AID ASK  \u00b7  "
              "14 TARIFF PARTNERS  \u00b7  5 TONS DESTROYED")
    ticker_size = 14
    while d.textlength(ticker, font=sans_bold(ticker_size)) > 960 and ticker_size > 10:
        ticker_size -= 1
    d.text((512, 944), ticker, font=sans_bold(ticker_size), fill=NAVY, anchor="ma")
    d.text((512, 970),
           "Sources: Reuters \u00b7 AP \u00b7 Nature \u00b7 Just Security "
           "\u00b7 Xinhua \u00b7 Eurostat",
           font=sans(12), fill=MUTED, anchor="ma")
    d.text((512, 992),
           "Drawn and checked 26 November 2026 \u00b7 All events of "
           "Wednesday 25 November 2026",
           font=sans(11), fill=MUTED, anchor="ma")
    return img


if __name__ == "__main__":
    render().save("entry.png", optimize=True)
    print("wrote entry.png")
