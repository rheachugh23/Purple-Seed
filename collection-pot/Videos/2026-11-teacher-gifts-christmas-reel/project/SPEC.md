# SPEC: Last day of term (Collection Pot, teacher gifts Reel)

GOAL:    The viewer feels how much one Pot from the whole class means to a teacher, then sees how simple it was to make, and taps CREATE A POT.
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps, Instagram Reels
TIME:    29.5 s x 30 = 885 frames. Bed ~96 bpm (1 beat = 18.75 frames); the cut to Gold lands on a downbeat.
TERRITORY: 2. Gifting is better when done together

LOOK:
- Two worlds, one cut between them at 12.5 s:
  1. The receiver's world (0–12.5 s): live-action Higgsfield plates. A real UK classroom at 3:30pm in December, low winter sun from the left, warm 3200K practicals (fairy lights), shallow depth of field. No faces: hands at most.
  2. Chip's world (12.5–29.5 s): flat brand fields, never all-Gold. Each frame mixes Wedding White #FFFCF8, Pot of Gold #F9B910 and at most one Work Bash Black #2F2F32 shape, divided by big crops of the real Pot shape (`assets/pot/pot.svg`, the site's potYellow.svg, recoloured, never redrawn).
     - F5: White with a Gold crop.
     - F6: Gold with a White crop.
     - F7: White with a Black Pot.
     - F8–F9: Gold with a White Pot turned over as a snowy hill.
- Festive, built from the Pot:
  - Pot baubles hanging on strings from the top edge: Red dark #B03D3D, Green dark #37B051 or Gold, on White only.
  - Pot "snow": small White Pots, 18–44 px, rotated, on Gold or Black only.
  - Chip always in his Santa hat (renders 143, 141, 2, 107).
- Ink:
  - On Gold and White, Work Bash Black carries every word.
  - On footage, Wedding White carries every word, with a 0 6px 28px rgba(0,0,0,0.35) shadow.
  - Message pills use 50% tints (pink, turquoise, sand, green) or White, with Black ink. They sit on footage only.
- Accent: a Gold Pot full stop on headlines (Black on Gold grounds).
- Display face: Faro Display Lucky, two settings (brand p.50):
  - Standard: sentence case, letter-spacing -0.01em, line-height 1.0, 104–120 px.
  - Expressive: 1–2 words only, letters tilted ±3–9°, lifted ±0.08em and scaled 0.95–1.10, at 136–210 px, with a small standfirst above (66–88 px).
- Body face: Inter. Sublines are Inter 600 at 42 px. Message names are Inter 600 at 28 px, messages Inter 400 at 32 px.
- Stickers and buttons: Inter 600, UPPERCASE, letter-spacing +0.025em, 40 px, Black pill with Wedding White text.
- Chip: official 3D renders only (`assets/chip/`), on Gold or White, never over the Black shape. He fills 30–45% of the frame height.
- Product: the real Teacher Pot screens (`assets/screens/`) and the real printed No.1 Teacher card (`assets/card/`).
- Contact shadow under Chip and the card: an ellipse, rgba(10,10,10,0.16), blur 16 px.

OBJECTS:
- Phone: black body, 44 px corner radius, 14 px bezel, the real Pot screen inside.
- Message card: Wedding White, 32 px radius, 36 px padding, the first name in Inter 600 above the message.
- Printed card: the real PNG at a -5° tilt, with a contact shadow.
- Logo: `assets/logo/collection-pot-logo-linear-black.svg`, 560 px wide (above the 300 px minimum), Black on Gold.

MOTION:
- Enter: expo.out over 14 frames. Text lines arrive one at a time, rising 40 px from below the baseline ("Longer text" style).
- Chip: a pop-in with back.out(1.6) over 12 frames, then a gentle sway of ±1.5° over 90 frames. No stretching.
- Camera: a slow push on plates (scale 1.00 → 1.06 over the shot), sine.inOut.
- Cut to Gold: a hard cut on the downbeat.
- Logo: the Pot pops into the "O" (brand motion), then the letters reveal from behind it.
- Holds: every line stays on screen at least 2 s after it lands.

