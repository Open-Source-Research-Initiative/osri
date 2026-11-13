# Research resource starter catalog

[Browse the resource catalog](https://open-source-research-initiative.github.io/resources/) or [download the comma-separated values (CSV) table](resources.csv). It lists 28 starting points for literature discovery, existing-data research, analysis, simulation, and research practice. It supports the six [OSRI research areas](../areas/README.md) and the proposed shared Simulation Lab. Healthcare use should follow OSRI's initial public health, health systems, and nonclinical scope. Operations Research and Decision Science sit within Engineering; Computational Natural Sciences sits within Informatics.

This is a starter list, not an exhaustive inventory, endorsement, or qualification for a particular study. Official provider and maintainer documentation was reviewed on **2026-11-13**. No authenticated access, software installation, dataset download, or application programming interface (API) integration test was performed. A documentation check does not establish that an endpoint works or a dataset answers the question. It does not establish that a model predicts the system being studied.

## Choose a starting point

| Research task | Useful catalog entries |
| --- | --- |
| Find papers, identifiers, citations, and related works | PubMed, Europe PMC, Crossref, OpenAlex |
| Study population health and local public health needs | WHO Data, CDC PLACES, NHANES public-use files |
| Compare economic, demographic, and policy indicators | World Bank Indicators, OECD Data Explorer, Eurostat, U.S. Census; FRED after checking series rights |
| Study attitudes, behavior, and political participation | General Social Survey, American National Election Studies |
| Examine U.S. public expenditure | USAspending; check source definitions and unresolved reuse terms before choosing data |
| Work with computational biology, chemical data, or ML benchmarks | GEO, ChEMBL, BioModels, OpenML |
| Analyze data or optimize allocations, routes, and schedules | R, SciPy, OR-Tools |
| Model queues, agents, dynamic systems, or biochemical networks | SimPy, Mesa, OpenModelica, COPASI; BioModels for existing published models |
| Plan reproducible work and find registered study plans | The Turing Way, OSF Registries |

Start with the research question, population or system, unit of analysis, time period, and intended output. Check a candidate's definitions, provenance, coverage, missingness, revisions, and method documentation before committing to it. Survey microdata may require design weights and restrictions on pooling; aggregate indicators may not support individual-level conclusions. A benchmark or published simulation model still needs a fit assessment for the proposed study.

## Read the access and rights fields together

Free access, an open data licence, a free API allowance, and open-source software describe different permissions. A free API can have limits or require a key. A publicly downloadable survey can carry research-use conditions. A software licence does not grant rights to its example data, external solver, model library, or input datasets. Article discovery metadata does not grant access or reuse rights to the full text.

The catalog records the access model, account or key requirement, and licence or terms summary. It also links to the provider's documentation. Check the specific dataset, article, release, model, or package notices at the time of use. FRED series, GSS data, and repository-hosted files particularly require item-level attention. Do not assume that university access permits redistribution.

For an account, key, unavailable resource, restricted dataset, paid service, or unclear permissions, follow the [administrative resource-request process](../governance/resource-requests.md). Post a public request in [Q&A](https://github.com/Open-Source-Research-Initiative/.github/discussions/new?category=q-a), without credentials or private data. If you cannot use Discussions, use the [issue queue](https://github.com/Open-Source-Research-Initiative/.github/issues). For a private request, contact [Cole](mailto:cole.lyons@pennmedicine.upenn.edu) directly. Agree on delivery and storage before sending restricted material.

## Keep the research record

For each resource used, record its catalog ID, provider, and original source. Record the dataset or model identifier and DOI or accession where available. Record the release or version, retrieval date, query or filters, variables and units, applicable terms, and citation. Retain permitted source snapshots and checksums alongside the retrieval and transformation code. Pin software and model versions. Record solver settings and random seeds where relevant. Retain enough information to explain revisions to the inputs.

In human-driven Agentic-Powered-Research, a person chooses the sources, directs retrieval and analysis, and evaluates the evidence. Record the agent's role and the human review of source selection, transformations, and conclusions. Model execution alone does not establish validity or a publishable finding.

## Maintain this catalog

The CSV uses semicolon-separated values within `areas` and `exchange_formats`. `Cross-field` marks resources usable across disciplines; `Simulation Lab` marks potential use in the proposed lab. These tags are routing aids, not separate research areas or approved projects.

| Field or status | Meaning |
| --- | --- |
| `official_url`, `api_or_docs_url`, `license_or_terms_url` | Provider or maintainer evidence for the entry. A terms link can cover a service generally; item-level terms may still differ. A blank terms URL means an applicable source was not established. |
| `checked_date` | Date of the documentation review, not a promise of continued availability. |
| `docs_reviewed` | Official documentation supports the description. Access and study suitability remain untested. |
| `needs_terms_review` | Access is documented, but reuse rights need clarification for the intended use. |
| `needs_transition_review` | Provider documentation describes a service or endpoint transition, or current access could not be confirmed. |

When adding or updating a row, prefer an official provider or maintainer, describe its intended research role, and distinguish observed access from statements in documentation. Preserve unknowns in `notes`. Do not copy a generic licence onto all content from a repository. Recheck changing access and terms before a project depends on them. Record any actual access probe separately with its date and result.
