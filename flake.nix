{
  description = "Vim autoformatter plugins generator.";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-21.11";
  };

  outputs = { self, nixpkgs }:
    let pkg-name = "vim-autofmt-gen";
    in
    {
    defaultPackage.x86_64-linux =
      with import nixpkgs { system = "x86_64-linux"; };
      pkgs.stdenv.mkDerivation {
        name = pkg-name;
        src = self;
        buildInputs = [
          (pkgs.python39.withPackages (ps: with ps; [
            jinja2
            pyyaml
          ])
          )
        ];
        unpackPhase = "true";
        installPhase = ''
          mkdir -p $out/bin
          cp $src/${pkg-name}.py $out/bin/${pkg-name}
          chmod +x $out/bin/${pkg-name}
        '';
      };

    devShell.x86_64-linux =
      with import nixpkgs { system = "x86_64-linux"; };
      pkgs.mkShell {
        buildInputs = [
          pkgs.nixpkgs-fmt
          pkgs.pyright
          (python39.withPackages (ps: with ps; [ jinja2 pyxdg pyyaml yapf ]))
        ];
        shellHook = ''
          export PS1="\e[01;32mnix-develop\e[m\e[01;31m (${pkg-name})\e[m\$ "
        '';
      };
  };
}
