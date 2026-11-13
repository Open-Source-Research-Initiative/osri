# Finding a worthwhile research question

Guidance for OSRI's six [research areas](../areas/README.md) and shared Simulation Lab. A person directs the question, judges the evidence, and takes responsibility for the conclusions. Agents can help search, extract, code, and challenge an argument; their output still needs checking.

Anyone can bring a question, a paper, a dataset lead, or an explanation of a problem. You do not need a completed topic brief, academic credentials, coding experience, or an agent subscription to start. The [contribution standards](../governance/contribution-standards.md) explain how to make a contribution and get help.

Share a research idea in [Ideas](https://github.com/Open-Source-Research-Initiative/.github/discussions/new?category=ideas). Ask questions or request help in [Q&A](https://github.com/Open-Source-Research-Initiative/.github/discussions/new?category=q-a).

## Start with a useful uncertainty

State what you want to learn, about which people or system, and under which conditions. Explain why someone would use the answer. For example, “How does bursty demand change waiting time under two dispatch rules at the same staffing level?” is a question that can guide a bounded experiment. “Use AI to improve services” needs further definition.

A worthwhile contribution can resolve a disagreement, test an assumption, or reproduce a consequential result. It can explain a failure to reproduce, improve a method, compare alternatives fairly, or make fragmented evidence usable. A topic does not become useful merely because a search returned few papers. Replacing one variable or dataset with another also needs a reason that matters to the question.

## Check fit and feasibility together

Use these questions to compare a small set of ideas. Write the evidence and remaining uncertainty in plain language. A total score would hide the tradeoffs.

| Check | What to establish |
| --- | --- |
| Purpose and scope | Who needs the answer? What system, population, setting, time span, comparison, and outcome are included? Does the question fit an OSRI area or a connected contribution? |
| Closest research | Find the closest studies and recent reviews, then inspect their methods and limitations. Compare the exact question, sample or model, measurements, and proposed contribution. Search relevant preprints and protocols when applicable. Record the databases, search terms, dates, and access limits. |
| Evidence and access | Locate the actual codebook, source text, model, or benchmark. Check variables, time coverage, units, missingness, access conditions, reuse terms, and redistribution limits. A public landing page does not establish that the needed data or full text is available. |
| Valid method | Identify the unit of analysis, comparison, assumptions, uncertainty, and main threats to validity. Explain what the design could establish and which claims would exceed it. For a review, check whether the evidence supports a map, narrative synthesis, or quantitative pooling. |
| People and resources | Identify the domain and methods help needed, a human lead, and a small first task. Estimate storage, memory, runtime, software, and any paid access from a bounded pilot before proposing a larger study. Available compute does not establish scientific validity. |
| Contribution and output | State what a reader would learn beyond the closest work, even if the result is negative. Identify a useful first artifact and a plausible audience. Keep publication form provisional until the evidence and venue scope are clear. |

Start searches with synonyms for the question's main concepts, then follow references backward and citations forward from the closest papers. Use databases that cover the field; PubMed alone cannot map engineering, economics, or policy research. Search counts, citation counts, an author's publication record, and an agent's answer do not establish novelty. Read the nearest work before describing an idea as a gap.

Public data also require careful interpretation. For example, the [BRFSS documentation](https://www.cdc.gov/brfss/annual_data/annual_2024.html) describes weighting, coverage, comparability, and changes to its public file. The [Consumer Expenditure Survey](https://www.bls.gov/cex/pumd.htm) distinguishes public microdata from published tables and provides a guide for reproducing those tables. Those details can change whether a question is answerable.

## Choose a manageable route

**For a first contribution:** choose a question you care about and bring one credible source. With a maintainer or collaborator, you can summarize what the source establishes or explain one uncertainty. You can also check a few source records or reproduce one documented table or figure. A small literature comparison or a careful technical explanation can be useful without original analysis. Catalog topics H02 and P01 have entry tasks based on reading and source checking. S02 also has a browser model for learning.

**For an experienced contributor:** turn the question into a study design. Compare the closest research and inspect the source definitions. Specify the analysis or experiment, identify assumptions and alternatives, and plan uncertainty and sensitivity checks. Reproduce the baseline before changing it. Record deviations from the source method. Seek domain and methods review matched to the claim, especially for causal inference, complex surveys, optimization, and scientific simulation.

The installed topic skills offer parts of this work. Literature verification and documented replication methods transfer well. Clinical cohort defaults, professor matching, numerical “gap” rankings, and suggested journal tiers need separate judgment. They are not OSRI selection rules. The initial Healthcare scope is nonclinical public health and health systems research. Public or de-identified data do not by themselves settle every project's ethics, consent, or data-use requirements.

## Use the Simulation Lab to test defined models

A practical starting point is a published model or benchmark with explicit inputs. Reproduce a stated result, check the implementation, and change one justified assumption or decision rule. Specify the experiment's conditions, comparison, outcomes, randomness, stopping rules, and uncertainty. Check numerical or simulation error as appropriate, and compare against analytical cases, reference calculations, or independent evidence.

The [STRESS guidelines](https://doi.org/10.1080/17477778.2018.1442155) cover reporting for discrete-event, agent-based, and system-dynamics simulation. [NIST's Lennard-Jones reference results](https://www.nist.gov/mml/csd/chemical-informatics-group/lennard-jones-fluid-properties) illustrate the need to match the stated model conditions when checking code. Reproducing reference calculations is bounded evidence about implementation. Claims about a real system require evidence connecting that model to that system. A hypothetical scenario remains conditional on its assumptions.

## Match the publication to the completed work

| Form | Appropriate use |
| --- | --- |
| Journal article | A developed empirical, review, replication, theoretical, or methods contribution with evidence that meets the journal's scope and requirements. |
| Full conference paper | A complete contribution suited to a field's conference and review process; distinguish it from an abstract, poster, or talk. |
| Preprint | A shareable research manuscript with its review status clear. Use arXiv where its subject categories fit; otherwise choose an appropriate repository. |
| Substantive research blog or technical essay | A source-backed analysis, replication, evidence synthesis, method, finding, or developed argument with enough detail to assess it. Routine updates and announcements are different outputs. |

These are possible routes, not promises of novelty, acceptance, or publication. Software, data, and models can support any of them. Follow the [publication tracking conventions](../publications/README.md) when one research work produces several outputs.

## A lean topic brief

Use this when it helps develop an idea; incomplete entries are useful discussion points.

```text
Working question and OSRI area:
Human lead or person bringing the idea:
Who could use the answer, and why:
Closest research and what remains uncertain:
Source/data/model links; access and reuse conditions:
Initial method, comparison, and unit of analysis:
Main assumptions and validity risks:
Small first task; help and compute needed:
Possible contribution and output form:
What would make us narrow, change, or stop this approach:
```

## Example questions to explore

The [example-topic catalog](example-topics.csv) contains twelve **IDEAS**, two per area. Each row includes a question, initial approach, official source, skills and compute needs, and possible outputs. It also includes a verified example paper or methods paper. The examples demonstrate approaches; they do not establish that the candidate questions are new. All ideas remain pending scope, literature, data, reuse, and methods checks.

| IDs | Area | Candidate focus |
| --- | --- | --- |
| H01–H02 | Healthcare | Reported cost barriers to care; how service simulations represent missed appointments and access. |
| E01–E02 | Engineering | Queue dispatch under bursty demand; project scheduling under duration uncertainty. |
| I01–I02 | Informatics | RNA-seq analysis sensitivity; molecular-simulation numerical sensitivity in Computational Natural Sciences. |
| C01–C02 | Economics | Household energy spending measurement; hypothetical cash-transfer microsimulation. |
| S01–S02 | Social and Behavioral Sciences | Survey weighting and political interest; update rules in segregation models. |
| P01–P02 | Public Policy | Government open-data metadata; reproduction of a policy-evaluation methods example. |

Sources and reference identities were checked on 2026-11-13. This was a bounded source and method check, not a systematic novelty search, dataset audit, executed analysis, simulation run, or venue assessment. The catalog records access limits and bibliographic discrepancies where found.
