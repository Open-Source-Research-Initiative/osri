# Energy and natural sciences: paper-to-code routes

[All 60 tools](README.md) · [How to contribute](../contributing.md)

These are construction routes researched by agents. The execution line reports the bounded work actually performed; the comparison section defines what remains before claiming a published result. Human scientific review is pending.

## pypsa

**PyPSA** — Can the historical European transmission network and its validation be reconstructed from the authors' workflow?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for pypsa

Jonas Hörsch; Fabian Hofmann; David Schlachtberger; Tom Brown (2018). [PyPSA-Eur: An Open Optimisation Model of the European Transmission System](https://arxiv.org/abs/1806.01613). 10.1016/j.esr.2018.08.012.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://arxiv.org/abs/1806.01613). Metadata verification: confirmed. Full-text access: Open author preprint; original metadata refreshed through arXiv after Crossref returned 429.

**Target in the paper:** Network dataset description and validation; 6001 lines and 3657 substations reported in the abstract. Section 3.4 validation is the first reproduction target.

### Code and inputs for pypsa

[Artifact or upstream source](https://github.com/PyPSA/pypsa-eur). Author model repository and historical release; v0.1.0 README cites the 2018 article but this release is later than the paper, so exact paper inputs remain to establish.

**Source inspected:** yes. **Ref:** v0.1.0. **Commit:** 192b605bb55e74184e7bd1bb4217dd01b25d020f.

**Files:** README.md; environment.yaml; Snakefile

**Terms:** Historical source and component licenses must be read at the pin; input data have separate terms. Current PyPSA-Eur is MIT.

**Environment and compute:** Historical conda environment.yaml, Snakemake, PyPSA, atlite, geospatial packages, and solver versions must be reconstructed. Do not replace with the current Pixi tutorial silently. Geospatial workflow and continental optimization can require substantial RAM and hours; build a prebuilt-network inspection exercise first.

**Inputs:** GridKit/ENTSO-E topology, OPSD demand, plant database, reanalysis/cutout and eligibility inputs; prefer an archived prebuilt network to redownloading changing services.

**Data access:** README links archived prebuilt models at https://doi.org/10.5281/zenodo.3601882; archive contents/version-to-paper correspondence not yet inspected.

### Construct and compare pypsa

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed preparation: git clone https://github.com/PyPSA/pypsa-eur.git; cd pypsa-eur; git checkout 192b605bb55e74184e7bd1bb4217dd01b25d020f ``
2. `` Upstream environment: conda env create -f environment.yaml ``
3. `` Proposed inspection: snakemake --cores 1 --dry-run; select the network-construction target after identifying the archived input bundle ``

**Expected outputs:** Historical PyPSA network files, input hashes, configuration, workflow log, topology summary and validation tables.

**Comparison with the paper:** First compare network line/substation counts to the paper's 6001/3657 and geographic/voltage scope; then reproduce the paper's validation tables/plots. Count agreement alone is insufficient. Numeric tolerance for validation requires reading the complete target table and matching its input snapshots.

**Execution result:** Sources and construction route inspected; no scientific result reproduced here.

**Execution evidence:** None recorded.

**Blockers:** Historical release does not by itself identify the exact 2018 input snapshot.; Full target-table extraction and immutable input-file hashes are pending.

**Next action:** Inspect the model archive and article methods; recover the paper-era snapshot, then lock one validation comparison before solving.

**Gaps:** Historical release does not by itself identify the exact 2018 input snapshot.; Full target-table extraction and immutable input-file hashes are pending.

### Sources for pypsa

- [Title, authors, year, reported network counts and validation scope.](https://arxiv.org/abs/1806.01613) (inspected 2026-11-15).
- [Historical model, article relationship and archived-network link.](https://github.com/PyPSA/pypsa-eur/blob/192b605bb55e74184e7bd1bb4217dd01b25d020f/README.md) (inspected 2026-11-15).
- [Historical workflow source inspected.](https://github.com/PyPSA/pypsa-eur/blob/192b605bb55e74184e7bd1bb4217dd01b25d020f/Snakefile) (inspected 2026-11-15).

## pandapower

**pandapower** — How do switching states and transformer taps affect losses and operating constraints in the published 10 kV ring network?

**Route:** Paper result candidate. **Execution:** Not run. **Source confidence:** high.

### Paper for pandapower

Leon Thurner; Alexander Scheidler; Florian Schäfer; Jan-Hendrik Menke; Julian Dollichon; Friederike Meier; Steffen Meinecke; Martin Braun (2018). [Pandapower—An Open-Source Python Tool for Convenient Modeling, Analysis, and Optimization of Electric Power Systems](https://arxiv.org/abs/1709.06743). 10.1109/TPWRS.2018.2829021.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1109/TPWRS.2018.2829021). Metadata verification: confirmed. Full-text access: Open author preprint; Crossref title/authors/year verified.

**Target in the paper:** Paper case study: 10 kV ring network; feasible switching states and one-day optimized time series. Author repository explicitly identifies the three notebooks as the paper case study.

### Code and inputs for pandapower

[Artifact or upstream source](https://github.com/e2nIEE/pandapower-paper). Exact paper-associated case study, explicitly linked by maintainers to the IEEE reference article.

**Source inspected:** yes. **Ref:** master. **Commit:** 6213b92acd265cf7803ff4b8978542957d0c9777.

**Files:** grid.ipynb; switch_evaluation.ipynb; timeseries_simulation.ipynb; requirements.txt; data/; results/

**Terms:** pandapower BSD-3-Clause; artifact redistribution terms not yet independently established, so link rather than vendor notebooks/data.

**Environment and compute:** Author README requires pandapower 1.4.3; requirements.txt is otherwise unpinned (pandapower, python-igraph, xlrd, numba, notebook). Reconstruct a compatible legacy Python/pandas/numpy environment before installing. Small CPU network; switching/time-series batch can take longer than one power-flow solve.

**Inputs:** Bundled 10 kV network, load profiles and author reference results; do not replace the legacy network with a current built-in test network.

**Data access:** Data and reference results are present in the public author repository; data licensing and numeric reference files still need audit.

### Construct and compare pandapower

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Upstream: git clone https://github.com/e2nIEE/pandapower-paper ``
2. `` Proposed pin: cd pandapower-paper; git checkout 6213b92acd265cf7803ff4b8978542957d0c9777 ``
3. `` Upstream: pip install -r requirements.txt (only after adding the documented pandapower==1.4.3 constraint in an isolated compatible environment) ``
4. `` Upstream: jupyter notebook; execute grid.ipynb, switch_evaluation.ipynb, then timeseries_simulation.ipynb ``

**Expected outputs:** Executed notebooks, feasible switch-state table, one-day losses/line-loading/transformer-loading/voltage time series, and differences against results/.

**Comparison with the paper:** Compare exact admissible switch-state IDs and time-series arrays against the bundled author results and corresponding paper case-study plots; record units, tap positions and control objectives. Inspect result files and set tolerances before numerical comparison.

**Execution result:** Sources and construction route inspected; no scientific result reproduced here.

**Execution evidence:** None recorded.

**Blockers:** Legacy environment must be reconstructed; current pandapower API differs materially.; Paper figure numbering and exact numeric tolerances still need extraction.

**Next action:** Create a paper-specific environment lock, inspect results/, then run the three notebooks in original order.

**Gaps:** Legacy environment must be reconstructed; current pandapower API differs materially.; Paper figure numbering and exact numeric tolerances still need extraction.

### Sources for pandapower

- [Article identity verified.](https://api.crossref.org/works/10.1109/TPWRS.2018.2829021) (inspected 2026-11-15).
- [Author attribution, three case-study notebooks and required pandapower 1.4.3.](https://github.com/e2nIEE/pandapower-paper) (inspected 2026-11-15).
- [Actual dependency list; unpinned environment limitation.](https://raw.githubusercontent.com/e2nIEE/pandapower-paper/6213b92acd265cf7803ff4b8978542957d0c9777/requirements.txt) (inspected 2026-11-15).

## calliope

**Calliope** — Can the study's baseline carbon-neutral European energy system and near-optimal alternatives be regenerated?

**Route:** Paper result candidate. **Execution:** Not run. **Source confidence:** high.

### Paper for calliope

Bryn Pickering; Francesco Lombardi; Stefan Pfenninger (2022). [Diversity of options to eliminate fossil fuels and reach carbon neutrality across the entire European energy system](https://pmc.ncbi.nlm.nih.gov/articles/PMC9220955/). 10.1016/j.joule.2022.05.009.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1016/j.joule.2022.05.009). Metadata verification: confirmed. Full-text access: Open full text and author archives; metadata verified.

**Target in the paper:** Resource availability and experimental procedures; baseline least-cost model and SPORES alternatives. Rebuild baseline first, then reproduce selected capacity/cost results using the archived result ensemble.

### Code and inputs for calliope

[Artifact or upstream source](https://github.com/calliope-project/sector-coupled-euro-calliope). Exact article-associated workflow tag identified by the authors' README, plus prebuilt model DOI 10.5281/zenodo.5774988 and result archive DOI 10.5281/zenodo.6546817.

**Source inspected:** yes. **Ref:** 2021-11-29. **Commit:** f81453a454424e36f45eb0a304f28f82f6e126d7.

**Files:** README.md; environment.yaml; Snakefile; config/; run_scripts/; euro-calliope (submodule)

**Terms:** MIT workflow; archived data/results and solver terms separate.

**Environment and compute:** Historical customized Calliope 0.6.6 fork and submodules; archive includes model definitions. Original optimization used ETH Euler; obtain solver/version and license from the archived configuration before execution. Large CPU optimization; full ensemble used an HPC cluster. Begin with archive-only analysis and one baseline solve.

**Inputs:** Prebuilt sector-coupled 98-region model with 2018 input data, scenario overrides, SPORES settings and result archive (~1.1 GB).

**Data access:** Paper explicitly deposits model (5774988) and all results (6546817) on Zenodo. Full downloads were not performed.

### Construct and compare calliope

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Upstream clone, HTTPS equivalent: git clone --recurse-submodules https://github.com/calliope-project/sector-coupled-euro-calliope.git ``
2. `` Proposed paper pin: cd sector-coupled-euro-calliope; git checkout f81453a454424e36f45eb0a304f28f82f6e126d7; git submodule update --init --recursive ``
3. `` Current README route, which must be checked against the historical tag: conda env create -f environment.yaml ``
4. `` Current README route: snakemake --use-conda --cores 1 (build model); inspect historical optimization entry point before running it ``

**Expected outputs:** Baseline model/result NetCDF, exact scenario YAML, solver log, SPORES result NetCDF ensemble and figures.

**Comparison with the paper:** Compare baseline objective and carrier/technology capacities against archived result files before drawing any paper figure. Reproduce one selected paper plot with identical spatial and temporal aggregation; tolerance pending archived numeric-value audit. Subsequent versions corrected technology costs/efficiencies and transport, so current main is a different experiment.

**Execution result:** Sources and construction route inspected; no scientific result reproduced here.

**Execution evidence:** None recorded.

**Blockers:** Historical customized Calliope/solver environment not instantiated.; Archive numerical values, solver terms and exact figure target tolerance pending inspection.; Current main changes data and model assumptions; cannot silently substitute it for the article tag.

**Next action:** Download the prebuilt model and one result, verify checksums and scenario IDs, then agree a baseline objective/capacity comparison before optimization.

**Gaps:** Historical customized Calliope/solver environment not instantiated.; Archive numerical values, solver terms and exact figure target tolerance pending inspection.; Current main changes data and model assumptions; cannot silently substitute it for the article tag.

### Sources for calliope

- [Article experimental procedures and explicit code/model/result deposits.](https://pmc.ncbi.nlm.nih.gov/articles/PMC9220955/) (inspected 2026-11-15).
- [README identifies exact 2021-11-29 paper workflow and subsequent assumption changes.](https://github.com/calliope-project/sector-coupled-euro-calliope) (inspected 2026-11-15).
- [Published result archive identity, filename and size.](https://zenodo.org/records/6546817) (inspected 2026-11-15).
- [Historical tagged workflow and bespoke Calliope fork.](https://github.com/calliope-project/sector-coupled-euro-calliope/tree/f81453a454424e36f45eb0a304f28f82f6e126d7) (inspected 2026-11-15).

## sumo

**SUMO** — Can the published Luxembourg traffic-demand validation be repeated with the original scenario and simulator?

**Route:** Paper result candidate. **Execution:** Not run. **Source confidence:** high.

### Paper for sumo

Lara Codeca; Raphael Frank; Sebastien Faye; Thomas Engel (2017). [Luxembourg SUMO Traffic (LuST) Scenario: Traffic Demand Evaluation](https://doi.org/10.1109/MITS.2017.2666585). 10.1109/MITS.2017.2666585.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1109/MITS.2017.2666585). Metadata verification: confirmed. Full-text access: Metadata and author README inspected; full validation tables not yet read.

**Target in the paper:** Traffic-demand evaluation for 24-hour Luxembourg mobility; four author configurations: shortest-path/rerouting versus dynamic user equilibrium, static versus actuated signals.

### Code and inputs for sumo

[Artifact or upstream source](https://github.com/lcodeca/LuSTScenario). Author scenario repository explicitly cites the paper and warns that validation used SUMO 0.26.

**Source inspected:** yes. **Ref:** master. **Commit:** 5edb7ecb9ad196c39172b6eb95d19ed789f4b1a6.

**Files:** README.md; dua.static.sumocfg; dua.actuated.sumocfg; due.static.sumocfg; due.actuated.sumocfg

**Terms:** MIT scenario; SUMO licensing follows its chosen historical release.

**Environment and compute:** SUMO 0.26 legacy executable and scenario pin; modern SUMO runs are adaptations requiring a new comparison. 24-hour city simulation on CPU; historical binary/build support required.

**Inputs:** Author network, demand, routes, rerouting configuration and original detector/traffic-count validation data.

**Data access:** Scenario source public; original observation/validation data availability must be checked in the article.

### Construct and compare sumo

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed source pin: git clone https://github.com/lcodeca/LuSTScenario.git; cd LuSTScenario; git checkout 5edb7ecb9ad196c39172b6eb95d19ed789f4b1a6 ``
2. `` Upstream (using SUMO 0.26): sumo -c dua.static.sumocfg ``
3. `` Upstream alternatives: sumo -c dua.actuated.sumocfg; sumo -c due.static.sumocfg; sumo -c due.actuated.sumocfg ``

**Expected outputs:** Configured SUMO output files, simulation log, completed vehicle/trip counts, travel-time profiles and detector-flow comparison tables.

**Comparison with the paper:** Reproduce the article's time-of-day traffic-count and travel-time comparisons using its matching configuration and original validation data. Full text must establish exact target values and error metric/tolerance; do not infer validation from successful execution.

**Execution result:** Sources and construction route inspected; no scientific result reproduced here.

**Execution evidence:** None recorded.

**Blockers:** SUMO 0.26 environment not installed.; Full validation targets and observational data provenance are pending.

**Next action:** Retrieve the article validation tables and establish a working legacy SUMO binary, then run one configuration and compare the designated detector series.

**Gaps:** SUMO 0.26 environment not installed.; Full validation targets and observational data provenance are pending.

### Sources for sumo

- [Title/authors/year verified.](https://api.crossref.org/works/10.1109/MITS.2017.2666585) (inspected 2026-11-15).
- [Author command list, paper citation and explicit SUMO 0.26 validation restriction.](https://github.com/lcodeca/LuSTScenario/blob/5edb7ecb9ad196c39172b6eb95d19ed789f4b1a6/README.md) (inspected 2026-11-15).

## energyplus

**EnergyPlus** — How closely do a building simulator's cooling-system outputs match the analytical BESTEST test cases?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for energyplus

Robert H. Henninger; Michael J. Witte; Drury B. Crawley (2004). [Analytical and comparative testing of EnergyPlus using IEA HVAC BESTEST E100–E200 test suite](https://doi.org/10.1016/j.enbuild.2004.01.025). 10.1016/j.enbuild.2004.01.025.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1016/j.enbuild.2004.01.025). Metadata verification: confirmed. Full-text access: Publisher abstract/metadata inspected; LBNL validation reports openly available.

**Target in the paper:** Single-zone DX cooling analytical/comparative E100–E200 tests; first candidate is the base cooling case. Current Standard 140-2020 successor tests must be kept separate from 2004 results.

### Code and inputs for energyplus

[Artifact or upstream source](https://github.com/NatLabRockies/BESTEST-GSR). Official EnergyPlus/OpenStudio BESTEST workflow implementing later versions of the same benchmark family, with published result release assets; not the exact 2004 article code.

**Source inspected:** yes. **Ref:** v25.2. **Commit:** 80c3f2e56a501da996676086573f4c7f29fe9c5c.

**Files:** README.md; run_all_generate_reports.rb; results/; resources/

**Terms:** Read repository and bundled standard-resource terms before redistributing; EnergyPlus BSD-style license, OpenStudio dependency terms separate.

**Environment and compute:** OpenStudio 3.11.0 (includes EnergyPlus 25.2.0), Ruby 3.2.2, rubyXL and Parallel gems as documented at tag v25.2. CPU; upstream README estimates one test case under a minute and full suite under 30 minutes on typical computers; these estimates were not measured here.

**Inputs:** Packaged test-generation measures, weather/resource inputs, standard reporting spreadsheets and release reference results.

**Data access:** Official workflow and release outputs public. ASHRAE standard and resource-file reuse conditions separate; current test suite does not include every Standard 140 case.

### Construct and compare energyplus

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed pin: git clone https://github.com/NatLabRockies/BESTEST-GSR.git; cd BESTEST-GSR; git checkout 80c3f2e56a501da996676086573f4c7f29fe9c5c ``
2. `` Upstream: ruby run_all_generate_reports.rb ``

**Expected outputs:** Generated OSM and IDF models, EnergyPlus results, workflow_results.csv, populated RESULTS5-*.xlsx and per-case result ZIPs.

**Comparison with the paper:** For the current-version exercise compare cooling energy/capacity outputs with the pinned release's corresponding test-case reference spreadsheet and analytical benchmark range. To reproduce the 2004 article recover EnergyPlus 1.0.x inputs and E100–E200 reference tables; a modern BESTEST pass cannot establish that historical reproduction.

**Execution result:** Sources and construction route inspected; no scientific result reproduced here.

**Execution evidence:** None recorded.

**Blockers:** Exact 2004 source/input files and numerical reference targets not recovered.; OpenStudio and Ruby dependencies are not installed here.

**Next action:** Build a current pinned BESTEST cooling-case exercise first; inspect the 2004 full text and LBNL reports to determine whether a historical reproduction is feasible.

**Gaps:** Exact 2004 source/input files and numerical reference targets not recovered.; OpenStudio and Ruby dependencies are not installed here.

### Sources for energyplus

- [Article identity verified.](https://api.crossref.org/works/10.1016/j.enbuild.2004.01.025) (inspected 2026-11-15).
- [Published E100–E200 analytical test scope and historical EnergyPlus versions.](https://www.sciencedirect.com/science/article/abs/pii/S0378778804000362) (inspected 2026-11-15).
- [Actual current workflow commands, dependencies, outputs and missing-case limitations.](https://github.com/NatLabRockies/BESTEST-GSR/blob/80c3f2e56a501da996676086573f4c7f29fe9c5c/README.md) (inspected 2026-11-15).
- [Official historical validation reports.](https://simulationresearch.lbl.gov/dirpubs/valid_ep.html) (inspected 2026-11-15).

## wrf

**WRF** — Does an idealized atmospheric dynamical core produce the Held–Suarez benchmark circulation?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** high.

### Paper for wrf

Isaac M. Held; Max J. Suarez (1994). [A Proposal for the Intercomparison of the Dynamical Cores of Atmospheric General Circulation Models](https://journals.ametsoc.org/view/journals/bams/75/10/1520-0477_1994_075_1825_apftio_2_0_co_2.xml). 10.1175/1520-0477(1994)075<1825:APFTIO>2.0.CO;2.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1175/1520-0477(1994)075%3C1825:APFTIO%3E2.0.CO;2). Metadata verification: confirmed. Full-text access: Publisher metadata and abstract plus official WRF source inspected; NOAA hosts author full text.

**Target in the paper:** Held–Suarez long-term circulation benchmark, presented as latitude/vertical cross sections of time-averaged zonal means.

### Code and inputs for wrf

[Artifact or upstream source](https://github.com/wrf-model/WRF). Official WRF idealized implementation explicitly identifies the Held–Suarez article; a different dynamical core and coarser default resolution.

**Source inspected:** yes. **Ref:** master. **Commit:** 06d4240ae989cc3e50af412bb472df3d9048783c.

**Files:** test/em_heldsuarez/README.heldsuarez; test/em_heldsuarez/namelist.input

**Terms:** UCAR public-domain source notice; dependencies have their own terms.

**Environment and compute:** WRF ARW, supported C/Fortran compilers and NetCDF; compile idealized em_heldsuarez case. Serial configuration is available; MPI is optional for this controlled case. Long CPU integration; README notes its coarse default can run on a single processor. Higher resolution requires more compute.

**Inputs:** Bundled namelist and idealized dry global initial state; no real meteorological forcing or WPS geographic preprocessing required.

**Data access:** All idealized initial inputs bundled; numerical reference-field extraction from the article is still required.

### Construct and compare wrf

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed pin: git clone https://github.com/wrf-model/WRF.git; cd WRF; git checkout 06d4240ae989cc3e50af412bb472df3d9048783c ``
2. `` Official idealized workflow: ./configure; ./compile em_heldsuarez ``
3. `` Official idealized workflow: cd test/em_heldsuarez; ./ideal.exe; ./wrf.exe ``

**Expected outputs:** wrfinput file, time-indexed wrfout NetCDF and solver logs; postprocess zonal/time means of temperature and zonal wind.

**Comparison with the paper:** Default namelist runs 1000 days. Official README says averages use the last few hundred days and warns that default resolution is much coarser than the article. Compare latitude-pressure circulation structure and sensitivity to resolution/dissipation; no exact solution exists, so a pointwise exact-match tolerance is inappropriate. Fix averaging window and refinement comparison before claiming a benchmark reproduction.

**Execution result:** Sources and construction route inspected; no scientific result reproduced here.

**Execution evidence:** None recorded.

**Blockers:** No Fortran/NetCDF build environment qualified here.; Default resolution does not match the paper.; Averaging window, refinement settings and comparison criteria remain to be fixed.

**Next action:** Compile the idealized case in a dedicated scientific project, run a short setup check, then the documented climatology and a refinement study.

**Gaps:** No Fortran/NetCDF build environment qualified here.; Default resolution does not match the paper.; Averaging window, refinement settings and comparison criteria remain to be fixed.

### Sources for wrf

- [Publisher title/authors/year/DOI and benchmark purpose.](https://journals.ametsoc.org/view/journals/bams/75/10/1520-0477_1994_075_1825_apftio_2_0_co_2.xml) (inspected 2026-11-15).
- [Exact paper link, 1000-day route, resolution and qualitative-comparison limits.](https://github.com/wrf-model/WRF/blob/06d4240ae989cc3e50af412bb472df3d9048783c/test/em_heldsuarez/README.heldsuarez) (inspected 2026-11-15).
- [Official idealized compile/initialize/run workflow.](https://www2.mmm.ucar.edu/wrf/site/online_tutorial/ideal_exercise.html) (inspected 2026-11-15).

## opendrift

**OpenDrift** — Where does a 5000-particle unballasted life-raft ensemble drift over 48 hours?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for opendrift

Knut-Frode Dagestad; Johannes Röhrs; Øyvind Breivik; Bjørn Ådlandsvik (2018). [OpenDrift v1.0: a generic framework for trajectory modelling](https://gmd.copernicus.org/articles/11/1405/2018/). 10.5194/gmd-11-1405-2018.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.5194/gmd-11-1405-2018). Metadata verification: confirmed. Full-text access: Open article; metadata and paper Leeway listing/Figure 2 description inspected.

**Target in the paper:** Section 3.1 OpenLeeway code listing and Figure 2: 5000 objectType 26 particles near longitude 4.5, latitude 60, radius 1000 m at 2017-07-01 12:00 for 48 hours.

### Code and inputs for opendrift

[Artifact or upstream source](https://github.com/OpenDrift/opendrift). Current official Leeway example implements the same model family, but uses 2015 forcing and is not identical to the 2017 paper listing.

**Source inspected:** yes. **Ref:** master. **Commit:** ffd8e68b4be39ed42ed7187a875dd8eda65a3322.

**Files:** examples/example_leeway.py

**Terms:** GPL-2.0 code; ocean/wind forcing datasets and coastline have separate terms.

**Environment and compute:** OpenDrift with NetCDF/geospatial/plotting dependencies; for a historical result recover v1.0-era model and exact meteorological/ocean reader files. CPU ensemble; plotting/animation dependencies and external forcing downloads can dominate setup.

**Inputs:** Paper: 5000 life-rafts, 1000 m release radius, prescribed release time, 48-hour integration. Archive full wind/ocean forcing and coastline version; do not depend on a latest.nc endpoint.

**Data access:** Paper uses transient MET Norway THREDDS endpoints; exact historical files must be located. Current example uses different archived dates.

### Construct and compare opendrift

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed pin: git clone https://github.com/OpenDrift/opendrift.git; cd opendrift; git checkout ffd8e68b4be39ed42ed7187a875dd8eda65a3322 ``
2. `` Current upstream example: python examples/example_leeway.py ``
3. `` Proposed paper route: transcribe Section 3.1 listing into a dedicated run script and replace transient reader endpoints only with byte-identical archived forcing; record all differences ``

**Expected outputs:** Particle trajectory NetCDF (add explicit export), leeway_example.png and animation; preserve seed, reader datasets and object-property table.

**Comparison with the paper:** Compare Figure 2 endpoint distribution, drift extent and stranding statistics after matching forcing and release settings. The article listing lacks a fixed random seed, so use ensemble distribution/uncertainty criteria, not a trajectory-by-trajectory byte comparison. Numeric target/tolerance requires figure extraction or original output.

**Execution result:** Sources and construction route inspected; no scientific result reproduced here.

**Execution evidence:** None recorded.

**Blockers:** Paper-era forcing snapshots and output not recovered.; Random seed was not specified in the printed listing.; Current example cannot reproduce Figure 2 without matching the original inputs.

**Next action:** Retrieve historical forcing, freeze release/model settings and a statistical comparison; otherwise publish a clearly labeled current-data adaptation.

**Gaps:** Paper-era forcing snapshots and output not recovered.; Random seed was not specified in the printed listing.; Current example cannot reproduce Figure 2 without matching the original inputs.

### Sources for opendrift

- [Article identity and open access.](https://gmd.copernicus.org/articles/11/1405/2018/) (inspected 2026-11-15).
- [Indexed Section 3.1 listing and Figure 2 relationship inspected through web; PDF not downloaded.](https://gmd.copernicus.org/articles/11/1405/2018/gmd-11-1405-2018.pdf) (inspected 2026-11-15).
- [Actual current official example and different forcing dates.](https://github.com/OpenDrift/opendrift/blob/ffd8e68b4be39ed42ed7187a875dd8eda65a3322/examples/example_leeway.py) (inspected 2026-11-15).

## copasi

**COPASI** — Can the published PER/TIM circadian-clock model be rerun before exploring chaotic and birhythmic regimes?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for copasi

Jean-Christophe Leloup; Albert Goldbeter (1999). [Chaos and birhythmicity in a model for circadian oscillations of the PER and TIM proteins in drosophila](https://pubmed.ncbi.nlm.nih.gov/10366496/). 10.1006/jtbi.1999.0924.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://pubmed.ncbi.nlm.nih.gov/10366496/). Metadata verification: confirmed. Full-text access: PubMed metadata verified; author-hosted 15-page full text inspected through web, not downloaded. COPASI native/SBML model inspected.

**Target in the paper:** Section 2 equations (1a)–(1j); Figure 2 on article p.449 reports sustained oscillations close to a 24-hour period and gives the full baseline parameter set.

### Code and inputs for copasi

[Artifact or upstream source](https://github.com/copasi/COPASI). Maintainer-distributed model explicitly cites Leloup and Goldbeter 1999. This is a later COPASI encoding, not an identified original author code archive.

**Source inspected:** yes. **Ref:** develop. **Commit:** ed1677836f03f1b56a2da227f3fa8ba793dd125a.

**Files:** TestSuite/distribution/CircadianClock.cps; TestSuite/sbml/CircadianClockExportedFromCopasi.xml

**Terms:** Artistic-2.0 COPASI repository; preserve model/article attribution and inspect model redistribution notices before vendoring.

**Environment and compute:** COPASI GUI or CopasiSE, pinned version. Existing .cps has deterministic LSODA time course: 96 hours, 960 steps, 0.1 hour step, relative tolerance 1e-6 and absolute tolerance 1e-12. Small deterministic CPU model; parameter-scan and attractor analysis need longer controlled runs.

**Inputs:** Bundled CPS initial state, PER/TIM kinetic parameters and reaction definitions; task is initially scheduled=false and has no report target.

**Data access:** Executable model source is openly inspectable in the official COPASI tree; author full text located at https://utc.ulb.be/ARTICLES/1999_Leloup_JTB.pdf but not downloaded.

### Construct and compare copasi

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed pin: git clone https://github.com/copasi/COPASI.git; cd COPASI; git checkout ed1677836f03f1b56a2da227f3fa8ba793dd125a ``
2. `` GUI route: open TestSuite/distribution/CircadianClock.cps; inspect Time-Course settings; run the task and export concentrations ``
3. `` Proposed batch route after explicitly scheduling the time-course task and defining a report in a copy: CopasiSE CircadianClock-run.cps ``

**Expected outputs:** 96-hour concentration table and plots; saved run CPS containing scheduled task/report path; solver/version provenance.

**Comparison with the paper:** Target Figure 2 baseline concentration trajectories and period near 24 hours. The inspected COPASI exported SBML has transcription repression K=0.9 for Mp/Mt, whereas the Figure 2 caption specifies K_IP=K_IT=1 nM; change these only in a documented paper-matched copy after auditing every other parameter and initial condition. Then compare oscillation period, amplitudes and phase relations, with transient treatment and figure-derived tolerances fixed before running. The article describes these parameter values as arbitrary physiological-range choices, so execution is not empirical biological validation.

**Execution result:** Sources and construction route inspected; no scientific result reproduced here.

**Execution evidence:** None recorded.

**Blockers:** Native distributed model does not exactly match Figure 2: transcription repression K is 0.9 rather than the paper's 1 nM. Other parameters and initial conditions still need a complete audit.; Figure-reference numeric trajectories/tolerances not recovered.; CPS task/report must be configured before batch execution; blindly running the unscheduled source file does not generate the target trace.

**Next action:** Create a paper-matched copy for Figure 2, document the K_IP/K_IT correction and all initial conditions, configure a numeric report, and compare period/amplitudes/phase with digitized or author-supplied reference data.

**Gaps:** Native distributed model does not exactly match Figure 2: transcription repression K is 0.9 rather than the paper's 1 nM. Other parameters and initial conditions still need a complete audit.; Figure-reference numeric trajectories/tolerances not recovered.; CPS task/report must be configured before batch execution; blindly running the unscheduled source file does not generate the target trace.

### Sources for copasi

- [Verified publication identity and chaos/birhythmicity scope.](https://pubmed.ncbi.nlm.nih.gov/10366496/) (inspected 2026-11-15).
- [Explicit 1999 paper annotation, actual time-course duration/steps/tolerances, initially unscheduled task.](https://github.com/copasi/COPASI/blob/ed1677836f03f1b56a2da227f3fa8ba793dd125a/TestSuite/distribution/CircadianClock.cps) (inspected 2026-11-15).
- [Equivalent exported SBML model inspected.](https://github.com/copasi/COPASI/blob/ed1677836f03f1b56a2da227f3fa8ba793dd125a/TestSuite/sbml/CircadianClockExportedFromCopasi.xml) (inspected 2026-11-15).
- [Author full text inspected: Section 2 model equations and Figure 2 baseline parameters, target period and concentration traces.](https://utc.ulb.be/ARTICLES/1999_Leloup_JTB.pdf) (inspected 2026-11-15).

## tellurium

**Tellurium** — Can a standards-based archive regenerate the paper's Drosophila cell-cycle simulations?

**Route:** Paper result candidate. **Execution:** Not run. **Source confidence:** high.

### Paper for tellurium

J. Kyle Medley; Kiri Choi; Matthias König; Lucian Smith; Stanley Gu; Joseph Hellerstein; Stuart C. Sealfon; Herbert M. Sauro (2018). [Tellurium notebooks—An environment for reproducible dynamical modeling in systems biology](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006220). 10.1371/journal.pcbi.1006220.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1371/journal.pcbi.1006220). Metadata verification: confirmed. Full-text access: Open full text and actual COMBINE archive inspected.

**Target in the paper:** Second case study and Figures 4–6; reference 54 explicitly links calzone-fig1-fig3.omex. The archive contains Calzone2007-simulation-figure-1B.xml and BIOMD0000000144.xml.

### Code and inputs for tellurium

[Artifact or upstream source](https://github.com/0u812/tellurium-combine-archive-test-cases). Paper-author archive repository named in the article. Paper links a former demos/ path; current files reside in real-models/ and were actually inspected.

**Source inspected:** yes. **Ref:** master. **Commit:** eff025846c5b12ee4350f043623332158e05f262.

**Files:** real-models/calzone-fig1-fig3.omex; real-models/calzone-feedback-study.omex; real-models/calzone-log-plot.omex

**Terms:** Tellurium software Apache-2.0; individual model/COMBINE archive attribution and license must be checked independently.

**Environment and compute:** Tellurium, libRoadRunner, libSEDML, libCombine and plotting dependencies; paper-era Python 3.6 environment or separately labeled modern compatibility execution. Small biochemical ODE model on CPU; binary package compatibility may limit setup.

**Inputs:** Archive embeds SBML model and SED-ML model variants/solver protocol; inspected time courses use 250 and 180 units, 1000 points, KISAO:0000019; variant alters ksstg/kdstg and StgPc.

**Data access:** SBML and SED-ML bundled inside a public COMBINE archive; no clinical or human data needed.

### Construct and compare tellurium

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed pin: git clone https://github.com/0u812/tellurium-combine-archive-test-cases.git; cd tellurium-combine-archive-test-cases; git checkout eff025846c5b12ee4350f043623332158e05f262 ``
2. `` Tellurium execution API route to check against the chosen version: python -c "import tellurium as te; te.executeCombineArchive('real-models/calzone-fig1-fig3.omex', workingDir='run-calzone')" ``

**Expected outputs:** Executed SED-ML trajectories/plots and extracted model/experiment files, plus full environment, archive SHA256 and numeric result exports.

**Comparison with the paper:** Compare Wee1/MPF/String/cyclin trajectories and the encoded parameter variant against the paper's Figure 4 and original Calzone figure. Archive encodes the exact experiment but supplies no inspected numeric gold-standard CSV; extract or recover reference trajectories and establish tolerance before claiming reproduction.

**Execution result:** Sources and construction route inspected; no scientific result reproduced here.

**Execution evidence:** None recorded.

**Blockers:** Numeric reference trajectories/tolerances have not been recovered.; Paper-era runtime differs from current binary packages.; Archive/API compatibility not yet executed.

**Next action:** Run the pinned archive and export numeric trajectories, then compare them with archived figure data or agreed digitization of the exact figure.

**Gaps:** Numeric reference trajectories/tolerances have not been recovered.; Paper-era runtime differs from current binary packages.; Archive/API compatibility not yet executed.

### Sources for tellurium

- [Full-text figure mapping, code availability and references 54/55.](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006220) (inspected 2026-11-15).
- [Actual current archive path; original paper's demos/ URL no longer locates this file.](https://github.com/0u812/tellurium-combine-archive-test-cases/tree/eff025846c5b12ee4350f043623332158e05f262/real-models) (inspected 2026-11-15).
- [Downloaded and unzipped actual SBML/SED-ML protocol inspected.](https://github.com/0u812/tellurium-combine-archive-test-cases/blob/eff025846c5b12ee4350f043623332158e05f262/real-models/calzone-fig1-fig3.omex) (inspected 2026-11-15).

## brian2

**Brian 2** — Can the article's closed-loop eye-movement model be executed from the authors' notebook?

**Route:** Paper result candidate. **Execution:** Example executed. **Source confidence:** high.

### Paper for brian2

Marcel Stimberg; Romain Brette; Dan FM Goodman (2019). [Brian 2, an intuitive and efficient neural simulator](https://elifesciences.org/articles/47314). 10.7554/eLife.47314.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.7554/eLife.47314). Metadata verification: confirmed. Full-text access: Open full text, figure descriptions and author notebook inspected.

**Target in the paper:** Case study 2, Figure 3: retinal/motor spikes and eye/object position during 10 seconds. Alternative author notebooks cover Figures 1–7; Figure 8 benchmarks are separate supplementary code.

### Code and inputs for brian2

[Artifact or upstream source](https://github.com/brian-team/brian2_paper_examples). Exact author repository explicitly identified by the eLife article for reproducing Figures 1–7; original notebook uses seed 79620.

**Source inspected:** yes. **Ref:** master. **Commit:** 73045cd61322e923e96883dc97c0848154f79f8c.

**Files:** example_2_eye_movements.ipynb; environment.yml; README.md

**Terms:** Author code/data dual licensed CC BY 4.0 or MIT; Brian 2 simulator CeCILL-2.1.

**Environment and compute:** Author environment pins Python 3.6, Brian2 2.2.2.1, scipy 1.2, sympy 1.3 and Plotly 3.6. A modern Python/Brian run must be labeled compatibility execution and compared to historical output. Small CPU model; optional compiler backend, no GPU required.

**Inputs:** Notebook equations/units, 20 retinal neurons, 2 motor neurons, one eye, seed 79620, 10-second integration; no external dataset.

**Data access:** All inputs in the public author notebook; Figure 8 performance data separately supplied by eLife and should not be confused with Figure 3 outputs.

### Construct and compare brian2

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Upstream: git clone https://github.com/brian-team/brian2_paper_examples.git ``
2. `` Proposed pin: cd brian2_paper_examples; git checkout 73045cd61322e923e96883dc97c0848154f79f8c ``
3. `` Upstream: conda env create -f environment.yml ``
4. `` Upstream interactive route: open example_2_eye_movements.ipynb and execute cells in order; headless numeric execution can omit only the final Plotly presentation cell while preserving all model cells ``

**Expected outputs:** 10-second eye/object/target position arrays, retinal/motor spike trains and Figure 3-style plots; save model-cell hashes, seed, dt and runtime versions.

**Comparison with the paper:** Compare the Figure 3 eye/object time series and spike timings with author reference trajectories using the same seed and historical versions. Modern-version execution alone demonstrates runnable author code; it is not a validated reproduction of the exact published trace. Numeric reference data and tolerance need recovery/digitization.

**Execution result:** Unmodified author model cells executed on Python 3.12.16 / Brian2 2.9.0 / NumPy 1.26.4, NumPy backend. Seed 79620, dt 0.1 ms, 10 s, 100000 samples; 2406 retinal spikes and motor counts 56/51. Six bounded consistency checks passed. All arrays retained in NPZ/CSV with SHA256, plus a new Matplotlib plot. Original Plotly presentation cell omitted. Published numeric reference was not recovered; this is author-code compatibility execution, not a verified Figure 3 reproduction.

**Execution evidence:** [Run receipt](verification/brian2.json)

**Blockers:** Historical Python 3.6 environment not instantiated.; Exact published numeric trajectories/tolerance not available in the inspected notebook.

**Next action:** Run the historical environment or recover the paper/reference numeric traces; compare them with the retained modern execution under explicit error criteria. Current author model executes successfully.

**Gaps:** Historical Python 3.6 environment not instantiated.; Exact published numeric trajectories/tolerance not available in the inspected notebook.

### Sources for brian2

- [Figure 3 case-study and simulation description; separate Figure 8 benchmarks.](https://elifesciences.org/articles/47314/figures) (inspected 2026-11-15).
- [Article explicitly links author and eLife-archived code repositories.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6786860/) (inspected 2026-11-15).
- [Actual equations, seed and 10-second run inspected.](https://github.com/brian-team/brian2_paper_examples/blob/73045cd61322e923e96883dc97c0848154f79f8c/example_2_eye_movements.ipynb) (inspected 2026-11-15).
- [Original environment pin list.](https://github.com/brian-team/brian2_paper_examples/blob/73045cd61322e923e96883dc97c0848154f79f8c/environment.yml) (inspected 2026-11-15).
