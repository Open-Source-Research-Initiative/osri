#!/bin/sh
set -eu
FINANCE_DYNARE_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$FINANCE_DYNARE_ROOT"
export OCTAVE_HOME="$FINANCE_DYNARE_ROOT/octave-env"
export PATH="$OCTAVE_HOME/bin:$PATH"
export CC="$OCTAVE_HOME/bin/x86_64-conda-linux-gnu-gcc"
export CXX="$OCTAVE_HOME/bin/x86_64-conda-linux-gnu-g++"
export FC="$OCTAVE_HOME/bin/x86_64-conda-linux-gnu-gfortran"
export TMPDIR="$FINANCE_DYNARE_ROOT/tmp"
export CXXFLAGS="-I$OCTAVE_HOME/include"
export LDFLAGS="-L$OCTAVE_HOME/lib"
export PKG_CONFIG_PATH="$FINANCE_DYNARE_ROOT/pkgconfig:$OCTAVE_HOME/lib/pkgconfig"
mkdir -p "$TMPDIR" pkgconfig octave-packages
# Conda package supplies HDF5 libraries/headers but lacks its .pc descriptor.
# Exact restored environment uses HDF5 1.14.6.
cat > pkgconfig/hdf5.pc <<EOF
prefix=$OCTAVE_HOME
libdir=\${prefix}/lib
includedir=\${prefix}/include
Name: HDF5
Description: Existing portable HDF5 runtime
Version: 1.14.6
Libs: -L\${libdir} -lhdf5
Cflags: -I\${includedir}
EOF
make -C slicot-source/src -f makefile_Unix -j4 FORTRAN="$FC" OPTS='-O2 -fPIC -fallow-argument-mismatch'
cp slicot-source/slicot.a "$OCTAVE_HOME/lib/libslicot.a"
meson setup -Dbuild_for=octave --buildtype=release dynare-6.4/build-octave dynare-6.4
meson compile -C dynare-6.4/build-octave -j4
"$OCTAVE_HOME/bin/octave-cli" --no-gui --quiet --eval "pkg prefix '$FINANCE_DYNARE_ROOT/octave-packages'; pkg local_list '$FINANCE_DYNARE_ROOT/octave-packages/local-list'; pkg install '$FINANCE_DYNARE_ROOT/statistics-1.7.7.tar.gz';"
