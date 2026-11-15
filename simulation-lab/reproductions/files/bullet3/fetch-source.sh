#!/bin/sh
set -eu
mkdir -p sources
git clone --filter=blob:none --no-checkout --depth 1 https://github.com/bulletphysics/bullet3.git sources/bullet3
git -C sources/bullet3 sparse-checkout set examples/pybullet/gym
git -C sources/bullet3 fetch --depth 1 origin d3afe76132fc76b0f9b2359cbaef47a3766e7fbb
git -C sources/bullet3 checkout d3afe76132fc76b0f9b2359cbaef47a3766e7fbb
git -C sources/bullet3 apply ../../compatibility.patch
