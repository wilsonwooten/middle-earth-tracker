#!/usr/bin/env python3
"""Extract per-feature highlight masks for the Third Age map from the mapome SVG source.

For every shape in data/shapes.js (thirdage) that names a drawn feature (range, forest, river,
road, lake), pick the SVG paths of the matching mapome layer that fall inside the rough traced
shape, and write them to data/shapes-svg.js with their SVG transforms. The app uses them as the
mask for the ink pulse, so only the feature's own ink lights up. Shapes with no entry in LAYER
(regions such as Rohan) keep the rough trace as their mask.

Usage, from the repo root:
    git clone https://github.com/k1tesurfen/mapome /tmp/mapome   # CC BY-SA 4.0
    python3 tools/extract-svg-masks.py /tmp/mapome/preview-mapome.svg [--verify check.svg]

FIT is the affine from SVG user units to image pixels, found with tools/fit-svg-to-map.py
(98% ink overlap between a text-free render of the SVG and maps/third-age.jpg). Redo it only
if the map image changes. Stdlib only.
"""
import argparse
import json
import math
import os
import re
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
W, H = 10000, 5455                       # maps/third-age.jpg
FIT = (0.566, 0.5654, 1224.0, -29.0)     # image x = a*X + e, image y = d*Y + f
# Which mapome layer draws each shape. Rivers and the coastline are long paths that carry
# several rivers each, so for those layers only the runs inside the traced band are kept and
# the app strokes them; mountains, forests, roads and lakes are whole filled glyphs.
# Smaller rivers: some are filled shapes in the rivers layer, others strokes inside the coastline
# path, so they are tried in both and the picks merged.
RIVERS = ['Entwash', 'Snowbourn', 'Limlight', 'Silverlode', 'Nimrodel', 'Gladden River', 'Forest River', 'Celduin', 'Carnen', 'Lhun', 'Glanduin', 'Adorn', 'Lefnui', 'Morthond', 'Kiril', 'Ringlo', 'Gilrain', 'Serni', 'Celos', 'Sirith', 'Erui', 'Poros', 'Harnen']
LAYER = {
    "rivers": ["Anduin", "Brandywine", "Hoarwell", "Loudwater"] + RIVERS,
    "mountains-and-forests": ["Misty Mountains", "White Mountains", "Ered Nimrais", "Ephel Duath", "Ered Lithui",
                              "Fangorn", "Lorien", "Old Forest", "Blue Mountains", "Grey Mountains", "Iron Hills",
                              "Emyn Muil", "Druadan Forest", "Ettenmoors", "Mirkwood", "Dead Marshes"],
    "streets": ["Great East Road"],
    "lakes": ["Sea of Rhun", "Sea of Nurnen"],
    "coastline": ["Greyflood", "Isen"] + RIVERS,
}
STROKED = {"rivers", "coastline"}
NUM = re.compile(r'[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?')


# --- SVG geometry -------------------------------------------------------
def parse_tf(t):
    m = [1, 0, 0, 1, 0, 0]
    if not t:
        return m
    for name, args in re.findall(r'(\w+)\(([^)]*)\)', t):
        v = [float(x) for x in re.split(r'[ ,]+', args.strip()) if x]
        if name == "matrix":
            n = v
        elif name == "translate":
            n = [1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0]
        elif name == "scale":
            n = [v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0]
        else:
            raise SystemExit("unsupported transform " + name)
        m = mul(m, n)
    return m


def mul(a, b):
    return [a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1], a[0] * b[2] + a[2] * b[3],
            a[1] * b[2] + a[3] * b[3], a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5]]


def apply(m, x, y):
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


