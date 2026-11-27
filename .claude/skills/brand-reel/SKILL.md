---
name: brand-reel
description: Make short branded social videos (Instagram Reels, TikToks, Shorts, paid social, story ads) that combine AI-generated live-action clips from Higgsfield with on-brand motion-graphic frames built in HyperFrames. Covers the whole pipeline. It runs from a brief or campaign (emailer, landing page, idea) through a thorough brand-guideline study, storylines and a 4-column script (Timing · What happens on the screen · VO · On screen text), and a one-page storyboard image the person approves, to credit-efficient Higgsfield plates and a composited, animated, scored and rendered film. Works for any brand. Use it whenever someone wants a video, reel, ad or social post for a brand or campaign, asks for a script or storyboard for a brand video, wants to turn an emailer or campaign into a video, or mentions Higgsfield together with HyperFrames, even if they don't name this skill.
---

# Brand reel: AI clips + brand graphic frames

A brand reel has two layers, and keeping them apart is what makes it work:

1. **Live-action plates** generated on Higgsfield: rooms, desks, hands, objects, places, light. They carry the feeling and the real-world moment.
2. **The brand layer** built in HyperFrames: type, mascot, logo, product screens, printed items and the brand's own shapes. It carries the message, and **every element comes from the brand's own files.**

AI never makes a brand asset. A mascot, logo, icon, font, product UI or packaging that the brand owns is used from its original file, every time. The AI only makes what the brand has no file for: the world around it.

This skill orchestrates; HyperFrames does the building. Load the `hyperframes` skill (and `hyperframes-cli` / `media-use` as needed) before building, and follow its contract.

## The gates

The person approves each stage before the next one starts. Skipping a gate wastes their money and time, because Higgsfield credits are spent and rendering takes long.

| Stage | You deliver | Gate |
|---|---|---|
| 1. Brand study | `BRAND.md` digest + asset inventory (refresh if one exists) | Ask about anything ambiguous |
| 2. Brief + mood | `source-*.md` (brief verbatim) + a 5-line mood card | — |
| 3. Script | `STORYLINES.md` (3 options) → locked `SCRIPT.md` in the 4-column format | **Go on the script** |
| 4. Storyboard | One-page storyboard **image** + planned plates with quoted credits | **Go on the storyboard: nothing is generated before this** |
| 5. Plates | Higgsfield clips, one take each, logged | — |
| 6–7. Build + sound | Animated HyperFrames film with music and SFX | — |
| 8. Deliver | Rendered MP4, `REVIEW.md`, short delivery note | Feedback round |

## Workspace

Each brand gets its own folder. If the repository already has conventions (a `CLAUDE.md`, a brand README, a `Videos/README.md`), follow those instead. Otherwise use:

```
<brand>/
├── brand/                     guidelines PDF, BRAND.md digest, logos/, mascot/, icons/, fonts/, references/
└── Videos/YYYY-MM-<slug>/     one folder per video
    ├── README.md              brief, channel, format, territory, campaign line, status
    ├── source-*.md            the brief / emailer copy, verbatim
    ├── STORYLINES.md          the options; SCRIPT.md is the locked one
    ├── higgsfield/            PROMPTS.md (prompts + generation log) and the clips
    ├── project/               the HyperFrames project (SPEC.md, STORYBOARD.md, boards/, compositions/, assets/)
    └── export/                final renders, with a .gitignore for render scratch (work-*/)
```

## 1. Study the brand before any visual

Read **all** of the brand's guidelines before writing a word of script. That means the PDF page by page (render it to contact sheets with `scripts/pdf_contact_sheets.py` and look at every sheet), the website captures and the asset folders. A guideline you skimmed is a rule you will break. `references/brand-study.md` has the checklist. In short, write or refresh `brand/BRAND.md` with:

