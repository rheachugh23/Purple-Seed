# Sound, render and delivery

## Music

1. **Use the person's own licensed track first.**
2. **Otherwise, generate a bed on Higgsfield.** `models_explore` with `type: audio` lists the music models (e.g. `elevenlabs_music_v2_5`). Quote it with `estimate_audio_cost` (about 9 credits for 2 × 30 s), then generate one request. Write the prompt from the mood card: instruments, tempo in bpm, feeling, where it should lift (the cut into the brand world), how it should end ("resolves with a soft final chord at 30 seconds"), and "no vocals" when there's text to read.
3. **Measure it, since you can't hear it.** Run `npx hyperframes audio <file> --json` for duration, loudness (aim for about −16 to −14 LUFS and a true peak at or below −1 dBTP) and its moments, and `npx hyperframes beats <file> --json` for bpm and beat times. Move the key cut a few frames to land on a beat when it reads better.
4. **Place it** as one `<audio id="music" class="clip">` on its own track, `data-volume="1"`, with a short `data-fade-out`.

## Voiceover

Only when the script's VO column has lines. Many Reels play muted, so the on-screen text must still carry the film without the voice.

1. **Write the lines into the script first.** They should add to the on-screen words, not read them out. Follow the brand's tone of voice, and give the campaign line to the VO on the end card. Leave silent moments where the picture should breathe.
2. **Generate on ElevenLabs.** Use the hosted MCP (`https://api.elevenlabs.io/v1/mcp`, OAuth). Higgsfield's `generate_audio` with an ElevenLabs TTS model is the fallback.
   - **Choose a voice.** Run `creative_list_voices` with `languages` and the brand's accent, then pick a voice that fits the brief and say which one you picked. On a free account, prefer voices with `is_library_voice: false` (the account's own and premade voices).
   - **Quote and generate one take.** Use `creative_generate_speech` with `estimate_only: true` first. Then generate once with `generations_count: 1`, putting **every line in one prompt**, separated by `[long pause]`. One take keeps the read consistent and costs one generation. Use `eleven_v4` audio tags sparingly (`[warmly]`, `[happy]`, `[mischievously]`).
   - **Poll, don't resubmit.** Poll `creative_get_flow_run_status` until the take is ready, then download `content_url`. The file host is `elevenlabsusercontent.com`, so it must be allowed on the network.
3. **Cut the take into lines.**
   - Level the whole take first: high-pass at 80 Hz, a light compressor, gain to about −16 LUFS, and a limiter at −1.5 dBTP.
   - Find the pauses with `silencedetect=noise=-40dB:d=0.35` and map the speech chunks to the lines by length and syllables.
   - Cut each line inside its surrounding silence, with a 15 ms fade-in and a 60 ms fade-out.
   - Log the voice, model, prompt, cost and cut points in `assets/audio/vo/VO.md`.
4. **Place one `<audio>` per line,** each on the beat it belongs to, in a `voiceover` group (`data-audio-group="voiceover"` plus `<hf-audio-group id="voiceover"></hf-audio-group>`). Turn down any effects that land under a line.
5. **Make room in the music.**
   - Add a `volume` lane on the music: down to about 0.5 (−6 dB) under each line, and back up in gaps longer than about 1.5 s, especially on a big cut.
   - **Then carve it** with `node <media-use>/audio/scripts/carve.mjs --comp index.html --bed music --strength 0.5`. That cuts the voice's frequencies.
   - **Don't stack two ducks.** The carve also writes a broadband level dip (a `gain` node with an `fx.nN.gain` lane down to −12 dB) that recovers slowly. On top of the volume lane, it buried the music about 20 dB under the voice and kept it down in the gaps. Delete that one lane and keep the carve's EQ lanes and your own volume lane.
   - **Aim** for the voice about 11–15 dB above the music in each line.
   - **Measure before the long render.** `python3 <skill>/scripts/sim_mix.py index.html -o mix.wav` rebuilds the mix offline, and `--only music` or `--only vo-` writes a single stem. It ignores effects chains (the carve), so the music comes out a few dB louder than it will in the render. Check that the voice sits at least 7 dB above the music in every line (ebur128 on each line's window in both stems), and that the whole mix peaks below −1 dBTP.
   - **Measure the render, too.** For each line, project the render's audio onto the voice clip (least squares). The leftover is the music and effects under that line. The renderer also played the mono voice clips about 3 dB hotter than their files, so leave headroom for that.
6. **Licence.** ElevenLabs's free plan has no commercial licence. Before a client piece is posted, regenerate the same prompt on a paid plan and say so in the delivery note.

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
