with import <nixpkgs> {};
    with pkgs.python35Packages;

    buildPythonPackage {
      name = "dev";
      buildInputs = [
         python35
	 python35Packages.pyqt5
    	 python35Packages.matplotlib
    	 python35Packages.numpy
         stdenv];
    }
    
