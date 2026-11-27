# REVIEW: Last day of term (v1 film, 27 Nov 2026)

## What was built
- **Length:** 30 s, 1080×1920 at 30 fps, for Instagram Reels.
- **Story:** storyline C, "Last day of term" (territory 2), built from the approved storyboard v4.
- **Act 1 (0–12.5 s):** two Higgsfield plates (Cinema Studio Video 3.0, 1080p, no audio).
  - **Plate 1:** classroom take A, using 2.4–4.9 s of it, so the phone lights up just before the cut.
  - **Plate 2:** desk take B, using 1.8–11.8 s of it across frames 2–4. It's a single locked-off take with a slow push-in in HyperFrames (scale 1.00 → 1.08 over 10 s).
  - **The phone screen** is the real Teacher demo Pot. The plate's green screen was measured (stable at x 441–638, y 842–1228). The screenshot was perspective-warped into it, keyed behind the hands, and warmed to the late-afternoon light, with spill suppressed on fingertips (`higgsfield/` source → `assets/plates/plate-2-desk.mp4`).
  - **Frame 3:** the desk softens with the HyperFrames blur treatment (`--hf-color-grading-blur` 0 → 0.85 → 0), not a CSS filter.
- **Act 2–3 (12.5–30 s):**
  - The White, Gold and Black Pot-shape grounds and Pot baubles and snow, all built from `potYellow.svg` and never redrawn.
  - Chip renders 121 and 139, each with a Santa-hat layer lifted from render 108.
  - The two Christmas emailer Chips, cut out.
  - The real No.1 Teacher card and the real Teacher Pot screens.
  - The campaign line "Teacher's gift made easy." on the end card.
- **Sound:**
  - **Music:** "festive felt piano and glockenspiel", 96 bpm, generated on Higgsfield with ElevenLabs Music v2.5.
  - **Effects:** 18 cues from the bundled Pixabay-licensed set (`assets/sfx/CREDITS.md`), placed so each peaks one frame after its picture.

## Measured, not only looked at
- **`check --safe-zone reels`:** ok, no errors.
  - Remaining warnings: "timeline_track_too_dense" only, which is structural and kept on purpose (one scene per storyboard frame).
- **Music:** 30.04 s, 95.9 bpm, −15.7 LUFS integrated, −1.3 dBTP true peak, no clipping.
  - It has a beat at 12.56 s, against the cut to Gold at 12.5 s.
- **The rendered file:** checked with `hyperframes audio` after the render; see the delivery note.
- **The sound was measured, not heard.** Nobody has listened to the mix yet.

## Looked at
- Beat, seam and phone-width sheets (`snapshot --review`).
- A 1 s draft render to confirm the blur treatment shows up in real renders. Snapshots don't draw it.

## Weakest shot, and what I'd change with more time
- **The titles over the desk plate (frames 2–4)** sit over a busy top third (the paper chain and mug), because the model didn't keep that area plain. They read, thanks to the 0.45 shadow, but a soft top vignette (media-treatment `details.vignette`) or a regenerated plate with a clearer top would be cleaner.
- **The two emailer Chips (frames 7–8)** are upscaled from about 1,100 px screenshots and look slightly soft. The brand team's full-size originals would fix it.
- **Chip's pop-in** has a 3-frame opacity ramp that can read as a ghost on a paused frame. It's invisible at speed.

## Kept on purpose
- **No voiceover:** Reels autoplay muted.
- **The "timeline_track_too_dense" warnings:** kept as noted above.