def path_segments(d):
    """(kind, absolute points) per segment; kind M/L/C. mapome only uses M L C Z."""
    toks = re.findall(r'[MLCZmlcz]|' + NUM.pattern, d)
    segs = []
    cx = cy = sx = sy = 0.0
    i = 0
    cmd = "M"
    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]
            i += 1
        u = cmd.upper()
        rel = cmd.islower()
        if u == "Z":
            segs.append(("L", [(sx, sy)]))
            cx, cy = sx, sy
            continue
        n = 6 if u == "C" else 2
        v = [float(toks[i + j]) for j in range(n)]
        i += n
        if rel:
            v = [v[j] + (cx if j % 2 == 0 else cy) for j in range(n)]
        pts = [(v[j], v[j + 1]) for j in range(0, n, 2)]
        segs.append((u, pts))
        cx, cy = pts[-1]
        if u == "M":
            sx, sy = cx, cy
            cmd = "l" if rel else "L"
    return segs


def path_points(d):
    return [p for _, pts in path_segments(d) for p in pts]


def clip_path(d, keep):
    """Rebuild a path from the runs of segments whose points all satisfy keep(local point)."""
    out = []
    run = None
    for kind, pts in path_segments(d):
        if kind == "M":
            run = pts[-1]
            continue
        if run is not None and all(keep(p) for p in pts):
            if not out or out[-1] == "|":
                out.append("M%.1f,%.1f" % run)
            out.append(("C" if kind == "C" else "L") + " ".join("%.1f,%.1f" % q for q in pts))
        elif out and out[-1] != "|":
            out.append("|")
        run = pts[-1]
    return "".join(x for x in out if x != "|")


def load_geometry(svg_path):
    """Every path with its layer (top-level group id) and full transform."""
    root = ET.parse(svg_path).getroot()
    items = []

    def walk(el, m, layer):
        m2 = mul(m, parse_tf(el.get("transform")))
        tag = el.tag.replace(NS, "")
        if tag == "g" and el.get("id"):
            layer = el.get("id")
        if tag == "path":
            items.append({"layer": layer, "m": [round(v, 4) for v in m2], "d": el.get("d")})
        for c in el:
            walk(c, m2, layer)
    walk(root, [1, 0, 0, 1, 0, 0], "root")
    return items


