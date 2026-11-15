# Multiphysics and water networks: paper-to-code routes

[All 60 tools](README.md) · [How to contribute](../contributing.md)

These are construction routes researched by agents. The execution line reports the bounded work actually performed; the comparison section defines what remains before claiming a published result. Human scientific review is pending.

## elmerfem

**Elmer FEM** — How does basal topography change ice-sheet surface velocity in ISMIP-HOM A010?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for elmerfem

O. Gagliardini; T. Zwinger; F. Gillet-Chaulet; G. Durand; L. Favier; B. de Fleurian; R. Greve; M. Malinen; C. Martín; P. Råback; J. Ruokolainen; M. Sacchettini; M. Schäfer; H. Seddik; J. Thies (2013). [Capabilities and performance of Elmer/Ice, a new-generation ice sheet model](https://doi.org/10.5194/gmd-6-1299-2013). 10.5194/gmd-6-1299-2013.

**Publication type:** journal-article. [Primary metadata](https://api.crossref.org/works/10.5194/gmd-6-1299-2013). Metadata verification: confirmed. Full-text access: Open journal landing page inspected; full numerical benchmark results not extracted.

**Target in the paper:** Gagliardini et al. (2013), ISMIP-HOM validation discussion; current A010 10 km sinusoidal-bed benchmark model. Exact figure/table target still to select.

### Code and inputs for elmerfem

[Artifact or upstream source](https://github.com/ElmerCSC/elmerfem). Official Elmer/Ice model example linked to benchmark family discussed in the software paper; current source is newer than paper.

**Source inspected:** yes. **Ref:** devel. **Commit:** a4082d84aa7aaff25edbb066648428fafc3ebf75.

**Files:** elmerice/examples/ISMIP-HOM/A010/ismip_a.sif; elmerice/examples/ISMIP-HOM/A010/README.text

**Terms:** Elmer components GPL/LGPL; inspect LICENSE.md and solver notices.

**Environment and compute:** ElmerGrid and ElmerSolver with Elmer/Ice solvers; native Linux build or scoped runtime. CPU; Fortran FEM installation and mesh-refinement runs.

**Inputs:** Bundled rectangle.grd and SIF; bed geometry, viscosity, units, boundary conditions preserved.

**Data access:** Public repository inputs; separate component and model terms still apply.

### Construct and compare elmerfem

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` [proposed setup] git clone https://github.com/ElmerCSC/elmerfem.git && cd elmerfem && git checkout a4082d84aa7aaff25edbb066648428fafc3ebf75 ``
2. `` [upstream README] cd elmerice/examples/ISMIP-HOM/A010 && ElmerGrid 1 2 rectangle.grd ``
3. `` [corrected upstream filename] ElmerSolver ismip_a.sif ``

**Expected outputs:** Native mesh/result files and surface velocity field.

**Comparison with the paper:** Compare dimensionless surface-velocity profile to the ISMIP-HOM A 10 km intercomparison data after selecting exact source dataset and tolerance; residual convergence and mesh refinement are additional checks.

**Execution result:** Source and setup inspected; no new execution yet.

**Execution evidence:** None recorded.

**Blockers:** Elmer runtime not provisioned in this research task.; Exact published reference curve/data and tolerance pending.

**Next action:** Retrieve the source benchmark reference data; resolve upstream README typo ismisp_a.sif versus actual ismip_a.sif before running.

**Gaps:** Current code is not the 2013 execution environment.; No published result comparison performed.

### Sources for elmerfem

- [Live title, authors, date, DOI metadata verified.](https://api.crossref.org/works/10.5194/gmd-6-1299-2013) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/ElmerCSC/elmerfem/blob/a4082d84aa7aaff25edbb066648428fafc3ebf75/elmerice/examples/ISMIP-HOM/A010/ismip_a.sif) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/ElmerCSC/elmerfem/blob/a4082d84aa7aaff25edbb066648428fafc3ebf75/elmerice/examples/ISMIP-HOM/A010/README.text) (inspected 2026-11-15).

## calculix

**CalculiX** — How does a pressure pulse expand an elastic tube in partitioned fluid–structure simulation?

**Route:** Software paper example. **Execution:** Not run. **Source confidence:** medium.

### Paper for calculix

Gerasimos Chourdakis; Kyle Davis; Benjamin Rodenberg; Miriam Schulte; Frédéric Simonis; Benjamin Uekermann; Georg Abrams; Hans-Joachim Bungartz; Lucia Cheung Yau; Ishaan Desai; Konrad Eder; Richard Hertrich; Florian Lindner; Alexander Rusch; Dmytro Sashko; David Schneider; Amin Totounferoush; Dominik Volland; Peter Vollmer; Oguz Ziya Koseomur (2022). [preCICE v2: A sustainable and user-friendly coupling library](https://doi.org/10.12688/openreseurope.14445.2). 10.12688/openreseurope.14445.2.

**Publication type:** journal-article. [Primary metadata](https://api.crossref.org/works/10.12688/openreseurope.14445.2). Metadata verification: confirmed. Full-text access: Metadata verified; article result sections not audited.

**Target in the paper:** preCICE v2 software paper; current elastic-tube-3d tutorial is a related authors/maintainers example. No exact published numerical target established.

### Code and inputs for calculix

[Artifact or upstream source](https://github.com/precice/tutorials). Official coupling-project tutorial using CalculiX; software-paper-linked current model, not an asserted paper artifact.

**Source inspected:** yes. **Ref:** develop. **Commit:** a2aab6b46cf556ce1a5187a40d8eb2685634f228.

**Files:** elastic-tube-3d/README.md; elastic-tube-3d/solid-calculix/run.sh; elastic-tube-3d/solid-calculix/tube.inp; elastic-tube-3d/fluid-openfoam/run.sh

**Terms:** Tutorial repository LGPL-3.0; CalculiX GPL-2.0, OpenFOAM and adapters carry own terms.

**Environment and compute:** Compatible pinned preCICE, CalculiX adapter/ccx_preCICE, OpenFOAM adapter and pimpleFoam. CPU; two coupled solver processes, seconds-to-hours depending runtime and mesh.

**Inputs:** Bundled tube mesh, pressure pulse applied for 3 ms then zero for 7 ms, precice-config.xml and solver decks.

**Data access:** Public repository inputs; separate component and model terms still apply.

### Construct and compare calculix

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` [proposed setup] git clone https://github.com/precice/tutorials.git && cd tutorials && git checkout a2aab6b46cf556ce1a5187a40d8eb2685634f228 ``
2. `` [upstream route, terminal 1] cd elastic-tube-3d/fluid-openfoam && ./run.sh ``
3. `` [upstream route, terminal 2] cd elastic-tube-3d/solid-calculix && ./run.sh ``

**Expected outputs:** CalculiX native structural output, OpenFOAM fields, preCICE midpoint displacement logs.

**Comparison with the paper:** Compare midpoint displacement time history to bundled reference-results/fluid-openfoam_solid-calculix.tar.gz; agree tolerance and check coupling/mesh/time-step convergence. This reference is a tutorial baseline, not yet a published target.

**Execution result:** Source and setup inspected; no new execution yet.

**Execution evidence:** None recorded.

**Blockers:** Compatible solver/adapter stack not installed for this task.; Exact article target and paper-era versions not established.

**Next action:** Pin all solver/adaptor versions and inspect the archived tutorial reference before running.

**Gaps:** No exact paper-result correspondence established.

### Sources for calculix

- [Live title, authors, date, DOI metadata verified.](https://api.crossref.org/works/10.12688/openreseurope.14445.2) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/precice/tutorials/blob/a2aab6b46cf556ce1a5187a40d8eb2685634f228/elastic-tube-3d/README.md) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/precice/tutorials/blob/a2aab6b46cf556ce1a5187a40d8eb2685634f228/elastic-tube-3d/solid-calculix/run.sh) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/precice/tutorials/blob/a2aab6b46cf556ce1a5187a40d8eb2685634f228/elastic-tube-3d/solid-calculix/tube.inp) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/precice/tutorials/blob/a2aab6b46cf556ce1a5187a40d8eb2685634f228/elastic-tube-3d/fluid-openfoam/run.sh) (inspected 2026-11-15).

## openmodelica

**OpenModelica** — Can safe Bayesian tuning improve inverter current control while constraining unsafe trajectories?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for openmodelica

Stefan Heid; Daniel Weber; Henrik Bode; Eyke Hüllermeier; Oliver Wallscheid (2020). [OMG: A Scalable and Flexible Simulation and Testing Environment Toolbox for Intelligent Microgrid Control](https://doi.org/10.21105/joss.02435). 10.21105/joss.02435.

**Publication type:** journal-article. [Primary metadata](https://api.crossref.org/works/10.21105/joss.02435). Metadata verification: confirmed. Full-text access: JOSS paper metadata and author README/example inspected; associated arXiv white paper 2005.04869 identified.

**Target in the paper:** Heid et al. (2020) OMG software paper; detailed applied example in associated Bode et al. white paper, safe Bayesian low-level controller tuning. Exact figure/curve comparison pending.

### Code and inputs for openmodelica

[Artifact or upstream source](https://github.com/upb-lea/openmodelica-microgrid-gym). Author-associated OMG project uses OpenModelica as FMU backend and links the JOSS article and white paper.

**Source inspected:** yes. **Ref:** master. **Commit:** a81e522594c4048aa63ae0cfdc2ea4682ca98307.

**Files:** README.rst; examples/single_inverter_current_control_safe_opt.py; docs/parts/user_guide/examples/single_inverter_current_control_safe_opt.rst; setup.py

**Terms:** OMG GPL-3.0; OpenModelica, Modelica libraries, PyFMI and FMU components have separate terms.

**Environment and compute:** Legacy OMG Python environment, PyFMI, OpenModelica/FMU toolchain; use pinned project requirements and package data. CPU; FMU runtime and iterative controller tuning.

**Inputs:** Bundled inverter FMU, network configuration, controller parameters, SafeOpt/GP settings.

**Data access:** Public repository inputs; separate component and model terms still apply.

### Construct and compare openmodelica

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` [proposed setup] git clone https://github.com/upb-lea/openmodelica-microgrid-gym.git && cd openmodelica-microgrid-gym && git checkout a81e522594c4048aa63ae0cfdc2ea4682ca98307 ``
2. `` [proposed setup after matching FMU dependencies] python -m pip install -e . ``
3. `` [upstream example] python examples/single_inverter_current_control_safe_opt.py ``

**Expected outputs:** Controller learning histories and inverter current/control plots.

**Comparison with the paper:** Match source/white-paper system, random seed and tuning budget; compare control error, constraint violations and optimization trace to selected published plot. Numerical target/tolerance awaits detailed white-paper audit.

**Execution result:** Source and setup inspected; no new execution yet.

**Execution evidence:** None recorded.

**Blockers:** Legacy PyFMI/FMUs and Python compatibility need qualification.; No OpenModelica runtime change authorized or made.

**Next action:** Freeze a paper-era release/FMU and extract exact white-paper figure parameters before reproducing.

**Gaps:** Current repository is newer than JOSS paper.; JOSS paper itself presents software; applied results are in associated white paper.

### Sources for openmodelica

- [Live title, authors, date, DOI metadata verified.](https://api.crossref.org/works/10.21105/joss.02435) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/upb-lea/openmodelica-microgrid-gym/blob/a81e522594c4048aa63ae0cfdc2ea4682ca98307/README.rst) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/upb-lea/openmodelica-microgrid-gym/blob/a81e522594c4048aa63ae0cfdc2ea4682ca98307/examples/single_inverter_current_control_safe_opt.py) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/upb-lea/openmodelica-microgrid-gym/blob/a81e522594c4048aa63ae0cfdc2ea4682ca98307/docs/parts/user_guide/examples/single_inverter_current_control_safe_opt.rst) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/upb-lea/openmodelica-microgrid-gym/blob/a81e522594c4048aa63ae0cfdc2ea4682ca98307/setup.py) (inspected 2026-11-15).
- [Author-associated white-paper identity and application scope.](https://arxiv.org/abs/2005.04869) (inspected 2026-11-15).

## pybamm

**PyBaMM** — Can we recover the published DFN constant-current discharge voltage and inspect model states?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** high.

### Paper for pybamm

Valentin Sulzer; Scott G. Marquis; Robert Timms; Martin Robinson; S. Jon Chapman (2021). [Python Battery Mathematical Modelling (PyBaMM)](https://doi.org/10.5334/jors.309). 10.5334/jors.309.

**Publication type:** journal-article. [Primary metadata](https://api.crossref.org/works/10.5334/jors.309). Metadata verification: confirmed. Full-text access: Open article already inspected in lab; live metadata and official DFN source refreshed.

**Target in the paper:** Sulzer et al. (2021), Listing 1; DFN simulation of discharge.

### Code and inputs for pybamm

[Artifact or upstream source](https://github.com/pybamm-team/PyBaMM). Official current DFN example implements the model and simulation construction illustrated in Listing 1; current source includes additional options.

**Source inspected:** yes. **Ref:** main. **Commit:** d90fd464edefdd8de5f0de8941da84a319b699ba.

**Files:** examples/scripts/DFN.py

**Terms:** BSD-3-Clause; parameter-set and external data terms separate.

**Environment and compute:** Existing lab pins pybamm 26.10.1.1; exact 2021 comparison needs paper-era environment and defaults. CPU; small DFN demonstration.

**Inputs:** DFN model, parameter set, current protocol and t_eval preserved explicitly; use paper-era values when claiming reproduction.

**Data access:** Public repository inputs; separate component and model terms still apply.

### Construct and compare pybamm

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` [existing executed adaptation] python simulation-lab/examples/battery_discharge.py --output RUN_DIR ``
2. `` [upstream route after qualifying pinned version] python examples/scripts/DFN.py ``

**Expected outputs:** Voltage-time curve and native model solution; existing lab adaptation emits CSV/JSON.

**Comparison with the paper:** Recreate Listing 1 with matched PyBaMM version/default parameter set, compare voltage-time samples to article figure or archived source run with specified tolerance; current adaptation only confirms execution and model checks.

**Execution result:** Source and setup inspected; no new execution yet.

**Execution evidence:** None recorded.

**Blockers:** Paper-era defaults/environment not yet reconstructed.

**Next action:** Retrieve archived 2021 source/version and the plotted target curve; retain current checked adaptation as separate baseline.

**Gaps:** Four prior lab teaching runs remain adaptations, not paper-result reproductions.

### Sources for pybamm

- [Live title, authors, date, DOI metadata verified.](https://api.crossref.org/works/10.5334/jors.309) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/pybamm-team/PyBaMM/blob/d90fd464edefdd8de5f0de8941da84a319b699ba/examples/scripts/DFN.py) (inspected 2026-11-15).

## openems

**openEMS** — How do cylindrical subgrids change electromagnetic-wave propagation and efficiency?

**Route:** Related tutorial only. **Execution:** Not run. **Source confidence:** medium.

### Paper for openems

Thorsten Liebig; Andreas Rennings; Sebastian Held; Daniel Erni (2012). [openEMS – a free and open source equivalent‐circuit (EC) FDTD simulation platform supporting cylindrical coordinates suitable for the analysis of traveling wave MRI applications](https://doi.org/10.1002/jnm.1875). 10.1002/jnm.1875.

**Publication type:** journal-article. [Primary metadata](https://api.crossref.org/works/10.1002/jnm.1875). Metadata verification: confirmed. Full-text access: Publisher abstract and metadata inspected; full numeric methods/figures not audited.

**Target in the paper:** Liebig et al. paper on cylindrical EC-FDTD; current CylindricalWave_CC.m demonstrates the method family, not the exact traveling-wave MRI geometry.

### Code and inputs for openems

[Artifact or upstream source](https://github.com/thliebig/openEMS). Official author-maintained cylindrical-grid tutorial; exact paper MRI geometry artifact not located.

**Source inspected:** yes. **Ref:** master. **Commit:** 92cd92a8d924c78a93453c25fa541384c2ac1d0e.

**Files:** matlab/Tutorials/CylindricalWave_CC.m; matlab/Tutorials/Rect_Waveguide.m

**Terms:** GPL-3.0; CSXCAD and other runtime component notices apply.

**Environment and compute:** openEMS/CSXCAD and MATLAB or Octave; current source says openEMS 0.37 and Octave 11.3 tested. CPU; FDTD mesh can be substantial.

**Inputs:** Bundled cylindrical mesh and excitation; preserve physical units, nested subgrids, absorbing boundary and convergence criterion.

**Data access:** Public repository inputs; separate component and model terms still apply.

### Construct and compare openems

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` [proposed setup] git clone https://github.com/thliebig/openEMS.git && cd openEMS && git checkout 92cd92a8d924c78a93453c25fa541384c2ac1d0e ``
2. `` [proposed bounded execution] run matlab/Tutorials/CylindricalWave_CC.m from Octave with installed openEMS/CSXCAD paths; stop before the final infinite phase-animation loop ``

**Expected outputs:** XML model, Et_ra VTK field dumps, Ef_ra.h5 complex fields.

**Comparison with the paper:** Use field continuity/refinement and analytic cylindrical-wave comparisons as tutorial checks. To reproduce the article, first obtain exact MRI geometry, dielectric properties and published field/performance targets.

**Execution result:** Source and setup inspected; no new execution yet.

**Execution evidence:** None recorded.

**Blockers:** Paper-specific MRI model not found.; Full paper numeric target not audited.; Source tutorial ends in while 1 animation; batch runner must omit animation and record patch.

**Next action:** Locate author paper archive/model before promoting to paper-result candidate.

**Gaps:** Current tutorial is related to the paper method, not a direct reproduction route.

### Sources for openems

- [Live title, authors, date, DOI metadata verified.](https://api.crossref.org/works/10.1002/jnm.1875) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/thliebig/openEMS/blob/92cd92a8d924c78a93453c25fa541384c2ac1d0e/matlab/Tutorials/CylindricalWave_CC.m) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/thliebig/openEMS/blob/92cd92a8d924c78a93453c25fa541384c2ac1d0e/matlab/Tutorials/Rect_Waveguide.m) (inspected 2026-11-15).

## ngspice

**ngspice** — Can the public AutoCkt ngspice operational-amplifier task recover held-out circuit specifications?

**Route:** Paper result candidate. **Execution:** Not run. **Source confidence:** high.

### Paper for ngspice

Keertana Settaluri; Ameer Haj-Ali; Qijing Huang; Kourosh Hakhamaneshi; Borivoje Nikolic (2020). [AutoCkt: Deep Reinforcement Learning of Analog Circuit Designs](https://doi.org/10.23919/date48585.2020.9116200). 10.23919/date48585.2020.9116200.

**Publication type:** proceedings-article. [Primary metadata](https://api.crossref.org/works/10.23919/date48585.2020.9116200). Metadata verification: confirmed. Full-text access: IEEE/author repository and conference/arXiv primary records inspected; live DOI metadata verified.

**Target in the paper:** Settaluri et al. DATE 2020 AutoCkt, schematic generalization success and design-speed results; public two-stage op-amp task only.

### Code and inputs for ngspice

[Artifact or upstream source](https://github.com/ksettaluri6/AutoCkt). Authors explicitly identify repository as DATE 2020 code and separate ngspice circuits from proprietary Spectre results.

**Source inspected:** yes. **Ref:** master. **Commit:** a6c8a61d3dffb8b433f19251e135994a5b0f6ee4.

**Files:** README.md; environment.yml; autockt/rollout.py; eval_engines/ngspice/ngspice_wrapper.py; eval_engines/ngspice/ngspice_inputs/yaml_files/two_stage_opamp.yaml

**Terms:** AutoCkt repository has no detected LICENSE; do not redistribute until reuse terms clarified. ngspice has separate BSD-based terms; transistor-model rights separate.

**Environment and compute:** Author environment.yml (legacy Python/Ray/TensorFlow), conda; README links ngspice release 27 (spelled 2.7 in text). CPU; README reports 8 cores, warns fewer than 2; training is not a quick smoke test.

**Inputs:** Bundled two-stage op-amp netlist/45nm model, generated training/test specifications; preserve random seeds and CPU-worker allocation.

**Data access:** Public repository inputs; separate component and model terms still apply.

### Construct and compare ngspice

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` [upstream] conda env create -f environment.yml ``
2. `` [upstream] source activate autockt ``
3. `` [upstream] python eval_engines/ngspice/ngspice_inputs/correct_inputs.py ``
4. `` [upstream paper setting] python autockt/gen_specs.py --num_specs 350 ``
5. `` [upstream IPython training] run autockt/val_autobag_ray.py ``
6. `` [upstream validation with explicit user-set counts] run autockt/rollout.py /path/to/ray/checkpoint --run PPO --env opamp-v0 --num_val_specs NUM --traj_len LENGTH --no-render ``

**Expected outputs:** Training checkpoints and opamp_obs_reached_test/opamp_obs_nreached_test pickle files.

**Comparison with the paper:** Measure held-out specification success and runtime against the public ngspice experiment. Article abstract reports at least 96.3% across tested schematic tasks; README explicitly reports seed/test-set variability of 80%-96% and an example 938/1000, so do not require a single exact success fraction without matching seeds/data.

**Execution result:** Source and setup inspected; no new execution yet.

**Execution evidence:** None recorded.

**Blockers:** Legacy dependencies; exact paper seeds/spec sets and training hyperparameters need extraction.; Author-code redistribution license absent.; Proprietary Spectre/BAG technology results cannot be reproduced using only public ngspice artifact.

**Next action:** Qualify a container/environment without changing host baseline; run public circuit validation and retain all seeds and test specs.

**Gaps:** No public-code license detected; linking/inspection only.; README writes checkpoints under home by default; configure Ray output to /workspace before execution.

### Sources for ngspice

- [Live title, authors, date, DOI metadata verified.](https://api.crossref.org/works/10.23919/date48585.2020.9116200) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/ksettaluri6/AutoCkt/blob/a6c8a61d3dffb8b433f19251e135994a5b0f6ee4/README.md) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/ksettaluri6/AutoCkt/blob/a6c8a61d3dffb8b433f19251e135994a5b0f6ee4/environment.yml) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/ksettaluri6/AutoCkt/blob/a6c8a61d3dffb8b433f19251e135994a5b0f6ee4/autockt/rollout.py) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/ksettaluri6/AutoCkt/blob/a6c8a61d3dffb8b433f19251e135994a5b0f6ee4/eval_engines/ngspice/ngspice_wrapper.py) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/ksettaluri6/AutoCkt/blob/a6c8a61d3dffb8b433f19251e135994a5b0f6ee4/eval_engines/ngspice/ngspice_inputs/yaml_files/two_stage_opamp.yaml) (inspected 2026-11-15).

## cantera

**Cantera** — How does a real-gas equation of state change n-dodecane shock-tube ignition delay?

**Route:** Paper model adaptation. **Execution:** Example executed. **Source confidence:** high.

### Paper for cantera

Gandhali Kogekar; Canan Karakaya; Gary J. Liskovich; Matthew A. Oehlschlaeger; Steven C. DeCaluwe; Robert J. Kee (2018). [Impact of non-ideal behavior on ignition delay and chemical kinetics in high-pressure shock tube reactors](https://doi.org/10.1016/j.combustflame.2017.10.014). 10.1016/j.combustflame.2017.10.014.

**Publication type:** journal-article. [Primary metadata](https://api.crossref.org/works/10.1016/j.combustflame.2017.10.014). Metadata verification: confirmed. Full-text access: Official full HTML example read, including references and tabulated printed results; primary article metadata verified.

**Target in the paper:** Kogekar et al. (2018), real-gas shock-tube ignition delays; official non_ideal_shock_tube.py follows method using Wang et al. reduced mechanism. It is a later implementation, not exact paper code.

### Code and inputs for cantera

[Artifact or upstream source](https://github.com/Cantera/cantera). Official Cantera v3.2.0 example explicitly cites the application paper; exact example executed. It uses a representative reduced mechanism, so article-exact reproduction remains separate.

**Source inspected:** yes. **Ref:** v3.2.0. **Commit:** 4a8358eb80cfeb50474386b5f9ec0b3a83519889.

**Files:** samples/python/reactors/non_ideal_shock_tube.py; data/nDodecane_Reitz.yaml

**Terms:** Cantera BSD-3-Clause; bundled mechanism source/references must be preserved.

**Environment and compute:** Executed Python3.12.16 with cantera3.2.0, numpy2.5.4, matplotlib3.11.2; full environment captured in requirements-tested.txt. CPU; documentation reports roughly 98 seconds full script.

**Inputs:** Stoichiometric n-dodecane/O2/N2 at 1000 K and 40 atm; nDodecane_Reitz.yaml phases nDodecane_RK and nDodecane_IG; OH mass-fraction peak defines ignition delay.

**Data access:** Public repository inputs; separate component and model terms still apply.

### Construct and compare cantera

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` [tested isolated setup] python -m venv VENV && VENV/bin/python -m pip install cantera==3.2.0 numpy matplotlib ``
2. `` [executed harness] From a directory containing the pinned script as upstream.py and source.json: MPLBACKEND=Agg VENV/bin/python ../run_harness.py; harness executes upstream.py unchanged, exports sweep CSV and saves existing figures. ``
3. `` [direct source route, numerical code tested via harness] MPLBACKEND=Agg VENV/bin/python upstream.py ``

**Expected outputs:** Printed ignition delays and ideal/real-gas profile plus temperature-sweep plots; harness should serialize curves/figures because upstream only displays them.

**Comparison with the paper:** First recover official example baseline (3.2 docs print real-gas 4.093e-4 s at 1000 K, 40 atm). Then match actual article oxygen concentrations, mechanism and full experiment settings before comparing published shock-tube curves; tutorial air ratio may differ from article experiments.

**Execution result:** Official Cantera v3.2.0 script ran unchanged under a logging/plot-export harness. At 1000 K and 40 atm, real-gas ignition delay=0.0004092691037528133 s and ideal-gas delay=0.00043326392307736766 s; real-gas value matches documented 4.093e-4 s within the declared 0.2% example tolerance. Both 16-point temperature sweeps finite and positive. This checks official example output, not a paper figure.

**Execution evidence:** [Run receipt](verification/cantera.json); [Numeric output](verification/cantera-temperature-sweep.csv)

**Blockers:** Article-exact input/mechanism and target curve require full-text comparison.

**Next action:** Run official version-pinned example, retain mechanism hash and compare its own documented baseline; then derive paper-target experiment independently.

**Gaps:** Official example explicitly chooses a representative mechanism; it is not claimed to be authors exact 2018 artifact.

### Sources for cantera

- [Live title, authors, date, DOI metadata verified.](https://api.crossref.org/works/10.1016/j.combustflame.2017.10.014) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/Cantera/cantera/blob/25c1ab1c397e2991c77560b1ad5154919a12c733/samples/python/reactors/non_ideal_shock_tube.py) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/Cantera/cantera/blob/25c1ab1c397e2991c77560b1ad5154919a12c733/data/nDodecane_Reitz.yaml) (inspected 2026-11-15).
- [Full official model setup, OH-peak definition, printed baseline and linked paper.](https://cantera.org/stable/examples/python/reactors/non_ideal_shock_tube.html) (inspected 2026-11-15).
- [Exact v3.2.0 upstream script downloaded, inspected, hashed and executed unchanged.](https://github.com/Cantera/cantera/blob/4a8358eb80cfeb50474386b5f9ec0b3a83519889/samples/python/reactors/non_ideal_shock_tube.py) (inspected 2026-11-15).

## lammps

**LAMMPS** — How does a Lennard-Jones solid melt and equilibrate in a particle simulation?

**Route:** Software paper example. **Execution:** Not run. **Source confidence:** medium.

### Paper for lammps

Aidan P. Thompson; H. Metin Aktulga; Richard Berger; Dan S. Bolintineanu; W. Michael Brown; Paul S. Crozier; Pieter J. in 't Veld; Axel Kohlmeyer; Stan G. Moore; Trung Dac Nguyen; Ray Shan; Mark J. Stevens; Julien Tranchida; Christian Trott; Steven J. Plimpton (2022). [LAMMPS - a flexible simulation tool for particle-based materials modeling at the atomic, meso, and continuum scales](https://doi.org/10.1016/j.cpc.2021.108171). 10.1016/j.cpc.2021.108171.

**Publication type:** journal-article. [Primary metadata](https://api.crossref.org/works/10.1016/j.cpc.2021.108171). Metadata verification: confirmed. Full-text access: Live software-paper metadata verified; official example input and README inspected; applied result figure not established.

**Target in the paper:** Thompson et al. (2022) LAMMPS software overview; official examples/melt is a teaching demonstration. No exact article figure/table linkage established.

### Code and inputs for lammps

[Artifact or upstream source](https://github.com/lammps/lammps). Official software example supplied by LAMMPS maintainers; demonstrates the software-paper model class, not an identified published application.

**Source inspected:** yes. **Ref:** develop. **Commit:** 713cd85974ef9697063f039155563ff722653fe7.

**Files:** examples/melt/in.melt; examples/README

**Terms:** GPL-2.0; potential/input-specific terms separate.

**Environment and compute:** Pinned LAMMPS CPU executable with LJ pair style; preserve build options and numeric precision. CPU; small serial LJ demonstration.

**Inputs:** Bundled LJ reduced-unit FCC solid, random velocity seed 87287, NVE integration, thermo output every 50 steps, 250 steps by default.

**Data access:** Public repository inputs; separate component and model terms still apply.

### Construct and compare lammps

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` [proposed setup] git clone https://github.com/lammps/lammps.git && cd lammps && git checkout 713cd85974ef9697063f039155563ff722653fe7 ``
2. `` [upstream invocation form] cd examples/melt && lmp -in in.melt ``

**Expected outputs:** log.lammps thermodynamic history; optional trajectory dumps only if enabled.

**Comparison with the paper:** Verify recorded thermo output, energy/temperature trends and step count against same-version reference logs; for a genuine article reproduction select a published potential/model dataset and exact observable rather than claiming melt example reproduces the overview.

**Execution result:** Source and setup inspected; no new execution yet.

**Execution evidence:** None recorded.

**Blockers:** No applied paper-result artifact selected yet.; LAMMPS executable not installed/qualified for this task.

**Next action:** Use this as a runnable tutorial scaffold; select an author-associated application artifact before promoting to reproduction.

**Gaps:** The 2022 software citation is not evidence that this input reproduces a published scientific figure.

### Sources for lammps

- [Live title, authors, date, DOI metadata verified.](https://api.crossref.org/works/10.1016/j.cpc.2021.108171) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/lammps/lammps/blob/713cd85974ef9697063f039155563ff722653fe7/examples/melt/in.melt) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/lammps/lammps/blob/713cd85974ef9697063f039155563ff722653fe7/examples/README) (inspected 2026-11-15).

## dualsphysics

**DualSPHysics** — Can a 2D dam-break front match published experimental tip-position data?

**Route:** Paper result candidate. **Execution:** Not run. **Source confidence:** high.

### Paper for dualsphysics

A.J.C. Crespo; J.M. Domínguez; B.D. Rogers; M. Gómez-Gesteira; S. Longshaw; R. Canelas; R. Vacondio; A. Barreiro; O. García-Feal (2015). [DualSPHysics: Open-source parallel CFD solver based on Smoothed Particle Hydrodynamics (SPH)](https://doi.org/10.1016/j.cpc.2014.10.004). 10.1016/j.cpc.2014.10.004.

**Publication type:** journal-article. [Primary metadata](https://api.crossref.org/works/10.1016/j.cpc.2014.10.004). Metadata verification: confirmed. Full-text access: Crespo software-paper metadata verified; Koshizuka/Oka benchmark metadata also verified; official wiki explains exact validation case.

**Target in the paper:** Crespo et al. (2015) software validation route, with direct experimental benchmark: Koshizuka and Oka (1996), Moving-Particle Semi-Implicit Method for Fragmentation of Incompressible Fluid, DOI10.13182/NSE96-A24205. Exact paper figure locator still to audit.

### Code and inputs for dualsphysics

[Artifact or upstream source](https://github.com/DualSPHysics/DualSPHysics). Official dam-break validation case bundles experimental nondimensional dam-front positions and references the 1996 experiment.

**Source inspected:** yes. **Ref:** master. **Commit:** ef3721a861fda961f0e2f9ec4cd317b19de99086.

**Files:** examples/main/01_DamBreak/CaseDambreakVal2D_Def.xml; examples/main/01_DamBreak/xCaseDambreakVal2D_linux64_CPU.sh; examples/main/01_DamBreak/EXP_X-DamTipPosition_Koshizula&Oka1996.txt

**Terms:** LGPL-2.1 solver; verify bundled validation-data attribution and auxiliary binary terms.

**Environment and compute:** Complete compatible DualSPHysics release: GenCase, CPU solver, postprocessors; Linux CPU script. CPU supported; cost depends on particle resolution.

**Inputs:** CaseDambreakVal2D_Def.xml and experimental tip-position text; preserve particle spacing, gravity, geometry, pressure treatment and output cadence.

**Data access:** Public repository inputs; separate component and model terms still apply.

### Construct and compare dualsphysics

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` [upstream CPU route] cd examples/main/01_DamBreak && bash xCaseDambreakVal2D_linux64_CPU.sh ``

**Expected outputs:** Particle output, postprocessed dam-front position versus time, comparison plot against bundled experiment.

**Comparison with the paper:** Compare normalized tip position at all bundled experimental times using interpolation, report RMSE/max error and particle-resolution convergence; choose numerical tolerance after reading benchmark uncertainty, not merely visually matching snapshots.

**Execution result:** Source and setup inspected; no new execution yet.

**Execution evidence:** None recorded.

**Blockers:** Complete matching binaries and dependencies not provisioned.; Published figure locator and experimental uncertainty/tolerance still pending.

**Next action:** Read original benchmark methods/figure, qualify complete release, run CPU script and compare exported time series to bundled experimental coordinates.

**Gaps:** Current code differs from 2015 release.; Experimental data-file presence is not itself reproduction.

### Sources for dualsphysics

- [Live title, authors, date, DOI metadata verified.](https://api.crossref.org/works/10.1016/j.cpc.2014.10.004) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/DualSPHysics/DualSPHysics/blob/ef3721a861fda961f0e2f9ec4cd317b19de99086/examples/main/01_DamBreak/CaseDambreakVal2D_Def.xml) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/DualSPHysics/DualSPHysics/blob/ef3721a861fda961f0e2f9ec4cd317b19de99086/examples/main/01_DamBreak/xCaseDambreakVal2D_linux64_CPU.sh) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/DualSPHysics/DualSPHysics/blob/ef3721a861fda961f0e2f9ec4cd317b19de99086/examples/main/01_DamBreak/EXP_X-DamTipPosition_Koshizula&Oka1996.txt) (inspected 2026-11-15).
- [Original experimental benchmark metadata verified.](https://api.crossref.org/works/10.13182/NSE96-A24205) (inspected 2026-11-15).
- [Official documentation identifies dam-break validation with Koshizuka and Oka data.](https://github.com/DualSPHysics/DualSPHysics/wiki/7.-Testcases) (inspected 2026-11-15).

## wntr

**WNTR** — How does repairing the largest earthquake-induced leaks change water-service availability?

**Route:** Paper model adaptation. **Execution:** Example executed. **Source confidence:** high.

### Paper for wntr

Katherine A. Klise; Michael Bynum; Dylan Moriarty; Regan Murray (2017). [A software framework for assessing the resilience of drinking water systems to disasters with an example earthquake case study](https://doi.org/10.1016/j.envsoft.2017.06.022). 10.1016/j.envsoft.2017.06.022.

**Publication type:** journal-article. [Primary metadata](https://api.crossref.org/works/10.1016/j.envsoft.2017.06.022). Metadata verification: confirmed. Full-text access: Primary article abstract/metadata and full current official earthquake notebook inspected.

**Target in the paper:** Klise et al. (2017), example earthquake case study. Current earthquake_tutorial.ipynb implements magnitude-6.5 event, partial repair, pressure/WSA/population metrics, but is not established as exact 2017 case.

### Code and inputs for wntr

[Artifact or upstream source](https://github.com/USEPA/WNTR). Official EPA WNTR example for the same earthquake-resilience method family; exact paper-era case settings not established.

**Source inspected:** yes. **Ref:** main. **Commit:** 39e6b34f37d4b2d074f107d822752c989bf108aa.

**Files:** examples/earthquake_tutorial.ipynb; examples/networks/Net3.inp; documentation/disaster_models.rst

**Terms:** WNTR BSD-3-Clause; EPANET and bundled network/model notices apply.

**Environment and compute:** Executed Python3.12.16 with wntr1.4.0, numpy2.5.4, pandas3.1.1, scipy1.18.1, matplotlib3.11.2 and six1.17.0; full environment captured. CPU; small network, two 24-hour hydraulic runs.

**Inputs:** Bundled Net3 network, seed12345, epicenter(32000,15000)m, depth10000m, magnitude6.5, 24h simulation, leaks start5h and 4 largest repaired15h, PDD pressure limits3.52/14.06m.

**Data access:** Public repository inputs; separate component and model terms still apply.

### Construct and compare wntr

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` [tested isolated setup] python -m venv VENV && VENV/bin/python -m pip install wntr==1.4.0 matplotlib scipy six ``
2. `` [executed extraction] Concatenate every code cell of examples/earthquake_tutorial.ipynb in source order without numerical edits; keep networks/Net3.inp beside the script. ``
3. `` [executed harness] From notebook examples directory: MPLBACKEND=Agg VENV/bin/python ../run_harness.py; executes extracted upstream.py unchanged and saves existing plots. ``

**Expected outputs:** earthquake_people_impacted.csv and earthquake_people_impacted_wrepair.csv; pressure/WSA/affected-population plots.

**Comparison with the paper:** Compare no-repair and repair time series against same-version repository regression fixtures first; for paper reproduction recover exact 2017 network, fragility curves and realizations and compare corresponding published metric/figure.

**Execution result:** All current official earthquake notebook code cells executed without numerical edits. Both 25x108 population-impacted CSV arrays exactly match current upstream regression fixtures (maximum absolute difference 0). 16 damaged pipes, 4 repaired after 15 h. Missing six dependency found on first attempt and installed only in isolated venv; failed attempt retained. This reproduces current upstream fixtures, not an established 2017 paper result.

**Execution evidence:** [Run receipt](verification/wntr.json); [Numeric output](verification/wntr-earthquake_people_impacted.csv); [Numeric output](verification/wntr-earthquake_people_impacted_wrepair.csv)

**Blockers:** Paper-era input and figure mapping not yet audited.

**Next action:** Execute current upstream notebook, compare existing regression fixture within stated numeric tolerance, then retrieve paper-specific scenario.

**Gaps:** Running current earthquake tutorial does not establish reproduction of 2017 earthquake case.; Published wheel omitted six as an installed dependency in this environment; adding six resolved the import failure.

### Sources for wntr

- [Live title, authors, date, DOI metadata verified.](https://api.crossref.org/works/10.1016/j.envsoft.2017.06.022) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/USEPA/WNTR/blob/39e6b34f37d4b2d074f107d822752c989bf108aa/examples/earthquake_tutorial.ipynb) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/USEPA/WNTR/blob/39e6b34f37d4b2d074f107d822752c989bf108aa/examples/networks/Net3.inp) (inspected 2026-11-15).
- [Exact source file inspected for model, inputs, or invocation.](https://github.com/USEPA/WNTR/blob/39e6b34f37d4b2d074f107d822752c989bf108aa/documentation/disaster_models.rst) (inspected 2026-11-15).
- [Current upstream fixture compared against actual numerical output; exact equality of all 2700 values.](https://github.com/USEPA/WNTR/blob/39e6b34f37d4b2d074f107d822752c989bf108aa/wntr/tests/data_for_testing/earthquake_people_impacted.csv) (inspected 2026-11-15).
- [Current upstream fixture compared against actual numerical output; exact equality of all 2700 values.](https://github.com/USEPA/WNTR/blob/39e6b34f37d4b2d074f107d822752c989bf108aa/wntr/tests/data_for_testing/earthquake_people_impacted_wrepair.csv) (inspected 2026-11-15).
