# Higgsfield plates: the credit-efficient recipe

## 0. Make sure you can generate

- The tools you need are `generate_video_batch`, `estimate_video_cost`, `jobs_wait`, `show_generations` and `models_explore`. They come from Higgsfield's **full** MCP server, `https://mcp.higgsfield.ai/mcp`, which is added on claude.ai under Settings → Connectors → Add custom connector and then signed in with the Higgsfield account.
- A connector named "Higgsfield AI" pointing at `claude-mcp.higgsfield.ai` is the Claude Motion importer. It only reads balance, history and models, and can't generate. If that's all there is, tell the person how to add the full one, and that a new session may be needed for its tools to load.
- Generated files download from Higgsfield's CDN (a `*.cloudfront.net` host shown in each result URL). In a sandbox with a network allowlist, that host must be allowed before you can pull clips into the project.
- Generations spend the account's plan credits. Check `balance` before you plan.

## 1. Plan the fewest plates

Plates are expensive, and HyperFrames is free. Decide what truly needs live action:

- **One locked-off take can serve several shots.** For example, one 12 s overhead desk take served three scenes, with a focus pull and a push-in added in HyperFrames, each scene trimmed with `data-media-start`. Camera moves (push-ins, crops, punch-ins) can be added afterwards on a wrapper.
- **Generate only the seconds you use,** plus about 1 s of handle. Respect the model's minimum duration.
- **Anything the brand owns stays out of the plate:** text, UI, logos, mascots, packaging. Those are added later from the real files.
- **Reuse before you generate.** `show_generations` may already hold a usable clip from earlier work.

## 2. Pick the model and settings

- `models_explore` (`list`, `type: video`) gives the current shortlist; `get` gives one model's durations, aspect ratios and parameters.
- For cinematic realism, Cinema Studio Video 3.0 (`cinematic_studio_3_0`) has worked well: `aspect_ratio` 9:16, `resolution` 1080p (not 4K unless the delivery needs it), `generate_audio` false (the film has its own sound), and a `genre` that suits the mood.
- Quote every plate with `estimate_video_cost` and add up the total. For reference, at the time of writing 1080p cost about 13 credits per second (5 s = 65, 12 s = 156).

## 3. Write prompts for compositing

Describe one continuous shot in plain language: place, time of day, light direction and colour, the props (only those the story needs), the exact action with timings ("at about one second… around eight seconds in…"), and the camera ("locked-off overhead", "slow dolly push forward", lens, depth of field). Then add the compositing needs:

- **A clear title zone.** "Keep the top third of the frame calm and plain … to leave room for titles."
- **People per the brand's rules.** When faces aren't allowed or you're unsure: "Only hands and forearms are ever in frame, never a face or head", "No people anywhere".
- **No brand-like content.** "No text, letters or writing anywhere, no logos, no posters with words".
- **Screen replacement.** "a smartphone lies face up … with a plain bright green screen; the phone never moves … hands … not touching it". Ask for a locked-off camera.
- **Realism guards.** "Realistic skin, five fingers on each hand".

Most of these models have no negative-prompt field, so put the "no …" clauses in the prompt itself. Save every prompt in `higgsfield/PROMPTS.md` before generating.

## 4. Generate once

1. Tell the person the plan and the quoted total. If it exceeds what they authorised, wait for a yes.
2. Submit all plates in **one** `generate_video_batch` call, one request per plate (`count` 1). No alternate takes "to pick from".
3. Wait with `jobs_wait` in short polls. While you wait, build the brand frames, which don't depend on the plates.
4. **Never resubmit after a timeout or a lost response.** The job usually exists. Poll its ID, and only resubmit once you know it failed.
5. Download each `result_url` into `higgsfield/` with a descriptive name (`plate-2-desk.mp4`), and probe it with ffprobe (size, fps, duration).

## 5. Review before you build on it

Extract frames across the clip (`ffmpeg -ss <t> -frames:v 1`) and lay them out side by side. Check:
- no faces or people beyond what's allowed;
- no readable text or logos;
- the action happens and when (note the plate times);
- the camera holds still where a screen will be replaced;
- the title zone is calm;
- hands are anatomically sound.

If a plate fails, fix the prompt for that failure only, state the cost, and regenerate that plate alone. One clean take is the goal, not a contact sheet of options.

## 6. Log it

Add a generation log to `higgsfield/PROMPTS.md`:

| File | Model | Settings | Credits | Used? |
|---|---|---|---|---|
| `plate-1-classroom.mp4` | Cinema Studio Video 3.0 | 9:16, 1080p, 5 s, drama, no audio | 65 | Yes: frame 1 (2.4–4.9 s) |

Copy the used plates into `project/assets/plates/`. Keep the downloaded originals in `higgsfield/`, and record each plate's in and out points as you cut it.
