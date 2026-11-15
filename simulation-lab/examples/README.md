# Literature examples

Start with a paper and a specific model, equation, listing, or benchmark. The table distinguishes local teaching runs from upstream reproduction routes. The [bibliography](../bibliography.md) supplies complete citations. For the full catalog, use the [paper-to-code construction routes for all 60 tools](../research/README.md); their source and execution assessments are separate from the teaching runs below.

| Example | Literature connection | Available now |
| --- | --- | --- |
| [Battery discharge](cpu-walkthroughs.md#battery-discharge) | Sulzer et al. (2021), Listing 1 | Executed adaptation; Python, CSV, parameter JSON |
| [Option pricing](cpu-walkthroughs.md#option-pricing) | Black and Scholes (1973), assumptions on p. 640 and Eq. 13 on p. 644 | Executed equation-based example; synthetic inputs |
| [Household saving](cpu-walkthroughs.md#household-saving) | Carroll (1997), Sections II–III; baseline from the Econ-ARK reproduction | Executed port of the baseline calibration |
| [Results in OpenUSD](cpu-walkthroughs.md#results-in-openusd) | Carries the battery example's outputs into a scene data prim | Executed original exchange example; not a method from the paper |
| [Robot learning](robotics.md) | Mittal et al. (2023), Orbit's USD architecture and RL workflows | Checked Isaac Lab v2.2.0 task and training entry point; not run |
| [Market microstructure](markets.md) | Byrd et al. (2020), ABIDES; upstream RMSC03 experiment | Checked configuration and upstream commands; not run |
| [Household paper reproduction](../reproductions/hark.md) | Carroll (1997), author-associated Econ-ARK figures and tables | Legacy author code executed; Table I rounding target not met |
| [Fluid–structure interaction](fluid-structure.md) | Turek and Hron (2006), numerical benchmark | Checked preCICE FSI3 run route; not run |
| [European energy networks](energy.md) | Hörsch et al. (2018), PyPSA-Eur | Checked current tutorial; not a rerun of the 2018 model |
| [Service queues](queues.md) | Monks and Harper (2023), worked urgent-care call-centre model | Published code archive and browser/local setup; not run |
| [Urban traffic](../reproductions/sumo.md) | Codeca et al. (2017), Luxembourg traffic-demand evaluation | SUMO 0.26 author city model executed for one hour; original validation data still required |
| [Fisheries and policy](fisheries.md) | Lemmen et al. (2024), ViNoS | Versioned model and experiment inspected; not run |

**New to simulation?** Start with [battery discharge](cpu-walkthroughs.md#battery-discharge), then inspect its CSV before changing a parameter. For a browser route, try the published [service-model notebooks](queues.md). A hosted notebook service's availability is separate from the availability of the source code.

**Planning a reproduction?** Use the paper-associated archive, identify a particular result, match its inputs and settings, and agree the comparison measure before running. A current software tutorial may implement the same kind of model with different defaults. Keep those differences visible.

## Author-code campaign examples

The [21-candidate campaign](../reproductions/README.md) records every attempted route, including blocked targets. These additional examples include actual outputs, repeatable bundles and scoped comparisons. A successful code execution does not establish agreement with every result in the article.

| Example | Paper connection | Recorded status |
| --- | --- | --- |
| [Generate a published MOVi-A dataset scene with Kubric and Blender](../reproductions/blender.md) | UnmodifiedMOVi-Aworker from paper-submission-dateKubriccommit; generatedscene and publisheddesign-property comparison. Currentpublicassetbytes and reconstructedruntime differ from fullhistoricalimage. | Author code executed; see paper comparison |
| [Gazebo](../reproductions/gz-sim.md) | Exact author paper artifact, explicitly labeled research artifact; paper links same repository. | Author code executed; see paper comparison |
| [Bullet / PyBullet](../reproductions/bullet3.md) | Author repository explicitly identifies the two environments used in the paper and releases PPO checkpoints. Released checkpoint widths differ from TableII, so this is an adapted author-policy replay. | Executed adaptation |
| [CARLA](../reproductions/carla.md) | Official CARLA team CoRL2017 experiment suite for CARLA 0.8.4. This is a later benchmark implementation, not automatically the exact original simulator revision. | Executed adaptation |
| [FEniCSx / DOLFINx](../reproductions/dolfinx.md) | Unmodified author model and adaptive estimator implementation; one named preprint figure result compared numerically using the same parameters. | Selected published target compared; human review pending |
| [AutoCkt public op-amp: author-code training and held-out evaluation](../reproductions/ngspice.md) | Direct author circuit and public ngspice code; paper/code architecture discrepancies documented before execution. | Executed adaptation |
| [DualSPHysics](../reproductions/dualsphysics.md) | Current author SPH validation case compared against the authors’ experimental fixture attributed to Koshizuka and Oka (1996). This executes the current case, not the original MPS algorithm or historical software-paper results. | Executed adaptation |
| [TaxFuncIntegr: fresh macro steady states from public fitted inputs](../reproductions/tax-calculator.md) | Fresh author-code macro stage with supplied public fitted inputs; named author-manuscript table comparison. Not a rerun of Tax-Calculator micro-estimation or the complete published study. | Author code executed; see paper comparison |
| [The published M/M/1 queue and its replication interval](../reproductions/simmer.md) | Direct publisher-supplied model and Section4.2 printed result, with isolated modernR compatibility environment; independent-seed extension separately labeled. | Selected published target compared; human review pending |
| [Published ring-network switching states and full-day comparison](../reproductions/pandapower.md) | Actual author code and original model/data; partial quantitative reproduction of an identified paper case study. | Author code executed; see paper comparison |
| [Archived energy-system metric comparison and verified optimizer blocker](../reproductions/calliope.md) | Exact paper-deposited model/results and exact requested runtime source recovered. Successful archive analysis is explicitly separate from new optimization. | Archived outputs analysed; simulation not rerun |
| [Tellurium Calzone archive: selected Figure4B Wee1c comparison](../reproductions/tellurium.md) | Exact author artifact; execution and numeric paper comparison scoped as declared above | Selected published target compared; human review pending |
| [Historical Brian eye-movement author model with exploratory Figure3 comparison](../reproductions/brian2.md) | Exact author artifact; execution and numeric paper comparison scoped as declared above | Author code executed; see paper comparison |
| [Unison: Table 2 and thread determinism](../reproductions/ns-3-dev-git.md) | Original author-code reconstruction of Section 6.2, Table 2, with matched source, input data and settings. Thread-determinism checks have the narrower tested scope recorded separately. | Selected published target compared; human review pending |
| [SimGrid: Figure 13 endpoint workloads](../reproductions/simgrid.md) | Original reference-66 model and workload family. The introduction passage before Section 2 reconciles paper v3/v4 language with repository 3.10/3.36 pins. Makespan agreement is an author-benchmark consistency check, separate from historical hardware-performance reproduction. | Author code executed; see paper comparison |
| [Smets–Wouters maintained model: fresh mode evaluation and shock decomposition](../reproductions/dynare.md) | Maintained author-derived implementation of the published DSGE model ran with bundled data/mode and modern runtime; distinct from original archive reproduction. | Executed adaptation |
