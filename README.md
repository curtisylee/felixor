# felixor.com

The Felixor marketing site. One self-contained static page with a hash router,
served straight from the repo root. No framework, no build step at deploy time.

## Layout

```
index.html        the whole site: four routes, all markup, inlined CSS and JS
assets/           subset font + generated product artwork
vercel.json       cache headers for /assets/*, security headers everywhere
src/              the generator that produces index.html and assets/
```

`index.html` is generated, not hand-edited. Change the source, rebuild, commit both.

## Routes

Client-side hash router. Every route's markup is present in the HTML source,
so the content is crawlable even though navigation is client-side.

| Route | Page |
|---|---|
| `#/` | Studio (home) |
| `#/portfolio` | Portfolio index |
| `#/product/<slug>` | Product detail: quorum, camber, understory, tidemark |
| `#/about` | About and founder |

## Editing content

Copy, products, the scroll-section steps, and the career timeline all live in
`src/data.py`. Nothing else needs touching for a copy change.

```bash
cd src
python3 build.py iris      # writes ../index.html with assets inlined
python3 extract.py         # splits inlined assets back out to assets/
```

## Changing the accent colour

`src/palettes.py` defines the full palette. Three are set up: `iris` (live),
`glacier`, `amethyst`. Swapping regenerates the hero gradient, the scroll
field, and all four product artworks so nothing is left behind.

```bash
python3 src/art.py glacier && python3 src/build.py glacier && python3 src/extract.py
```

Each palette carries a separate `btn_bg` because the accent at full strength
does not always clear WCAG AA behind button text.

## Product artwork

`src/art.py` generates the four product images with Pillow: interference rings
(Quorum), a flow field (Camber), strata (Understory), wave interference
(Tidemark). They are committed to `assets/`, so a normal deploy does not need
Python at all.

## Deploying

Vercel serves the repo root as-is. No build command, no output directory.
Pushing to `main` deploys.

## Notes for whoever picks this up

- The scroll section on the home page is driven entirely by IntersectionObserver
  and CSS scroll timelines. There are no scroll event listeners anywhere, on
  purpose; that is also why the sequence reverses correctly on the way back up.
- The two canvases (hero gradient, scroll field) pause when off-screen.
- `prefers-reduced-motion` resolves every animation to its end state.
- The font is subsetted to Latin-1 plus smart quotes. Adding copy outside that
  range means re-subsetting in `src/extract.py`.
- Placeholder content still in the site: `hello@felixor.com`, the four product
  names, and the "Visit <product>" links, which point at `#` until launch.
