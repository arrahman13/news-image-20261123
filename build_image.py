#!/usr/bin/env python3
"""Render the news-image-20261123 broadsheet (1024x1024 PNG).

Fresh build for Monday 23 November 2026. All art is drawn in code with
Pillow; no photos, no downloads, no network. Deterministic output:
fixed fonts, fixed layout, no timestamps, no randomness.
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SERIF_R = lambda s: font("DejaVuSerif.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

INK = (18, 18, 18)
PAPER = (250, 247, 238)
RED = (178, 24, 24)
DARK = (16, 32, 54)
MAPBG = (10, 31, 51)
LAND = (38, 90, 130)
GRID = (24, 58, 88)
MUTED = (90, 90, 90)

LEADS = [
    (1, "NVIDIA BRINGS HUANG BACK",
     "Board reinstates Jensen Huang as CEO, 11 days after he resigned; shares jump ~33%, S&P 500 +4.82%.",
     "AP · BBC · CNBC", "REPORTED", (30, 90, 140)),
    (2, "UKRAINE SINKS RUSSIAN SHIP OFF LIBYA",
     "Zelensky: seven naval drones sank corvette Merkury at Benghazi port; a cargo ship also hit.",
     "AP · BBC · THE GUARDIAN", "REPORTED", (20, 70, 110)),
    (3, "IRAN VOWS TO FIGHT US BLOCKADE",
     "Tehran: \u201call available means\u201d against the US naval blockade; US sanctions dozens in shadow-banking networks.",
     "REUTERS · AL JAZEERA", "REPORTED", (120, 60, 50)),
]

CARDS = [
    (4, "COP31 AFTERMATH", "EU \u201cdisappointed\u201d by the collapse, urges talks on; Erdogan: summit laid groundwork.", "REUTERS", "REPORTED"),
    (5, "EU'S 22nd SANCTIONS", "Commission proposes curbs on 60 banks, crypto platforms, 70 shadow-fleet ships.", "REUTERS · AP", "REPORTED"),
    (6, "RUSSIA WARNS ESTONIA", "Moscow: border closure \u201con the verge of open war\u201d; Finland summons envoy.", "REUTERS", "REPORTED"),
    (7, "KYIV TOLL RISES", "Russian strikes kill at least 15 around Kyiv; Dymer block toll reaches 11.", "REUTERS", "REPORTED"),
    (8, "CIKANDE FIRE TOLL 24", "Indonesian sweets-factory blaze: 24 dead, ~30 missing; rescuers hunt 34 missing workers.", "THE GUARDIAN · BBC · AP", "REPORTED"),
    (9, "DEMOCRATS TAKE HOUSE", "At least 258 seats, largest House majority since 1992.", "AP", "REPORTED"),
    (10, "FBI PROBES DATABASE HACK", "Apparent hack of the national crime database NCIC under investigation.", "AP", "REPORTED"),
    (11, "TRUMP CURBS CONGRESS", "Executive order limits how Congress seeks information from agencies.", "AP", "REPORTED"),
    (12, "SENATE PASSES PERMIT BILL", "Faster reviews; data centres must pay their energy costs.", "AP", "REPORTED"),
    (13, "CROWDSTRIKE BUYS ZSCALER", "$44bn deal to build a cybersecurity giant.", "AP", "REPORTED"),
    (14, "2031 WORLD CUP", "FIFA: USA, Mexico, Costa Rica, Jamaica host 2031 (48 teams); UK hosts 2035.", "REUTERS · AP", "REPORTED"),
    (15, "PENGE WINS RSM CLASSIC", "First PGA Tour title in a four-way playoff; birdied the 18th all four rounds.", "AP", "REPORTED"),
    (16, "IRAN FLOGS SINGER", "Parastoo Ahmadi gets 74 lashes over a 2024 hijab-free video; bandmates also flogged.", "REUTERS", "REPORTED"),
]

BRIEFS = [
    (17, "Zelenskiy: intel shows Russia planning new strikes; pleads for air defences.", "REUTERS", "CLAIM"),
    (18, "UK: SpaceX curbs in Ukraine \u201cdented confidence and trust\u201d.", "REUTERS", "REPORTED"),
    (19, "Germany to adopt Kyiv's Delta battlefield-analysis tool.", "REUTERS", "REPORTED"),
    (20, "Hungary's PM Magyar to visit Transcarpathia \u201csoon\u201d.", "REUTERS", "REPORTED"),
    (21, "Russian drone briefly violated Polish airspace in an overnight attack.", "REUTERS", "REPORTED"),
    (22, "US probes Iran as possible culprit in dozens of cyberattacks on tankers.", "WSJ VIA REUTERS", "CLAIM"),
    (23, "Khartoum drones hit homes and a UN building; army blames RSF, says drones came from Ethiopia.", "FRANCE 24 · AL JAZEERA", "CLAIM"),
    (24, "Gaza contamination threatens health for generations \u2014 Oxfam/Ceobs report, 99% of strip toxic.", "THE GUARDIAN · AL JAZEERA", "REPORTED"),
    (25, "Herzog and Eisenkot condemn West Bank settler arson; \u201cJewish terrorism\u201d.", "THE GUARDIAN · FRANCE 24", "REPORTED"),
    (26, "India pledges \u20ac1.4bn to help Nepal rebuild after August floods.", "DAILY SUMMARY OF WORLD", "REPORTED"),
    (27, "Euro-area inflation rises to 4.0%, Eurostat reports.", "EUROSTAT", "REPORTED"),
    (28, "NHS starts AI trial in breast-cancer screening.", "BBC NEWS", "REPORTED"),
    (29, "Anthropic says AI helped prove the Riemann hypothesis; mathematicians debate it.", "ANTHROPIC", "CLAIM"),
    (30, "China sentences an official to death for spying and leaking secrets.", "AP", "REPORTED"),
    (31, "South Korea: several Russian aircraft entered its air-defence zone.", "AP", "REPORTED"),
    (32, "Houston leaps to No. 1 in AP Top 25 men's basketball poll.", "AP", "REPORTED"),
    (33, "49ers release Brandon Aiyuk, ending contract saga.", "AP", "REPORTED"),
    (34, "TCU fires football coach Sonny Dykes, four years after CFP final.", "AP", "REPORTED"),
    (35, "House Ethics: \u201csubstantial evidence\u201d Rep. Jimmy Gomez engaged in sexual misconduct.", "AP", "REPORTED"),
]

TIMELINE = [
    ("00:00", "Khartoum drones strike"),
    ("09:00", "EU proposes 22nd sanctions"),
    ("12:00", "FIFA confirms 2031/2035 hosts"),
    ("15:00", "Nvidia board reinstates Huang"),
    ("17:00", "Zelensky confirms Libya strike"),
    ("19:00", "US sanctions Iran shadow banks"),
    ("21:00", "S&P 500 closes +4.82%"),
]

# lon, lat, pixel jitter (dx, dy) to separate clustered pins
PINS = {
    1: (-100, 39, -8, -8), 2: (20, 32, -14, 10), 3: (56, 26, 0, 0),
    4: (33, 39, 0, 0), 5: (4, 50, 0, -18), 6: (25, 59, 6, -18),
    7: (30, 50, -16, 4), 8: (106, -6, 0, 0), 9: (-77, 39, -26, -18),
    10: (-77, 39, 16, 12), 11: (-77, 39, -16, 20), 12: (-77, 39, 18, -14),
    13: (-95, 37, 4, -18), 14: (-100, 25, -14, 8), 15: (-81, 31, 10, -4),
    16: (51, 35, -10, -12), 17: (30, 50, -24, -6), 18: (0, 51, -20, -6),
    19: (13, 52, 12, -16), 20: (23, 48, 4, 16), 21: (19, 52, 20, 2),
    22: (54, 26, 22, 14), 23: (32, 15, 0, 0), 24: (34, 31, -12, 14),
    25: (35, 32, 16, -14), 26: (85, 28, 0, 0), 27: (4, 50, 18, 14),
    28: (0, 51, -8, 16), 29: (10, 45, -16, 10), 30: (116, 40, 0, 0),
    31: (127, 37, 0, 0), 32: (-95, 30, -8, 12), 33: (-122, 37, 0, 0),
    34: (-97, 32, -16, 2), 35: (-77, 39, 8, 26),
}

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-85, 70), (-75, 62), (-60, 55), (-55, 47), (-65, 45), (-75, 40), (-80, 32), (-85, 25), (-90, 20), (-97, 16), (-105, 20), (-110, 23), (-117, 32), (-125, 40), (-125, 48), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 0), (-60, -5), (-50, -5), (-40, -10), (-35, -20), (-40, -30), (-50, -35), (-60, -40), (-70, -45), (-70, -55), (-75, -40), (-75, -20), (-80, -10)],
    [(-10, 36), (-5, 37), (0, 38), (5, 38), (10, 40), (15, 44), (20, 45), (25, 40), (28, 41), (30, 36), (35, 36), (30, 42), (28, 45), (23, 48), (20, 50), (15, 55), (10, 57), (5, 58), (0, 60), (-5, 58), (-10, 55), (-10, 45), (-10, 38)],
    [(-17, 15), (-15, 25), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 20), (43, 12), (48, 10), (51, 10), (45, 0), (40, -10), (35, -20), (30, -30), (25, -35), (18, -35), (15, -25), (12, -15), (13, -5), (10, 5), (0, 5), (-8, 5), (-15, 10)],
    [(35, 36), (40, 40), (45, 40), (50, 45), (55, 50), (60, 55), (70, 60), (75, 70), (85, 75), (100, 75), (110, 75), (130, 72), (150, 70), (170, 67), (178, 65), (170, 60), (160, 55), (150, 50), (140, 45), (135, 40), (127, 35), (122, 30), (115, 22), (108, 15), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 10), (77, 8), (72, 20), (65, 25), (60, 25), (55, 26), (50, 28), (45, 25), (40, 20), (38, 18), (35, 28)],
    [(113, -22), (120, -15), (130, -12), (140, -17), (145, -15), (150, -22), (153, -28), (150, -35), (140, -38), (130, -32), (120, -35), (113, -30)],
]

def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(draw, x, y, tag):
    colors = {"REPORTED": (20, 110, 60), "CLAIM": (176, 110, 10), "FORECAST": (40, 80, 160)}
    c = colors.get(tag, (90, 90, 90))
    f = F_SANS_B(8)
    w = int(draw.textlength(tag, font=f)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=6, fill=c)
    draw.text((x + 5, y + 2), tag, font=f, fill=(255, 255, 255))
    return w

def draw_map(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=MAPBG)
    for gx in range(0, w + 1, 64):
        draw.line([(x0 + gx, y0), (x0 + gx, y0 + h)], fill=GRID, width=1)
    for gy in range(0, h + 1, 36):
        draw.line([(x0, y0 + gy), (x0 + w, y0 + gy)], fill=GRID, width=1)
    def proj(lon, lat):
        return (x0 + (lon + 180) / 360.0 * w, y0 + (90 - lat) / 180.0 * h)
    for poly in CONTINENTS:
        draw.polygon([proj(lo, la) for lo, la in poly], fill=LAND, outline=(70, 130, 175))
    draw.text((x0 + 8, y0 + 6), "THE WORLD, PINNED  \u2014  35 STORIES, ONE DAY",
              font=F_SANS_B(11), fill=(255, 255, 255))
    for n, (lon, lat, dx, dy) in sorted(PINS.items()):
        px, py = proj(lon, lat)
        px, py = px + dx, py + dy
        big = n <= 16
        r = 9 if big else 7
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED if n <= 3 else (255, 255, 255),
                     outline=(120, 10, 10), width=2)
        f = F_SANS_B(9 if big else 8)
        tw = draw.textlength(str(n), font=f)
        draw.text((px - tw / 2, py - 6 if big else py - 5), str(n), font=f,
                  fill=(255, 255, 255) if n <= 3 else (178, 24, 24))

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    # --- masthead ---
    d.text((M, 8), "MONDAY 23 NOVEMBER 2026", font=F_SERIF(40), fill=INK)
    d.text((M, 56), "T H E   W O R L D   I N   O N E   D A Y", font=F_SANS_B(17), fill=RED)
    d.text((W - M - 210, 14), "35 STORIES \u00b7 1 DAY", font=F_SANS_B(13), fill=INK)
    d.text((W - M - 210, 34), "ALL DATED MONDAY 23 NOV 2026", font=F_SANS(10), fill=MUTED)
    d.text((W - M - 210, 50), "SOURCES NAMED ON EVERY STORY", font=F_SANS(10), fill=MUTED)
    d.line([(M, 82), (W - M, 82)], fill=INK, width=2)
    # --- stat strip ---
    stats = "S&P +4.82%   \u00b7   NVIDIA +33%   \u00b7   NIKKEI \u22125%   \u00b7   EURO INFLATION 4.0%   \u00b7   HOUSE 258 SEATS   \u00b7   KYIV 15 KILLED   \u00b7   CIKANDE 24 DEAD"
    d.rectangle([M, 90, W - M, 114], fill=(18, 18, 18))
    tw = d.textlength(stats, font=F_SANS_B(11))
    d.text(((W - tw) / 2, 97), stats, font=F_SANS_B(11), fill=(255, 255, 255))
    # --- UTC timeline ---
    d.text((M, 120), "UTC TIMELINE", font=F_SANS_B(10), fill=RED)
    d.line([(M, 136), (W - M, 136)], fill=(200, 200, 200), width=1)
    seg = (W - 2 * M) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = M + seg * i + seg / 2
        d.ellipse([cx - 4, 132, cx + 4, 140], fill=RED)
        d.text((cx - d.textlength(t, font=F_SANS_B(9)) / 2, 142), t, font=F_SANS_B(9), fill=INK)
        lines = wrap(d, label, F_SANS(8), seg - 8)
        for j, ln in enumerate(lines[:2]):
            d.text((cx - d.textlength(ln, font=F_SANS(8)) / 2, 154 + j * 10), ln, font=F_SANS(8), fill=MUTED)
    # --- region tally + legend ---
    tally = "EUROPE 10  \u00b7  AMERICAS 11  \u00b7  MIDDLE EAST 5  \u00b7  ASIA-PACIFIC 4  \u00b7  AFRICA 2  \u00b7  WORLD 3  =  35 STORIES"
    d.text((M, 178), tally, font=F_SANS_B(11), fill=INK)
    lx = M + int(d.textlength(tally, font=F_SANS_B(11))) + 16
    d.text((lx, 178), "LEGEND:", font=F_SANS_B(10), fill=INK)
    lx += 54
    for tag in ("REPORTED", "CLAIM", "FORECAST"):
        lx += chip(d, lx, 177, tag) + 6
    d.line([(M, 196), (W - M, 196)], fill=INK, width=1)
    # --- leads: 3 columns ---
    lw = (W - 2 * M - 2 * 12) // 3
    ly = 204
    lh = 168
    for i, (n, head, body, outlet, tag, col) in enumerate(LEADS):
        x = M + i * (lw + 12)
        d.rectangle([x, ly, x + lw, ly + 62], fill=col)
        # simple illustration: bars / waves / blockade
        if i == 0:
            base = ly + 52
            for j, bh in enumerate((14, 24, 18, 34, 44)):
                d.rectangle([x + 16 + j * 22, base - bh, x + 30 + j * 22, base], fill=(255, 255, 255))
            d.line([(x + 10, base - 46), (x + lw - 12, base - 52)], fill=(255, 210, 60), width=3)
        elif i == 1:
            d.polygon([(x + 60, ly + 44), (x + 150, ly + 44), (x + 165, ly + 20), (x + 45, ly + 20)], fill=(255, 255, 255))
            d.rectangle([x + 95, ly + 8, x + 100, ly + 20], fill=(255, 255, 255))
            for j in range(4):
                d.arc([x + 20 + j * 55, ly + 46, x + 60 + j * 55, ly + 60], 0, 180, fill=(255, 255, 255), width=2)
        else:
            for j in range(3):
                d.rectangle([x + 30 + j * 70, ly + 26, x + 70 + j * 70, ly + 44], fill=(255, 255, 255))
                d.rectangle([x + 44 + j * 70, ly + 12, x + 48 + j * 70, ly + 26], fill=(255, 255, 255))
            d.line([(x + 12, ly + 50), (x + lw - 12, ly + 50)], fill=(255, 210, 60), width=2)
        d.rectangle([x, ly + 62, x + lw, ly + 84], fill=RED)
        d.text((x + 8, ly + 67), "LEAD %d" % n, font=F_SANS_B(12), fill=(255, 255, 255))
        # headline wrapped to 2 lines max
        hl = wrap(d, head, F_SERIF(14), lw - 16)
        for j, ln in enumerate(hl[:2]):
            d.text((x + 8, ly + 90 + j * 17), ln, font=F_SERIF(14), fill=INK)
        by = ly + 90 + len(hl[:2]) * 17 + 2
        bl = wrap(d, body, F_SANS(10), lw - 16)
        for j, ln in enumerate(bl[:2]):
            d.text((x + 8, by + j * 12), ln, font=F_SANS(10), fill=(50, 50, 50))
        ty = ly + lh - 16
        chip(d, x + 8, ty, tag)
        d.text((x + 78, ty + 2), outlet, font=F_SANS(8), fill=MUTED)
        d.rectangle([x, ly, x + lw, ly + lh], outline=(180, 180, 180), width=1)
    # --- cards: 13 in a 4-col grid (rows of 4, 4, 4, 1 + filler) ---
    cy = ly + lh + 10
    cw = (W - 2 * M - 3 * 10) // 4
    ch = 56
    for idx, (n, head, body, outlet, tag) in enumerate(CARDS):
        r, c = divmod(idx, 4)
        x = M + c * (cw + 10)
        y = cy + r * (ch + 6)
        d.rectangle([x, y, x + cw, y + ch], fill=(255, 255, 255), outline=(190, 190, 190))
        d.rectangle([x, y, x + 5, y + ch], fill=RED)
        d.text((x + 10, y + 4), "%d. %s" % (n, head), font=F_SANS_B(10), fill=INK)
        bl = wrap(d, body, F_SANS(9), cw - 16)
        for j, ln in enumerate(bl[:2]):
            d.text((x + 10, y + 19 + j * 11), ln, font=F_SANS(9), fill=(60, 60, 60))
        chip(d, x + 10, y + ch - 16, tag)
        d.text((x + 82, y + ch - 14), outlet, font=F_SANS(7), fill=MUTED)
    # filler cell in last row: tally reminder
    fx = M + 1 * (cw + 10)
    fy = cy + 3 * (ch + 6)
    d.rectangle([fx, fy, fx + cw, fy + ch], fill=(240, 236, 224), outline=(190, 190, 190))
    d.text((fx + 10, fy + 8), "13 CARDS + 3 LEADS", font=F_SANS_B(10), fill=INK)
    d.text((fx + 10, fy + 24), "+ 19 BRIEFS = 35 STORIES", font=F_SANS_B(10), fill=INK)
    d.text((fx + 10, fy + 40), "Every story dated 23 Nov 2026.", font=F_SANS(9), fill=MUTED)
    # --- map ---
    my = cy + 4 * ch + 3 * 6 + 10
    mh = 132
    draw_map(d, M, my, W - 2 * M, mh)
    # --- briefs ---
    by = my + mh + 8
    d.text((M, by), "IN BRIEF \u2014 19 MORE STORIES FROM MONDAY 23 NOVEMBER 2026", font=F_SANS_B(11), fill=RED)
    by += 16
    chip_x = W - M - 210
    for n, text, outlet, tag in BRIEFS:
        d.text((M, by), "%d." % n, font=F_SANS_B(9), fill=INK)
        # fixed columns: text | chip | outlet, so nothing can overlap
        max_tw = chip_x - (M + 24) - 8
        while d.textlength(text, font=F_SANS(9)) > max_tw and len(text) > 4:
            text = text[:-4].rstrip() + "\u2026"
        d.text((M + 24, by), text, font=F_SANS(9), fill=INK)
        chip(d, chip_x, by - 1, tag)
        ow = d.textlength(outlet, font=F_SANS(8))
        d.text((W - M - ow, by), outlet, font=F_SANS(8), fill=MUTED)
        by += 10
    # --- date-check box ---
    dy = by + 4
    d.rectangle([M, dy, W - M, 1020], fill=(245, 240, 225), outline=RED, width=1)
    d.text((M + 8, dy + 4), "DATE-CHECK \u2014 LEFT OUT ON PURPOSE (NOT 23 NOVEMBER):",
           font=F_SANS_B(9), fill=RED)
    left = ("COP31 collapse itself (Sun 22 Nov \u2014 Mon aftermath is the story)  \u00b7  Skubal's $450m Mets deal agreed Sun  \u00b7  "
            "Miley Cyrus wedding Sat  \u00b7  \u201cEl Chapo Isidro\u201d captured Fri night  \u00b7  Amtrak derailment Sun evening  \u00b7  "
            "BepiColombo Mercury orbit Sun  \u00b7  Alcaraz ATP Finals title Sun  \u00b7  Merkury strike itself Sun (Zelensky's Mon confirmation is the story)  \u00b7  "
            "Dymer strike Sun night (Mon toll update is the story).")
    lines = wrap(d, left, F_SANS(8), W - 2 * M - 16)
    for j, ln in enumerate(lines[:2]):
        d.text((M + 8, dy + 16 + j * 10), ln, font=F_SANS(8), fill=(60, 60, 60))
    img.save(OUT, optimize=True)
    data = open(OUT, "rb").read()
    print("wrote", OUT, len(data), "bytes sha256", hashlib.sha256(data).hexdigest())

if __name__ == "__main__":
    main()
