# Scenes and robotics: paper-to-code routes

[All 60 tools](README.md) · [How to contribute](../contributing.md)

These are construction routes researched by agents. The execution line reports the bounded work actually performed; the comparison section defines what remains before claiming a published result. Human scientific review is pending.

## openusd

**OpenUSD** — Can a paper-associated robot scene preserve the model and time-varying experiment metadata through USD?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for openusd

Mayank Mittal et al. (2023). [Orbit: A Unified Simulation Framework for Interactive Robot Learning Environments](https://doi.org/10.1109/LRA.2023.3270034). 10.1109/LRA.2023.3270034.

**Publication type:** journal_article. [Primary metadata](https://api.crossref.org/works/10.1109/LRA.2023.3270034). Metadata verification: confirmed. Full-text access: Live Crossref metadata refreshed; prior lab inspected open manuscript architecture

**Target in the paper:** USD scene architecture; current successor Cartpole USD asset is an adaptation, not the 2023 experiment archive.

### Code and inputs for openusd

[Artifact or upstream source](https://github.com/isaac-sim/IsaacLab). Isaac Lab is Orbit successor; inspected source loads Cartpole/cartpole.usd through UsdFileCfg. USD supports scene exchange; PhysX solves dynamics.

**Source inspected:** yes. **Ref:** v2.2.0. **Commit:** 46dff135f44683f031edf346e544fcfd8456b2bb.

**Files:** source/isaaclab_assets/isaaclab_assets/robots/cartpole.py; source/isaaclab_tasks/isaaclab_tasks/direct/cartpole/cartpole_env.py

**Terms:** BSD-3-Clause source; separate NVIDIA runtime and asset terms

**Environment and compute:** Isaac Lab v2.2.0 with compatible Isaac Sim 5.0.0; standalone usd-core for inspection CPU for USD inspection; NVIDIA GPU for coupled Isaac simulation.

**Inputs:** Cartpole USD asset referenced by upstream configuration; preserve resolved dependency hashes and simulator settings.

**Data access:** Source public; robot assets and runtime carry separate terms.

### Construct and compare openusd

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed: fetch the configured Cartpole USD asset through the documented Isaac asset endpoint and retain a local dependency manifest. ``
2. `` Proposed: use pxr.Usd.Stage.Open(local_asset), inspect articulation/physics schemas and reference dependencies, and compare attributes before/after export. ``

**Expected outputs:** Editable USD scene, dependency manifest, source-to-export attribute comparison.

**Comparison with the paper:** Verify composed prim paths, units, joint names and physics attributes are preserved. No paper numerical outcome is claimed.

**Execution result:** No execution claim; commands were inspected upstream or explicitly marked proposed.

**Execution evidence:** None recorded.

**Blockers:** Original Orbit experiment version not matched; local USD asset retrieval not attempted.

**Next action:** Develop the scene-manifest exercise beside the existing battery-results-to-USD example.

**Gaps:** Original Orbit experiment version not matched; local USD asset retrieval not attempted.

### Sources for openusd

- [Paper identity](https://api.crossref.org/works/10.1109/LRA.2023.3270034) (inspected 2026-11-15).
- [Concrete published-framework USD scene loading configuration](https://github.com/isaac-sim/IsaacLab/blob/46dff135f44683f031edf346e544fcfd8456b2bb/source/isaaclab_assets/isaaclab_assets/robots/cartpole.py) (inspected 2026-11-15).

## blender

**Blender** — Can we regenerate MOVi-A synthetic videos and their ground-truth annotations?

**Route:** Paper result candidate. **Execution:** Example executed. **Source confidence:** high.

### Paper for blender

Klaus Greff et al. (2022). [Kubric: A scalable dataset generator](https://arxiv.org/abs/2203.03570). arXiv:2203.03570v1.

**Publication type:** conference_paper. [Primary metadata](https://arxiv.org/abs/2203.03570). Metadata verification: confirmed. Full-text access: Open CVPR 2022 manuscript HTML inspected

**Target in the paper:** Section 4.1 and Figure 5, MOVi-A scene-generation properties; Table 3 learning results require a separate training reproduction.

### Code and inputs for blender

[Artifact or upstream source](https://github.com/google-research/kubric). Authors explicitly identify MOVi as a dataset contribution of their CVPR paper; Blender renders and PyBullet simulates.

**Source inspected:** yes. **Ref:** main at inspection. **Commit:** 61f2422c84bab75006df33c6989e0b483db3ccfe.

**Files:** challenges/movi/README.md; challenges/movi/movi_ab_worker.py; challenges/movi/movi_a.py

**Terms:** Kubric Apache-2.0; Blender GPL; inspect bundled object/material terms

**Environment and compute:** Authors kubricdockerhub/kubruntu image; upstream documents Blender 2.93. Resolve/pin image digest before production reproduction. CPU rendering possible for one scene; full dataset rendering is expensive.

**Inputs:** CLEVR-style object set, background and camera; one fixed scene seed initially, then matching dataset generator settings.

**Data access:** Public authors code and public dataset bucket; retain asset manifest and terms.

### Construct and compare blender

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Upstream README: git clone https://github.com/google-research/kubric.git ``
2. `` Proposed pin: git checkout 61f2422c84bab75006df33c6989e0b483db3ccfe ``
3. `` Upstream MOVi-A command: docker run --rm --interactive --user $(id -u):$(id -g) --volume "$(pwd):/kubric" kubricdockerhub/kubruntu /usr/bin/python3 challenges/movi/movi_ab_worker.py --objects_set=clevr --background=clevr --camera=clevr ``

**Expected outputs:** RGB frames, instance segmentation, depth, optical flow, scene metadata and saved scene as configured by worker.

**Comparison with the paper:** PublishedMOVi-A dataset-design properties match; all9numerical/design checks passed. Originalfigurepixels, originalassetbytes andTable3learning scores are outside this comparison.

**Execution result:** Paper-date author worker ran to completion onCPU:24frames,256×256,7objects and all rendered annotations/native states. Nine design checks passed; second scene has identical instance metadata and24/24RGBAhashes.

**Execution evidence:** [Author-code attempt](../reproductions/blender.md); [Run record](../reproductions/records/blender.json)

**Blockers:** Exact2022assetbytes and full originaldependencylock not established; SAVi/SIMONeTable3training benchmark not attempted.

**Next action:** Human review of the dataset-generation guide; match archivedassets and modeltraining protocol before reproducingTable3.

**Gaps:** Exact2022assetbytes and full originaldependencylock not established; SAVi/SIMONeTable3training benchmark not attempted.

### Sources for blender

- [Paper identity](https://arxiv.org/abs/2203.03570) (inspected 2026-11-15).
- [Section 4.1 and Figure 5](https://arxiv.org/html/2203.03570v1) (inspected 2026-11-15).
- [Author generator command and dataset properties](https://github.com/google-research/kubric/blob/61f2422c84bab75006df33c6989e0b483db3ccfe/challenges/movi/README.md) (inspected 2026-11-15).

## isaacsim

**Isaac Sim** — Can the published framework train a physics-based classic-control policy?

**Route:** Software paper example. **Execution:** Not run. **Source confidence:** medium.

### Paper for isaacsim

NVIDIA; Mayank Mittal et al. (2025). [Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning](https://arxiv.org/abs/2511.04831). arXiv:2511.04831v1.

**Publication type:** preprint. [Primary metadata](https://arxiv.org/abs/2511.04831). Metadata verification: confirmed. Full-text access: Open preprint HTML inspected; publication beyond preprint not established

**Target in the paper:** Section 3.7.3 classic Cartpole environments; Section 4.1 throughput definition. This route does not reproduce hardware throughput figures.

### Code and inputs for isaacsim

[Artifact or upstream source](https://github.com/isaac-sim/IsaacLab). Paper directly links this author framework. Inspected v2.2.0 is a concrete supported baseline; correspondence to the paper benchmark commit is unestablished.

**Source inspected:** yes. **Ref:** v2.2.0. **Commit:** 46dff135f44683f031edf346e544fcfd8456b2bb.

**Files:** source/isaaclab_tasks/isaaclab_tasks/direct/cartpole/cartpole_env.py; source/isaaclab_tasks/isaaclab_tasks/direct/cartpole/agents/rsl_rl_ppo_cfg.py; scripts/reinforcement_learning/rsl_rl/train.py; docs/source/overview/reinforcement-learning/rl_existing_scripts.rst

**Terms:** Isaac Lab BSD-3-Clause core; Isaac Sim source Apache-2.0; runtime/assets separate terms

**Environment and compute:** Isaac Lab v2.2.0; Isaac Sim 5.0.0 and supported NVIDIA GPU/driver; RSL-RL wrapper. NVIDIA GPU runtime; no hardware-scale training attempted.

**Inputs:** Isaac-Cartpole-Direct-v0, explicit seed and recorded number of environments; task dt=1/120 s and decimation=2 in inspected config.

**Data access:** Public source; network robot assets and NVIDIA runtime terms.

### Construct and compare isaacsim

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed pin: git checkout 46dff135f44683f031edf346e544fcfd8456b2bb ``
2. `` Upstream wrapper installation route: ./isaaclab.sh -i rsl_rl ``
3. `` Proposed task selection using inspected train entry point: ./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Cartpole-Direct-v0 --num_envs 64 --seed 42 --headless ``

**Expected outputs:** Training configuration, logs and policy checkpoints; deterministic evaluation episodes; optional USD scene manifest.

**Comparison with the paper:** Compare multiple same-seed and different-seed reward/episode-length curves. A 64-environment teaching run is not the paper throughput experiment; matching Section 4.1 requires exact task, GPU, environment count and timing definition.

**Execution result:** No execution claim; commands were inspected upstream or explicitly marked proposed.

**Execution evidence:** None recorded.

**Blockers:** No local compatible GPU runtime verified; paper benchmark revision/hardware not matched.

**Next action:** Provision an approved GPU runner, pin the paper environment, then run a small complete training/evaluation cycle.

**Gaps:** No local compatible GPU runtime verified; paper benchmark revision/hardware not matched.

### Sources for isaacsim

- [Paper metadata and direct author-code association](https://arxiv.org/abs/2511.04831) (inspected 2026-11-15).
- [Section 3.7.3 names classic tasks; Section 4.1 defines throughput](https://arxiv.org/html/2511.04831v1) (inspected 2026-11-15).
- [Concrete model timestep/rewards/reset configuration](https://github.com/isaac-sim/IsaacLab/blob/46dff135f44683f031edf346e544fcfd8456b2bb/source/isaaclab_tasks/isaaclab_tasks/direct/cartpole/cartpole_env.py) (inspected 2026-11-15).
- [Training wrapper route](https://github.com/isaac-sim/IsaacLab/blob/46dff135f44683f031edf346e544fcfd8456b2bb/docs/source/overview/reinforcement-learning/rl_existing_scripts.rst) (inspected 2026-11-15).

## isaaclab

**Isaac Lab** — Can we train, save and evaluate a paper-associated Cartpole policy reproducibly?

**Route:** Software paper example. **Execution:** Not run. **Source confidence:** medium.

### Paper for isaaclab

NVIDIA; Mayank Mittal et al. (2025). [Isaac Lab: A GPU-Accelerated Simulation Framework for Multi-Modal Robot Learning](https://arxiv.org/abs/2511.04831). arXiv:2511.04831v1.

**Publication type:** preprint. [Primary metadata](https://arxiv.org/abs/2511.04831). Metadata verification: confirmed. Full-text access: Open preprint HTML inspected; publication beyond preprint not established

**Target in the paper:** Section 3.7.3 classic Cartpole environments; Section 4.1 throughput definition. This route does not reproduce hardware throughput figures.

### Code and inputs for isaaclab

[Artifact or upstream source](https://github.com/isaac-sim/IsaacLab). Paper directly links this author framework. Inspected v2.2.0 is a concrete supported baseline; correspondence to the paper benchmark commit is unestablished.

**Source inspected:** yes. **Ref:** v2.2.0. **Commit:** 46dff135f44683f031edf346e544fcfd8456b2bb.

**Files:** source/isaaclab_tasks/isaaclab_tasks/direct/cartpole/cartpole_env.py; source/isaaclab_tasks/isaaclab_tasks/direct/cartpole/agents/rsl_rl_ppo_cfg.py; scripts/reinforcement_learning/rsl_rl/train.py; docs/source/overview/reinforcement-learning/rl_existing_scripts.rst

**Terms:** Isaac Lab BSD-3-Clause core; Isaac Sim source Apache-2.0; runtime/assets separate terms

**Environment and compute:** Isaac Lab v2.2.0; Isaac Sim 5.0.0 and supported NVIDIA GPU/driver; RSL-RL wrapper. NVIDIA GPU runtime; no hardware-scale training attempted.

**Inputs:** Isaac-Cartpole-Direct-v0, explicit seed and recorded number of environments; task dt=1/120 s and decimation=2 in inspected config.

**Data access:** Public source; network robot assets and NVIDIA runtime terms.

### Construct and compare isaaclab

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed pin: git checkout 46dff135f44683f031edf346e544fcfd8456b2bb ``
2. `` Upstream wrapper installation route: ./isaaclab.sh -i rsl_rl ``
3. `` Proposed task selection using inspected train entry point: ./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Cartpole-Direct-v0 --num_envs 64 --seed 42 --headless ``

**Expected outputs:** Training configuration, logs and policy checkpoints; deterministic evaluation episodes; optional USD scene manifest.

**Comparison with the paper:** Compare multiple same-seed and different-seed reward/episode-length curves. A 64-environment teaching run is not the paper throughput experiment; matching Section 4.1 requires exact task, GPU, environment count and timing definition.

**Execution result:** No execution claim; commands were inspected upstream or explicitly marked proposed.

**Execution evidence:** None recorded.

**Blockers:** No local compatible GPU runtime verified; paper benchmark revision/hardware not matched.

**Next action:** Provision an approved GPU runner, pin the paper environment, then run a small complete training/evaluation cycle.

**Gaps:** No local compatible GPU runtime verified; paper benchmark revision/hardware not matched.

### Sources for isaaclab

- [Paper metadata and direct author-code association](https://arxiv.org/abs/2511.04831) (inspected 2026-11-15).
- [Section 3.7.3 names classic tasks; Section 4.1 defines throughput](https://arxiv.org/html/2511.04831v1) (inspected 2026-11-15).
- [Concrete model timestep/rewards/reset configuration](https://github.com/isaac-sim/IsaacLab/blob/46dff135f44683f031edf346e544fcfd8456b2bb/source/isaaclab_tasks/isaaclab_tasks/direct/cartpole/cartpole_env.py) (inspected 2026-11-15).
- [Training wrapper route](https://github.com/isaac-sim/IsaacLab/blob/46dff135f44683f031edf346e544fcfd8456b2bb/docs/source/overview/reinforcement-learning/rl_existing_scripts.rst) (inspected 2026-11-15).

## mujoco

**MuJoCo** — Can we run the paper Cartpole environment and reproduce its explicit quaternion example?

**Route:** Software paper example. **Execution:** Example executed. **Source confidence:** high.

### Paper for mujoco

Yuval Tassa et al. (2018). [DeepMind Control Suite](https://arxiv.org/abs/1801.00690). arXiv:1801.00690v1.

**Publication type:** preprint. [Primary metadata](https://arxiv.org/abs/1801.00690). Metadata verification: confirmed. Full-text access: Open manuscript HTML inspected

**Target in the paper:** Section 4 suite.load Cartpole swingup and reset/step episode example; Section 5 quaternion-to-matrix example.

### Code and inputs for mujoco

[Artifact or upstream source](https://github.com/google-deepmind/dm_control). Paper explicitly releases DeepMind Control Suite, powered by MuJoCo. Modern package differs from 2018 engine.

**Source inspected:** yes. **Ref:** main at inspection. **Commit:** d7e52e3602a555df6cc20cc928ea5b41e9920158.

**Files:** dm_control/suite/cartpole.py; dm_control/suite/cartpole.xml; README.md

**Terms:** Apache-2.0; MuJoCo Apache-2.0

**Environment and compute:** Isolated Python 3.12; dm-control==1.0.52; freeze all resolved MuJoCo dependencies. CPU; omit rendering to avoid display dependency.

**Inputs:** Paper Cartpole swingup; seed=42 for environment and action generator; quaternion (0.5,0.5,0.5,0.5).

**Data access:** Public code and bundled MJCF assets.

### Construct and compare mujoco

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Upstream installation: python -m pip install dm-control==1.0.52 ``
2. `` Paper API route: from dm_control import suite; env = suite.load(domain_name="cartpole", task_name="swingup"); env.reset(); env.step(action) ``
3. `` Proposed modern binding for paper Section 5: mujoco.mju_quat2Mat(matrix, quaternion) ``

**Expected outputs:** One full episode trajectory and summary; quaternion matrix compared with explicitly printed paper matrix.

**Comparison with the paper:** Paper matrix is [[0,0,1],[1,0,0],[0,1,0]]. Check exactly with tolerance 1e-12; run the paper episode loop and verify finite states/rewards. These checks do not reproduce learning-algorithm performance curves.

**Execution result:** Modern dm-control 1.0.52: 1000 Cartpole swingup steps over 9.999999999999831 simulated seconds; two seeded episodes exactly identical. Paper Section 5 quaternion matrix matched with zero error (chosen absolute tolerance 1e-12). This is execution of paper software examples, not learning-benchmark reproduction.

**Execution evidence:** [Run receipt](verification/mujoco.json); [Numeric output](verification/mujoco-cartpole-episode.csv); [Numeric output](verification/mujoco-quaternion-matrix.json)

**Blockers:** Modern engine/package differs from 2018; original learning benchmark not attempted.

**Next action:** Execute and retain full episode CSV, package lock, matrix comparison, source and output hashes.

**Gaps:** Modern engine/package differs from 2018; original learning benchmark not attempted.

### Sources for mujoco

- [Paper metadata](https://arxiv.org/abs/1801.00690) (inspected 2026-11-15).
- [Actual example API and printed matrix](https://arxiv.org/html/1801.00690v1) (inspected 2026-11-15).
- [Author task implementation](https://github.com/google-deepmind/dm_control/blob/d7e52e3602a555df6cc20cc928ea5b41e9920158/dm_control/suite/cartpole.py) (inspected 2026-11-15).
- [Installation and supported simulation backend](https://github.com/google-deepmind/dm_control/blob/d7e52e3602a555df6cc20cc928ea5b41e9920158/README.md) (inspected 2026-11-15).

## gz-sim

**Gazebo** — Do isolated same-seed PPO runs produce identical checkpoints and evaluation curves?

**Route:** Paper result candidate. **Execution:** Example executed. **Source confidence:** high.

### Paper for gz-sim

Amal Dev Haridevan; Junjie Kang; Jinjun Shan (2026). [GzDRL: Reproducible and Scalable Deep Reinforcement Learning with Gazebo](https://arxiv.org/abs/2609.13243). arXiv:2609.13243v1.

**Publication type:** preprint. [Primary metadata](https://arxiv.org/abs/2609.13243). Metadata verification: confirmed. Full-text access: Open preprint HTML inspected; manuscript says submitted to IEEE, publication not established

**Target in the paper:** Section V-B, Figure 6, Table II: process-isolated same-seed and different-seed PPO reproducibility.

### Code and inputs for gz-sim

[Artifact or upstream source](https://github.com/amaldevh/gz-drl). Exact author paper artifact, explicitly labeled research artifact; paper links same repository.

**Source inspected:** yes. **Ref:** HEAD at inspection. **Commit:** 3e5c5f9a62c1160b3b2889e6d34d794a5361e178.

**Files:** experiments_paper/reproducability_validation/README.md; experiments_paper/reproducability_validation/config.json; experiments_paper/reproducability_validation/run_experiment.py; experiments_paper/reproducability_validation/verify_determinism.py

**Terms:** MIT; Gazebo/dependency notices separate

**Environment and compute:** Upstream Gazebo/DRLServer C++ build prerequisites plus Python RL extra; freeze compiler, Gazebo and SB3 versions. CPU physics and PPO; 10 full training runs. Paper hardware must be recorded for throughput claims.

**Inputs:** Author config: 5 same-seed runs with seed 42; different seeds {1,5,25,42,125}; eight environments; 500000 timesteps; checkpoints every 50000; 20 deterministic evaluation episodes.

**Data access:** Public code and bundled config; no private data indicated.

### Construct and compare gz-sim

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Upstream installation, from repository root after native build: python -m pip install -e '.[rl]' ``
2. `` cd experiments_paper/reproducability_validation ``
3. `` python run_experiment.py ``

**Expected outputs:** results/determinism_check.json; per-run checkpoint/evaluation data; analysis CSV, plots, LaTeX table and machine/config manifest.

**Comparison with the paper:** Same-seed determinism is supported by full author-code execution and independent parameter hashing. The published numerical final return is not reproduced; no tolerance is invented. Historical package/compiler lock is not established, and this portablebuild uses Gazebo10.6/GCC15 plus a mechanical constructor-disambiguation patch. Different-seed row was not run. Human scientific review pending.

**Execution result:** Completed all5full same-seed500000-requested-step training runs and1200evaluation episodes. Author preflight and independent12-checkpoint parameter identity checks pass; finalreturn16.53217 differs from paper18.43.

**Execution evidence:** [Author-code attempt](../reproductions/gz-sim.md); [Run record](../reproductions/records/gz-sim.json)

**Blockers:** Paper final-return18.43not reproduced (actual16.53217); original package/compiler lock and exactpaperartifactversionnot established.; Different-seedTableIIrownot run.

**Next action:** Review native task/config/environment differences with paper authors; reproduce the original score only after exact software/config provenance is resolved.

**Gaps:** Paper final-return18.43not reproduced (actual16.53217); original package/compiler lock and exactpaperartifactversionnot established.; Different-seedTableIIrownot run.

### Sources for gz-sim

- [Paper metadata](https://arxiv.org/abs/2609.13243) (inspected 2026-11-15).
- [Specific Table II result and full experiment settings](https://arxiv.org/html/2609.13243v1) (inspected 2026-11-15).
- [Exact author run commands and output contract](https://github.com/amaldevh/gz-drl/blob/3e5c5f9a62c1160b3b2889e6d34d794a5361e178/experiments_paper/reproducability_validation/README.md) (inspected 2026-11-15).

## webots

**Webots** — Can a Webots Cartpole learn balancing through the paper Deepbots interface?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for webots

Manos Kirtas; Konstantinos Tsampazis; Nikolaos Passalis; Anastasios Tefas (2020). [Deepbots: A Webots-Based Deep Reinforcement Learning Framework for Robotics](https://doi.org/10.1007/978-3-030-49186-4_6). 10.1007/978-3-030-49186-4_6.

**Publication type:** conference_paper. [Primary metadata](https://api.crossref.org/works/10.1007/978-3-030-49186-4_6). Metadata verification: confirmed. Full-text access: PMC article search text and author docs inspected; direct PMC open was access challenged

**Target in the paper:** Section 4 use cases and Cartpole code examples; exact published learning-curve settings require full-text comparison.

### Code and inputs for webots

[Artifact or upstream source](https://github.com/aidudezzz/deepworlds). Official Deepbots documentation links deepworlds as its example repository; current examples implement author framework but are not a pinned 2020 artifact.

**Source inspected:** yes. **Ref:** HEAD at inspection. **Commit:** 4f21e555216750a4aafb84baad261aeda7cb1f74.

**Files:** examples/cartpole/README.md; examples/cartpole/cartpole_discrete/worlds/cartpole_world_robot_supervisor.wbt; examples/cartpole/cartpole_discrete/controllers/robot_supervisor_manager/PPO_runner.py

**Terms:** Review deepworlds/deepbots license and Webots asset notices before copying code; Webots Apache-2.0

**Environment and compute:** Webots plus matching Python deepbots/PyTorch/Gym requirements from chosen example. CPU simulation and small neural network; Webots native runtime required.

**Inputs:** Discrete-action Cartpole world, robot-supervisor scheme and PPO agent; retain seeds, episode lengths and reset settings.

**Data access:** Public author code and robot world; no private dataset.

### Construct and compare webots

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Upstream concrete route: install the selected example requirements, open examples/cartpole/cartpole_discrete/worlds/cartpole_world_robot_supervisor.wbt in Webots, and run the supervisor PPO controller. ``
2. `` Proposed automation: record environment/controller versions, log episode reward and evaluate a frozen checkpoint over fixed-seed episodes. ``

**Expected outputs:** Episode reward plot and trained agent as illustrated in authors README; retain policy and per-episode logs.

**Comparison with the paper:** Compare against paper Section 4 Cartpole result after recovering its original settings; current README rewardPlot.png is a lead, not an established paper numeric target.

**Execution result:** No execution claim; commands were inspected upstream or explicitly marked proposed.

**Execution evidence:** None recorded.

**Blockers:** Historical Deepbots/Webots/Gym versions not matched; paper curve not digitized; native runtime unavailable.

**Next action:** Retrieve full text via legitimate route and map the current world to the paper use case before accepting a reproduction target.

**Gaps:** Historical Deepbots/Webots/Gym versions not matched; paper curve not digitized; native runtime unavailable.

### Sources for webots

- [Title/authors/year/DOI verified live](https://api.crossref.org/works/10.1007/978-3-030-49186-4_6) (inspected 2026-11-15).
- [Author framework citation and official deepworlds link](https://deepbots.readthedocs.io/en/latest/index.html) (inspected 2026-11-15).
- [Concrete world/controller routes and existing reward plot](https://github.com/aidudezzz/deepworlds/blob/4f21e555216750a4aafb84baad261aeda7cb1f74/examples/cartpole/README.md) (inspected 2026-11-15).

## bullet3

**Bullet / PyBullet** — Can the released Minitaur trotting and galloping controllers be replayed?

**Route:** Paper result candidate. **Execution:** Example executed. **Source confidence:** high.

### Paper for bullet3

Jie Tan; Tingnan Zhang; Erwin Coumans; Atil Iscen; Yunfei Bai; Danijar Hafner; Steven Bohez; Vincent Vanhoucke (2018). [Sim-to-Real: Learning Agile Locomotion For Quadruped Robots](https://arxiv.org/abs/1804.10332). arXiv:1804.10332v2.

**Publication type:** conference_paper. [Primary metadata](https://arxiv.org/abs/1804.10332). Metadata verification: confirmed. Full-text access: Open abstract and author environment README inspected; detailed experimental section not audited

**Target in the paper:** Paper trotting and galloping policies; authors README explicitly identifies the two exact environments used.

### Code and inputs for bullet3

[Artifact or upstream source](https://github.com/bulletphysics/bullet3). Author README explicitly states these two environments were used in the paper and links pre-trained PPO examples.

**Source inspected:** yes. **Ref:** master at inspection. **Commit:** d3afe76132fc76b0f9b2359cbaef47a3766e7fbb.

**Files:** examples/pybullet/gym/pybullet_envs/minitaur/envs/README.md; examples/pybullet/gym/pybullet_envs/minitaur/envs/minitaur_reactive_env.py; examples/pybullet/gym/pybullet_envs/minitaur/envs/minitaur_trotting_env.py; examples/pybullet/gym/pybullet_data/policies/ppo/minitaur_trotting_env/config.yaml

**Terms:** Zlib core; separate example/model/checkpoint dependency notices

**Environment and compute:** Historical TensorFlow-1-style PPO environment, Gym, ruamel.yaml and compatible PyBullet; inspect imports and resolve original versions before installation. CPU policy replay possible with legacy-compatible dependencies; training and physical testing are separate.

**Inputs:** Bundled Minitaur URDF, PPO checkpoint/config and paper motor/latency/randomization configuration.

**Data access:** Public source, bundled checkpoints and model; review individual asset notices.

### Construct and compare bullet3

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Upstream README: pip install gym; pip install ruamel.yaml ``
2. `` Upstream, from example directory with dependencies available: python minitaur_reactive_env_example.py ``
3. `` Upstream: python minitaur_trotting_env_example.py ``

**Expected outputs:** Policy rollouts, robot states/actions and gait trajectories; archive raw logs and exact checkpoint hashes.

**Comparison with the paper:** Released policies execute, but published simulation speeds are not reproduced by matched methods/checkpoints. Trot mean0.9215m/s versus paper approximately0.50; gallop mean1.3084 with SD0.5209 and only2/5 complete. No physical sim-to-real claim.

**Execution result:** Replayed author frozen PPO policies for five seeds per gait; all numerical traces retained.

**Execution evidence:** [Author-code attempt](../reproductions/bullet3.md); [Run record](../reproductions/records/bullet3.json)

**Blockers:** Published TableII policy widths/checkpoint selection not matched; native physics revision not2018; no physical robot evaluation.

**Next action:** Recover paper-specific checkpoint/environment; agree the speed estimator and tolerance, then compare with repeated episodes.

**Gaps:** Published TableII policy widths/checkpoint selection not matched; native physics revision not2018; no physical robot evaluation.

### Sources for bullet3

- [Primary metadata and declared trotting/galloping outcomes](https://arxiv.org/abs/1804.10332) (inspected 2026-11-15).
- [Explicit author association, released environments and replay commands](https://github.com/bulletphysics/bullet3/blob/d3afe76132fc76b0f9b2359cbaef47a3766e7fbb/examples/pybullet/gym/pybullet_envs/minitaur/envs/README.md) (inspected 2026-11-15).

## chrono

**Project Chrono** — How do steering and terrain inputs affect a template-based HMMWV model?

**Route:** Software paper example. **Execution:** Not run. **Source confidence:** medium.

### Paper for chrono

Radu Serban; Michael Taylor; Dan Negrut; Alessandro Tasora (2019). [Chrono::Vehicle: template-based ground vehicle modelling and simulation](https://doi.org/10.1504/IJVP.2019.097096). 10.1504/IJVP.2019.097096.

**Publication type:** journal_article. [Primary metadata](https://api.crossref.org/works/10.1504/IJVP.2019.097096). Metadata verification: confirmed. Full-text access: Publisher abstract and metadata inspected; full text not inspected

**Target in the paper:** Software architecture and ground-vehicle modeling demonstration; exact paper figure/model identification pending full text.

### Code and inputs for chrono

[Artifact or upstream source](https://github.com/projectchrono/chrono). Official current HMMWV example is by Chrono authors and uses Chrono::Vehicle, the module described in the paper. It is not established as the exact 2019 experiment.

**Source inspected:** yes. **Ref:** main at inspection. **Commit:** c2865ec31e5913838898bf9c13b1bba66804db3e.

**Files:** src/demos/python/vehicle/demo_VEH_HMMWV.py

**Terms:** BSD-3-Clause code; model/data notices separate

**Environment and compute:** PyChrono with vehicle and Irrlicht modules, matching supplied vehicle data; prefer a supported binary environment over rebuilding all modules. CPU multibody dynamics; display support for unmodified Irrlicht demo.

**Inputs:** Upstream HMMWV_Full, terrain, driver and tire settings in demo; replace interactive driver with a saved deterministic input only as a documented adaptation.

**Data access:** Public model code and bundled vehicle data.

### Construct and compare chrono

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed from a matching PyChrono environment: python src/demos/python/vehicle/demo_VEH_HMMWV.py ``

**Expected outputs:** Interactive vehicle demo; for reproducibility add logged vehicle position, speed, steering input and model configuration.

**Comparison with the paper:** First check finite state and repeatability under recorded driver input. Identify the paper figure and mesh/tire/terrain settings before comparing published trajectories or response curves.

**Execution result:** No execution claim; commands were inspected upstream or explicitly marked proposed.

**Execution evidence:** None recorded.

**Blockers:** Full article and exact published model/response not inspected; demo is interactive and current API differs from 2019.

**Next action:** Obtain author manuscript from official Chrono whitepaper list, extract a target figure, then choose its matching model version.

**Gaps:** Full article and exact published model/response not inspected; demo is interactive and current API differs from 2019.

### Sources for chrono

- [Verified live DOI/title/authors](https://api.crossref.org/works/10.1504/IJVP.2019.097096) (inspected 2026-11-15).
- [Primary publication record and abstract](https://www.inderscience.com/info/inarticle.php?artid=97096) (inspected 2026-11-15).
- [Concrete author HMMWV model and dependencies](https://github.com/projectchrono/chrono/blob/c2865ec31e5913838898bf9c13b1bba66804db3e/src/demos/python/vehicle/demo_VEH_HMMWV.py) (inspected 2026-11-15).

## sofa

**SOFA** — How does tendon displacement bend a finite-element soft finger?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for sofa

Eulalie Coevoet et al. (2017). [Software toolkit for modeling, simulation, and control of soft robots](https://doi.org/10.1080/01691864.2017.1395362). 10.1080/01691864.2017.1395362.

**Publication type:** journal_article. [Primary metadata](https://api.crossref.org/works/10.1080/01691864.2017.1395362). Metadata verification: confirmed. Full-text access: Publisher abstract and author publication metadata inspected; full model/results not inspected

**Target in the paper:** Direct forward soft-robot simulation described in article; current CableConstraint/Finger.py is an author-associated teaching model, not a verified exact figure.

### Code and inputs for sofa

[Artifact or upstream source](https://github.com/SofaDefrost/SoftRobots). The paper presents the SOFA-based toolkit. Current official plugin source supplies a cable-driven FEM finger; paper-specific historical mesh and constants are unverified.

**Source inspected:** yes. **Ref:** master at inspection. **Commit:** 3dadbaff9f50b379bf1cc680b379b74810751ee0.

**Files:** examples/component/constraint/CableConstraint/Finger.py; examples/component/constraint/CableConstraint/FingerController.py; examples/component/constraint/CableConstraint/mesh/finger.vtk

**Terms:** SoftRobots LGPL-3.0 according to live repository license metadata; SOFA LGPL-2.1; dependencies separate

**Environment and compute:** SOFA with matching SoftRobots and SofaPython3 plugins; preserve full component/plugin versions. CPU FEM; SOFA native runtime and plugins; optional display.

**Inputs:** Bundled finger mesh; source sets dt=0.01 and gravity=[0,-9810,0] in model units; inspect and retain material, constraint and actuator definitions.

**Data access:** Public source and supplied mesh; verify mesh redistribution terms.

### Construct and compare sofa

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed supported-runner route: runSofa examples/component/constraint/CableConstraint/Finger.py ``
2. `` Proposed reproducibility adaptation: drive a saved tendon-displacement series and export tip displacement and solver residuals. ``

**Expected outputs:** Deformed finger scene and, after instrumentation, displacement-vs-actuation series and convergence logs.

**Comparison with the paper:** Compare paper actuator/mesh/material settings and a specific deflection curve after full text is obtained. A plausible bending animation or converged linear solve does not establish paper reproduction.

**Execution result:** No execution claim; commands were inspected upstream or explicitly marked proposed.

**Execution evidence:** None recorded.

**Blockers:** Exact 2017 model, mesh, material parameters and numeric target not matched; native plugin stack unavailable.

**Next action:** Retrieve legitimate author manuscript, map one forward cable-actuation experiment, then instrument exact mesh and loading.

**Gaps:** Exact 2017 model, mesh, material parameters and numeric target not matched; native plugin stack unavailable.

### Sources for sofa

- [Verified live primary citation metadata](https://api.crossref.org/works/10.1080/01691864.2017.1395362) (inspected 2026-11-15).
- [Paper links toolkit and states SOFA modeling relation](https://www.tandfonline.com/doi/full/10.1080/01691864.2017.1395362) (inspected 2026-11-15).
- [Actual mesh/plugin/actuator scene source](https://github.com/SofaDefrost/SoftRobots/blob/3dadbaff9f50b379bf1cc680b379b74810751ee0/examples/component/constraint/CableConstraint/Finger.py) (inspected 2026-11-15).
