# A published service-model walkthrough with SimPy and Ciw

**Question:** How do demand and staffing change waiting times and resource utilization?

[Monks and Harper (2023)](https://doi.org/10.3310/nihropenres.13467.2) present reproducible discrete-event simulation using Python, with an urgent-care call-centre example. The [open article](https://openresearch.nihr.ac.uk/articles/3-48/v2) links an executable book and the [v1.1.2 code archive](https://doi.org/10.5281/zenodo.8193001). This is an operational teaching model, not evidence for a clinical intervention.

## Start in a browser

Open the [authors' book](https://health-data-science-or.github.io/simpy-streamlit-tutorial/) and follow its worked model and reproducibility chapters. Its notebook launch route can provide a browser environment; hosted service availability is separate from source availability. Record the notebook revision and environment rather than assuming a live launch matches the archived paper.

## Use a local environment

The inspected repository snapshot is `69288c31fde06114a49c1fbb2186ad163139c126`:

```sh
git clone https://github.com/health-data-science-OR/simpy-streamlit-tutorial.git
cd simpy-streamlit-tutorial
git checkout 69288c31fde06114a49c1fbb2186ad163139c126
conda env create -f binder/environment.yml
conda activate sim
python main.py
```

The last command is the repository's setup check. Follow the book for the model notebooks and experiment. For a paper-specific reproduction, use the v1.1.2 archive and its environment instead: the article reports Python 3.9.16, SimPy 4.0.1, Ciw 2.3.7, and Streamlit 1.23.0, while the current repository has changed.

## Design a useful comparison

Keep arrival and service distributions, staffing, queue discipline, run length, warm-up, and seeds explicit. Compare a baseline staffing scenario with one defined change using repeated runs. Report waiting-time distributions and utilization with uncertainty; one mean from one run can hide congestion and stochastic variation. Preserve input distributions and replication-level outputs, not just a dashboard screenshot.

**Status:** Open article's worked-example and reproducibility material, archive record, and repository setup inspected on 2026-11-15. Upstream notebooks and local environment were not executed here.
