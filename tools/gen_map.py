"""Render the briefing map (docs/carte.jpg + the DCS briefing picture) on a real basemap.

Data: briefing_data.json (from gather.py, DCS x/y). Basemap: OpenStreetMap standard raster tiles, Web Mercator. Tiles are cached next to this script (tiles/), so the map
can be re-rendered offline once fetched.
"""

import json
import math
import os

import requests
from PIL import Image, ImageDraw, ImageFont

from paths import ROOT as _ROOT  # noqa: E402  (also puts VMCT on sys.path)
from veaf_libs import coordinates as C  # noqa: E402

S = os.path.dirname(os.path.abspath(__file__))
ROOT = str(_ROOT)
D = json.load(open(os.path.join(S, "briefing_data.json"), encoding="utf-8"))

# ── geography ──────────────────────────────────────────────────────────────────────────────
ZOOM = 9
TILE = 256
TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
UA = {"User-Agent": "veaf-briefing-map/1.0 (+https://github.com/VEAF/VEAF-Mission-Creation-Tools)"}  # jamais de donnée personnelle
# window in lat/lon (checked against the mission: every drawn object falls inside)
LAT_N, LAT_S, LON_W, LON_E = 54.8, 49.0, 6.0, 14.95
OUT_W = 2000  # output width in px; height follows


def ll(x, y):
    return C.xy_to_latlon("GermanyCW", x, y)


def merc(lat, lon):
    """Web Mercator tile-space coordinates (in tiles) at ZOOM."""
    n = 2 ** ZOOM
    xt = (lon + 180) / 360 * n
    yt = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return xt, yt


X0, Y0 = merc(LAT_N, LON_W)
X1, Y1 = merc(LAT_S, LON_E)
SCALE = OUT_W / ((X1 - X0) * TILE)  # output px per tile px
OUT_H = round((Y1 - Y0) * TILE * SCALE)


def px(x, y):
    """DCS x (north) / y (east) → output pixel."""
    xt, yt = merc(*ll(x, y))
    return ((xt - X0) * TILE * SCALE, (yt - Y0) * TILE * SCALE)


def px_per_m(x, y):
    """Local scale at a DCS point (Mercator stretches with latitude)."""
    lat, _ = ll(x, y)
    m_per_tilepx = 156543.03 * math.cos(math.radians(lat)) / (2 ** ZOOM) * 256 / TILE
    return SCALE / m_per_tilepx


# ── basemap ────────────────────────────────────────────────────────────────────────────────
def basemap():
    cache = os.path.join(S, "tiles")
    os.makedirs(cache, exist_ok=True)
    tx0, ty0, tx1, ty1 = int(X0), int(Y0), int(X1), int(Y1)
    sheet = Image.new("RGB", ((tx1 - tx0 + 1) * TILE, (ty1 - ty0 + 1) * TILE), "#f4f6f2")
    sess = requests.Session()
    for i, tx in enumerate(range(tx0, tx1 + 1)):
        for j, ty in enumerate(range(ty0, ty1 + 1)):
            f = os.path.join(cache, f"{ZOOM}_{tx}_{ty}.png")
            if not os.path.exists(f):
                url = TILE_URL.format(z=ZOOM, x=tx, y=ty)
                r = sess.get(url, headers=UA, timeout=30)
                r.raise_for_status()
                open(f, "wb").write(r.content)
            sheet.paste(Image.open(f).convert("RGB"), (i * TILE, j * TILE))
    # crop the window then scale to the output size
    box = (round((X0 - tx0) * TILE), round((Y0 - ty0) * TILE), round((X1 - tx0) * TILE), round((Y1 - ty0) * TILE))
    return sheet.crop(box).resize((OUT_W, OUT_H), Image.LANCZOS)


# ── drawing helpers ────────────────────────────────────────────────────────────────────────
FONT = r"C:\Windows\Fonts\segoeui.ttf"
FONTB = r"C:\Windows\Fonts\segoeuib.ttf"
FONTI = r"C:\Windows\Fonts\segoeuii.ttf"


def font(size, bold=False, italic=False):
    return ImageFont.truetype(FONTB if bold else FONTI if italic else FONT, size)


