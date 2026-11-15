# Run the CPU examples

These small examples produce inspectable files without downloading research datasets or using paid APIs. They were run with Python 3.12 on Linux. Other platforms need their own check. Run commands from the root of an OSRI checkout.

## Setup

Create an environment outside the checkout. The example below uses a sibling directory; choose another location if needed. On Windows, use its `Scripts/python.exe` instead of `bin/python`.

```sh
python3 -m venv ../osri-sim-env
../osri-sim-env/bin/python -m pip install -r simulation-lab/examples/requirements.txt
```

[requirements.txt](requirements.txt) pins the four direct packages. [requirements-tested.txt](requirements-tested.txt) records the complete dependency set used for the Linux check; it is not a cross-platform lockfile. If Python cannot create an environment, use an existing Python or Conda environment that supports the pinned packages. No global solver installation is required.

Every command requires a new output directory and refuses to overwrite an existing run. `run.json` records versions, parameters, results, checks, and hashes. The scripts disable PyBaMM's optional telemetry for this exercise.

## Battery discharge

**Source:** [Sulzer et al. (2021)](https://doi.org/10.5334/jors.309), Listing 1 in the open article. It solves the Doyle–Fuller–Newman battery model over a one-hour discharge. Read the model and pipeline discussion before running.

```sh
../osri-sim-env/bin/python simulation-lab/examples/battery_discharge.py --output ../sim-runs/battery
```

The [script](battery_discharge.py) makes the parameter set (`Marquis2019`), 1C current, solver, and tolerances explicit, then writes `voltage.csv` and `parameters.json`. This is an adaptation to PyBaMM 26.10.1.1; it does not recreate the paper's historical environment. A voltage cutoff can end a changed case before 3,600 seconds.

Inspect time in seconds and terminal voltage in volts. The recorded checks cover finite values, increasing time, the requested horizon, and positive voltage. They do not test mesh convergence or agreement with a measured cell. A useful next experiment compares two discharge rates while holding the cell parameter set fixed; record cutoff time as well as voltage.

## Option pricing

**Source:** [Black and Scholes (1973)](https://doi.org/10.1086/260062), p. 640 and Eq. 13, p. 644. Those passages were checked in the supplied library PDF. The example uses a European call, constant interest and volatility, no dividends, and the paper's idealized trading assumptions.

```sh
../osri-sim-env/bin/python simulation-lab/examples/option_monte_carlo.py --output ../sim-runs/options --seed 42 --paths 50000
```

The [script](option_monte_carlo.py) uses synthetic spot and strike values of 100, a one-year maturity, a 5% annual interest rate, and volatility of 0.2 per square-root year. These inputs are chosen for this exercise. They are not observations from the article. QuantLib generates the terminal stock price under the risk-neutral process; discounting the terminal payoff estimates the call value. One exact geometric-Brownian transition is enough for this terminal-only payoff.

Compare the estimate and its standard error with QuantLib's analytical price and a separately coded Eq. 13 expression. `payoffs.csv` contains the simulated sample; `run.json` reports the estimate, 95% interval, and checks. The five-standard-error check is a broad stochastic regression check; it is not a guarantee for every seed. Monte Carlo is the lab's numerical illustration, not a method claimed to appear in the 1973 paper. This example evaluates the mathematical model, not a trading strategy or forecast.

## Household saving

**Source:** [Carroll (1997)](https://doi.org/10.1162/003355397555109), Sections II–III, and the baseline in the [Econ-ARK reproduction source](https://github.com/econ-ark/BufferStock-LifeCycle/blob/0a278360b77eeac1df1e91374c168b3091365fbf/Code/Python/BufferStock-LifeCycle.py). The original model and parameter discussion were checked in the supplied PDF.

```sh
../osri-sim-env/bin/python simulation-lab/examples/household_saving.py --output ../sim-runs/households --seed 42
```

The [script](household_saving.py) ports the reproduction code's infinite-horizon baseline into HARK 0.17.2: CRRA 2, discount factor 0.96, gross interest factor 1, permanent-income growth 1.02, zero-income probability 0.005, and no artificial borrowing constraint. It solves the consumption policy and simulates 1,000 households for 120 periods. Values are normalized by permanent income; they are not currency amounts or empirical households.

`households.csv` reports period means. Checks cover finite histories, positive consumption, nonnegative assets, and the budget identity. They do not show convergence of the distribution or agreement with the article's tables. The paper's prose and the later reproduction code differ in how some parameters are expressed; see the [source comparison and full reproduction route](economics.md).

## Results in OpenUSD

Run the battery example first:

```sh
../osri-sim-env/bin/python simulation-lab/examples/results_to_usd.py --input ../sim-runs/battery --output ../sim-runs/usd
```

The [adapter](results_to_usd.py) writes `battery.usda`, a readable OpenUSD stage, and packages the source CSV, parameters, and run record with relative paths. Its data prim contains time-sampled voltage, units, and a source hash. It verifies the CSV against the run record and checks every authored sample after reopening the stage.

This is an original OSRI exchange example using the [OpenUSD attribute API](https://openusd.org/release/api/class_usd_attribute.html). The custom `research:` attributes are not a standard electrochemical schema. No battery geometry, material model, or solver is created in USD. Copy the entire output directory when sharing the stage; a USD viewer alone may not display custom numeric attributes as a plot.

See [verification](../verification.md) for observed outputs and the scope of each check.
