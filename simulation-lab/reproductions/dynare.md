# Execute the Smets–Wouters DSGE model at its supplied mode

[Smets and Wouters (2007)](https://www.aeaweb.org/articles?id=10.1257/aer.97.3.586) estimate a seven-observable US DSGE model. The [official replication archive](https://doi.org/10.3886/E116269V1) requires an account to download in this session. We instead ran the [maintained, attributed author-derived implementation](https://github.com/JohannesPfeifer/DSGE_mod/tree/26c21f79e4c6a6b19b18e6330edc5b23489907a4/Smets_Wouters_2007), whose header credits the original authors and documents differences.

The bounded run evaluates the model at the included old mode file, with `mode_compute=0`, `mh_replic=0`, `first_obs=1`, and 230 observations. It does **not** optimize the posterior or run MCMC. Exact original article sample/mode correspondence and a printed numerical target remain unverified, so this example makes no paper-result reproduction claim.

The portable Linux runtime was built under an ordinary user account, with Octave 9.4.0, Dynare 6.4, statistics 1.7.7, and pinned SLICOT source. No system packages or services changed. A clean reconstruction is:

```sh
sh get-source.sh
micromamba create -y -p ./octave-env -f environment-explicit.txt
sh build_runtime.sh
sh run_model.sh > model-run.log 2>&1
# In a separate Python environment, install requirements-postprocess.txt:
python extract_outputs.py
```

The explicit environment is Linux x86-64 and occupies about 3.5 GB. Source/build files and a working compiler need additional space. Build took several minutes here. `OCTAVE_HOME` relocates the portable package correctly; compiler variables and a local HDF5 pkg-config descriptor address package build metadata. The source retrieval script fetches dependencies at the recorded commits/releases; `source-hashes.json` records downloaded archive hashes. A clean reconstruction of the combined wrapper has not yet been repeated; the component commands were run during the retained build history.

The fresh model run produced `model-outputs.mat` and a **40 × 9 × 230** finite shock-decomposition array. `output-decomposition-y.csv` exports the output variable’s seven shock contributions, initial-condition term and total. Their sum residual is approximately **7.1e-15**. Laplace log data density is **−1844.0985587223** under these settings. These are actual run outputs and exploratory consistency diagnostics, not a comparison to a published target.

Warnings remain: Dynare cannot establish that the old mode file matches the present model; a prior-bound `gaminv` calculation reports convergence trouble; shock-decomposition setup converts negative array dimensions to zero; the preprocessor reports 33 warnings for unassigned steady-state variables. Do not infer scientific validity from finite output or exit 0. Inspect and resolve those warnings and match the official archive before a paper-level comparison. Human scientific review remains pending.

The maintained model implementation is GPL-3.0-or-later; Dynare and Octave have their own GPL notices and SLICOT is BSD-3-Clause. Original-data/archive terms remain separate. This bundle links/fetches upstream sources instead of vendoring them. Its original shell harness is MIT and guide CC BY 4.0.

## Download the recorded files

- [model-outputs.mat](files/dynare/model-outputs.mat) — native result.
- [output-decomposition-y.csv](files/dynare/output-decomposition-y.csv) — native result.
- [results.json](files/dynare/results.json) — execution evidence.
- [guide.md](files/dynare/guide.md) — portable driver or environment/source record.
- [get-source.sh](files/dynare/get-source.sh) — portable driver or environment/source record.
- [build_runtime.sh](files/dynare/build_runtime.sh) — portable driver or environment/source record.
- [run_model.sh](files/dynare/run_model.sh) — portable driver or environment/source record.
- [extract_outputs.py](files/dynare/extract_outputs.py) — portable driver or environment/source record.
- [environment-explicit.txt](files/dynare/environment-explicit.txt) — portable driver or environment/source record.
- [requirements-postprocess.txt](files/dynare/requirements-postprocess.txt) — portable driver or environment/source record.
- [source-hashes.json](files/dynare/source-hashes.json) — portable driver or environment/source record.
- [target.json](files/dynare/target.json) — portable driver or environment/source record.

[Complete run record](records/dynare.json) · [All candidate attempts](README.md). Human scientific review is pending.
