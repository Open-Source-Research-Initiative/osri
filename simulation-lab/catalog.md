# Simulation tool catalog

60 tools with open-source cores, grouped by use. This is a growing inventory; it is not an exhaustive list of all simulators. Some components depend on separately licensed runtimes or assets, as noted below.

Read the [example index](examples/README.md), [source notes](source-notes.md), and [verification record](verification.md). Repository availability does not mean a tool was installed or a paper reproduced. A software-description paper establishes context; it is not automatically an application example.

Generated from [tools.csv](tools.csv), [papers.csv](papers.csv), and [examples.csv](examples.csv). To contribute, follow the [catalog guide](contributing.md).

## Scenes and robotics

### OpenUSD

Compose scenes and exchange time-sampled results; not a solver.

[Source](https://github.com/PixarAnimationStudios/OpenUSD) · [Documentation](https://openusd.org/release/tut_usd_tutorials.html) · [License](https://github.com/PixarAnimationStudios/OpenUSD/blob/dev/LICENSE.txt)

**Terms:** TOST-1.0 (Apache-derived; modified trademarks). Custom result attributes need an agreed schema; preserve native solver inputs.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** [Battery results in OpenUSD](examples/cpu-walkthroughs.md#results-in-openusd) — Executed adaptation; [Robot learning with Isaac Lab](examples/robotics.md) — Upstream instructions checked; not run

**Research construction route:** [Orbit: A Unified Simulation Framework for Interactive Robot Learning Environments](research/scenes-robotics.md#openusd) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Blender

Create and inspect geometry; render simulation outputs.

[Source](https://github.com/blender/blender) · [Documentation](https://docs.blender.org/manual/en/latest/) · [License](https://github.com/blender/blender#license)

**Terms:** GNU GPL; component notices apply. Scene authoring and rendering do not establish physical validity.

**Literature:** [BlenderProc2: A Procedural Pipeline for Photorealistic Rendering (2023)](bibliography.md#blenderproc); [Kubric: A scalable dataset generator (2022)](bibliography.md#replication-blender)

**Walkthrough:** [Generate a published MOVi-A dataset scene with Kubric and Blender](reproductions/blender.md) — Author code executed; see paper comparison

**Research construction route:** [Kubric: A scalable dataset generator](research/scenes-robotics.md#blender) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Isaac Sim

Robot dynamics; sensors; synthetic scenes.

[Source](https://github.com/isaac-sim/IsaacSim) · [Documentation](https://docs.isaacsim.omniverse.nvidia.com/) · [License](https://github.com/isaac-sim/IsaacSim/blob/release/6.3/LICENSE)

**Terms:** Apache-2.0 source; additional runtime and asset terms. Omniverse Kit and assets have separate NVIDIA terms; suitable NVIDIA GPU required for the documented workflow.

**Literature:** [Orbit: A Unified Simulation Framework for Interactive Robot Learning Environments (2023)](bibliography.md#orbit)

**Walkthrough:** [Robot learning with Isaac Lab](examples/robotics.md) — Upstream instructions checked; not run

**Research construction route:** [Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning](research/scenes-robotics.md#isaacsim) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Isaac Lab

Robot-learning environments and parallel training.

[Source](https://github.com/isaac-sim/IsaacLab) · [Documentation](https://isaac-sim.github.io/IsaacLab/) · [License](https://github.com/isaac-sim/IsaacLab/blob/main/LICENSE)

**Terms:** BSD-3-Clause core; dependency terms apply. The walkthrough pins v2.2.0 with Isaac Sim 5.0.0; current main has changed. GPU runtime and assets have separate terms.

**Literature:** [Orbit: A Unified Simulation Framework for Interactive Robot Learning Environments (2023)](bibliography.md#orbit)

**Walkthrough:** [Robot learning with Isaac Lab](examples/robotics.md) — Upstream instructions checked; not run

**Research construction route:** [Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning](research/scenes-robotics.md#isaaclab) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### MuJoCo

Articulated-body dynamics and contact.

[Source](https://github.com/google-deepmind/mujoco) · [Documentation](https://mujoco.readthedocs.io/) · [License](https://github.com/google-deepmind/mujoco#license)

**Terms:** Apache-2.0. CPU core; rendering and accelerated backends have additional requirements.

**Literature:** [MuJoCo: A physics engine for model-based control (2012)](bibliography.md#mujoco)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [DeepMind Control Suite](research/scenes-robotics.md#mujoco) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Gazebo

Robot worlds; sensors; systems integration.

[Source](https://github.com/gazebosim/gz-sim) · [Documentation](https://gazebosim.org/docs/) · [License](https://github.com/gazebosim/gz-sim#license)

**Terms:** Apache-2.0. Current Gazebo differs from the historical Gazebo in the 2004 paper; pin simulator and plugins together.

**Literature:** [Design and use paradigms for gazebo, an open-source multi-robot simulator (2004)](bibliography.md#gazebo); [GzDRL: Reproducible and Scalable Deep Reinforcement Learning with Gazebo (2026)](bibliography.md#replication-gz-sim)

**Walkthrough:** [Gazebo](reproductions/gz-sim.md) — Author code executed; see paper comparison

**Research construction route:** [GzDRL: Reproducible and Scalable Deep Reinforcement Learning with Gazebo](research/scenes-robotics.md#gz-sim) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Webots

Robot simulation with ready-made worlds and controllers.

[Source](https://github.com/cyberbotics/webots) · [Documentation](https://cyberbotics.com/doc/guide/index) · [License](https://github.com/cyberbotics/webots#license)

**Terms:** Apache-2.0. Check the individual robot and scene asset licenses.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Deepbots: A Webots-Based Deep Reinforcement Learning Framework for Robotics](research/scenes-robotics.md#webots) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Bullet / PyBullet

Rigid-body dynamics; collision; Python robotics environments.

[Source](https://github.com/bulletphysics/bullet3) · [Documentation](https://github.com/bulletphysics/bullet3/tree/master/examples/pybullet) · [License](https://github.com/bulletphysics/bullet3/blob/master/LICENSE.txt)

**Terms:** Zlib core; separate bundled notices. Robot models and third-party examples carry separate terms.

**Literature:** [Sim-to-Real: Learning Agile Locomotion For Quadruped Robots (2018)](bibliography.md#replication-bullet3)

**Walkthrough:** [Bullet / PyBullet](reproductions/bullet3.md) — Executed adaptation

**Research construction route:** [Sim-to-Real: Learning Agile Locomotion For Quadruped Robots](research/scenes-robotics.md#bullet3) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Project Chrono

Multibody dynamics; contact; vehicle and granular systems.

[Source](https://github.com/projectchrono/chrono) · [Documentation](https://api.projectchrono.org/) · [License](https://github.com/projectchrono/chrono#license)

**Terms:** BSD-3-Clause. Choose modules and dependencies for the intended model; some workflows need substantial compute.

**Literature:** [Chrono: An Open Source Multi-physics Dynamics Engine (2016)](bibliography.md#chrono)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Chrono::Vehicle: template-based ground vehicle modelling and simulation](research/scenes-robotics.md#chrono) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### SOFA

Deformable-body and interactive multiphysics simulation.

[Source](https://github.com/sofa-framework/sofa) · [Documentation](https://www.sofa-framework.org/community/doc/) · [License](https://github.com/sofa-framework/sofa#license)

**Terms:** LGPL-2.1. Use for nonclinical computational studies here; plugin and material models need their own checks.

**Literature:** [SOFA: A Multi-Model Framework for Interactive Physical Simulation (2012)](bibliography.md#sofa)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Software toolkit for modeling, simulation, and control of soft robots](research/scenes-robotics.md#sofa) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Drake

Robot dynamics; control; optimization and system analysis.

[Source](https://github.com/RobotLocomotion/drake) · [Documentation](https://drake.mit.edu/) · [License](https://github.com/RobotLocomotion/drake/blob/master/LICENSE.TXT)

**Terms:** BSD-3-Clause core; third-party notices. Some optional optimization backends are proprietary; use an open backend when required.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Swing up control of the Acrobot](research/robotics-fem-cfd.md#drake) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### BlenderProc

Generate synthetic images with labeled scene data.

[Source](https://github.com/DLR-RM/BlenderProc) · [Documentation](https://dlr-rm.github.io/BlenderProc/) · [License](https://github.com/DLR-RM/BlenderProc#license)

**Terms:** GPL-3.0. Rendering pipeline; external meshes and textures need separate rights checks.

**Literature:** [BlenderProc2: A Procedural Pipeline for Photorealistic Rendering (2023)](bibliography.md#blenderproc)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [BOP Challenge 2020 on 6D Object Localization](research/robotics-fem-cfd.md#blenderproc) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### CARLA

Autonomous-driving worlds; sensors and traffic agents.

[Source](https://github.com/carla-simulator/carla) · [Documentation](https://carla.readthedocs.io/) · [License](https://github.com/carla-simulator/carla#license)

**Terms:** MIT. MIT source does not cover the entire Unreal Engine runtime or every asset.

**Literature:** [CARLA: An Open Urban Driving Simulator (2017)](bibliography.md#replication-carla)

**Walkthrough:** [CARLA](reproductions/carla.md) — Executed adaptation

**Research construction route:** [CARLA: An Open Urban Driving Simulator](research/robotics-fem-cfd.md#carla) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

## Engineering and multiphysics

### OpenFOAM (Foundation)

Finite-volume CFD and related continuum solvers.

[Source](https://github.com/OpenFOAM/OpenFOAM-dev) · [Documentation](https://doc.cfd.direct/openfoam/user-guide) · [License](https://github.com/OpenFOAM/OpenFOAM-dev/blob/master/COPYING)

**Terms:** GPL-3.0-or-later. Foundation and OpenCFD releases are different distributions; adapters must match the selected distribution.

**Literature:** [A tensorial approach to computational continuum mechanics using object-oriented techniques (1998)](bibliography.md#openfoam); [Proposal for Numerical Benchmarking of Fluid-Structure Interaction between an Elastic Object and Laminar Incompressible Flow (2006)](bibliography.md#fsi-benchmark)

**Walkthrough:** [Turek-Hron fluid-structure interaction](examples/fluid-structure.md) — Upstream instructions checked; not run

**Research construction route:** [Proposal for Numerical Benchmarking of Fluid-Structure Interaction between an Elastic Object and Laminar Incompressible Flow](research/robotics-fem-cfd.md#openfoam-dev) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### SU2

Aerodynamics; CFD; adjoint design optimization.

[Source](https://github.com/su2code/SU2) · [Documentation](https://su2code.github.io/docs/) · [License](https://github.com/su2code/SU2/blob/master/LICENSE.md)

**Terms:** LGPL-2.1. Mesh and boundary-condition checks are required before interpreting forces.

**Literature:** [Stanford University Unstructured (SU2): An open-source integrated computational environment for multi-physics simulation and design (2013)](bibliography.md#su2)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Stanford University Unstructured (SU2): An open-source integrated computational environment for multi-physics simulation and design](research/robotics-fem-cfd.md#su2) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### preCICE

Couple separate solvers across meshes and time steps.

[Source](https://github.com/precice/precice) · [Documentation](https://precice.org/docs.html) · [License](https://github.com/precice/precice#license)

**Terms:** LGPL-3.0. Coupling library; requires compatible native solvers and adapters.

**Literature:** [preCICE v2: A sustainable and user-friendly coupling library (2022)](bibliography.md#precice); [Proposal for Numerical Benchmarking of Fluid-Structure Interaction between an Elastic Object and Laminar Incompressible Flow (2006)](bibliography.md#fsi-benchmark)

**Walkthrough:** [Turek-Hron fluid-structure interaction](examples/fluid-structure.md) — Upstream instructions checked; not run

**Research construction route:** [Proposal for Numerical Benchmarking of Fluid-Structure Interaction between an Elastic Object and Laminar Incompressible Flow](research/robotics-fem-cfd.md#precice) — attempted blocked. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### FEniCSx / DOLFINx

Finite-element PDE models in Python and C++.

[Source](https://github.com/FEniCS/dolfinx) · [Documentation](https://docs.fenicsproject.org/dolfinx/main/python/) · [License](https://github.com/FEniCS/dolfinx#license)

**Terms:** LGPL-3.0. Keep variational equations; boundary conditions; mesh and solver configuration.

**Literature:** [Adaptive Finite Element Methods Based on Flux Equilibration Using FEniCSx (2026)](bibliography.md#replication-dolfinx)

**Walkthrough:** [FEniCSx / DOLFINx](reproductions/dolfinx.md) — Selected paper target compared; human review pending

**Research construction route:** [Adaptive Finite Element Methods Based on Flux Equilibration Using FEniCSx](research/robotics-fem-cfd.md#dolfinx) — reproduced target. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### deal.II

Finite-element framework with adaptive meshes.

[Source](https://github.com/dealii/dealii) · [Documentation](https://www.dealii.org/current/doxygen/deal.II/Tutorial.html) · [License](https://github.com/dealii/dealii/blob/master/LICENSE.md)

**Terms:** Apache-2.0 with LLVM exception OR LGPL-2.1-or-later. Tutorial examples can have their own notices; the FSI3 guide requires the nonlinear adapter solver.

**Literature:** [Proposal for Numerical Benchmarking of Fluid-Structure Interaction between an Elastic Object and Laminar Incompressible Flow (2006)](bibliography.md#fsi-benchmark)

**Walkthrough:** [Turek-Hron fluid-structure interaction](examples/fluid-structure.md) — Upstream instructions checked; not run

**Research construction route:** [Proposal for Numerical Benchmarking of Fluid-Structure Interaction between an Elastic Object and Laminar Incompressible Flow](research/robotics-fem-cfd.md#dealii) — attempted blocked. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### MFEM

High-order finite-element discretization and solvers.

[Source](https://github.com/mfem/mfem) · [Documentation](https://mfem.org/examples/) · [License](https://github.com/mfem/mfem#license)

**Terms:** BSD-3-Clause. CPU and accelerator support depends on the chosen build and backend.

**Literature:** [MFEM: A modular finite element methods library (2021)](bibliography.md#mfem)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [MFEM: A modular finite element methods library](research/robotics-fem-cfd.md#mfem) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### MOOSE

Build coupled finite-element and finite-volume applications.

[Source](https://github.com/idaholab/moose) · [Documentation](https://mooseframework.inl.gov/) · [License](https://github.com/idaholab/moose#license)

**Terms:** LGPL-2.1. Framework and downstream applications can have different licenses and data requirements.

**Literature:** [MOOSE: Enabling massively parallel multiphysics simulation (2020)](bibliography.md#moose)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [MOOSE: Enabling massively parallel multiphysics simulation](research/robotics-fem-cfd.md#moose) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Elmer FEM

Structural; thermal; electromagnetic and fluid PDE models.

[Source](https://github.com/ElmerCSC/elmerfem) · [Documentation](https://www.elmerfem.org/blog/documentation/) · [License](https://github.com/ElmerCSC/elmerfem/blob/devel/LICENSE.md)

**Terms:** GPL-2.0; some libraries LGPL. Inspect component notices and the selected solver manual.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Capabilities and performance of Elmer/Ice, a new-generation ice sheet model](research/multiphysics.md#elmerfem) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### CalculiX

Structural and thermal finite-element analysis.

[Source](https://github.com/Dhondtguido/CalculiX) · [Documentation](https://www.calculix.de/) · [License](https://github.com/Dhondtguido/CalculiX#license)

**Terms:** GPL-2.0. Keep native input decks and constitutive-model assumptions; pre/postprocessor is a separate component.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [preCICE v2: A sustainable and user-friendly coupling library](research/multiphysics.md#calculix) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### OpenModelica

Equation-based dynamic systems and Modelica models.

[Source](https://github.com/OpenModelica/OpenModelica) · [Documentation](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/) · [License](https://github.com/OpenModelica/OpenModelica/blob/master/OSMC-License.txt)

**Terms:** AGPL-3.0 option; OSMC alternatives; separate runtime terms. Modelica libraries and FMUs have their own terms and dependencies.

**Literature:** [The OpenModelica Integrated Environment for Modeling, Simulation, and Model-Based Development (2020)](bibliography.md#openmodelica)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [OMG: A Scalable and Flexible Simulation and Testing Environment Toolbox for Intelligent Microgrid Control](research/multiphysics.md#openmodelica) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### PyBaMM

Electrochemical battery models and discharge protocols.

[Source](https://github.com/pybamm-team/PyBaMM) · [Documentation](https://docs.pybamm.org/) · [License](https://github.com/pybamm-team/PyBaMM#license)

**Terms:** BSD-3-Clause. CPU example included; parameter sets apply to particular cells and conditions.

**Literature:** [Python Battery Mathematical Modelling (PyBaMM) (2021)](bibliography.md#pybamm)

**Walkthrough:** [Battery discharge](examples/cpu-walkthroughs.md#battery-discharge) — Executed adaptation; [Battery results in OpenUSD](examples/cpu-walkthroughs.md#results-in-openusd) — Executed adaptation

**Research construction route:** [Python Battery Mathematical Modelling (PyBaMM)](research/multiphysics.md#pybamm) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### openEMS

Electromagnetic fields with finite-difference time-domain methods.

[Source](https://github.com/thliebig/openEMS) · [Documentation](https://docs.openems.de/) · [License](https://github.com/thliebig/openEMS#license)

**Terms:** GPL-3.0. Requires geometry and a mesh; check excitation; absorbing boundaries and convergence.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [openEMS – a free and open source equivalent‐circuit (EC) FDTD simulation platform supporting cylindrical coordinates suitable for the analysis of traveling wave MRI applications](research/multiphysics.md#openems) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### ngspice

Analog and mixed-signal circuit simulation.

[Source](https://github.com/imr/ngspice) · [Documentation](https://ngspice.sourceforge.io/docs.html) · [License](https://github.com/imr/ngspice#license)

**Terms:** BSD-based; mixed component notices. Linked GitHub source is a mirror; upstream is SourceForge. Device models may have separate restrictions.

**Literature:** [AutoCkt: Deep Reinforcement Learning of Analog Circuit Designs (2020)](bibliography.md#replication-ngspice)

**Walkthrough:** [AutoCkt public op-amp: author-code training and held-out evaluation](reproductions/ngspice.md) — Executed adaptation

**Research construction route:** [AutoCkt: Deep Reinforcement Learning of Analog Circuit Designs](research/multiphysics.md#ngspice) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Cantera

Chemical kinetics; reacting flows and transport.

[Source](https://github.com/Cantera/cantera) · [Documentation](https://cantera.org/) · [License](https://github.com/Cantera/cantera/blob/main/License.txt)

**Terms:** BSD-3-Clause. Reaction-mechanism files and their validity ranges matter independently of software licensing.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Impact of non-ideal behavior on ignition delay and chemical kinetics in high-pressure shock tube reactors](research/multiphysics.md#cantera) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### LAMMPS

Particle and molecular dynamics across scales.

[Source](https://github.com/lammps/lammps) · [Documentation](https://docs.lammps.org/) · [License](https://github.com/lammps/lammps#license)

**Terms:** GPL-2.0. Select potential files and units explicitly; accelerator packages are optional.

**Literature:** [LAMMPS - a flexible simulation tool for particle-based materials modeling at the atomic, meso, and continuum scales (2022)](bibliography.md#lammps)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [LAMMPS - a flexible simulation tool for particle-based materials modeling at the atomic, meso, and continuum scales](research/multiphysics.md#lammps) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### DualSPHysics

Particle-based free-surface flow and fluid-body interaction.

[Source](https://github.com/DualSPHysics/DualSPHysics) · [Documentation](https://dual.sphysics.org/) · [License](https://github.com/DualSPHysics/DualSPHysics#license)

**Terms:** LGPL-2.1. CPU or CUDA builds; runtime depends strongly on particle count and duration. The case generator GenCase is a separately licensed binary-only helper; the example retrieves it and preserves its own terms.

**Literature:** [DualSPHysics: Open-source parallel CFD solver based on Smoothed Particle Hydrodynamics (SPH) (2015)](bibliography.md#dualsphysics)

**Walkthrough:** [DualSPHysics](reproductions/dualsphysics.md) — Executed adaptation

**Research construction route:** [DualSPHysics: Open-source parallel CFD solver based on Smoothed Particle Hydrodynamics (SPH)](research/multiphysics.md#dualsphysics) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

## Finance

### QuantLib

Derivative pricing; stochastic processes and Monte Carlo.

[Source](https://github.com/lballabio/QuantLib) · [Documentation](https://www.quantlib.org/docs.shtml) · [License](https://github.com/lballabio/QuantLib/blob/master/LICENSE.TXT)

**Terms:** BSD-3-Clause. Synthetic example needs no market-data subscription; real curves and prices have separate terms.

**Literature:** [The Pricing of Options and Corporate Liabilities (1973)](bibliography.md#black-scholes)

**Walkthrough:** [European option pricing](examples/cpu-walkthroughs.md#option-pricing) — Executed adaptation

**Research construction route:** [The Pricing of Options and Corporate Liabilities](research/finance-economics.md#quantlib) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### ABIDES

Agent-based limit-order-book market simulation.

[Source](https://github.com/abides-sim/abides) · [Documentation](https://github.com/abides-sim/abides/wiki) · [License](https://github.com/abides-sim/abides/blob/master/LICENSE.txt)

**Terms:** BSD-3-Clause. Original repository uses an old Python stack. The separate JPMorgan ABIDES-Gym repository is archived as checked 2026-11-15.

**Literature:** [ABIDES Towards High-Fidelity Multi-Agent Market Simulation (2020)](bibliography.md#abides)

**Walkthrough:** [Market microstructure](examples/markets.md) — Upstream instructions checked; not run

**Research construction route:** [ABIDES: Towards High-Fidelity Market Simulation for AI Research](research/finance-economics.md#abides) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### FinRL

Financial reinforcement-learning environments and backtests.

[Source](https://github.com/AI4Finance-Foundation/FinRL) · [Documentation](https://finrl.readthedocs.io/) · [License](https://github.com/AI4Finance-Foundation/FinRL#license)

**Terms:** MIT. Training and backtesting platform; historical data access and out-of-sample evaluation are separate tasks.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Deep reinforcement learning for automated stock trading: an ensemble strategy](research/finance-economics.md#finrl) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Open Source Risk Engine

Portfolio scenarios; exposure and risk calculations.

[Source](https://github.com/OpenSourceRisk/Engine) · [Documentation](https://www.opensourcerisk.org/documentation/) · [License](https://github.com/OpenSourceRisk/Engine/blob/master/license.txt)

**Terms:** BSD-3-Clause. QuantLib-based; use bundled example markets before connecting licensed market data.

**Literature:** [Computing the impact of central clearing on systemic risk (2024)](bibliography.md#replication-engine)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Computing the impact of central clearing on systemic risk](research/finance-economics.md#engine) — attempted blocked. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

## Economics and policy

### HARK / Econ-ARK

Heterogeneous-household choice and simulation.

[Source](https://github.com/econ-ark/HARK) · [Documentation](https://docs.econ-ark.org/) · [License](https://github.com/econ-ark/HARK#license)

**Terms:** Apache-2.0. Current HARK example differs from the historical REMARK environment; see the authors' reproduction route.

**Literature:** [Buffer-Stock Saving and the Life Cycle/Permanent Income Hypothesis (1997)](bibliography.md#carroll1997)

**Walkthrough:** [Household saving baseline](examples/cpu-walkthroughs.md#household-saving) — Executed adaptation; [Carroll author-associated HARK replication: executed with failed strict table comparison](reproductions/hark.md) — Author code executed; see paper comparison

**Research construction route:** [Buffer-Stock Saving and the Life Cycle/Permanent Income Hypothesis](research/finance-economics.md#hark) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### QuantEcon.py

Markov chains; dynamic programming and economic computation.

[Source](https://github.com/QuantEcon/QuantEcon.py) · [Documentation](https://quanteconpy.readthedocs.io/en/latest/) · [License](https://github.com/QuantEcon/QuantEcon.py#license)

**Terms:** MIT. Supporting numerical library and lectures; choose and identify a specific economic model.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Uninsured Idiosyncratic Risk and Aggregate Saving](research/finance-economics.md#quantecon) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### OG-Core

Overlapping-generations equilibrium and fiscal-policy models.

[Source](https://github.com/PSLmodels/OG-Core) · [Documentation](https://pslmodels.github.io/OG-Core/) · [License](https://github.com/PSLmodels/OG-Core#license)

**Terms:** CC0-1.0. CC0 dedication; country calibrations and tax functions are separate inputs.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Integrating Microsimulation Models of Tax Policy into a DGE Macroeconomic Model](research/finance-economics.md#og-core) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Tax-Calculator

U.S. income and payroll-tax microsimulation.

[Source](https://github.com/PSLmodels/Tax-Calculator) · [Documentation](https://taxcalc.pslmodels.org/) · [License](https://github.com/PSLmodels/Tax-Calculator/blob/master/LICENSE)

**Terms:** CC0-1.0. Use allowed public-use inputs; code access does not supply restricted tax records or establish current-law accuracy.

**Literature:** [Integrating Microsimulation Models of Tax Policy into a DGE Macroeconomic Model (2019)](bibliography.md#replication-tax-calculator)

**Walkthrough:** [TaxFuncIntegr: fresh macro steady states from public fitted inputs](reproductions/tax-calculator.md) — Author code executed; see paper comparison

**Research construction route:** [Integrating Microsimulation Models of Tax Policy into a DGE Macroeconomic Model](research/finance-economics.md#tax-calculator) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### OpenFisca

Tax-benefit microsimulation from rules and household inputs.

[Source](https://github.com/openfisca/openfisca-core) · [Documentation](https://openfisca.org/doc/) · [License](https://github.com/openfisca/openfisca-core#license)

**Terms:** AGPL-3.0. Core engine; install the appropriate country package and pin the legislation period.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [How does targeted cash assistance affect incentives to work?](research/finance-economics.md#openfisca-core) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Dynare

Dynamic stochastic general equilibrium and related macroeconomic models.

[Source](https://git.dynare.org/Dynare/dynare) · [Documentation](https://www.dynare.org/manual/) · [License](https://www.dynare.org/)

**Terms:** GPL-3.0-or-later for most source; component notices. Use GNU Octave for an open runtime; MATLAB is an optional proprietary alternative. Pin .mod file and calibration.

**Literature:** [Shocks and Frictions in US Business Cycles: A Bayesian DSGE Approach (2007)](bibliography.md#replication-dynare)

**Walkthrough:** [Smets–Wouters maintained model: fresh mode evaluation and shock decomposition](reproductions/dynare.md) — Executed adaptation

**Research construction route:** [Shocks and Frictions in US Business Cycles: A Bayesian DSGE Approach](research/finance-economics.md#dynare) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; official docs available.

## Agents and operations

### Mesa

Python agent-based models and batch experiments.

[Source](https://github.com/mesa/mesa) · [Documentation](https://mesa.readthedocs.io/) · [License](https://github.com/mesa/mesa#license)

**Terms:** Apache-2.0. Software paper verified; a specific published application still needs selection.

**Literature:** [Mesa 3: Agent-based modeling with Python in 2025 (2025)](bibliography.md#mesa)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Mesa 3: Agent-based modeling with Python in 2025](research/agents-operations.md#mesa) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Agents.jl

Agent-based modeling in Julia.

[Source](https://github.com/JuliaDynamics/Agents.jl) · [Documentation](https://juliadynamics.github.io/Agents.jl/stable/) · [License](https://github.com/JuliaDynamics/Agents.jl#license)

**Terms:** MIT. Julia environment; preserve agent activation and random-number settings.

**Literature:** [Agents.jl: a performant and feature-full agent-based modeling software of minimal code complexity (2022)](bibliography.md#agentsjl)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Agents.jl: a performant and feature-full agent-based modeling software of minimal code complexity](research/agents-operations.md#agents) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### NetLogo

Interactive agent-based models and experiment sweeps.

[Source](https://github.com/NetLogo/NetLogo) · [Documentation](https://docs.netlogo.org/) · [License](https://github.com/NetLogo/NetLogo#license)

**Terms:** GPL-2.0. Engine license does not cover every Models Library entry. ViNoS requires its own archived model.

**Literature:** [Viable North Sea (ViNoS): A NetLogo Agent-based Model of German Small-scale Fisheries (2024)](bibliography.md#vinos)

**Walkthrough:** [Fisheries and policy](examples/fisheries.md) — Upstream instructions checked; not run

**Research construction route:** [Viable North Sea (ViNoS): A NetLogo Agent-based Model of German Small-scale Fisheries](research/agents-operations.md#netlogo) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### GAMA

Spatial agent-based models with geographic inputs.

[Source](https://github.com/gama-platform/gama) · [Documentation](https://gama-platform.org/wiki/Home) · [License](https://github.com/gama-platform/gama#license)

**Terms:** GPL-3.0. GIS inputs and scenario models have separate terms.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Participatory Modeling and Simulation with the GAMA Platform](research/agents-operations.md#gama) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Ciw

Queueing-network discrete-event simulation.

[Source](https://github.com/CiwPython/Ciw) · [Documentation](https://ciw.readthedocs.io/) · [License](https://github.com/CiwPython/Ciw#license)

**Terms:** MIT. CPU; arrival; service; blocking and queue disciplines must match the research model.

**Literature:** [Ciw: An open-source discrete event simulation library (2018)](bibliography.md#ciw); [Improving the usability of open health service delivery simulation models using Python and web apps (2023)](bibliography.md#simpy-service)

**Walkthrough:** [Service queues and staffing](examples/queues.md) — Upstream instructions checked; not run

**Research construction route:** [Improving the usability of open health service delivery simulation models using Python and web apps](research/agents-operations.md#ciw) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### simmer

Trajectory-based discrete-event simulation in R.

[Source](https://github.com/r-simmer/simmer) · [Documentation](https://r-simmer.org/) · [License](https://github.com/r-simmer/simmer#license)

**Terms:** GPL-2.0. Keep R package versions and replication seeds.

**Literature:** [simmer: Discrete-Event Simulation for R (2019)](bibliography.md#simmer)

**Walkthrough:** [The published M/M/1 queue and its replication interval](reproductions/simmer.md) — Selected paper target compared; human review pending

**Research construction route:** [simmer: Discrete-Event Simulation for R](research/agents-operations.md#simmer) — reproduced target. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### SimPy

Process-based discrete-event simulation in Python.

[Source](https://gitlab.com/team-simpy/simpy) · [Documentation](https://simpy.readthedocs.io/) · [License](https://simpy.readthedocs.io/en/latest/)

**Terms:** MIT. CPU; service-system models must preserve warm-up; replications and random streams.

**Literature:** [Improving the usability of open health service delivery simulation models using Python and web apps (2023)](bibliography.md#simpy-service)

**Walkthrough:** [Service queues and staffing](examples/queues.md) — Upstream instructions checked; not run

**Research construction route:** [Improving the usability of open health service delivery simulation models using Python and web apps](research/agents-operations.md#simpy) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; official docs available.

## Energy and infrastructure

### PyPSA

Power flow; dispatch and energy-system optimization.

[Source](https://github.com/PyPSA/PyPSA) · [Documentation](https://docs.pypsa.org/) · [License](https://github.com/PyPSA/PyPSA#license)

**Terms:** MIT. Current core is MIT; historical releases used GPL. Use an open solver such as HiGHS when needed.

**Literature:** [PyPSA: Python for Power System Analysis (2018)](bibliography.md#pypsa); [PyPSA-Eur: An open optimisation model of the European transmission system (2018)](bibliography.md#pypsa-eur)

**Walkthrough:** [European energy network optimization](examples/energy.md) — Upstream instructions checked; not run

**Research construction route:** [PyPSA-Eur: An Open Optimisation Model of the European Transmission System](research/energy-natural-sciences.md#pypsa) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### pandapower

Power flow; short circuits and network analysis.

[Source](https://github.com/e2nIEE/pandapower) · [Documentation](https://www.pandapower.org/) · [License](https://github.com/e2nIEE/pandapower/blob/develop/LICENSE)

**Terms:** BSD-3-Clause. Some optional optimization engines have separate licenses; verify network input data.

**Literature:** [Pandapower—An Open-Source Python Tool for Convenient Modeling, Analysis, and Optimization of Electric Power Systems (2018)](bibliography.md#pandapower)

**Walkthrough:** [Published ring-network switching states and full-day comparison](reproductions/pandapower.md) — Author code executed; see paper comparison

**Research construction route:** [Pandapower—An Open-Source Python Tool for Convenient Modeling, Analysis, and Optimization of Electric Power Systems](research/energy-natural-sciences.md#pandapower) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Calliope

Energy-system planning and optimization.

[Source](https://github.com/calliope-project/calliope) · [Documentation](https://calliope.readthedocs.io/) · [License](https://github.com/calliope-project/calliope#license)

**Terms:** Apache-2.0. Optimization model; open and commercial solver backends are distinct choices.

**Literature:** [Calliope: a multi-scale energy systems modelling framework (2018)](bibliography.md#calliope); [Diversity of options to eliminate fossil fuels and reach carbon neutrality across the entire European energy system (2022)](bibliography.md#replication-calliope)

**Walkthrough:** [Archived energy-system metric comparison and verified optimizer blocker](reproductions/calliope.md) — Archived outputs analysed; simulation not rerun

**Research construction route:** [Diversity of options to eliminate fossil fuels and reach carbon neutrality across the entire European energy system](research/energy-natural-sciences.md#calliope) — analysed saved output. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### SUMO

Microscopic multimodal traffic simulation.

[Source](https://github.com/eclipse-sumo/sumo) · [Documentation](https://sumo.dlr.de/docs/) · [License](https://github.com/eclipse-sumo/sumo#license)

**Terms:** EPL-2.0. LuST's published validation used SUMO 0.26; a modern port requires a new comparison.

**Literature:** [Luxembourg SUMO Traffic (LuST) Scenario: Traffic Demand Evaluation (2017)](bibliography.md#lust)

**Walkthrough:** [Historical LuST city-model run with three seeds](reproductions/sumo.md) — Executed adaptation

**Research construction route:** [Luxembourg SUMO Traffic (LuST) Scenario: Traffic Demand Evaluation](research/energy-natural-sciences.md#sumo) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### MATSim

Large-scale agent-based transport demand and mobility.

[Source](https://github.com/matsim-org/matsim-libs) · [Documentation](https://matsim.org/docs/) · [License](https://github.com/matsim-org/matsim-libs/blob/main/matsim/COPYING)

**Terms:** GPL-2.0; see module notices. Java; population and transport-network inputs have separate access and licensing.

**Literature:** [The Multi-Agent Transport Simulation MATSim (2016)](bibliography.md#matsim)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [The Multi-Agent Transport Simulation MATSim](research/agents-operations.md#matsim-libs) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### WNTR

Water-network hydraulics; failures and resilience.

[Source](https://github.com/USEPA/WNTR) · [Documentation](https://usepa.github.io/WNTR/) · [License](https://github.com/USEPA/WNTR/blob/main/LICENSE.md)

**Terms:** BSD-3-Clause. Depends on EPANET and other separately licensed components; network data may be sensitive.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [A software framework for assessing the resilience of drinking water systems to disasters with an example earthquake case study](research/multiphysics.md#wntr) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### EnergyPlus

Building energy; HVAC and water-use simulation.

[Source](https://github.com/NatLabRockies/EnergyPlus) · [Documentation](https://energyplus.readthedocs.io/en/stable/) · [License](https://github.com/NatLabRockies/EnergyPlus/blob/develop/LICENSE.txt)

**Terms:** BSD-style EnergyPlus license with naming clause. Weather files and building descriptions are separate inputs; check design-day and annual-run settings.

**Literature:** [EnergyPlus: creating a new-generation building energy simulation program (2001)](bibliography.md#energyplus)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Analytical and comparative testing of EnergyPlus using IEA HVAC BESTEST E100–E200 test suite](research/energy-natural-sciences.md#energyplus) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

## Environment and natural sciences

### WRF

Numerical weather and atmospheric simulation.

[Source](https://github.com/wrf-model/WRF) · [Documentation](https://www.mmm.ucar.edu/models/wrf) · [License](https://github.com/wrf-model/WRF/blob/master/LICENSE.txt)

**Terms:** UCAR public-domain notice. HPC commonly needed; forcing data; preprocessing and parameterizations are separate dependencies.

**Literature:** See the research construction route below for a candidate paper and its source assessment.

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [A Proposal for the Intercomparison of the Dynamical Cores of Atmospheric General Circulation Models](research/energy-natural-sciences.md#wrf) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### OpenDrift

Lagrangian ocean; atmosphere and particle trajectories.

[Source](https://github.com/OpenDrift/opendrift) · [Documentation](https://opendrift.github.io/) · [License](https://github.com/OpenDrift/opendrift#license)

**Terms:** GPL-2.0. Forecast/reanalysis forcing data can need accounts and can change independently of the code.

**Literature:** [OpenDrift v1.0: a generic framework for trajectory modelling (2018)](bibliography.md#opendrift)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [OpenDrift v1.0: a generic framework for trajectory modelling](research/energy-natural-sciences.md#opendrift) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### COPASI

Biochemical reaction networks; deterministic and stochastic models.

[Source](https://github.com/copasi/COPASI) · [Documentation](https://copasi.org/Support/) · [License](https://github.com/copasi/COPASI#license)

**Terms:** Artistic-2.0. Use published model files and kinetic parameters; no clinical inference from model execution.

**Literature:** [COPASI—a COmplex PAthway SImulator (2006)](bibliography.md#copasi)

**Walkthrough:** No OSRI walkthrough yet; start with the official documentation.

**Research construction route:** [Chaos and birhythmicity in a model for circadian oscillations of the PER and TIM proteins in drosophila](research/energy-natural-sciences.md#copasi) — not run. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Tellurium

Reproducible systems-biology models and simulation experiments.

[Source](https://github.com/sys-bio/tellurium) · [Documentation](https://tellurium.readthedocs.io/) · [License](https://github.com/sys-bio/tellurium#license)

**Terms:** Apache-2.0. SBML; SED-ML and COMBINE workflows; third-party solvers and model licenses remain separate.

**Literature:** [Tellurium notebooks—An environment for reproducible dynamical modeling in systems biology (2018)](bibliography.md#tellurium)

**Walkthrough:** [Tellurium Calzone archive: selected Figure4B Wee1c comparison](reproductions/tellurium.md) — Selected paper target compared; human review pending

**Research construction route:** [Tellurium notebooks—An environment for reproducible dynamical modeling in systems biology](research/energy-natural-sciences.md#tellurium) — reproduced target. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### Brian 2

Spiking neural-network simulation.

[Source](https://github.com/brian-team/brian2) · [Documentation](https://brian2.readthedocs.io/) · [License](https://github.com/brian-team/brian2/blob/master/LICENSE)

**Terms:** CeCILL-2.1. Equation-based models; compilation backend and units need explicit selection.

**Literature:** [Brian 2, an intuitive and efficient neural simulator (2019)](bibliography.md#brian2)

**Walkthrough:** [Historical Brian eye-movement author model with exploratory Figure3 comparison](reproductions/brian2.md) — Author code executed; see paper comparison

**Research construction route:** [Brian 2, an intuitive and efficient neural simulator](research/energy-natural-sciences.md#brian2) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

## Computing and networks

### ns-3

Packet-level network simulation.

[Source](https://github.com/nsnam/ns-3-dev-git) · [Documentation](https://www.nsnam.org/documentation/) · [License](https://github.com/nsnam/ns-3-dev-git/blob/master/LICENSE)

**Terms:** GPL-2.0-only compatible codebase; component notices. GitHub is an upstream-maintained mirror; primary development is on GitLab.

**Literature:** [Unison: A Parallel-Efficient and User-Transparent Network Simulation Kernel (2024)](bibliography.md#replication-ns-3-dev-git)

**Walkthrough:** [Unison: Table 2 and thread determinism](reproductions/ns-3-dev-git.md) — Selected paper target compared; human review pending

**Research construction route:** [Unison: A Parallel-Efficient and User-Transparent Network Simulation Kernel](research/agents-operations.md#ns-3-dev-git) — reproduced target. See the source and comparison assessment.

Source checked 2026-11-15; repository available.

### SimGrid

Distributed-computing and scheduling simulation.

[Source](https://github.com/simgrid/simgrid) · [Documentation](https://simgrid.org/doc/latest/) · [License](https://github.com/simgrid/simgrid/blob/master/COPYING)

**Terms:** LGPL-2.1 core; separate bundled notices. GitHub mirror; simulation platform files need calibration against the hardware being modeled.

**Literature:** [Lowering entry barriers to developing custom simulators of distributed applications and platforms with SimGrid (2025)](bibliography.md#replication-simgrid)

**Walkthrough:** [SimGrid: Figure 13 endpoint workloads](reproductions/simgrid.md) — Author code executed; see paper comparison

**Research construction route:** [Lowering entry barriers to developing custom simulators of distributed applications and platforms with SimGrid](research/agents-operations.md#simgrid) — executed example. See the source and comparison assessment.

Source checked 2026-11-15; repository available.
