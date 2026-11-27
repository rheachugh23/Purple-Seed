#!/usr/bin/env python3
"""Rebuild a HyperFrames film's sound offline, so you can measure the mix before a long render.

    python3 sim_mix.py index.html -o /tmp/mix.wav [--only "vo-"] [--duration 30]

It reads every <audio> in the file: src, data-start, data-duration, data-volume and data-fade-in/out,
plus the `volume` lane of data-automation. It delays each clip, mixes them without normalising, and
writes a WAV. Effects chains and carves are ignored, so the music comes out slightly louder than it
will in the render: a conservative estimate.

--only takes a regex on element ids (e.g. "music" or "vo-") to write a single stem. Then measure:
    ffmpeg -i mix.wav -af ebur128=peak=true -f null -          (whole mix: LUFS and true peak)
    ffmpeg -ss 7 -to 11 -i vo.wav -af ebur128 -f null -        (one line, voice stem vs music stem)
Run from the project folder so relative src paths resolve. Needs ffmpeg.
"""
import argparse, html, json, re, subprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("comp")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--only", help="regex on element ids to keep")
    ap.add_argument("--duration", type=float, help="trim the mix to this length (default: longest clip end)")
    a = ap.parse_args()
    s = open(a.comp).read()
    clips = []
    for tag in re.findall(r"<audio ([^>]*)>", s):
        attr = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
        if a.only and not re.search(a.only, attr.get("id", "")):
            continue
        clips.append(attr)
    if not clips:
        raise SystemExit("no <audio> clips matched")
    inputs, chains, end = [], [], 0.0
    for i, c in enumerate(clips):
        st, du = float(c["data-start"]), float(c["data-duration"])
        end = max(end, st + du)
        inputs += ["-i", c["src"]]
        f = f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{du},asetpts=PTS-STARTPTS"
        if "data-automation" in c:
            lanes = json.loads(html.unescape(c["data-automation"])).get("lanes", [])
            vol = [l for l in lanes if l.get("target") == "volume"]
            if vol and vol[0]["points"]:
                pts = sorted(vol[0]["points"], key=lambda p: p["t"])
                expr = str(pts[-1]["v"])
                for p, q in reversed(list(zip(pts, pts[1:]))):
                    expr = f"if(lt(t,{q['t']}),{p['v']}+({q['v']}-{p['v']})*(t-{p['t']})/({q['t']}-{p['t']}+1e-9),{expr})"
                f += f",volume='{expr}':eval=frame"
        if float(c.get("data-fade-in", 0)) > 0:
            f += f",afade=t=in:d={c['data-fade-in']}"
        if float(c.get("data-fade-out", 0)) > 0:
            fo = float(c["data-fade-out"])
            f += f",afade=t=out:st={max(0, du - fo)}:d={fo}"
        f += f",volume={float(c.get('data-volume', 1))},adelay={int(st * 1000)}:all=1[a{i}]"
        chains.append(f)
    dur = a.duration or end
    graph = ";".join(chains) + ";" + "".join(f"[a{i}]" for i in range(len(clips)))
    graph += f"amix=inputs={len(clips)}:normalize=0:duration=longest,atrim=0:{dur}[out]"
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph,
                           "-map", "[out]", "-c:a", "pcm_s16le", a.out])
    print(f"wrote {a.out}: {len(clips)} clips, {dur:.2f} s")


if __name__ == "__main__":
    main()
