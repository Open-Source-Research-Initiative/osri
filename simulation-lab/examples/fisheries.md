# Fisheries and policy with ViNoS

**Question:** How can a model connect fishing decisions, ecological conditions, and policy?

[Lemmen et al. (2024)](https://doi.org/10.21105/joss.05731) present ViNoS, a NetLogo model for small-scale fisheries. The [open JOSS article](https://joss.theoj.org/papers/10.21105/joss.05731) describes its purpose and links source and archived artifacts. This example broadens the catalog beyond financial and physical models into coupled social and ecological simulation.

**Dated access correction, 2026-11-15:** The first review encountered a source-host challenge and left the model uninspected. The author archive **v1.3.2 (2024-03-08)** has now been retrieved and inspected at [version DOI 10.5281/zenodo.10798132](https://doi.org/10.5281/zenodo.10798132). The archive SHA256 is `23e401344956f3c275d8df697039dd0f865e63c62fc073ba36a31365a3db2782`. The earlier concept DOI now points to a newer release; use this version DOI for the paper-era route.

The model is `netlogo/vinos.nlogo`; the archived README requires NetLogo 6.4 or newer. Its `netlogo/behavior/reproducibility.xml` experiment uses seed `123456789`, resets the date to `2021-04-01`, and runs 10 steps, reporting `count turtles`. After qualifying the runtime and extensions, retain the extracted directory layout and try the proposed headless command from its root:

```sh
netlogo-headless.sh --model netlogo/vinos.nlogo \
  --setup-file netlogo/behavior/reproducibility.xml \
  --experiment reproducibility --table reproducibility.csv
```

This command has not been run here. Repeat the deterministic experiment twice and compare numeric outputs before extending the archived `vary-diesel.xml` experiment. A quantitative policy result and comparison tolerance still need selection; policy conclusions require separate assessment of calibration and empirical support.

The model is Apache-2.0, but archive data and assets have individual terms, including noncommercial/no-derivatives material. Inspect per-file SPDX notices and `LICENSES` before redistributing inputs. This guide links to the archive rather than repackaging it.

**Status:** Original JOSS article reviewed; versioned artifact and experiment instructions now inspected; model execution and published-result comparison remain pending. See the [complete NetLogo construction route](../research/agents-operations.md#netlogo).
