# Robotics, finite elements, and fluid dynamics: paper-to-code routes

[All 60 tools](README.md) · [How to contribute](../contributing.md)

These are construction routes researched by agents. The execution line reports the bounded work actually performed; the comparison section defines what remains before claiming a published result. Human scientific review is pending.

## drake

**Drake** — Can energy shaping swing up and balance a two-link underactuated acrobot?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for drake

Mark W. Spong (1994). [Swing up control of the Acrobot](https://doi.org/10.1109/ROBOT.1994.350934). 10.1109/ROBOT.1994.350934.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ROBOT.1994.350934?fields=title,authors,year,externalIds,url,openAccessPdf). Metadata verification: confirmed. Full-text access: Metadata verified through Semantic Scholar API; original ICRA paper full text not inspected. IEEE page requires browser challenge.

**Target in the paper:** Acrobot swing-up model and controller; Drake spong_controller.h explicitly cites this 1994 paper.

### Code and inputs for drake

[Artifact or upstream source](https://github.com/RobotLocomotion/drake). Official Drake implementation explicitly cites Spong 1994; it adds an LQR balancing phase and saturation, so it is a model adaptation rather than archived author experiment code.

**Source inspected:** yes. **Ref:** master. **Commit:** 9977d90894fe487195e9ac95a93ca4330a6ae81b.

**Files:** examples/acrobot/spong_controller.h; examples/acrobot/run_swing_up.cc; examples/acrobot/README.md

**Terms:** BSD-3-Clause core; third-party components separate

**Environment and compute:** Pinned Drake source and documented Bazel toolchain; use CPU simulator. A Python Drake wheel is an alternative only after binding coverage is checked. Small CPU dynamics example; a source build is substantially heavier than the simulation.

**Inputs:** Default AcrobotParams and SpongControllerParams; initial state from run_swing_up.cc; record integration and controller settings.

**Data access:** No external dataset; robot parameters are in source.

### Construct and compare drake

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Upstream README command, after building pinned Drake: ``
2. `` bazel run //examples/acrobot:run_swing_up ``

**Expected outputs:** Acrobot state and control trajectory; upstream executable publishes LCM visualization. Add an explicitly documented state/torque logger for quantitative comparison.

**Comparison with the paper:** Compare upright angle error, energy, elbow torque and swing-up/settling time against the original paper after full-text extraction. Do not infer reproduction from an animation.

**Execution result:** Source and instructions inspected; no local execution or paper-result claim.

**Execution evidence:** None recorded.

**Blockers:** Original paper figure targets and tolerances have not been extracted; LQR switching and torque saturation may differ from paper.

**Next action:** Retrieve original 1994 paper, map model/controller equations and initial state, then record a numerical trajectory from the pinned controller.

**Gaps:** 1994 full text needed for exact figure/table target and matched initial conditions.; Author-hosted ICRA94.pdf was located but returned HTTP403; original paper remains unread.

### Sources for drake

- [Explicit paper citation and controller implementation](https://raw.githubusercontent.com/RobotLocomotion/drake/9977d90894fe487195e9ac95a93ca4330a6ae81b/examples/acrobot/spong_controller.h) (inspected 2026-11-15).
- [Upstream run command and hybrid-controller description](https://github.com/RobotLocomotion/drake/blob/9977d90894fe487195e9ac95a93ca4330a6ae81b/examples/acrobot/README.md) (inspected 2026-11-15).
- [Live paper identity metadata](https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ROBOT.1994.350934?fields=title,authors,year,externalIds,url,openAccessPdf) (inspected 2026-11-15).
- [Author publication list corroborates 1994 citation and links ICRA94.pdf; author PDF returned HTTP403 when opened](https://personal.utdallas.edu/~mspong/Articles/index_sv.htm) (inspected 2026-11-15).

## blenderproc

**BlenderProc** — How can the paper-associated renderer generate pose-annotated BOP Challenge training images?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** high.

### Paper for blenderproc

Tomáš Hodaň; Martin Sundermeyer; Bertram Drost; Yann Labbé; Eric Brachmann; Frank Michel; Carsten Rother; Jiří Matas (2020). [BOP Challenge 2020 on 6D Object Localization](https://doi.org/10.1007/978-3-030-66096-3_39). 10.1007/978-3-030-66096-3_39.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://link.springer.com/chapter/10.1007/978-3-030-66096-3_39). Metadata verification: confirmed. Full-text access: Publisher identity/abstract/footnote inspected; author arXiv:2009.07378 available. ECCVW 2020 citation year, first online 2021-01-03. Original result tables not yet extracted.

**Target in the paper:** Photorealistic training-data generation: 350K images across seven core datasets. Publisher footnote 4 links directly to BlenderProc4BOP source. Pose-estimation accuracy tables need separate method/checkpoint reproduction.

### Code and inputs for blenderproc

[Artifact or upstream source](https://github.com/DLR-RM/BlenderProc). Paper footnote and official challenge page identify this exact author-associated data-generation pipeline. Current Python examples port the original BlenderProc YAML configs to BlenderProc2; this is an adaptation until historical renderer/config versions are matched.

**Source inspected:** yes. **Ref:** main. **Commit:** 76bd8b82ee19489843578ff045298642197bf883.

**Files:** README_BlenderProc4BOP.md; examples/datasets/bop_challenge/README.md; examples/datasets/bop_challenge/main_lm_upright.py; examples/basics/basic/README.md

**Terms:** GPL-3.0; external scene/texture terms separate

**Environment and compute:** Isolated Python environment with BlenderProc and compatible Blender; set Blender installation and temporary paths under the workspace. CPU rendering possible; GPU helpful for BOP-scale datasets; first Blender download is nontrivial.

**Inputs:** BOP LM object models plus T-LESS/YCB-V/TYOL distractors used by main_lm_upright.py; BOP intrinsics; CC textures; record scene/material/light/pose random seeds and all asset versions.

**Data access:** Bundled basic assets available; BOP object meshes and textures have separate dataset terms.

### Construct and compare blenderproc

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # First verify the small bundled scene using the upstream command: ``
2. `` blenderproc run examples/basics/basic/main.py examples/resources/camera_positions examples/resources/scene.obj examples/basics/basic/output ``
3. `` # Proposed bounded paper-pipeline run, after downloading and pinning required assets: ``
4. `` blenderproc run examples/datasets/bop_challenge/main_lm_upright.py /path/to/bop-data /path/to/cctextures /path/to/output --num_scenes=1 ``
5. `` # Upstream full LM generation uses --num_scenes=2000 (25 images per scene). ``

**Expected outputs:** BOP-format RGB/depth images and camera/ground-truth object-pose JSON; one scene produces 25 images, while the documented full per-dataset route produces 50K.

**Comparison with the paper:** Check intrinsics, units, annotations, image counts and scene/pose distributions against the released BlenderProc4BOP training data. This reproduces a data-generation stage; reproducing pose-estimation accuracy additionally requires a chosen trained method, checkpoints, BOP toolkit version and paper score table. Do not infer method accuracy from rendered images.

**Execution result:** Source and instructions inspected; no local execution or paper-result claim.

**Execution evidence:** None recorded.

**Blockers:** Current BlenderProc2 port is newer than the original YAML/Blender pipeline; historic configuration/renderer equivalence and random seeds remain unresolved.; Full pose-accuracy table targets and trained-method artifacts have not been selected; multiple mesh/texture downloads and separate licenses are required.

**Next action:** Pin the historic configs or document the current port, gather exact object/texture assets, run one 25-image scene, then compare annotations/distributions to released paper training data before scaling.

**Gaps:** Current BlenderProc2 port is newer than the original YAML/Blender pipeline; historic configuration/renderer equivalence and random seeds remain unresolved.; Full pose-accuracy table targets and trained-method artifacts have not been selected; multiple mesh/texture downloads and separate licenses are required.

### Sources for blenderproc

- [Publication identity, author repository and software archive](https://joss.theoj.org/papers/10.21105/joss.04901) (inspected 2026-11-15).
- [Exact example inputs, output and command](https://raw.githubusercontent.com/DLR-RM/BlenderProc/76bd8b82ee19489843578ff045298642197bf883/examples/basics/basic/README.md) (inspected 2026-11-15).
- [Author-associated application route for BOP 2020](https://raw.githubusercontent.com/DLR-RM/BlenderProc/76bd8b82ee19489843578ff045298642197bf883/README_BlenderProc4BOP.md) (inspected 2026-11-15).
- [Primary publication identity, author list, date, 350K training images and footnote 4 linking renderer source](https://link.springer.com/chapter/10.1007/978-3-030-66096-3_39) (inspected 2026-11-15).
- [Official challenge identifies BlenderProc4BOP and source publication](https://bop.felk.cvut.cz/challenges/bop-challenge-2020/) (inspected 2026-11-15).
- [Actual inputs, 2000-scene default and CLI for current author pipeline](https://github.com/DLR-RM/BlenderProc/blob/76bd8b82ee19489843578ff045298642197bf883/examples/datasets/bop_challenge/main_lm_upright.py) (inspected 2026-11-15).

## carla

**CARLA** — How well does a driving agent generalize across urban routes and weather?

**Route:** Paper result candidate. **Execution:** Example executed. **Source confidence:** medium.

### Paper for carla

Alexey Dosovitskiy; German Ros; Felipe Codevilla; Antonio Lopez; Vladlen Koltun (2017). [CARLA: An Open Urban Driving Simulator](https://proceedings.mlr.press/v78/dosovitskiy17a.html). PMLR 78:1-16; arXiv:1711.03938.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://proceedings.mlr.press/v78/dosovitskiy17a.html). Metadata verification: confirmed. Full-text access: Open proceedings metadata and author benchmark code inspected; original numerical tables still need extraction.

**Target in the paper:** CoRL2017 driving benchmark: route success and infractions across tasks, weather, Town01 and Town02.

### Code and inputs for carla

[Artifact or upstream source](https://github.com/carla-simulator/driving-benchmarks). Official CARLA team CoRL2017 experiment suite for CARLA 0.8.4. This is a later benchmark implementation, not automatically the exact original simulator revision.

**Source inspected:** yes. **Ref:** master. **Commit:** 1614d19581d43eac9966e4001611cc8341bf5319.

**Files:** Docs/benchmark_start.md; Docs/benchmark_metrics.md; benchmarks_084.py; version084/driving_benchmarks/corl2017/corl_2017.py

**Terms:** MIT benchmark code; Unreal runtime and assets have separate terms

**Environment and compute:** Legacy CARLA 0.8.4 server and matching Python client; modern CARLA 0.9+/UE5 is not a drop-in environment. Compatible graphics machine; full suite many episodes.

**Inputs:** Town01/Town02, exact task/weather suite, evaluated agent checkpoint, seeds and episode counts. Bundled trivial agent is only a harness check.

**Data access:** Benchmark definitions public; locate historic simulator assets and trained agent weights separately.

### Construct and compare carla

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Upstream command with a CARLA 0.8.4 server on localhost:2000: ``
2. `` ./benchmarks_084.py --corl-2017 ``

**Expected outputs:** Per-episode benchmark records; completion/success and infraction metrics as documented in Docs/benchmark_metrics.md.

**Comparison with the paper:** Author benchmark reached3/3 goals, with no recorded collisions. This partial ForwardAgent result cannot be compared as a reproduction of originalMP/IL/RL success rates. Native summary+per-frame metrics retained.

**Execution result:** Official CARLA0.8.4 CPU/headless server and author CoRL2017 benchmark executed3 original straight-route pose pairs with ForwardAgent; all3 reached their goals.

**Execution evidence:** [Author-code attempt](../reproductions/carla.md); [Run record](../reproductions/records/carla.json)

**Blockers:** Original MP/IL/RL weights and exact2017simulator revision not matched; camera images unavailable with-nullrhi; only3pose subset executed.

**Next action:** Obtain original paper checkpoint and matching historic simulator; run graphics-enabled complete100/50 episode conditions, then compare Table1/2.

**Gaps:** Original MP/IL/RL weights and exact2017simulator revision not matched; camera images unavailable with-nullrhi; only3pose subset executed.

### Sources for carla

- [Primary publication identity](https://proceedings.mlr.press/v78/dosovitskiy17a.html) (inspected 2026-11-15).
- [Exact legacy version and CoRL2017 run command](https://github.com/carla-simulator/driving-benchmarks/blob/1614d19581d43eac9966e4001611cc8341bf5319/Docs/benchmark_start.md) (inspected 2026-11-15).
- [CARLA team explains later simulator revisions can change benchmark outcomes](https://carla.org/2018/04/23/release-0.8.2/) (inspected 2026-11-15).

## openfoam-dev

**OpenFOAM (Foundation)** — Can a coupled fluid/structure solve recover the published FSI3 oscillation and force observables?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for openfoam-dev

Stefan Turek; Jaroslav Hron (2006). [Proposal for Numerical Benchmarking of Fluid-Structure Interaction between an Elastic Object and Laminar Incompressible Flow](https://doi.org/10.1007/3-540-34596-5_15). 10.1007/3-540-34596-5_15.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1007/3-540-34596-5_15). Metadata verification: confirmed. Full-text access: Springer primary metadata verified; original numerical reference table not yet inspected. Author-hosted benchmark HTML parameter/result tables and downloadable FSI3 reference series were subsequently inspected.

**Target in the paper:** Published FSI3 channel/cylinder/elastic-flap benchmark; compare tip displacement, frequency, drag and lift. Current preCICE tutorial additionally cites the 2010 extension.

### Code and inputs for openfoam-dev

[Artifact or upstream source](https://github.com/precice/tutorials). Maintainer implementation of the literature benchmark; this tool supplies the fluid solver. Three tool records refer to one coupled experiment, not three independent reproductions.

**Source inspected:** yes. **Ref:** master. **Commit:** 98a78fe2dc2f6c5d84b2b30d35d00352782236f8.

**Files:** turek-hron-fsi3/precice-config.xml; turek-hron-fsi3/fluid-openfoam/run.sh; turek-hron-fsi3/solid-dealii/run.sh; turek-hron-fsi3/solid-dealii/parameters.prm

**Terms:** preCICE tutorials LGPL-3.0; solver and adapter licenses separately apply

**Environment and compute:** Compatible preCICE, OpenFOAM adapter and nonlinear deal.II adapter. Pin each participant and adapter independently, not only the tutorial. Foundation OpenFOAM dev is not interchangeable with OpenCFD releases. Advanced multi-core CPU coupled run, upstream estimates hours; default parallel fluid decomposition uses 25 ranks.

**Inputs:** FSI3 geometry, fluid/solid constitutive parameters, inlet ramp, mesh, time step and XML coupling settings from pinned case.

**Data access:** Case/meshes public. Author FSI3 reference series retrieved (1,113,417bytes; SHA256c428bc3ff48c1698cd10aacf0941cba6aabdfcb9d61c8b7e42c343f381434e63); this is upstream data, not a local simulation.

### Construct and compare openfoam-dev

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Inspected upstream commands; execute participants in separate terminals after compatibility setup: ``
2. `` cd turek-hron-fsi3/fluid-openfoam && ./run.sh ``
3. `` cd turek-hron-fsi3/solid-dealii && ./run.sh ``
4. `` # Optional upstream post-processing: ``
5. `` ./plot-displacement.sh solid-dealii ``

**Expected outputs:** Participant logs; OpenFOAM fields; solid VTK; preCICE tip watchpoint displacement history.

**Comparison with the paper:** Compare settled-window displacement histories to authors ref_fsi3.point: time column1, x/y tip displacement columns11/12; combined drag columns5+7 and lift6+8. The retrieved file is the author site's dt=0.00025 series. Match benchmark-definition/version and force normalization, demonstrate mesh/time-step/coupling convergence, and set a scientifically justified tolerance before claiming agreement. The original2006 printed table and tutorial2010 citation still require reconciliation.

**Execution result:** Source and instructions inspected; no local execution or paper-result claim.

**Execution evidence:** None recorded.

**Blockers:** Original reference target table and the tutorial's 2010 reference must be reconciled; target values and tolerances are not yet imported.; No coupled solver execution has occurred; mesh/time-step/coupling convergence must be demonstrated.; Current adapter documentation says preCICE v3 adapter default supports OpenCFD/ESI; Foundation 10/9/etc branches are experimental and the v3 ports remain pending. Resolve a compatible historic stack or port before executing this Foundation catalog entry.

**Next action:** Select exact reference publication/case; resolve solver/adapter versions; digitize or obtain reference data; then run three refinement levels and compare observables.

**Gaps:** Original reference target table and the tutorial's 2010 reference must be reconciled; target values and tolerances are not yet imported.; No coupled solver execution has occurred; mesh/time-step/coupling convergence must be demonstrated.; Current adapter documentation says preCICE v3 adapter default supports OpenCFD/ESI; Foundation 10/9/etc branches are experimental and the v3 ports remain pending. Resolve a compatible historic stack or port before executing this Foundation catalog entry.; Author manuscript located at https://riemann.mathematik.uni-dortmund.de/papers/TurekHron2006.pdf; browser fetch timed out, so no target-table values were transcribed.

### Sources for openfoam-dev

- [Primary benchmark identity and scope](https://link.springer.com/chapter/10.1007/3-540-34596-5_15) (inspected 2026-11-15).
- [Solver pair, run commands, watchpoint, refinement and 2010 reference](https://precice.org/tutorials/turek-hron-fsi3/) (inspected 2026-11-15).
- [Immutable case files](https://github.com/precice/tutorials/tree/98a78fe2dc2f6c5d84b2b30d35d00352782236f8/turek-hron-fsi3) (inspected 2026-11-15).
- [Foundation vs OpenCFD compatibility and current v3 adapter limitation](https://precice.org/docs/adapters/openfoam/openfoam-support/) (inspected 2026-11-15).
- [Author numerical reference series and exact column mapping; downloaded FSI3 file with retained hash](https://wwwold.mathematik.tu-dortmund.de/~featflow/en/benchmarks/cfdbenchmarking/fsi_benchmark/fsi_reference.html) (inspected 2026-11-15).
- [Author benchmark parameter and numerical-result tables across mesh/time-step choices](https://wwwold.mathematik.tu-dortmund.de/~featflow/en/benchmarks/cfdbenchmarking/fsi_benchmark/fsi_tests/fsi_fsi_tests.html) (inspected 2026-11-15).

## su2

**SU2** — Can an Euler flow/adjoint calculation predict transonic airfoil pressure and drag sensitivities?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for su2

Francisco Palacios; Juan Alonso; Karthikeyan Duraisamy; Michael Colonno; Jason Hicken; Aniket Aranake; Alejandro Campos; Sean Copeland; Thomas Economon; Amrita Lonkar; Trent Lukaczyk; Thomas Taylor (2013). [Stanford University Unstructured (SU2): An open-source integrated computational environment for multi-physics simulation and design](https://doi.org/10.2514/6.2013-287). 10.2514/6.2013-287.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.2514/6.2013-287). Metadata verification: confirmed. Full-text access: Live DOI metadata verified; current official example inspected. Original 2013 full-text numerical example still requires checking.

**Target in the paper:** Published software/design framework; proposed NACA0012 Euler/adjoint example from the author-maintained QuickStart. Original article figure mapping not yet established.

### Code and inputs for su2

[Artifact or upstream source](https://github.com/su2code/SU2). Official authors/developer source, with newer QuickStart NACA0012 example. A concrete path to the published methods, but not an identified archived 2013 result.

**Source inspected:** yes. **Ref:** master. **Commit:** 6c0e5c5c720936b175c4004e57332884443437f5.

**Files:** QuickStart/inv_NACA0012.cfg; QuickStart/mesh_NACA0012_inv.su2

**Terms:** LGPL-2.1; mesh terms need preservation

**Environment and compute:** SU2_CFD built from matching pinned source; serial CPU is sufficient for the starter. SU2_CFD_AD needed only for discrete adjoint. Small 2D CPU analysis; optimization/mesh studies longer.

**Inputs:** NACA0012 mesh, Mach 0.8, angle 1.25 degrees, freestream pressure 101325Pa and temperature 273.15K; configuration version 8.6.0 in current file.

**Data access:** Bundled public mesh and configuration; no observational data.

### Construct and compare su2

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Upstream QuickStart command: ``
2. `` cd QuickStart && SU2_CFD inv_NACA0012.cfg ``

**Expected outputs:** Flow field, surface pressure data and history; exact extensions depend on pinned OUTPUT_FILES.

**Comparison with the paper:** Compare pressure-coefficient distribution and lift/drag after grid and residual convergence; for an exact paper result first identify its matching case/figure and historic config. For adjoint verification compare directional derivatives against finite differences.

**Execution result:** Source and instructions inspected; no local execution or paper-result claim.

**Execution evidence:** None recorded.

**Blockers:** Current file postdates 2013 and is not an exact paper artifact; original article figure and reference coefficients remain unchecked.

**Next action:** Retrieve 2013 full text, map its NACA or design experiment to archived configs, then freeze a comparison before running.

**Gaps:** Current file postdates 2013 and is not an exact paper artifact; original article figure and reference coefficients remain unchecked.

### Sources for su2

- [Verified original software paper identity](https://api.crossref.org/works/10.2514/6.2013-287) (inspected 2026-11-15).
- [Official input settings, commands and outputs](https://su2code.github.io/docs_v7/Quick-Start/) (inspected 2026-11-15).
- [Current exact configuration and version](https://github.com/su2code/SU2/blob/6c0e5c5c720936b175c4004e57332884443437f5/QuickStart/inv_NACA0012.cfg) (inspected 2026-11-15).

## precice

**preCICE** — Can a coupled fluid/structure solve recover the published FSI3 oscillation and force observables?

**Route:** Paper result candidate. **Execution:** Attempted; blocked. **Source confidence:** medium.

### Paper for precice

Stefan Turek; Jaroslav Hron (2006). [Proposal for Numerical Benchmarking of Fluid-Structure Interaction between an Elastic Object and Laminar Incompressible Flow](https://doi.org/10.1007/3-540-34596-5_15). 10.1007/3-540-34596-5_15.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1007/3-540-34596-5_15). Metadata verification: confirmed. Full-text access: Springer primary metadata verified; original numerical reference table not yet inspected. Author-hosted benchmark HTML parameter/result tables and downloadable FSI3 reference series were subsequently inspected.

**Target in the paper:** Original 2006 FSI3 benchmark; maintained tutorial also cites the 2010 extension DOI 10.1007/978-3-642-14206-2_8. Historical reference/constitutive alignment unresolved; no original result comparison.

### Code and inputs for precice

[Artifact or upstream source](https://github.com/precice/tutorials). Maintainer implementation of the literature benchmark; this tool supplies the partitioned coupling. Three tool records refer to one coupled experiment, not three independent reproductions.

**Source inspected:** yes. **Ref:** master. **Commit:** 98a78fe2dc2f6c5d84b2b30d35d00352782236f8.

**Files:** turek-hron-fsi3/precice-config.xml; turek-hron-fsi3/fluid-openfoam/run.sh; turek-hron-fsi3/solid-dealii/run.sh; turek-hron-fsi3/solid-dealii/parameters.prm

**Terms:** preCICE tutorials LGPL-3.0; solver and adapter licenses separately apply

**Environment and compute:** Compatible preCICE, OpenFOAM adapter and nonlinear deal.II adapter. Pin each participant and adapter independently, not only the tutorial. Advanced multi-core CPU coupled run, upstream estimates hours; default parallel fluid decomposition uses 25 ranks.

**Inputs:** FSI3 geometry, fluid/solid constitutive parameters, inlet ramp, mesh, time step and XML coupling settings from pinned case.

**Data access:** Case/meshes public. Author FSI3 reference series retrieved (1,113,417bytes; SHA256c428bc3ff48c1698cd10aacf0941cba6aabdfcb9d61c8b7e42c343f381434e63); this is upstream data, not a local simulation.

### Construct and compare precice

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Inspected upstream commands; execute participants in separate terminals after compatibility setup: ``
2. `` cd turek-hron-fsi3/fluid-openfoam && ./run.sh ``
3. `` cd turek-hron-fsi3/solid-dealii && ./run.sh ``
4. `` # Optional upstream post-processing: ``
5. `` ./plot-displacement.sh solid-dealii ``

**Expected outputs:** Participant logs; OpenFOAM fields; solid VTK; preCICE tip watchpoint displacement history.

**Comparison with the paper:** No published periodic observable compared. A short transient cannot recover FSI3 mean, amplitude or frequency; exit 0 did not establish coupling convergence.

**Execution result:** Actual coupling executed. The CG adaptation completed 0.003 s with both participants exiting 0, but the first two of three windows were unconverged. A tighter fluid solver retry also failed its first two windows and hit the 240 s bound. The Direct solver failed due to missing UMFPACK. No qualified coupled solution or paper-result comparison.

**Execution evidence:** [Author-code attempt](../reproductions/precice.md); [Run record](../reproductions/records/precice.json)

**Blockers:** Installed deal.II 9.3.2 build has no UMFPACK; author Direct solver unavailable.; CG adaptation failed implicit coupling convergence in the first two windows; tighter fluid tolerances did not resolve it.; Current neo-Hookean solid, publication and reference-series constitutive alignment unresolved.; Full periodic benchmark and refinement study require a qualified setup and an hours-scale run; not launched.

**Next action:** Qualify the Direct solver or CG alternative and converged coupling; resolve original 2006 versus 2010 reference/material law; then predeclare the analysis window/tolerance and run the full horizon with mesh/time-step convergence.

**Gaps:** Installed deal.II 9.3.2 build has no UMFPACK; author Direct solver unavailable.; CG adaptation failed implicit coupling convergence in the first two windows; tighter fluid tolerances did not resolve it.; Current neo-Hookean solid, publication and reference-series constitutive alignment unresolved.; Full periodic benchmark and refinement study require a qualified setup and an hours-scale run; not launched.

### Sources for precice

- [Primary benchmark identity and scope](https://link.springer.com/chapter/10.1007/3-540-34596-5_15) (inspected 2026-11-15).
- [Solver pair, run commands, watchpoint, refinement and 2010 reference](https://precice.org/tutorials/turek-hron-fsi3/) (inspected 2026-11-15).
- [Immutable case files](https://github.com/precice/tutorials/tree/98a78fe2dc2f6c5d84b2b30d35d00352782236f8/turek-hron-fsi3) (inspected 2026-11-15).
- [Author numerical reference series and exact column mapping; downloaded FSI3 file with retained hash](https://wwwold.mathematik.tu-dortmund.de/~featflow/en/benchmarks/cfdbenchmarking/fsi_benchmark/fsi_reference.html) (inspected 2026-11-15).
- [Author benchmark parameter and numerical-result tables across mesh/time-step choices](https://wwwold.mathematik.tu-dortmund.de/~featflow/en/benchmarks/cfdbenchmarking/fsi_benchmark/fsi_tests/fsi_fsi_tests.html) (inspected 2026-11-15).

## dolfinx

**FEniCSx / DOLFINx** — Can flux equilibration drive adaptive FEM to the published convergence and efficiency values?

**Route:** Paper result candidate. **Execution:** Selected paper target compared. **Source confidence:** high.

### Paper for dolfinx

Maximilian Brodbeck; Fleurianne Bertrand; Tim Ricken (2026). [Adaptive Finite Element Methods Based on Flux Equilibration Using FEniCSx](https://doi.org/10.1007/978-3-032-17396-6_1). 10.1007/978-3-032-17396-6_1.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://link.springer.com/chapter/10.1007/978-3-032-17396-6_1). Metadata verification: confirmed. Full-text access: Published open chapter metadata inspected; full-text model/results inspected in the linked 2024 arXiv:2410.09764v1 preprint. Published/preprint target equivalence still requires checking.

**Target in the paper:** Section4.1, Figure2(a), contrast5, k=1, m=2

### Code and inputs for dolfinx

[Artifact or upstream source](https://github.com/brodbeck-m/AFEM-by-Equilibration). Author-associated exact experiment repository linked from preprint supplementary-material section; immutable DaRUS V1 archive DOI 10.18419/DARUS-4500. Uses dolfinx_eqlb v1.2.0 and DOLFINx 0.6.0-r1.

**Source inspected:** yes. **Ref:** main. **Commit:** 3d9741498712c13ce901f5fbd6255a82a3cec1ac.

**Files:** README.md; docker/Dockerfile; docker/launch_container.sh; execute_all.sh; case_poisson_riviere/solve_riviere.py; case_poisson_lshape/solve_lshape.py

**Terms:** LICENSE file says GPL-3.0; README says LGPL-3.0-or-later. Treat as an unresolved license discrepancy before copying code.

**Environment and compute:** Historic Docker image dolfinx/dolfinx:v0.6.0-r1 plus dolfinx_eqlb v1.2.0, PETSc/MUMPS; original Dockerfile upgrades OS packages so archive image digest is preferable. Small 2D CPU start, increasingly heavy adaptive refinements; archived ready image about 1.4GB dataset download.

**Inputs:** Quadrant coefficient contrast 5 or 100, Dörfler theta=0.5, primal/flux orders, 20/40 refinements as in preprint; use the interface (Riviere) script for Figure 2.

**Data access:** Author code and DaRUS archive are open; no restricted observations.

### Construct and compare dolfinx

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Upstream setup; run in a fresh study copy: ``
2. `` docker pull dolfinx/dolfinx:v0.6.0-r1 ``
3. `` ./docker/build_image.sh ``
4. `` # Corrected file spelling after inspection (README has launch-container.sh): ``
5. `` ./docker/launch_container.sh ``
6. `` # Inside container; proposed bounded Figure-2 route from the inspected driver structure: ``
7. `` cd case_poisson_riviere && python3 solve_riviere.py ``

**Expected outputs:** CSV convergence/error/efficiency tables and XDMF/HDF5 fields; full execute_all.sh also runs timing and elasticity cases and deletes prior CSV outputs.

**Comparison with the paper:** One author-code preprint parameter combination; comparison uses rounded printed reference values, with human scientific review pending.

**Execution result:** Exact author adaptive_solver(1,2,20,0.5,5) completed all20 levels; native CSV/XDMF/HDF5 outputs retained. Both printed targets matched within predeclared reporting-precision tolerance.

**Execution evidence:** [Author-code attempt](../reproductions/dolfinx.md); [Run record](../reproductions/records/dolfinx.json)

**Blockers:** None recorded.

**Next action:** Human scientific review of one matched case; expand to other paper parameter combinations separately.

**Gaps:** None recorded.

### Sources for dolfinx

- [Published 2026 title/authors/year and DOI](https://link.springer.com/chapter/10.1007/978-3-032-17396-6_1) (inspected 2026-11-15).
- [Section 4 target settings/values and direct supplementary-code links](https://arxiv.org/html/2410.09764v1) (inspected 2026-11-15).
- [Author archive, environment and experiment provenance](https://darus.uni-stuttgart.de/dataset.xhtml?persistentId=doi%3A10.18419%2Fdarus-4500) (inspected 2026-11-15).
- [Exact author source and runnable case structure](https://github.com/brodbeck-m/AFEM-by-Equilibration/tree/3d9741498712c13ce901f5fbd6255a82a3cec1ac) (inspected 2026-11-15).

## dealii

**deal.II** — Can a coupled fluid/structure solve recover the published FSI3 oscillation and force observables?

**Route:** Paper result candidate. **Execution:** Attempted; blocked. **Source confidence:** medium.

### Paper for dealii

Stefan Turek; Jaroslav Hron (2006). [Proposal for Numerical Benchmarking of Fluid-Structure Interaction between an Elastic Object and Laminar Incompressible Flow](https://doi.org/10.1007/3-540-34596-5_15). 10.1007/3-540-34596-5_15.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1007/3-540-34596-5_15). Metadata verification: confirmed. Full-text access: Springer primary metadata verified; original numerical reference table not yet inspected. Author-hosted benchmark HTML parameter/result tables and downloadable FSI3 reference series were subsequently inspected.

**Target in the paper:** Original 2006 FSI3 benchmark; maintained tutorial also cites the 2010 extension DOI 10.1007/978-3-642-14206-2_8. Historical reference/constitutive alignment unresolved; no original result comparison.

### Code and inputs for dealii

[Artifact or upstream source](https://github.com/precice/tutorials). Maintainer implementation of the literature benchmark; this tool supplies the nonlinear solid solver. Three tool records refer to one coupled experiment, not three independent reproductions.

**Source inspected:** yes. **Ref:** master. **Commit:** 98a78fe2dc2f6c5d84b2b30d35d00352782236f8.

**Files:** turek-hron-fsi3/precice-config.xml; turek-hron-fsi3/fluid-openfoam/run.sh; turek-hron-fsi3/solid-dealii/run.sh; turek-hron-fsi3/solid-dealii/parameters.prm

**Terms:** preCICE tutorials LGPL-3.0; solver and adapter licenses separately apply

**Environment and compute:** Compatible preCICE, OpenFOAM adapter and nonlinear deal.II adapter. Pin each participant and adapter independently, not only the tutorial. Advanced multi-core CPU coupled run, upstream estimates hours; default parallel fluid decomposition uses 25 ranks.

**Inputs:** FSI3 geometry, fluid/solid constitutive parameters, inlet ramp, mesh, time step and XML coupling settings from pinned case.

**Data access:** Case/meshes public. Author FSI3 reference series retrieved (1,113,417bytes; SHA256c428bc3ff48c1698cd10aacf0941cba6aabdfcb9d61c8b7e42c343f381434e63); this is upstream data, not a local simulation.

### Construct and compare dealii

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Inspected upstream commands; execute participants in separate terminals after compatibility setup: ``
2. `` cd turek-hron-fsi3/fluid-openfoam && ./run.sh ``
3. `` cd turek-hron-fsi3/solid-dealii && ./run.sh ``
4. `` # Optional upstream post-processing: ``
5. `` ./plot-displacement.sh solid-dealii ``

**Expected outputs:** Participant logs; OpenFOAM fields; solid VTK; preCICE tip watchpoint displacement history.

**Comparison with the paper:** No published periodic observable compared. A short transient cannot recover FSI3 mean, amplitude or frequency; exit 0 did not establish coupling convergence.

**Execution result:** Actual coupling executed. The CG adaptation completed 0.003 s with both participants exiting 0, but the first two of three windows were unconverged. A tighter fluid solver retry also failed its first two windows and hit the 240 s bound. The Direct solver failed due to missing UMFPACK. No qualified coupled solution or paper-result comparison.

**Execution evidence:** [Author-code attempt](../reproductions/dealii.md); [Run record](../reproductions/records/dealii.json)

**Blockers:** Installed deal.II 9.3.2 build has no UMFPACK; author Direct solver unavailable.; CG adaptation failed implicit coupling convergence in the first two windows; tighter fluid tolerances did not resolve it.; Current neo-Hookean solid, publication and reference-series constitutive alignment unresolved.; Full periodic benchmark and refinement study require a qualified setup and an hours-scale run; not launched.

**Next action:** Qualify the Direct solver or CG alternative and converged coupling; resolve original 2006 versus 2010 reference/material law; then predeclare the analysis window/tolerance and run the full horizon with mesh/time-step convergence.

**Gaps:** Installed deal.II 9.3.2 build has no UMFPACK; author Direct solver unavailable.; CG adaptation failed implicit coupling convergence in the first two windows; tighter fluid tolerances did not resolve it.; Current neo-Hookean solid, publication and reference-series constitutive alignment unresolved.; Full periodic benchmark and refinement study require a qualified setup and an hours-scale run; not launched.

### Sources for dealii

- [Primary benchmark identity and scope](https://link.springer.com/chapter/10.1007/3-540-34596-5_15) (inspected 2026-11-15).
- [Solver pair, run commands, watchpoint, refinement and 2010 reference](https://precice.org/tutorials/turek-hron-fsi3/) (inspected 2026-11-15).
- [Immutable case files](https://github.com/precice/tutorials/tree/98a78fe2dc2f6c5d84b2b30d35d00352782236f8/turek-hron-fsi3) (inspected 2026-11-15).
- [Author numerical reference series and exact column mapping; downloaded FSI3 file with retained hash](https://wwwold.mathematik.tu-dortmund.de/~featflow/en/benchmarks/cfdbenchmarking/fsi_benchmark/fsi_reference.html) (inspected 2026-11-15).
- [Author benchmark parameter and numerical-result tables across mesh/time-step choices](https://wwwold.mathematik.tu-dortmund.de/~featflow/en/benchmarks/cfdbenchmarking/fsi_benchmark/fsi_tests/fsi_fsi_tests.html) (inspected 2026-11-15).

## mfem

**MFEM** — How does a finite-element discretization solve a Poisson equation with zero boundary values?

**Route:** Software paper example. **Execution:** Example executed. **Source confidence:** medium.

### Paper for mfem

Robert Anderson; Julian Andrej; Andrew Barker; Jamie Bramwell; Jean-Sylvain Camier; Jakub Cerveny; Veselin Dobrev; Yohann Dudouit; Aaron Fisher; Tzanio Kolev; Will Pazner; Mark Stowell; Vladimir Tomov; Ido Akkerman; Johann Dahm; David Medina; Stefano Zampini (2021). [MFEM: A modular finite element methods library](https://doi.org/10.1016/j.camwa.2020.06.009). 10.1016/j.camwa.2020.06.009.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1016/j.camwa.2020.06.009). Metadata verification: confirmed. Full-text access: Publication metadata and author manuscript example-code passage inspected; official ex1 source inspected.

**Target in the paper:** Paper example-code discussion explicitly introduces ex1 Poisson problem; this starter reproduces the documented software example, not scaling plots.

### Code and inputs for mfem

[Artifact or upstream source](https://github.com/mfem/mfem). Official library example discussed in the software paper; current source is newer than the paper and cannot establish its timing/scaling claims.

**Source inspected:** yes. **Ref:** master. **Commit:** 781ed1cadaae3a03380c4d1414bc2e8969aac2b6.

**Files:** INSTALL; examples/ex1.cpp; data/star.mesh; examples/ex3.cpp

**Terms:** BSD-3-Clause

**Environment and compute:** Serial C++17 build from pinned source; GNU make and g++; no MPI or accelerator needed for serial example. Serial CPU; build minutes, solve small model.

**Inputs:** Bundled star.mesh; order 1 by default; use -no-vis to avoid socket visualization.

**Data access:** Bundled mesh, no external data.

### Construct and compare mfem

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Upstream INSTALL and ex1.cpp route; no system installation required: ``
2. `` make serial -j 2 ``
3. `` cd examples && make ex1 ``
4. `` ./ex1 -m ../data/star.mesh -no-vis ``
5. `` # Also executed upstream manufactured-solution starter: ``
6. `` ./ex3 -m ../data/star.mesh -o 1 -no-vis ``

**Expected outputs:** refined.mesh, sol.gf and conjugate-gradient iteration/residual log.

**Comparison with the paper:** Verify Dirichlet boundary enforcement and finite solution, then compare integrated quantities/refinement behavior. A paper timing/scaling reproduction requires its exact version, meshes, hardware and numerical target; no such claim follows from ex1 success.

**Execution result:** Pinned MFEM source built serially without system installation. Poisson ex1: 20,801 unknowns, 111 iterations, solution and mesh saved. Maxwell ex3 order 1: 41,280 unknowns, 386 iterations, manufactured-solution L2 error 0.0134918. Two order 2 extensions exited 0 but reported PCG nonconvergence after 500 iterations; retained as failed. These are current upstream examples, not paper-result reproductions.

**Execution evidence:** [Run receipt](verification/mfem.json)

**Blockers:** Current software version differs from paper; no specific paper quantitative result selected.; Observed order2 Maxwell nonconvergence despite exit0; its lower printed error cannot establish convergence-order agreement.

**Next action:** Keep the converged Poisson/first-order Maxwell starter; use a suitable H(curl) preconditioner or documented direct solver before interpreting higher-order Maxwell results. Select an exact paper quantitative target separately.

**Gaps:** Current software version differs from paper; no specific paper quantitative result selected.; Order2 Maxwell and order2 static-condensation attempts reached the built-in500iteration cap; both logs preserved.

### Sources for mfem

- [Verified software paper and example-code discussion](https://doi.org/10.1016/j.camwa.2020.06.009) (inspected 2026-11-15).
- [Official Example 1 problem and capabilities](https://mfem.org/examples/) (inspected 2026-11-15).
- [Actual CLI, solution and mesh output names](https://github.com/mfem/mfem/blob/781ed1cadaae3a03380c4d1414bc2e8969aac2b6/examples/ex1.cpp) (inspected 2026-11-15).

## moose

**MOOSE** — How does temperature-dependent microstructure degradation change the coupled porous-column thermal response?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for moose

Cody J. Permann; Derek R. Gaston; David Andrš; Robert W. Carlsen; Fande Kong; Alexander D. Lindsay; Jason M. Miller; John W. Peterson; Andrew E. Slaughter; Roy H. Stogner; Richard C. Martineau (2020). [MOOSE: Enabling massively parallel multiphysics simulation](https://doi.org/10.1016/j.softx.2020.100430). 10.1016/j.softx.2020.100430.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1016/j.softx.2020.100430). Metadata verification: confirmed. Full-text access: Open author preprint read for illustrative example; journal metadata verified live.

**Target in the paper:** Section 3 and Figure 2: engineering-scale Darcy flow/thermal mechanics coupled to six degrading steel-sphere microstructure calculations; snapshot at 58 seconds.

### Code and inputs for moose

[Artifact or upstream source](https://github.com/idaholab/moose). Maintainer multiscale tutorial implements the same type of coupled packed-column/sphere calculation as paper Figure 2. Current input differs, so exact historic case equivalence is not asserted.

**Source inspected:** yes. **Ref:** master. **Commit:** 08315af82ed0b71e3edf82c04161b2da6a1aff19.

**Files:** tutorials/darcy_thermo_mech/doc/content/workshop/problem/step10.md; tutorials/darcy_thermo_mech/step10_multiapps/problems/step10.i; tutorials/darcy_thermo_mech/step10_multiapps/problems/step10_micro.i; tutorials/darcy_thermo_mech/step10_multiapps/src/auxkernels/RandomCorrosion.C

**Terms:** MOOSE LGPL-2.1 core; tutorial local LICENSE and dependencies also apply

**Environment and compute:** Pinned MOOSE source and matched libMesh/PETSc toolchain, C++ compiler and optional MPI; build only darcy_thermo_mech application after framework setup. Multi-core CPU with six micro-models; substantially heavier build than starter Poisson example.

**Inputs:** Macro mesh, water-property CSVs, six micro-app positions, corrosion settings/seed, thermal/pressure boundary ramps and time stepping; retain macro/micro files.

**Data access:** Code and tabulated water properties provided by upstream; preserve local terms.

### Construct and compare moose

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` # Upstream workshop commands; adjust build parallelism to available resources: ``
2. `` cd tutorials/darcy_thermo_mech/step10_multiapps && make -j 2 ``
3. `` cd problems && ../darcy_thermo_mech-opt -i step10.i ``

**Expected outputs:** Macro and micro Exodus fields; effective thermal conductivity and degradation histories must be exported explicitly for comparison.

**Comparison with the paper:** Compare Figure 2 temperature field and six conductivity histories at 58s. First reconcile original timestep/ramp, units and stochastic corrosion with current inputs; add numeric postprocessors and compare native fields/history, not just a similar image.

**Execution result:** Source and instructions inspected; no local execution or paper-result claim.

**Execution evidence:** None recorded.

**Blockers:** Current macro input uses a function timestep initially 0.1 whereas paper describes 0.25; original corrosion random seed and figure source data not established.; Paper temperature unit text and current input comments require reconciliation; no matched-parameter validation or target tolerance yet.

**Next action:** Locate the paper-era commit, resolve parameter/unit and random-seed differences, export the six conductivity series, then compare the selected 58s result.

**Gaps:** Current macro input uses a function timestep initially 0.1 whereas paper describes 0.25; original corrosion random seed and figure source data not established.; Paper temperature unit text and current input comments require reconciliation; no matched-parameter validation or target tolerance yet.

### Sources for moose

- [Open author manuscript Section 3 / Figure 2 model and run description](https://arxiv.org/pdf/1911.04488) (inspected 2026-11-15).
- [Actual multiscale build and run command](https://github.com/idaholab/moose/blob/08315af82ed0b71e3edf82c04161b2da6a1aff19/tutorials/darcy_thermo_mech/doc/content/workshop/problem/step10.md) (inspected 2026-11-15).
- [Six microapps, transfer mechanism and current parameter differences](https://github.com/idaholab/moose/blob/08315af82ed0b71e3edf82c04161b2da6a1aff19/tutorials/darcy_thermo_mech/step10_multiapps/problems/step10.i) (inspected 2026-11-15).
