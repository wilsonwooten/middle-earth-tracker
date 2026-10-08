#!/usr/bin/env python3
"""Check the data files against each other. Run from the repo root before a merge request.

Checks: every place used in chapter data, pins, events and the Gondor labels exists in
places.js or shapes.js for a map the book uses; every chapter id in events, deaths and
summaries exists in its book; every death names a cast member; every icon in the manifest
is a file; ASCII only in data and the app. Exit code 1 on any problem. Needs node.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
problems = []


def load():
    """Evaluate the data files the way the browser does (a bare `window`) and return them."""
    import subprocess
    files = ["data/hobbit-lotr.js", "data/silmarillion.js", "data/unfinished-tales.js", "data/places.js", "data/shapes.js",
             "data/place-events.js", "data/deaths.js", "data/extra-cast.js", "data/labels-gondor.js", "icons/manifest.js",
             "data/summaries-hobbit-lotr.js", "data/summaries-silmarillion.js", "data/summaries-unfinished-tales.js", "data/lineage.js"]
    js = r"""
      const vm = require("vm"), fs = require("fs");
      const window = { BOOKS: [] }; const ctx = vm.createContext({ window });
      for (const f of process.argv.filter(a => a.endsWith(".js"))) {
        const src = fs.readFileSync(f, "utf8");
        // files declare top-level const PLACES / SHAPES / SHAPES_SVG: capture them onto window
        const tail = ["PLACES", "SHAPES", "SHAPES_SVG"].map(k => `if (typeof ${k} !== "undefined") window.${k} = ${k};`).join("");
        vm.runInContext(src + "\n;" + tail, ctx, { filename: f });
      }
      process.stdout.write(JSON.stringify(window));
    """
    out = subprocess.run(["node", "-e", js, "--"] + files, cwd=ROOT, capture_output=True, text=True)
    if out.returncode != 0:
        print("PROBLEM data files do not evaluate:\n" + out.stderr.strip())
        sys.exit(1)
    return json.loads(out.stdout)


# --- load ---------------------------------------------------------------
W = load()
books = {b["id"]: b for b in W.get("BOOKS", [])}
places = W.get("PLACES") or {}
shapes = W.get("SHAPES") or {}
events = W.get("PLACE_EVENTS") or {}
deaths = W.get("DEATHS") or {}
extra = W.get("EXTRA_CAST") or {}
labels = W.get("MAP_LABELS") or {}
icons = W.get("ICONS") or {}
summaries = W.get("SUMMARIES") or {}
lineage = W.get("LINEAGE") or {}

all_names = {m: set(places.get(m, {})) | set(shapes.get(m, {})) for m in set(places) | set(shapes)}
every_name = set().union(*all_names.values()) if all_names else set()

# --- chapter data -------------------------------------------------------
cast = {}
for bid, b in books.items():
    chs = b.get("chapters", [])
    ids = [c["n"] for c in chs]
    if len(ids) != len(set(ids)):
        problems.append("%s: duplicate chapter ids" % bid)
    names = set()
    for c in chs:
        m = c.get("map", b.get("map"))
        if m not in all_names:
            problems.append("%s %s: unknown map %r" % (bid, c["n"], m))
            continue
        for who, pl in (c.get("where") or {}).items():
            names.add(who)
            if pl and pl not in every_name:
                problems.append("%s %s: %s placed at unknown place %r" % (bid, c["n"], who, pl))
        for pl in c.get("pins") or []:
            if pl not in all_names[m]:
                problems.append("%s %s: pin %r is not on the %s map" % (bid, c["n"], pl, m))
    for n, w in (extra.get(bid) or {}).items():
        if n not in ids:
            problems.append("extra-cast %s: chapter %r does not exist" % (bid, n))
        for who, pl in (w or {}).items():
            names.add(who)
            if pl and pl not in every_name:
                problems.append("extra-cast %s %s: %s at unknown place %r" % (bid, n, who, pl))
    cast[bid] = names
    for n in summaries.get(bid, {}):
        if n not in ids:
            problems.append("summaries %s: chapter %r does not exist" % (bid, n))

# --- events, deaths, labels, icons ----------------------------------------
for pl, lines in events.items():
    if pl not in every_name:
        problems.append("place-events: %r is not a place or shape" % pl)
    for ln in lines:
        bid, n = ln[0], ln[1]
        if bid not in books:
            problems.append("place-events %s: unknown book %r" % (pl, bid))
        elif n not in [c["n"] for c in books[bid]["chapters"]]:
            problems.append("place-events %s: %s has no chapter %r" % (pl, bid, n))
for bid, d in deaths.items():
    if bid not in books:
        problems.append("deaths: unknown book %r" % bid)
        continue
    ids = [c["n"] for c in books[bid]["chapters"]]
    for who, n in d.items():
        if n not in ids:
            problems.append("deaths %s: %s has no chapter %r" % (bid, who, n))
        if who not in cast.get(bid, set()):
            problems.append("deaths %s: %s is not in the cast" % (bid, who))
for m, ls in labels.items():
    for l in ls:
        if "p" not in l and ("x" not in l or "y" not in l):
            problems.append("labels %s: %r has neither p nor x,y" % (m, l.get("t")))
for who, f in icons.items():
    if not os.path.exists(os.path.join(ROOT, "icons", f)):
        problems.append("icons: %s -> %s is missing" % (who, f))

# --- ASCII ---------------------------------------------------------------
for dirpath, _, files in os.walk(ROOT):
    if "/.git" in dirpath:
        continue
    for fn in files:
        if fn.endswith((".js", ".html", ".md", ".py", ".txt", ".sh", ".tsv")):
            p = os.path.join(dirpath, fn)
            for i, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
                bad = [c for c in line if ord(c) > 127]
                if bad:
                    problems.append("%s:%d: non-ASCII %r" % (os.path.relpath(p, ROOT), i, "".join(bad[:5])))
                    break

# --- report ----------------------------------------------------------------
print("books %d, places %d, shapes %d, events %d, deaths %d, icons %d" % (
    len(books), sum(len(v) for v in places.values()), sum(len(v) for v in shapes.values()),
    sum(len(v) for v in events.values()), sum(len(v) for v in deaths.values()), len(icons)))
for p in problems:
    print("PROBLEM", p)
print("%d problem(s)" % len(problems))
sys.exit(1 if problems else 0)