BLUE, RED, TKB, TKR, GREEN, INK, FRONT = "#1f5fbf", "#c2362b", "#0b86a8", "#c96a10", "#2e7f38", "#1b2629", "#a4221a"
HALO = "#ffffff"


def dashed(draw, a, b, fill, width, dash=(14, 8)):
    (ax, ay), (bx, by) = a, b
    length = math.hypot(bx - ax, by - ay)
    if length == 0:
        return
    ux, uy = (bx - ax) / length, (by - ay) / length
    t, on = 0.0, True
    while t < length:
        seg = dash[0] if on else dash[1]
        t2 = min(t + seg, length)
        if on:
            draw.line([(ax + ux * t, ay + uy * t), (ax + ux * t2, ay + uy * t2)], fill=fill, width=width)
        t, on = t2, not on


def dashed_poly(draw, pts, fill, width, dash):
    for a, b in zip(pts, pts[1:]):
        dashed(draw, a, b, fill, width, dash)


def label(draw, xy, text, fill, size=17, bold=True, anchor="la", italic=False, halo=3):
    draw.text(xy, text, font=font(size, bold, italic), fill=fill, anchor=anchor, stroke_width=halo, stroke_fill=HALO)


def disc(draw, c, r, fill, outline, w=3):
    draw.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=fill, outline=outline, width=w)


# label placement chosen by eye on the rendered map, to keep names off each other
QRA_LABEL_BELOW = {"QRA Francfort"}
SUPPORT_LABEL_AT_END = {"Arco 1", "Arco 2", "Shell 1"}


