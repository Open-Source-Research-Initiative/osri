# Replay the released Minitaur policies on CPU

Tan et al. (2018), [Sim-to-Real: Learning Agile Locomotion For Quadruped Robots](https://arxiv.org/abs/1804.10332), release their trotting and galloping environments and PPO checkpoints in Bullet. This example replays those author policies with a legacy TensorFlow environment and records every state/action step.

Use Python 3.7 with TensorFlow 1.15.5, NumPy 1.18.5, PyBullet 3.2.5, Gym 0.17.3 and ruamel.yaml 0.16.13. Clone `bulletphysics/bullet3` at `d3afe76132fc76b0f9b2359cbaef47a3766e7fbb` under `sources/bullet3`. Apply the included `bullet-compatibility.patch` to replace the upstream non-existent `tf` module import with the TensorFlow 1 module. Keep the source, checkpoints and their license notices in place. Run `python run_minitaur.py` from this example directory with two BLAS/TensorFlow threads.

The adapter invokes the author configuration loader and `SimplePPOPolicy`, restores `model.ckpt-14000000`, disables display, and runs seeds 0–4 for at most 1,000 control steps each. The physics time step, motor and latency model remain in the author environment. Output CSV files record simulation time, base position, reward, observation and action. `summary.json` records each episode and aggregate speed variability.

Five trotting episodes completed 1,000 steps (six simulated seconds). Mean forward speed was 0.921524 m/s (sample SD 0.035527). Two of five galloping episodes completed; mean speed across the five variable-length episodes was 1.308420 m/s (SD 0.520918). Short episodes and stalled trajectories remain in the record.

Section VI-A reports simulation trotting speed roughly 0.50 m/s and galloping 1.34 m/s. Our episode-average estimator includes startup; the paper does not specify an equivalent speed estimator. More importantly, the released checkpoint network widths differ from paper Table II: trotting (133, 100) versus (125, 89), and galloping (114, 45) versus (185, 95). Current PyBullet also differs from the historical engine. These results demonstrate execution and expose a reproduction gap; they do not establish the paper speeds or physical transfer. Human scientific review remains pending.

## Download the recorded files

- [reactive-seed0.csv](files/bullet3/external/robotics/bullet-output/reactive-seed0.csv) — raw trajectory.
- [reactive-seed1.csv](files/bullet3/external/robotics/bullet-output/reactive-seed1.csv) — raw trajectory.
- [reactive-seed2.csv](files/bullet3/external/robotics/bullet-output/reactive-seed2.csv) — raw trajectory.
- [reactive-seed3.csv](files/bullet3/external/robotics/bullet-output/reactive-seed3.csv) — raw trajectory.
- [reactive-seed4.csv](files/bullet3/external/robotics/bullet-output/reactive-seed4.csv) — raw trajectory.
- [summary.json](files/bullet3/external/robotics/bullet-output/summary.json) — aggregate run summary.
- [trotting-seed0.csv](files/bullet3/external/robotics/bullet-output/trotting-seed0.csv) — raw trajectory.
- [trotting-seed1.csv](files/bullet3/external/robotics/bullet-output/trotting-seed1.csv) — raw trajectory.
- [trotting-seed2.csv](files/bullet3/external/robotics/bullet-output/trotting-seed2.csv) — raw trajectory.
- [trotting-seed3.csv](files/bullet3/external/robotics/bullet-output/trotting-seed3.csv) — raw trajectory.
- [trotting-seed4.csv](files/bullet3/external/robotics/bullet-output/trotting-seed4.csv) — raw trajectory.
- [trajectories.png](files/bullet3/external/robotics/bullet-output/trajectories.png) — plot of actual simulated trajectories.
- [trajectories.svg](files/bullet3/external/robotics/bullet-output/trajectories.svg) — plot of actual simulated trajectories.
- [run_minitaur.py](files/bullet3/run_minitaur.py) — portable driver or environment/source record.
- [compatibility.patch](files/bullet3/compatibility.patch) — portable driver or environment/source record.
- [requirements.txt](files/bullet3/requirements.txt) — portable driver or environment/source record.
- [requirements-tested.txt](files/bullet3/requirements-tested.txt) — portable driver or environment/source record.
- [fetch-source.sh](files/bullet3/fetch-source.sh) — portable driver or environment/source record.

[Complete run record](records/bullet3.json) · [All candidate attempts](README.md). Human scientific review is pending.
