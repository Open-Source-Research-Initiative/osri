# Repeat the author GzDRL same-seed PPO experiment

[Haridevan, Kang and Shan](https://arxiv.org/abs/2609.13243) present GzDRL in a 2026 preprint. Section V-B, Figure 6 and Table II compare process-isolated PPO runs with identical and different seeds. This example executes their released same-seed research artifact on CPU and compares its actual checkpoint parameters and evaluation returns with the paper.

Create an isolated conda environment from environment.yml. The checked Linux build is recorded in environment-explicit.txt; Python packages are recorded in requirements-tested.txt. Run `sh fetch-source.sh` inside the activated environment, then `sh run.sh`. Source is pinned to `3e5c5f9a62c1160b3b2889e6d34d794a5361e178`. The author code is MIT, with separate Gazebo and bundled EnvPool dependency notices. Keep its LICENSE/THIRD_PARTY_NOTICES files.

This portable build uses conda-forge Gazebo 10.6.0 and GCC 15 instead of the authors GCC 11 system installation. A mechanical compatibility patch disambiguates 22 scalar-bound constructor calls with explicit `std::tuple<float,float>`; dynamics and task logic were not edited. The source needed that patch to compile with this toolchain. CPU PyTorch 2.7.1 and Stable Baselines3 2.7.0 were used. The historical paper dependency lock is not established.

The unmodified author configuration trains five independent processes with seed 42, eight environments, domain randomization disabled, 500,000 requested timesteps and checkpoints every 50,000 steps. PPO's rollout batching produces 501,760 actual timesteps. Every checkpoint is evaluated over 20 fixed-seed episodes in a fresh process with saved observation normalization restored and frozen. The different-seed row of Table II is outside this run.

The author preflight check passed all five hashes: initial observations, a fixed transition sequence, initial policy, one-PPO-update policy and normalization state. An independent state-dictionary check also found identical parameters across all five runs at all 12 saved checkpoint positions. Zip archive timestamps are excluded from that parameter comparison.

The paper reports same-seed return 18.43 ± 0.00 and 100% identical checkpoints. Across all five completed runs, final return was 16.53216975 ± 0.00 across runs. Each checkpoint received 20 fixed-seed evaluation episodes, totaling 1,200 evaluations. Within-run final episode-return SD was 14.98144; final episode-length success rate was 0.55. The trained parameters and evaluation curves were identical across processes. The checkpoint determinism claim is supported by this run; the paper's numerical return is not reproduced. There is no invented acceptance tolerance for its rounded return, and software/compiler differences remain material.

Keep raw episode CSVs, the preflight record, independent policy comparison, effective configuration and author analysis outputs. Human scientific review remains pending. A full training/evaluation run here supplies concrete evidence for a useful Lab example while preserving the disagreement with the paper.

## Download the recorded files

- [checkpoint_variability.csv](files/gz-sim/external/robotics/gazebo-results/analysis/checkpoint_variability.csv) — native analysis/evaluation data.
- [table_training_reproducibility.tex](files/gz-sim/external/robotics/gazebo-results/analysis/table_training_reproducibility.tex) — native analysis/evaluation data.
- [fig_training_variability.png](files/gz-sim/external/robotics/gazebo-results/analysis/fig_training_variability.png) — native analysis/evaluation data.
- [training_reproducibility_summary.csv](files/gz-sim/external/robotics/gazebo-results/analysis/training_reproducibility_summary.csv) — native analysis/evaluation data.
- [final_run_statistics.csv](files/gz-sim/external/robotics/gazebo-results/analysis/final_run_statistics.csv) — native analysis/evaluation data.
- [fig_training_reproducibility.png](files/gz-sim/external/robotics/gazebo-results/analysis/fig_training_reproducibility.png) — native analysis/evaluation data.
- [fig_training_reproducibility.svg](files/gz-sim/external/robotics/gazebo-results/analysis/fig_training_reproducibility.svg) — native analysis/evaluation data.
- [analysis_manifest.json](files/gz-sim/external/robotics/gazebo-results/analysis/analysis_manifest.json) — native analysis/evaluation data.
- [checkpoint_run_statistics.csv](files/gz-sim/external/robotics/gazebo-results/analysis/checkpoint_run_statistics.csv) — native analysis/evaluation data.
- [fig_training_variability.svg](files/gz-sim/external/robotics/gazebo-results/analysis/fig_training_variability.svg) — native analysis/evaluation data.
- [determinism_check.json](files/gz-sim/external/robotics/gazebo-results/determinism_check.json) — native analysis/evaluation data.
- [effective_config.json](files/gz-sim/external/robotics/gazebo-results/effective_config.json) — native analysis/evaluation data.
- [gazebo-independent-policy-comparison.json](files/gz-sim/external/robotics/gazebo-independent-policy-comparison.json) — native analysis/evaluation data.
- [gazebo-comparison.json](files/gz-sim/external/robotics/gazebo-comparison.json) — native analysis/evaluation data.
- [checkpoint_evaluations.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/checkpoint_evaluations.csv) — native analysis/evaluation data.
- [monitor.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/monitor.csv) — native analysis/evaluation data.
- [metadata.json](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/metadata.json) — native analysis/evaluation data.
- [checkpoint_250000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_250000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_100000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_100000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_50000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_50000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_500000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_500000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_501760_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_501760_episodes.csv) — native analysis/evaluation data.
- [checkpoint_450000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_450000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_0_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_0_episodes.csv) — native analysis/evaluation data.
- [checkpoint_350000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_350000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_200000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_200000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_300000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_300000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_400000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_400000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_150000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/fixed_evaluation/checkpoint_150000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_evaluations.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/checkpoint_evaluations.csv) — native analysis/evaluation data.
- [monitor.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/monitor.csv) — native analysis/evaluation data.
- [metadata.json](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/metadata.json) — native analysis/evaluation data.
- [checkpoint_250000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_250000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_100000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_100000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_50000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_50000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_500000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_500000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_501760_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_501760_episodes.csv) — native analysis/evaluation data.
- [checkpoint_450000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_450000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_0_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_0_episodes.csv) — native analysis/evaluation data.
- [checkpoint_350000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_350000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_200000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_200000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_300000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_300000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_400000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_400000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_150000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_02_seed_42/fixed_evaluation/checkpoint_150000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_evaluations.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/checkpoint_evaluations.csv) — native analysis/evaluation data.
- [monitor.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/monitor.csv) — native analysis/evaluation data.
- [metadata.json](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/metadata.json) — native analysis/evaluation data.
- [checkpoint_250000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_250000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_100000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_100000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_50000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_50000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_500000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_500000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_501760_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_501760_episodes.csv) — native analysis/evaluation data.
- [checkpoint_450000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_450000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_0_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_0_episodes.csv) — native analysis/evaluation data.
- [checkpoint_350000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_350000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_200000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_200000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_300000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_300000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_400000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_400000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_150000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_03_seed_42/fixed_evaluation/checkpoint_150000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_evaluations.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/checkpoint_evaluations.csv) — native analysis/evaluation data.
- [monitor.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/monitor.csv) — native analysis/evaluation data.
- [metadata.json](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/metadata.json) — native analysis/evaluation data.
- [checkpoint_250000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_250000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_100000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_100000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_50000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_50000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_500000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_500000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_501760_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_501760_episodes.csv) — native analysis/evaluation data.
- [checkpoint_450000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_450000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_0_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_0_episodes.csv) — native analysis/evaluation data.
- [checkpoint_350000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_350000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_200000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_200000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_300000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_300000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_400000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_400000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_150000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_04_seed_42/fixed_evaluation/checkpoint_150000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_evaluations.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/checkpoint_evaluations.csv) — native analysis/evaluation data.
- [monitor.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/monitor.csv) — native analysis/evaluation data.
- [metadata.json](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/metadata.json) — native analysis/evaluation data.
- [checkpoint_250000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_250000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_100000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_100000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_50000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_50000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_500000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_500000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_501760_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_501760_episodes.csv) — native analysis/evaluation data.
- [checkpoint_450000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_450000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_0_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_0_episodes.csv) — native analysis/evaluation data.
- [checkpoint_350000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_350000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_200000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_200000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_300000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_300000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_400000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_400000_episodes.csv) — native analysis/evaluation data.
- [checkpoint_150000_episodes.csv](files/gz-sim/external/robotics/gazebo-results/same_seed/run_05_seed_42/fixed_evaluation/checkpoint_150000_episodes.csv) — native analysis/evaluation data.
- [model_501760_steps.zip](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/checkpoints/model_501760_steps.zip) — trainedpolicy/normalizer.
- [model_vecnormalize_501760_steps.pkl](files/gz-sim/external/robotics/gazebo-results/same_seed/run_01_seed_42/checkpoints/model_vecnormalize_501760_steps.pkl) — trainedpolicy/normalizer.
- [run.sh](files/gz-sim/run.sh) — portable driver or environment/source record.
- [environment.yml](files/gz-sim/environment.yml) — portable driver or environment/source record.
- [requirements.txt](files/gz-sim/requirements.txt) — portable driver or environment/source record.
- [compatibility.patch](files/gz-sim/compatibility.patch) — portable driver or environment/source record.
- [fetch-source.sh](files/gz-sim/fetch-source.sh) — portable driver or environment/source record.
- [config.json](files/gz-sim/config.json) — portable driver or environment/source record.
- [requirements-tested.txt](files/gz-sim/requirements-tested.txt) — portable driver or environment/source record.
- [environment-explicit.txt](files/gz-sim/environment-explicit.txt) — portable driver or environment/source record.

[Complete run record](records/gz-sim.json) · [All candidate attempts](README.md). Human scientific review is pending.
