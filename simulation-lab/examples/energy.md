# European energy networks with PyPSA-Eur

**Question:** How do transmission, generation, and storage choices change a modeled electricity system?

[Hörsch et al. (2018)](https://doi.org/10.1016/j.esr.2018.08.012) describe PyPSA-Eur's open European transmission model. The [current tutorial](https://pypsa-eur.readthedocs.io/en/latest/tutorial/) supplies a smaller executable learning case. Current software, input data, and scenarios have changed since 2018; this route introduces the model family and does not reproduce that article's numerical results.

## Run the smaller electricity case

The inspected snapshot is `07284029a715ecf5c64f6b83b1f900df497319fc`. Follow the [installation guide](https://pypsa-eur.readthedocs.io/en/latest/installation/) to provide Pixi and the platform dependencies, then:

```sh
git clone https://github.com/PyPSA/pypsa-eur.git
cd pypsa-eur
git checkout 07284029a715ecf5c64f6b83b1f900df497319fc
pixi shell
snakemake --cores 2 -n results/test-elec/networks/solved_2050.nc --configfile config/test/config.electricity.yaml
```

The dry run lists the planned work. After reviewing downloads and resource requirements, remove `-n` to execute. The checked [configuration](https://github.com/PyPSA/pypsa-eur/blob/07284029a715ecf5c64f6b83b1f900df497319fc/config/test/config.electricity.yaml) selects Belgium, a short March 2013 weather window, five clusters, daily averaging, and the open HiGHS solver. The output's `2050` label is a scenario year, not the weather-data year. This deliberately coarse tutorial should not be interpreted as a national planning result.

Other workflows and clustering steps can need different solvers; consult the upstream compatibility notes. Commercial solver packages in an environment do not confer commercial licenses. Input datasets and weather services also have terms independent of the software license.

## Inspect the resulting network

Preserve `solved_2050.nc`, the configuration, logs, workflow revision, environment lock, and the input-data provenance. Inspect capacities, dispatch, energy balances, objective value, constraint residuals, and solver termination. The tutorial contains an expected-objective check; passing it is a regression check for that configuration, not validation of a future energy system.

For a follow-on experiment, vary a single constraint such as the emissions budget and compare cost and capacity while holding weather, time aggregation, and network clustering fixed. For reproduction of the 2018 article, locate its historical code and data versions first.

**Status:** DOI metadata, current tutorial, and pinned electricity configuration inspected on 2026-11-15. Full paper methods, workflow downloads, and optimization were not executed or fully audited here.
