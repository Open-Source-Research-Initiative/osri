# Literature examples

Start with a paper and a specific model, equation, listing, or benchmark. The table distinguishes local teaching runs from upstream reproduction routes. The [bibliography](../bibliography.md) supplies complete citations.

| Example | Literature connection | Available now |
| --- | --- | --- |
| [Battery discharge](cpu-walkthroughs.md#battery-discharge) | Sulzer et al. (2021), Listing 1 | Executed adaptation; Python, CSV, parameter JSON |
| [Option pricing](cpu-walkthroughs.md#option-pricing) | Black and Scholes (1973), assumptions on p. 640 and Eq. 13 on p. 644 | Executed equation-based example; synthetic inputs |
| [Household saving](cpu-walkthroughs.md#household-saving) | Carroll (1997), Sections II–III; baseline from the Econ-ARK reproduction | Executed port of the baseline calibration |
| [Results in OpenUSD](cpu-walkthroughs.md#results-in-openusd) | Carries the battery example's outputs into a scene data prim | Executed original exchange example; not a method from the paper |
| [Robot learning](robotics.md) | Mittal et al. (2023), Orbit's USD architecture and RL workflows | Checked Isaac Lab v2.2.0 task and training entry point; not run |
| [Market microstructure](markets.md) | Byrd et al. (2020), ABIDES; upstream RMSC03 experiment | Checked configuration and upstream commands; not run |
| [Household paper reproduction](economics.md) | Carroll (1997), author-associated Econ-ARK figures and tables | Checked source and reproduction script; old environment not run |
| [Fluid–structure interaction](fluid-structure.md) | Turek and Hron (2006), numerical benchmark | Checked preCICE FSI3 run route; not run |
| [European energy networks](energy.md) | Hörsch et al. (2018), PyPSA-Eur | Checked current tutorial; not a rerun of the 2018 model |
| [Service queues](queues.md) | Monks and Harper (2023), worked urgent-care call-centre model | Published code archive and browser/local setup; not run |
| [Urban traffic](traffic.md) | Codeca et al. (2017), Luxembourg traffic-demand evaluation | Author configuration files and version restriction; not run |
| [Fisheries and policy](fisheries.md) | Lemmen et al. (2024), ViNoS | Article read; model artifact retrieval pending |

**New to simulation?** Start with [battery discharge](cpu-walkthroughs.md#battery-discharge), then inspect its CSV before changing a parameter. For a browser route, try the published [service-model notebooks](queues.md). A hosted notebook service's availability is separate from the availability of the source code.

**Planning a reproduction?** Use the paper-associated archive, identify a particular result, match its inputs and settings, and agree the comparison measure before running. A current software tutorial may implement the same kind of model with different defaults. Keep those differences visible.
