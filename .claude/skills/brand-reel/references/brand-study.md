# Studying a brand before making anything

The film will be judged against the brand's own guidelines by people who know them by heart. Read everything once, carefully, and write down what you learned, so the build never has to guess.

## 1. Gather the sources

Look in the repo first (`<brand>/brand/`, `guidelines/`, `references/`, `logos/`, `mascot/`, `fonts/`), then ask for anything missing:

- the guidelines PDF (or Figma, or a brand site);
- logo files in every supplied version;
- mascot or character files, including seasonal versions;
- fonts and their licence notes;
- the brand device (a signature shape, pattern or frame) as a vector;
- icons;
- product UI: live product URLs you can capture, or screenshots they send;
- printed items (cards, packaging);
- website captures and past campaigns.

## 2. Read every page

```bash
python3 <skill>/scripts/pdf_contact_sheets.py guidelines.pdf -o /tmp/<brand>-pages --dpi 40 --per-sheet 12
pdftotext -layout guidelines.pdf /tmp/<brand>-guidelines.txt    # for exact wording, numbers and hex values
```

Open every contact sheet. Re-render single pages at a higher DPI (`--pages 42-44 --dpi 90`) where the detail matters: logo construction, colour tables, type specimens, mascot rules, layout examples. Take numbers from the text (hex values, tracking, minimum sizes), not from the pictures. Where the PDF contradicts itself, note it and use the more specific source.

## 3. Write the digest: `brand/BRAND.md`

Keep it short enough to reread before every video, and cite page numbers so the PDF stays the authority. Sections:

1. **Strategy:** promise, positioning, personality, audience.
2. **Tone of voice:** traits, words to use and avoid, the copy bank, name and product casing rules, internal-only lines that must never appear in comms.
3. **Communication territories**, if the brand has them, with example angles.
4. **Logo:** versions, approved colour pairs, clear space, minimum sizes, logo motion, misuse.
5. **Mascot or character:** personality, voice, which files exist, allowed backgrounds, expressions and poses, scene and accessory rules, motion rules, 2D/3D mixing rules, and the fact that it is never AI-generated or off-model.
6. **Colour:** hex/RGB per colour, hero vs secondary, where each may appear (e.g. "secondary never on the hero colour").
7. **Typography:** display, body, subhead and button faces with their settings, and text motion principles with minimum hold times.
8. **Brand device:** what it is, where the vector file is, and how the guidelines use it (crops, dividers, punctuation, icon base, props).
9. **Iconography and illustration:** what exists and when to use it.
10. **Layout:** grids and examples worth borrowing for 9:16.

Also add `tokens.css` (colours, font faces from local files, type classes) if it doesn't exist. Every composition will link or copy it.

## 4. The asset inventory

Write a table of every usable file, with columns for path, what it shows, its resolution, whether it has a transparent background, and notes such as "seasonal", "low-res screenshot" or "use only on light grounds". This table is the film's whole brand vocabulary: if it isn't in the inventory, it isn't in the film.

For mascots with many renders, make a contact sheet of the candidates on the brand's ground colour and look at it before choosing poses. Group them by mood (happy, neutral, wink, seasonal) and by props (phone, gift, card).

## 5. Feedback becomes rules

When the client corrects something (too much of one colour, type too playful, an asset they consider off-model, a campaign line to carry), write it under the brand's section in the repo's `CLAUDE.md`, phrased as a rule with the reason. That file loads in every future session, so the next video starts where this one finished.

## 6. Ask, don't guess

If a rule is ambiguous or an asset is missing (for example, no stacked logo, unknown font licence or no seasonal mascot), ask once and say what you'll do meanwhile. A lookalike is never the fallback.
