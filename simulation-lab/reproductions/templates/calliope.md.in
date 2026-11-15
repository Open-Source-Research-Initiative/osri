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

## What prevented a new optimization

The [prebuilt model archive](https://doi.org/10.5281/zenodo.5774988) was also downloaded and its MD5 verified. It expands to about 2.67 GB and includes all input years, author setup instructions, model-building code and extra optimization constraints. Its `requirements.yml` specifies Python 3.7, Gurobi **9.1.2**, and Calliope commit `304cba8ab5e4fd212ea9f35cde49ac3a1a2303d7`.

The exact Calliope source was recovered via GitHub's commit archive after a normal Git checkout could not reach that commit. It was installed as `0.6.8-dev` in an isolated Python 3.7 environment; compatibility pins and the actual environment lock are included. Initial install failures from missing legacy NetCDF wheels and incompatible setuptools were diagnosed and resolved.

The original Gurobi runtime fails even a minimal solver prerequisite with **“License expired 2022-01-13.”** No new model optimization is claimed. `outputs/solver-blocker.log` preserves that failure; no license file is included. The archive README also estimates about two days for its full hourly model. Reducing geography or time without redesigning annual-demand constraints would change the experiment.

A licensed original solver, or an explicitly qualified open-solver port, is the next requirement for a new optimization. After that, solve one baseline with the archived assumptions and compare objective, feasibility residuals and capacities before attempting the 441-case ensemble. The included results analysis remains useful while that work is pending.

## Attribution and terms

The CSV is from Bryn Pickering's archived study outputs, DOI `10.5281/zenodo.6546817`; its data package specifies **CC BY 4.0**. Credit the study authors and archive when reusing it. The OSRI analysis/retrieval scripts are MIT. Model, source-code and solver terms remain separate. Human scientific review is pending.
