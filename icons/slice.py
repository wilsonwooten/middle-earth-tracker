#!/usr/bin/env python3
"""Slice a Gemini grid image into icon PNGs named per the batch header in portrait-batches.txt.
Usage: slice.py <batch-number> <image-file>"""
import re, sys, os
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__))
n, img = sys.argv[1], sys.argv[2]
hdr = next((l for l in open(f"{here}/portrait-batches.txt") if l.startswith(f"=== Batch {n} ")), None)
if not hdr: sys.exit(f"no batch {n}")
cols, rows = map(int, re.search(r"grid: (\d+)x(\d+)", hdr).groups())
files = re.search(r"files: (.*?)\)", hdr).group(1).split(", ")
im = Image.open(img).convert("RGB"); W, H = im.size; cw, ch = W / cols, H / rows
for i, f in enumerate(files):
    c, r = i % cols, i // cols
    tile = im.crop((round(c * cw), round(r * ch), round((c + 1) * cw), round((r + 1) * ch))).resize((256, 256), Image.LANCZOS)
    tile.save(f"{here}/{f}"); print("wrote", f)
