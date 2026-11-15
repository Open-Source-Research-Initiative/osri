# OSRI Simulation Lab

Find a simulation tool, learn from a published model, and keep enough information for someone else to repeat the work.

- [Browse the tool catalog](catalog.md): 60 tools across robotics, engineering, finance, economics, operations, energy, natural sciences, and computing.
- [Inspect the 21 candidate attempts](reproductions/README.md): author-code runs, native outputs, comparisons, adaptations, and verified blockers.
- [Plan an example for any of the 60 tools](research/README.md): paper artifacts, construction steps, comparison targets, and unresolved access needs.
- [Choose a literature example](examples/README.md): paper locations, source code, setup routes, outputs to inspect, and execution status.
- [Run the CPU examples](examples/cpu-walkthroughs.md): battery discharge, option pricing, household saving, and OpenUSD result exchange.
- [Read the bibliography](bibliography.md) or download [tools](tools.csv), [papers](papers.csv), [examples](examples.csv), and [BibTeX](references.bib).

## Choose a question

| What would you like to investigate? | Start here |
| --- | --- |
| How does a robot learn to move in a simulated world? | [Isaac Sim, Isaac Lab, and OpenUSD](examples/robotics.md) |
| How do battery voltage and discharge time relate? | [PyBaMM's published code example](examples/cpu-walkthroughs.md#battery-discharge) |
| How do order flow and execution change a simulated market? | [ABIDES](examples/markets.md) |
| How can simulated payoffs be checked against a pricing formula? | [Black–Scholes with QuantLib](examples/cpu-walkthroughs.md#option-pricing) |
| How does income risk affect household saving? | [Carroll's model with Econ-ARK](examples/economics.md) |
| How does a flexible structure respond to flow? | [The Turek–Hron benchmark with preCICE](examples/fluid-structure.md) |
| How do networks, dispatch, and capacity affect an energy system? | [PyPSA-Eur](examples/energy.md) |
| How do staffing and demand affect waiting? | [A published SimPy and Ciw service model](examples/queues.md) |
| How do routing and signals affect urban traffic? | [SUMO's LuST scenario](examples/traffic.md) |

A browser is enough to read papers, inspect models, compare assumptions, and contribute a source. The CPU examples need a Python environment. The Isaac walkthrough needs a compatible NVIDIA GPU and its documented runtime. Larger models have their own requirements.

## Understand the evidence

The catalog is a growing inventory, not a claim to list every open-source simulator. It includes solvers, modeling frameworks, and supporting scene tools. A source-code license does not necessarily cover a complete runtime, an input dataset, or a model asset. Isaac Sim and CARLA particularly require reading the dependency notes. OpenUSD composes scenes and data; the numerical calculation remains in the selected solver.

Each example states its relationship to the paper. **Executed adaptation** means the included teaching code ran and passed the listed checks. **Upstream instructions checked** means the authors' or maintainers' code and run route were inspected but not executed here. **Access pending** means an artifact still needs retrieval. None of these labels alone establishes reproduction of a published result.

Sources were checked on **2026-11-15**. See [verification](verification.md), [source and access notes](source-notes.md), and the [contribution guide](contributing.md).

## Start a study

Keep a new study in its own [research repository](../projects/README.md), with a defined question, responsible human, model version, inputs, assumptions, and intended comparison. This hub holds shared learning resources. Use the [simulation workflow](../tooling/workflows.md#simulation-or-replication) and [run-record template](run-record-template.md) when developing a study. Human review and acceptance remain separate from automated checks.
