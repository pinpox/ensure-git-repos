{
  description = "Ensure a list of Git repositories is set up";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {  nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        python = pkgs.python3;
        python-env = python.withPackages (ps: with ps; [
          gitpython
          pyyaml
        ]);
      in {
        packages.default = pkgs.stdenv.mkDerivation {
          pname = "ensure-git-repos";
          version = "1.0.0";

          src = ./.;

          buildInputs = [ python-env ];

          installPhase = ''
            mkdir -p $out/bin
            cp ./ensure-git-repos.py $out/bin/ensure-git-repos
            chmod +x $out/bin/ensure-git-repos
          '';
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [ python-env ];
        };
      }
    );
}
