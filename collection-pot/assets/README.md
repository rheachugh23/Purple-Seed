# Marketing assets

Each asset lives in its **own folder**:

```
assets/
└── YYYY-MM-<short-slug>/        e.g. 2026-12-teacher-gift-reel
    ├── README.md                brief, channel, sizes, copy used, status
    ├── source/                  editable files (HTML, project files, scripts)
    └── export/                  final deliverables (PNG/JPG/MP4/PDF), named <slug>_<size>.<ext>
```

Conventions:
- Slugs are lowercase-kebab-case and say the occasion or campaign plus the format (`birthday-ooh-poster`, `leaver-instagram-carousel`).
- Export names include dimensions, e.g. `leaver-carousel_1080x1350_01.png`.
- 2D and 3D Chip never go in the same piece (brand rule). Note which one the asset uses in its README.
- Pull logos, Chip, fonts and colours from `../brand/`. Don't copy modified brand files back into `brand/`.
