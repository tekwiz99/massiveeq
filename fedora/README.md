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
| `LICENSE` | MIT license from upstream. |

## Quick install (from source)

```bash
git clone https://github.com/<you>/massiveeq-fedora.git
cd massiveeq-fedora
./massiveeq-fedora-install.sh
```

The script installs build deps with `dnf`, builds the workspace in release
mode, installs binaries to `/usr/local/bin`, installs systemd user units,
the D-Bus service, desktop entry, icon, and the Noctalia v5 widget.

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
spectool -g -R massiveeq.spec
rpmbuild -ba massiveeq.spec
```

Or with `mock`:

```bash
sudo dnf install -y mock
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
