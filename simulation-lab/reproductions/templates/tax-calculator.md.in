# Rerun the macro stage of a tax-policy paper

This exercise uses the [author replication archive](https://github.com/rickecon/TaxFuncIntegr/tree/715cc76e3305c00dd64d79521c504bb388c6d87d) for DeBacker, Evans and Phillips, *Integrating Microsimulation Models of Tax Policy into a DGE Macroeconomic Model*. The archive includes its **May 2018 manuscript** and public fitted tax-function/calibration inputs. The [journal article](https://doi.org/10.1177/1091142118816744) appeared in 2019; agreement with its final numerical tables has not been checked.

We freshly solved the baseline and counterfactual **macro steady states** using the authors’ unchanged OG-USA solver and supplied fitted parameters. **Tax-Calculator microsimulation/PUF estimation and transition paths were not rerun.** Tax-Calculator 0.19.0 is installed because the legacy macro package imports it; that import does not count as micro-estimation execution.

```sh
sh get-source.sh
micromamba create -y -p ./legacy-env -f environment.yml
./legacy-env/bin/python -m pip install -r requirements-legacy.txt
./legacy-env/bin/python -m pip install --no-deps ./taxcalc-source
MPLBACKEND=Agg OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ./legacy-env/bin/python run_fitted_pair.py
```

The harness reads the pinned archive’s `model_params.pkl` for `_DEP_Age`, invokes `SS.create_steady_state_parameters` and `SS.run_SS`, and stores fresh native results under `output/` and `pair-output/`. It does not read PUF records or invoke `get_micro_data`. The source’s `OUTPUT_BASELINE` represents TCJA law and `OUTPUT_REFORM` represents the 2017-law counterfactual; the ratio is oriented accordingly.

Before the paired run, we selected Table 7/8 of the **May 2018 manuscript**, preferred age-and-income-source specification, steady-state GDP change **+0.07%**, with absolute tolerance **0.005 percentage points** (half its printed 0.01-point unit). Actual change: **+0.069545535143%**, difference **0.000454464857 percentage points**, which passes that rounding comparison. The six baseline aggregate outputs also match the author’s archived steady state within `3e-15`; the declared regression tolerance was `rtol=1e-6, atol=1e-8`.

This run also exposes an economic-feasibility problem: government spending is **−0.01294664762** in the TCJA steady state and **−0.01051179371** in the counterfactual, in model units. The author solver warns that the debt closure requires infeasible negative spending. Thus the numerical table match is useful reproduction evidence for a bounded implementation stage; it does not establish a feasible policy prediction. Native resource residuals are about `5.3e-14`/`1.6e-14` and maximum Euler residuals below `4e-13`, but those residuals do not cure the negative-spending condition.

Historical dependency recovery required Python 3.6 and Dask 0.17.5; newer Dask removes the solver’s `get=` API. Failed Python 3.7/Dask attempts are retained in the research record. The source and public fitted inputs are CC0; this original harness is MIT and guide CC BY 4.0. Do not add restricted IRS PUF data to the lab. Human scientific review remains pending.
