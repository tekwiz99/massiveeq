# MassiveEQ — Fedora port

Unofficial **Fedora 44** packaging for [MassiveEQ](https://github.com/massiveadam/massiveeq),
a device-aware systemwide parametric EQ for PipeWire with a native Noctalia
quick-controls widget.

> MassiveEQ itself is officially Arch/AUR-only. This repo adds Fedora build
> instructions, an install script, and an RPM spec so it can be built and
> packaged on Fedora. MassiveEQ is still beta software.

## What's here

| File | Purpose |
|------|---------|
| `massiveeq-fedora-install.sh` | One-shot build + install from source (no RPM). |
| `massiveeq.spec` | RPM spec for `rpmbuild` / COPR / mock. |
| `patches/` | Local fix for upstream's device-discovery CPU loop. |
| `LICENSE` | MIT license from upstream. |

## Presets

The [`presets/`](../presets/) directory holds ready-to-import profiles:

- [`presets/thinkpad-unsuck/`](../presets/thinkpad-unsuck/) — ThinkPad laptop
  speaker profile derived from the MIT-licensed EasyEffects
  `thinkpad-unsuck` preset (high-pass EQ part; the dynamic effects remain
  EasyEffects-only).

Import a profile with the MassiveEQ GUI (**Profiles → Import**) or:

```bash
gdbus call --session --dest org.massiveeq.Service1 \
  --object-path /org/massiveeq/Service1 \
  --method org.massiveeq.Service1.ImportProfile \
  "$PWD/presets/thinkpad-unsuck/thinkpad-unsuck.txt"
```

Then assign it to the output device in the GUI or with
`massiveeqctl assign <device-key> <profile-id>`.

## Quick install (from source)

```bash
git clone https://github.com/<you>/massiveeq-fedora.git
cd massiveeq-fedora
./massiveeq-fedora-install.sh
```

The script installs build deps with `dnf`, builds the workspace in release
mode, installs binaries to `/usr/local/bin`, installs systemd user units,
the D-Bus service, desktop entry, icon, and the Noctalia v5 widget.

### Device-discovery CPU fix

Upstream `v0.3.0-beta.2` has a feedback loop in `massiveeqd`: every PipeWire
global (including the `pw-dump` process spawned by device discovery) triggers
another discovery pass. This spawns `pw-dump` about ten times per second and
keeps the daemon at roughly 25% CPU even when no audio is playing.

The installer applies `patches/0001-device-monitor-ignore-non-audio-globals.patch`
automatically and skips it if it is already present or no longer applies.
You can verify the fix with:

```bash
pgrep -c pw-dump                  # expect 0 most of the time
ps -o pcpu= -p "$(pgrep -x massiveeqd)"   # expect well under 1%
```

Remove the patch once upstream ships an equivalent fix.

Then enable the widget in Noctalia:

```bash
noctalia msg plugins enable massiveeq/massiveeq
```

and add **MassiveEQ** to a bar (or add it to `~/.local/state/noctalia/settings.toml`):

```toml
[bar.default]
end = [ "massiveeq", "tray", "notifications", ... ]

[widget.massiveeq]
type = "massiveeq/massiveeq:quick-controls"
```

## RPM build

```bash
sudo dnf install -y rpm-build rpmdevtools dnf-plugins-core
sudo dnf builddep massiveeq.spec
rpmdev-setuptree
cp patches/*.patch ~/rpmbuild/SOURCES/
spectool -g -R massiveeq.spec
rpmbuild -ba massiveeq.spec
```

Or with `mock`:

```bash
sudo dnf install -y mock
cp patches/*.patch .
mock -r fedora-44-x86_64 --buildsrpm --spec massiveeq.spec --sources .
mock -r fedora-44-x86_64 --rebuild massiveeq-*.src.rpm
```

## Runtime requirements

- PipeWire + WirePlumber (with `pw-dump`, provided by `pipewire-utils`)
- GTK 4 and libadwaita
- `libsndfile`, `libsamplerate`
- A supported Wayland compositor for the Noctalia widget

## Caveats

- Fedora is **not** an upstream-supported target; files are installed under
  `/usr/local` by the script and `/usr` by the RPM.
- The Noctalia widget is optional; the GTK editor and StatusNotifier tray work
  without it.
- Upstream is beta; profile/routing formats may change.

## Upstream

- Source: https://github.com/massiveadam/massiveeq
- Noctalia widget docs: `docs/noctalia-widget.md` in upstream.
