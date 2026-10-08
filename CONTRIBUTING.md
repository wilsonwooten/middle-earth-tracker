# Contributing

This file is for people and for coding agents (`AGENTS.md` is a copy). It covers what the
README does not: how the pieces fit, how to check a change, and what is generated.

## Run and check

- No build. Open `index.html` in a browser; everything loads from `file://`.
- URL parameters for a fixed view: `?book=lotr&ch=20` (chapter index, 0-based),
  `&q=Name` opens a search result, `&follow=1` follows that character, `&still=1`
  freezes the highlight pulse, `&zoom=N&at=x,y` (image percent) sets a view with
  auto-fit off, `&labels=1` shows place labels, `&jump=1` presses the first
  "View on the ... map" button.
- `python3 tools/validate.py` (needs `node`) checks the data files against each other:
  place names, chapter ids, deaths against the cast, icons, ASCII. It is what CI runs.
- `?selftest=1` renders every chapter, follow, tray, card and place highlight of every
  book and writes findings to `<pre id="selftest">`. Run it before a pull request; it
  should report only `offmap` lines (a character placed somewhere the chapter's map does
  not have).
- A JavaScript error leaves the page blank with no message. After editing `index.html`,
  pull the inline script out and run `node --check` on it, or watch the browser console.
- Headless Chrome screenshots work (`--headless=new --screenshot`), but Chrome caches
  `file://` scripts between runs: use a fresh `--user-data-dir` per shot.

## Layout

| Path | What it is |
|---|---|
| `index.html` | The whole app: Leaflet map, panel, search, highlight, labels. One file. |
| `data/hobbit-lotr.js`, `silmarillion.js`, `unfinished-tales.js` | Books: chapters with `where` (who is where), `pins`, `map`, `note`. |
| `data/extra-cast.js` | Second-tier cast merged into the chapters at load, with their card notes. |
| `data/summaries-*.js` | Per chapter `summary`, `moves`, and `who` (one line per character). |
| `data/places.js` | Place coordinates per map, percent of image width and height. |
| `data/shapes.js` | Highlight shapes: rivers, roads and ranges as `line`, regions as `area`. |
| `data/place-events.js` | What happens at a place: `[book id, chapter, one line]`. |
| `data/deaths.js` | Chapter a character dies in, per book. |
| `data/lineage.js` | One race, kindred, house line per character. |
| `data/labels-gondor.js` | Names drawn by the app on the Gondor map (it was rendered without text). |
| `data/shapes-svg.js` | Generated. Vector masks for Third Age shapes, from the mapome SVG. |
| `data/icon-colors.js` | Generated. Ring and route colour per character, from the icons. |
| `icons/` | Character portraits, `CHARACTERS.tsv` (name, file, books), `manifest.js`. |
| `maps/` | Map images and the prompts used to make the Gemini ones. |
| `fonts/` | IM Fell, used for the drawn labels. |
| `tools/` | Generators for the two generated data files. |

## Data rules

- Chapter ids are strings and are the join key everywhere: `n` in the book file,
  the second element of a place event, the value in `deaths.js`, the key in summaries.
  Use them exactly as the book file spells them (`"I.3"`, `"19b"`, `"Ak.3"`, `"I.2m"`).
- Place and shape names are the other join key. A name in `where`, `pins`,
  `place-events.js` or `labels-gondor.js` must match `places.js` or `shapes.js` exactly.
  A place can exist on several maps under the same name; the app offers a jump.
- Positions are sticky: a character stays where the last chapter put them until a
  later chapter moves them. `""` takes them off the map (left the story, or out of
  view). Death is separate: add the chapter to `deaths.js` when the text makes it plain.
- Coordinates are percent of the image, read off a grid, and about 2 percent is normal
  error. Fix them in the app: "Edit places", drag the pin, "Copy places JSON", paste
  over the file. Shapes: open the place, "Trace line" or "Trace area", double-click to
  finish, "Copy shapes JSON".
