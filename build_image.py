#!/usr/bin/env python3
"""Broadsheet generator for Friday, 27 November 2026.

Draws a one-page world-news summary at 1024x1024 with Pillow.
Every story in STORIES was verified against the sources listed in
SOURCES.md (kept in the work folder) on the day itself.
Run:  python3 build_image.py   ->  writes entry.png next to this file
"""
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

W = H = 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
RED = (178, 34, 24)
NAVY = (23, 54, 93)
GOLD = (166, 124, 10)
GREY = (92, 92, 86)
LIGHT = (232, 226, 208)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
COND_B = "/usr/share/fonts/truetype/noto/NotoSans-CondensedBold.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 18  # margin

def wrap(text, font, width):
    out, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            line = trial
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out

def text_block(x, y, text, font, width, fill=INK, leading=4, max_lines=None):
    lines = wrap(text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    step = font.size + leading
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += step
    return y

# ---------- masthead ----------
d.text((W // 2, 10), "THE DAILY WORLD", font=f(SERIF_B, 46), fill=INK, anchor="ma")
d.line([(M, 62), (W - M, 62)], fill=INK, width=3)
d.rectangle([M, 66, W - M, 100], fill=NAVY)
d.text((W // 2, 71), "FRIDAY, 27 NOVEMBER 2026", font=f(SANS_B, 27), fill=(255, 255, 255), anchor="ma")
d.rectangle([M, 103, W - M, 127], fill=RED)
d.text((W // 2, 108), "28 STORIES  ·  EUROPE 6  ·  ASIA 7  ·  AFRICA 4  ·  N. AMERICA 4  ·  MIDDLE EAST 3  ·  S. AMERICA 2  ·  OCEANIA 1  ·  GLOBAL 1",
       font=f(SANS_B, 14), fill=(255, 255, 255), anchor="ma")

# ---------- lead story ----------
LY = 136
d.text((M, LY), "LEAD STORY — KUWAIT CITY, KUWAIT", font=f(SANS_B, 13), fill=RED)
y = text_block(M, LY + 20,
               "Drone strike kills two Italians in Kuwait — Iran denies blame",
               f(SERIF_B, 31), 612)
y = text_block(M, y + 4,
               "Two Italian technicians working on an air-defence system were killed when debris from "
               "intercepted drones hit a Kuwaiti military site. Kuwait and Italy blame Iran. Tehran calls "
               "the incident a \u201cprecooked recipe for war\u201d, denies any role and offers a joint investigation. "
               "A Kuwaiti and a Pakistani were also hurt — the first fatal strike in Kuwait in this war.",
               f(SANS, 14), 612, leading=3)
d.text((M, y + 6), "Trump: US has \u201cvictory at hand\u201d in Iran war, offers Tehran a deal  ·  Brent near $96 on Hormuz fears",
       font=f(SANS_B, 12), fill=NAVY)

# ---------- where-it-happened map ----------
MX0, MY0, MX1, MY1 = 652, 136, W - M, 318
d.rectangle([MX0, MY0, MX1, MY1], outline=INK, width=2)
d.rectangle([MX0, MY0, MX1, MY0 + 22], fill=INK)
d.text(((MX0 + MX1) // 2, MY0 + 4), "WHERE IT HAPPENED", font=f(SANS_B, 13), fill=(255, 255, 255), anchor="ma")
# graticule + continent labels
for lon in range(-150, 181, 30):
    x = MX0 + 8 + (lon + 180) / 360 * (MX1 - MX0 - 16)
    d.line([(x, MY0 + 26), (x, MY1 - 6)], fill=(214, 208, 190), width=1)
for name, lon, lat in [("N. AMERICA", -105, 48), ("S. AMERICA", -62, -18), ("EUROPE", -28, 58),
                       ("AFRICA", 22, -10), ("ASIA", 92, 46), ("OCEANIA", 140, -28)]:
    x = MX0 + 8 + (lon + 180) / 360 * (MX1 - MX0 - 16)
    yy = MY0 + 26 + (78 - lat) / 138 * (MY1 - MY0 - 34)
    d.text((x, yy), name, font=f(SANS_B, 9), fill=(150, 142, 118), anchor="mm")

def plot(num, lon, lat):
    x = MX0 + 8 + (lon + 180) / 360 * (MX1 - MX0 - 16)
    yy = MY0 + 26 + (78 - lat) / 138 * (MY1 - MY0 - 34)
    r = 8
    d.ellipse([x - r, yy - r, x + r, yy + r], fill=RED, outline=(255, 255, 255), width=1)
    d.text((x, yy - 6), str(num), font=f(SANS_B, 10), fill=(255, 255, 255), anchor="ma")

for num, lon, lat in [(1, 47, 29), (2, 30, 50), (3, 30, 2), (4, -96, 38), (14, 174, -41),
                      (20, 31, 30), (19, 10, 16), (23, 116, 39), (27, 107, -7), (15, -3, 40),
                      (13, 34, 31), (22, 100, 13), (25, -58, -34), (18, -122, 37)]:
    plot(num, lon, lat)
d.text((MX0 + 8, MY1 - 20), "Numbers match the stories below.", font=f(SANS, 10), fill=GREY)

# ---------- story grid ----------
STORIES = [
    ("2 · UKRAINE", "Zelenskyy warns of new Russian mass strike",
     "Kyiv says Moscow is preparing a major attack on the power grid. Trump says he pressed Putin to pull back in Europe; overnight missiles wounded 7 in Kyiv."),
    ("3 · DR CONGO — HEALTH", "Ebola outbreak passes 12,000 cases",
     "Deaths reach 5,904 in the second-largest Ebola outbreak on record. Fighting in Ituri is disrupting the response and responders have evacuated."),
    ("4 · UNITED STATES", "Thanksgiving storms cut power to 800,000+",
     "Storms on both coasts blacked out over 800,000 homes, cancelled some 400 flights and postponed New York's Macy's parade for the first time in 100 years."),
    ("5 · EUROPEAN UNION", "EU delays \u20ac45bn Ukraine loan and budget deal",
     "Leaders ended a special summit with no deal, pushing both decisions to December. 24 states back the loan; Slovakia, Hungary and Czechia seek an opt-out."),
    ("6 · EURO ZONE", "Spain's de Cos chosen as next ECB president",
     "EU leaders pick Pablo Hern\u00e1ndez de Cos, ex-Bank of Spain governor, to succeed Christine Lagarde in February 2027 — the first Spaniard to hold the post."),
    ("7 · MYANMAR — JUSTICE", "Myanmar defies ICJ genocide ruling",
     "Yangon says it will not fully comply with the World Court, which held Myanmar responsible for genocide against the Rohingya — a first for the UN court."),
    ("8 · TRADE", "US proposes new tariffs on 14 partners",
     "Washington cites \u201cstructural overcapacity\u201d, with rates up to 40% on China. Beijing, Brussels and Bras\u00edlia all reject the rationale outright."),
    ("9 · AFRICA — HEALTH", "Twice-yearly HIV prevention shot reaches Africa",
     "A cheaper version of lenacapavir, an injection given twice a year and nearly 100% effective at preventing HIV, has now reached patients in Africa."),
    ("10 · CLIMATE", "Earth above 2\u00b0C for seven straight days",
     "The planet averaged over 2\u00b0C above pre-industrial levels for a full week, a first. Pope Leo calls the collapse of the COP31 climate talks \u201ctroubling\u201d."),
    ("11 · UKRAINE — WAR", "Ukraine hits Russian airbase, five aircraft",
     "Kyiv says a strike on Savasleyka airbase damaged three MiG-31 fighters and two Su-34 bombers. IAEA seeks a ceasefire to repair Zaporizhzhia's power link."),
    ("12 · SAUDI ARABIA / YEMEN", "Houthi attack halts Jazan refinery",
     "A Houthi strike killed a Nepali worker and halted part of the Jazan refinery. Saudi Arabia answered with air strikes on 50 Houthi targets in Yemen."),
    ("13 · GAZA", "Israeli strikes kill 8–10, incl. Hamas official",
     "Strikes killed Palestinians in Gaza including Hamas-appointed deputy education minister Khaled Abu Nada. Hamas is weighing its response; truce strains."),
    ("14 · NEW ZEALAND", "Coalition falls one seat short of majority",
     "Final results give PM Luxon's National-led coalition 65 of 130 seats, one short. He now needs the centrist Opportunity Party to stay in power."),
    ("15 · SPAIN", "Spain votes Sunday as conservatives lead",
     "A snap election looms: the Popular Party leads polls but may need far-right Vox for a majority. PM S\u00e1nchez called the vote after a parliament setback."),
    ("16 · TAIWAN", "Taiwan holds local elections on Saturday",
     "The vote is a midterm test for President Lai Ching-te ahead of 2028. Officials warn of Chinese interference; a nuclear-power referendum is also on the ballot."),
    ("17 · TECHNOLOGY — US", "Nvidia's Huang returns; S&P warns on rating",
     "Jensen Huang is back as Nvidia CEO after a sudden exit and board reversal. S&P puts its rating on CreditWatch Negative over governance risk."),
    ("18 · SPACE — US", "FCC clears SpaceX plan for 1 million satellites",
     "Regulators approve up to one million orbital data-centre satellites. Musk also pledges two SpaceX shares to every US child, a gift worth about $18bn."),
    ("19 · NIGER", "13 soldiers killed in attack near Mali border",
     "Gunmen attacked a National Guard compound at Sanam, Tillab\u00e9ri, killing at least 13 soldiers and wounding 20. No group has claimed the attack."),
    ("20 · EGYPT", "Driver detained after Cairo tanker fire kills 31",
     "Prosecutors detain a 21-year-old driver after a fuel tanker overturned and burned on Cairo's Ring Road, killing 31 people and injuring 21."),
    ("21 · SPAIN — DISASTER", "Diesel tanker capsizes off Ibiza, one dead",
     "A tanker carrying up to 7,000 tonnes of diesel capsized off Ibiza. One crew member died, 16 were rescued and an anti-pollution plan was activated."),
    ("22 · THAILAND", "Explosion at Bangkok oil facility injures nine",
     "A blast and fire at a Bangchak oil facility in Bangkok injured at least nine people, three critically. Nearby residents were urged to leave the area."),
    ("23 · CHINA — MARKETS", "Profits +20.1%; stocks surge on state support",
     "Industrial profits jumped in October on AI demand. Shanghai rose ~3.3% and the STAR 50 about 12% after Beijing vowed stronger market support."),
    ("24 · JAPAN", "Tokyo inflation at 16-month high, 2.9%",
     "Core prices in Tokyo rose 2.9% in November, strengthening the case for a Bank of Japan rate hike as soon as December, board members signal."),
    ("25 · ARGENTINA", "Congress bars central bank from funding state",
     "Lawmakers bar the central bank from printing money to fund government spending. The Senate also voted 43–29 to suspend the 2027 primary elections."),
    ("26 · BRAZIL", "Lula picks banker Trabuco as finance minister",
     "President Lula names Bradesco chairman Luiz Carlos Trabuco, 75, for his fourth term. Markets welcome the pick; the Bovespa index jumps 6.07%."),
    ("27 · INDONESIA", "Gold mine flood: 13 dead, 13 missing",
     "Heavy rain burst the Ciseureuh River into an illegal gold mine shaft about 100 metres deep in West Java, killing 13 miners; 13 more are missing."),
    ("28 · INDONESIA — ECONOMY", "Jakarta weighs first fuel price hike in 5 years",
     "Reuters: officials consider raising subsidised fuel prices in early 2027 as the subsidy bill nears Rp500tn and the rupiah hits a record low."),
]

GY = 322
d.line([(M, GY - 6), (W - M, GY - 6)], fill=INK, width=2)
COLS = 3
col_w = (W - 2 * M - (COLS - 1) * 14) // COLS
rows = 9
row_h = (986 - GY) // rows
hf, bf, tf = f(COND_B, 14), f(SANS, 11), f(SANS_B, 9)
for i, (tag, head, body) in enumerate(STORIES):
    col, row = i // rows, i % rows
    x = M + col * (col_w + 14)
    yy = GY + row * row_h
    if row:
        d.line([(x, yy - 4), (x + col_w, yy - 4)], fill=LIGHT, width=1)
    d.text((x, yy), tag, font=tf, fill=RED)
    yy2 = text_block(x, yy + 13, head, hf, col_w, leading=1, max_lines=2)
    text_block(x, yy2 + 1, body, bf, col_w, fill=(40, 40, 38), leading=2, max_lines=3)

# ---------- footer ----------
d.line([(M, 990), (W - M, 990)], fill=INK, width=2)
d.text((W // 2, 996),
       "All 28 stories reported on Friday, 27 November 2026 · Sources: Reuters · BBC · Al Jazeera · The Guardian · AP · France 24 · CNBC · One Turn daily digest",
       font=f(SANS, 11), fill=GREY, anchor="ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print(out, os.path.getsize(out), img.size)
