#!/usr/bin/env python3
"""Paint the round-3 poster: one day of world news laid out as a 24-hour wire.

The page opens with a navy masthead naming the day, then three large
hand-painted panels carry the biggest stories, and a two-column wire below
them runs through the rest of the day in order. Every position is fixed
and every picture is painted with Pillow alone, so running this file twice
gives byte-identical PNG output.
"""
from PIL import Image
from PIL import ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
SHEET = (246, 241, 231)
INK_COL = (25, 25, 35)
NAVY_COL = (20, 38, 63)
NAVY_SOFT_COL = (38, 62, 96)
SCARLET = (179, 38, 30)
TEAL_COL = (14, 107, 107)
GOLD_COL = (176, 124, 18)
MUTED_COL = (90, 90, 102)
WHITE_COL = (255, 255, 255)
CARD = (255, 255, 255)
RULE_COL = (196, 188, 172)

TYPE_DIR = "/usr/share/fonts/truetype/dejavu/"


def _open_typeface(path, size):
    return ImageFont.truetype(path, size)


_TYPEFACE_FILES = {
    "serif_strong": "DejaVuSerif-Bold.ttf",
    "sans_strong": "DejaVuSans-Bold.ttf",
    "sans_plain": "DejaVuSans.ttf",
}


def _typeface(kind):
    path = TYPE_DIR + _TYPEFACE_FILES[kind]
    return lambda size: _open_typeface(path, size)


serif_strong = _typeface("serif_strong")
sans_strong = _typeface("sans_strong")
sans_plain = _typeface("sans_plain")


def fit_lines(pen, text, face, span):
    """Break `text` into lines no wider than `span`, measured in the real face."""
    pieces = text.split()
    built, current = [], ""
    for piece in pieces:
        attempt = (current + " " + piece).strip()
        if pen.textlength(attempt, font=face) <= span:
            current = attempt
        else:
            if current:
                built.append(current)
            current = piece
    if current:
        built.append(current)
    return built


def blit_lines(pen, xy, rows, face, colour, pitch):
    """Stamp each row of text, stepping down `pitch` pixels per row."""
    x, y = xy
    for row in rows:
        pen.text((x, y), row, font=face, fill=colour)
        y += pitch
    return y


def _paint_puffs(pen, puffs, tone):
    """Stamp a run of soft round smoke puffs onto the canvas."""
    for cx, cy, radius in puffs:
        pen.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                    fill=tone)


# ---------------------------------------------------------------- painted scenes
def draw_tanker_scene(pen, left, top, span, tall):
    """A tanker ablaze in a strait at dusk, seen from the waterline."""
    pen.rectangle([left, top, left + span, top + tall], fill=(27, 42, 74))
    pen.ellipse([left + span - 52, top + 10, left + span - 18, top + 44],
                fill=(232, 214, 160))
    pen.rectangle([left, top + tall * 0.62, left + span, top + tall],
                  fill=(39, 75, 99))
    # white wave crests rippling across the lower water
    for k in range(5):
        crest_x = left + 12 + k * 62
        pen.arc([crest_x, top + tall - 26, crest_x + 44, top + tall - 8],
                180, 360, fill=(255, 255, 255))
    # the hull and its red waterline band
    pen.rectangle([left + 28, top + tall * 0.58, left + span - 28,
                   top + tall * 0.80], fill=(32, 32, 40))
    pen.rectangle([left + 28, top + tall * 0.58, left + span - 28,
                   top + tall * 0.63], fill=(179, 38, 30))
    # containers stacked on the deck
    for bay, tone in enumerate([(196, 90, 30), (38, 110, 140), (176, 124, 18)]):
        crate_x = left + 48 + bay * 62
        pen.rectangle([crate_x, top + tall * 0.40, crate_x + 54,
                       top + tall * 0.58], fill=tone)
    # the bridge tower at the stern
    pen.rectangle([left + span - 78, top + tall * 0.34, left + span - 44,
                   top + tall * 0.58], fill=(240, 240, 235))
    # three flames licking up from the deck
    for base_x, tip_dx, end_dx, tip_frac, flame in [
            (96, 20, 42, 0.18, (232, 110, 20)),
            (150, 18, 36, 0.30, (240, 180, 40)),
            (196, 16, 32, 0.22, (232, 110, 20))]:
        pen.polygon([(left + base_x, top + tall * 0.58),
                     (left + base_x + tip_dx, top + tall * tip_frac),
                     (left + base_x + end_dx, top + tall * 0.58)],
                    fill=flame)
    # smoke drifting above the fire
    _paint_puffs(pen, [(left + 120, top + 26, 12), (left + 150, top + 14, 15),
                       (left + 186, top + 24, 11), (left + 214, top + 12, 13)],
                 (120, 120, 128))


