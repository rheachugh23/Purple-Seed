#!/usr/bin/env python3
"""Render a one-page storyboard image: title, subtitle, then the frames in a grid in film order,
each with a time pill (brand accent), the speaker and the VO cue underneath.

    python3 storyboard_onepager.py boards/onepager.json -o boards/storyboard-onepager.png \
        [--title-font Brand-Display.otf] [--body-font Brand-Regular.ttf] [--bold-font Brand-SemiBold.ttf] [--scale 2]

Manifest (paths relative to the manifest file):
{
  "title": "Last day of term · Collection Pot · storyboard",
  "subtitle": "9:16 · 30 s · ...",
  "accent": "#F9B910", "ink": "#2F2F32", "background": "#FBFAF6",
  "columns": 5, "width": 1600,
  "frames": [{"image": "stills/frame-00.png", "time": "0:00", "speaker": "VO", "cue": "So I'm class rep this year..."}]
}
Needs Pillow only.
"""
import argparse, json, os, re, sys
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = {
    "bold": ["/usr/share/fonts/opentype/inter/Inter-Bold.otf", "/usr/share/fonts/truetype/inter/Inter-Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/Library/Fonts/Arial Bold.ttf"],
    "semibold": ["/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", "/usr/share/fonts/truetype/inter/Inter-SemiBold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/Library/Fonts/Arial Bold.ttf"],
    "regular": ["/usr/share/fonts/opentype/inter/Inter-Regular.otf", "/usr/share/fonts/truetype/inter/Inter-Regular.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/Library/Fonts/Arial.ttf"],
}
EMOJI = re.compile("[\U0001F000-\U0001FFFF☀-➿️‍]")


def font(path, kind, size):
    for p in ([path] if path else []) + FONT_CANDIDATES[kind]:
        if p and os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--title-font")
    ap.add_argument("--body-font")
    ap.add_argument("--bold-font")
    ap.add_argument("--scale", type=float, default=2.0)
    a = ap.parse_args()

    m = json.load(open(a.manifest))
    base = os.path.dirname(os.path.abspath(a.manifest))
    S = a.scale
    W = int(m.get("width", 1600) * S)
    cols = int(m.get("columns", 5))
    margin, gap, row_gap = int(22 * S), int(18 * S), int(44 * S)
    bg, ink, accent = hex_rgb(m.get("background", "#FBFAF6")), hex_rgb(m.get("ink", "#2F2F32")), hex_rgb(m.get("accent", "#F9B910"))
    sub_ink = tuple(int(c + (255 - c) * 0.38) for c in ink)
    cue_ink = tuple(int(c + (255 - c) * 0.12) for c in ink)

    f_title = font(a.title_font or a.bold_font, "bold", int(40 * S))
    f_sub = font(a.body_font, "regular", int(19 * S))
    f_pill = font(a.bold_font, "bold", int(19 * S))
    f_speaker = font(a.bold_font, "semibold", int(18 * S))
    f_cue = font(a.body_font, "regular", int(17 * S))

    card_w = (W - 2 * margin - (cols - 1) * gap) // cols
    frames = m["frames"]
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    # lay out
    items = []
    for fr in frames:
        im = Image.open(os.path.join(base, fr["image"])).convert("RGB")
        h = int(card_w * im.height / im.width)
        im = im.resize((card_w, h), Image.LANCZOS)
        cue = EMOJI.sub("", fr.get("cue", "")).strip()
        cue_lines = wrap(probe, f"“{cue}”", f_cue, card_w) if cue else []
        items.append((im, fr.get("time", ""), EMOJI.sub("", fr.get("speaker", "")).strip(), cue_lines))

    pill_h = int(34 * S)
    line_h = int(24 * S)
    head_h = int(40 * S) + int(14 * S) + int(26 * S) + int(26 * S)
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    row_heights = []
    for row in rows:
        img_h = max(it[0].height for it in row)
        text_h = pill_h + int(12 * S) + max(len(it[3]) for it in row) * line_h
        row_heights.append((img_h, text_h))
    H = margin + head_h + sum(ih + th for ih, th in row_heights) + row_gap * (len(rows) - 1) + margin

    page = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(page)
    y = margin
    d.text((margin, y), m.get("title", ""), font=f_title, fill=ink)
    y += int(40 * S) + int(14 * S)
    d.text((margin, y), m.get("subtitle", ""), font=f_sub, fill=sub_ink)
    y += int(26 * S) + int(26 * S)

    border = tuple(int(c * 0.9) for c in bg)
    for row, (img_h, text_h) in zip(rows, row_heights):
        for c, (im, time, speaker, cue_lines) in enumerate(row):
            x = margin + c * (card_w + gap)
            page.paste(im, (x, y))
            d.rectangle([x, y, x + card_w - 1, y + im.height - 1], outline=border, width=max(1, int(S)))
            ty = y + img_h + int(14 * S)
            # time pill
            tw = d.textlength(time, font=f_pill)
            pw = int(tw + 26 * S)
            d.rounded_rectangle([x, ty, x + pw, ty + pill_h], radius=pill_h // 2, fill=accent)
            tb = d.textbbox((0, 0), time, font=f_pill)
            d.text((x + (pw - tw) / 2, ty + (pill_h - (tb[3] - tb[1])) / 2 - tb[1]), time, font=f_pill, fill=ink)
            sb = d.textbbox((0, 0), speaker, font=f_speaker)
            d.text((x + pw + int(12 * S), ty + (pill_h - (sb[3] - sb[1])) / 2 - sb[1]), speaker, font=f_speaker, fill=ink)
            cy = ty + pill_h + int(12 * S)
            for ln in cue_lines:
                d.text((x, cy), ln, font=f_cue, fill=cue_ink)
                cy += line_h
        y += img_h + text_h + row_gap

    page.save(a.out, optimize=True)
    print(f"wrote {a.out} ({W}x{H}, {len(frames)} frames)")


if __name__ == "__main__":
    sys.exit(main())