- strategy, promise, tone of voice, copy bank, words to use and avoid, name casing;
- **communication territories**, if the brand has them (each script names one; options spread across them);
- logo rules: versions, approved colour pairs, clear space, minimum size, logo motion;
- mascot or character rules: which files exist (including seasonal versions), allowed backgrounds, expressions, poses, what may and may not be changed;
- colour: primary vs secondary, and where each may and may not appear;
- type: display/body/button faces and their settings, plus text motion;
- brand devices (a signature shape, pattern or frame) and how the guidelines use them;
- layout examples worth borrowing, and the don'ts.

Then make an **asset inventory**: every usable file with its path. The film may only use brand elements from this list. Record the client's feedback as durable rules under the brand's section in the repo's `CLAUDE.md`, so later videos inherit it.

## 2. Read the brief, set the mood

Copy the source (emailer, campaign page, brief) into `source-*.md` verbatim. Find the **campaign line** and make sure the video carries it, so the campaign reads as one across channels. Then write a five-line **mood card** from *this* brief, never from the last video:

1. **Occasion and season:** Christmas, back-to-school, summer, a launch, or evergreen.
2. **Emotional temperature:** heartfelt, witty, calm, urgent.
3. **Light and palette balance:** the plate lighting, and how the brand colours share the frame.
4. **Props and accents:** seasonal only when the brief is seasonal, and built from the brand's own devices where possible.
5. **Sound:** the music's feel and tempo.

Seasonal looks follow the asset rules. Use the brand's own seasonal mascot versions when they exist. Otherwise use a standard render plus at most one seasonal accessory layer, and only if the client allows it. Evergreen briefs get none of it.

## 3. Storylines and the script

Write three storylines that are different films, not three titles on one film. Each has its own world, device and form. Spread them across the brand's territories, recommend one, and save `STORYLINES.md`. The `hyperframes` skill's `references/story.md` covers the craft.

The locked script is **always** this table, in this column order. Leave a cell empty when it isn't needed (e.g. no VO). Put sound, music and production notes under the table, never in extra columns:

| Timing | What happens on the screen | VO | On screen text |
|---|---|---|---|
| 0.0–2.5s | **[Higgsfield 1]** Empty classroom at 3:31pm, slow push to the teacher's desk; a phone lights up. | | **Last day of term. 3:31pm.** |

Rules for the script:
- Put the territory, format and campaign line at the top.
- Mark every AI shot `[Higgsfield N]`; the same N can serve several rows.
- Use the client's copy verbatim and follow the brand's casing rules.
- Keep lines to six words or fewer, and give each line about 0.5 s plus 0.3 s per word (at least 2 s).

Stop for the go. `references/script.md` has more.

## 4. The storyboard: a one-page image, before any generation

Pose every shot in the HyperFrames project at its key moment, in the real fonts, colours and assets. Show each planned AI plate as a cheap labelled **sketch** in the frame, so the person approves the composition without anything being generated. Snapshot the stills, write `STORYBOARD.md`, then make the **one-pager**:

```bash
python3 <skill>/scripts/storyboard_onepager.py boards/onepager.json -o boards/storyboard-onepager.png
```

