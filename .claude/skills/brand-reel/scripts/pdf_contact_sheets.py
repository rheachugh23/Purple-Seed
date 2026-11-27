#!/usr/bin/env python3
"""Render a brand-guidelines PDF into labelled contact sheets so every page can be looked at.

    python3 pdf_contact_sheets.py guidelines.pdf -o /tmp/brand-pages [--dpi 40] [--per-sheet 12] [--cols 3] [--pages 42-63]

Writes sheet-01.jpg, sheet-02.jpg, ... each holding up to --per-sheet pages with their page numbers.
Re-run with --pages and a higher --dpi (e.g. 90) for pages whose detail matters.
Needs pdftoppm (poppler-utils) and Pillow.
"""
import argparse, glob, os, re, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--dpi", type=int, default=40)
    ap.add_argument("--per-sheet", type=int, default=12)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--pages", help="e.g. 42-63")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tmp = tempfile.mkdtemp()
    cmd = ["pdftoppm", "-r", str(a.dpi), "-png"]
    if a.pages:
        f, l = a.pages.split("-")
        cmd += ["-f", f, "-l", l]
    subprocess.check_call(cmd + [a.pdf, os.path.join(tmp, "p")])
    files = sorted(glob.glob(os.path.join(tmp, "p-*.png")), key=lambda p: int(re.findall(r"(\d+)\.png$", p)[0]))
    try:
        fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except OSError:
        fnt = ImageFont.load_default()
    for s in range(0, len(files), a.per_sheet):
        chunk = files[s:s + a.per_sheet]
        ims = [Image.open(f).convert("RGB") for f in chunk]
        w, h = max(i.width for i in ims), max(i.height for i in ims)
        rows = (len(ims) + a.cols - 1) // a.cols
        sheet = Image.new("RGB", (a.cols * w, rows * h), "white")
        d = ImageDraw.Draw(sheet)
        for k, (im, f) in enumerate(zip(ims, chunk)):
            x, y = (k % a.cols) * w, (k // a.cols) * h
            sheet.paste(im, (x, y))
            n = re.findall(r"(\d+)\.png$", f)[0]
            d.rectangle([x, y, x + 64, y + 26], fill="black")
            d.text((x + 6, y + 3), f"p.{int(n)}", font=fnt, fill="white")
        out = os.path.join(a.out, f"sheet-{s // a.per_sheet + 1:02d}.jpg")
        sheet.save(out, quality=85)
        print("wrote", out)


if __name__ == "__main__":
    main()
