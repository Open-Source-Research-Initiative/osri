# Run the author dam-break validation case

This example builds DualSPHysics 5.4 from the authors' pinned source, runs their unchanged two-dimensional dam-break input to 2 seconds, and compares the simulated front with the experimental coordinates bundled by the authors. The comparison found a discrepancy: MAE **0.2473 m**, RMSE **0.2637 m**, maximum absolute difference **0.3347 m** across 14 pre-impact coordinates. No scientific pass threshold was supplied, and the original article's scaling and front definition have not been independently checked. This is an executed validation case, with human scientific review pending.

The experimental reference is Koshizuka and Oka (1996), [*Moving-Particle Semi-Implicit Method for Fragmentation of Incompressible Fluid*](https://doi.org/10.13182/NSE96-A24205), Nuclear Science and Engineering 123, 421–434. The [official DualSPHysics test-case documentation](https://github.com/DualSPHysics/DualSPHysics/wiki/7.-Testcases/f27d173a1735cae5f0def598ceccdfe2fc05e2df) describes comparison of the dam tip before wall impact. The historical paper uses MPS; this current implementation uses SPH. It does not reproduce the historical algorithm or the performance results of the 2015 DualSPHysics software paper.

## Retrieve, build and run

Use a Linux machine with Git, Python 3, GNU Make, GCC, and OpenMP support. The tested compiler was GCC 13.3.0 on x86-64 Linux. Run these commands in a directory with space for the source, build and particle files:

```sh
python3 bootstrap-dambreak.py --source DualSPHysics
python3 run-dambreak.py --source DualSPHysics --output dam-break-results --wall-seconds 300
python3 compare-dambreak.py \
  --gauge dam-break-results/initial/GaugesSWL_Swl_z003.csv \
  --experiment 'DualSPHysics/examples/main/01_DamBreak/EXP_X-DamTipPosition_Koshizula&Oka1996.txt' \
  --output comparison
```

The bootstrap retrieves commit `ef3721a861fda961f0e2f9ec4cd317b19de99086` from [the authors' repository](https://github.com/DualSPHysics/DualSPHysics/tree/ef3721a861fda961f0e2f9ec4cd317b19de99086). It builds the CPU solver, supplies GCC's missing `cstdint` include, and disables optional Chrono, wave-generator and MoorDyn components unused by this case. It preserves upstream fast-math settings. The model equations and input XML are unchanged.

The runner uses two CPU threads. If its first 300-second bound expires, it retains that output and resumes once from the last native particle file. On this host, the initial run reached approximately 1.44 seconds before the bound; the restart completed the 2-second horizon in another 124.799 seconds. The solver warns that restarting from single-precision particle positions introduces small differences. All comparison coordinates are covered by the initial, unrestarted run, so the restart does not affect the reported comparison. A faster host may finish without a restart.

The shipped wrappers express the same commands used for the recorded run; a complete clean bootstrap has not been replayed separately. Keep their command logs and `execution.json` when repeating the example.

## Compare the observable

The unchanged `CaseDambreakVal2D_Def.xml` creates 21,001 particles with 0.01 m spacing, a 1 m by 2 m water column and a 4 m by 3 m tank. It uses gravity 9.81 m/s², artificial viscosity 0.02, Fourtakas density diffusion 0.1, a Wendland kernel and Verlet integration. Its native horizontal SWL gauge samples the front at `z=0.03 m`.

Before execution, the comparison selected experimental coordinates whose supplied front position was at most 3.9, avoiding contact with the 4 m wall. The harness linearly interpolates the native gauge at those 14 supplied times and writes every difference to `front-comparison.csv`. It reports errors without inventing an acceptance tolerance. The fixture is used in its supplied coordinate scale; original-article normalization and alignment with this gauge remain review requirements. The exact original-paper figure locator is unresolved.

Optional plots require the packages in `plot-requirements.txt`; install these in an isolated environment and add `--plot` to the comparison command. Numerical comparison itself uses only Python's standard library. The archived CSV, JSON and SVG show the actual discrepancies; they are not evidence of agreement.

## Attribution and component terms

The solver source is LGPL-2.1-or-later. The upstream **GenCase helper is a separate binary-only component**: its runtime notice allows unmodified binary redistribution with its notices, but restricts source redistribution/modification without permission. This bundle distributes no helper executable; the bootstrap retrieves the upstream distribution, whose component notices must be retained. The experimental text is attributed by its authors to Koshizuka and Oka; no separate dataset license was located. The guide links to it rather than redistributing that reference file. Generated solver gauge files and the compact comparison are included as run evidence.

Native particle files, restart files, full logs and source/build failure evidence remain in the research campaign. Human scientific review, original-article method checks and spatial/time-step convergence assessment are still required before interpreting this case as a validated prediction.
