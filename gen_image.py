#!/usr/bin/env python3
"""Draw the 26 November 2026 front page (1024x1024 PNG) with Pillow.

Layout: masthead with the date, a lead banner with a hand-drawn scene of the
Ras Tanura refinery burning over the Gulf, six story cards, and a footer
ticker of briefs. Deterministic: no randomness, no timestamps, no network.
Re-running this script reproduces the identical PNG bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, max_w, text, fnt, fill, leading=None):
    """Draw wrapped text; return the y just below the last line."""
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), (247, 243, 234))  # newsprint cream
    d = ImageDraw.Draw(img)
    ink = (18, 18, 18)
    red = (178, 34, 28)
    navy = (24, 52, 96)
    grey = (90, 88, 82)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 96], fill=navy)
    d.text((512, 14), "THE WORLD TODAY", font=font(SERIF_B, 58),
           fill=(255, 255, 255), anchor="ma")
    d.text((512, 74), "THURSDAY, 26 NOVEMBER 2026  •  ONE DAY, ONE PAGE",
           font=font(SANS_B, 17), fill=(214, 222, 235), anchor="ma")
    d.line([24, 104, W - 24, 104], fill=red, width=4)

    # ---- lead story ----------------------------------------------------
    d.text((24, 118), "THE GULF BURNS",
           font=font(SERIF_B, 46), fill=red)
    d.text((24, 168), "Houthis hit Saudi refinery as crisis deepens",
           font=font(SERIF_B, 25), fill=ink)

    # Scene: dusk sky, sea, refinery towers, flames and smoke.
    sx, sy, sw, sh = 24, 204, 976, 190
    d.rectangle([sx, sy, sx + sw, sy + sh], fill=(42, 58, 86))  # dusk sky
    d.rectangle([sx, sy + 118, sx + sw, sy + sh], fill=(28, 74, 96))  # sea
    # sun low on the horizon
    d.ellipse([sx + 700, sy + 88, sx + 764, sy + 152], fill=(240, 150, 60))
    # refinery towers and tanks on the shore
    d.rectangle([sx + 60, sy + 62, sx + 88, sy + 118], fill=(30, 30, 34))
    d.rectangle([sx + 110, sy + 48, sx + 138, sy + 118], fill=(30, 30, 34))
    d.rectangle([sx + 160, sy + 78, sx + 196, sy + 118], fill=(30, 30, 34))
    d.rectangle([sx + 300, sy + 88, sx + 420, sy + 118], fill=(52, 52, 56))
    d.rectangle([sx + 470, sy + 96, sx + 560, sy + 118], fill=(52, 52, 56))
    d.rectangle([sx + 620, sy + 82, sx + 660, sy + 118], fill=(30, 30, 34))
    # flare stack with flame
    d.rectangle([sx + 880, sy + 30, sx + 892, sy + 118], fill=(30, 30, 34))
    d.polygon([(sx + 872, sy + 32), (sx + 886, sy + 2), (sx + 900, sy + 32)],
              fill=(255, 120, 20))
    # flames over the refinery
    for fx, fw, fh in [(70, 34, 46), (118, 40, 58), (330, 60, 44),
                       (480, 46, 36), (630, 30, 40)]:
        d.polygon([(sx + fx, sy + 92), (sx + fx + fw // 2, sy + 92 - fh),
                   (sx + fx + fw, sy + 92)], fill=(255, 120, 20))
        d.polygon([(sx + fx + 6, sy + 92), (sx + fx + fw // 2, sy + 92 - fh + 16),
                   (sx + fx + fw - 6, sy + 92)], fill=(255, 200, 60))
    # smoke columns
    for cx, cy, r in [(140, 40, 26), (170, 24, 30), (360, 46, 28),
                      (500, 52, 24), (700, 30, 30)]:
        d.ellipse([sx + cx - r, sy + cy - r, sx + cx + r, sy + cy + r],
                  fill=(120, 118, 112))
    # oil tanker on the sea
    d.rectangle([sx + 690, sy + 140, sx + 920, sy + 168], fill=(20, 20, 24))
    d.rectangle([sx + 700, sy + 128, sx + 740, sy + 140], fill=(20, 20, 24))
    d.rectangle([sx + 880, sy + 122, sx + 892, sy + 140], fill=(20, 20, 24))
    d.line([sx + 700, sy + 176, sx + 940, sy + 176], fill=(120, 160, 180), width=2)
    d.text((sx + 8, sy + sh - 26), "RAS TANURA, SAUDI ARABIA",
           font=font(SANS_B, 14), fill=(255, 255, 255))

    lead_body = (
        "Houthi forces say they struck the Ras Tanura oil refinery and two "
        "Saudi ports in retaliatory strikes, a day after two tankers hit "
        "naval mines in the Strait of Hormuz. India condemned the attack "
        "after two Indians were hurt in Riyadh."
    )
    draw_text_block(d, 24, 406, 976, lead_body, font(SERIF, 20), ink)

    # ---- story cards ---------------------------------------------------
    cards = [
        ("GAZA CEASEFIRE STRAINS",
         "Israel strikes a senior Hamas official in Gaza as the fragile "
         "ceasefire comes under strain."),
        ("PUTIN VOWS REVENGE",
         "Ukraine hits Russian oil refineries; Putin vows retaliation. "
         "Russia's own figures show nearly 500,000 lost in the war."),
        ("PACIFIC PACT",
         "Solomon Islands and Australia sign a historic security treaty, "
         "deepening ties across the Pacific."),
        ("FIRST PAKISTANI IN SPACE",
         "Pakistan's first astronaut joins China's Shenzhou-24 mission to "
         "the Tiangong space station."),
        ("MUMBAI REMEMBERS 26/11",
         "India marks 18 years since the Mumbai attacks, on Constitution "
         "Day. North Korea expels a Swiss diplomat."),
        ("HOSTAGES FREED IN COLOMBIA",
         "Police storm a supermarket and free 20 people held hostage for "
         "17 hours. A Cairo fuel-tanker fire kills at least 30."),
    ]
    cw, chh = 476, 128
    x0, y0 = 24, 500
    for i, (title, body) in enumerate(cards):
        cx = x0 + (i % 2) * (cw + 24)
        cy = y0 + (i // 2) * (chh + 14)
        d.rectangle([cx, cy, cx + cw, cy + chh], outline=(150, 146, 138), width=2)
        d.rectangle([cx, cy, cx + 8, cy + chh], fill=red)
        d.text((cx + 20, cy + 10), title, font=font(SANS_B, 20), fill=navy)
        draw_text_block(d, cx + 20, cy + 40, cw - 36, body,
                        font(SANS, 16), ink, leading=21)

    # ---- footer ticker -------------------------------------------------
    fy = 500 + 3 * chh + 2 * 14 + 16
    d.line([24, fy, W - 24, fy], fill=red, width=3)
    d.text((24, fy + 10), "ALSO TODAY", font=font(SANS_B, 18), fill=red)
    briefs = (
        "US stocks tumble as Nvidia paces an AI sell-off  •  "
        "Vaibhav Sooryavanshi, 15, smashes the fastest List A double "
        "century — 204 off 53 balls  •  Gukesh draws game 2 of the World "
        "Chess Championship  •  Duran Duran guitarist Andy Taylor dies "
        "at 65  •  Asteroid-defence test images reveal a new crater  •  "
        "Six die in a plane crash off the Mississippi coast"
    )
    draw_text_block(d, 24, fy + 36, 976, briefs, font(SANS, 16), grey, leading=22)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
