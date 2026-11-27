# The storyboard: posed frames and the one-pager image

The storyboard is the last gate before money is spent. It must look like the film, in real fonts, colours and brand assets, so the person approves something real. And it must cost nothing, so the AI plates appear as sketches.

## 1. Pose the frames in HyperFrames

- Scaffold the project at the platform size (`init <dir> --resolution portrait`). Bundle GSAP locally if the CDN is blocked, and copy the brand fonts and assets into `assets/`.
- Write one scene per script row (or per beat), each mounted at its planned start in `index.html`.
- Use the brand layer for real: headline type, the mascot files, the logo, real product screens and the brand device as crops.
- Draw each **Higgsfield plate as a simple labelled sketch** in flat colours (a room, a desk, hands), with a tag such as `SKETCH · Higgsfield plate 2 · desk from above` outside the safe zone. Overlays (titles, cards, phone screens) go on top exactly where they will sit on the real plate.
- Pose each shot at its key moment, with no animation needed yet.
- Run `check --safe-zone <platform>`, fix overlaps and contrast, then `snapshot --at <one time per frame> -o boards/stills`.
- Look at every still and fix anything off before showing it: collisions, text over busy areas, assets on disallowed grounds.
- Write `STORYBOARD.md` (the frame list with timing, scene, VO, on-screen text, sound, asset or plate), following `hyperframes/references/storyboard-format.md`.

## 2. Make the one-pager image

Write a manifest beside the stills, `boards/onepager.json`:

```json
{
  "title": "Last day of term · Collection Pot · storyboard",
  "subtitle": "9:16 · 30 s · frames 1–4 show Higgsfield plate sketches; brand frames are final",
  "accent": "#F9B910",
  "ink": "#2F2F32",
  "background": "#FBFAF6",
  "columns": 5,
  "frames": [
    { "image": "stills/frame-00-at-1.5s.png", "time": "0:00", "speaker": "TEXT", "cue": "Last day of term. 3:31pm." },
    { "image": "stills/frame-01-at-4.5s.png", "time": "0:02", "speaker": "VO", "cue": "From the whole class." }
  ]
}
```

```bash
python3 <skill>/scripts/storyboard_onepager.py boards/onepager.json -o boards/storyboard-onepager.png
# optional: --title-font <brand display .otf/.ttf> --body-font <brand body .ttf> --scale 2
```

Field by field:
- **`time`** is where the frame starts in the film, as `m:ss`.
- **`speaker`** is who speaks: a character's name, `VO`, several names joined with ` / `, or `TEXT` when the frame has no VO.
- **`cue`** is the VO line for that frame, which the script wraps in quotes. With no VO, use the on-screen line.
- **`accent`** is the brand's hero colour for the time pills.
- **Fonts:** pass the brand's own fonts when they're available, so the page feels like the brand.

The image shows the title and subtitle, then the frames in a grid, one after another in film order, each with its time pill, speaker and cue underneath. Send it with SendUserFile, along with the plate plan (prompt, model, duration and quoted credits per plate), and stop.

## 3. Revisions

Notes on frames change only those frames: re-pose, re-snapshot just those moments, and regenerate the one-pager. Keep the approved stills as they are. Once the person says go, the posed scenes become the film's scenes. Replace each sketch with its plate and animate.
