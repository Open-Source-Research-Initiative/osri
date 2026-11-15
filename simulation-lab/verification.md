# Simulation Lab verification record

Checks performed by **Codex on 2026-11-15**, under Cole's direction. This is a technical record, not independent human scientific review. Cole authorized merging and publishing after the final technical review; the acceptance and release record is [PR #11](https://github.com/Open-Source-Research-Initiative/osri/pull/11).

## Original release: executed CPU examples

The four included examples ran in an isolated Python 3.12.16 environment on Linux x86-64. Direct versions were PyBaMM 26.10.1.1, QuantLib 1.44, Econ-ARK/HARK 0.17.2, and usd-core 26.11. The [complete tested dependency set](examples/requirements-tested.txt) and [machine-readable run records](verification/example-runs.json) preserve versions, parameters, checks, and file/source hashes.

| Example | Observed output | Checks passed |
| --- | --- | --- |
| Battery discharge | 121 samples; 3,600 s; initial 3.7717806 V and final 3.1716841 V; termination at final time | Finite positive voltage, increasing time, within requested horizon |
| European call | Analytical price 10.45058357; independent formula 10.45058357; Monte Carlo 10.45453708 with standard error 0.06579664 | Formula agreement, finite nonnegative payoffs, nonzero variance, estimate within five standard errors |
| Household saving | At period 120, mean resources 1.33295862, consumption 0.99375371, assets 0.33920491, all normalized by permanent income | Finite histories, positive consumption, nonnegative assets, budget identity |
| Battery results in USD | 121 time samples; every stored voltage equals the source CSV value | Sample times and values preserved, seconds retained, packaged CSV hash matches |

The option run used 50,000 paths and seed 42. Its approximate 95% interval was [10.32557566, 10.58349849]. The household run used 1,000 agents, 120 periods, and seed 42 with the baseline described in the [Carroll comparison](examples/economics.md). Values above describe these runs only.

All 16 recorded example checks passed. The run records' Python-source hashes were compared against the submitted scripts. Raw outputs were retained in the development run directory; they can be regenerated using the [CPU walkthrough](examples/cpu-walkthroughs.md). Bit-for-bit numerical identity on other hardware or dependency sets has not been established.

## Input and preservation checks

The [rejection-check record](verification/input-checks.json) confirms four observed behaviors:

- Changing the input voltage CSV made the USD adapter reject it before creating an output directory.
- Changing the parameter JSON also caused rejection before output creation.
- Reusing a battery output directory failed and preserved the existing run record.
- A zero QuantLib seed was rejected; that value does not select a fixed seed for this generator.

