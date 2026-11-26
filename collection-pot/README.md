# Collection Pot

Workspace for **Collection Pot** marketing assets. Brand source material lives in `brand/`. Each marketing asset we make gets its own folder in `assets/`.

> Collection Pot is the easiest way to sort a group gift, for any occasion.
> **Easy to sort. Impossible to forget.**

## Folder structure

```
collection-pot/
├── README.md                  ← you are here
├── brand/                     ← source of truth: read before making anything
│   ├── BRAND.md               ← condensed brand guidelines (voice, colour, type, Chip rules, copy bank)
│   ├── tokens.css             ← colour + type tokens ready to drop into HTML assets
│   ├── tokens.json            ← same tokens as data
│   ├── LINKS.md               ← website, demo Pots, Drive source links
│   ├── guidelines/            ← full brand guidelines PDF (Nov 2026, 63 pages)
│   ├── logos/                 ← SVG logos (linear black/white, Pot-icon lockup)
│   ├── mascot-3d/renders/     ← 148 official 3D Chip renders (PNG, from Drive)
│   ├── mascot-2d/             ← 2D Chip SVGs (from the live site)
│   ├── icons/                 ← UI and occasion icons used on the site
│   ├── fonts/                 ← Faro Display Lucky (headline font)
│   └── references/
│       ├── website/home/      ← collectionpot.com screenshots, HTML, copy text
│       ├── website/site-assets/ ← every image/SVG the site and demos load, original CDN paths
│       └── demo-pots/<occasion>/ ← each demo Pot: desktop + mobile screenshot, HTML, copy
└── assets/                    ← marketing assets, one folder each
    └── README.md              ← naming + per-asset conventions
```

## Making a new asset

1. Read `brand/BRAND.md` (5 min) and, for anything with Chip, the Chip rules in it.
2. Create `assets/YYYY-MM-<short-slug>/` (e.g. `assets/2026-12-teacher-gift-reel/`).
3. Put a short `README.md` in it (brief, format/sizes, status), plus the sources and the exports.
4. Use `brand/tokens.css` for colours and type. Don't use any colour outside the palette.