# --- selection ----------------------------------------------------------
def seg_dist(p, u, v):
    px, py = p
    ux, uy = u
    vx, vy = v
    dx, dy = vx - ux, vy - uy
    t = 0 if dx == dy == 0 else max(0, min(1, ((px - ux) * dx + (py - uy) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ux + t * dx), py - (uy + t * dy))


def inside(p, poly):
    x, y = p
    c = False
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def main():
    ap = argparse.ArgumentParser(description="Extract Third Age highlight masks from the mapome SVG.")
    ap.add_argument("svg", help="path to mapome preview-mapome.svg")
    ap.add_argument("--shapes", default="data/shapes.js")
    ap.add_argument("--out", default="data/shapes-svg.js")
    ap.add_argument("--verify", help="also write an SVG overlaying the picked paths on the map, for a visual check")
    ap.add_argument("--report", help="print the picked paths of this shape as image-percent boxes")
    args = ap.parse_args()
    a, d, e, f = FIT

    def to_img(m, x, y):
        X, Y = apply(m, x, y)
        return (a * X + e, d * Y + f)

    geom = load_geometry(args.svg)
    shapes_js = open(args.shapes).read()
    js = re.sub(r'\b(type|pts|w)\s*:', r'"\1":', shapes_js.split("=", 1)[1].strip().rstrip(";"))
    sh = json.loads(re.sub(r',(\s*[\]}])', r'\1', js))["thirdage"]   # JS allows trailing commas, JSON does not
    out = {}
    for layer, names in LAYER.items():
        items = [it for it in geom if it["layer"] == layer]
        for name in names:
            s = sh.get(name)
            if not s:
                print("no shape traced for", name)
                continue
            poly = [(p[0] / 100 * W, p[1] / 100 * H) for p in s["pts"]]
            band = s.get("w", 2.5) / 100 * W
            thr = 0.5
            near = lambda p: min(seg_dist(p, poly[i], poly[i + 1]) for i in range(len(poly) - 1)) <= band
            picked = []
            for it in items:
                if layer in STROKED:
                    # one path carries several rivers: keep only the runs inside the band
                    dd = clip_path(it["d"], lambda q: near(to_img(it["m"], q[0], q[1])))
                    if dd:
                        picked.append(({"m": it["m"], "d": dd, "f": 0}, [to_img(it["m"], x, y) for x, y in path_points(dd)]))
                    continue
                pts = [to_img(it["m"], x, y) for x, y in path_points(it["d"])]
                hit = sum(inside(p, poly) for p in pts) if s["type"] == "area" else sum(near(p) for p in pts)
                if hit / len(pts) >= thr:
                    picked.append((it, pts))
            if not picked:
                if name not in RIVERS or layer == "coastline" and name not in out:
                    print("MISS %-16s nothing in layer %s inside the trace; widen the trace or drop it from LAYER" % (name, layer))
                continue
            if args.report == name:
                for it, pts in picked:
                    print("   %s x %.1f-%.1f%% y %.1f-%.1f%% (%d pts)" % (name, min(q[0] for q in pts) / W * 100, max(q[0] for q in pts) / W * 100,
                                                                         min(q[1] for q in pts) / H * 100, max(q[1] for q in pts) / H * 100, len(pts)))
            allp = [p for _, pts in picked for p in pts]
            bb = [round(min(p[0] for p in allp)), round(min(p[1] for p in allp)), round(max(p[0] for p in allp)), round(max(p[1] for p in allp))]
            if name in out:
                cur = out[name]; cur["layer"] += "+" + layer
                cur["bb"] = [min(cur["bb"][0], bb[0]), min(cur["bb"][1], bb[1]), max(cur["bb"][2], bb[2]), max(cur["bb"][3], bb[3])]
            else:
                cur = out[name] = {"layer": layer, "paths": [], "bb": bb}
            for it, _ in picked:
                rec = {"m": it["m"], "d": re.sub(r'(\d+\.\d{2,})', lambda mm: "%.1f" % float(mm.group(1)), it["d"])}
                if it.get("f") == 0:
                    rec["f"] = 0
                cur["paths"].append(rec)
            print("%-16s %-22s %3d paths %7d bytes" % (name, layer, len(picked), sum(len(p["d"]) for p in cur["paths"])))
    res = {"fit": [round(a, 5), 0, 0, round(d, 5), round(e, 2), round(f, 2)], "shapes": out}
    txt = ("// Per-feature masks for the Third Age map, extracted from the mapome SVG source\n"
           "// (github.com/k1tesurfen/mapome, CC BY-SA 4.0). `fit` maps SVG user units to image pixels; each\n"
           "// path keeps its own SVG transform. Generated by tools/extract-svg-masks.py; do not hand-edit.\n"
           "const SHAPES_SVG = {\"thirdage\": " + json.dumps(res) + "};\n")
    open(args.out, "w").write(txt)
    print("wrote", args.out, len(txt), "bytes")
    if args.verify:
        cols = ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#42d4f4", "#f032e6", "#bfef45", "#469990",
                "#9A6324", "#800000", "#808000", "#000075", "#ffd8b1", "#dcbeff", "#fabed4", "#ffe119", "#aaffc3"]
        parts = []
        for i, (name, v) in enumerate(out.items()):
            col = cols[i % len(cols)]
            parts.append('<g fill="%s" stroke="%s" stroke-width="6" opacity=".85">%s</g>' % (col, col, "".join(
                '<path transform="matrix(%s)" d="%s"%s/>' % (",".join(str(x) for x in p["m"]), p["d"], ' fill="none"' if p.get("f") == 0 else "")
                for p in v["paths"])))
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="2000" height="1091">'
               '<image href="file://%s" width="%d" height="%d"/><g transform="matrix(%s)">%s</g></svg>'
               % (W, H, os.path.abspath("maps/third-age.jpg"), W, H, ",".join(str(x) for x in [a, 0, 0, d, e, f]), "".join(parts)))
        open(args.verify, "w").write(svg)
        print("wrote", args.verify)


if __name__ == "__main__":
    main()
