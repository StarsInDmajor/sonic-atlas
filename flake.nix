{
  description = "Development environment via uv2nix for sonic-atlas";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
    uv2nix.url = "github:pyproject-nix/uv2nix";
    pyproject-build-systems.url = "github:pyproject-nix/build-system-pkgs";
    pyproject-build-systems.inputs.nixpkgs.follows = "nixpkgs";
    pyproject-build-systems.inputs.pyproject-nix.follows = "uv2nix/pyproject-nix";
  };

  outputs =
    inputs@{
      flake-parts,
      nixpkgs,
      uv2nix,
      pyproject-build-systems,
      ...
    }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      perSystem =
        { pkgs, system, ... }:
        let
          lib = pkgs.lib;
          pyproject-nix = uv2nix.inputs.pyproject-nix;

          workspace = uv2nix.lib.workspace.loadWorkspace {
            workspaceRoot = builtins.path {
              path = ./.;
              name = "sonic-atlas-src";
              filter =
                path: type:
                let
                  base = builtins.baseNameOf path;
                in
                !(
                  base == ".git"
                  || base == ".direnv"
                  || base == ".venv"
                  || base == "result"
                  || base == "data"
                  || lib.hasSuffix ".egg-info" base
                );
            };
          };

          python = lib.head (
            pyproject-nix.lib.util.filterPythonInterpreters {
              inherit (workspace) requires-python;
              inherit (pkgs) pythonInterpreters;
            }
          );

          overlay = workspace.mkPyprojectOverlay {
            sourcePreference = "wheel";
          };

          pythonBase = pkgs.callPackage pyproject-nix.build.packages {
            inherit python;
          };

          pythonSet = pythonBase.overrideScope (
            lib.composeManyExtensions [
              pyproject-build-systems.overlays.wheel
              overlay
              # Fix numba's libtbb dependency for auto-patchelf
              (final: prev: {
                numba = prev.numba.overrideAttrs (old: {
                  buildInputs = (old.buildInputs or [ ]) ++ [ pkgs.tbb ];
                });
              })
            ]
          );

          venv = pythonSet.mkVirtualEnv "sonic-atlas-env" workspace.deps.default;
        in
        {
          packages.default = venv;

          devShells.default = pkgs.mkShell {
            packages = [
              python
              pkgs.uv
              pkgs.basedpyright
              pkgs.stdenv.cc.cc
              pkgs.zlib
              # Audio native dependencies (libsndfile for soundfile/librosa)
              pkgs.libsndfile
              # numba needs libtbb at runtime
              pkgs.tbb
            ];
            env = {
              UV_PYTHON = python.interpreter;
              UV_PYTHON_DOWNLOADS = "never";
              LIBRARY_PATH = "${pkgs.glibc}/lib:${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.zlib}/lib:${pkgs.libsndfile.out}/lib:${pkgs.tbb}/lib";
            };
            shellHook = ''
              unset PYTHONPATH
              export VIRTUAL_ENV=${venv}
              export PATH=$VIRTUAL_ENV/bin:$PATH
              export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.zlib}/lib:${pkgs.libsndfile.out}/lib:${pkgs.tbb}/lib''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
              echo "Environment loaded via flake."
              echo "Run 'uv sync' to install/update dependencies."
            '';
          };
        };
    };
}
