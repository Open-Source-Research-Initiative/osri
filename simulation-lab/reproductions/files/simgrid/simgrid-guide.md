# Compare the authors’ SimGrid coordinator-worker models

[Casanova et al. (2025)](https://doi.org/10.1016/j.parco.2025.103125) compare simulator time and memory in **Section 7, Figures 13–14**. Their [open manuscript](https://fred-suter.com/files/publications/simgrid-parco25.pdf), introductory paragraph before Section 2, explicitly calls **SimGrid 3.10 “v3”** and describes development through **3.36**, culminating in v4. Reference 66 links the [coordinator-worker benchmark](https://github.com/simgrid/coordinator_worker_flashback/tree/b09453d19541b7186703f4d651c1bba790461e44), whose Dockerfiles select 3.10 and 3.36.

This example runs those author implementations at the lower and upper workload anchors of Figure 13. The source pins are benchmark `b09453d19541b7186703f4d651c1bba790461e44`, SimGrid 3.10 `9a82cac1b6f73bb342495c39807acd7380e153d5`, and SimGrid 3.36 `7ed73b43153fc79a8c5eb5cff8e9f81e4f52e619`. It does not establish that 3.36 is the exact unnamed development commit used for every plotted paper observation.

## Construct and run

Use Linux, Python 3 with `venv`, git, GCC/G++, GNU `time`, and a compiler-compatible Boost prefix. The [build harness](build-network-tools.sh) and [pinned build requirements](requirements-build.txt) keep downloads, builds and temporary XML inputs inside the example folder. Set `BOOST_ROOT` to the selected Boost prefix, then run:

```sh
bash build-network-tools.sh
SIMGRID_DEPENDENCY_PREFIX="$BOOST_ROOT" python3 run_simgrid.py
python3 analyse_simgrid.py
```

The SimGrid runner independently writes `simgrid-output/runs.json` and its makespan-comparison receipt. Run into a fresh output folder; preserve an earlier run when repeating.

The build applies the exact CMake workaround in the authors’ `Dockerfile_simgrid_v3_10`, runs that old configure from its build directory, and changes two hardcoded `/tmp` XML filenames to the local temporary folder. Numerical model/event logic is unchanged. Both simulator builds use the same GCC 13.3 compiler and optimization level on Ubuntu 24.04. The article used Debian 12 and a dedicated Intel Xeon Platinum 8380 core; this run used one pinned CPU in a shared host. Timing differences therefore remain descriptive local measurements. Primary wall time comes from GNU `time -v`, matching the author driver; Python subprocess-wrapper elapsed is retained separately and includes launch/wait overhead.

Each simulated platform contains 1,000 four-core worker hosts, 100 network links, routes of 10 links, 100–200 Mflop/s core speeds, and 100–200 MB/s bandwidths. Every workunit communicates 100 MB and computes 100 Mflop. The 3.36 run enables host-energy simulation as the authors’ driver does. The lower/upper workloads are **4,000 and 60,000 workunits**, with **ten seeds per version per workload**. Intermediate Figure 13 points and the Figure 14 core-count sweep remain unexecuted.

Before timing, three small fixed-seed cases check both models’ makespans. A separate paper-size 4,000-workunit check compares native completion timestamps. The predeclared tolerance is 0.000001 simulated seconds, reflecting the native log resolution; it is a local consistency rule, not a published paper tolerance.

## Inspect the outputs

[Replication-level measurements](simgrid-output/performance-replications.csv), [summaries](simgrid-output/performance-summary.csv), and the [complete comparison](simgrid-output/comparison.json) retain all ten runs and native makespan checks. Error bars in the supplied endpoint figure are minimum/maximum over repetitions.

| Workunits | SimGrid 3.10 mean peak RSS | SimGrid 3.36 mean peak RSS | Local RSS ratio | Local wall-time ratio |
| --- | ---: | ---: | ---: | ---: |
| 4,000 | 354,393.6 KiB | 68,160 KiB | 5.1994 | 1.2995 |
| 60,000 | 365,107.2 KiB | 68,160 KiB | 5.3566 | 1.5847 |

All four native makespan comparisons matched exactly. At 1,000 hosts and 4,000 workunits, seed 0, both reported **4,233.049287 simulated seconds**. The local RSS ratios exceed the paper’s reported minimum 4.1 reduction, while the local wall-time ratio at the lower endpoint is below its reported minimum 1.45. These are two endpoint observations on a different host/compiler; the complete historical curves and hardware speedups are not claimed reproduced.

The source programs carry SimGrid-team LGPL notices; the associated SimGrid package identifies LGPL-2.1 with separate component notices. Retrieve source through the pinned harness and preserve those notices. Do not apply OSRI’s original-code license to third-party model code. Human scientific review remains pending.
