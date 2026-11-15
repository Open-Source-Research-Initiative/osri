# Household saving from Carroll (1997)

**Question:** How does a household's saving response depend on income uncertainty and expected income growth?

[Carroll (1997)](https://doi.org/10.1162/003355397555109) develops a buffer-stock model with permanent and transitory income shocks. Sections II–III define the model and its infinite-horizon behavior; Section IV adds life-cycle income profiles. The [Econ-ARK material record](https://econ-ark.org/materials/bufferstock-lifecycle/) identifies an author-associated reproduction with code for figures and tables.

## Start with the local baseline

The [CPU walkthrough](cpu-walkthroughs.md#household-saving) runs a port of the reproduction's baseline. It keeps the reproduction's calibration while changing the HARK version and adding a short simulation and file exports. It has not reproduced a particular figure or table.

| Quantity | Original paper | Reproduction code used for the local port |
| --- | --- | --- |
| Preference curvature | CRRA 2, printed p. 8 | `CRRA=2` |
| Time preference | 4% annual discount rate, p. 7 | `DiscFac=0.96`; retained as coded rather than silently replacing it with `1/1.04` |
| Risk-free return | Zero baseline net rate, p. 7 | `Rfree=1` |
| Permanent-income growth | 2% annually, p. 7 | `PermGroFac=[1.02]` |
| Zero-income event | Probability 0.5% annually, p. 6 | `UnempPrb=0.005`, `IncUnemp=0` |
| Shock dispersion | The prose on p. 7 says “0.1 percent per year” | The reproduction uses log standard deviations `0.1`; the port follows the code. This discrepancy remains explicit. |
| Borrowing | No imposed liquidity constraint; discussion on p. 8 | `BoroCnstArt=None`; zero-income risk induces the natural limit |

The supplied PDF's printed pp. 5–8 and the reproduction's baseline block were reviewed on 2026-11-15. The restricted PDF is not redistributed. The local run does not reproduce the paper's truncated shock distribution, life-cycle calibration, or all historical numerical settings.

## Use the paper reproduction

The inspected snapshot is `0a278360b77eeac1df1e91374c168b3091365fbf`:

```sh
git clone https://github.com/econ-ark/BufferStock-LifeCycle.git
cd BufferStock-LifeCycle
git checkout 0a278360b77eeac1df1e91374c168b3091365fbf
```

Read its [environment instructions](https://github.com/econ-ark/BufferStock-LifeCycle/blob/0a278360b77eeac1df1e91374c168b3091365fbf/README.md). They document `nbreproduce` with `econark/econ-ark-notebook:0.10.4`; this historical container has not been pulled or tested here. The README has an older script name. The checked [reproduce.sh](https://github.com/econ-ark/BufferStock-LifeCycle/blob/0a278360b77eeac1df1e91374c168b3091365fbf/reproduce.sh) actually executes `Code/Python/BufferStock-LifeCycle.py` with IPython.

After preparing that environment, run `bash reproduce.sh`. Preserve the generated figures, tables, source revision, environment, and any errors. Compare a named result with the original paper before describing it as reproduced. For a new study, vary one assumption at a time and distinguish individual policy functions, population distributions, and general-equilibrium claims.

**Status:** Original model passages and upstream code inspected; local baseline port executed; historical full reproduction not executed.
