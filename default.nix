{}:

let
  sources = import ./nix/sources.nix;
  pkgs = import sources.nixpkgs {};
in
{
  exe = pkgs.stdenv.mkDerivation {
    name = "vim-autofmt-gen";
    src = ./.;
    buildInputs = [
      (pkgs.python39.withPackages (ps: with ps; [
        jinja2
        pyyaml
      ])
    )];
    unpackPhase = "true";
    installPhase = ''
      mkdir -p $out/bin
      cp $src/$name.py $out/bin/$name
      chmod +x $out/bin/$name
    '';
  };

  shell = pkgs.mkShell {
    buildInputs = [
      pkgs.python39Packages.jinja2
      pkgs.python39Packages.yapf
      pkgs.python39Packages.pyyaml
      pkgs.nixpkgs-fmt
    ];
  };
}
