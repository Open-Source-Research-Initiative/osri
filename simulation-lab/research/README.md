# Research routes for all 60 Simulation Lab tools

Choose a tool, inspect the linked paper and code, and identify the result to compare before launching a run. These routes extend the [existing teaching examples](../examples/README.md).

Researched 2026-11-15 at Cole / @ajhcs's request by six domain agents, with integration and source review by Codex. Human scientific review is pending. Each record distinguishes paper-associated code, a model adaptation, a software-paper demonstration, and a related tutorial. A route covering a tool does not mean its paper has been reproduced.

## Current evidence

[Author-code attempts for the 21 selected candidates](../reproductions/README.md) report actual runs, comparisons, adaptations, archive analyses, and blockers.

[Initial planning review](verification/review.json) · [Author-code campaign review](../reproductions/review.json). The reviewers were agents; human scientific review remains pending.

| Execution status | Tools |
| --- | ---: |
| Not run | 33 |
| Attempted; blocked | 3 |
| Example executed | 19 |
| Saved author outputs analysed; simulator not run | 1 |
| Published target compared | 4 |

| Relationship to the paper | Tools |
| --- | ---: |
| Paper result candidate | 21 |
| Paper model adaptation | 27 |
| Software paper example | 10 |
| Related tutorial only | 1 |
| Unresolved | 1 |

Counts apply to these new research routes. The four original executed teaching examples retain their separate run records.

## Build an example

1. Select a named figure, table, equation, or benchmark and record its inputs and observable. Prefer the paper's archived code over a moving default branch.
2. Pin source commits, environment, datasets, random seeds, and data or asset terms. If an exact environment is unavailable, document the adaptation before interpreting its output.
3. Run in an isolated environment and keep the original outputs, logs, failures, package versions, and hashes. A smoke test establishes only that the selected path runs.
4. Compare the stated observable using a justified tolerance or uncertainty interval. Record deviations and obtain human scientific review before calling it a reproduced research result.

The per-tool next action identifies the remaining work. Restricted papers may be supplied through the [resource-request route](../../governance/resource-requests.md); library PDFs stay outside the public repository. Larger studies belong in their own research repositories.

## Choose a route

[Download the route inventory](routes.csv) · [Structured source records](routes.json)

