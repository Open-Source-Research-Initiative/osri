# Rebuild Unison’s published network-accuracy table

The [Unison paper](https://doi.org/10.1145/3627703.3629574) by Bai et al. (EuroSys 2024) compares ns-3’s sequential kernel with the authors’ parallel kernel. This example reconstructs the four ns-3/Unison configurations in **Section 6.2, Table 2**. It also checks the section’s claim that Unison’s event counts and simulation results remain identical across thread counts. Figure 2 is a conceptual diagram; the driver’s `# 2` comment refers to Table 2.

The [coauthor-hosted manuscript](https://cs.nju.edu.cn/tianchen/lunwen/2024/eurosys24-final201.pdf) provides the reference values. The [authors’ code](https://github.com/NASA-NJU/UNISON-for-ns-3/tree/7b3274167615c55ae8d69f7edee4e2dc2d81f706) is pinned to the evaluated branch’s commit `7b3274167615c55ae8d69f7edee4e2dc2d81f706`, based on ns-3.36.1. Its source, model, traffic distribution and postprocessing remain unchanged.

## Construct and run

Use Linux, Python 3 with `venv`, git, GCC/G++, and an existing compiler-compatible Boost prefix if also building the accompanying SimGrid example. The [build harness](files/ns-3-dev-git/build-network-tools.sh) creates local environments and source builds; [requirements-build.txt](files/ns-3-dev-git/requirements-build.txt) pins CMake and Ninja. The combined harness downloads both network examples. Set `BOOST_ROOT` to the selected Boost prefix, then run:

```sh
bash build-network-tools.sh
python3 run_unison.py
python3 analyse_unison.py
```

The upstream `python3 unison/process.py 2` route converts the generated accuracy CSV; the supplied analysis harness writes that CSV and calls the author postprocessor.

The isolated source build fixes GCC 13 compatibility with the compiler option `-include cstdint`; it does not edit model code. The paper recommends Ubuntu 22.04, while this run used Ubuntu 24.04, GCC 13.3, and CMake 3.31.6. MPI, root access and host initialization are unnecessary for these local sequential/multithreaded configurations. Preserve the author `scratch/cdf/web-search.txt` input and run from the cloned repository, as its relative path is part of the model.

The scenario uses 2- and 4-cluster fat-trees, TCP NewReno, RED queues, 100 Mbps links, 500 μs delay, a 100-packet buffer, 500-byte application packets, 70% offered load, 10% incast, and five simulated seconds. Threads equal the cluster count for Table 2. The default author seed is retained. The supplied runner additionally repeats the 2-cluster scenario at 1, 2, and 4 threads.

## Inspect the comparison

[Download the twelve metric checks](files/ns-3-dev-git/ns3-output/table2-comparison.csv), [the authors’ processed table](files/ns-3-dev-git/ns3-output/author-table2.csv), and the [comparison receipt](files/ns-3-dev-git/ns3-output/comparison.json). The receipt retains exact counts and the four fixed-input determinism runs.

| Configuration | Paper FCT (ms) | Local FCT (ms) | Paper RTT (ms) | Local RTT (ms) | Paper throughput (Mbps) | Local throughput (Mbps) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sequential, 2 clusters | 650.89 | 650.895 | 15.14 | 15.13888 | 6.81 | 6.81012 |
| Unison, 2 clusters | 632.52 | 632.525 | 15.03 | 15.03370 | 6.99 | 6.98695 |
| Sequential, 4 clusters | 480.84 | 480.842 | 10.49 | 10.49304 | 6.50 | 6.50213 |
| Unison, 4 clusters | 472.45 | 472.454 | 11.39 | 11.38678 | 6.41 | 6.40928 |

The comparison rule was declared before numerical output: absolute difference at most 0.005 in each printed unit, half the table’s last decimal place. All twelve entries passed, including values on the boundary. This establishes agreement with displayed values, without estimating uncertainty in the article. The authors’ `process.py` defines RTT as twice mean end-to-end delay; that exact conversion is retained.

All four 2-cluster Unison runs reported **7,447,618 events**, **676,639 received packets**, and identical model metrics. The fixed-input result is deterministic across the tested 1/2/4 threads and the repeated 2-thread run. This does not test all 1–16 thread counts discussed in the paper or its separate Figure 11 topology.

An initial 0.05-second diagnostic produced no observed completed flows and undefined averages. That failed diagnostic is preserved and excluded. The successful comparison does not establish the paper’s hardware speedups, all other experiments, or physical-network validity. Human scientific review remains pending.

The upstream ns-3/Unison source is GPL-2.0; preserve its notices. The download harness leaves that source in its own checkout. OSRI’s original harnesses, comparison data and figures have their stated repository licenses.

## Download the recorded files

- [author-postprocess.log](files/ns-3-dev-git/ns3-output/author-postprocess.log) — native run output or command record.
- [author-table2.csv](files/ns-3-dev-git/ns3-output/author-table2.csv) — numerical result.
- [comparison.json](files/ns-3-dev-git/ns3-output/comparison.json) — numerical comparison receipt.
- [default-cluster2-time.log](files/ns-3-dev-git/ns3-output/default-cluster2-time.log) — native run output or command record.
- [default-cluster2.log](files/ns-3-dev-git/ns3-output/default-cluster2.log) — native run output or command record.
- [default-cluster4-time.log](files/ns-3-dev-git/ns3-output/default-cluster4-time.log) — native run output or command record.
- [default-cluster4.log](files/ns-3-dev-git/ns3-output/default-cluster4.log) — native run output or command record.
- [diagnostic-time.log](files/ns-3-dev-git/ns3-output/diagnostic-time.log) — native run output or command record.
- [diagnostic.log](files/ns-3-dev-git/ns3-output/diagnostic.log) — native run output or command record.
- [table2-comparison.csv](files/ns-3-dev-git/ns3-output/table2-comparison.csv) — numerical result.
- [table2-comparison.png](files/ns-3-dev-git/ns3-output/table2-comparison.png) — original comparison figure.
- [table2-comparison.svg](files/ns-3-dev-git/ns3-output/table2-comparison.svg) — original comparison figure.
- [unison-cluster2-thread1-time.log](files/ns-3-dev-git/ns3-output/unison-cluster2-thread1-time.log) — native run output or command record.
- [unison-cluster2-thread1.log](files/ns-3-dev-git/ns3-output/unison-cluster2-thread1.log) — native run output or command record.
- [unison-cluster2-thread2-repeat-time.log](files/ns-3-dev-git/ns3-output/unison-cluster2-thread2-repeat-time.log) — native run output or command record.
- [unison-cluster2-thread2-repeat.log](files/ns-3-dev-git/ns3-output/unison-cluster2-thread2-repeat.log) — native run output or command record.
- [unison-cluster2-thread2-time.log](files/ns-3-dev-git/ns3-output/unison-cluster2-thread2-time.log) — native run output or command record.
- [unison-cluster2-thread2.log](files/ns-3-dev-git/ns3-output/unison-cluster2-thread2.log) — native run output or command record.
- [unison-cluster2-thread4-time.log](files/ns-3-dev-git/ns3-output/unison-cluster2-thread4-time.log) — native run output or command record.
- [unison-cluster2-thread4.log](files/ns-3-dev-git/ns3-output/unison-cluster2-thread4.log) — native run output or command record.
- [unison-cluster4-thread4-time.log](files/ns-3-dev-git/ns3-output/unison-cluster4-thread4-time.log) — native run output or command record.
- [unison-cluster4-thread4.log](files/ns-3-dev-git/ns3-output/unison-cluster4-thread4.log) — native run output or command record.
- [compact-unison-record.json](files/ns-3-dev-git/compact-unison-record.json) — portable compact run/comparison receipt.
- [build-network-tools.sh](files/ns-3-dev-git/build-network-tools.sh) — portable driver or environment/source record.
- [requirements-build.txt](files/ns-3-dev-git/requirements-build.txt) — portable driver or environment/source record.
- [THIRD-PARTY-NOTICES.md](files/ns-3-dev-git/THIRD-PARTY-NOTICES.md) — portable driver or environment/source record.
- [targets-before-run.json](files/ns-3-dev-git/targets-before-run.json) — portable driver or environment/source record.
- [plot_network_results.py](files/ns-3-dev-git/plot_network_results.py) — portable driver or environment/source record.
- [requirements-plot.txt](files/ns-3-dev-git/requirements-plot.txt) — portable driver or environment/source record.
- [ns3-guide.md](files/ns-3-dev-git/ns3-guide.md) — portable driver or environment/source record.
- [run_unison.py](files/ns-3-dev-git/run_unison.py) — portable driver or environment/source record.
- [analyse_unison.py](files/ns-3-dev-git/analyse_unison.py) — portable driver or environment/source record.

[Complete run record](records/ns-3-dev-git.json) · [All candidate attempts](README.md). Human scientific review is pending.
