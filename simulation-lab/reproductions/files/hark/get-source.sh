#!/bin/sh
set -eu
git clone https://github.com/econ-ark/BufferStock-LifeCycle.git source
git -C source checkout --detach 0a278360b77eeac1df1e91374c168b3091365fbf