# ── render ─────────────────────────────────────────────────────────────────────────────────
def render():
    img = basemap().convert("RGBA")
    # slightly fade the basemap so the overlays lead
    img = Image.alpha_composite(img, Image.new("RGBA", img.size, (255, 255, 255, 95)))

    # translucent areas (QRA discs) on their own layer
    area = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ad = ImageDraw.Draw(area)
    for q in D["qra"]:
        col = (194, 54, 43) if q["side"] == "red" else (31, 95, 191)
        c = px(q["x"], q["y"])
        r = q["radius_nm"] * 1852 * px_per_m(q["x"], q["y"])
        ad.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=col + (38,), outline=col + (230,), width=3)
    img = Image.alpha_composite(img, area)
    d = ImageDraw.Draw(img)

    # QRA names
    for q in D["qra"]:
        col = RED if q["side"] == "red" else BLUE
        c = px(q["x"], q["y"])
        r = q["radius_nm"] * 1852 * px_per_m(q["x"], q["y"])
        if q["name"] in QRA_LABEL_BELOW:
            label(d, (c[0], c[1] + r + 6), q["name"], col, 18, anchor="mt")
        else:
            label(d, (c[0], c[1] - r - 6), q["name"], col, 18, anchor="ms")

    # sanctuaries (thick dashes, the colour of the side they protect)
    for z in D["sanctuaries"]:
        col = BLUE if z["side"] == "blue" else RED
        if z["side"] == "blue":
            poly = [px(p["x"], p["y"]) for p in z["poly"]]
            dashed_poly(d, poly + poly[:1], col, 6, (18, 10))
            cx, cy = px(z["x"], z["y"])
            label(d, (cx, cy + 40), "SANCTUAIRE BLEU", col, 18, anchor="mm")
        else:
            cx, cy = px(z["x"], z["y"])
            r = z["radius_nm"] * 1852 * px_per_m(z["x"], z["y"])
            n = 48
            ring = [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]
            dashed_poly(d, ring, col, 5, (12, 8))

    # front line
    front = [px(p["x"], p["y"]) for p in D["front"]]
    dashed_poly(d, front, FRONT, 6, (22, 12))
    fx, fy = front[6]
    label(d, (fx - 16, fy), "ligne de front (approx.)", FRONT, 18, bold=False, italic=True, anchor="rm")

    # CAP on demand (dashed) and support racetracks (solid, thick)
    for cp in D["caps"]:
        a, b = px(cp["a"]["x"], cp["a"]["y"]), px(cp["b"]["x"], cp["b"]["y"])
        dashed(d, a, b, RED if cp["side"] == "red" else BLUE, 4, (10, 8))
    for s in D["support"]:
        a, b = px(s["a"]["x"], s["a"]["y"]), px(s["b"]["x"], s["b"]["y"])
        col = TKR if s["side"] == "red" else TKB
        d.line([a, b], fill=col, width=9)
        for p in (a, b):
            disc(d, p, 4.5, col, col, 1)
        low = s["name"] in SUPPORT_LABEL_AT_END  # label at the far end, where nothing else sits
        anc = b if low else a
        label(d, (anc[0] + 9, anc[1] + (18 if low else -6)), s["name"], col, 17)

    # training zones (green, lettered) and combat zones (red, numbered)
    LETTER = {"Baumholder": "H", "WahnerHeide": "A", "Borkenberge": "S", "Hunsrueck": "R"}
    num = 0
    for z in D["zones"]:
        c = px(z["x"], z["y"])
        if z["training"]:
            if z["key"].endswith("_Easy") or z["key"].endswith("_SAR"):
                fam = z["key"].split("_")[1]
                disc(d, c, 14, HALO, GREEN, 4)
                label(d, (c[0], c[1]), LETTER[fam], GREEN, 16, anchor="mm", halo=0)
                label(d, (c[0] + 20, c[1]), z["name"].split(" - ")[0], GREEN, 17, anchor="lm")
            continue
        num += 1
        disc(d, c, 14, RED, HALO, 3)
        label(d, (c[0], c[1]), str(num), HALO, 15, anchor="mm", halo=0)

    # bases and FARPs
    for b in D["bases"]:
        col = RED if b["side"] == "red" else BLUE
        c = px(b["x"], b["y"])
        d.rectangle([c[0] - 8, c[1] - 8, c[0] + 8, c[1] + 8], fill=col, outline=HALO, width=2)
        label(d, (c[0] + 14, c[1]), b["name"], col, 18, anchor="lm")
    for f in D["farps"]:
        c = px(f["x"], f["y"])
        d.polygon([(c[0], c[1] - 11), (c[0] + 11, c[1] + 8), (c[0] - 11, c[1] + 8)], fill=GREEN, outline=HALO)
        label(d, (c[0] + 14, c[1] + 10), f"FARP {f['name']}", GREEN, 16, anchor="lm")

    # carrier (ship marker) and the arena, north of the frame (arrow on the top edge)
    cv = D["carrier"]
    c = px(cv["x"], cv["y"])
    d.polygon([(c[0] - 16, c[1] - 5), (c[0] + 16, c[1] - 5), (c[0] + 10, c[1] + 7), (c[0] - 10, c[1] + 7)], fill=BLUE, outline=HALO)
    label(d, (c[0] + 22, c[1]), "CVN-74 Stennis", BLUE, 17, anchor="lm")
    az = D["arena_zone"]
    ax, _ = px(az["x"], az["y"])
    d.polygon([(ax, 8), (ax - 14, 34), (ax + 14, 34)], fill=INK)
    label(d, (ax + 20, 24), f"Arène (Grand Belt, bullseye {az['be']})", INK, 17, anchor="lm")

    # bullseye
    bu = px(D["bullseye"]["x"], D["bullseye"]["y"])
    disc(d, bu, 11, None, INK, 3)
    disc(d, bu, 3.5, INK, INK, 1)
    label(d, (bu[0] + 15, bu[1] - 12), "BULLSEYE", INK, 17, anchor="ls")

    # title, legend, scale bar, attribution
    label(d, (24, 22), "VEAF Open Training — GermanyCW (moderne)", INK, 30, anchor="la")
    label(d, (24, 62), f"Bullseye : Brocken {D['bullseye']['ddm']}", INK, 17, bold=False, anchor="la")
    # bottom right, above the scale bar: the top left corner is where the North Sea carrier sits
    legend(d, (OUT_W - 24 - 470, OUT_H - 70 - 12 * 28 - 20 - 70))
    scalebar(d, (OUT_W - 24, OUT_H - 70))
    label(d, (OUT_W - 24, OUT_H - 24), "Fond de carte © OpenStreetMap contributors", "#5a6668", 15,
          bold=False, anchor="rs", halo=2)

    out = img.convert("RGB")
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    out.save(os.path.join(ROOT, "docs", "carte.jpg"), quality=88, optimize=True)
    # DCS briefing picture: same map, 1600 px JPEG (the briefing panel shows it smaller; keeps the .miz light)
    small = out.resize((1600, round(OUT_H * 1600 / OUT_W)), Image.LANCZOS)
    small.save(os.path.join(ROOT, "src", "mission", "l10n", "DEFAULT", "carte.jpg"), quality=80, optimize=True)
    return out


