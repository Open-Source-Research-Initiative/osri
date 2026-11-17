#!/usr/bin/env bash
set -euo pipefail
if [[ $# != 1 || "$(uname -s):$(uname -m)" != Linux:x86_64 ]]; then
    echo "Usage on Linux x86_64: bash setup.sh WORK_DIR" >&2
    exit 2
fi
packet=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
mkdir -p -- "$1"
work=$(cd -- "$1" && pwd)
if [[ -e "$work/env" ]]; then
    echo "Choose a work directory without an existing env: $work" >&2
    exit 2
fi
mkdir -p "$work/tmp" "$work/tools" "$work/logs" "$work/cache"
export TMPDIR="$work/tmp" XDG_CACHE_HOME="$work/cache"
export LC_ALL=C TZ=UTC
# Keep default R user and site libraries out of the installed environment.
unset R_HOME R_LIBS R_LIBS_SITE R_LIBS_USER
export R_ENVIRON_USER=/dev/null R_ENVIRON=/dev/null
export R_PROFILE_USER=/dev/null R_PROFILE=/dev/null
export R_MAKEVARS_USER="$packet/Makevars"

python3 "$packet/prepare_inputs.py" "$work" | tee "$work/logs/inputs.log"
tar -xjf "$work/sources/micromamba.tar.bz2" -C "$work/tools" bin/micromamba
mamba="$work/tools/bin/micromamba"
test "$("$mamba" --version)" = 2.10.0
"$mamba" --no-rc --root-prefix "$work/mamba" create --yes --offline \
    --prefix "$work/env" --file "$work/conda-explicit-local.txt" 2>&1 | tee "$work/logs/conda.log"
"$work/env/bin/R" CMD INSTALL "$work/sources/BH_1.69.0-1.tar.gz" 2>&1 | tee "$work/logs/BH.log"
"$work/env/bin/R" CMD INSTALL "$work/sources/simmer-publisher.tar.gz" 2>&1 | tee "$work/logs/simmer.log"
{
    uname -srm
    /usr/bin/gcc --version
    /usr/bin/g++ --version
    "$work/env/bin/Rscript" --vanilla -e 'sessionInfo()'
} > "$work/logs/platform.txt"
