# A published fluid–structure benchmark with preCICE

**Question:** Can a coupled flow and structural model reproduce the motion and forces of a defined benchmark?

[Turek and Hron (2006)](https://doi.org/10.1007/3-540-34596-5_15) define a benchmark for an elastic object in laminar incompressible flow. The [preCICE FSI3 tutorial](https://precice.org/tutorials/turek-hron-fsi3/) provides a concrete implementation using **OpenFOAM for the fluid and nonlinear deal.II for the solid**. The [preCICE v2 paper](https://doi.org/10.12688/openreseurope.14445.2) describes the coupling software. These are different contributions: benchmark specification, coupling method, and executable tutorial.

## Prepare a compatible solver pair

This is an advanced example that can take hours. Start with the [perpendicular-flap tutorial](https://precice.org/tutorials-perpendicular-flap) if you are learning preCICE. Install mutually compatible preCICE, adapters, OpenFOAM, and deal.II versions according to the tutorial. OpenFOAM Foundation and OpenCFD distributions have different release conventions; a name match is not a compatibility check.

The tutorial repository was inspected at `a2aab6b46cf556ce1a5187a40d8eb2685634f228`:

```sh
git clone https://github.com/precice/tutorials.git
cd tutorials
git checkout a2aab6b46cf556ce1a5187a40d8eb2685634f228
cd turek-hron-fsi3
```

After the documented setup, start each participant in its own terminal from that case directory:

```sh
# Terminal 1
cd fluid-openfoam
./run.sh
```

```sh
# Terminal 2
cd solid-dealii
./run.sh
```

## Compare an observable

Retain the participant logs, meshes, coupling configuration, time steps, tolerances, and the structural-tip watchpoint output. Define a settled time window and compare tip displacement, frequency, drag, and lift against the selected benchmark's definitions and reference values. Check convergence with respect to mesh, time step, and coupling tolerance before treating a close-looking curve as agreement.

The current tutorial also cites later benchmark work. Select the exact benchmark publication and case before importing numerical targets. The original 2006 target tables were not fully reviewed for this catalog, so no reference numbers are copied here. A clean solver exit or converged coupling residual is narrower evidence than reproduction of the benchmark.

**Status:** Benchmark citation and upstream FSI3 setup/run instructions inspected on 2026-11-15. Original numerical target review and coupled execution remain to be done.
