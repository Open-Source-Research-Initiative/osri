#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
: "${AUTOCKT_RUN_ROOT:?Set this to your isolated run directory}"
: "${AUTOCKT_BUILD_TOOLS:?Set this to an existing prefix containing autoconf automake libtool flex bison}"
export PATH="$AUTOCKT_BUILD_TOOLS/bin:$PATH"
export TMPDIR="$AUTOCKT_RUN_ROOT/tmp"
mkdir -p "$TMPDIR"
cd "$AUTOCKT_RUN_ROOT"
if [ ! -d ngspice-27-source ]; then
  git clone --depth 1 --branch ngspice-27 https://git.code.sf.net/p/ngspice/ngspice ngspice-27-source
fi
actual_ref=$(git -C ngspice-27-source rev-parse HEAD)
[ "$actual_ref" = af7ab797c2b5548a99d9bcb4c7f74556aa4ac67e ]
cd ngspice-27-source
sh autogen.sh
CFLAGS='-O2 -fcommon' ./configure --prefix="$AUTOCKT_RUN_ROOT/ngspice27" --without-x --with-readline=no --disable-debug
make -j4
make install
