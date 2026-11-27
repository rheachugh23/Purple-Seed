# Voiceover: generation log

| | |
|---|---|
| **Service** | ElevenLabs (hosted MCP), text to speech |
| **Model** | eleven_v4 |
| **Voice** | "Elizabeth – Professional British Narrator" (`AXdMgz6evoL7OPd7eU12`): a warm, friendly British female voice from ElevenLabs's own set, not a library voice |
| **Takes** | 1 (one take of all seven lines, no alternates) |
| **Cost** | 427 characters on the account's free plan, 27 Nov 2026 |
| **ElevenLabs flow** | `cN7445EUCAbUV2IC5NSv` |

**Prompt (sent exactly as written):**

> [warmly] From Aisha's mum. Leo's dad. And everyone in between. [long pause] Twenty-eight messages… one very emotional teacher. [long pause] [happy] And this year, there's a Gift Card in there too. [long pause] [mischievously] No chasing anyone for a fiver. [long pause] [warmly] And the card? Print it, or we'll pop it in the post. [long pause] Teacher's gift… made easy. [long pause] [happy] Collection Pot. Start yours today.

**Processing:**
1. **Level the take.** High-pass at 80 Hz, a 3:1 compressor from −24 dB, +13.5 dB of gain and a limiter at −1.5 dB. The result is −16.6 LUFS with peaks at −1.8 dBFS.
2. **Find the lines.** The take was split at its pauses (silencedetect at −40 dB for 0.35 s). That gave 10 speech chunks, which map onto the 7 lines by length and syllable count.
3. **Cut the clips.** Each line was cut with a 15 ms fade-in and a 60 ms fade-out.

| Clip | Take (s) | In the film (s) | Line |
|---|---|---|---|
| vo-01.wav | 0.00–4.34 | 2.30 | From Aisha's mum. Leo's dad. And everyone in between. |
| vo-02.wav | 4.88–9.36 | 6.90 | Twenty-eight messages… one very emotional teacher. |
| vo-03.wav | 9.88–12.51 | 12.95 | And this year, there's a Gift Card in there too. |
| vo-04.wav | 12.93–15.04 | 17.35 | No chasing anyone for a fiver. |
| vo-05.wav | 15.47–18.46 | 20.85 | And the card? Print it, or we'll pop it in the post. |
| vo-06.wav | 18.83–20.95 | 24.45 | Teacher's gift… made easy. |
| vo-07.wav | 21.39–23.88 | 27.25 | Collection Pot. Start yours today. |

**The mix in `index.html`:**
- **Voice clips:** grouped as `voiceover`.
- **Music:**
  - A volume lane takes it down to 0.5 (−6 dB) under each line, and to 0.42 from 20.85 s, then back up in the gaps.
  - On top of that, a carve at strength 0.5 (`media-use` `carve.mjs`) takes −5 to −10 dB from 250 Hz to 2.5 kHz while the voice speaks.
  - **The carve's level dip was deleted on purpose.** That was the `fx.n5.gain` lane, which went down to −12 dB and recovered slowly. With it, the first VO render had the music 18–25 dB under the voice, and it never came back up in the gaps.
  - **Re-running `carve.mjs` brings that lane back,** so delete it again afterwards.
- **Card pops** are down to 0.2, and the **logo chime** to 0.25.

**Licence:** ElevenLabs's free plan doesn't include a commercial licence. Upgrade the account (Starter or above) and regenerate this same prompt before the Reel is posted. It costs about 430 characters, and the timings above still apply if the read comes out the same length.
