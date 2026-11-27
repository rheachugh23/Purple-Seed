# Compositing the brand layer onto AI plates

Every technique here keeps brand assets intact. It cuts out, places, keys, masks and recolours, but never redraws or regenerates.

## Real product screen on a green-screen phone

When a plate has a phone with a plain green screen and a still camera:

```bash
python3 <skill>/scripts/phone_screen_comp.py \
  --plate higgsfield/plate-2-desk.mp4 \
  --screen project/assets/screens/product-screen.png \
  --seed 540,1035 \
  --out project/assets/plates/plate-2-desk-comp.mp4
```

- `--seed` is any point inside the green screen, measured on the plate's first frame.
- The script finds the green region connected to the seed and fits its four corners. It then perspective-warps the screenshot into that quad and keys the green only inside the phone's box, so the hands and fingers stay in front.
- It also suppresses green spill on fingertips, and warms or dims the screen to the plate's light (`--tint 0.97,0.93,0.86` is warm late-afternoon; `--tint 1,1,1` is neutral).
- It prints the quad it found. Check a few frames, especially where hands pass close to the phone.
- Capture the product screen from the real product: a Playwright screenshot at the device size, with tours, cookie banners and chat widgets hidden by CSS. Crop it to the phone's aspect ratio (usually about 0.49).

## Cut-outs from flat-background images

For brand images supplied on a flat colour (an emailer screenshot, a render on a coloured card):

1. Run `npx hyperframes remove-background <image> -o <cutout.png>`. It uses a local model; if it needs `onnxruntime-node`, install it with `--onnxruntime-node-install-cuda=skip`.
2. If the model ghosts part of the subject (it can treat a coloured tree or prop as background), repair it:
   ```bash
   python3 <skill>/scripts/cutout_repair.py --source image.png --ai-cutout cutout.png --out cutout-fixed.png
   ```
   This adds back every pixel that clearly differs from the background colour (sampled from the border, or set with `--bg '#E8A501'`). It changes only transparency, never colours.
3. Place the cut-out on a ground close to its original background. A gold-backed image keeps a faint gold fringe and looks best on gold.

## Accessory layers (only when the client allows)

When the client allows, say, a seasonal hat on a standard mascot render:

- Lift the accessory from an official render that already wears it. Segment it by colour from a connected seed, cut away the mascot's own pixels under it, and remove thin outlines with a morphological opening.
- Place it as its own `<img>` over the untouched render, inside a wrapper with both, positioned in the render's pixel coordinates (percent of the render size). It can then be removed at any time.
- Trial it on the ground colour, and check that it sits snugly. It should cover the top of the head without floating above it, and be tilted the way the official seasonal renders tilt it.

## The brand device as background

- **Recolour by masking.** Mask the brand's vector shape with `mask: url(shape.svg) center / 100% 100% no-repeat` and set any brand colour as the `background`. For outlines, reuse the file's own path data with `stroke` and `vector-effect: non-scaling-stroke`.
- **Use it the way the guidelines do:** as large crops dividing the frame, a frame for a product or mascot, small props (baubles, confetti, snow) or punctuation, if the guidelines show it.
- **Animate a wrapper,** never the masked element itself. The element carries its rotation in CSS, and GSAP must not fight it.

## Reusing one plate across scenes

- Mount the same file in each scene with a different `data-media-start` (plate time = film time minus an offset), and wrap the `<video>` in an untimed div.
- For a continuous push-in, tween the wrapper's `scale` from scene to scene (1.00 → 1.03, 1.03 → 1.06, …) with the same transform origin.
- For a focus pull, use the blur treatment, not a CSS filter. Set `npx hyperframes media-treatment --file <scene> --selector '#plate' --grading '{"effects":{"blur":0.85}}' --apply`, put `style="--hf-color-grading-blur: 0"` on the video, then tween `'--hf-color-grading-blur'` 0 → 0.85 → 0.
- **Snapshots don't draw the treatment.** Confirm it with a short `render --start --end` draft.

## Titles over footage

Use the brand's light ink with a soft shadow (e.g. `0 6px 28px rgba(0,0,0,0.45)`), set in the calm zone the plate prompt asked for. If the plate came back busy there, prefer a gentle vignette through the media-treatment `details` before moving the type.