- Place events are one line each, present tense, no spoilers beyond that chapter. The
  app hides lines for chapters past the one being read.
- Summaries are paraphrase. Do not paste the text of the books.
- ASCII only in every file: `--` not an em dash, plain quotes, no accents in names
  (`Numenor`, `Dunharrow`). The map labels and search are ASCII too.
- Keep the file-local style: one entry per line, same quoting, same spacing.

## Generated files

Do not hand-edit these; change the input and rerun the tool from the repo root.

- `data/shapes-svg.js`: `git clone https://github.com/k1tesurfen/mapome /tmp/mapome`
  then `python3 tools/extract-svg-masks.py /tmp/mapome/preview-mapome.svg`. The `LAYER`
  table in the script says which mapome layer each Third Age shape comes from; a shape
  not listed keeps its rough trace. `--verify out.svg` writes an overlay to eyeball.
- `data/icon-colors.js`: `python3 tools/icon-colors.py` (needs Pillow and numpy).
  `OVERRIDES` in the script takes hand picks.
- `icons/manifest.js`: `icons/make-manifest.sh` after adding portraits.

## Why things are the way they are

- Place highlight. Searching a river, range or region pulses the map's own ink inside
  the shape: the map image is redrawn through an SVG colour-matrix filter that keeps
  dark pixels as a tinted alpha layer, masked to the shape, and the mask edge is
  feathered. Pure SVG so it works from `file://`, where canvas pixel reads are blocked.
  On the Third Age map the mask is the feature as drawn in the mapome vector source,
  so only that range or river lights; elsewhere it is the rough trace in `shapes.js`.
- Third Age masks. mapome's SVG is the same drawing as the parchment render, so a
  uniform scale and offset maps SVG units to image pixels (`tools/fit-svg-to-map.py`
  finds it by ink overlap, 98 percent). `tools/extract-svg-masks.py` then picks the
  paths of the matching layer inside each traced shape; rivers are clipped out of the
  long river and coastline strokes. The mask data is CC BY-SA 4.0 from mapome.
- Ring and route colours come from the portraits (`tools/icon-colors.py`): the most
  prominent saturated colour wins (a garment, a gem), all-grey figures get a slate,
  all-tan figures a dark umber so the ring reads on parchment, and the result is
  softened to a mid tone. Hand picks go in `OVERRIDES`.
- Gondor map. The image model could not spell the names (a third wrong on the best
  attempt), so the map was rendered without any text from Christopher Tolkien's map
  and the app letters it from `data/labels-gondor.js`, in his wording and placement,
  set in IM Fell because it is the closest open face to his tall thin capitals.
- Positions are sticky and `""` means "off the map" rather than dead, because many
  characters simply leave the narrative. `deaths.js` is separate so the panel can say
  "dies here" on the chapter and "died V.7" after, without touching the position data.
- Place events are hidden past the current chapter, and the whole app draws nothing
  later than the chapter being read. That rule is the point of the project.
- The data validator exists because a wrong name or chapter id fails silently in the
  browser; its first run found one entry naming a character absent from the cast.

## What helps most

- Corrections to the Silmarillion and Unfinished Tales positions, the place events and
  the deaths table. Those were drafted from memory. A fix is one data line; say which
  chapter of the book supports it in the pull request.
- Missing characters: add them to the book file's `where` (or `extra-cast.js` for
  minor cast), `lineage.js`, and a portrait in `icons/` if you have one.
- New shapes for rivers and regions that are drawn on a map but not yet searchable.

Run `python3 tools/validate.py` and `?selftest=1` before opening a pull request; the
`Check` workflow runs both on every push and pull request, and `Pages` deploys `main`.

## Licenses

Code is MIT. The Third Age map and the mask data derived from it are CC BY-SA 4.0
(mapome); the Beleriand map is CC BY-SA 3.0 (Starcave). The Gemini-made maps and
portraits are used here for this project and carry no CC license. A new map image needs
a line in `LICENSE` and a credit in the map's `MAPS` entry. Fonts are OFL.
