# Felixor - notes for Claude Code

Marketing site for Felixor, an AI product studio. Static, no framework, no build
step at deploy time. Lives at felixor.com (also .ai and .net, which redirect).

## How this repo works

`index.html` is **generated**. Do not hand-edit it - your changes will be wiped
on the next build. Edit the source in `src/`, then rebuild.

```
index.html        generated: 4 routes, all markup, inlined CSS + JS
assets/           subset font + 4 generated product images
vercel.json       cache headers for /assets/*, security headers
src/              the generator
```

### Rebuild

```bash
cd src
python3 art.py iris      # regenerates product artwork -> art.json
python3 build.py iris    # writes ../index.html with everything inlined
python3 extract.py       # splits assets back out to ../assets/, subsets the font
```

`extract.py` exits non-zero if any asset reference fails to resolve. Trust it.
Only rerun `art.py` if the palette changed - it is the slow step.

### Where things live

| Want to change | Edit |
|---|---|
| Any copy, product info, career timeline | `src/data.py` |
| Accent colour / palette | `src/palettes.py` |
| Styles | `src/style.css` |
| Router, scroll engine, canvases | `src/app.js` |
| Page structure, meta tags, `<head>` | `src/build.py` |

## Routes

Hash router. Every route's markup ships in the HTML source, so content is
crawlable even though navigation is client-side.

`#/` studio · `#/portfolio` · `#/product/<slug>` · `#/about`

Slugs: quorum, camber, understory, tidemark.

## Constraints that are deliberate

Breaking these is a regression, not a style preference.

- **No scroll event listeners.** IntersectionObserver and CSS scroll timelines
  only. This is also why the pinned scroll section reverses correctly on the
  way back up - get this wrong and reverse scrolling breaks.
- **No em-dashes or en-dashes** anywhere in visible copy. Use a hyphen.
- **`prefers-reduced-motion` resolves every animation to its end state.** Any
  new animation needs a reduced-motion path.
- **One accent colour**, from `palettes.py`. Buttons use `--accent-btn`, a
  darker shade, because the accent at full strength fails WCAG AA behind white
  button text. Do not "simplify" these into one token.
- **Zero external requests.** Font and images are local. No CDNs, no Google
  Fonts link.
- **The font is subsetted** to Latin-1 plus smart quotes. Copy outside that
  range renders as tofu - widen `SUBSET_RANGE` in `src/extract.py` if needed.

## Palette

Three are defined: `iris` (live), `glacier`, `amethyst`. Switching regenerates
the hero gradient, the scroll field, and all four product images together:

```bash
cd src && python3 art.py glacier && python3 build.py glacier && python3 extract.py
```

## Deploying

Push to `main`. Vercel builds from GitHub with no build command and no output
directory - it serves the repo root. Nothing else to do.

## Known placeholders

- The four product names are invented; every "Visit product" link is `#`
- The About page career timeline has no dates, and Stripe may be in the wrong
  chronological position
- No founder photo

## Verifying a change

There is no test suite. Before pushing anything visual, serve it and look:

```bash
python3 -m http.server 8000     # from the repo root
```

Check at 1440, 390 and 320 px. At 320 the nav CTA is hidden on purpose - it
clips otherwise. Confirm the scroll section on `#/` still advances 0→3 going
down and reverses 3→0 coming back up.
