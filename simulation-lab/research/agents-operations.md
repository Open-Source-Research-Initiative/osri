# Agents, operations, and computing: paper-to-code routes

[All 60 tools](README.md) · [How to contribute](../contributing.md)

These are construction routes researched by agents. The execution line reports the bounded work actually performed; the comparison section defines what remains before claiming a published result. Human scientific review is pending.

## mesa

**Mesa** — How do local satisfaction rules generate residential segregation?

**Route:** Software paper example. **Execution:** Not run. **Source confidence:** medium.

### Paper for mesa

Ewout ter Hoeven; Jan Kwakkel; Vincent Hess; Thomas Pike; Boyu Wang; rht; Jackie Kazil (2025). [Mesa 3: Agent-based modeling with Python in 2025](https://joss.theoj.org/papers/10.21105/joss.07668). 10.21105/joss.07668.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.21105/joss.07668). Metadata verification: confirmed. Full-text access: Open JOSS metadata and linked official source inspected.

**Target in the paper:** Mesa 3 software article; official Schelling example is a teaching route, not a quantitative target reported in this paper.

### Code and inputs for mesa

[Artifact or upstream source](https://github.com/mesa/mesa). Official versioned example for the Mesa 3 software paper; not an author archive for a quantitative applied paper.

**Source inspected:** yes. **Ref:** v3.1.4. **Commit:** 8c24e1b021eef2e5b4282683f1a2801d1d37d076.

**Files:** mesa/examples/basic/schelling/model.py; mesa/examples/basic/schelling/Readme.md

**Terms:** Apache-2.0

**Environment and compute:** Isolated Python environment; Mesa v3.1.4 (commit 8c24e1b021eef2e5b4282683f1a2801d1d37d076). Preserve NumPy/Python versions and seed. Single CPU; small grid suitable for local execution.

**Inputs:** Schelling example grid dimensions, density, minority fraction, homophily and seed; record all explicitly.

**Data access:** Synthetic grid; no private data.

### Construct and compare mesa

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed: git clone https://github.com/mesa/mesa.git && cd mesa && git checkout 8c24e1b021eef2e5b4282683f1a2801d1d37d076 ``
2. `` Proposed: python -m venv .venv && .venv/bin/python -m pip install -e . ``
3. `` Proposed headless driver: import Schelling from mesa.examples.basic.schelling.model; construct with explicit seed; step until model.running is false or a fixed recorded cap; export model.datacollector.get_model_vars_dataframe(). ``

**Expected outputs:** Step-level happy-agent counts and final agent grid; record final number of occupied cells and seed.

**Comparison with the paper:** Check population and group-count conservation and repeated-seed equality; select a separately cited applied paper before claiming a reproduced segregation statistic.

**Execution result:** Source inspected; no execution or paper-result reproduction claimed.

**Execution evidence:** None recorded.

**Blockers:** No quantitative paper result selected in Mesa 3 article.

**Next action:** Build a versioned headless driver and add a published application with specified segregation metric.

**Gaps:** No quantitative paper result selected in Mesa 3 article.

### Sources for mesa

- [Software paper metadata and repository association.](https://joss.theoj.org/papers/10.21105/joss.07668) (inspected 2026-11-15).
- [Pinned implementation, parameters and data collection.](https://github.com/mesa/mesa/blob/8c24e1b021eef2e5b4282683f1a2801d1d37d076/mesa/examples/basic/schelling/model.py) (inspected 2026-11-15).
- [Example meaning and original model attribution.](https://github.com/mesa/mesa/blob/8c24e1b021eef2e5b4282683f1a2801d1d37d076/mesa/examples/basic/schelling/Readme.md) (inspected 2026-11-15).

## agents

**Agents.jl** — Can the Schelling benchmark and cross-framework timing comparison be rebuilt?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for agents

George Datseris; Ali R. Vahdati; Timothy C. DuBois (2022). [Agents.jl: a performant and feature-full agent-based modeling software of minimal code complexity](https://arxiv.org/html/2101.10072v3). 10.1177/00375497211068820.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1177/00375497211068820). Metadata verification: confirmed. Full-text access: Open arXiv author manuscript and Crossref metadata inspected.

**Target in the paper:** Section 3, Table 2 performance/line-count comparison; Section 2 Schelling code. Published stack: Agents.jl 4.4, Mesa 0.8, NetLogo 6.2, MASON 20.0.

### Code and inputs for agents

[Artifact or upstream source](https://github.com/JuliaDynamics/ABMFrameworksComparison). Author-maintained benchmark repository cited by the 2022 paper; current snapshot uses newer versions than the published comparison.

**Source inspected:** yes. **Ref:** main. **Commit:** 5ef9bf4fe05945688a10f7818d7e089fb88e34c3.

**Files:** README.md; Project.toml; Schelling/DECLARATION.md; Schelling/Agents/benchmark_schelling.jl

**Terms:** Repository license file exists; inspect exact text before redistributing benchmark code; Agents.jl itself MIT.

**Environment and compute:** Julia project in the pinned benchmark archive; current README uses Agents.jl 6.2.10, unlike paper 4.4. Avoid the README root installation commands; use an isolated existing Julia runtime. Single CPU; multi-language benchmark needs Julia, Python, Java/JDK and NetLogo.

**Inputs:** Current pinned Schelling benchmark: 1,000 agents in 40x40 grid, threshold 3/radius 1; 8,000 in 100x100, threshold 8/radius 2; 20 steps and 100 seeds from MersenneTwister(42).

**Data access:** Synthetic benchmark; declared initial conditions and seed generator bundled.

### Construct and compare agents

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed: git clone https://github.com/JuliaDynamics/ABMFrameworksComparison.git && cd ABMFrameworksComparison && git checkout 5ef9bf4fe05945688a10f7818d7e089fb88e34c3 ``
2. `` Upstream project setup: julia --project=. -e 'using Pkg; Pkg.instantiate()' ``
3. `` Proposed: cd Schelling/Agents && julia --project=../.. benchmark_schelling.jl; full upstream comparison route: bash runall.sh after all runtimes exist. ``

**Expected outputs:** Median runtime in milliseconds for small/large Schelling; equivalent run logs for other frameworks.

**Comparison with the paper:** Recover the publication-era commit/environment before testing Table 2 ratios. Current code can repeat a benchmark experiment but cannot establish the 2022 timing ratios; report CPU/compiler/JIT warm-up and implementation differences.

**Execution result:** Source inspected; no execution or paper-result reproduction claimed.

**Execution evidence:** None recorded.

**Blockers:** Current benchmark snapshot differs from publication versions.; Julia unavailable in shell PATH during this review.

**Next action:** Find and pin publication-era repository history; start with one model and compare outcomes before timings.

**Gaps:** Current benchmark snapshot differs from publication versions.; Julia unavailable in shell PATH during this review.

### Sources for agents

- [Sections 2-3, Tables 1-2 and citation of comparison repository.](https://arxiv.org/html/2101.10072v3) (inspected 2026-11-15).
- [Current framework versions and local comparison route.](https://github.com/JuliaDynamics/ABMFrameworksComparison/blob/5ef9bf4fe05945688a10f7818d7e089fb88e34c3/README.md) (inspected 2026-11-15).
- [Concrete benchmark sizes, seeds, steps and repetition count.](https://github.com/JuliaDynamics/ABMFrameworksComparison/blob/5ef9bf4fe05945688a10f7818d7e089fb88e34c3/Schelling/Agents/benchmark_schelling.jl) (inspected 2026-11-15).

## netlogo

**NetLogo** — How does fuel cost alter fishing effort in the German small-vessel fleet?

**Route:** Software paper example. **Execution:** Not run. **Source confidence:** medium.

### Paper for netlogo

Carsten Lemmen; Sascha Hokamp; Serra Örey; Jürgen Scheffran (2024). [Viable North Sea (ViNoS): A NetLogo Agent-based Model of German Small-scale Fisheries](https://joss.theoj.org/papers/10.21105/joss.05731). 10.21105/joss.05731.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.21105/joss.05731). Metadata verification: confirmed. Full-text access: Open JOSS record and original author archive retrieved and inspected.

**Target in the paper:** ViNoS software paper/model; exact published quantitative policy figure still needs selection. Archive reproducibility experiment is a deterministic functionality target, not a paper policy result.

### Code and inputs for netlogo

[Artifact or upstream source](https://doi.org/10.5281/zenodo.10798132). Author archive v1.3.2 dated 2024-03-08, shortly before the March 2024 JOSS publication. Concept DOI 7928199 now resolves to newer 2026 software and is not an immutable paper-version pin.

**Source inspected:** yes. **Ref:** v1.3.2. **Commit:** Not established..

**Files:** netlogo/vinos.nlogo; netlogo/behavior/reproducibility.xml; netlogo/behavior/vary-diesel.xml; ReadMe.md; LICENSE.md; doc/odd/odd.md

**Terms:** Model Apache-2.0; archive contains individually licensed data/assets including noncommercial/no-derivatives material. Consult per-file SPDX and LICENSES; do not redistribute entire archive under MIT.

**Environment and compute:** NetLogo >=6.4 as archived ReadMe requires; pin 6.4.0 for the first run and all extensions referenced in vinos.nlogo. CPU; Java/NetLogo runtime, GIS extensions, bundled spatial inputs.

**Inputs:** Bundled geospatial/resource data; archived reproducibility experiment sets random-seed 123456789, resets date to 2021-04-01 and runs 10 steps.

**Data access:** Archive retrieved (10.9 MB); SHA256 23e401344956f3c275d8df697039dd0f865e63c62fc073ba36a31365a3db2782; per-file data/asset reuse restrictions remain.

### Construct and compare netlogo

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Archive route: retrieve https://zenodo.org/api/records/10798132/files/platipodium/vinos-v1.3.2.zip/content and verify recorded checksum. ``
2. `` Upstream GUI route: launch NetLogo and open netlogo/vinos.nlogo; use go; inspect Effort MWh scene. ``
3. `` Proposed headless route after runtime verification: netlogo-headless.sh --model netlogo/vinos.nlogo --setup-file netlogo/behavior/reproducibility.xml --experiment reproducibility --table reproducibility.csv; retain the complete extracted folder layout. ``

**Expected outputs:** NetLogo BehaviorSpace CSV with count turtles; netlogo/results/total_avg.csv and weekly ESRI ASCII effort rasters.

**Comparison with the paper:** Repeat the same archived reproducibility experiment twice and compare numeric outputs; then run vary-diesel.xml with archived inputs. Published policy-effect tolerance/target is not specified by the inspected JOSS software article.

**Execution result:** Source inspected; no execution or paper-result reproduction claimed.

**Execution evidence:** None recorded.

**Blockers:** NetLogo runtime not installed/qualified here.; Specific quantitative published-result target still needs selection.

**Next action:** Run the archived deterministic experiment, then select a paper-linked policy comparison with explicit output/tolerance.

**Gaps:** Previous access-pending gap is now resolved by archive retrieval; the published existing guide should retain its historical review statement and receive a dated correction.; No model execution yet; data license review is required before repackaging inputs.

### Sources for netlogo

- [Published title/authors/date and software-archive association.](https://joss.theoj.org/papers/10.21105/joss.05731) (inspected 2026-11-15).
- [Immutable v1.3.2 archive metadata and file checksum; downloaded archive ReadMe, model and experiments inspected.](https://zenodo.org/api/records/10798132) (inspected 2026-11-15).
- [Concept DOI now points at version 1.7.0; cannot identify the 2024 code without version pin.](https://zenodo.org/api/records/7928199) (inspected 2026-11-15).

## gama

**GAMA** — Can the paper-linked Marrakech traffic and pollution demonstrator be reconstructed?

**Route:** Software paper example. **Execution:** Not run. **Source confidence:** medium.

### Paper for gama

Patrick Taillandier; Arnaud Grignard; Nicolas Marilleau; Damien Philippon; Quang-Nghi Huynh; Benoit Gaudou; Alexis Drogoul (2019). [Participatory Modeling and Simulation with the GAMA Platform](https://jasss.soc.surrey.ac.uk/22/2/3.html). 10.18564/jasss.3964.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.18564/jasss.3964). Metadata verification: confirmed. Full-text access: Open JASSS full text and linked GAMA model inspected.

**Target in the paper:** Figure 9 and note 6: MarrakAir installation and author repository; no numerical air-pollution validation target is stated for this demonstrator.

### Code and inputs for gama

[Artifact or upstream source](https://github.com/gnoubi/MarrakAir). Paper note 6 explicitly links this MarrakAir project; Figure 9 shows its tangible pollution interface.

**Source inspected:** yes. **Ref:** master. **Commit:** 52cbac5bf8c45696bf0736a429e29fbd7aa4a3fa.

**Files:** README.md; LICENSE; GAMA/marrakAir/models/marrakAir.gaml; GAMA/marrakAir/models/MarraSketch.gaml

**Terms:** GPL-3.0 repository LICENSE; individual GIS and third-party input provenance still needs review.

**Environment and compute:** GAMA desktop runtime compatible with legacy GAML; exact publication-time GAMA version must be recovered. Current compiler compatibility not tested. Desktop CPU/GPU for map rendering; physical 3D-printed display only if reproducing installation itself.

**Inputs:** Bundled GAMA/marrakAir/includes GIS layers and emissions CSV tables; keep map coordinate system and road/vehicle settings.

**Data access:** Model and GIS files publicly present; individual data license provenance not yet complete.

### Construct and compare gama

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed: git clone https://github.com/gnoubi/MarrakAir.git && cd MarrakAir && git checkout 52cbac5bf8c45696bf0736a429e29fbd7aa4a3fa ``
2. `` Upstream source route: import GAMA/marrakAir as a GAMA project; open models/marrakAir.gaml; launch GUI experiment MarrakAir (declared near end of model). ``
3. `` Proposed: first validate GIS rendering with models/MarraSketch.gaml; then record traffic/pollution measures from the main experiment; no headless command was verified. ``

**Expected outputs:** Interactive Marrakech traffic/pollution displays; reproducible parameter and seed record; numeric emissions export requires a documented driver.

**Comparison with the paper:** Reconstruct Figure 9 model/display behavior. A tangible 3D interface is a separate hardware project. Do not infer physically calibrated air-quality accuracy from a successful GUI run.

**Execution result:** Source inspected; no execution or paper-result reproduction claimed.

**Execution evidence:** None recorded.

**Blockers:** Legacy runtime version/compatibility unresolved.; The paper-linked example is demonstrative; no numerical target recovered.

**Next action:** Pin the historic GAMA release, qualify project compilation, then choose a quantitative applied GAMA study if a numerical reproduction is required.

**Gaps:** Legacy runtime version/compatibility unresolved.; The paper-linked example is demonstrative; no numerical target recovered.

### Sources for gama

- [Figure 9 and note 6 explicitly identify MarrakAir and source repository.](https://jasss.soc.surrey.ac.uk/22/2/3.html) (inspected 2026-11-15).
- [Actual model, emissions inputs, displays and experiment name.](https://github.com/gnoubi/MarrakAir/blob/52cbac5bf8c45696bf0736a429e29fbd7aa4a3fa/GAMA/marrakAir/models/marrakAir.gaml) (inspected 2026-11-15).
- [GPL-3.0 license text.](https://github.com/gnoubi/MarrakAir/blob/52cbac5bf8c45696bf0736a429e29fbd7aa4a3fa/LICENSE) (inspected 2026-11-15).

## ciw

**Ciw** — How do operator/nurse staffing and callback probability affect queue waits and utilization?

**Route:** Paper model adaptation. **Execution:** Example executed. **Source confidence:** high.

### Paper for ciw

Thomas Monks; Alison Harper (2023). [Improving the usability of open health service delivery simulation models using Python and web apps](https://openresearch.nihr.ac.uk/articles/3-48/v2). 10.3310/nihropenres.13467.2.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.3310/nihropenres.13467.2). Metadata verification: confirmed. Full-text access: Open article v2 full text and author archive read.

**Target in the paper:** Case-study urgent-care call centre; Listings 3-6 define parameter class and single_run/multiple_replications interface. Listing 6 uses 13 operators, 9 nurses, callback probability 0.4 and 5 replications.

### Code and inputs for ciw

[Artifact or upstream source](https://doi.org/10.5281/zenodo.8193001). Authors explicitly identify this v1.1.2 archive as source at publication; both implementations of the urgent-care call-centre model are included.

**Source inspected:** yes. **Ref:** v1.1.2. **Commit:** 38c102ff46292496d1b2a3e5e4f83f4ab6331f28.

**Files:** content/03_streamlit/ciw_model.py; binder/environment.yml; LICENSE

**Terms:** MIT code; synthetic service-system demonstration, no patient records.

**Environment and compute:** Executed: Python 3.12.16, NumPy 1.26.4, pandas 2.2.3, SimPy 4.0.1, Ciw 2.3.7 and setuptools 75.8.0. Paper uses Python 3.9.16; simulator versions match, Python/array/dataframe versions differ. Isolated venv; no source edits. Single CPU, seconds to minutes; no Streamlit server needed for headless model.

**Inputs:** Archived defaults: 1,000-minute collection, 13 operators, 9 nurses, callback probability 0.4; exponential arrival and triangular/uniform service distributions from archived module. Synthetic inputs.

**Data access:** Author archive retrieved; SHA256 e3a1db0130c74cba160d692764fe2a4a478263bbfb1205deea2a96d591936203. All inputs synthetic.

### Construct and compare ciw

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Archive route: retrieve author v1.1.2 DOI archive, verify checksum and preserve source module unchanged. ``
2. `` Tested isolated setup: python -m venv .venv; .venv/bin/python -m pip install numpy==1.26.4 pandas==2.2.3 simpy==4.0.1 ciw==2.3.7 setuptools==75.8.0. ``
3. `` From content/03_streamlit: import Experiment, multiple_replications from ciw_model; construct Experiment(n_operators=13, n_nurses=9, chance_callback=0.4); call multiple_replications(exp, n_reps=5); save DataFrame to CSV. ``
4. `` Executed harness: env/bin/python run_service_models.py; uses the archived module unchanged, writes unseeded Listing-6-style and fixed-seed replication CSVs and repeats seeded runs exactly. ``

**Expected outputs:** Five-row replication CSV: mean operator wait, operator utilization, mean nurse wait and nurse utilization.; ciw-seeded-five-replications.csv and service-execution.json; actual seeded means and SHA256 output hashes are retained.

**Comparison with the paper:** First reproduce the paper’s executable method and API. Compare simulator implementations over independent repeated runs using input-distribution checks and confidence intervals, not identical seeded trajectories. The tutorial does not supply a prespecified quantitative result/tolerance for Listing 6.

**Execution result:** Unmodified v1.1.2 module executed with ciw 2.3.7, Python 3.12.16, NumPy 1.26.4 and pandas 2.2.3. Listing-6-style five-replication wrapper and a separate five-seed experiment ran; four checks passed, including exact repeatability of the seeded experiment. Seeded mean operator wait 3.270952 min; mean nurse wait 45.480603 min. The tutorial supplies no quantitative target/tolerance, so no paper-result reproduction is claimed.

**Execution evidence:** [Run receipt](verification/ciw.json); [Numeric output](verification/ciw-simpy-listing6-five-replications.csv); [Numeric output](verification/ciw-ciw-listing6-five-replications.csv); [Numeric output](verification/ciw-simpy-seeded-five-replications.csv); [Numeric output](verification/ciw-ciw-seeded-five-replications.csv)

**Blockers:** Published tutorial provides no prespecified numeric target/tolerance.; Cross-implementation statistical equivalence has not been tested; five replications establish execution and bounded checks only.

**Next action:** Review source and replication results, define a quantitative reference comparison, and add uncertainty estimates before asserting equivalent simulator behavior.

**Gaps:** Exact historical Python3.9 dependency environment not recreated.; The first SimPy import failed because Python3.12 venv omitted pkg_resources; resolved by pinning setuptools75.8.0, with failed log retained in attempt-1/.; No independent human scientific review.

### Sources for ciw

- [Listings 3-6, declared environment and data-availability archive/license.](https://openresearch.nihr.ac.uk/articles/3-48/v2) (inspected 2026-11-15).
- [Author archive v1.1.2 and checksum.](https://zenodo.org/api/records/8193001) (inspected 2026-11-15).
- [Actual archived implementation and input defaults.](https://github.com/health-data-science-OR/simpy-streamlit-tutorial/blob/38c102ff46292496d1b2a3e5e4f83f4ab6331f28/content/03_streamlit/ciw_model.py) (inspected 2026-11-15).

## simmer

**simmer** — Does the paper’s M/M/1 simulation agree with its queueing-theory baseline?

**Route:** Paper result candidate. **Execution:** Selected paper target compared. **Source confidence:** high.

### Paper for simmer

Iñaki Ucar; Bart Smeets; Arturo Azcorra (2019). [simmer: Discrete-Event Simulation for R](https://www.jstatsoft.org/article/view/v090i02). 10.18637/jss.v090.i02.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.18637/jss.v090.i02). Metadata verification: confirmed. Full-text access: Open publisher metadata and complete R replication script inspected.

**Target in the paper:** Sections4.1–4.2, pp19–20, Figure3 and printed t-test; Section5.2 deterministic arrival example

### Code and inputs for simmer

[Artifact or upstream source](https://www.jstatsoft.org/article/download/v090i02/3818). Publisher-hosted R replication code distributed with the article; strongest direct paper-code route in this group.

**Source inspected:** yes. **Ref:** JSS v090i02 R replication supplement. **Commit:** Not established..

**Files:** v090i02 replication R script, Sections 4.1 and 4.2

**Terms:** Publisher supplement associated with open JSS article; simmer GPL-2.0; inspect supplement redistribution terms before copying into public repo.

**Environment and compute:** R with publication-compatible simmer/simmer.plot; archive exact R/package versions before reproducing graphics. Avoid running entire old performance-comparison supplement, which additionally requests Python 2.7 and Julia 0.5. Single CPU; R runtime required.

**Inputs:** Exponential arrival rate 2 and service rate 4; infinite queue, single server; Section 4.1 runs until 2,000; Section 4.2 100 replications each until 1,000/lambda.

**Data access:** Synthetic M/M/1 inputs; publisher supplement publicly downloadable.

### Construct and compare simmer

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Publisher command route: download the R replication code from https://www.jstatsoft.org/article/download/v090i02/3818. ``
2. `` Proposed: extract only Sections 4.1-4.2 into a documented driver without changing model expressions; run Rscript mm1-paper.R in an isolated R library. ``
3. `` Export arrival/resource monitors and replication-level end_time-start_time means; retain t.test output and plots. ``

**Expected outputs:** Resource/system occupancy plots, per-replication mean time in system, t.test confidence interval.

**Comparison with the paper:** Reproduces selected publisher-code printed numerical output within prespecified rounding tolerance. Additional validation uses independent seeds. Literal source interval is not accepted as independent100-replication uncertainty because forked streams are duplicated. Modern R runtime difference and pending human review remain explicit.

**Execution result:** All three printed Section4.2 numbers matched at7-decimal rounding; two independently seeded theory intervals contain analytic values; all1000 deterministic arrival records exactly match. Literal forked run has duplicated streams (50 unique replication means), retained as a source limitation.

**Execution evidence:** [Author-code attempt](../reproductions/simmer.md); [Run record](../reproductions/records/simmer.json)

**Blockers:** None recorded.

**Next action:** Integrate this bounded target comparison as a Lab example, retain duplicated-stream warning, and obtain human scientific review; optional exact historicalR reconstruction is separate.

**Gaps:** None recorded.

### Sources for simmer

- [Publisher title/authors/DOI and R replication supplement.](https://www.jstatsoft.org/article/view/v090i02) (inspected 2026-11-15).
- [Exact parameters, seeds, monitor calculations and 100-replication method.](https://www.jstatsoft.org/article/download/v090i02/3818) (inspected 2026-11-15).

## matsim-libs

**MATSim** — How do route replanning and congestion affect agents’ plan scores in Equil?

**Route:** Paper model adaptation. **Execution:** Not run. **Source confidence:** medium.

### Paper for matsim-libs

Andreas Horni (editor); Kai Nagel (editor); Kay W. Axhausen (editor) (2016). [The Multi-Agent Transport Simulation MATSim](https://matsim.org/the-book/). 10.5334/baw.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.5334/baw). Metadata verification: confirmed. Full-text access: Crossref book metadata and official book/user-guide page inspected; updated 2025 Part I provides concrete Equil scenario. Official MATSim book page supplies the three editors; Crossref includes partial/corporate contributor records.

**Target in the paper:** Book Part I, Chapter 2, Equil example; updated user guide Section 2.2 / Figure 2.3 has network and config explanation, not a reproduced 2016 numerical result.

### Code and inputs for matsim-libs

[Artifact or upstream source](https://github.com/matsim-org/matsim-code-examples). Official MATSim code-examples repository includes the Equil teaching scenario used in the book/user-guide tradition; current code differs from 2016 release.

**Source inspected:** yes. **Ref:** dev.x. **Commit:** 02a54c66ee6d8b29ec2ecfff77fd49109b97bdfc.

**Files:** README.md; scenarios/equil/config.xml; pom.xml; src/main/java/org/matsim/codeexamples/run/RunMatsim.java

**Terms:** GPL-2.0 code; MATSim example input/output terms generally CC BY 4.0, confirm this repository’s specific LICENSE and scenario notices.

**Environment and compute:** Java and Maven matched to pinned pom.xml; historical 2016 stack differs from current code. Official current example-project requires Java 25 and has moved inputs, so do not combine its instructions with stale scenario paths. Single CPU for 100-agent Equil; large urban case studies require much larger memory.

**Inputs:** Pinned code-examples scenarios/equil/config.xml: randomSeed 4711, network.xml, plans100.xml, iterations 0-10, 90% BestScore / 10% ReRoute.

**Data access:** Synthetic Equil inputs in inspected code-examples tree; no real population privacy dependency.

### Construct and compare matsim-libs

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed: git clone https://github.com/matsim-org/matsim-code-examples.git && cd matsim-code-examples && git checkout 02a54c66ee6d8b29ec2ecfff77fd49109b97bdfc ``
2. `` Proposed after matching JDK/Maven to pom.xml: mvn compile exec:java -Dexec.mainClass=org.matsim.codeexamples.run.RunMatsim -Dexec.args=scenarios/equil/config.xml. RunMatsim.java was inspected: it defaults to exactly this scenario; Maven invocation remains unexecuted. ``
3. `` Current alternative inspected: matsim-org/matsim-example-project README uses ./mvnw clean package then java -jar matsim-example-project-0.0.1-SNAPSHOT.jar run --config <path>; current snapshot lacks scenarios/equil/config.xml, so input path must be supplied explicitly. ``

**Expected outputs:** output/example iteration events, plan-score statistics and final plans/network; exact filenames follow selected MATSim version.

**Comparison with the paper:** Check source scenario population count, network connectivity, configuration echo and score/travel-time evolution. Treat updated Equil as a teaching-model reconstruction; recover 2016 inputs and numerical target before claiming a book-result reproduction.

**Execution result:** Source inspected; no execution or paper-result reproduction claimed.

**Execution evidence:** None recorded.

**Blockers:** Pinned repository is archived and has moved into matsim-libs/code-examples; choose one consistent source/version before building.; Build/classpath and historical-versus-current paper inputs still require qualification.

**Next action:** Qualify the inspected RunMatsim controller with its bundled Equil config in one consistent pinned Java/Maven environment; then add a paper-result target.

**Gaps:** Pinned repository is archived and has moved into matsim-libs/code-examples; choose one consistent source/version before building.; Build/classpath and historical-versus-current paper inputs still require qualification.

### Sources for matsim-libs

- [Official 2016 book attribution and distinction from updated user guide.](https://matsim.org/the-book/) (inspected 2026-11-15).
- [Updated Chapter 2 Equil scenario, network figure, population and replanning explanation.](https://www.matsim.org/files/book/partOne-latest.pdf) (inspected 2026-11-15).
- [Pinned actual config, seed, 100-agent file and iteration/replanning settings.](https://github.com/matsim-org/matsim-code-examples/blob/02a54c66ee6d8b29ec2ecfff77fd49109b97bdfc/scenarios/equil/config.xml) (inspected 2026-11-15).
- [Current Java 25 wrapper build/run route; scenario path drift discovered.](https://github.com/matsim-org/matsim-example-project/blob/74d23af9bf248f1ea099ebc9d2174be3650bfd96/README.md) (inspected 2026-11-15).
- [Actual main entry point loads the bundled Equil config and runs the controller.](https://github.com/matsim-org/matsim-code-examples/blob/02a54c66ee6d8b29ec2ecfff77fd49109b97bdfc/src/main/java/org/matsim/codeexamples/run/RunMatsim.java) (inspected 2026-11-15).

## ns-3-dev-git

**ns-3** — Can Unison preserve packet/flow outcomes while speeding up ns-3 execution?

**Route:** Paper result candidate. **Execution:** Selected paper target compared. **Source confidence:** medium.

### Paper for ns-3-dev-git

Songyuan Bai; Hao Zheng; Chen Tian; Xiaoliang Wang; Chang Liu; Xin Jin; Fu Xiao; Qiao Xiang; Wanchun Dou; Guihai Chen (2024). [Unison: A Parallel-Efficient and User-Transparent Network Simulation Kernel](https://doi.org/10.1145/3627703.3629574). 10.1145/3627703.3629574.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1145/3627703.3629574). Metadata verification: confirmed. Full-text access: Crossref metadata and authors’ evaluated-code README/driver inspected.

**Target in the paper:** Section6.2, Table2; exact thread/result determinism paragraph after Figure11.

### Code and inputs for ns-3-dev-git

[Artifact or upstream source](https://github.com/NASA-NJU/UNISON-for-ns-3). Paper-associated evaluated branch based on ns-3.36.1; README points to persistent evaluated artifact DOI 10.5281/zenodo.10077300.

**Source inspected:** yes. **Ref:** unison-evaluations. **Commit:** 7b3274167615c55ae8d69f7edee4e2dc2d81f706.

**Files:** README.md; exp.py; process.py

**Terms:** GPL-2.0 ns-3 codebase; preserve per-file notices.

**Environment and compute:** Ubuntu 22.04 upstream recommendation, ns-3.36.1 branch, C++ compiler, CMake and OpenMPI; exact evaluated archive preferred over current branch. Upstream accuracy example approximately 30 minutes; small experiments need 8 cores/16 GB; full suite requires up to 144 cores/512 GB.

**Inputs:** accuracy experiment: fat-tree k=4, cluster=[2,4], delay=500000 ns, 100 Mbps, 100-packet buffer, NewReno, load=0.7, 5 simulated seconds; driver compares Unison and default ns-3.

**Data access:** Synthetic network traffic; included flow-size CDF files.

### Construct and compare ns-3-dev-git

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed source retrieval: git clone --branch unison-evaluations https://github.com/NASA-NJU/UNISON-for-ns-3.git && cd UNISON-for-ns-3 && git checkout 7b3274167615c55ae8d69f7edee4e2dc2d81f706 ``
2. `` Upstream experiment command after isolated dependency and script audit: python3 exp.py accuracy (driver comments map this to Figure 2). ``
3. `` Do not run exp.py init on shared host: upstream initialization changes host settings and packages. Audit Experiment.run before executing any driver; choose a local-only sandbox and explicit hosts. ``
4. `` Upstream processing: inspect process.py and resulting results/NAME-DATE-TIME.csv; record exact mode, core count and random inputs. ``

**Expected outputs:** results/*.sh, *.txt and *.csv with automated command provenance and metrics; figure-specific processed CSV.

**Comparison with the paper:** All12 table entries agree to the predeclared half-last-digit threshold. This does not independently establish validity of packet models, table uncertainty, other paper experiments or hardware speedups.

**Execution result:** Seven full author-model simulations completed. All twelve Table 2 printed-value checks passed at predeclared 0.005 tolerance. Four two-cluster Unison runs (one/two/four threads plus repeated two-thread run) had identical 7,447,618 events and model metrics. One short diagnostic with no observed completed flows is preserved separately.

**Execution evidence:** [Author-code attempt](../reproductions/ns-3-dev-git.md); [Run record](../reproductions/records/ns-3-dev-git.json)

**Blockers:** Human scientific review is pending.; Native log values use six significant digits; two FCT comparisons touch the predeclared half-last-decimal threshold.; Tested one/two/four threads, not all one-to-sixteen threads or the distinct Figure 11 topology. No hardware speedup claim.

**Next action:** Human methods review of source, inputs and numerical comparison; then extend to the remaining named paper targets.

**Gaps:** Human scientific review is pending.; Native log values use six significant digits; two FCT comparisons touch the predeclared half-last-decimal threshold.; Tested one/two/four threads, not all one-to-sixteen threads or the distinct Figure 11 topology. No hardware speedup claim.

### Sources for ns-3-dev-git

- [Published title/authors/date/DOI.](https://api.crossref.org/works/10.1145/3627703.3629574) (inspected 2026-11-15).
- [Evaluated artifact DOI, hardware/software requirements and outputs.](https://github.com/NASA-NJU/UNISON-for-ns-3/blob/7b3274167615c55ae8d69f7edee4e2dc2d81f706/README.md) (inspected 2026-11-15).
- [Figure-specific experiment definitions and potentially host-mutating initialization.](https://github.com/NASA-NJU/UNISON-for-ns-3/blob/7b3274167615c55ae8d69f7edee4e2dc2d81f706/exp.py) (inspected 2026-11-15).

## simgrid

**SimGrid** — Can the paper’s simulator-version time and memory comparison be rebuilt?

**Route:** Paper result candidate. **Execution:** Example executed. **Source confidence:** medium.

### Paper for simgrid

Henri Casanova; Arnaud Giersch; Arnaud Legrand; Martin Quinson; Frédéric Suter (2025). [Lowering entry barriers to developing custom simulators of distributed applications and platforms with SimGrid](https://fred-suter.com/files/publications/simgrid-parco25.pdf). 10.1016/j.parco.2025.103125.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.1016/j.parco.2025.103125). Metadata verification: confirmed. Full-text access: Open author manuscript (19 pages) and upstream benchmark repository inspected.

**Target in the paper:** Introduction paragraph before Section 2; Section 7, Figures 13-14; reference 66.

### Code and inputs for simgrid

[Artifact or upstream source](https://github.com/simgrid/coordinator_worker_flashback). Explicitly cited as reference 66 in 2025 paper; coordinator-worker scalability benchmark for Figures 13-14.

**Source inspected:** yes. **Ref:** main. **Commit:** b09453d19541b7186703f4d651c1bba790461e44.

**Files:** README.md; Makefile; run_experiments.py; plot_results.py

**Terms:** No repository-wide license detected in inspected tree; SimGrid core LGPL-2.1. Link artifact; resolve benchmark permission before redistributing its code.

**Environment and compute:** Docker or equivalent isolated builds of exact SimGrid v3/v4 commits using same compiler; Python3/matplotlib for experiment driver/plots. Upstream benchmark snapshot requires edits to select correct versions. Benchmark runs on one physical core; many simulated actors; container builds may dominate setup time.

**Inputs:** 100 randomly routed links; core speeds 100-200 Mflop/s, bandwidths 100-200 MB/s; each workunit sends 100 MB then computes 100 Mflop; energy simulation enabled.

**Data access:** Synthetic compute/network platform; random platform generation must be pinned.

### Construct and compare simgrid

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Proposed: git clone https://github.com/simgrid/coordinator_worker_flashback.git && cd coordinator_worker_flashback && git checkout b09453d19541b7186703f4d651c1bba790461e44 ``
2. `` Upstream: edit Makefile to select simulator versions, then make build. ``
3. `` Upstream: make run; parameter overrides MIN_WORKERS, MAX_WORKERS, MIN_TASKS, MAX_TASKS, NUM_TRIALS are documented. For paper Figures 13-14 use paper’s 10 repeats and ranges after matching the driver/version definitions. ``

**Expected outputs:** Experiment timing and maximum RSS data; two PDF figures for worker/task-count sweeps.

**Comparison with the paper:** Four makespan consistency checks passed. Local RSS reduction at the tested endpoints is 5.1994x/5.3566x, exceeding the article reported 4.1 minimum. The lower-endpoint wall-time ratio is 1.2995x, below its reported 1.45 minimum. Different host/compiler and partial curves prevent a historical performance-reproduction claim.

**Execution result:** 48 native runs: forty performance runs (two Figure 13 endpoints, ten seeds and two versions), six small makespan-validation runs and two paper-size makespan-validation runs. All exited zero; all four makespan checks matched to 0.000001 simulated seconds.

**Execution evidence:** [Author-code attempt](../reproductions/simgrid.md); [Run record](../reproductions/records/simgrid.json)

**Blockers:** Human scientific review is pending.; Exact dedicated historical CPU/compiler not matched; shared-host load affects wall time.; Intermediate Figure 13 points and Figure 14 core-count sweep remain unexecuted.; Paper introduction calls 3.10 v3 and describes developments through 3.36 culminating in v4. Reference 66 Dockerfiles pin 3.10/3.36, but the exact development commit behind every printed v4 curve observation is unestablished.

**Next action:** Human methods review of source, inputs and numerical comparison; then extend to the remaining named paper targets.

**Gaps:** Human scientific review is pending.; Exact dedicated historical CPU/compiler not matched; shared-host load affects wall time.; Intermediate Figure 13 points and Figure 14 core-count sweep remain unexecuted.; Paper introduction calls 3.10 v3 and describes developments through 3.36 culminating in v4. Reference 66 Dockerfiles pin 3.10/3.36, but the exact development commit behind every printed v4 curve observation is unestablished.

### Sources for simgrid

- [Official citation metadata and open author manuscript.](https://simgrid.org/publications.html) (inspected 2026-11-15).
- [Figures 13-14 parameters, repetition count, reference 66 and reported performance ratios.](https://fred-suter.com/files/publications/simgrid-parco25.pdf) (inspected 2026-11-15).
- [Actual benchmark build/run instructions.](https://github.com/simgrid/coordinator_worker_flashback/blob/b09453d19541b7186703f4d651c1bba790461e44/README.md) (inspected 2026-11-15).
- [Version-selection and experiment orchestration.](https://github.com/simgrid/coordinator_worker_flashback/blob/b09453d19541b7186703f4d651c1bba790461e44/Makefile) (inspected 2026-11-15).

## simpy

**SimPy** — How do operator/nurse staffing and callback probability affect queue waits and utilization?

**Route:** Paper model adaptation. **Execution:** Example executed. **Source confidence:** high.

### Paper for simpy

Thomas Monks; Alison Harper (2023). [Improving the usability of open health service delivery simulation models using Python and web apps](https://openresearch.nihr.ac.uk/articles/3-48/v2). 10.3310/nihropenres.13467.2.

**Publication type:** See primary metadata record; not classified here.. [Primary metadata](https://api.crossref.org/works/10.3310/nihropenres.13467.2). Metadata verification: confirmed. Full-text access: Open article v2 full text and author archive read.

**Target in the paper:** Case-study urgent-care call centre; Listings 3-6 define parameter class and single_run/multiple_replications interface. Listing 6 uses 13 operators, 9 nurses, callback probability 0.4 and 5 replications.

### Code and inputs for simpy

[Artifact or upstream source](https://doi.org/10.5281/zenodo.8193001). Authors explicitly identify this v1.1.2 archive as source at publication; both implementations of the urgent-care call-centre model are included.

**Source inspected:** yes. **Ref:** v1.1.2. **Commit:** 38c102ff46292496d1b2a3e5e4f83f4ab6331f28.

**Files:** content/03_streamlit/model.py; binder/environment.yml; LICENSE

**Terms:** MIT code; synthetic service-system demonstration, no patient records.

**Environment and compute:** Executed: Python 3.12.16, NumPy 1.26.4, pandas 2.2.3, SimPy 4.0.1, Ciw 2.3.7 and setuptools 75.8.0. Paper uses Python 3.9.16; simulator versions match, Python/array/dataframe versions differ. Isolated venv; no source edits. Single CPU, seconds to minutes; no Streamlit server needed for headless model.

**Inputs:** Archived defaults: 1,000-minute collection, 13 operators, 9 nurses, callback probability 0.4; exponential arrival and triangular/uniform service distributions from archived module. Synthetic inputs.

**Data access:** Author archive retrieved; SHA256 e3a1db0130c74cba160d692764fe2a4a478263bbfb1205deea2a96d591936203. All inputs synthetic.

### Construct and compare simpy

The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.

1. `` Archive route: retrieve author v1.1.2 DOI archive, verify checksum and preserve source module unchanged. ``
2. `` Tested isolated setup: python -m venv .venv; .venv/bin/python -m pip install numpy==1.26.4 pandas==2.2.3 simpy==4.0.1 ciw==2.3.7 setuptools==75.8.0. ``
3. `` From content/03_streamlit: import Experiment, multiple_replications from model; construct Experiment(n_operators=13, n_nurses=9, chance_callback=0.4); call multiple_replications(exp, n_reps=5); save DataFrame to CSV. ``
4. `` Executed harness: env/bin/python run_service_models.py; uses the archived module unchanged, writes unseeded Listing-6-style and fixed-seed replication CSVs and repeats seeded runs exactly. ``

**Expected outputs:** Five-row replication CSV: mean operator wait, operator utilization, mean nurse wait and nurse utilization.; simpy-seeded-five-replications.csv and service-execution.json; actual seeded means and SHA256 output hashes are retained.

**Comparison with the paper:** First reproduce the paper’s executable method and API. Compare simulator implementations over independent repeated runs using input-distribution checks and confidence intervals, not identical seeded trajectories. The tutorial does not supply a prespecified quantitative result/tolerance for Listing 6.

**Execution result:** Unmodified v1.1.2 module executed with simpy 4.0.1, Python 3.12.16, NumPy 1.26.4 and pandas 2.2.3. Listing-6-style five-replication wrapper and a separate five-seed experiment ran; four checks passed, including exact repeatability of the seeded experiment. Seeded mean operator wait 4.118375 min; mean nurse wait 43.501354 min. The tutorial supplies no quantitative target/tolerance, so no paper-result reproduction is claimed.

**Execution evidence:** [Run receipt](verification/simpy.json); [Numeric output](verification/simpy-simpy-listing6-five-replications.csv); [Numeric output](verification/simpy-ciw-listing6-five-replications.csv); [Numeric output](verification/simpy-simpy-seeded-five-replications.csv); [Numeric output](verification/simpy-ciw-seeded-five-replications.csv)

**Blockers:** Published tutorial provides no prespecified numeric target/tolerance.; Cross-implementation statistical equivalence has not been tested; five replications establish execution and bounded checks only.

**Next action:** Review source and replication results, define a quantitative reference comparison, and add uncertainty estimates before asserting equivalent simulator behavior.

**Gaps:** Exact historical Python3.9 dependency environment not recreated.; The first SimPy import failed because Python3.12 venv omitted pkg_resources; resolved by pinning setuptools75.8.0, with failed log retained in attempt-1/.; No independent human scientific review.

### Sources for simpy

- [Listings 3-6, declared environment and data-availability archive/license.](https://openresearch.nihr.ac.uk/articles/3-48/v2) (inspected 2026-11-15).
- [Author archive v1.1.2 and checksum.](https://zenodo.org/api/records/8193001) (inspected 2026-11-15).
- [Actual archived implementation and input defaults.](https://github.com/health-data-science-OR/simpy-streamlit-tutorial/blob/38c102ff46292496d1b2a3e5e4f83f4ab6331f28/content/03_streamlit/model.py) (inspected 2026-11-15).
