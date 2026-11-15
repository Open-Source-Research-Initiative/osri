# Reproducing 21 paper-linked candidates

Author code, accessible inputs, measured outputs, and comparisons from the candidate reproduction campaign. Cole / @ajhcs directed the work; domain agents performed the runs and other agents reviewed the evidence. Human scientific review remains pending.

A completed code run and a match to a published target are reported separately. Some paper-linked artifacts differ from the article or no longer supply the required runtime, trained model, data, or reference output. These differences and failed attempts remain part of the record.

| Recorded outcome | Tools |
| --- | ---: |
| Published target compared | 5 |
| Author code executed | 6 |
| Adapted run executed | 6 |
| Saved outputs analysed; simulation not rerun | 1 |
| Attempted; blocked | 3 |

Pass/fail in the table applies only to the comparison defined in its guide, including exploratory or archived-output checks. A passing selected paper target additionally needs the corresponding execution classification.

The preCICE and deal.II candidates share one coupled experiment. Counts describe tools; they do not imply independent experiments or reproduction of every result in a paper.

| Candidate | Execution | Recorded comparison (scope in guide) |
| --- | --- | --- |
| [Generate a published MOVi-A dataset scene with Kubric and Blender ](blender.md) | Author code executed | Passed within stated rule |
| [Gazebo ](gz-sim.md) | Author code executed | Did not pass |
| [Bullet / PyBullet ](bullet3.md) | Adapted run executed | Did not pass |
| [CARLA ](carla.md) | Adapted run executed | Did not pass |
| [preCICE ](precice.md) | Attempted; blocked | Not established |
| [FEniCSx / DOLFINx ](dolfinx.md) | Published target compared | Passed within stated rule |
| [deal.II ](dealii.md) | Attempted; blocked | Not established |
| [AutoCkt public op-amp: author-code training and held-out evaluation ](ngspice.md) | Adapted run executed | Did not pass |
| [DualSPHysics ](dualsphysics.md) | Adapted run executed | Not established |
| [ORE central-clearing study: fresh simulation blocked by missing author generator ](engine.md) | Attempted; blocked | Not established |
| [Carroll author-associated HARK replication: executed with failed strict table comparison ](hark.md) | Author code executed | Did not pass |
| [TaxFuncIntegr: fresh macro steady states from public fitted inputs ](tax-calculator.md) | Author code executed | Passed within stated rule |
| [The published M/M/1 queue and its replication interval ](simmer.md) | Published target compared | Passed within stated rule |
| [Published ring-network switching states and full-day comparison ](pandapower.md) | Published target compared | Did not pass |
| [Archived energy-system metric comparison and verified optimizer blocker ](calliope.md) | Saved outputs analysed; simulation not rerun | Passed within stated rule |
| [Historical LuST city-model run with three seeds ](sumo.md) | Adapted run executed | Not established |
| [Tellurium Calzone archive: selected Figure4B Wee1c comparison ](tellurium.md) | Published target compared | Passed within stated rule |
| [Historical Brian eye-movement author model with exploratory Figure3 comparison ](brian2.md) | Author code executed | Passed within stated rule |
| [Unison: Table 2 and thread determinism ](ns-3-dev-git.md) | Published target compared | Passed within stated rule |
| [SimGrid: Figure 13 endpoint workloads ](simgrid.md) | Author code executed | Passed within stated rule |
| [Smets–Wouters maintained model: fresh mode evaluation and shock decomposition ](dynare.md) | Adapted run executed | Not established |

The [structured campaign record](campaign.json) preserves all candidate outcomes. Each guide links numeric outputs and a compact run record; full environments, sources, native results and failed attempts remain in the development evidence directory. Follow the [contribution guide](../contributing.md) when extending a result.
