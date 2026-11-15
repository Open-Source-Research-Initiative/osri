# Market microstructure with ABIDES

**Question:** How does an execution agent change prices and order-book conditions in a simulated market?

[Byrd et al. (2020)](https://doi.org/10.1145/3384441.3395986) introduce ABIDES, an agent-based discrete-event market simulator. The [original repository](https://github.com/abides-sim/abides) and its [RMSC03 experiment guide](https://github.com/abides-sim/abides/wiki/RMSC03) provide a concrete starting case. RMSC03 is an upstream experiment using the framework; this walkthrough does not identify it as a reproduction of a particular paper figure.

## Prepare the historical environment

The inspected snapshot is `c4bf157678928934417aba6073eb0651aeaf6d15`:

```sh
git clone https://github.com/abides-sim/abides.git
cd abides
git checkout c4bf157678928934417aba6073eb0651aeaf6d15
```

Inspect the snapshot's requirements before creating a separate environment. Its old NumPy, pandas, and SciPy versions should not be mixed into the lab's modern CPU environment. A working historical Python environment has not been established here. The distinct JPMorgan repository `abides-jpmc-public` was archived when checked; it is not interchangeable with this original codebase.

## Follow the published code example

Once the upstream dependencies are working, the RMSC03 guide's baseline command is:

```sh
python -u abides.py -c rmsc03 -t ABM -d 20200603 -s 1234 -l rmsc03_two_hour
```

`ABM` is the simulated instrument. The date labels the simulation; this command does not load that day's real market. Inspect the configuration's agents, latency assumptions, and session times. The guide documents exchange and order-book logs including `log/rmsc03_two_hour/EXCHANGE_AGENT.bz2` and `ORDERBOOK_ABM_FULL.bz2`.

The guide also adds an execution agent using `-e` and a participation rate such as `-p 0.1`. Use a new log directory for each case. For a comparison, pair the baseline and execution cases on the same seed, then repeat the pair over several independent seeds. Measure a specified price-impact or execution-cost statistic and retain the raw logs and analysis code. A single stochastic path is not an estimated population effect.

For a smaller mathematical finance exercise that already runs in the lab, use [Black–Scholes and QuantLib](cpu-walkthroughs.md#option-pricing). That example prices a model payoff; ABIDES models market interactions.

**Status:** DOI metadata, original source, historical dependencies, and upstream experiment commands inspected on 2026-11-15. Article methods have not received a full-text audit; this historical environment and experiment were not run.