The one-pager is a single image:
- a title (`<video> · <brand> · storyboard`) and a subtitle (`9:16 · ~30 s · …`);
- the frames in a grid, one after another (5 per row for 9:16);
- under each frame, the **timestamp pill** in the brand accent, the **speaker** (`VO`, a character's name, or `TEXT` when there's no VO), and the **VO cue** in quotes (the on-screen line when there's no VO).

`references/storyboard.md` has the manifest format and how to pose frames.

Send the image itself (SendUserFile or an attachment), plus the plate plan: each Higgsfield plate's prompt, model, duration and **quoted credits**. Then stop. Generation starts only after the go. Notes on frames change only those frames.

## 5. Higgsfield plates, without wasting credits

Credits are the person's money. `references/higgsfield.md` has the full recipe. The essentials:

- **The right connector.** Generation needs the full Higgsfield MCP (`https://mcp.higgsfield.ai/mcp`, with tools such as `generate_video_batch`, `estimate_video_cost` and `jobs_wait`). The "Claude Motion" connector (`claude-mcp.higgsfield.ai`) can only read the account. Results download from Higgsfield's CDN host, so it must be allowed on the network.
- **Plan fewer, longer plates.** One locked-off take can serve several shots. Trim it per scene with `data-media-start`, and generate only the seconds the edit needs.
- **Check history first** (`show_generations`) for a clip that already fits.
- **Quote everything** (`estimate_video_cost`), tell the person the total, then submit all plates in **one** `generate_video_batch`, **one take per plate**. Don't generate alternates "to pick from".
- **Never resubmit on a timeout.** Wait on the job IDs; a lost response doesn't mean a lost job.
- **Regenerate only a plate that fails review.** Fix the prompt first, say what it will cost, and regenerate that plate alone.
- **Write prompts for compositing.**
  - No text, logos, brand items or mascots; the brand layer adds those.
  - People only as the brand and brief allow (when unsure, hands and places, no faces).
  - A calm area where titles will sit.
  - A locked-off camera and a plain green screen wherever a real product screen will be placed.
- **Log every generation** in `higgsfield/PROMPTS.md`: file, model, settings, credits, and whether it was used.

## 6. Build the film

Follow the `hyperframes` skill's contract and work loop, plus the brand rules from step 1:

- **Brand elements come from the asset inventory, unaltered.**
  - Cutting a mascot image out of its background is fine. Redrawing, restyling, AI-generating or AI-animating it is not.
  - Brand shapes come from the brand's own vector file, recoloured or masked, never redrawn.
  - Product screens are captured from the real product.
- **Composition follows the guidelines.** Typically that means balanced colour fields, never one flat colour; the brand's device as crops and dividers; the type settings as written; and the platform's safe zone (`check --safe-zone reels|tiktok|shorts`).
- **Compositing** recipes are in `references/compositing.md`:
  - green-screen phone replacement (`scripts/phone_screen_comp.py`);
  - cutout repair for flat-background images (`scripts/cutout_repair.py`);
  - accessory layers;
  - the blur treatment for focus pulls;
  - reusing one plate across scenes.
- **Motion follows the brand's motion principles.** Keep the mascot's movement within its rules (usually pop, slide and gentle sway, never stretching).

## 7. Sound

The person's own track comes first. Otherwise, generate a bed on Higgsfield (ElevenLabs Music is inexpensive; quote it first). Then measure it with `npx hyperframes audio` and `beats`, and land the key cuts on its beats. Add a few exact SFX on visible actions, each peaking one frame after its picture.

When the script has VO, record the lines in **one** ElevenLabs take (quoted first), cut it at its pauses, and place each line on its beat. Duck and carve the music under the voice, and measure the mix before rendering. A free ElevenLabs plan isn't licensed for commercial posting.

`references/sound-and-render.md` has the levels, placement and the voiceover recipe.

## 8. Review, render, deliver

1. Run `check --json --safe-zone <platform>` and fix every error.
2. Run `snapshot --review`, write `REVIEW.md`, and fix P0s and worthwhile P1s.
3. Render with `--quality delivery` in the background; a 30 s film with footage and effects takes a while.
4. Verify the file with ffprobe and `npx hyperframes audio`.
5. Make sure `export/.gitignore` ignores the render scratch before you commit.
6. Deliver the MP4 with a short note: what was made, what each plate cost, what was measured and what wasn't (the sound was measured, not heard), and the weakest shot.
7. Commit and push per the repo's rules.

## Asset rules, in one place

- Use the files the brand supplied, exactly. When a needed asset is missing, ask for it. Don't make a lookalike.
- Mascots and characters, logos, icons, fonts, product UI and printed items are never AI-generated, re-drawn or animated by an AI video model.
- Supplied images that are small or low-res may be used, but say so and ask for originals.
- When the person corrects a visual choice, write the correction into the repo's `CLAUDE.md` for that brand, so the next video starts from it.