def draw_market_scene(pen, left, top, span, tall):
    """A market board whose line plunges off a cliff."""
    pen.rectangle([left, top, left + span, top + tall], fill=(255, 255, 255))
    for row in range(4):
        grid_y = top + 18 + row * 26
        pen.line([left + 12, grid_y, left + span - 12, grid_y],
                 fill=(228, 228, 228))
    # the plunging line, arrowhead at its foot
    path = [(left + 16, top + 22), (left + 70, top + 30),
            (left + 120, top + 26), (left + 168, top + 52),
            (left + 214, top + 66), (left + 258, top + 96),
            (left + span - 16, top + tall - 18)]
    pen.line(path, fill=(179, 38, 30), width=5, joint="curve")
    pen.polygon([(left + span - 16, top + tall - 18),
                 (left + span - 34, top + tall - 30),
                 (left + span - 30, top + tall - 10)], fill=(179, 38, 30))
    # red bars sinking toward the floor
    for bay, bar_h in enumerate([66, 52, 40, 26]):
        bar_x = left + 30 + bay * 64
        pen.rectangle([bar_x, top + tall - 12 - bar_h, bar_x + 34,
                       top + tall - 12], fill=(196, 60, 48))
    pen.text((left + 14, top + 6), "KOSPI", font=sans_strong(13),
             fill=(90, 90, 102))
    pen.text((left + span - 118, top + 8), "-6.16%", font=sans_strong(30),
             fill=(179, 38, 30))


def draw_rocket_scene(pen, left, top, span, tall):
    """A crewed rocket climbing away through a starry sky."""
    pen.rectangle([left, top, left + span, top + tall], fill=(16, 24, 48))
    stars = [(30, 18), (70, 44), (120, 14), (170, 38),
             (220, 16), (262, 48), (52, 84), (250, 84),
             (140, 70), (200, 96)]
    for star_x, star_y in stars:
        pen.ellipse([left + star_x - 2, top + star_y - 2,
                     left + star_x + 2, top + star_y + 2],
                    fill=(255, 255, 255))
    # the pad ground at the foot of the panel
    pen.rectangle([left, top + tall - 14, left + span, top + tall],
                  fill=(60, 58, 66))
    # the exhaust flame under the body
    centre = left + span // 2
    pen.polygon([(centre - 12, top + 74), (centre, top + 118),
                 (centre + 12, top + 74)], fill=(240, 140, 20))
    pen.polygon([(centre - 6, top + 74), (centre, top + 100),
                 (centre + 6, top + 74)], fill=(250, 210, 80))
    # body, nose cone, fins and window
    pen.rounded_rectangle([centre - 16, top + 12, centre + 16, top + 76],
                          radius=14, fill=(240, 240, 235))
    pen.polygon([(centre - 16, top + 22), (centre, top + 2),
                 (centre + 16, top + 22)], fill=(179, 38, 30))
    pen.polygon([(centre - 16, top + 56), (centre - 32, top + 78),
                 (centre - 16, top + 76)], fill=(179, 38, 30))
    pen.polygon([(centre + 16, top + 56), (centre + 32, top + 78),
                 (centre + 16, top + 76)], fill=(179, 38, 30))
    pen.ellipse([centre - 7, top + 30, centre + 7, top + 44],
                fill=(38, 62, 96))
    # smoke curling around the pad
    _paint_puffs(pen, [(centre - 46, top + tall - 30, 12),
                       (centre + 44, top + tall - 26, 14),
                       (centre - 24, top + tall - 22, 10),
                       (centre + 22, top + tall - 20, 9)], (150, 150, 158))


# ---------------------------------------------------------------- the stories
REGION_INK = {
    "MIDDLE EAST": SCARLET,
    "EAST ASIA": TEAL_COL,
    "SPACE": NAVY_SOFT_COL,
    "PACIFIC": (31, 111, 178),
    "EUROPE": (46, 94, 140),
    "NORTH AMERICA": (138, 90, 0),
    "AFRICA": (62, 122, 58),
    "LATIN AMERICA": (194, 94, 0),
    "WORLD": MUTED_COL,
}

