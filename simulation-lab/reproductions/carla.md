# Run a CARLA 0.8.4 benchmark subset on CPU

[Dosovitskiy et al. (2017)](https://proceedings.mlr.press/v78/dosovitskiy17a.html) evaluate urban driving with goal completion and infractions in CARLA. The official [driving-benchmarks repository](https://github.com/carla-simulator/driving-benchmarks) provides the CoRL2017 task suite for the later CARLA 0.8.4 release.

This example runs three original straight-route pose pairs with the authors trivial ForwardAgent. It disables camera rendering to exercise the native physics and benchmark metrics on a machine without an NVIDIA GPU. Original paper MP/IL/RL model weights have not been matched; this is a benchmark adaptation, not a reproduction of their success rates.

Use an isolated Python 3.7 environment and the included requirements. Retrieve the official 0.8.4 Linux binary through its GitHub release link, verify the archive hash in provenance.json, and extract it into carla084. Run fetch-source.sh after placing the archive beside it; this retrieves the pinned benchmark source and applies compatibility changes. The changes replace explicit generator StopIteration with return (Python PEP 479) and replace a NaN print threshold with a finite one (display formatting only).

Run `python launch_carla.py --attempt 1 --client carla_benchmark_subset.py`. The launcher starts the original Unreal server in headless/nullRHI mode, runs the author benchmark, and stops its own server. Keep its native CSV files under `_benchmarks_results` and summary under `carla-output`.

The checked run used Town01, WeatherId 1, no other actors and pose pairs 36→40, 39→35, and 110→114. All three reached the goal with zero recorded collisions. Completion times were 8.3, 8.3, and 7.8 simulation seconds, leaving 0.2231, 0.2231, and 0.9137 meters to the goal. The complete configuration uses 25 pose pairs per task/weather; this example uses 3. Do not infer a population success rate from this subset.

Table 1 reports training-condition straight-route success rates of 98% (MP), 95% (IL), and 89% (RL). Our ForwardAgent and reduced sensor/task setup differ, so 3/3 success is not an estimate of those rates. Reproducing Tables 1 and 2 requires original paper-agent weights, the matched simulator version, rendered sensor inputs and complete evaluation conditions. Runtime/assets retain their bundled terms; benchmark source is MIT. Human scientific review is pending.

## Download the recorded files

- [summary.csv](files/carla/external/robotics/_benchmarks_results/headless-corl2017-subset-1/summary.csv) — native benchmark result.
- [measurements.csv](files/carla/external/robotics/_benchmarks_results/headless-corl2017-subset-1/measurements.csv) — native benchmark result.
- [summary.json](files/carla/external/robotics/carla-output/summary.json) — summary.
- [benchmark-summary.json](files/carla/external/robotics/carla-output/benchmark-summary.json) — summary.
- [trajectory.csv](files/carla/external/robotics/carla-output/trajectory.csv) — native benchmark result.
- [carla_headless_client.py](files/carla/carla_headless_client.py) — portable driver or environment/source record.
- [carla_benchmark_subset.py](files/carla/carla_benchmark_subset.py) — portable driver or environment/source record.
- [launch_carla.py](files/carla/launch_carla.py) — portable driver or environment/source record.
- [requirements.txt](files/carla/requirements.txt) — portable driver or environment/source record.
- [patch-legacy.py](files/carla/patch-legacy.py) — portable driver or environment/source record.
- [fetch-source.sh](files/carla/fetch-source.sh) — portable driver or environment/source record.
- [provenance.json](files/carla/provenance.json) — portable driver or environment/source record.

[Complete run record](records/carla.json) · [All candidate attempts](README.md). Human scientific review is pending.
