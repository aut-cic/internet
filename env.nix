with (import <nixpkgs> {});
let
  python-package-managers = python-packages: with python-packages; [
  ];
  python-with-package-managers = python311.withPackages python-package-managers;
in
mkShell {
  buildInputs = [
    python-with-package-managers
    pipenv
  ];
}

