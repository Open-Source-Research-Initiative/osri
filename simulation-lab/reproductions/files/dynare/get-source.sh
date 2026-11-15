#!/bin/sh
set -eu
git clone https://github.com/JohannesPfeifer/DSGE_mod.git pfeifer-source
git -C pfeifer-source checkout --detach 26c21f79e4c6a6b19b18e6330edc5b23489907a4
git clone https://github.com/SLICOT/SLICOT-Reference.git slicot-source
git -C slicot-source checkout --detach 5eeb845d84f5a60f6069754b7819dad468951933
curl -fL https://www.dynare.org/release/source/dynare-6.4.tar.xz -o dynare-6.4.tar.xz
tar -xf dynare-6.4.tar.xz
curl -fL https://github.com/gnu-octave/statistics/releases/download/release-1.7.7/statistics-1.7.7.tar.gz -o statistics-1.7.7.tar.gz
