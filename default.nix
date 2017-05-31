with import <nixpkgs> {};

    with pkgs.python35Packages;

    let
    _pynmea2 = buildPythonPackage rec {

        doCheck = false;

	pname = "pynmea2";
	version = "1.7.1";
	name = "${pname}-${version}";

	src = fetchPypi {
	inherit pname version;
	sha256 = "b7d15b82047e181d01f829dd41e1699e0f020a18a36021f74d3b4670d283877e";
	};

	meta = {
	description = "Python library for parsing the NMEA 0183 protocol (GPS)";
	homepage = "https://github.com/Knio/pynmea2";
	};
    };
    in {

        me = buildPythonPackage {
	name = "dev";
      	buildInputs = [
 	python35
	python35Packages.pyqt5
    	python35Packages.matplotlib # NB You might need a ~/.config/matplotlib/matplotlibrc to specify a Qt5Agg backend
    	python35Packages.numpy
	python35Packages.pandas
	_pynmea2
        stdenv
	];
	};
    }

