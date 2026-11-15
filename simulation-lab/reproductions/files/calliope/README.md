# Check the published Calliope decision-space data

Can the authors' archived results recover the published range of energy-system choices?

[Pickering, Lombardi and Pfenninger (2022)](https://doi.org/10.1016/j.joule.2022.05.009) describe 441 near-optimal configurations and nine high-level metrics in Figure 3 and Table 1. This example analyzes the actual author result archive. It does **not** perform a new energy-system optimization.

## Run the data comparison

Python 3's standard library is sufficient. The bundled `paper_metrics.csv` is the exact `slack-10/data/paper_metrics.csv` extracted from the verified [author results archive](https://doi.org/10.5281/zenodo.6546817). Its SHA256 is checked before analysis.

```sh
python3 analyse_archive.py
```

To repeat extraction from the original archive instead, allow about 1.1 GB of download space:

```sh
python3 fetch_archives.py
python3 analyse_archive.py --archive euro-spores-results-v2022-05-13.zip
```

The comparison counts configurations and checks the minimum and maximum of each metric against the paper's rounded Table 1 values. Acceptance intervals are half the final published digit, chosen before this analysis; they are rounding checks, not engineering prediction tolerances. `analysis-output/comparison.json` records every measured range and comparison.

The actual archive contained 3,969 metric rows for **441 configurations**. All nine ranges agreed with the published rounding. Examples are storage discharge capacity **0.0295569–10.8661 TW**, electricity-production Gini **0.536960–0.739856**, and average national import **3.76719–69.4641 TWh**. The script was also run against the bundled CSV successfully. These are recovered published results, not newly solved simulations or independent empirical validation.

## Fresh author-model attempt and open-solver check

Both author archives were downloaded and their published MD5s verified. The [model archive](https://doi.org/10.5281/zenodo.5774988) expands to about 2.67 GB and includes YAML, CSV, model-building code and custom constraints. Neither archive contains compiled NetCDF inputs or an LP/MPS file, so the constructor must run before a fresh backend can be built.

The archive specifies Python 3.7 and Calliope commit `304cba8ab5e4fd212ea9f35cde49ac3a1a2303d7`. This exact source was recovered through its GitHub commit archive and installed as `0.6.8-dev`. The reconstructed dependency lock and compatibility pins are included.

An earlier Gurobi 9.1.2 prerequisite failed with **“License expired 2022-01-13.”** That does not block every open-solver route. An existing **GLPK 5.0** executable was recognized by the exact author Pyomo 6.0.1 environment and passed a minimal LP-interface prerequisite. That probe tests the interface, not the study model.

A separate fresh-solver protocol was declared before attempting the original 98-region, 2018, two-hour scenario. Its archived baseline objective reference is 849.8662003464812 billion 2015 EUR; objective, primal-residual and capacity comparisons were specified. None of those comparisons was performed because input construction failed first. They are separate from the successful Table 1 archive analysis above.

The author constructor completed YAML/scenario preprocessing in about 210 seconds. It then raised:

```text
MemoryError: Unable to allocate 8.05 GiB for an array
with shape (6491, 8760) and data type <U38
```

The failure occurred in `add_time_dimension` while copying a broadcast array, before time resampling, native-input persistence, backend construction or a study-model solve. The process had a deliberately scoped **12 GiB address-space limit**; observed peak resident memory was about **8.58 GiB**. This is a measured failure under that budget, not proof that the host or an open solver inherently cannot solve the LP.

Measured source sets include 6,491 location–technology entries, 6,319 production entries, 6,076 consumption entries, 1,252 storage entries and 3,305 variable-cost entries. Their source-defined two-hour time-index products suggest approximately 74.7 million scalar entries in several base variable families. These are sizing estimates, **not an instantiated or solved LP size**.

`outputs/fresh-model-attempt.json` records the actual failure, scope and memory measurements. `fresh-solver-protocol.json` preserves the separate proposed optimizer comparison. No new objective, capacity, feasibility or solver-convergence result is asserted.

## Repeat the bounded input-construction check

This optional step downloads the model archive in addition to the results archive and may use several gigabytes of working space. Use a writable study directory and micromamba. The driver preserves the original model/scenario, applies a process memory limit and attempts to save native inputs if construction succeeds; it never launches the study optimizer.

```sh
export MAMBA_ROOT_PREFIX="$PWD/.mamba"
export PIP_CACHE_DIR="$PWD/.cache/pip"
export TMPDIR="$PWD/.tmp"
mkdir -p "$TMPDIR"
python3 fetch_archives.py --model
python3 -m zipfile -e euro-calliope-sector-coupled-v0.1.zip author-model
micromamba create -y -p "$PWD/.author-env" -c conda-forge python=3.7 pip=20.0.2 setuptools=67.8.0
.author-env/bin/python -m pip install -c compatibility-constraints.txt https://github.com/calliope-project/calliope/archive/304cba8ab5e4fd212ea9f35cde49ac3a1a2303d7.tar.gz
OPENBLAS_NUM_THREADS=1 .author-env/bin/python check_model_resources.py --model-directory author-model/model --memory-gib 12 --wall-seconds 1200
```

If a GLPK executable is already available, provide its path using `--glpsol`. This only checks whether the author environment can locate that solver. A caught constructor failure returns exit code 2 and writes `resource-check/resource-check.json`.

The next step is to qualify input construction in an appropriately provisioned environment, or a carefully verified memory representation change, then build the same LP and run an explicitly documented open-solver adaptation. Reducing time or geography would change annual-demand and network constraints and needs its own scientific scope. The archive-only analysis remains complete and usable while fresh optimization is pending.

## Attribution and terms

The CSV is from Bryn Pickering's archived study outputs, DOI `10.5281/zenodo.6546817`; its data package specifies **CC BY 4.0**. Credit the study authors and archive when reusing it. The OSRI analysis/retrieval scripts are MIT. Model, source-code and solver terms remain separate. Human scientific review is pending.
