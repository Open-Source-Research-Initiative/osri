# Adaptive FEM from an author experiment

Re-run one result from Brodbeck, Bertrand and Ricken, *Adaptive finite element methods based on flux and stress equilibration using FEniCSx*, [arXiv:2410.09764v1](https://arxiv.org/html/2410.09764v1), Section 4.1, Figure 2(a). A related [published 2026 chapter](https://doi.org/10.1007/978-3-032-17396-6_1) has a shortened title; this comparison explicitly uses the preprint's target table.

The question is whether an equilibrated flux provides an efficient error estimate while adaptivity resolves the coefficient-interface singularity. This run uses the authors' actual `case_poisson_riviere/solve_riviere.py`, not a replacement implementation. It selects their contrast-5, P1 primal/RT2 flux case, Dörfler parameter 0.5, and all 20 refinement levels.

## Re-run

On Linux x86-64 with Git and micromamba, keep this guide, `bootstrap-afem.py`, `conda-linux64.lock`, and `run-afem.py` together:

```sh
python3 bootstrap-afem.py --work afem-work
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMPI_MCA_btl=self,tcp \
XDG_CACHE_HOME="$PWD/afem-work/cache" MPLCONFIGDIR="$PWD/afem-work/cache/matplotlib" \
afem-work/env/bin/python run-afem.py --source afem-work/source --output afem-work/results
```

The lock captures the tested conda layer. The bootstrap then applies the recorded setuptools 80.9.0 compatibility pin, builds the exact dolfinx_eqlb v1.2.0 commit, and installs its bindings. Added wrapper/Eigen include paths address build discovery. The author package's internal version string is 1.1.0 even at the v1.2.0 Git tag, so the commit identifies the source. No numerical source is changed.

The original author environment uses a DOLFINx 0.6.0 Docker image. Here DOLFINx 0.6.0, Python 3.10, PETSc 3.19.6, and corresponding conda packages replace that container. Docker was unavailable on the execution host. Setup downloaded about 0.61 GB of conda packages; the selected computation took 8.12 seconds here. Hardware-dependent runtime is illustrative.

## Actual comparison

| Observable after the last refinement | Figure 2(a) | This run | Check |
| --- | --- | --- | --- |
| Observed convergence order | 0.50 | 0.5021171064 | Within 0.005 |
| Estimator efficiency | 1.06 | 1.0627164504 | Within 0.005 |

The 0.005 threshold was declared before numerical execution and corresponds to half the last printed unit in the two-decimal reference table. It establishes agreement at reporting precision for this case. It does not establish every result in the article.

The final primal solve has 183,899 degrees of freedom, true energy error 0.0094834760, and estimated error 0.0100782460. The CSV contains all 20 refinement levels. XDMF/HDF5 files retain the adaptive meshes and error-indicator fields; those files include the newly refined mesh after each iteration, so their final mesh can differ from the last CSV solve mesh.

`run-record.json` records the selected inputs, comparison, and output hashes. Preserve the CSV, figure, and full run log alongside it. Human scientific review remains pending.

## Source and terms

Author experiment commit: `3d9741498712c13ce901f5fbd6255a82a3cec1ac`. Flux library tag v1.2.0 commit: `16f5ea6e16aa15d856381e32a3be5fc2f913215a`. The author experiment file has an LGPL-3.0-or-later SPDX notice; the repository's LICENSE and README differ. This bundle retrieves upstream code and preserves its notices rather than relicensing it. OSRI's original harness uses MIT; generated comparison figures and numerical outputs may be shared with source attribution.

Failed attempts remain recorded: initial environment-prefix spelling; UFL requiring pkg_resources; missing wrapper and Eigen include paths during binding builds. Those failures occurred before numerical output. The successful author script is unchanged.

## Download the recorded files

- [Riviere-5_P1_RT2.csv](files/dolfinx/output-attempt3/Riviere-5_P1_RT2.csv) — Raw20-level numerical convergence/error/efficiency table.
- [afem-comparison.svg](files/dolfinx/output-attempt3/afem-comparison.svg) — Editable vector comparison plot.
- [afem-comparison.png](files/dolfinx/output-attempt3/afem-comparison.png) — Comparison preview.
- [run-record.json](files/dolfinx/output-attempt3/run-record.json) — Full inputs/comparison/native-output hashes.
- [bootstrap-afem.py](files/dolfinx/bootstrap-afem.py) — portable driver or environment/source record.
- [run-afem.py](files/dolfinx/run-afem.py) — portable driver or environment/source record.
- [conda-linux64.lock](files/dolfinx/conda-linux64.lock) — portable driver or environment/source record.
- [requirements-frozen.txt](files/dolfinx/requirements-frozen.txt) — portable driver or environment/source record.
- [GUIDE.md](files/dolfinx/GUIDE.md) — portable driver or environment/source record.

[Complete run record](records/dolfinx.json) · [All candidate attempts](README.md). Human scientific review is pending.
