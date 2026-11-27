#!/usr/bin/env python3
"""Place a real product screenshot onto a green-screen phone in a locked-off plate.

    python3 phone_screen_comp.py --plate plate.mp4 --screen screen.png --seed 540,1035 --out plate-comp.mp4
        [--probe-time 0.5] [--tint 0.97,0.93,0.86] [--margin 16] [--crf 15]

- --seed: any pixel inside the green screen (x,y) on the probe frame.
- The green region connected to the seed is found, its four corners fitted, and the screenshot is
  perspective-warped into that quad. Green is keyed only inside the phone's box, so hands in front stay
  in front; green spill on fingertips is removed. --tint multiplies the screen's RGB to sit it in the
  plate's light (1,1,1 = untouched).
Needs numpy, Pillow and ffmpeg/ffprobe on PATH. The phone must not move during the take.
"""
import argparse, json, subprocess, sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter


def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,r_frame_rate", "-of", "json", path])
    s = json.loads(out)["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return int(s["width"]), int(s["height"]), float(num) / float(den), s["r_frame_rate"]


def frame_at(path, t, W, H):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1",
                                   "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    return np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(int)


def green_region(a, seed):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (g > 100) & (g > r + 35) & (g > b + 35)
    x, y = seed
    if not m[y, x]:
        sys.exit(f"seed {seed} is not on the green screen (rgb {a[y, x].tolist()}); pick a point inside it")
    H, W = m.shape
    seen = np.zeros_like(m)
    q = deque([(y, x)])
    seen[y, x] = True
    while q:
        cy, cx = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))
    return seen


def corners(mask, grow=1):
    """Fit a straight line to each edge (ignoring the rounded corners) and intersect them."""
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    rows = np.arange(int(y0 + 0.2 * (y1 - y0)), int(y1 - 0.2 * (y1 - y0)))
    w = x1 - x0  # top/bottom edges from the side bands only, so a notch or home bar doesn't bend the fit
    cols = np.concatenate([np.arange(int(x0 + 0.12 * w), int(x0 + 0.32 * w)), np.arange(int(x1 - 0.32 * w), int(x1 - 0.12 * w))])
    left = np.array([np.where(mask[r])[0].min() for r in rows])
    right = np.array([np.where(mask[r])[0].max() for r in rows])
    top = np.array([np.where(mask[:, c])[0].min() for c in cols])
    bottom = np.array([np.where(mask[:, c])[0].max() for c in cols])
    lx = np.polyfit(rows, left - grow, 1)      # x = a*y + b
    rx = np.polyfit(rows, right + grow, 1)
    ty = np.polyfit(cols, top - grow, 1)       # y = c*x + d
    by = np.polyfit(cols, bottom + grow, 1)

    def meet(xl, yl):
        a, b = xl
        c, d = yl
        y = (c * b + d) / (1 - c * a)
        return (int(round(a * y + b)), int(round(y)))

    quad = [meet(lx, ty), meet(rx, ty), meet(rx, by), meet(lx, by)]
    return quad, (x0, y0, x1, y1)


def persp_coeffs(dst, src):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plate", required=True)
    ap.add_argument("--screen", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", required=True, help="x,y inside the green screen")
    ap.add_argument("--probe-time", type=float, default=0.5)
    ap.add_argument("--tint", default="0.97,0.93,0.86")
    ap.add_argument("--margin", type=int, default=16)
    ap.add_argument("--crf", type=int, default=15)
    ap.add_argument("--key-low", type=float, default=25)
    ap.add_argument("--key-high", type=float, default=70)
    a = ap.parse_args()

    W, H, fps, rate = probe(a.plate)
    seed = tuple(int(v) for v in a.seed.split(","))
    mask = green_region(frame_at(a.plate, a.probe_time, W, H), seed)
    quad, (x0, y0, x1, y1) = corners(mask)
    print("screen quad TL,TR,BR,BL:", quad, "green px:", int(mask.sum()))
    X0, Y0 = max(0, x0 - a.margin), max(0, y0 - a.margin)
    X1, Y1 = min(W, x1 + a.margin + 1), min(H, y1 + a.margin + 1)

    scr = Image.open(a.screen).convert("RGB")
    sw, sh = scr.size
    warped = scr.transform((W, H), Image.PERSPECTIVE, persp_coeffs(quad, [(0, 0), (sw, 0), (sw, sh), (0, sh)]),
                           Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.6))
    tint = np.array([float(v) for v in a.tint.split(",")], np.float32)
    wbox = (np.asarray(warped).astype(np.float32) * tint)[Y0:Y1, X0:X1]

    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.plate, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", rate, "-i", "-", "-c:v", "libx264", "-crf", str(a.crf), "-preset", "slow",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.out], stdin=subprocess.PIPE)
    n = 0
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
        box = f[Y0:Y1, X0:X1].astype(np.float32)
        r, g, b = box[..., 0], box[..., 1], box[..., 2]
        k = np.clip((g - np.maximum(r, b) - a.key_low) / (a.key_high - a.key_low), 0, 1)[..., None]
        box[..., 1] = np.where(g > np.maximum(r, b), np.maximum(r, b), g)  # spill suppression
        f[Y0:Y1, X0:X1] = np.clip(box * (1 - k) + wbox * k, 0, 255).astype(np.uint8)
        enc.stdin.write(f.tobytes())
        n += 1
    enc.stdin.close()
    enc.wait()
    dec.wait()
    print(f"wrote {a.out}: {n} frames at {fps:.3f} fps")


if __name__ == "__main__":
    main()
