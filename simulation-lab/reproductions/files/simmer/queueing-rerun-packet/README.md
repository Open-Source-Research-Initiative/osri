# Independent rerun of the OSRI queueing methods note

The packet reruns the published single-server queue in Section 4.2, checks every pair of completed-arrival records, and tests whether assigning a separate random stream to each replication removes the systematic pairing. Use a fresh environment and generate new outputs. The packet contains comparison targets and executable checks. It has no saved simulation outputs as inputs. [OSRI methods note at the reviewed revision](https://github.com/Open-Source-Research-Initiative/osri/blob/51f2da6c5af203605d7da53271c2aa7efc58b66c/simulation-lab/queueing-methods-note.md) · [Paper and supplement](https://www.jstatsoft.org/article/view/v090i02)

## Setup and exact commands

The tested platform is Ubuntu 24.04 on Linux x86-64 with Bash, Python 3, GNU tar with bzip2, GNU coreutils and findutils, make, and `/usr/bin/gcc` and `/usr/bin/g++` 13.3.0. The setup uses outbound HTTPS to retrieve about 340 MB of archives and needs workspace room for the package cache and build. Record any host/compiler differences in the review form.

Run from the extracted packet directory. Keep runtime data on your chosen work volume. On BuilderBob, extract the packet and keep the work directory under `/workspace`.

```bash
set -euo pipefail
sha256sum -c SHA256SUMS
work="$PWD/../queueing-rerun-work"
bash setup.sh "$work"
bash run.sh "$work" "$work/evidence"
(
  cd "$work/evidence"
  sha256sum -c SHA256SUMS
)
```

`setup.sh` verifies every downloaded archive against `inputs.lock.json`, then installs the exact 94-package conda layer offline using micromamba 2.10.0. It installs the pinned BH 1.69.0-1 and publisher’s simmer 4.3.0 from source over that layer. The conda inventory still displays its original BH package version. The run checks the installed library versions, including R 4.5.3, Rcpp 1.1.2, magrittr 2.0.5 and jsonlite 2.0.0. See `logs/platform.txt` and `evidence/package-versions.csv`. The paper PDF and R supplement are also pinned by SHA-256.

Each run requires a new evidence directory. Failed checks exit nonzero and leave the evidence, log and checksums for inspection. Report mismatches and setup changes with the outputs. [Micromamba documentation](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)

## What the checker tests

The original code supplies the M/M/1 model, with arrival rate 2, service rate 4, one server and an initially empty queue. Each Section 4.2 run stops at 500 time units. R starts from seed 1234 and is configured for two forked workers with prescheduling enabled and automatic reseeding disabled. That makes the documented prescheduled assignment odd runs to one child and even runs to the other. The checker compares run 1 with 2, 3 with 4, through 99 with 100. It compares both the exact replication means and the completed-arrival records, including IDs, times, activity time and completion flags. Only the monitor’s local replication label is removed. [R prescheduling](https://stat.ethz.ch/R-manual/R-devel/library/parallel/html/mclapply.html) · [Fork seed behavior](https://stat.ethz.ch/R-manual/R-devel/library/parallel/html/mcparallel.html)

| Run | Configuration | Expected check |
| --- | --- | --- |
| Published-code reproduction | Mersenne-Twister, two workers with inherited state. Executes the publisher’s Section 4.2 statements unchanged after Section 4.1 model setup. | All 50 mean pairs and all 50 completed-arrival pairs are identical. The mean and interval match `0.4974943`, `[0.4868269, 0.5081617]` within `5e-8` per value. |
| One mean per pair | Recompute the t interval using runs 1, 3, …, 99 from the reproduction. | The mean is unchanged to numerical precision. The 95% t interval is `[0.4821378, 0.5128508]` within `5e-8` per endpoint and about 44% wider. |
| Shared-stream L’Ecuyer check | L’Ecuyer-CMRG with the same seed, model and scheduling. Each worker inherits the same starting state. | All 50 mean and record pairs still match. |
| Separate-stream control | Same L’Ecuyer-CMRG generator and two-worker schedule. Assign one stream per replication with `nextRNGStream()` and verify the assigned states and worker PIDs. | Zero of 50 corresponding pairs match in means or completed-arrival records. The shared-stream L’Ecuyer check holds the generator fixed for this comparison. |
| Distinct integer seeds | Reuse the model with Mersenne-Twister and seeds 10001–10100. Recompute per-run system time and time-weighted occupancy. | The 97.5% t intervals reproduce the note’s printed numbers and contain 0.5 and 1, respectively. |

The printed paper target was fixed in the original OSRI run and is retained in `targets.json`. The distinct-seed figures are compared at the note’s five-decimal precision, with tolerance `5e-6` per value. The one-per-pair interval is a recalculation under the t-interval assumptions. Pair equality is a check on the completed records retained by the monitor. The control tests systematic pairing under these configurations. The authors’ historical worker count, long-run accuracy and interval coverage remain outside these checks. [R streams documentation](https://stat.ethz.ch/R-manual/R-devel/library/parallel/html/RngStream.html)

## Evidence to return

Return a completed [review form](REVIEW.md), the evidence directory and the setup logs. Do not include the downloaded software archives or full environment.

- `summary.json` reports the intervals, pair totals, tolerance checks and overall outcome.
- Each two-worker arm records 50 rows in `*-pairs.csv`, 100 means in `*-replications.csv`, and all completed-arrival records in `*-completed-arrivals.rds`. RDS list elements are in run order, so an independent reader can apply `identical(logs[[1]], logs[[2]])` after loading an arm with `readRDS()`.
- `lecuyer-assigned-streams.csv` records starting states and process IDs. `distinct-seed-replications.csv` holds the finite-horizon checks.
- The two `executed-section*.R` files show the code read from the supplement. Each evidence file is listed in `SHA256SUMS`.

This packet was prepared for external reproducibility review. The external reviewer records the result and any deviations in their own words. Publisher and package archives are retrieved from their sources under their original terms.
