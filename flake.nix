{
  description = "Project Z - Trophee NSI 2023 (pygame escape game)";

  # System libraries (glibc, ALSA, SDL, X11/GL) are left to float with
  # current nixpkgs rather than pinned to the project's original 2023 era.
  # A fully pinned toolchain was tried first and broke: this machine's audio
  # stack (pipewire) is built against a newer glibc than an old nixpkgs
  # would provide, and pygame's mixer crashes trying to dlopen it. That
  # mismatch only gets worse with time, so instead the base system tracks
  # whatever's current - re-run `nix flake update` occasionally to refresh
  # it against future hosts. Only the actual game dependencies (the ones
  # named in README.md: pygame, pytmx, pyscroll) are version-pinned.
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3;

        # pyscroll has never been packaged in nixpkgs. Pin it to 2.30
        # (Apr 2022), the latest release that predates this project's first
        # commit (Apr 2023) - README credits pygame/pytmx/pyscroll but gives
        # no versions, and __pycache__ in the repo confirms CPython 3.10 was
        # used at the time.
        pyscroll = python.pkgs.buildPythonPackage rec {
          pname = "pyscroll";
          version = "2.30";
          format = "setuptools";
          src = python.pkgs.fetchPypi {
            inherit pname version;
            sha256 = "sha256-qgG+3T5wm63utyawuwpn/IYlCar4vp7F0gON8lDtw/M=";
          };
          propagatedBuildInputs = [ python.pkgs.pygame ];
          doCheck = false;
        };

        pythonEnv = python.withPackages (ps: [
          ps.pygame # README: pygame
          ps.pytmx  # README: pytmx
          pyscroll  # README: pyscroll (not in nixpkgs, built above)
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [ pythonEnv ];
        };

        packages.default = pkgs.writeShellApplication {
          name = "project-z";
          runtimeInputs = [ pythonEnv ];
          text = ''
            cd "${self}"
            exec python Main.py
          '';
        };

        apps.default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/project-z";
        };
      });
}
