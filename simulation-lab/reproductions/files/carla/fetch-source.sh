#!/bin/sh
set -eu
mkdir -p sources
git clone https://github.com/carla-simulator/driving-benchmarks.git sources/driving-benchmarks
git -C sources/driving-benchmarks checkout 1614d19581d43eac9966e4001611cc8341bf5319
# Download CARLA_0.8.4.tar.gz from the Linux link on the official release:
# https://github.com/carla-simulator/carla/releases/tag/0.8.4
# The release links Google Drive public file18OaDbQ2K9Dcs25d-nIxpw3GPRHhG1r_2 (1.6GB).
# Expected SHA256 is supplied in provenance.json.
mkdir -p carla084
tar -xzf CARLA_0.8.4.tar.gz -C carla084
python patch-legacy.py
