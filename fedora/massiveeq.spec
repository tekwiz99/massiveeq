%global commit 4d759466659909548e452f458df5365184a654f9
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           massiveeq
Version:        0.3.0~beta.2
Release:        2%{?dist}
Summary:        Device-aware systemwide equalizer for PipeWire and Wayland desktops
License:        MIT
URL:            https://github.com/massiveadam/massiveeq
Source0:        %{url}/archive/%{commit}/massiveeq-%{commit}.tar.gz
Source1:        https://raw.githubusercontent.com/massiveadam/massiveeq/%{commit}/LICENSE
Patch0:         0001-device-monitor-ignore-non-audio-globals.patch

BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  gcc
BuildRequires:  clang
BuildRequires:  pkgconfig
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  pipewire-devel
BuildRequires:  wireplumber-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libsamplerate-devel

Requires:       gtk4
Requires:       libadwaita
Requires:       pipewire
Requires:       wireplumber
Requires:       pipewire-utils
Requires:       libsndfile
Requires:       libsamplerate
Requires:       hicolor-icon-theme

%description
MassiveEQ is a systemwide playback equalizer for PipeWire. It combines a
GTK4/libadwaita profile editor with a user-level service that places PipeWire
smart filters in front of assigned output devices.

This is an unofficial Fedora package. Upstream supports Arch Linux only.

%prep
%autosetup -n massiveeq-%{commit}
cp -p %{SOURCE1} LICENSE

%build
%cargo_build

%install
install -Dm755 target/release/massiveeq      %{buildroot}%{_bindir}/massiveeq
install -Dm755 target/release/massiveeqd     %{buildroot}%{_bindir}/massiveeqd
install -Dm755 target/release/massiveeq-tray %{buildroot}%{_bindir}/massiveeq-tray
install -Dm755 target/release/massiveeqctl   %{buildroot}%{_bindir}/massiveeqctl

install -Dm644 packaging/massiveeq.service      %{buildroot}%{_userunitdir}/massiveeq.service
install -Dm644 packaging/massiveeq-tray.service %{buildroot}%{_userunitdir}/massiveeq-tray.service
install -Dm644 packaging/org.massiveeq.Service1.service %{buildroot}%{_datadir}/dbus-1/services/org.massiveeq.Service1.service
install -Dm644 packaging/org.massiveeq.MassiveEQ.desktop %{buildroot}%{_datadir}/applications/org.massiveeq.MassiveEQ.desktop
install -Dm644 packaging/org.massiveeq.MassiveEQ.metainfo.xml %{buildroot}%{_datadir}/metainfo/org.massiveeq.MassiveEQ.metainfo.xml
install -Dm644 packaging/org.massiveeq.MassiveEQ.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/org.massiveeq.MassiveEQ.svg

install -dm755 %{buildroot}%{_datadir}/massiveeq/noctalia-v4
cp -a packaging/noctalia-v4/massiveeq %{buildroot}%{_datadir}/massiveeq/noctalia-v4/
install -dm755 %{buildroot}%{_datadir}/massiveeq/noctalia-v5
cp -a packaging/noctalia-v5/massiveeq %{buildroot}%{_datadir}/massiveeq/noctalia-v5/

%files
%license LICENSE
%{_bindir}/massiveeq
%{_bindir}/massiveeqd
%{_bindir}/massiveeq-tray
%{_bindir}/massiveeqctl
%{_userunitdir}/massiveeq.service
%{_userunitdir}/massiveeq-tray.service
%{_datadir}/dbus-1/services/org.massiveeq.Service1.service
%{_datadir}/applications/org.massiveeq.MassiveEQ.desktop
%{_datadir}/metainfo/org.massiveeq.MassiveEQ.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/org.massiveeq.MassiveEQ.svg
%{_datadir}/massiveeq/noctalia-v4/massiveeq
%{_datadir}/massiveeq/noctalia-v5/massiveeq

%changelog
* Wed Oct 21 2026 tekwiz99 <5897201+tekwiz99@users.noreply.github.com> - 0.3.0~beta.2-2
- Fix device-discovery feedback loop that consumed ~25% CPU by spawning
  pw-dump about ten times per second

* Wed Oct 21 2026 Your Name <you@example.com> - 0.3.0~beta.2-1
- Initial Fedora packaging of MassiveEQ (upstream commit %{shortcommit})
