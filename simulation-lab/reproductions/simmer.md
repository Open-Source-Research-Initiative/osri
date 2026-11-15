# Reproduce simmer's published M/M/1 example

The question is whether the single-server queue in Ucar, Smeets and Azcorra (2019), [simmer: Discrete-Event Simulation for R](https://doi.org/10.18637/jss.v090.i02), produces the printed result in Section 4.2 and agrees with the queueing-theory baseline in Section 4.1. The publisher supplies the actual [R replication script](https://www.jstatsoft.org/article/download/v090i02/3818) and [simmer 4.3.0 source package](https://www.jstatsoft.org/index.php/jss/article/view/v090i02/3817).

## Model and comparison fixed before execution

The model has exponential arrivals at rate 2, exponential service at rate 4, one server, and an infinite queue. Section 4.1 runs for 2,000 simulation-time units. Section 4.2 uses 100 replications, each running for 500 units, with `set.seed(1234)` and `mclapply(..., mc.set.seed = FALSE)`. Two forked workers are made explicit to reproduce R's default in the supplied example. Time has abstract simulation units.

The published p. 20 mean is **0.4974943**, with 95% interval **[0.4868269, 0.5081617]**. The comparison tolerance is **5 × 10^-8**, half a unit in the last printed decimal, declared before running. This tests the printed output rather than a new scientific tolerance. The statistic is mean completed-arrival time in the system (`end_time - start_time`); the surrounding article text calls it average population, but the executable expression and its units are time.

A separate validation uses 100 distinct seeds, 10001–10100, under the same model and 500-unit horizon. The predeclared rule requires the exact M/M/1 values, mean system time **1/(4−2) = 0.5** and mean population **(2/4)/(1−2/4) = 1**, to lie within their respective 97.5% Student-t intervals. The two intervals provide a Bonferroni simultaneous confidence level of at least 95%. This extension changes seed handling and is labeled separately from the literal paper run. Empty initial conditions and completion censoring remain finite-horizon limitations.

The deterministic Section 5.2 example adds arrivals at times 1–1000, each with delay 1. It must produce exactly 1,000 completed records, departures 2–1001, and activity time 1, with zero tolerance for these exactly representable integer values.

## Repeat the run

Files needed: `prepare_sources.py`, `run_mm1.R`, `plot_results.R`, `Makevars`, and the recorded environment files. `prepare_sources.py` retrieves author code and checks SHA256; it refuses altered source bytes. The author supplement is downloaded during setup, not copied into the Lab's source.

Use Linux with a C++ compiler. Create a project environment, keeping its caches and working files on the selected workspace. The observed runtime was R **4.5.3**, simmer **4.3.0**, Rcpp **1.1.2**, BH **1.69.0.1**, magrittr **2.0.5**, and jsonlite **2.0.0**. The article's performance section reports R 3.3.3; this is a newer R runtime with the publisher's original simmer source. `conda-linux-64-explicit.txt` records the portable runtime packages. Its conda metadata still lists the initially installed newer BH package; the required final source-install step below replaces its files with BH 1.69.0-1. `R-packages.csv` records the actual package versions used.

```sh
python3 prepare_sources.py
micromamba create -y -p ./env -c conda-forge \
  r-base=4.5.3 r-rcpp=1.1.2 r-magrittr=2.0.5 r-jsonlite=2.0.0 r-codetools
# Set project-local TMPDIR and cache paths before these commands.
./env/bin/R CMD INSTALL sources/BH_1.69.0-1.tar.gz
R_MAKEVARS_USER="$PWD/Makevars" ./env/bin/R CMD INSTALL sources/simmer-publisher.tar.gz
./env/bin/Rscript --vanilla run_mm1.R .
./env/bin/Rscript --vanilla plot_results.R .
```

The tested `Makevars` selects `/usr/bin/g++`; adjust that compiler path for the local machine and record any changes. There are no patient data or external datasets. The article's unrelated Python/Julia timing benchmarks and its plotting dependencies are not executed. The queue model expressions, random-number calls, seed and horizons are preserved; plots are rendered separately from native monitors using base R.

## Observed comparison

| Check | Observed result | Reference / rule | Outcome |
| --- | --- | --- | --- |
| Paper Section 4.2 mean | 0.49749431258942678 | 0.4974943, absolute error ≤5e-8 | Pass: error 1.259e-8 |
| Paper Section 4.2 interval lower end | 0.48682693460382809 | 0.4868269, absolute error ≤5e-8 | Pass: error 3.460e-8 |
| Paper Section 4.2 interval upper end | 0.50816169057502547 | 0.5081617, absolute error ≤5e-8 | Pass: error 9.425e-9 |
| Independent-seed mean time | 0.49806184986850421; 97.5% interval [0.48818870937393966, 0.50793499036306877] | Contains 0.5 | Pass |
| Independent-seed mean population | 0.99769534465266396; 97.5% interval [0.97465534840801427, 1.0207353408973137] | Contains 1 | Pass |
| Section 5.2 deterministic arrivals | 1,000 correct starts, ends, activity times and completion flags | Exact integer equality | Pass |

The numerical run took about 1.26 seconds after environment setup on this host. Full arrival and resource monitors, per-replication CSVs, deterministic outputs, extracted executed blocks, session information, a machine-readable receipt, and a plot in PNG/SVG are retained.

## What the match does and does not establish

The printed Section 4.2 output was matched to its displayed precision using the publisher's code. **The literal 100-replication run contains only 50 distinct replication means**: with two forked workers and `mc.set.seed = FALSE`, corresponding workers inherit the same RNG state. A separate exploratory two-worker check confirmed that the complete arrival-monitor dataframes, not only the means, are exactly identical. Its printed interval should therefore not be treated as an independently validated uncertainty interval over 100 independent runs. The separate independent-seed experiment addresses that issue under its stated finite horizon. No seed or sample-size adjustment was made after viewing numerical results.

The first source build failed because modern BH 1.90 no longer supplied macros expected by the 2019 source. Pinning publication-era BH 1.69.0-1 fixed the build without changing simmer code. The first conda solve also failed because `r-simmer` is absent from the channel. Both failures remain in the evidence directory. Agent technical review and successful numerical comparison are separate from human scientific review, which remains pending.

The package is GPL >=2; the publisher/CRAN sources retain their own terms. Newly generated numeric outputs and Lab documentation may be shared under the hub's original-content terms. The source-retrieval harness verifies upstream bytes before execution.

## Download the recorded files

- [author-arrivals.csv](files/simmer/outputs/author-arrivals.csv) — numeric output.
- [author-replications.csv](files/simmer/outputs/author-replications.csv) — numeric output.
- [author-resource-monitor.csv](files/simmer/outputs/author-resource-monitor.csv) — numeric output.
- [author-t-test.txt](files/simmer/outputs/author-t-test.txt) — session or test output.
- [deterministic-arrivals.csv](files/simmer/outputs/deterministic-arrivals.csv) — numeric output.
- [independent-replications.csv](files/simmer/outputs/independent-replications.csv) — numeric output.
- [mm1-paper-comparison.png](files/simmer/outputs/mm1-paper-comparison.png) — plot.
- [mm1-paper-comparison.svg](files/simmer/outputs/mm1-paper-comparison.svg) — plot.
- [results.json](files/simmer/outputs/results.json) — numeric output.
- [sessionInfo.txt](files/simmer/outputs/sessionInfo.txt) — session or test output.
- [duplicate-stream-check.json](files/simmer/outputs/duplicate-stream-check.json) — exploratory source-diagnostic output.
- [prepare_sources.py](files/simmer/prepare_sources.py) — portable driver or environment/source record.
- [run_mm1.R](files/simmer/run_mm1.R) — portable driver or environment/source record.
- [plot_results.R](files/simmer/plot_results.R) — portable driver or environment/source record.
- [check_fork_streams.R](files/simmer/check_fork_streams.R) — portable driver or environment/source record.
- [Makevars](files/simmer/Makevars) — portable driver or environment/source record.
- [R-packages.csv](files/simmer/R-packages.csv) — portable driver or environment/source record.
- [conda-linux-64-explicit.txt](files/simmer/conda-linux-64-explicit.txt) — portable driver or environment/source record.
- [targets.json](files/simmer/targets.json) — portable driver or environment/source record.

[Complete run record](records/simmer.json) · [All candidate attempts](README.md). Human scientific review is pending.
