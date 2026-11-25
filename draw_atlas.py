#!/usr/bin/env python3
"""Draw the round-2 news-image entry: THE WORLD ATLAS, 25 November 2026.

A world-atlas broadsheet: header, a stylised world-map strip with red
story dots, and seven region panels holding 38 dated stories.
Deterministic: same input always renders the same PNG bytes.
Requires Pillow and the DejaVu fonts shipped with the system.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
DATE = "25 NOVEMBER 2026"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PARCHMENT = (245, 238, 220)
CARD = (255, 253, 246)
INK = (31, 42, 68)
BODY = (74, 70, 60)
BORDER = (216, 205, 178)
OCEAN = (196, 214, 221)
LAND = (220, 203, 156)
LAND_EDGE = (160, 140, 90)
DOT = (179, 64, 46)
WHITE = (255, 255, 255)

REGIONS = [
    ("EUROPE", (36, 71, 110), [
        ("Kyiv claims Baltic ship strike",
         "Drones hit the weapons ship Sparta II in the Gulf of Finland."),
        ("11 dead in Kyiv flat strike",
         "Rescuers pull 11 bodies from a block hit by drones; 2 killed in Zaporizhzhia."),
        ("War dead put at 720,000",
         "Leaked Russian records put the war's dead at 720,000 - the grimmest toll yet."),
        ("Sarkozy ordered to trial",
         "Sarkozy and Carla Bruni face trial over Libya; first hearing 1 April 2027."),
        ("NATO jets scrambled for Poland",
         "Putin warns retaliation is \u201cinevitable\u201d as Ukraine hits Russian refineries."),
        ("Norway pledges $7bn for 2027",
         "Norway will give Ukraine at least $7bn in 2027, air defence first."),
    ]),
    ("MIDDLE EAST", (168, 68, 42), [
        ("Houthis hit Riyadh's tallest tower",
         "Strike wounds 11 in the financial district; Houthis now 60 km from Aden."),
        ("Tankers hit by mines in Hormuz",
         "Three tankers under US air escort struck by mines in the Strait of Hormuz."),
        ("Iran rations electricity",
         "Tehran rations power and vows \u201call available means\u201d against the US blockade."),
        ("Iraq moves on Kurdish oilfields",
         "Baghdad moves to take control of Kurdish oilfields in a new escalation."),
        ("Gaza strikes kill seven",
         "Israeli strikes kill seven in Gaza, including Hamas's security director."),
        ("Houthis threaten Jeddah",
         "Houthis threaten Jeddah and Saudi Red Sea ports if Hodeidah is attacked."),
    ]),
    ("ASIA-PACIFIC", (31, 110, 107), [
        ("Huawei guilty in US court",
         "Jury finds Huawei guilty of trade-secrets conspiracy and fraud over Iran."),
        ("Pakistan's first astronaut",
         "Pakistan sends its first astronaut to China's space station."),
        ("China probes Shanghai chief",
         "Beijing investigates party chief Chen Jining; Hong Kong marks Tai Po fire year."),
        ("Dozens trapped in Indonesia mine",
         "Rescuers search for miners trapped in a 100-metre-deep mine after rains."),
        ("Solomons sign security pact",
         "Solomon Islands and Australia sign a treaty excluding foreign bases."),
        ("Russian jets enter Korean zone",
         "South Korea says Russian jets entered its air defence identification zone."),
    ]),
    ("AFRICA", (176, 122, 31), [
        ("Congo rebels pull back from Bunia",
         "Rebels retreat after heavy clashes; a military aircraft is reported missing."),
        ("175 migrants missing at sea",
         "A boat from Senegal vanishes; 175 migrants feared missing."),
        ("Senegal's title restored",
         "CAS reinstates Senegal as Africa Cup of Nations champions, overturning Morocco."),
        ("Benghazi strike fallout",
         "Kyiv calls sinking the corvette Merkury self-defence; Libya seeks UN meeting."),
        ("Zambia indicts opposition leader",
         "Zambia indicts an opposition leader on treason charges; Khartoum drones condemned."),
        ("Drones hit Khartoum",
         "Drone attacks on Khartoum draw condemnation; abductions reported in Blue Nile."),
    ]),
    ("THE AMERICAS", (62, 107, 47), [
        ("Trump spares two turkeys",
         "Trump pardons turkeys Freedom and Feathers at the White House Thanksgiving ceremony."),
        ("Fort Hood gunman seeks stay",
         "The Fort Hood gunman asks a court to stay his execution."),
        ("Cartagena hostages freed",
         "Armed men held about 20 hostages in a supermarket; all freed without casualties."),
        ("Democrats take the House",
         "Democrats win a House majority of at least 259 seats in Washington."),
        ("Colombia car bomb injures 23",
         "A car bomb injures 23 people in Colombia."),
        ("Six die in Gulf plane crash",
         "A small plane crashes in the Gulf of Mexico, killing six people."),
    ]),
    ("SPORT", (142, 43, 59), [
        ("England level the T20 series",
         "England beat Australia by 8 wickets in the 2nd T20I, chasing 184 on the Gold Coast."),
        ("Real Madrid sink PSV 5-1",
         "Madrid overturn an early deficit to win 5-1 in the Champions League."),
        ("15-year-old smashes 204",
         "Vaibhav Sooryavanshi, 15, hits 204 off 53 balls - 28 sixes, a List A record - in Doha."),
        ("Ronaldo's 987th goal",
         "Cristiano Ronaldo scores his 987th career goal as Al Nassr win the Asian Champions League."),
        ("Gukesh holds Sindarov",
         "World champion Gukesh draws game one of his title defence in Geneva, 0.5-0.5."),
        ("Sri Lanka Women take trophy",
         "Sri Lanka Women beat Ireland by six wickets to win the Emerging Nations Trophy."),
    ]),
    ("MARKETS & TECH", (91, 58, 110), [
        ("Nvidia's $1 trillion day",
         "Shares jump 31.5% as Huang returns as CEO, recouping ~$34bn - then fall 7% on Tuesday."),
        ("Nikkei slides 2.76%",
         "Asian tech stocks sell off on AI doubts; S&P 500 -0.5%; Brent down 21% in the month."),
        ("COP31 talks collapse",
         "Climate talks in Antalya collapse as oil producers block a fossil-fuel phase-out."),
        ("AI safety doubts inside labs",
         "Staff at Anthropic and OpenAI doubt unreleased models can be safely released."),
        ("Bangladesh wage rises 36%",
         "Textile minimum wage rises 36% after weeks of protests; Sensex gains 1.8%."),
        ("Venezuela reveals $237.5bn debt",
         "Caracas reveals $237.5 billion in public debt; 112 ransomware claims logged in 48 hours."),
    ]),
]

CONTINENTS = [
    [(70, 148), (120, 126), (200, 122), (258, 130), (284, 144), (270, 160),
     (240, 170), (222, 182), (196, 190), (170, 196), (140, 190), (106, 176), (74, 164)],
    [(292, 116), (318, 114), (326, 126), (302, 134)],
    [(252, 202), (290, 196), (320, 206), (314, 224), (290, 222), (266, 212), (250, 206)],
    [(478, 134), (516, 124), (548, 128), (552, 144), (534, 152), (506, 152), (482, 144)],
    [(478, 160), (536, 154), (578, 164), (592, 186), (574, 214), (550, 224),
     (522, 218), (496, 196), (476, 176)],
    [(552, 124), (640, 114), (750, 116), (850, 126), (890, 142), (872, 164),
     (824, 176), (776, 190), (716, 186), (664, 176), (616, 166), (572, 152)],
    [(806, 212), (868, 208), (892, 220), (874, 226), (824, 226), (804, 220)],
]

# (x, y, label-or-None, label-dx, label-dy) story dots on the map strip
DOTS = [
    (556, 132, None, 8, -6), (540, 146, "KYIV", -30, 9), (498, 142, None, 8, -6),
    (490, 136, None, 8, -6),
    (606, 186, "RIYADH", 8, -6), (620, 200, None, 8, -6), (648, 158, "TEHRAN", 8, -6),
    (622, 172, None, 8, -6), (560, 146, None, 8, -6), (548, 208, "BUNIA", 8, -6),
    (468, 186, "DAKAR", -38, -6), (540, 168, None, 8, -6),
    (218, 158, "WASHINGTON", 8, -6),
    (288, 210, "BOGOTA", 8, -6), (792, 140, "BEIJING", 8, -6), (812, 212, None, 8, -6),
    (614, 182, None, 8, -6), (892, 222, None, 8, -6), (706, 158, None, 8, -6),
    (266, 200, None, 8, -6),
]

SOURCES = ("SOURCES: REUTERS \u00b7 KYIV INDEPENDENT \u00b7 AL JAZEERA \u00b7 PRO PUBLICA "
           "\u00b7 AXIOS \u00b7 AP \u00b7 CAS \u00b7 THE DAILY EDITION \u00b7 ONE TURN "
           "\u00b7 HORIZON \u00b7 MYKHEL")


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
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


def centre(draw, y, text, fnt, fill):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")

def draw_header(draw):
    kicker = font("DejaVuSans-Bold.ttf", 12)
    title = font("DejaVuSerif-Bold.ttf", 52)
    total = sum(len(items) for _, _, items in REGIONS)
    centre(draw, 28, "TUESDAY \u00b7 25 NOVEMBER 2026 \u00b7 %d STORIES \u00b7 SEVEN REGIONS" % total,
           kicker, BODY)
    centre(draw, 46, "THE WORLD ATLAS", title, INK)
    draw.line([(120, 104), (904, 104)], fill=INK, width=2)
    draw.line([(120, 108), (904, 108)], fill=INK, width=1)


def draw_map(draw):
    x0, y0, x1, y1 = 24, 116, 1000, 228
    draw.rectangle([x0, y0, x1, y1], fill=OCEAN, outline=INK, width=1)
    for gx in range(120, 1000, 120):
        draw.line([(gx, y0), (gx, y1)], fill=(255, 255, 255), width=1)
    for gy in (150, 185, 220):
        draw.line([(x0, gy), (x1, gy)], fill=(255, 255, 255), width=1)
    for poly in CONTINENTS:
        draw.polygon(poly, fill=LAND, outline=LAND_EDGE)
    draw.ellipse([795, 196, 812, 206], fill=LAND, outline=LAND_EDGE)
    draw.ellipse([828, 200, 842, 210], fill=LAND, outline=LAND_EDGE)
    lab = font("DejaVuSans-Bold.ttf", 9)
    for (x, y, name, dx, dy) in DOTS:
        draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=DOT, outline=WHITE, width=1)
        draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=WHITE)
        if name:
            draw.text((x + dx, y + dy), name, font=lab, fill=INK)
    draw.ellipse([956, 120, 978, 142], outline=INK, width=1)
    draw.text((967, 121), "N", font=font("DejaVuSans-Bold.ttf", 10), fill=INK, anchor="ma")
    draw.polygon([(967, 130), (963, 140), (971, 140)], fill=INK)
    cap = font("DejaVuSans-Bold.ttf", 9)
    draw.text((x0 + 8, y1 - 16), "RED DOTS MARK TODAY'S STORIES",
              font=cap, fill=(70, 90, 100))


def draw_panel(draw, x, y, w, h, name, color, items, hl=14, dl=13, gap=6):
    head = font("DejaVuSans-Bold.ttf", 13)
    count = font("DejaVuSans-Bold.ttf", 10)
    bold = font("DejaVuSans-Bold.ttf", 12)
    body = font("DejaVuSans.ttf", 10)
    tag = font("DejaVuSans-Bold.ttf", 8)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=CARD, outline=BORDER)
    draw.rounded_rectangle([x, y, x + w, y + 30], radius=6, fill=color)
    draw.rectangle([x, y + 24, x + w, y + 30], fill=color)
    draw.text((x + 10, y + 8), name, font=head, fill=WHITE)
    label = "%d STORIES" % len(items)
    draw.text((x + w - 10, y + 10), label, font=count, fill=WHITE, anchor="ra")
    cy = y + 40
    for headline, detail in items:
        draw.rounded_rectangle([x + 10, cy, x + 54, cy + 13], radius=3, fill=color)
        draw.text((x + 32, cy + 2), "25 NOV", font=tag, fill=WHITE, anchor="ma")
        ly = cy - 1
        for line in wrap(draw, headline, bold, w - 70):
            draw.text((x + 60, ly), line, font=bold, fill=INK)
            ly += hl
        for line in wrap(draw, detail, body, w - 20):
            draw.text((x + 10, ly + 1), line, font=body, fill=BODY)
            ly += dl
        cy = ly + gap
        if cy > y + h - 4:
            print("OVERFLOW in panel %s (ends %d, limit %d)" % (name, cy, y + h),
                  file=sys.stderr)
    return cy


def draw_footer(draw):
    small = font("DejaVuSans.ttf", 9)
    bold = font("DejaVuSans-Bold.ttf", 9)
    centre(draw, 968, SOURCES, small, BODY)
    centre(draw, 986, "ALL STORIES DATED 25 NOVEMBER 2026 \u00b7 DRAWN WITH PILLOW \u00b7 1024 \u00d7 1024",
           bold, INK)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PARCHMENT)
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)
    draw.rectangle([16, 16, W - 17, H - 17], outline=BORDER, width=1)
    draw_header(draw)
    draw_map(draw)
    row1 = REGIONS[:4]
    row2 = REGIONS[4:]
    xs1 = [24, 270, 516, 762]
    for (name, color, items), px in zip(row1, xs1):
        draw_panel(draw, px, 238, 236, 372, name, color, items, hl=13, dl=12, gap=5)
    xs2 = [24, 353, 682]
    for (name, color, items), px in zip(row2, xs2):
        draw_panel(draw, px, 620, 317, 338, name, color, items, hl=15, dl=13, gap=8)
    draw_footer(draw)
    img.save(out, format="PNG", optimize=True)
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
