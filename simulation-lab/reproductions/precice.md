# preCICE

[All candidate attempts](README.md) · [Simulation Lab](../README.md)

Can a coupled fluid/structure solve recover the published FSI3 oscillation and force observables?

**Execution:** Attempted; blocked. **Paper comparison:** not established. Human scientific review is pending.

## Paper and author code

[Proposal for Numerical Benchmarking of Fluid-Structure Interaction between an Elastic Object and Laminar Incompressible Flow](https://doi.org/10.1007/3-540-34596-5_15) (10.1007/3-540-34596-5_15). Publication type: book-chapter.

**Paper location:** Original 2006 FSI3 benchmark; maintained tutorial also cites the 2010 extension DOI 10.1007/978-3-642-14206-2_8. Historical reference/constitutive alignment unresolved; no original result comparison.

[Source](https://github.com/precice/tutorials); ref: v202211.0; commit: 0482e5b4d3e1604dd031d2b113a2aaa63733c9a8.

**Source files:** turek-hron-fsi3/precice-config.xml; turek-hron-fsi3/fluid-openfoam/run.sh; turek-hron-fsi3/solid-dealii/run.sh; turek-hron-fsi3/solid-dealii/parameters.prm

**Terms:** preCICE tutorials LGPL-3.0; solver and adapter licenses separately apply

**Relationship to the paper:** Maintainer implementation of the literature benchmark; this tool supplies the partitioned coupling. Both preCICE and deal.II records refer to one coupled experiment. Exact historical case equivalence and the scientific target remain unresolved.

## Inputs and environment

description: FSI3 geometry, fluid/solid constitutive parameters, inlet ramp, mesh, time step and XML coupling settings from pinned case.; access: Case/meshes public. Author FSI3 reference series retrieved (1,113,417bytes; SHA256c428bc3ff48c1698cd10aacf0941cba6aabdfcb9d61c8b7e42c343f381434e63); this is upstream data, not a local simulation.; hashes: qualification-cg/precice-config.xml: 924518a5fa58a2ee1eaec42a8eaedb527adeaf7b0ae5f700b5179abbe01b8c68; qualification-cg/solid-dealii/parameters.prm: b5dd918bcb97daa1918f289066c914386a88acab589b10e0c05c823a50541a3d; qualification-cg/fluid-openfoam/0/U: 9c4083af85c05dc489a2a2fb06d9807c44a1beb82b198e8123d774f2fdd5a874; qualification-cg/fluid-openfoam/system/fvSolution: a0d399eaba95fbe39a0d1cd3aeb2eb4a0a834312772354cc0c553e22d2752d75; qualification-tight/fluid-openfoam/system/fvSolution: 01990053fa8dd2adf52a30c86bbf20ec392c17d610b9ddc4c154f891f9564396

versions: boost-cpp: 1.74.0; cmake: 3.27.9; dealii: 9.3.2; openmpi: 4.1.6; petsc: 3.17.4; precice: 2.5.0; openfoam: OpenCFD2412; compiler: GCC13.3.0; changes_from_author: 15 s horizon shortened to 0.003 s in all controls.; Replace unavailable groovyBC with the current maintainer codedFixedValue parabolic/cosine inlet.; Direct solver unavailable because conda deal.II 9.3.2 lacks UMFPACK; CG is an explicit numerical adaptation.; Third attempt tightens fluid absolute tolerances to 1e-11.

## Repeat the run

These steps describe the recorded run. Environment reconstruction and any changes to author code are identified above. Downloadable drivers retain the original source references and input hashes.

1. `` argv: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/env/bin/cmake; -S; /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/dealii-adapter; -B; /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/build-dealii-attempt2; -DCMAKE_PREFIX_PATH=/workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/env; -DCMAKE_CXX_COMPILER=/usr/bin/g++; cwd: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi; log: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/dealii-configure-attempt2.log ``
2. `` argv: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/env/bin/cmake; --build; /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/build-dealii-attempt2; -j2; cwd: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi; log: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/dealii-build.log ``
3. `` argv: ./Allwmake; cwd: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/openfoam-adapter; environment_wrapper: /home/builderbob/.local/bin/openfoam; environment_overrides: FOAM_USER_LIBBIN: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/lib; PKG_CONFIG_PATH: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/env/lib/pkgconfig; LD_LIBRARY_PATH: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/env/lib plus installed wrapper prefix; PATH: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/env/bin plus inherited path; GXX: /usr/bin/g++; WM_NCOMPPROCS: 2; MAKEFLAGS: LIB_SRC=/workspace/cache/builderbob/engineering-tools/20261029/solvers/include/OpenFOAM-2412/src GXX=/usr/bin/g++; log: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/openfoam-adapter/adapter-build-attempt2.log ``
4. `` participant: solid; argv: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/build-dealii-attempt2/elasticity; parameters.prm; cwd: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/qualification-cg/solid-dealii ``
5. `` participant: fluid; argv: /home/builderbob/.local/bin/openfoam; pimpleFoam; cwd: /workspace/repos/builderbob/open-source-research-initiative/planning/simulation-reproduction-2026-11-15/runs/numerics/fsi/qualification-cg/fluid-openfoam ``

## Comparison

**Observable:** Settled-window x/y tip displacement mean/amplitude/frequency and combined force

**Reference:** Author ref_fsi3.point dt0.00025; SHA256c428bc3ff48c1698cd10aacf0941cba6aabdfcb9d61c8b7e42c343f381434e63

**Rule and basis:** Not established.. No valid benchmark pass threshold before resolving reference version, matching input and mesh/time-step convergence. Short coupling qualification cannot satisfy settled-oscillation target.

**Defined before this run:** True. **Comparison scope:** Try compatible preCICE2.5/deal.II9.3 stack with installed OpenCFD2412. A short run may qualify participant coupling while a full hours-scale benchmark remains pending.

Measured results:

```json
{
  "qualification_windows": [
    {
      "attempt": "qualification-cg",
      "windows": [
        {
          "window": 1,
          "iterations": 100,
          "converged": false
        },
        {
          "window": 2,
          "iterations": 100,
          "converged": false
        },
        {
          "window": 3,
          "iterations": 30,
          "converged": true
        }
      ]
    },
    {
      "attempt": "qualification-tight",
      "windows": [
        {
          "window": 1,
          "iterations": 100,
          "converged": false
        },
        {
          "window": 2,
          "iterations": 100,
          "converged": false
        }
      ]
    }
  ],
  "cg_final_tip": {
    "time_s": 0.003,
    "dx_m": -2.8799859e-08,
    "dy_m": -4.82644979e-09,
    "interpretation": "Transient diagnostic values; the first two preceding windows were unconverged."
  }
}
```

No published periodic observable compared. A short transient cannot recover FSI3 mean, amplitude or frequency; exit 0 did not establish coupling convergence.

**Run result:** Actual coupling executed. The CG adaptation completed 0.003 s with both participants exiting 0, but the first two of three windows were unconverged. A tighter fluid solver retry also failed its first two windows and hit the 240 s bound. The Direct solver failed due to missing UMFPACK. No qualified coupled solution or paper-result comparison.

## Outputs and evidence

- [run-record.json](files/precice/fsi/run-record.json) — Shared two-tool actual execution and failure provenance; SHA256 `000ed88932d43215f0eb820a48888da3a968d3e3331b0a223c0181e6e9675c85`.
- [precice-Solid-iterations.log](files/precice/fsi/qualification-cg/solid-dealii/precice-Solid-iterations.log) — Native CG coupling convergence flags; SHA256 `f3c5f5149425712c7cc5eb7fb9a13cd76c71b683bbbea2b726a3e0a1723c33b8`.
- [precice-Solid-watchpoint-Flap-Tip.log](files/precice/fsi/qualification-cg/solid-dealii/precice-Solid-watchpoint-Flap-Tip.log) — Transient diagnostic watchpoint; unconverged preceding windows; SHA256 `cae3fd169db99133000bbaa9d47e2fd6c77dad5978ce72721568ff45abb05b4f`.
- [precice-Solid-iterations.log](files/precice/fsi/qualification-tight/solid-dealii/precice-Solid-iterations.log) — Native tighter-tolerance retry convergence flags; SHA256 `9ace7d95a9d615ac9ef8329b29f7338f5028f99b93658901504793645a6e8314`.

[Complete run record](records/precice.json). Native outputs, command logs and failed attempts are retained in the development evidence directory identified by that record.

## Limits and next step

**Blockers:** Installed deal.II 9.3.2 build has no UMFPACK; author Direct solver unavailable.; CG adaptation failed implicit coupling convergence in the first two windows; tighter fluid tolerances did not resolve it.; Current neo-Hookean solid, publication and reference-series constitutive alignment unresolved.; Full periodic benchmark and refinement study require a qualified setup and an hours-scale run; not launched.

**Next action:** Qualify the Direct solver or CG alternative and converged coupling; resolve original 2006 versus 2010 reference/material law; then predeclare the analysis window/tolerance and run the full horizon with mesh/time-step convergence.
