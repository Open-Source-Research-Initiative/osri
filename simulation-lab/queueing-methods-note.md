# When a reproduced confidence interval counts the same runs twice

*Methods note. Human scientific review and an external rerun are pending.*

[Download the independent rerun packet](../site/assets/downloads/queueing-rerun-packet.zip) · [Read the pinned setup and run instructions](reproductions/files/simmer/queueing-rerun-packet/README.md)

OSRI’s Simulation Lab ran the published R code for a single-server queue with two workers and reproduced its mean of 0.4974943 and 95% confidence interval of [0.4868269, 0.5081617] to the printed precision. The 100 saved replication means formed 50 consecutive pairs, with two identical values in each pair. Using one mean from each pair gave the same estimate and an interval 44% wider. Section 4.2 gives the seed and parallel call. The worker count for the paper’s printed result is unconfirmed. [Ucar, Smeets, and Azcorra (2019), Section 4.2 and R supplement](https://www.jstatsoft.org/article/view/v090i02) · [OSRI run guide](reproductions/simmer.md)

## Where the pairs came from

The simmer example simulates an M/M/1 queue with an arrival rate of 2 and a service rate of 4. Each run starts empty and stops after 500 time units. The paper describes average population, which counts customers in the system over time. The R code averages departure time minus arrival time for the customers who departed in each run. In this queue, the steady-state mean time in the system is 0.5 time units and the steady-state mean population is 1 customer. [Published R supplement](https://www.jstatsoft.org/article/download/v090i02/3818)

The published code sets seed 1234 and disables reseeding in the parallel call. In OSRI’s two-worker run, both workers inherited the same random-number state. A separate two-run diagnostic compared the workers’ completed-arrival records and found that every column matched. The full 100-run output preserves the replication means, which match across all 50 pairs. [R documentation on seed inheritance](https://stat.ethz.ch/R-manual/R-devel/library/parallel/html/mcparallel.html) · [Two-worker diagnostic](reproductions/files/simmer/outputs/duplicate-stream-check.json)

The t-test calculated its standard error as if all 100 entries were independent. To isolate the effect of counting both copies, we ran the same t-test on rows 1, 3, …, 99 of the saved replication data. The resulting 95% interval, [0.4821378, 0.5128508], shows how much the duplicate entries narrowed the interval in this run. Interpreting the wider interval at its nominal 95% level depends on the assumptions of the t interval, including independence across retained runs. [Saved replication means](reproductions/files/simmer/outputs/author-replications.csv)

## A check with distinct seeds

The Lab kept the model and horizon and assigned seeds 10001–10100 to 100 new runs. The mean system time was 0.49806 with a 97.5% t interval of [0.48819, 0.50793]. The time-weighted mean population was 0.99770 with a 97.5% t interval of [0.97466, 1.02074]. The 97.5% level for each interval accounts for the two comparisons. Both intervals contained their respective steady-state references. Both estimates describe an empty-start, 500-time-unit experiment. The time estimate includes only customers who departed before the cutoff. Steady-state accuracy and interval coverage remain untested. [Recorded comparisons and run settings](reproductions/files/simmer/outputs/results.json)

If you rerun a parallel simulation to check its interval, save the per-run results alongside the seed settings and worker count. Here, the per-run results exposed the duplication and the seed settings explained it.

*Research record. OSRI’s Simulation Lab ran the reproduction and diagnostic under Cole Lyons’s direction with agent assistance. Codex checked the paper and code and recalculated the intervals from the saved data.*
