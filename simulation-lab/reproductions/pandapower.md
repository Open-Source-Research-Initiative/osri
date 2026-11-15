# Recompute the published pandapower switching analysis

How many switching states satisfy supply, radiality, and fault-current constraints in the paper's 10 kV ring network?

This example runs the authors' [case-study notebooks](https://github.com/e2nIEE/pandapower-paper/tree/6213b92acd265cf7803ff4b8978542957d0c9777) using pandapower 1.4.3. The research target is Section VII-B of [Thurner et al. (2018)](https://arxiv.org/html/1709.06743v2), DOI [10.1109/TPWRS.2018.2829021](https://doi.org/10.1109/TPWRS.2018.2829021): 276 combinations, 96 invalid topologies, 100 additional fault-current failures, and 80 valid states. Count equality is required. Per-state currents are additionally compared with the author archive at an analyst-selected tolerance of 1e-5 kA.

## Run the bounded target

Use Linux x86-64 with micromamba, Git, and a writable study directory. The supplied explicit environment lock downloads an isolated Python 3.6 environment. This legacy runtime is retained for this historical example.

```sh
export MAMBA_ROOT_PREFIX="$PWD/.mamba"
export PIP_CACHE_DIR="$PWD/.cache/pip"
export MPLCONFIGDIR="$PWD/.cache/matplotlib"
export NUMBA_CACHE_DIR="$PWD/.cache/numba"
export TMPDIR="$PWD/.tmp"
mkdir -p "$TMPDIR"
micromamba create -y -p "$PWD/.venv" --file python36-linux-64.explicit
.venv/bin/python -m pip install -r requirements-lock.txt
git clone https://github.com/e2nIEE/pandapower-paper.git
git -C pandapower-paper checkout 6213b92acd265cf7803ff4b8978542957d0c9777
MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 .venv/bin/python run_pandapower.py
```

The harness reads the original notebook model/functions and supplied Excel network. It adds reporting and comparison, without rewriting the numerical functions. No notebook server, Cairo, or igraph is needed for the switching analysis. Outputs go to `pandapower-output/`: `switches.csv`, `switches.json`, `switch-comparison.json`, and `run-record.json`.

The recorded run matched all four published counts. Valid switch IDs matched the author reference, and maximum fault-current error was **4.7622e-11 kA**, below the stated tolerance. The portable harness was run again successfully. This verifies this bounded paper target; human scientific review remains pending.

## Optional full-day computation and discrepancies

```sh
MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 .venv/bin/python run_pandapower.py --full-day
```

This executes all 97 supplied quarter-hour profile points using the original loaded switching-table order. The controller retains tap state across candidate evaluations; changing row order changes the numerical experiment. Use the original JSON order for a faithful notebook run.

The complete recorded calculation took about 133 seconds. It met the paper's voltage, line/transformer loading and fault-current bounds. Voltage, line loading, tap positions, current and switch choices matched the archived numerical results. Two measurement conventions need explicit treatment:

- The notebook computes interval loss energy in kWh by dividing power in kW by four. Stored reference `losses` use the power values. After the documented quarter-hour conversion, maximum energy error is **1.75e-10 kWh**. The initial raw-column comparison failed because the quantities had different units; the correction was established from the source formula, not fitted to a desired answer.
- Reference transformer loading is one tenth of the new percentage. The supplied transformer has `df=0.1`, and pandapower 1.4.3 explicitly divides nominal loading by this derating factor. This explains a plausible nominal-versus-derated convention, but the archived result's originating convention is not documented. The raw comparison remains flagged.

The article text reports nine selected switching states; the author notebook explicitly reports eleven. The new run matches the notebook's eleven and the saved switch choices. This difference remains unresolved, so the full-day execution is not labeled a complete reproduction of the article.

`outputs/` retains both the successful bounded comparison and full-day results, including all failed raw comparisons. `target.json` records the comparison declared before running. Original notebook and model notices remain upstream; pandapower is BSD-3-Clause. The OSRI wrapper is MIT. No claim to relicense the authors' model files is made.

## Download the recorded files

- [timeseries.png](files/pandapower/outputs/timeseries.png) — figure_or_log.
- [switch-run-record.json](files/pandapower/outputs/switch-run-record.json) — numeric_result.
- [switches.json](files/pandapower/outputs/switches.json) — numeric_result.
- [timeseries.csv](files/pandapower/outputs/timeseries.csv) — numeric_result.
- [switch-comparison.json](files/pandapower/outputs/switch-comparison.json) — numeric_result.
- [switches.csv](files/pandapower/outputs/switches.csv) — numeric_result.
- [timeseries.json](files/pandapower/outputs/timeseries.json) — numeric_result.
- [full-day-run-record.json](files/pandapower/outputs/full-day-run-record.json) — numeric_result.
- [README.md](files/pandapower/README.md) — portable driver or environment/source record.
- [python36-linux-64.explicit](files/pandapower/python36-linux-64.explicit) — portable driver or environment/source record.
- [requirements-lock.txt](files/pandapower/requirements-lock.txt) — portable driver or environment/source record.
- [requirements.txt](files/pandapower/requirements.txt) — portable driver or environment/source record.
- [run_pandapower.py](files/pandapower/run_pandapower.py) — portable driver or environment/source record.
- [target.json](files/pandapower/target.json) — portable driver or environment/source record.

[Complete run record](records/pandapower.json) · [All candidate attempts](README.md). Human scientific review is pending.
