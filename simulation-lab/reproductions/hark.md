# Run Carroll’s author-associated HARK replication

This exercise runs the [Econ-ARK reproduction](https://econ-ark.org/materials/bufferstock-lifecycle/) of Carroll (1997), [Buffer-Stock Saving and the Life Cycle/Permanent Income Hypothesis](https://doi.org/10.1162/003355397555109). Carroll, Yusuf and Son are credited by the upstream material record. We restored its Python 3.7 / HARK 0.10.4 environment and executed its unmodified script at commit `0a278360b77eeac1df1e91374c168b3091365fbf`.

Run this in a new working directory containing the provided harness and environment files:

```sh
sh get-source.sh
micromamba create -y -p ./env -f environment.yml
MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ./env/bin/python capture_author_run.py
```

`environment-explicit.txt` also preserves exact Conda package URLs used here; `requirements-tested.txt` records installed Python versions. The harness reads `source/Code/Python/BufferStock-LifeCycle.py` without changing it, executes all its figure/table code, exports `table1.csv` and `results.json`, and copies the generated figures/tables to `output/`.

The specified comparison was the baseline **target net wealth/income ratio**, printed as **0.32** in Table I on p. 18. Before execution, we fixed an absolute tolerance of **0.005**, half the table’s 0.01 reporting unit. The run gives **0.3137699549295425**, an absolute difference of **0.00623004507045749**: the strict rounding comparison fails. This is an executed author-associated replication with a reported discrepancy; the original paper’s numerical result has not been established as reproduced.

The full script generated seven figures and two LaTeX tables. Its baseline average net wealth is 0.3417701614 and MPC out of wealth is 0.3158204896. Those simulation summaries are a single seeded author run, and do not supply uncertainty estimates. The deterministic target comparison is the primary recorded test. A SciPy non-progress warning occurs elsewhere in the full script; exit 0 does not establish convergence of every computed quantity.

The upstream reproduction differs from the original paper in shock discretization and simulation setup, and its baseline uses `DiscFac=0.96`. The paper/code shock-dispersion discrepancy remains documented in the existing lab guide. Resolve these methodological differences and inspect solver residuals before broadening the scientific claim. Human scientific review is pending.

The paper PDF is restricted and is not included. Fetch the public author source from its own repository; review its reuse terms before redistributing code. HARK itself is Apache-2.0. This bundle’s original harness is MIT and original guide is CC BY 4.0.

## Download the recorded files

- [results.json](files/hark/results.json) — execution evidence.
- [table1.csv](files/hark/table1.csv) — native result.
- [table1.tex](files/hark/output/Tables/table1.tex) — native result.
- [table2.tex](files/hark/output/Tables/table2.tex) — native result.
- [Figure1a.png](files/hark/output/Figures/Figure1a.png) — execution evidence.
- [Figure1b.png](files/hark/output/Figures/Figure1b.png) — execution evidence.
- [Figure5a.png](files/hark/output/Figures/Figure5a.png) — execution evidence.
- [Figure5b.png](files/hark/output/Figures/Figure5b.png) — execution evidence.
- [Figure5c.png](files/hark/output/Figures/Figure5c.png) — execution evidence.
- [Figure6.png](files/hark/output/Figures/Figure6.png) — execution evidence.
- [Figure7.png](files/hark/output/Figures/Figure7.png) — execution evidence.
- [guide.md](files/hark/guide.md) — portable driver or environment/source record.
- [capture_author_run.py](files/hark/capture_author_run.py) — portable driver or environment/source record.
- [get-source.sh](files/hark/get-source.sh) — portable driver or environment/source record.
- [environment.yml](files/hark/environment.yml) — portable driver or environment/source record.
- [environment-explicit.txt](files/hark/environment-explicit.txt) — portable driver or environment/source record.
- [requirements-tested.txt](files/hark/requirements-tested.txt) — portable driver or environment/source record.
- [target.json](files/hark/target.json) — portable driver or environment/source record.

[Complete run record](records/hark.json) · [All candidate attempts](README.md). Human scientific review is pending.