| Tool | Research route | Execution |
| --- | --- | --- |
| [OpenUSD](scenes-robotics.md#openusd) | Paper model adaptation | Not run |
| [Blender](scenes-robotics.md#blender) | Paper result candidate | Example executed |
| [Isaac Sim](scenes-robotics.md#isaacsim) | Software paper example | Not run |
| [Isaac Lab](scenes-robotics.md#isaaclab) | Software paper example | Not run |
| [MuJoCo](scenes-robotics.md#mujoco) | Software paper example | Example executed |
| [Gazebo](scenes-robotics.md#gz-sim) | Paper result candidate | Example executed |
| [Webots](scenes-robotics.md#webots) | Paper model adaptation | Not run |
| [Bullet / PyBullet](scenes-robotics.md#bullet3) | Paper result candidate | Example executed |
| [Project Chrono](scenes-robotics.md#chrono) | Software paper example | Not run |
| [SOFA](scenes-robotics.md#sofa) | Paper model adaptation | Not run |
| [Drake](robotics-fem-cfd.md#drake) | Paper model adaptation | Not run |
| [BlenderProc](robotics-fem-cfd.md#blenderproc) | Paper model adaptation | Not run |
| [CARLA](robotics-fem-cfd.md#carla) | Paper result candidate | Example executed |
| [OpenFOAM (Foundation)](robotics-fem-cfd.md#openfoam-dev) | Paper model adaptation | Not run |
| [SU2](robotics-fem-cfd.md#su2) | Paper model adaptation | Not run |
| [preCICE](robotics-fem-cfd.md#precice) | Paper result candidate | Attempted; blocked |
| [FEniCSx / DOLFINx](robotics-fem-cfd.md#dolfinx) | Paper result candidate | Published target compared |
| [deal.II](robotics-fem-cfd.md#dealii) | Paper result candidate | Attempted; blocked |
| [MFEM](robotics-fem-cfd.md#mfem) | Software paper example | Example executed |
| [MOOSE](robotics-fem-cfd.md#moose) | Paper model adaptation | Not run |
| [Elmer FEM](multiphysics.md#elmerfem) | Paper model adaptation | Not run |
| [CalculiX](multiphysics.md#calculix) | Software paper example | Not run |
| [OpenModelica](multiphysics.md#openmodelica) | Paper model adaptation | Not run |
| [PyBaMM](multiphysics.md#pybamm) | Paper model adaptation | Not run |
| [openEMS](multiphysics.md#openems) | Related tutorial only | Not run |
| [ngspice](multiphysics.md#ngspice) | Paper result candidate | Example executed |
| [Cantera](multiphysics.md#cantera) | Paper model adaptation | Example executed |
| [LAMMPS](multiphysics.md#lammps) | Software paper example | Not run |
| [DualSPHysics](multiphysics.md#dualsphysics) | Paper result candidate | Example executed |
| [QuantLib](finance-economics.md#quantlib) | Paper model adaptation | Not run |
| [ABIDES](finance-economics.md#abides) | Paper model adaptation | Not run |
| [FinRL](finance-economics.md#finrl) | Paper model adaptation | Not run |
| [Open Source Risk Engine](finance-economics.md#engine) | Paper result candidate | Attempted; blocked |
| [HARK / Econ-ARK](finance-economics.md#hark) | Paper result candidate | Example executed |
| [QuantEcon.py](finance-economics.md#quantecon) | Paper model adaptation | Not run |
| [OG-Core](finance-economics.md#og-core) | Paper model adaptation | Not run |
| [Tax-Calculator](finance-economics.md#tax-calculator) | Paper result candidate | Example executed |
| [OpenFisca](finance-economics.md#openfisca-core) | Unresolved | Not run |
| [Mesa](agents-operations.md#mesa) | Software paper example | Not run |
| [Agents.jl](agents-operations.md#agents) | Paper model adaptation | Not run |
| [NetLogo](agents-operations.md#netlogo) | Software paper example | Not run |
| [GAMA](agents-operations.md#gama) | Software paper example | Not run |
| [Ciw](agents-operations.md#ciw) | Paper model adaptation | Example executed |
| [simmer](agents-operations.md#simmer) | Paper result candidate | Published target compared |
| [PyPSA](energy-natural-sciences.md#pypsa) | Paper model adaptation | Not run |
| [pandapower](energy-natural-sciences.md#pandapower) | Paper result candidate | Example executed |
| [Calliope](energy-natural-sciences.md#calliope) | Paper result candidate | Saved author outputs analysed; simulator not run |
| [SUMO](energy-natural-sciences.md#sumo) | Paper result candidate | Example executed |
| [MATSim](agents-operations.md#matsim-libs) | Paper model adaptation | Not run |
| [WNTR](multiphysics.md#wntr) | Paper model adaptation | Example executed |
| [EnergyPlus](energy-natural-sciences.md#energyplus) | Paper model adaptation | Not run |
| [WRF](energy-natural-sciences.md#wrf) | Paper model adaptation | Not run |
| [OpenDrift](energy-natural-sciences.md#opendrift) | Paper model adaptation | Not run |
| [COPASI](energy-natural-sciences.md#copasi) | Paper model adaptation | Not run |
| [Tellurium](energy-natural-sciences.md#tellurium) | Paper result candidate | Published target compared |
| [Brian 2](energy-natural-sciences.md#brian2) | Paper result candidate | Example executed |
| [ns-3](agents-operations.md#ns-3-dev-git) | Paper result candidate | Published target compared |
| [SimGrid](agents-operations.md#simgrid) | Paper result candidate | Example executed |
| [SimPy](agents-operations.md#simpy) | Paper model adaptation | Example executed |
| [Dynare](finance-economics.md#dynare) | Paper result candidate | Example executed |

## Refresh and check

Edit `routes.json`, then run `python3 simulation-lab/research.py --write` and `python3 simulation-lab/catalog.py --write`. Validation enforces complete tool coverage and generated-file consistency; it does not verify scientific claims or contact upstream sources.
