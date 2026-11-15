# Robot learning with OpenUSD, Isaac Sim, and Isaac Lab

**Question:** How can a robot-learning experiment share scenes, tasks, and training settings?

[Mittal et al. (2023)](https://doi.org/10.1109/LRA.2023.3270034) describe Orbit in *IEEE Robotics and Automation Letters*. Read the [open manuscript](https://arxiv.org/html/2301.04195v2), especially Section III's world and task architecture and Section V's learning examples. Orbit is the predecessor of Isaac Lab. Running a current Isaac Lab task does not reproduce the paper's reported training results.

## Understand the three tools

| Tool | What it contributes | First resource |
| --- | --- | --- |
| OpenUSD | Scene composition, assets, transforms, and time-sampled data | [Official tutorials](https://openusd.org/release/tut_usd_tutorials.html) |
| Isaac Sim | The robot simulator, physics integration, sensors, and rendering | [Simulator documentation](https://docs.isaacsim.omniverse.nvidia.com/) |
| Isaac Lab | Task environments and learning workflows built on the simulator | [Versioned setup guide](https://isaac-sim.github.io/IsaacLab/v2.2.0/source/setup/installation/index.html) |

OpenUSD is a scene system, not a dynamics solver. Isaac Sim's source license is Apache-2.0; Omniverse Kit and assets carry additional terms. Isaac Lab's core is BSD-3-Clause. Consult the [catalog](../catalog.md) for source and license links. A complete Isaac installation is not an entirely open-source dependency stack.

## Try a bounded training run

This route deliberately uses **Isaac Lab v2.2.0 with Isaac Sim 5.0.0**, rather than assuming that current main has the same scripts. Follow that version's installation and hardware requirements first. It needs a compatible NVIDIA GPU; the local CPU examples do not install this runtime.

```sh
git clone --branch v2.2.0 https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab
```

After completing the versioned setup, run:

```sh
./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Reach-Franka-v0 --num_envs 64 --max_iterations 10 --seed 42 --headless
```

The [training entry point](https://github.com/isaac-sim/IsaacLab/blob/v2.2.0/scripts/reinforcement_learning/rsl_rl/train.py) and [Franka reach task registration](https://github.com/isaac-sim/IsaacLab/blob/v2.2.0/source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/reach/config/franka/__init__.py) were checked. Ten iterations are a setup exercise, not a trained-policy benchmark. Retain the generated logs, configuration, checkpoint, exact commit, GPU model, driver, runtime, and asset versions.

Inspect the task's observation, action, reward, reset, and success definitions before interpreting its learning curve. A research comparison needs a fixed evaluation procedure, multiple seeds, and the paper's environment and training settings. A high return does not establish real-world robot performance.

## Work without the GPU runtime

Use the [CPU result-to-USD example](cpu-walkthroughs.md#results-in-openusd) to inspect a stage, attributes, units, and source provenance. It exchanges a battery solver's output; it does not implement Orbit's robot experiment. For robot dynamics without this NVIDIA runtime, compare MuJoCo, Gazebo, Webots, and Drake in the catalog.

**Status:** Paper architecture, versioned documentation, task, and training script inspected on 2026-11-15. GPU installation and training not executed here.
