{
  description = "Python development environment with uv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          python312
          python312Packages.opencv4
          opencv4
          # (python312.withPackages (ps:
          #   with ps; [
          #     opencv4
          #   ]))
          zlib
          uv
        ];

        shellHook = ''
          # Create a virtual environment if it doesn't exist
          if [ ! -d ".venv" ]; then
            uv venv .venv
          fi
          source .venv/bin/activate
          # echo "uv pip env ready"
        '';
      };
    });
}
