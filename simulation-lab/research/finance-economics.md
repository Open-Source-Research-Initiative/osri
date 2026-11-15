# Finance, economics, and policy: paper-to-code routes

[All 60 tools](README.md) · [How to contribute](../contributing.md)

These are construction routes researched by agents. The execution line reports the bounded work actually performed; the comparison section defines what remains before claiming a published result. Human scientific review is pending.

## quantlib

**QuantLib** — Can a European call computed by a library and Monte Carlo agree with the original pricing equation?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** high.

### Paper for quantlib

Fischer Black; Myron Scholes (1973). [The Pricing of Options and Corporate Liabilities](https://doi.org/10.1086/260062). 10.1086/260062.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://www.journals.uchicago.edu/doi/10.1086/260062). Metadata verification: confirmed. Full-text access: Publisher metadata checked live; user-supplied restricted article previously inspected; no PDF redistribution.

**Target in the paper:** Assumptions p. 640; Eq. 13 p. 644. Eq. 13 is the target, using explicitly synthetic inputs rather than historical observations.

### Code and inputs for quantlib

[Artifact or upstream source](https://github.com/lballabio/QuantLib). Current official implementation and numerical-engine comparison, not Black/Scholes author code. Existing OSRI Python adaptation implements the equation.

**Source inspected:** yes. **Ref:** master. **Commit:** 9ba30347b4ea179a5f4daec446cd221d21b8721f.

**Files:** Examples/EquityOption/EquityOption.cpp

**Terms:** BSD-3-Clause

**Environment and compute:** Existing lab Python 3.12 environment: QuantLib 1.44 and pinned numerical dependencies; alternatively compile the upstream C++ example in a separate CMake build. CPU; seconds to minutes for the teaching case.

**Inputs:** Existing OSRI adaptation uses synthetic spot=100, strike=100, rate=0.05, volatility=0.2, maturity=1 year, 50000 paths and seed 42. The C++ upstream example has different put-option inputs.

**Data access:** Synthetic inputs; no market-data subscription.

### Construct and compare quantlib

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Existing lab command, not a new execution in this research pass ``
2. `` python simulation-lab/examples/option_monte_carlo.py --help ``
3. `` # Follow the existing CPU walkthrough with its pinned requirements and explicit output directory. Do not mix the C++ example parameters with the Python target. ``

**Expected outputs:** Native options CSV, parameters JSON, Monte Carlo standard error and confidence interval.

**Comparison with the paper:** Compute Eq. 13 independently; compare QuantLib analytic value to double-precision formula and assess Monte Carlo error using its reported standard error. Existing run analytic value was 10.450583572185565; matching it verifies the synthetic equation example, not an empirical published table.

**Execution result:** Source inspection only; no new execution for this route.

**Execution evidence:** None recorded.

**Blockers:** No original 1973 source-code artifact; the existing example is a modern adaptation.

**Next action:** Retain current formula test, add a grid over maturity/moneyness/volatility and convergence versus path count before proposing a numerical-method study.

**Gaps:** Equation adaptation already executed in prior lab release; no new paper-result reproduction.

### Sources for quantlib

- [Publisher confirms title/authors/year; Crossref request was rate-limited.](https://www.journals.uchicago.edu/doi/10.1086/260062) (inspected 2026-11-15).
- [Official source has distinct synthetic put inputs and analytic/MC pricing engines.](https://github.com/lballabio/QuantLib/blob/9ba30347b4ea179a5f4daec446cd221d21b8721f/Examples/EquityOption/EquityOption.cpp) (inspected 2026-11-15).

## abides

**ABIDES** — How does a large buy order alter a simulated order book and the subsequent price path?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** high.

### Paper for abides

David Byrd; Maria Hybinette; Tucker Hybinette Balch (2019). [ABIDES: Towards High-Fidelity Market Simulation for AI Research](https://arxiv.org/html/1904.12066). arXiv:1904.12066v1; conference version DOI 10.1145/3384441.3395986.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://arxiv.org/abs/1904.12066). Metadata verification: confirmed. Full-text access: Open HTML inspected; Crossref confirms 2020 conference ABIDES record. The detailed target here is explicitly the 2019 preprint.

**Target in the paper:** Section 6, Figures 6–7: greed-controlled impact event and aligned event-study paths; Section 5 Figure 4 uses historical IBM/MSFT trades.

### Code and inputs for abides

[Artifact or upstream source](https://github.com/abides-sim/abides). Repository explicitly linked by the preprint. Current impact.py uses a generated mean-reverting oracle, unlike the historical-data oracle described in the preprint.

**Source inspected:** yes. **Ref:** master. **Commit:** c4bf157678928934417aba6073eb0651aeaf6d15.

**Files:** config/impact.py; config/rmsc03.py; requirements.txt; README.md

**Terms:** BSD-3-Clause

**Environment and compute:** Isolated historical Python environment; inspect old NumPy/pandas/SciPy requirements before solving dependencies. Do not install into the modern CPU environment. CPU; many-agent event simulation; benchmark one session before scheduling seed batches.

**Inputs:** For a synthetic adaptation, config/impact.py, same random seed in control and treatment, documented greed parameter. Exact paper replay additionally requires original historical ticks and configuration revision.

**Data access:** Synthetic oracle needs no ticks; original historical-trade days may require licensed tick access.

### Construct and compare abides

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Proposed command from inspected CLI; clone and checkout the pinned artifact first ``
2. `` python -u abides.py -c impact -s 1234 -g 0.3 -l impact_g03 ``
3. `` python -u abides.py -c impact -s 1234 -g 1.9 -l impact_g19 ``
4. `` # Repeat paired control/treatment experiments over independently selected seeds; inspect -i semantics (it disables impact). ``

**Expected outputs:** Exchange/order-book logs, aligned trade/midprice series, per-seed price-impact curves.

**Comparison with the paper:** Predeclare event time and signed price-change metric; compare treatment-control impact over time with Figure 6/7 after recovering historical configuration and inputs. Current synthetic-oracle run is an adaptation; paper curve values and tolerance are not yet extracted.

**Execution result:** Source inspection only; no new execution for this route.

**Execution evidence:** None recorded.

**Blockers:** Current config uses different background agents/oracle.; Historical paper configuration and tick data not recovered.; Historical environment not executed.

**Next action:** Recover the paper-era commit/configuration and lawful tick inputs; begin with paired synthetic impact experiments while explicitly labeling the adaptation.

**Gaps:** A runnable RMSC03 tutorial alone would not reproduce these paper figures.

### Sources for abides

- [Sections 5–6 identify background agents, historical data, greed experiment and Figures 4–7; Section 8 links source.](https://arxiv.org/html/1904.12066) (inspected 2026-11-15).
- [CLI greed/seed/log flags; generated MeanRevertingOracle differs from the preprint.](https://github.com/abides-sim/abides/blob/c4bf157678928934417aba6073eb0651aeaf6d15/config/impact.py) (inspected 2026-11-15).

## finrl

**FinRL** — Does an ensemble of PPO, A2C and DDPG improve risk-adjusted stock-trading performance over the paper’s baselines?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for finrl

Hongyang Yang; Xiao-Yang Liu; Shan Zhong; Anwar Walid (2020). [Deep reinforcement learning for automated stock trading: an ensemble strategy](https://doi.org/10.1145/3383455.3422540). 10.1145/3383455.3422540.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1145/3383455.3422540). Metadata verification: confirmed. Full-text access: Crossref title/authors/year checked; author university-hosted paper text available.

**Target in the paper:** Empirical ensemble-versus-individual-agent and DJIA/minimum-variance backtests; target is the paper performance comparison, with table/figure numbers and numeric tolerances still to extract from full text.

### Code and inputs for finrl

[Artifact or upstream source](https://github.com/AI4Finance-Foundation/FinRL-Meta). Author-maintained notebook explicitly named for the ICAIF 2020 experiment, but subsequently updated. Exact paper repository linked by a later arXiv record returns HTTP 404.

**Source inspected:** yes. **Ref:** master. **Commit:** 286fef6c828a02a2ccf807c05b292d8cb28f8e95.

**Files:** examples/FinRL_Ensemble_StockTrading_ICAIF_2020.ipynb

**Terms:** MIT; market-data reuse rights separate

**Environment and compute:** Isolated pinned FinRL/Stable-Baselines3/PyTorch/Jupyter environment. Notebook installs FinRL from mutable Git HEAD; replace with a tested immutable version before execution. CPU possible for small diagnostics; full rolling ensemble training likely hours, GPU optional.

**Inputs:** DJIA constituents, adjusted OHLCV and indicators, transaction costs, split dates, turbulence threshold, training budgets and seeds. Inspected notebook currently uses 2010-01-01..2021-10-01 train and 2021-10-01..2023-03-01 test, so it is not the original 2020 evaluation.

**Data access:** Notebook calls YahooDownloader; freeze exact historical inputs and confirm provider terms and adjusted-price treatment. No live trading needed.

### Construct and compare finrl

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Proposed preparation: clone FinRL-Meta and checkout the recorded commit ``
2. `` # Inspect every notebook cell; pin FinRL dependency and archive lawful input data before training ``
3. `` jupyter nbconvert --execute --to notebook --ExecutePreprocessor.timeout=-1 examples/FinRL_Ensemble_StockTrading_ICAIF_2020.ipynb --output ensemble.executed.ipynb ``

**Expected outputs:** Executed notebook, models, account-value CSVs, ensemble-selection trace and backtest-statistic tables.

**Comparison with the paper:** Recreate the original evaluation universe and splits; compare annual return, drawdown and Sharpe statistics over repeated seeds. Predeclare tolerance/distributional comparison. Current notebook dates and dependencies require changes and must be described as an adaptation until matched.

**Execution result:** Source inspection only; no new execution for this route.

**Execution evidence:** None recorded.

**Blockers:** Exact original repository URL currently 404.; Notebook data splits are newer than paper.; Mutable dependency installs and random seeds not fully pinned.

**Next action:** Recover archived paper-era notebook/data, then run a frozen backtest with repeated seeds; use author notebook as a construction scaffold meanwhile.

**Gaps:** Do not describe contemporary notebook returns as reproduced ICAIF-2020 results.

### Sources for finrl

- [Verified article identity and 2020 date.](https://api.crossref.org/works/10.1145/3383455.3422540) (inspected 2026-11-15).
- [Notebook inspected: Yahoo data, ensemble algorithms, output files, mutable install and 2021–2023 test split.](https://github.com/AI4Finance-Foundation/FinRL-Meta/blob/286fef6c828a02a2ccf807c05b292d8cb28f8e95/examples/FinRL_Ensemble_StockTrading_ICAIF_2020.ipynb) (inspected 2026-11-15).
- [Author-hosted conference paper available for detailed performance-target extraction.](https://openfin.engineering.columbia.edu/sites/openfin.engineering.columbia.edu/files/content/publications/ensemble.pdf) (inspected 2026-11-15).

## engine

**Open Source Risk Engine** — How does central clearing change systemic exposure and counterparty credit risk?

**Route:** Paper result candidate. **Execution:** Attempted; blocked. **Source confidence:** high.

### Paper for engine

Nikolai Nowaczyk; Sharyn O’Halloran (2024). [Computing the impact of central clearing on systemic risk](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2024.1138611/full). 10.3389/frai.2024.1138611.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.3389/frai.2024.1138611). Metadata verification: confirmed. Full-text access: Open full HTML inspected, including methods, validation, results and source footnotes.

**Target in the paper:** Sections 7.3–7.6 ORE risk calculations and notebook visualization; Section 8.4 Figure 15: 50% of exposure concentrated in CCPs; Figure 14 relative CVA impacts. Footnotes 13, 16–17 link code and ORE v1.8.4.0 inputs.

### Code and inputs for engine

[Artifact or upstream source](https://github.com/niknow/systemic-risk). Paper-linked author notebook and precomputed simulation outputs. Repository tree contains dashboard assets, not the upstream generator that invokes ORE. ORE v1.8.4.0 is separately referenced by the article.

**Source inspected:** yes. **Ref:** master. **Commit:** 677f5e7b639d4b8de18767a0f2b8db4844ceaf1a.

**Files:** dashboards/central_clearing/simulation_cva/central_clearing_sim_cva.ipynb; dashboards/central_clearing/simulation_cva/environment.yml; dashboards/central_clearing/simulation_cva/df_risk_systemic.csv; dashboards/central_clearing/simulation_cva/df_risk_cp.csv; dashboards/central_clearing/simulation_cva/risk_graphs_nx.json

**Terms:** No repository license found; inspect permission before redistributing author assets. ORE itself BSD-3-Clause.

**Environment and compute:** Historical dashboard uses Windows-specific Conda Python 3.7.5, pandas 0.23.4, networkx 2.2; porting to Linux needs a new recorded environment. Fresh simulation additionally needs ORE v1.8.4.0 plus missing generator. Replot small enough for CPU; full ORE portfolio/network batch must be profiled after generator recovery.

**Inputs:** Bundled risk CSVs/graphs for a figure replot; original generated portfolios, market/calibration files, random graph settings and ORE inputs needed for a fresh run.

**Data access:** Public dashboard includes synthetic-output tables; reuse license unspecified. Bundled ORE market inputs referenced in paper.

### Construct and compare engine

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Proposed replot route, after constructing a compatible isolated environment ``
2. `` cd dashboards/central_clearing/simulation_cva ``
3. `` jupyter notebook central_clearing_sim_cva.ipynb ``
4. `` # Fresh simulation cannot be specified completely from this repository: retrieve portfolio-generation and ORE orchestration code first. ``

**Expected outputs:** Dashboard exposure/CVA plots and parsed risk tables; fresh ORE exposure CSVs require missing orchestration.

**Comparison with the paper:** No new ORE numerical outputs. Prior saved-output shares 50.339%–50.927% still differ from exact paper 50% statement and remain unadjudicated.

**Execution result:** Fresh simulation cannot run from retrieved author artifact: no portfolio generator or ORE orchestration in full source/history. Prior saved-output analysis is retained separately and not counted as a fresh run.

**Execution evidence:** [Author-code attempt](../reproductions/engine.md); [Run record](../reproductions/records/engine.json)

**Blockers:** Author portfolio generator, ORE orchestration/configurations and original seed specification missing.; Paper-linked saved-output version correspondence/discrepancy unresolved.; Dashboard repository has no license found.

**Next action:** Retrieve author generator/configuration artifact and versioned ORE v1.8.4.0 inputs; then declare a numerical target and tolerance before running.

**Gaps:** Author portfolio generator, ORE orchestration/configurations and original seed specification missing.; Paper-linked saved-output version correspondence/discrepancy unresolved.; Dashboard repository has no license found.

### Sources for engine

- [ORE use, linked dashboard and versioned inputs, validation checks, Figure 15 50% exposure target.](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2024.1138611/full) (inspected 2026-11-15).
- [Tree contains notebook/CSV/graph assets; no ORE generator found.](https://github.com/niknow/systemic-risk/tree/677f5e7b639d4b8de18767a0f2b8db4844ceaf1a) (inspected 2026-11-15).
- [Notebook explicitly explores result data and loads bundled CSVs.](https://github.com/niknow/systemic-risk/blob/677f5e7b639d4b8de18767a0f2b8db4844ceaf1a/dashboards/central_clearing/simulation_cva/central_clearing_sim_cva.ipynb) (inspected 2026-11-15).

## hark

**HARK / Econ-ARK** — Can the author-associated code regenerate Carroll’s buffer-stock saving figures and tables?

**Route:** Paper result candidate. **Execution:** Example executed. **Source confidence:** high.

### Paper for hark

Christopher D. Carroll (1997). [Buffer-Stock Saving and the Life Cycle/Permanent Income Hypothesis](https://doi.org/10.1162/003355397555109). 10.1162/003355397555109.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1162/003355397555109). Metadata verification: confirmed. Full-text access: User-supplied restricted full text previously inspected; live Crossref and Econ-ARK material record checked.

**Target in the paper:** Figures I, V, VI and VII and Tables I–II correspond to named Figure1a/1b, Figure5a/b/c, Figure6/7 and table1/2 output code. Original baseline pp. 5–8 already annotated by the lab.

### Code and inputs for hark

[Artifact or upstream source](https://github.com/econ-ark/BufferStock-LifeCycle). Econ-ARK identifies this as a replication by Carroll, Yusuf and Son. Source explicitly saves paper-associated figures/tables.

**Source inspected:** yes. **Ref:** master. **Commit:** 0a278360b77eeac1df1e91374c168b3091365fbf.

**Files:** reproduce.sh; Code/Python/BufferStock-LifeCycle.py; binder/environment.yml; Paper/Figures; Paper/Tables

**Terms:** Inspect repository license and HARK Apache-2.0 separately; restricted article excluded.

**Environment and compute:** Historical Econ-ARK notebook runtime; README documents econark/econ-ark-notebook:0.10.4; Python script metadata says 3.7.6. Modern HARK 0.17.2 has changed APIs. CPU; policy-function solutions and household lifecycle simulation, followed by plotting.

**Inputs:** Author calibration and lifecycle profiles from the pinned script; preserve shock distribution details, unemployment probability, discount factor and exact growth variants.

**Data access:** Code/input profiles publicly available; original PDF remains restricted and is not redistributed.

### Construct and compare hark

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` git clone https://github.com/econ-ark/BufferStock-LifeCycle.git ``
2. `` cd BufferStock-LifeCycle ``
3. `` git checkout 0a278360b77eeac1df1e91374c168b3091365fbf ``
4. `` # Prepare its historical environment; inspected reproduce.sh runs the Python script using IPython ``
5. `` bash reproduce.sh ``

**Expected outputs:** Paper/Figures/Figure1a.png, Figure1b.png, Figure5a.png, Figure5b.png, Figure5c.png, Figure6.png, Figure7.png; Paper/Tables/table1.tex and table2.tex.

**Comparison with the paper:** Actual script execution restored; baseline target net wealth rounds to 0.31 rather than printed 0.32. Author implementation methods differ from original paper. No paper reproduction claim.

**Execution result:** Seven figure PNGs and two LaTeX tables generated from exact source. Strict original-paper baseline target comparison failed; SciPy non-progress warning retained.

**Execution evidence:** [Author-code attempt](../reproductions/hark.md); [Run record](../reproductions/records/hark.json)

**Blockers:** Strict printed table comparison fails.; Author discretization/simulation and calibration conventions differ from original paper.; SciPy non-progress warning elsewhere in full script; convergence of all quantities not established.

**Next action:** Audit numerical settings/shock distribution and deterministic target residual; resolve mismatch before declaring paper result reproduced.

**Gaps:** Strict printed table comparison fails.; Author discretization/simulation and calibration conventions differ from original paper.; SciPy non-progress warning elsewhere in full script; convergence of all quantities not established.

### Sources for hark

- [Author-associated replication identity and setup.](https://econ-ark.org/materials/bufferstock-lifecycle/) (inspected 2026-11-15).
- [Named figure/table output paths and historical HARK imports.](https://github.com/econ-ark/BufferStock-LifeCycle/blob/0a278360b77eeac1df1e91374c168b3091365fbf/Code/Python/BufferStock-LifeCycle.py) (inspected 2026-11-15).
- [Actual script entry point differs from stale README wording.](https://github.com/econ-ark/BufferStock-LifeCycle/blob/0a278360b77eeac1df1e91374c168b3091365fbf/reproduce.sh) (inspected 2026-11-15).

## quantecon

**QuantEcon.py** — How does uninsured idiosyncratic earnings risk affect precautionary savings and equilibrium capital?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** high.

### Paper for quantecon

S. Rao Aiyagari (1994). [Uninsured Idiosyncratic Risk and Aggregate Saving](https://doi.org/10.2307/2118417). 10.2307/2118417.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.2307/2118417). Metadata verification: confirmed. Full-text access: Crossref identity checked; full original paper not read in this pass. Maintainers’ full model lecture/code inspected.

**Target in the paper:** QuantEcon lecture The Aiyagari Model, equilibrium implementation and capital-supply/demand plot; original article quantitative table target not yet inspected.

### Code and inputs for quantecon

[Artifact or upstream source](https://github.com/QuantEcon/lecture-python.myst). Maintainer-authored teaching implementation of Aiyagari’s model, not the 1994 author program. The live lecture uses a two-state simplified income process.

**Source inspected:** yes. **Ref:** main. **Commit:** 007bbd592a4c1f43931ebb0eeb0e64ba36fa8a47.

**Files:** lectures/aiyagari.md

**Terms:** Lecture/book license and QuantEcon.py MIT separately; inspect before copying code.

**Environment and compute:** Pinned Python + quantecon, JAX/JAXLIB, SciPy and matplotlib; enable JAX 64-bit as the lecture does. CPU supported although lecture was built using GPU. CPU supported; first JAX compilation adds overhead.

**Inputs:** Lecture model: log utility, beta=0.96, 100 asset points, two productivity states [0.1,1.0], transition [[0.9,0.1],[0.1,0.9]], alpha=0.33, delta=0.05. These are teaching defaults, not asserted to match the paper calibration.

**Data access:** Synthetic model inputs, no household microdata needed.

### Construct and compare quantecon

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` git clone https://github.com/QuantEcon/lecture-python.myst.git ``
2. `` cd lecture-python.myst ``
3. `` git checkout 007bbd592a4c1f43931ebb0eeb0e64ba36fa8a47 ``
4. `` # Proposed: execute lectures/aiyagari.md as a MyST/Jupyter notebook in its pinned book environment; preserve all cells and outputs. ``

**Expected outputs:** Savings policy, stationary distribution, capital-supply curve, demand curve and equilibrium interest rate/capital.

**Comparison with the paper:** For the teaching case verify stationarity, probability normalization, resource feasibility and capital-market residual under grid refinement. Recover the original paper’s discretization/calibration and named table cells before any 1994 numerical comparison.

**Execution result:** Source inspection only; no new execution for this route.

**Execution evidence:** None recorded.

**Blockers:** Original paper result/table and calibration not audited.; Book environment and JAX versions need a tested lock.

**Next action:** Execute the pinned lecture and export numerical arrays/residuals, then construct a separate paper-matched calibration and quantitative comparison.

**Gaps:** Do not label the simplified lecture as an original-paper table reproduction.

### Sources for quantecon

- [Explicit Aiyagari reference, model assumptions, code and CPU support.](https://python.quantecon.org/aiyagari.html) (inspected 2026-11-15).
- [Pinned live lecture source inspected.](https://github.com/QuantEcon/lecture-python.myst/blob/007bbd592a4c1f43931ebb0eeb0e64ba36fa8a47/lectures/aiyagari.md) (inspected 2026-11-15).
- [Verified article title/author/year.](https://api.crossref.org/works/10.2307/2118417) (inspected 2026-11-15).

## og-core

**OG-Core** — How do alternative tax-function representations change predicted macroeconomic responses to tax policy?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for og-core

Jason DeBacker; Richard W. Evans; Kerk L. Phillips (2019). [Integrating Microsimulation Models of Tax Policy into a DGE Macroeconomic Model](https://doi.org/10.1177/1091142118816744). 10.1177/1091142118816744.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1177/1091142118816744). Metadata verification: confirmed. Full-text access: Publisher/Crossref metadata and author replication README inspected; full-text draft available from authors/conference.

**Target in the paper:** Tax function alternatives and baseline/reform general-equilibrium results; exact published table/figure numbers and cells still require final-paper inspection. Author repository provides TFI_tables_figures.py.

### Code and inputs for og-core

[Artifact or upstream source](https://github.com/PSLmodels/OG-Core). Current OG-Core is a modern framework connected to country models such as OG-USA. Exact 2019 paper code lives in rickecon/TaxFuncIntegr and uses historical OG-USA; switching to OG-Core is a port, not a same-code rerun.

**Source inspected:** yes. **Ref:** master. **Commit:** 7c31fbb5e3cb0fc49de5e99da444af9c7c0bb469.

**Files:** examples/run_ogcore_example.py; examples/example-diffs; ogcore/SS.py; ogcore/TPI.py

**Terms:** CC0-1.0

**Environment and compute:** Isolated current OG-Core Python environment; separate historical TaxFuncIntegr environment if reproducing the 2019 result. Note README points to run_examples but inspected snapshot actually uses examples/. CPU; upstream README warns full baseline/reform paths may exceed two hours.

**Inputs:** Current official example sets baseline corporate rate 0.21 and reform 0.35 with its own spending paths, not the exact historical paper experiment. Paper route requires preserved tax-function fits and historical demographics.

**Data access:** Current example ships synthetic/default calibration; paper fits available but PUF microdata are restricted.

### Construct and compare og-core

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` git clone https://github.com/PSLmodels/OG-Core.git ``
2. `` cd OG-Core ``
3. `` git checkout 7c31fbb5e3cb0fc49de5e99da444af9c7c0bb469 ``
4. `` # Proposed environment install from the pinned pyproject, then run the actual inspected entry point ``
5. `` python examples/run_ogcore_example.py ``

**Expected outputs:** examples/OG-Core-Example/BASELINE and REFORM outputs, model_params.pkl, SS/SS_vars.pkl, TPI/TPI_vars.pkl, example_output.csv and example_plots.

**Comparison with the paper:** First reproduce the current official example with market-clearing/Euler residuals and its own regression reference, after resolving outdated example-diffs names. Then port a named TaxFuncIntegr paper case and compare aggregate transition paths under the same calibration.

**Execution result:** Source inspection only; no new execution for this route.

**Execution evidence:** None recorded.

**Blockers:** Exact historical model uses OG-USA, not current OG-Core.; README path/output names and examples/example-diffs are stale relative to current script.; Paper-matched port and full output comparison not performed.

**Next action:** Freeze a compatible OG-Core release and execute its example; separately define a paper-calibration port using the author archive and explicit differences.

**Gaps:** Current OG-Core tutorial cannot be presented as the historical paper replication.

### Sources for og-core

- [Framework/country-model relationship and runtime guidance.](https://github.com/PSLmodels/OG-Core/blob/7c31fbb5e3cb0fc49de5e99da444af9c7c0bb469/README.md) (inspected 2026-11-15).
- [Actual entry point, corporate tax experiment and output locations.](https://github.com/PSLmodels/OG-Core/blob/7c31fbb5e3cb0fc49de5e99da444af9c7c0bb469/examples/run_ogcore_example.py) (inspected 2026-11-15).
- [Paper-associated legacy OG-USA code and data restrictions.](https://github.com/rickecon/TaxFuncIntegr/blob/715cc76e3305c00dd64d79521c504bb388c6d87d/README.md) (inspected 2026-11-15).
- [Verified published paper identity.](https://api.crossref.org/works/10.1177/1091142118816744) (inspected 2026-11-15).

## tax-calculator

**Tax-Calculator** — Can the paper’s micro tax-rate estimates and macro tax-function comparisons be regenerated?

**Route:** Paper result candidate. **Execution:** Example executed. **Source confidence:** high.

### Paper for tax-calculator

Jason DeBacker; Richard W. Evans; Kerk L. Phillips (2019). [Integrating Microsimulation Models of Tax Policy into a DGE Macroeconomic Model](https://doi.org/10.1177/1091142118816744). 10.1177/1091142118816744.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1177/1091142118816744). Metadata verification: confirmed. Full-text access: Publisher/Crossref metadata and author replication README inspected; full-text draft available from authors/conference.

**Target in the paper:** May 2018 author manuscript DEP_TaxFuncs.pdf, Tables 7 and 8, preferred specification steady-state GDP change +0.07%; final 2019 journal numerical tables not independently matched.

### Code and inputs for tax-calculator

[Artifact or upstream source](https://github.com/rickecon/TaxFuncIntegr). Author replication code for the paper/draft; calls Tax-Calculator and stores fitted tax-function outputs and solved model outputs.

**Source inspected:** yes. **Ref:** master. **Commit:** 715cc76e3305c00dd64d79521c504bb388c6d87d.

**Files:** run_TaxFuncInt.py; TFI_tables_figures.py; environment.yml; 2017_law.json; OUTPUT_BASELINE; OUTPUT_REFORM

**Terms:** CC0-1.0 dedication; LICENSE.md inspected. Tax-Calculator itself also CC0.

**Environment and compute:** Historical Python 3.6 environment, taxcalc>=0.19.0 in a loose Conda environment.yml, historical OG-USA local package. Exact resolved historical dependency versions not preserved by this file. README estimates about 10 hours with 10+ processors or 100+ hours serial for full 12-case analysis.

**Inputs:** Original IRS PUF for fresh tax-function estimation; precomputed fitted-function pickle files provided as a partial open route. CPS data can replace PUF but changes the experiment.

**Data access:** IRS PUF not published; existing estimated functions are available. Never upload PUF/restricted tax records.

### Construct and compare tax-calculator

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` git clone https://github.com/rickecon/TaxFuncIntegr.git ``
2. `` cd TaxFuncIntegr ``
3. `` git checkout 715cc76e3305c00dd64d79521c504bb388c6d87d ``
4. `` # Historical environment must be reconstructed; README contains a pyton typo and outdated Python/ folder path. Inspect files before use. ``
5. `` # Proposed: set run_micro=False to reuse published fitted functions; do not claim this reruns the microsimulation stage ``
6. `` python run_TaxFuncInt.py ``
7. `` python TFI_tables_figures.py ``

**Expected outputs:** Baseline/reform fitted tax functions, SS/TPI outputs, publication tables and figures from the plotting script.

**Comparison with the paper:** Numerical +0.069545535% matches May-2018 draft +0.07% at declared tolerance; six baseline outputs match archived author SS. Scope is fresh macro solve using supplied fitted inputs. Negative G in both cases is retained as failed economic feasibility, so neither this match nor small Euler residuals establish a valid policy prediction.

**Execution result:** Fresh baseline and counterfactual macro steady states solved; author-manuscript SS GDP rounding target matches. Economic-feasibility diagnostic fails because both closures require negative government spending. Tax-Calculator imported but its microsimulation/PUF estimation NOT executed.

**Execution evidence:** [Author-code attempt](../reproductions/tax-calculator.md); [Run record](../reproductions/records/tax-calculator.json)

**Blockers:** Original restricted IRS PUF not available for fresh Tax-Calculator micro-estimation.; Government spending is negative in both solved macro steady states.; Final 2019 journal table identity not checked; selected comparison is the May 2018 author manuscript.; Full tax-function fitting and transition paths not rerun.

**Next action:** Resolve fiscal closure feasibility and verify final journal table/version; use lawful PUF access only if fresh microsimulation estimation is required.

**Gaps:** Original restricted IRS PUF not available for fresh Tax-Calculator micro-estimation.; Government spending is negative in both solved macro steady states.; Final 2019 journal table identity not checked; selected comparison is the May 2018 author manuscript.; Full tax-function fitting and transition paths not rerun.

### Sources for tax-calculator

- [Author-paper association, commands, run_micro=False route, CPS alternative, PUF restriction and runtime estimate.](https://github.com/rickecon/TaxFuncIntegr/blob/715cc76e3305c00dd64d79521c504bb388c6d87d/README.md) (inspected 2026-11-15).
- [Paper table/figure generation from baseline/reform outputs.](https://github.com/rickecon/TaxFuncIntegr/blob/715cc76e3305c00dd64d79521c504bb388c6d87d/TFI_tables_figures.py) (inspected 2026-11-15).
- [Verified published paper title/authors/year.](https://api.crossref.org/works/10.1177/1091142118816744) (inspected 2026-11-15).

## openfisca-core

**OpenFisca** — How does a targeted cash benefit create a work-incentive cliff compared with a child allowance?

**Route:** Unresolved. **Execution:** Not run. **Source confidence:** low.

### Paper for openfisca-core

Max Ghenis (2022). [How does targeted cash assistance affect incentives to work?](https://www.thecgo.org/research/how-does-targeted-cash-assistance-affect-incentives-to-work/). CGO Research in Focus, 2022-06-17 (research report; no DOI found).

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://www.thecgo.org/research/how-does-targeted-cash-assistance-affect-incentives-to-work/). Metadata verification: confirmed. Full-text access: Open full report and publisher byline/date inspected. This is a published policy research report, not a journal article.

**Target in the paper:** Cambridge-family net-income cliff and Massachusetts poverty simulations. Report states statewide overall poverty reduction 15%, child poverty 42%; these are model predictions, not empirical intervention effects.

### Code and inputs for openfisca-core

[Artifact or upstream source](https://github.com/TheCGO/cambridge-cash-assistance). Exact author notebook linked in the report, but repository currently returns 404. No immutable snapshot recovered. The report links historical OpenFisca-US; modern PolicyEngine is not assumed interchangeable.

**Source inspected:** no. **Ref:** Not established.. **Commit:** Not established..

**Files:** analysis.ipynb (named by report; unavailable for inspection)

**Terms:** Unavailable; do not assume source/data redistribution terms.

**Environment and compute:** Unresolved historical OpenFisca-US/Core environment until the notebook and dependency pin are recovered. Current OpenFisca core alone cannot recreate a historical country model or policy report. Likely CPU microsimulation; size unknown until data recovered.

**Inputs:** Original report notebook, household specification, 2022 law snapshot, survey microdata/weights and benefit assumptions; all still need recovery and terms inspection.

**Data access:** Report public; original notebook/data currently unavailable. Generic OpenFisca country-template is a separate tutorial and does not supply this research artifact.

### Construct and compare openfisca-core

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Recovery steps only; no working execution command is established ``
2. `` # Retrieve analysis.ipynb from the author or an authenticated archive; verify it matches the report ``
3. `` # Reconstruct the historical OpenFisca-US and Core versions, law period, data and weights ``
4. `` # Only then execute the recovered notebook in an isolated environment and compare the reported targets. ``

**Expected outputs:** Expected construction outputs: disposable-income-versus-earnings curve, poverty changes and budget-neutral child-allowance comparison. Filenames unknown until code recovered.

**Comparison with the paper:** After recovery, compare the specific report family’s benefit cliff and the stated poverty percentage changes using its original weights and definitions. Predeclare rounding tolerance; do not use current laws/country packages as a replacement and call it reproduction.

**Execution result:** Source inspection only; no new execution for this route.

**Execution evidence:** None recorded.

**Blockers:** Exact reproduction repo returns HTTP 404.; Historical model versions, input data rights and weighting not recovered.

**Next action:** Request the author notebook/archive and shareable input specification, or select an alternative paper with a surviving archive before constructing a public walkthrough.

**Gaps:** This tool does not yet have an accessible inspected research-code route from this candidate.

### Sources for openfisca-core

- [Report metadata, OpenFisca-US use, prediction targets and linked reproduction notebook.](https://www.thecgo.org/research/how-does-targeted-cash-assistance-affect-incentives-to-work/) (inspected 2026-11-15).
- [Live repository lookup returned 404 on 2026-11-15.](https://github.com/TheCGO/cambridge-cash-assistance) (inspected 2026-11-15).

## dynare

**Dynare** — Can a published Bayesian DSGE model’s shock responses and posterior estimates be regenerated?

**Route:** Paper result candidate. **Execution:** Example executed. **Source confidence:** high.

### Paper for dynare

Frank Smets; Rafael Wouters (2007). [Shocks and Frictions in US Business Cycles: A Bayesian DSGE Approach](https://www.aeaweb.org/articles?id=10.1257/aer.97.3.586). 10.1257/aer.97.3.586.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1257/aer.97.3.586). Metadata verification: confirmed. Full-text access: Official AEA article record and replication-package landing page inspected; code inspection uses a maintained third-party implementation.

**Target in the paper:** Paper’s Bayesian estimation, shock decomposition and impulse responses; specific printed table cells/figure tolerances still require full-text comparison. Official replication archive DOI 10.3886/E116269V1.

### Code and inputs for dynare

[Artifact or upstream source](https://github.com/JohannesPfeifer/DSGE_mod). Maintained replication by Johannes Pfeifer with explicit Smets/Wouters attribution and corrections. Prefer the AEA-linked original archive as reference and document differences.

**Source inspected:** yes. **Ref:** master. **Commit:** 26c21f79e4c6a6b19b18e6330edc5b23489907a4.

**Files:** Smets_Wouters_2007/Smets_Wouters_2007.mod; Smets_Wouters_2007/Smets_Wouters_2007_45.mod; Smets_Wouters_2007/usmodel_data.mat; Smets_Wouters_2007/usmodel_mode.mat

**Terms:** GPL-3.0-or-later for this Dynare implementation per header; original data/archive terms separate.

**Environment and compute:** Dynare with GNU Octave for open runtime; choose supported Dynare release and inspect the model’s version notes. Host has no Octave/Dynare identified; no system installation authorized. Inspected default model uses mh_replic=0, mode_compute=0 and the supplied usmodel_mode, then shock_decomposition y; it does not run a full MCMC chain by default. CPU; deterministic mode/IRF check smaller than full Bayesian MCMC estimation.

**Inputs:** Bundled seven-series usmodel_data.mat and posterior-mode starting file; original sample, transformations, priors, estimation options and seed must match selected target.

**Data access:** Original AEA-linked replication package available through OpenICPSR; bundled data exist in third-party repository. Check archive download/access terms.

### Construct and compare dynare

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` git clone https://github.com/JohannesPfeifer/DSGE_mod.git ``
2. `` cd DSGE_mod ``
3. `` git checkout 26c21f79e4c6a6b19b18e6330edc5b23489907a4 ``
4. `` cd Smets_Wouters_2007 ``
5. `` # Proposed Octave command after installing an isolated compatible Dynare runtime ``
6. `` octave --no-gui --eval "dynare Smets_Wouters_2007.mod" ``

**Expected outputs:** Dynare model/results files, evaluation at supplied posterior mode and shock decomposition for y under default settings. Full posterior/MCMC diagnostics require explicitly changing mh_replic and estimation options; default nograph/nodiagnostic suppress these outputs.

**Comparison with the paper:** Exploratory decomposition sum residual is 7.1e-15; Laplace density -1844.0985587 under provided mode/settings. Original published numerical target/sample/mode not matched, and runtime/model warnings remain.

**Execution result:** Fresh maintained model evaluation and finite 40×9×230 shock decomposition completed. No original-paper quantitative comparison or posterior estimation claimed.

**Execution evidence:** [Author-code attempt](../reproductions/dynare.md); [Run record](../reproductions/records/dynare.json)

**Blockers:** Old mode file cannot be verified against current model.; gaminv prior-bound calculation did not converge for some values.; Negative array dimensions converted to zero in shock-decomposition setup.; 33 preprocessor warnings from unassigned steady-state block variables.; Official original replication archive requires account to download.; Maintained model uses supplied old mode and 230 observations; correspondence to selected paper target unverified.

**Next action:** Match original archive/sample/mode and resolve prior-bound/mode compatibility warnings, then define a named paper comparison before full posterior estimation.

**Gaps:** Old mode file cannot be verified against current model.; gaminv prior-bound calculation did not converge for some values.; Negative array dimensions converted to zero in shock-decomposition setup.; 33 preprocessor warnings from unassigned steady-state block variables.; Official original replication archive requires account to download.; Maintained model uses supplied old mode and 230 observations; correspondence to selected paper target unverified.

### Sources for dynare

- [Official article metadata and original replication-package link.](https://www.aeaweb.org/articles?id=10.1257/aer.97.3.586) (inspected 2026-11-15).
- [Original replication archive landing page and persistent DOI.](https://www.openicpsr.org/openicpsr/project/116269/version/V1/view) (inspected 2026-11-15).
- [Maintained implementation, attribution, version notes and bundled inputs.](https://github.com/JohannesPfeifer/DSGE_mod/blob/26c21f79e4c6a6b19b18e6330edc5b23489907a4/Smets_Wouters_2007/Smets_Wouters_2007.mod) (inspected 2026-11-15).
- [Verified title/authors/year.](https://api.crossref.org/works/10.1257/aer.97.3.586) (inspected 2026-11-15).
