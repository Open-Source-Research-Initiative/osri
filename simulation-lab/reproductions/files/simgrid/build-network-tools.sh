#!/usr/bin/env bash
set -euo pipefail
# Original OSRI build harness. Requires Linux, git, GCC/G++, Python3 with venv,
# and an existing Boost dependency prefix. All writes stay beneath this directory.
root_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$root_dir"
: "${BOOST_ROOT:?Set BOOST_ROOT to a qualified Boost headers/library prefix}"
python3 -m venv build-env
build-env/bin/python -m pip install -r requirements-build.txt
export PATH="$root_dir/build-env/bin:$PATH"
export LD_LIBRARY_PATH="$BOOST_ROOT/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
fetch_pin() {
 local name=$1 repo=$2 ref=$3 pin=$4
 git clone --depth 1 --branch "$ref" "$repo" "$name"
 git -C "$name" fetch --depth 1 origin "$pin"
 git -C "$name" checkout --detach "$pin"
}
fetch_pin unison https://github.com/NASA-NJU/UNISON-for-ns-3.git unison-evaluations 7b3274167615c55ae8d69f7edee4e2dc2d81f706
fetch_pin simgrid-benchmark https://github.com/simgrid/coordinator_worker_flashback.git main b09453d19541b7186703f4d651c1bba790461e44
fetch_pin simgrid-v3.10 https://github.com/simgrid/simgrid.git v3_10 9a82cac1b6f73bb342495c39807acd7380e153d5
fetch_pin simgrid-v3.36 https://github.com/simgrid/simgrid.git v3.36 7ed73b43153fc79a8c5eb5cff8e9f81e4f52e619
# Reproduce the CMake workaround in authors' Dockerfile_simgrid_v3_10.
python3 - <<'PY'
from pathlib import Path
p=Path('simgrid-v3.10/CMakeLists.txt');s=p.read_text();Path('simgrid-v3.10-CMakeLists-original.txt').write_text(s);lines=s.splitlines(True);p.write_text(''.join(lines[:92]+lines[-151:]))
PY
mkdir simgrid-build-v3.10
# This old CMake's configure probes write conftestval in the current directory.
(cd simgrid-build-v3.10 && cmake ../simgrid-v3.10 -DCMAKE_BUILD_TYPE=Release -Denable_SMPI=OFF -Denable_documentation=OFF -DBOOST_ROOT="$BOOST_ROOT")
cmake --build simgrid-build-v3.10 --target simgrid -j 3
cmake -S simgrid-v3.36 -B simgrid-build-v3.36 -DCMAKE_BUILD_TYPE=Release -Denable_smpi=OFF -Denable_model-checking=OFF -Denable_documentation=OFF -DBoost_ROOT="$BOOST_ROOT"
cmake --build simgrid-build-v3.36 --target simgrid -j 3
# Only change two hardcoded /tmp paths; model equations/event logic remain intact.
python3 - <<'PY'
from pathlib import Path
root=Path.cwd();(root/'tmp').mkdir(exist_ok=True)
for source,dest in [('masterworker-v3_10.c','coordinator-workspace-v3.10.c'),('masterworker-v3_34.cpp','coordinator-workspace.cpp')]:
 original=(root/'simgrid-benchmark'/source).read_text();updated=original.replace('/tmp/platform_master_worker',str(root/'tmp/platform_master_worker'));(root/dest).write_text(updated)
PY
gcc -std=c99 -I simgrid-v3.10/include -I simgrid-build-v3.10/include coordinator-workspace-v3.10.c -L simgrid-build-v3.10/lib -Wl,-rpath,"$root_dir/simgrid-build-v3.10/lib" -lsimgrid -O3 -o coordinator-workspace-v3.10
g++ -std=c++17 -I simgrid-v3.36/include -I simgrid-build-v3.36/include -I "$BOOST_ROOT/include" coordinator-workspace.cpp -L simgrid-build-v3.36/lib -Wl,-rpath,"$root_dir/simgrid-build-v3.36/lib" -lsimgrid -O3 -o coordinator-workspace-v3.36
# Separate Unison and sequential builds; -include cstdint fixes GCC13 header compatibility.
for mode in mtp default; do
 if [ "$mode" = mtp ]; then mtp=ON; cache=cmake-cache; output=build; modules=applications,flow-monitor,mtp,nix-vector-routing,point-to-point
 else mtp=OFF; cache=cmake-cache-default; output=build-default; modules=applications,flow-monitor,nix-vector-routing,point-to-point; fi
 cmake -S unison -B "unison/$cache" -G Ninja -DCMAKE_BUILD_TYPE=release -DNS3_ASSERT=OFF -DNS3_LOG=OFF -DNS3_WARNINGS_AS_ERRORS=OFF -DNS3_NATIVE_OPTIMIZATIONS=ON -DNS3_EXAMPLES=ON -DNS3_MTP="$mtp" -DNS3_PYTHON_BINDINGS=OFF -DNS3_ENABLED_MODULES="$modules" -DNS3_OUTPUT_DIRECTORY="$root_dir/unison/$output" -DCMAKE_CXX_FLAGS='-include cstdint'
 cmake --build "unison/$cache" --target scratch_fat-tree -j 3
done
