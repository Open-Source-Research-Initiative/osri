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
