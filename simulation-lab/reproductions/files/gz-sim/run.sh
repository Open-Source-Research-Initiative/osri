#!/bin/sh
set -eu
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
python sources/gz-drl/experiments_paper/reproducability_validation/run_experiment.py --config config.json --results-dir output --groups same_seed
