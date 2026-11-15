#!/bin/sh
set -eu
mkdir -p sources
git clone https://github.com/amaldevh/gz-drl.git sources/gz-drl
git -C sources/gz-drl checkout 3e5c5f9a62c1160b3b2889e6d34d794a5361e178
git -C sources/gz-drl apply ../../compatibility.patch
# In the activated conda environment, install the CPU PyTorch wheel separately:
python -m pip install torch==2.7.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
CMAKE_BUILD_PARALLEL_LEVEL=2 python -m pip install --no-deps --no-build-isolation --config-settings=cmake.define.GZDRL_FORCE_GCC_11=OFF sources/gz-drl
