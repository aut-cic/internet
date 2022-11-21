{
  outputs = { nixpkgs, ... }:
    let
      system = builtins.currentSystem;
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [ pkgs.nodejs-19_x pkgs.python311 pkgs.pipenv ];
      };
    };
}