LEADS = [
    ("MIDDLE EAST", draw_tanker_scene,
     "Tankers burn in the Strait of Hormuz",
     "Iran says tankers struck mines and caught fire; Tehran says "
     "their route was unauthorised."),
    ("EAST ASIA", draw_market_scene,
     "Asia's chip shares plunge",
     "Seoul's Kospi falls 6.16% \u2014 Samsung \u22129.9%, SK Hynix "
     "\u221211.1% \u2014 as the AI rally unwinds."),
    ("SPACE", draw_rocket_scene,
     "Pakistan reaches orbit",
     "Shenzhou-24 lifts off at 00:18 GMT; Muhammad Zeeshan Ali, 40, "
     "is the first Pakistani in space."),
]

# (region, headline) -- every headline is dated 25 November 2026.
WIRE = [
    ("EAST ASIA", "Shenzhou-24 docks with Tiangong at 03:56 GMT, three and "
     "a half hours after lift-off."),
    ("EAST ASIA", "Tang Hongbo boards Tiangong for a third time, a first "
     "for any astronaut."),
    ("EAST ASIA", "Taiwan's Taiex slides about 5% as the chip sell-off "
     "spreads across Asia."),
    ("EAST ASIA", "SoftBank tumbles 14.8% in Tokyo, leading Japanese "
     "shares lower."),
    ("PACIFIC", "Australia and Solomon Islands sign a treaty in Canberra "
     "barring foreign bases on the islands."),
    ("EUROPE", "Ukrainian drones set two Rosneft refineries ablaze in "
     "Samara; one person is killed."),
    ("EUROPE", "A Russian strike on Odesa kills two and injures three, "
     "including a child."),
    ("EUROPE", "Kyiv reports a fire in a tower block after overnight "
     "strikes; two people are hurt."),
    ("MIDDLE EAST", "Houthis say they struck Saudi Arabia's Ras Tanura "
     "refinery; fires are reported."),
    ("NORTH AMERICA", "Washington proposes new tariffs on 14 partners at "
     "20\u201340%; nothing before a 25 January hearing."),
    ("EUROPE", "Zelensky says Ukraine needs \u20ac115bn in foreign aid "
     "for 2027."),
    ("EUROPE", "Poland presses for a permanent US troop presence after "
     "two airspace incursions in four days."),
    ("EUROPE", "Eurozone inflation rises to 4.0%, Eurostat "
     "reports."),
    ("PACIFIC", "Australian inflation climbs to 4.9%, driven by "
     "fuel prices."),
    ("MIDDLE EAST", "Israel kills Hamas colonel Mohammad Abuelouf in Gaza; "
     "his wife and two children also die."),
    ("AFRICA", "Sudanese paramilitary drone strikes kill 19 civilians and "
     "wound 20 in two cities."),
    ("LATIN AMERICA", "Colombian troops free every hostage in a Cartagena "
     "supermarket siege; one captor is killed."),
    ("EUROPE", "Pope Leo XIV speaks out over the COP31 talks' failure "
     "to reach a deal."),
    ("WORLD", "The UN warns funding cuts put decades of progress "
     "against HIV at risk."),
    ("EUROPE", "Kyiv says its drones sank a Russian warship off the "
     "Libyan coast."),
    ("NORTH AMERICA", "Kilmar Abrego Garcia leaves the US for Spain after a "
     "20-month legal fight."),
    ("NORTH AMERICA", "The US Army destroys about five tons of degraded "
     "explosive in a controlled Iowa blast."),
    ("AFRICA", "Senegal are restored as Africa Cup of Nations champions "
     "by sport's highest court."),
]


def paint_masthead(brush):
    """The navy banner across the top: title, date and story count."""
    brush.rectangle([0, 0, PAGE_W, 104], fill=NAVY_COL)
    brush.rectangle([0, 100, PAGE_W, 104], fill=GOLD_COL)
    brush.text((24, 14), "THE DAY IN 24 HOURS", font=serif_strong(42), fill=WHITE_COL)
    brush.text((24, 66), "One day of world news, hour by hour",
               font=sans_plain(15), fill=(200, 208, 222))
    brush.text((1000, 12), "WEDNESDAY", font=sans_strong(16),
               fill=(200, 208, 222), anchor="ra")
    brush.text((1000, 34), "25 NOVEMBER 2026", font=sans_strong(30),
               fill=WHITE_COL, anchor="ra")
    brush.text((1000, 70), "26 stories \u00b7 8 regions \u00b7 all times UTC",
               font=sans_plain(13), fill=(200, 208, 222), anchor="ra")


