# Published urban traffic scenarios with SUMO

**Question:** How do route assignment and traffic-signal choices change travel through a city model?

[Codeca et al. (2017)](https://doi.org/10.1109/MITS.2017.2666585) evaluate Luxembourg's LuST traffic-demand scenario. The [authors' repository](https://github.com/lcodeca/LuSTScenario) contains configurations for user assignment/equilibrium and static/actuated signals. These supplied cases give a concrete route from the publication to executable model inputs.

## Preserve the simulator version

The repository explicitly states that **SUMO 0.26** is the version used for validation. Running it with a newer SUMO does not transfer that validation. The README recommends the separate MoST scenario for a newer supported route. Choose historical reproduction or a documented port before installing dependencies.

The inspected snapshot is `5edb7ecb9ad196c39172b6eb95d19ed789f4b1a6`:

```sh
git clone https://github.com/lcodeca/LuSTScenario.git
cd LuSTScenario
git checkout 5edb7ecb9ad196c39172b6eb95d19ed789f4b1a6
cd scenario
sumo -c dua.static.sumocfg
```

Run that command only after preparing the chosen SUMO environment. The other documented configurations are `dua.actuated.sumocfg`, `due.static.sumocfg`, and `due.actuated.sumocfg`. Use a separate working copy or distinct output paths for each case, because configurations may reuse output filenames. Inspect the network, demand, and configuration XML before running.

## Compare results

Choose a specific article result, then match its demand, route-assignment procedure, signal control, seed, and aggregation interval. Preserve trip and network outputs and compare travel times, queues, and flows using the same definitions. If the simulator or scenario has been ported, record the change and establish a new baseline before attributing differences to the policy choice.

**Status:** DOI metadata, author README, scenario directory, and version restriction inspected on 2026-11-15. Article validation data and historical simulation were not fully reviewed or run here.