def legend(d, origin):
    x, y = origin
    rows = [
        ("rect", BLUE, "Base bleue avec slots"), ("rect", RED, "Base rouge avec slots"),
        ("tri", GREEN, "FARP"), ("line", TKB, "Ravitailleur / AWACS bleu (hippodrome)"),
        ("line", TKR, "Ravitailleur / AWACS rouge"), ("dash", BLUE, "CAP à la demande (bleue / rouge)"),
        ("qra", RED, "QRA : rayon d'intervention"), ("num", RED, "Zone de combat (numéro du briefing)"),
        ("let", GREEN, "Entraînement : H hélicos, A attaque, S SEAD, R sauvetage"), ("front", FRONT, "Ligne de front (approx.)"),
        ("sanct", BLUE, "Sanctuaire (bleu / rouge)"), ("ship", BLUE, "Porte-avions"),
    ]
    lh, w = 28, 470
    top = y
    y = top + len(rows) * lh + 20
    d.rounded_rectangle([x, top, x + w, y], radius=8, fill=(255, 255, 255, 235), outline="#b7c1c3")
    for i, (kind, col, text) in enumerate(rows):
        cy = top + 14 + i * lh + lh / 2
        cx = x + 22
        if kind == "rect":
            d.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], fill=col, outline=HALO, width=2)
        elif kind == "tri":
            d.polygon([(cx, cy - 10), (cx + 10, cy + 7), (cx - 10, cy + 7)], fill=col)
        elif kind == "line":
            d.line([(cx - 14, cy), (cx + 14, cy)], fill=col, width=8)
        elif kind == "dash":
            dashed(d, (cx - 14, cy), (cx + 14, cy), col, 4, (7, 5))
        elif kind == "qra":
            disc(d, (cx, cy), 11, (194, 54, 43, 40), col, 2)
        elif kind == "num":
            disc(d, (cx, cy), 11, col, HALO, 2)
            label(d, (cx, cy), "1", HALO, 12, anchor="mm", halo=0)
        elif kind == "let":
            disc(d, (cx, cy), 11, HALO, col, 3)
            label(d, (cx, cy), "H", col, 12, anchor="mm", halo=0)
        elif kind == "sanct":
            dashed(d, (cx - 14, cy), (cx + 14, cy), col, 6, (8, 5))
        elif kind == "ship":
            d.polygon([(cx - 13, cy - 4), (cx + 13, cy - 4), (cx + 8, cy + 6), (cx - 8, cy + 6)], fill=col)
        elif kind == "front":
            dashed(d, (cx - 14, cy), (cx + 14, cy), col, 5, (10, 6))
        d.text((x + 46, cy), text, font=font(15), fill=INK, anchor="lm")


def scalebar(d, origin):
    x1, y = origin
    nm = 50
    length = nm * 1852 * px_per_m(D["bullseye"]["x"], D["bullseye"]["y"])
    x0 = x1 - length
    d.rectangle([x0 - 6, y - 26, x1 + 6, y + 8], fill=(255, 255, 255, 220))
    d.line([(x0, y), (x1, y)], fill=INK, width=4)
    for x in (x0, x0 + length / 2, x1):
        d.line([(x, y - 8), (x, y + 4)], fill=INK, width=3)
    d.text(((x0 + x1) / 2, y - 12), f"{nm} nm (échelle au bullseye)", font=font(14), fill=INK, anchor="ms")


if __name__ == "__main__":
    im = render()
    print(im.size)
