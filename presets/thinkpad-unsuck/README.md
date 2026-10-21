# thinkpad-unsuck preset

Unofficial MassiveEQ profile derived from
[`sebastian-de/easyeffects-thinkpad-unsuck`](https://github.com/sebastian-de/easyeffects-thinkpad-unsuck)
by Sebastian Fleer, MIT licensed (see `LICENSE`).

The upstream preset targets the built-in speakers of the **ThinkPad P14s
Gen 2 AMD**. It can still be a useful starting point on other ThinkPads, but
it is not tuned for them.

## Files

| File | Use |
|------|-----|
| `thinkpad-unsuck.txt` | MassiveEQ / Equalizer APO-compatible profile (EQ part only). |
| `thinkpad-unsuck.json` | Original EasyEffects 7.x preset (full effects chain). |
| `LICENSE` | Upstream MIT license. |

## Import into MassiveEQ

GUI: **Profiles → Import** and pick `thinkpad-unsuck.txt`.

Or from a shell:

```bash
gdbus call --session \
  --dest org.massiveeq.Service1 \
  --object-path /org/massiveeq/Service1 \
  --method org.massiveeq.Service1.ImportProfile \
  "$PWD/thinkpad-unsuck.txt"
```

Then assign it to the laptop speakers with the MassiveEQ GUI (or
`massiveeqctl assign <device-key> <profile-id>`).

## What is and isn't reproduced

MassiveEQ implements parametric/graphic EQ and convolution only. The
translated profile contains:

- a preamp of **-6 dB** (headroom, matching the upstream bass-enhancer input gain);
- the upstream **36 dB/oct Butterworth high-pass at 140 Hz**, built from three
  cascaded 2nd-order sections (Q = 0.5176, 0.7071, 1.9319).

It does **not** reproduce the upstream bass enhancer, multiband compressor,
stereo tools or limiter. Those are dynamic effects and cannot be expressed in
an Equalizer APO profile. For the complete preset, import
`thinkpad-unsuck.json` into EasyEffects instead.

The `easyeffects6` variant of the upstream preset (145 Hz high-pass,
resonance -3 dB) is not included; this profile follows the current 7.x
preset (140 Hz).
