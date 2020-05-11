{ pkgs, ... }:
with (import <nixpkgs> {});
python38.pkgs.buildPythonApplication rec {
    pname = "bumblebee-status";
    version = "1.14.2";
    propagatedBuildInputs = with python38Packages; [
      dbus-python
      psutil
      requests
      libvirt
      parse
      yubico-client
      netifaces
      mock
      setuptools
      feedparser
    ];
    src = ./.;
}
