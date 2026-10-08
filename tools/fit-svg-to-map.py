#!/usr/bin/env python3
"""Fit the affine map from mapome SVG user units to maps/third-age.jpg pixels.

Inputs: a text-free render of the SVG (drop the frame, legend, font, arrows, cities and
bridges groups; render at 2668x2000 so svg units = px*5) and a 2000px-wide thumbnail of the
map. Searches x/y scale and offset for the best ink overlap. Needs numpy and Pillow.

    python3 tools/fit-svg-to-map.py render.png thumb.png fit.txt

Paste the result into FIT in tools/extract-svg-masks.py.
"""
import sys, numpy as np
from PIL import Image
svg = np.asarray(Image.open(sys.argv[1]).convert("L")) < 128          # 2668x2000 render, svg coords = px*5
jpg = np.asarray(Image.open(sys.argv[2]).convert("L")).astype(float) / 255  # 2000x1091 thumb, jpg px = px*5
ink = jpg < 0.40
h, w = ink.shape; m = np.zeros_like(ink); m[int(h*.03):int(h*.97), int(w*.03):int(w*.97)] = True; ink &= m
# dilate jpg ink by 1 px for a smoother score
d = ink.copy()
d[1:] |= ink[:-1]; d[:-1] |= ink[1:]; d[:,1:] |= ink[:,:-1]; d[:,:-1] |= ink[:,1:]
ys, xs = np.nonzero(svg); X = xs * 5.0; Y = ys * 5.0   # svg user coords
sel = np.random.RandomState(0).choice(len(X), min(len(X), 150000), replace=False); X = X[sel]; Y = Y[sel]
print("svg ink px", len(xs), "jpg ink px", ink.sum())
def score(a, dd, e, f):
    px = np.round((a * X + e) / 5).astype(int); py = np.round((dd * Y + f) / 5).astype(int)
    ok = (px >= 0) & (px < w) & (py >= 0) & (py < h)
    return d[py[ok], px[ok]].sum() / len(X)
best = (0, None)
for a in np.arange(0.50, 0.62, 0.01):
    for dd in np.arange(0.52, 0.64, 0.01):
        for e in np.arange(1000, 1600, 25):
            for f in np.arange(-400, 100, 25):
                sc = score(a, dd, e, f)
                if sc > best[0]: best = (sc, (a, dd, e, f))
print("coarse", best)
a, dd, e, f = best[1]
for step in [(0.004, 10), (0.001, 3), (0.0004, 1)]:
    improved = True
    while improved:
        improved = False
        for da in (-step[0], 0, step[0]):
            for ddd in (-step[0], 0, step[0]):
                for de in (-step[1], 0, step[1]):
                    for df in (-step[1], 0, step[1]):
                        sc = score(a + da, dd + ddd, e + de, f + df)
                        if sc > best[0] + 1e-6: best = (sc, (a + da, dd + ddd, e + de, f + df)); a, dd, e, f = best[1]; improved = True
print("fine", best)
a, dd, e, f = best[1]
print("FIT a=%.5f d=%.5f e=%.2f f=%.2f score=%.4f" % (a, dd, e, f, best[0]))
# residual check: shift sensitivity
for k, v in {"a+.002": (a+.002, dd, e, f), "d+.002": (a, dd+.002, e, f), "e+5": (a, dd, e+5, f), "f+5": (a, dd, e, f+5)}.items(): print(k, round(score(*v), 4))
open(sys.argv[3], "w").write("%r\n" % (best[1],))