SHOTS:
| # | Time | Hero move | Reads (window) | Sound | Hand-off |
|---|---|---|---|---|---|
| F1 | 0.0–2.5 | Push towards the desk; the phone lights up at 1.2 s | "Last day of term." (0.2–2.5), "3:31pm" tag (0.6–2.5) | Room tone, a distant school bell at 0.3 s, a phone buzz at 1.2 s | The phone's light motivates the cut to above |
| F2 | 2.5–5.5 | Hands enter and rest either side of the phone | "From the whole class." (2.8–5.5) | Soft hand-on-wood foley; the bed begins (felt piano) | The phone screen is the source of F3 |
| F3 | 5.5–10.0 | Message cards rise out of the phone, one every 0.9 s | "Every name. Every message." (5.7–10.0); cards are texture plus 1–2 reads | A soft pop per card; the bed builds (glockenspiel joins) | Cards clear upwards |
| F4 | 10.0–12.5 | Hands clasp beside the phone | "Pot delivered. Cue the happy tears." (10.2–12.5) | The bed lifts a step | Hard cut on the downbeat |
| F5 | 12.5–17.0 | The Gold Pot crop rises; Chip (143) pops in; the baubles swing in from the top; the NEW sticker slaps on at 13.4 s | "Now the gift's sorted too." (12.7–17.0), "A shop they love, or a multi-store card." (13.6–17.0) | Full bed; a pop on Chip; a sticker slap | Chip exits left as the next one enters |
| F6 | 17.0–20.0 | The phone slides up; Pot shapes fly in from the edges and land on it | "One Pot. One link." (17.2–20.0), "Everyone chips in." (17.8–20.0) | Soft pops as the Pots land | The last Pot falls into the next frame as the card's drop |
| F7 | 20.0–24.0 | The printed card drops onto the Black Pot and settles at -8°; Chip (141) slides in | "No trip to the shops." (20.2–24.0), "Print it at home, or we'll post it to your door." (21.0–24.0) | Paper slap on landing | The card slides off; the end card builds |
| F8 | 24.0–27.0 | The snowy hill rises; Chip (2) slides in; "everyone" bounces in letter by letter (Max relaxing) | "A card and gift in one, from everyone." (24.2–27.0) | The riser starts | The headline clears upwards; Chip rises and shrinks to his F9 spot |
| F9 | 27.0–29.5 | The hill rises again; Chip swaps to 107 (wink); the Pot pops into the logo's O at 27.3 s, then the letters reveal; CREATE A POT lands at 27.8 s | Logo (27.3–29.5), CREATE A POT (27.8–29.5) | A soft hit on the logo; the bed resolves on the last bar | End (hold 1.7 s) |

BANNED:
- The defaults: a dark void, glow or particles, purple or blue gradients, cream paper with a serif, everything fading in together, text drifting after it lands, corner labels, three cards in a row, the logo docked in a corner.
- For this film:
  - Faces of any kind.
  - Any AI-made or redrawn Chip, logo, Pot icon or card.
  - 2D Chip.
  - Secondary colours on Gold (the renders' own props aside).
  - A frame that's all Gold.
  - Shop or retailer logos.
  - Penguin puns.
  - The internal line "Chip in, chill out".

QA:
- 1.0 s: the type and the phone read at thumbnail size.
- 4.0 s: the Pot screen is legible on the phone.
- 7.5 s: at least one message reads.
- 11.0 s: the hands, with no face.
- 14.5 s: Chip, the sticker and two lines are clear of the Reels UI.
- 18.5 s: the plane path.
- 22.0 s: the card reads as "No.1 Teacher".
- 28.0 s: the logo, the button and the wink are all inside the safe zone.
