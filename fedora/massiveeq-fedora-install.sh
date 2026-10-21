#!/usr/bin/env bash
# massiveeq-fedora-install.sh
# Build and install MassiveEQ from source on Fedora 44.
#
# MassiveEQ is officially Arch-only. This script installs the Fedora build
# dependencies, builds the workspace, and installs binaries + desktop assets
# under /usr/local.
set -euo pipefail

PREFIX="${PREFIX:-/usr/local}"
SRC_DIR="${SRC_DIR:-$HOME/src/massiveeq}"
UPSTREAM="${UPSTREAM:-https://github.com/massiveadam/massiveeq.git}"

log() { printf '\033[1;34m==>\033[0m %s\n' "$*"; }

log "Installing Fedora build dependencies"
sudo dnf install -y \
  gcc make clang rust cargo git \
  gtk4-devel libadwaita-devel \
  pipewire-devel wireplumber-devel pipewire-utils \
  libsndfile-devel libsamplerate-devel \
  curl pkg-config

log "Fetching MassiveEQ source"
if [ ! -d "$SRC_DIR/.git" ]; then
  git clone "$UPSTREAM" "$SRC_DIR"
fi
cd "$SRC_DIR"
git pull --ff-only || true

log "Building (release)"
cargo build --workspace --release --locked

log "Running tests"
cargo test --workspace --release --locked

log "Installing binaries to $PREFIX/bin"
sudo install -Dm755 target/release/massiveeq      "$PREFIX/bin/massiveeq"
sudo install -Dm755 target/release/massiveeqd     "$PREFIX/bin/massiveeqd"
sudo install -Dm755 target/release/massiveeq-tray "$PREFIX/bin/massiveeq-tray"
sudo install -Dm755 target/release/massiveeqctl   "$PREFIX/bin/massiveeqctl"

log "Installing systemd user units"
mkdir -p "$HOME/.config/systemd/user"
install -Dm644 packaging/massiveeq.service      "$HOME/.config/systemd/user/massiveeq.service"
install -Dm644 packaging/massiveeq-tray.service "$HOME/.config/systemd/user/massiveeq-tray.service"
sed -i "s#/usr/bin/#$PREFIX/bin/#g" \
  "$HOME/.config/systemd/user/massiveeq.service" \
  "$HOME/.config/systemd/user/massiveeq-tray.service"

log "Installing desktop entry, icon, metainfo"
sudo install -Dm644 packaging/org.massiveeq.MassiveEQ.desktop /usr/share/applications/org.massiveeq.MassiveEQ.desktop
sudo sed -i "s#^Exec=.*#Exec=$PREFIX/bin/massiveeq#" /usr/share/applications/org.massiveeq.MassiveEQ.desktop
sudo install -Dm644 packaging/org.massiveeq.MassiveEQ.svg /usr/share/icons/hicolor/scalable/apps/org.massiveeq.MassiveEQ.svg
sudo install -Dm644 packaging/org.massiveeq.MassiveEQ.metainfo.xml /usr/share/metainfo/org.massiveeq.MassiveEQ.metainfo.xml

log "Installing D-Bus service"
sudo install -Dm644 packaging/org.massiveeq.Service1.service /usr/share/dbus-1/services/org.massiveeq.Service1.service
sudo sed -i "s#/usr/bin/massiveeqd#$PREFIX/bin/massiveeqd#" /usr/share/dbus-1/services/org.massiveeq.Service1.service

log "Installing Noctalia v5 widget"
mkdir -p "$HOME/.local/share/noctalia/plugins/massiveeq"
cp -a packaging/noctalia-v5/massiveeq/. "$HOME/.local/share/noctalia/plugins/massiveeq/"

log "Enabling audio service"
systemctl --user daemon-reload
systemctl --user enable --now massiveeq.service
systemctl --user enable --now massiveeq-tray.service || true

log "Done"
echo
echo "Check status:"
echo "  systemctl --user is-active massiveeq.service"
echo "  massiveeqctl status"
echo
echo "Enable the Noctalia widget:"
echo "  noctalia msg plugins enable massiveeq/massiveeq"
echo "  # then add the widget to a bar in Noctalia settings"
