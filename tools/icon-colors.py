#!/usr/bin/env python3
"""Pick a ring colour per character from their icon: the most prominent saturated colour in the
figure (centre of the image, background corners excluded), then softened for the map.

    python3 tools/icon-colors.py            # writes data/icon-colors.js
    python3 tools/icon-colors.py --sheet contact.png   # also a contact sheet to eyeball

Needs Pillow and numpy (the pe-streams conda env has them).
"""
import argparse, colorsys, json, os, re
import numpy as np
from PIL import Image, ImageDraw

ICON_DIR = "icons"
OUT = "data/icon-colors.js"
# Hand picks that beat the extraction, as "#rrggbb"; the ring is drawn as given.
OVERRIDES = {}


def accent(path):
    """Standout colour of the figure: a coloured garment or feature if there is one, else the
    hair or cloak grey, else (all-tan characters) a dark umber. Tan is the parchment colour, so
    a tan ring would vanish on the map."""
    im = Image.open(path).convert("RGB").resize((96, 96))
    a = np.asarray(im).astype(float) / 255
    corners = np.concatenate([a[:6, :6].reshape(-1, 3), a[:6, -6:].reshape(-1, 3), a[-6:, :6].reshape(-1, 3), a[-6:, -6:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    px = a.reshape(-1, 3)
    keep = np.linalg.norm(px - bg, axis=1) > 0.18
    px = px[keep] if keep.sum() > 200 else px
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in px])
    h = (hsv[:, 0] * 12).astype(int) % 12
    sb = np.minimum((hsv[:, 1] * 4).astype(int), 3)
    vb = np.minimum((hsv[:, 2] * 4).astype(int), 3)
    key = h * 16 + sb * 4 + vb
    colourful, greys = [], []
    for k in np.unique(key):
        sel = key == k
        n, mh, ms, mv = sel.sum(), hsv[sel, 0].mean(), hsv[sel, 1].mean(), hsv[sel, 2].mean()
        tan = 0.02 <= mh <= 0.14 and ms < 0.7
        if ms >= 0.25 and mv >= 0.2 and not tan:
            colourful.append((n * (ms ** 1.5) * (0.4 + mv), n, px[sel].mean(axis=0)))
        elif ms < 0.25 and 0.12 <= mv <= 0.85:
            greys.append((n, px[sel].mean(axis=0)))
    total = len(px)
    colourful = [c for c in colourful if c[1] >= 0.02 * total]   # a sash or gem counts, a stray pixel does not
    if colourful:
        return max(colourful, key=lambda c: c[0])[2], "colour"
    if greys and max(g[0] for g in greys) >= 0.08 * total:
        return max(greys, key=lambda g: g[0])[1], "grey"
    return np.array([0.45, 0.30, 0.15]), "tan"


def soften(rgb, kind):
    h, s, v = colorsys.rgb_to_hsv(*rgb)
    if kind == "colour":
        s = 0.40 + 0.30 * s        # keep the hue, ease the saturation
        v = 0.45 + 0.30 * v        # mid tones: lifted darks, no neon
    elif kind == "grey":
        h, s, v = (h if s > 0.08 else 0.58), 0.18, 0.35 + 0.25 * v   # slate, reads on parchment
    else:
        h, s, v = 0.07, 0.6, 0.42  # dark umber, clearly darker than the map
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet")
    args = ap.parse_args()
    manifest = open(os.path.join(ICON_DIR, "manifest.js")).read()
    names = dict(re.findall(r'"([^"]+)":\s*"([^"]+)"', manifest))
    out = {}
    for name, f in sorted(names.items()):
        p = os.path.join(ICON_DIR, f)
        if os.path.exists(p):
            out[name] = OVERRIDES.get(name) or soften(*accent(p))
    txt = "// Ring and route colour per character, taken from their icon by tools/icon-colors.py.\n// Generated; do not hand-edit.\nwindow.ICON_COLORS = " + json.dumps(out, indent=1) + ";\n"
    open(OUT, "w").write(txt)
    print("wrote", OUT, len(out), "colours")
    if args.sheet:
        cols, cell = 12, 80
        rows = (len(out) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell, rows * cell), (244, 232, 208))
        d = ImageDraw.Draw(sheet)
        for i, (name, col) in enumerate(out.items()):
            x, y = (i % cols) * cell, (i // cols) * cell
            d.ellipse([x + 6, y + 4, x + 62, y + 60], fill=col)
            ic = Image.open(os.path.join(ICON_DIR, names[name])).convert("RGB").resize((48, 48))
            mask = Image.new("L", (48, 48), 0); ImageDraw.Draw(mask).ellipse([0, 0, 47, 47], fill=255)
            sheet.paste(ic, (x + 10, y + 8), mask)
            d.text((x + 4, y + 64), name[:13], fill=(40, 30, 20))
        sheet.save(args.sheet); print("wrote", args.sheet)


if __name__ == "__main__":
    main()
