# Run the historical LuST city-traffic model

This example runs the authors' complete Luxembourg network and traffic demand with **SUMO 0.26.0**, the version identified in their [scenario repository](https://github.com/lcodeca/LuSTScenario/tree/5edb7ecb9ad196c39172b6eb95d19ed789f4b1a6). It is tied to [Codeca et al. (2017)](https://doi.org/10.1109/MITS.2017.2666585), *Luxembourg SUMO Traffic (LuST) Scenario: Traffic Demand Evaluation*.

The run covers the first simulated hour with three seeds. Network geometry and demand are retained. Bounding the duration makes this an adaptation; it does not reproduce the full-day traffic validation.

## Build the isolated historical runtime

Use Linux x86-64, Python 3.12+, Git, GNU C++/make, and micromamba. All working files are created in the study directory.

```sh
bash build_runtime.sh
python3 run_lust.py
```

`fetch_source.py` retrieves the exact source release, verifies its SHA256, and checks out the pinned author scenario. Downloads include roughly 13 MB of SUMO source and a scenario checkout of roughly 450 MB. `build_runtime.sh` creates an isolated Xerces environment from the explicit lock and compiles the release.

The tested build used GNU C++ 13.3.0. The compatibility flags select C++11, include the standard floating-point/math headers, and provide the legacy `HUGE` macro as `FLT_MAX`. No model or simulator algorithm source was edited. Local XML schema validation is disabled at execution because legacy Xerces cannot retrieve a current HTTPS schema; the simulator still parses the unchanged scenario inputs.

The actual configuration lives under **`LuSTScenario/scenario/`**. The harness supplies absolute output paths to avoid the legacy logger's path-prefix behavior. The preserved build/run logs include the original compiler and schema failures and their corrections.

## Inspect the results

`run-output/seed42`, `seed43`, and `seed44` contain native `summary.xml`, `tripinfo.xml`, and logs. `run-output/run-record.json` records exact commands, elapsed times, per-seed statistics and the limits of the comparison.

The recorded runs all inserted **878 vehicles** by the end of the first hour. Completed trips were **757, 761, and 756**, leaving **121, 117, and 122** vehicles running. Mean duration among completed trips was **486.024, 487.896, and 487.311 seconds**. The standard deviation of these three seed means is recorded; three repeats provide only a small check of simulation variability.

Trips still running at the cutoff are censored. These conditional completed-trip means cannot describe all trips or the full-day city. A successful run and valid XML output do not establish that the demand model matches real traffic observations.

## What is still needed for the paper comparison

The [2017 institutional record](https://orbilu.uni.lu/handle/10993/28678) lists `LuST2.pdf` as a 3.09 MB author preprint requiring a copy request. The full article's numerical validation target and original observed traffic series were not available for this run. Numbers from the distinct 2015 LuST paper were deliberately not substituted.

Retrieve the 2017 article and its validation observations, select the exact configuration/measurement window and error statistic, and declare tolerances before a new comparison. Then extend the original duration and use enough repeated runs to quantify uncertainty. This guide is a working author-model adaptation while that comparison remains pending.

SUMO 0.26 source is GPL-3.0-or-later. The LuST scenario is MIT; its bundled notices remain authoritative. The OSRI retrieval/build/run harnesses are MIT. No simulator binary or third-party scenario source is redistributed here. Human scientific review remains pending.
