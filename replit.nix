{ pkgs }: {
    deps = [
        pkgs.python310
    ];
    env = {
        PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
            # Needed for pandas / numpy
            pkgs.stdenv.cc.cc.lib
            pkgs.zlib
            # Needed for pygame
            pkgs.glib
            # Needed for matplotlib
            pkgs.xorg.libX11
        ];
        PYTHONBIN = "${pkgs.python310}/bin/python3.10";
        LANG = "en_US.UTF-8";
    };
}