def paint_lead(brush, x, entry):
    """One lead panel: colour strip, painted scene, headline and detail."""
    region, scene, head, detail = entry
    tint = REGION_INK[region]
    brush.rectangle([x, 116, x + 320, 336], fill=CARD, outline=RULE_COL, width=1)
    brush.rectangle([x, 116, x + 320, 122], fill=tint)
    brush.text((x + 12, 128), region, font=sans_strong(12), fill=tint)
    scene(brush, x + 12, 148, 296, 108)
    title_rows = fit_lines(brush, head, sans_strong(16), 296)
    blit_lines(brush, (x + 12, 262), title_rows[:2], sans_strong(16), INK_COL, 19)
    body_rows = fit_lines(brush, detail, sans_plain(12), 296)
    blit_lines(brush, (x + 12, 262 + len(title_rows[:2]) * 19 + 4),
               body_rows[:2], sans_plain(12), MUTED_COL, 14)


def paint_date_check(brush, check_x, check_y, span, pitch):
    """The small box that vouches for the date of every story."""
    brush.rounded_rectangle([check_x, check_y + 2, check_x + span,
                             check_y + pitch - 4], radius=6,
                            outline=NAVY_SOFT_COL, width=1, fill=(232, 238, 246))
    brush.text((check_x + 10, check_y + 6), "DATE CHECK", font=sans_strong(11),
               fill=NAVY_SOFT_COL)
    brush.text((check_x + 10, check_y + 22),
               "Every story is dated Wednesday 25 November 2026.",
               font=sans_plain(12), fill=INK_COL)


def paint_footer(brush):
    """The figures strip and the source lines along the bottom edge."""
    brush.line([24, 932, 1000, 932], fill=RULE_COL, width=1)
    figures = ("KOSPI \u22126.16%  \u00b7  NIKKEI \u22122.78%  \u00b7  SOFTBANK "
               "\u221214.8%  \u00b7  \u20ac115BN AID ASK  \u00b7  14 TARIFF "
               "PARTNERS  \u00b7  5 TONS DESTROYED")
    figures_size = 10
    for size in range(14, 9, -1):
        if brush.textlength(figures, font=sans_strong(size)) <= 960:
            figures_size = size
            break
    brush.text((512, 944), figures, font=sans_strong(figures_size),
               fill=NAVY_COL, anchor="ma")
    brush.text((512, 970),
               "Sources: Reuters \u00b7 AP \u00b7 Nature \u00b7 Just Security "
               "\u00b7 Xinhua \u00b7 Eurostat",
               font=sans_plain(12), fill=MUTED_COL, anchor="ma")
    brush.text((512, 992),
               "Drawn and checked 26 November 2026 \u00b7 All events of "
               "Wednesday 25 November 2026",
               font=sans_plain(11), fill=MUTED_COL, anchor="ma")


def compose_poster():
    """Assemble the whole page and hand back the finished image."""
    sheet = Image.new("RGB", (PAGE_W, PAGE_H), SHEET)
    pen = ImageDraw.Draw(sheet)

    # ---------------------------------------------------------- masthead
    paint_masthead(pen)

    # ---------------------------------------------------------- lead panels
    lead_lefts = [24, 352, 680]
    for slot, entry in enumerate(LEADS):
        paint_lead(pen, lead_lefts[slot], entry)

    # ---------------------------------------------------------- wire header
    pen.text((24, 348), "THE WIRE", font=sans_strong(17), fill=NAVY_COL)
    pen.text((150, 351),
             "the rest of the day, in order \u2014 every story dated 25 November 2026",
             font=sans_plain(13), fill=MUTED_COL)
    pen.line([24, 374, 1000, 374], fill=RULE_COL, width=1)

    # ---------------------------------------------------------- wire columns
    wire_lefts = [24, 528]
    wire_span = 472
    rows_per_col = 12
    wire_top, wire_base = 382, 920
    row_pitch = (wire_base - wire_top) / rows_per_col
    early = WIRE[:12]
    late = WIRE[12:]
    pen.line([512, wire_top, 512, wire_base], fill=RULE_COL, width=1)
    for x, stories in zip(wire_lefts, (early, late)):
        for row, (region, head) in enumerate(stories):
            y = wire_top + row * row_pitch
            pen.text((x, y), region, font=sans_strong(11),
                     fill=REGION_INK[region])
            rows = fit_lines(pen, head, sans_plain(13), wire_span)
            blit_lines(pen, (x, y + 13), rows[:2], sans_plain(13), INK_COL, 15)

    # the date-check box fills the spare cell of the right column
    check_x, check_y = wire_lefts[1], wire_top + 11 * row_pitch
    paint_date_check(pen, check_x, check_y, wire_span, row_pitch)

    # ---------------------------------------------------------- footer
    paint_footer(pen)
    return sheet


if __name__ == "__main__":
    compose_poster().save("entry.png", optimize=True)
    print("wrote entry.png")
