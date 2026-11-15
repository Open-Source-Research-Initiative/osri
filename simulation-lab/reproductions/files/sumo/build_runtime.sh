#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
study_dir=$(cd -- "$(dirname -- "$0")" && pwd)
cd "$study_dir"
export MAMBA_ROOT_PREFIX="$study_dir/.mamba"
micromamba create -y -p "$study_dir/.runtime" --file xerces-linux-64.explicit
python3 fetch_source.py
mkdir -p build
cd build
../sumo-0.26.0/configure --with-xerces="$study_dir/.runtime" CXXFLAGS='-O2 -std=c++11 -DHUGE=FLT_MAX -include cfloat -include cmath'
make -j2 CXXFLAGS='-O2 -std=c++11 -DHUGE=FLT_MAX -include cfloat -include cmath'