These checks test the examples' behavior. QuantLib's [generator implementation](https://github.com/lballabio/QuantLib/blob/master/ql/math/randomnumbers/mt19937uniformrng.cpp) documents the zero-seed behavior. The hash comparison checks consistency with a run record; it does not authenticate the scientific origin of an arbitrary record.

## Literature and upstream routes

The bibliography contains 36 DOI records checked against Crossref. The [reading-status field](papers.csv) distinguishes metadata checks from inspected full-text passages. Black–Scholes assumptions and Eq. 13 and Carroll's model/calibration passages were read in the supplied PDFs. The original articles are not redistributed.

At the original release, seven other example routes had inspected upstream instructions but were not executed: Isaac Lab, ABIDES, the historical Carroll reproduction, preCICE FSI3, PyPSA-Eur, service queues, and LuST. ViNoS was an artifact-access lead at that point; the later versioned-archive retrieval and new model executions are recorded in the follow-up below. No GPU training, historical container, full traffic model, energy workflow, or coupled CFD run is claimed here.

The catalog's source checks do not establish installation success for all 60 tools. Nor do the local checks establish mesh or time-step convergence, distributional convergence, empirical accuracy, real-world robot performance, or reproduction of an article's figures and tables.

## Catalog and website

`python3 simulation-lab/catalog.py` validates IDs, references, dates, local guide files, and the generated catalog/bibliography/BibTeX. The website consumes the same CSV records and runs that validator during its build. Website validation is recorded separately from simulation execution.

The site build and checker passed for 89 pages, 3,746 local links, and 198 search records, plus metadata, attribution, SVG fonts, and translation notices. All 14 site regression tests passed after integration with the current site design. Chromium checks covered case-insensitive search, domain filtering, combined filters, empty results, reset, keyboard-operated details and mobile navigation, CSV downloads, global search for all 60 tools, and content availability without JavaScript. Viewports from 320 to 1,440 pixels had no page-level horizontal overflow. Desktop and mobile screenshots were inspected. See the [browser-check record](verification/browser-check.json).

Documentation-link probes found two obsolete paths, which were replaced with the official QuantEcon and EnergyPlus documentation. After correction, 55 documentation endpoints returned HTTP 200; two GitHub documentation routes were inspected through the repository connector. Blender, MOOSE, and Elmer documentation hosts returned HTTP 403 to the automated probe. Their official links are retained; the access denial is not a finding that the documentation is missing.

## Follow-up: routes for the complete tool catalog

At Cole's request, six domain agents researched [construction routes for all 60 tools](research/README.md), and a seventh agent reviewed the records and live-checked 14 diverse primary paper/code routes. The records preserve the specific paper target, code relationship and version, inputs, terms, construction steps, comparison measure, execution status, and gaps. The [structured inventory](research/routes.json) and [CSV](research/routes.csv) keep these assessments separate from the original teaching runs.

New run receipts cover author/official software examples, a saved-output reanalysis, and a failed historical-code compatibility attempt. Each route links its actual receipt and compact numeric outputs. Full native outputs and environments remain in the development evidence directory with recorded hashes. The parent agent compared the recorded output hashes with the retained files. Source/output integrity, current regression-fixture agreement, convergence of one numerical example, and full paper-result reproduction are different checks. At that initial planning pass, no route claimed a reproduced published target; the later campaign below adds explicit comparisons to selected numerical targets.

ViNoS v1.3.2 was retrieved and inspected, so its original source-access gap is closed; its model has not run. ORE saved outputs differ from the paper's exact 50% exposure-concentration statement, and HARK's unmodified historical script fails under the modern API. MFEM variants that report nonconvergence remain failed numerical checks even when their process exits zero. These findings remain visible.

This follow-up is proposed work on a separate branch. Its technical and agent review does not record human scientific acceptance or authorization to publish the new result. The PR #11 authorization and checks above apply to the original release.

## Author-code campaign: 21 selected candidates

The [campaign index](reproductions/README.md) records all 21 candidates and links every attempt, compact receipt, output inventory and runnable bundle. Four selected numerical comparisons passed their declared rules: the DOLFINx preprint’s convergence/efficiency row, simmer’s printed result, Tellurium’s digitized Figure 4B points, and Unison’s Table 2 metrics. The complete declared pandapower scope has mixed results; matching published switch counts is reported separately from the remaining convention/state-count differences.

Other runs retain narrower or failed paper comparisons. GzDRL’s same-seed policy tensors agree but its return does not match the paper. HARK’s strict printed rounding target fails. AutoCkt training is incomplete and its reward threshold differs from strict constraint satisfaction. TaxFuncIntegr executes only the macro stage using public fitted inputs; restricted-PUF microsimulation was not run, and its negative government-spending closure fails feasibility. Dynare executes maintained third-party replication code with modern compatibility changes, not the inaccessible original estimation archive.

Calliope compares archived output ranges; an expired original solver license prevented fresh optimization. ORE lacks the original fresh-simulation generator. The shared preCICE/deal.II attempt ran but failed coupling convergence, including a retry, so it remains blocked for the scientific target despite zero process exits in one run.

The parent verified native output-file hashes before export and kept full sources, environments and failed attempts outside the hub contribution. Public files are selected, reusable teaching artifacts; Kubric asset derivatives retain CC BY-SA 4.0 terms. The bibliography now includes primary DataCite metadata for archival preprints as well as Crossref records. Agent scientific review and automated checks remain distinct from human scientific review.
