"""Draw the Connecticut banner and Dock icon artwork (assets/ct-banner.png, assets/ct-icon.png).

Run on macOS (uses system fonts): python scripts/draw_ct_artwork.py
The PNGs are committed; this script only regenerates them.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path('/System/Library/Fonts/Supplemental')
NAVY_TOP, NAVY_LOW = (4, 10, 26), (14, 34, 70)
GOLD, RED, WHITE = (232, 185, 49), (196, 40, 32), (244, 241, 234)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def gradient(size, top, bottom):
    width, height = size
    image = Image.new('RGB', size)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        t = y / max(1, height - 1)
        draw.line((0, y, width, y), fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    return image


def stars(draw, box, count, seed):
    rng = random.Random(seed)
    left, top, right, bottom = box
    for _ in range(count):
        x, y = rng.uniform(left, right), rng.uniform(top, bottom)
        r = rng.choice((1, 1, 1, 2, 2, 3))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 250, 225))


def lighthouse(draw, base_x, base_y, height):
    """Red-and-white striped shoreline lighthouse standing on rocks."""
    bottom_w, top_w = height * .22, height * .13
    top_y = base_y - height
    bands = 6
    for band in range(bands):
        y0 = top_y + height * band / bands
        y1 = top_y + height * (band + 1) / bands
        w0 = top_w + (bottom_w - top_w) * band / bands
        w1 = top_w + (bottom_w - top_w) * (band + 1) / bands
        draw.polygon([(base_x - w0 / 2, y0), (base_x + w0 / 2, y0),
                      (base_x + w1 / 2, y1), (base_x - w1 / 2, y1)],
                     fill=RED if band % 2 == 0 else WHITE)
    gallery = top_y - height * .03
    draw.rectangle((base_x - top_w * .75, gallery, base_x + top_w * .75, top_y), fill=(30, 30, 36))
    lamp_top = gallery - height * .14
    draw.rectangle((base_x - top_w * .42, lamp_top, base_x + top_w * .42, gallery), fill=(255, 226, 120))
    draw.polygon([(base_x - top_w * .55, lamp_top), (base_x + top_w * .55, lamp_top),
                  (base_x, lamp_top - height * .09)], fill=(30, 30, 36))
    rocks = [(base_x - bottom_w * 1.6, base_y + height * .06), (base_x - bottom_w * .9, base_y - height * .03),
             (base_x - bottom_w * .2, base_y + height * .01), (base_x + bottom_w * .6, base_y - height * .04),
             (base_x + bottom_w * 1.7, base_y + height * .06)]
    draw.polygon(rocks, fill=(12, 16, 24))
    return base_x, (lamp_top + gallery) / 2


def beam(image, origin, length, spread, angles):
    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x, y = origin
    for angle in angles:
        a = math.radians(angle)
        tip = [(x + math.cos(a + s) * length, y + math.sin(a + s) * length) for s in (-spread, spread)]
        draw.polygon([(x, y), *tip], fill=(255, 230, 140, 70))
    layer = layer.filter(ImageFilter.GaussianBlur(length / 60))
    return Image.alpha_composite(image.convert('RGBA'), layer)


def water(draw, box, seed, reflection_x=None):
    rng = random.Random(seed)
    left, top, right, bottom = box
    draw.rectangle(box, fill=(6, 18, 40))
    for row in range(40):
        y = top + (bottom - top) * row / 40
        for _ in range(18):
            x = rng.uniform(left, right)
            w = rng.uniform(15, 60) * (1 + row / 20)
            draw.line((x, y, x + w, y), fill=(40, 70, 120), width=2)
    if reflection_x is not None:
        for row in range(30):
            y = top + (bottom - top) * row / 30
            w = 20 + row * 6
            draw.line((reflection_x - w / 2 + rng.uniform(-10, 10), y,
                       reflection_x + w / 2 + rng.uniform(-10, 10), y), fill=(200, 165, 70), width=3)


def oak(draw, x, ground, size):
    """Charter Oak silhouette."""
    draw.polygon([(x - size * .08, ground), (x - size * .04, ground - size * .45),
                  (x + size * .04, ground - size * .45), (x + size * .1, ground)], fill=(8, 14, 22))
    rng = random.Random(1687)
    for _ in range(26):
        cx = x + rng.uniform(-size * .45, size * .45)
        cy = ground - size * .55 + rng.uniform(-size * .25, size * .15)
        r = rng.uniform(size * .12, size * .22)
        draw.ellipse((cx - r, cy - r * .8, cx + r, cy + r * .8), fill=(8, 14, 22))


def banner():
    size = (2172, 724)
    image = gradient(size, NAVY_TOP, NAVY_LOW)
    draw = ImageDraw.Draw(image)
    stars(draw, (0, 0, size[0], 470), 260, 78)
    draw.ellipse((1640, 70, 1740, 170), fill=(250, 240, 205))
    horizon = 520
    water(draw, (0, horizon, size[0], size[1]), 2011, reflection_x=1690)
    oak(draw, 1450, horizon + 6, 300)
    draw.rectangle((0, horizon - 8, size[0], horizon + 4), fill=(10, 16, 26))
    origin = lighthouse(draw, 1900, horizon + 40, 360)
    image = beam(image, origin, 900, .05, (190, 205)).convert('RGB')
    draw = ImageDraw.Draw(image)
    panel = Image.new('RGBA', size, (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle((40, 40, 1230, 684), 28, fill=(4, 10, 24, 215))
    image = Image.alpha_composite(image.convert('RGBA'), panel).convert('RGB')
    draw = ImageDraw.Draw(image)
    draw.text((90, 78), 'THE', font=font('Futura.ttc', 64), fill=WHITE)
    title = font('Impact.ttf', 250)
    draw.text((84, 140), 'PACKY', font=title, fill=GOLD)
    width = draw.textlength('PACKY ', font=title)
    draw.text((84 + width, 140), 'BBS', font=title, fill=RED)
    draw.text((92, 470), 'NUTMEG STATE  •  COMMUNICATIONS DIVISION',
              font=font('Futura.ttc', 44), fill=WHITE)
    draw.text((92, 560), 'Take a left where the old Ames used to be.',
              font=font('AmericanTypewriter.ttc', 38), fill=GOLD)
    image.save(ROOT / 'assets' / 'ct-banner.png', optimize=True)


def icon():
    side = 1254
    tile = gradient((side, side), NAVY_TOP, NAVY_LOW).convert('RGBA')
    draw = ImageDraw.Draw(tile)
    stars(draw, (80, 80, side - 80, 640), 90, 1978)
    water(draw, (0, 760, side, side), 95, reflection_x=None)
    origin = lighthouse(draw, side * .5, 800, 520)
    tile = beam(tile, origin, 760, .06, (195, 345))
    draw = ImageDraw.Draw(tile)
    band = Image.new('RGBA', tile.size, (0, 0, 0, 0))
    ImageDraw.Draw(band).rectangle((0, 850, side, 1120), fill=(4, 10, 24, 220))
    tile = Image.alpha_composite(tile, band)
    draw = ImageDraw.Draw(tile)
    title = font('Impact.ttf', 230)
    text = 'PACKY'
    draw.text(((side - draw.textlength(text, font=title)) / 2, 840), text, font=title, fill=GOLD)
    small = font('Futura.ttc', 70)
    draw.text(((side - draw.textlength('BBS  •  CT', font=small)) / 2, 1110), 'BBS  •  CT', font=small, fill=WHITE)
    mask = Image.new('L', tile.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((40, 40, side - 40, side - 40), 230, fill=255)
    ImageDraw.Draw(tile).rounded_rectangle((40, 40, side - 40, side - 40), 230, outline=GOLD, width=14)
    result = Image.new('RGBA', tile.size, (0, 0, 0, 0))
    result.paste(tile, mask=mask)
    result.save(ROOT / 'assets' / 'ct-icon.png', optimize=True)


if __name__ == '__main__':
    banner()
    icon()
