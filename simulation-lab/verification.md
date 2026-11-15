# Simulation Lab verification record

Checks performed by **Codex on 2026-11-15**, under Cole's direction. This is a technical record, not independent human scientific review. Human review and acceptance remain pending.

## Executed CPU examples

The four included examples ran in an isolated Python 3.12.16 environment on Linux x86-64. Direct versions were PyBaMM 26.10.1.1, QuantLib 1.44, Econ-ARK/HARK 0.17.2, and usd-core 26.11. The [complete tested dependency set](examples/requirements-tested.txt) and [machine-readable run records](verification/example-runs.json) preserve versions, parameters, checks, and file/source hashes.

| Example | Observed output | Checks passed |
| --- | --- | --- |
| Battery discharge | 121 samples; 3,600 s; initial 3.7717806 V and final 3.1716841 V; termination at final time | Finite positive voltage, increasing time, within requested horizon |
| European call | Analytical price 10.45058357; independent formula 10.45058357; Monte Carlo 10.45453708 with standard error 0.06579664 | Formula agreement, finite nonnegative payoffs, nonzero variance, estimate within five standard errors |
| Household saving | At period 120, mean resources 1.33295862, consumption 0.99375371, assets 0.33920491, all normalized by permanent income | Finite histories, positive consumption, nonnegative assets, budget identity |
| Battery results in USD | 121 time samples; every stored voltage equals the source CSV value | Sample times and values preserved, seconds retained, packaged CSV hash matches |

The option run used 50,000 paths and seed 42. Its approximate 95% interval was [10.32557566, 10.58349849]. The household run used 1,000 agents, 120 periods, and seed 42 with the baseline described in the [Carroll comparison](examples/economics.md). Values above describe these runs only.

All 16 recorded example checks passed. The run records' Python-source hashes were compared against the submitted scripts. Raw outputs were retained in the development run directory; they can be regenerated using the [CPU walkthrough](examples/cpu-walkthroughs.md). Bit-for-bit numerical identity on other hardware or dependency sets has not been established.

## Input and preservation checks

The [rejection-check record](verification/input-checks.json) confirms four observed behaviors:

- Changing the input voltage CSV made the USD adapter reject it before creating an output directory.
- Changing the parameter JSON also caused rejection before output creation.
- Reusing a battery output directory failed and preserved the existing run record.
- A zero QuantLib seed was rejected; that value does not select a fixed seed for this generator.

These checks test the examples' behavior. QuantLib's [generator implementation](https://github.com/lballabio/QuantLib/blob/master/ql/math/randomnumbers/mt19937uniformrng.cpp) documents the zero-seed behavior. The hash comparison checks consistency with a run record; it does not authenticate the scientific origin of an arbitrary record.

## Literature and upstream routes

The bibliography contains 36 DOI records checked against Crossref. The [reading-status field](papers.csv) distinguishes metadata checks from inspected full-text passages. Black–Scholes assumptions and Eq. 13 and Carroll's model/calibration passages were read in the supplied PDFs. The original articles are not redistributed.

Seven other example routes have inspected upstream instructions but were not executed: Isaac Lab, ABIDES, the historical Carroll reproduction, preCICE FSI3, PyPSA-Eur, service queues, and LuST. ViNoS remains an artifact-access lead. No GPU training, historical container, full traffic model, energy workflow, or coupled CFD run is claimed here.

The catalog's source checks do not establish installation success for all 60 tools. Nor do the local checks establish mesh or time-step convergence, distributional convergence, empirical accuracy, real-world robot performance, or reproduction of an article's figures and tables.

## Catalog and website

`python3 simulation-lab/catalog.py` validates IDs, references, dates, local guide files, and the generated catalog/bibliography/BibTeX. The website consumes the same CSV records and runs that validator during its build. Website validation is recorded separately from simulation execution.

The site build and checker passed for 83 pages and 2,752 local links, CSS assets, and translation notices. Chromium checks covered case-insensitive search, domain filtering, combined filters, empty results, reset, keyboard-operated details, CSV downloads, and content availability without JavaScript. Viewports from 320 to 1,440 pixels had no page-level horizontal overflow. Desktop and mobile screenshots were inspected. See the [browser-check record](verification/browser-check.json).

Documentation-link probes found two obsolete paths, which were replaced with the official QuantEcon and EnergyPlus documentation. After correction, 55 documentation endpoints returned HTTP 200; two GitHub documentation routes were inspected through the repository connector. Blender, MOOSE, and Elmer documentation hosts returned HTTP 403 to the automated probe. Their official links are retained; the access denial is not a finding that the documentation is missing.
