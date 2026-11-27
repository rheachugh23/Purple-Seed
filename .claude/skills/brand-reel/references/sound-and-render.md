# Sound, render and delivery

## Music

1. **Use the person's own licensed track first.**
2. **Otherwise, generate a bed on Higgsfield.** `models_explore` with `type: audio` lists the music models (e.g. `elevenlabs_music_v2_5`). Quote it with `estimate_audio_cost` (about 9 credits for 2 × 30 s), then generate one request. Write the prompt from the mood card: instruments, tempo in bpm, feeling, where it should lift (the cut into the brand world), how it should end ("resolves with a soft final chord at 30 seconds"), and "no vocals" when there's text to read.
3. **Measure it, since you can't hear it.** Run `npx hyperframes audio <file> --json` for duration, loudness (aim for about −16 to −14 LUFS and a true peak at or below −1 dBTP) and its moments, and `npx hyperframes beats <file> --json` for bpm and beat times. Move the key cut a few frames to land on a beat when it reads better.
4. **Place it** as one `<audio id="music" class="clip">` on its own track, `data-volume="1"`, with a short `data-fade-out`.

## Sound effects

Use few, exact effects, each with a cause on screen: a pop for a card or sticker landing, a whoosh for a big cut or a large move, a chime for the logo, a click for a button. The `media-use` skill bundles a small Pixabay-licensed set (`audio/assets/sfx/`, with `manifest.json` and `CREDITS.md`). Copy what you use into `assets/sfx/` along with its credits.

- **Align peaks.** Measure each effect's peak with `npx hyperframes audio <sfx> --json` (`moments.peak`). Then set start = visual moment − peak + one frame.
- **Rotate takes of a repeated effect.** For example, make a pitch variant with `ffmpeg -af "asetrate=44100*1.12,aresample=44100"`.
- **Keep them under the music.** Use `data-volume` of 0.2–0.4, one effects lane, and a second lane only where two overlap.

## Render

- Run `check --json --safe-zone <platform>` and fix every error, then `snapshot --review`, then write `REVIEW.md`.
- **Before the first render,** add `export/.gitignore` with `work-*/` and `.*.hf-transaction-*/`. The renderer writes its scratch there, and an `add -A` will otherwise sweep it into a commit.
- **Render in the background,** because footage plus effects falls back to a slower capture path and 30 s can take 30–40 minutes:
  ```bash
  npx hyperframes render --quality delivery -o ../export/<slug>_1080x1920.mp4 > render.log 2>&1; echo "EXIT $?" >> render.log
  ```
  Build or commit other work meanwhile, and wait for the background notification.
- **Verify the file.** ffprobe should report 1080×1920, 30 fps and the root duration. Run `npx hyperframes audio <video> --json` (sound present, loudness in range), and look at decoded frames from each act.

## Deliver

- Send the MP4 (SendUserFile, `display: render`).
- Add a short note covering:
  - what was made;
  - the plates used and their credits;
  - what was measured and what wasn't (the sound was measured, not heard);
  - the weakest shot and the fix you'd make;
  - anything the client should supply, such as high-res originals.
- Commit and push the project, the plates, the log and the export, per the repo's rules.
