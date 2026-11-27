#!/usr/bin/env python3
"""Repair an AI background-removal cut-out of an image that sat on a flat colour.

    python3 cutout_repair.py --source chip.webp --ai-cutout chip-cutout.png --out chip-cutout-fixed.png [--bg '#E8A501']

The AI model sometimes ghosts parts of the subject that are coloured differently from the subject's main
body (a tree behind a mascot, a prop). This keeps the model's alpha and adds back every pixel that clearly
differs from the flat background colour (sampled from the border unless --bg is given). Only transparency
changes; the source colours are untouched. Needs numpy and Pillow.
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--ai-cutout", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--bg", help="background colour, e.g. '#E8A501'; default: median of the border")
    ap.add_argument("--low", type=float, default=38, help="colour distance treated as background")
    ap.add_argument("--high", type=float, default=85, help="colour distance treated as subject")
    a = ap.parse_args()

    src = np.asarray(Image.open(a.source).convert("RGB")).astype(np.float32)
    ai = np.asarray(Image.open(a.ai_cutout).convert("RGBA").resize((src.shape[1], src.shape[0])))[..., 3].astype(np.float32) / 255
    if a.bg:
        h = a.bg.lstrip("#")
        bg = np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)
    else:
        border = np.concatenate([src[:4].reshape(-1, 3), src[-4:].reshape(-1, 3), src[:, :4].reshape(-1, 3), src[:, -4:].reshape(-1, 3)])
        bg = np.median(border, axis=0)
    dist = np.sqrt(((src - bg) ** 2).sum(-1))
    key = np.clip((dist - a.low) / (a.high - a.low), 0, 1)
    alpha = (np.maximum(ai, key) * 255).astype(np.uint8)
    alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.MedianFilter(3)))
    Image.fromarray(np.dstack([src.astype(np.uint8), alpha]), "RGBA").save(a.out)
    print(f"background {bg.round().astype(int).tolist()}, wrote {a.out}")


if __name__ == "__main__":
    main()
