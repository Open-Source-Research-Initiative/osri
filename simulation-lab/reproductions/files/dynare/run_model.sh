#!/bin/sh
set -eu
FINANCE_DYNARE_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export OCTAVE_HOME="$FINANCE_DYNARE_ROOT/octave-env"
export TMPDIR="$FINANCE_DYNARE_ROOT/tmp"
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
mkdir -p "$TMPDIR"
"$OCTAVE_HOME/bin/octave-cli" --no-gui --quiet --eval "pkg local_list '$FINANCE_DYNARE_ROOT/octave-packages/local-list'; pkg load statistics; addpath('$FINANCE_DYNARE_ROOT/dynare-6.4/matlab'); cd('$FINANCE_DYNARE_ROOT/pfeifer-source/Smets_Wouters_2007'); dynare Smets_Wouters_2007.mod noclearall; save('-mat7-binary', '$FINANCE_DYNARE_ROOT/model-outputs.mat', 'oo_', 'M_', 'options_');"
