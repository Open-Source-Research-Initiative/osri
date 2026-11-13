# OSRI initial research areas and publication plan

These are OSRI's starting areas and publication goals. Specific projects and Simulation Lab capabilities will develop with collaborators. Use the [start guide](../START_HERE.md) to develop a first question.

## Research scope

OSRI includes Healthcare, Engineering, Informatics, Economics, Social and Behavioral Sciences, and Public Policy. These areas provide a common direction while leaving room for related questions and contributions from other disciplines. Projects should connect to one or more of these areas, including through shared simulation work. Each should identify a question or contribution and have a person directing the research.

Agentic-Powered-Research is human-driven: people define the questions, direct the work, and evaluate the evidence and conclusions.

| Starting area | Working scope |
| --- | --- |
| Healthcare | Public health and health systems research: population health, access, equity, policy, service delivery, organizational performance, and use of resources. Evidence synthesis, meta-analysis, and analysis of existing data can support these questions. The initial focus is nonclinical research. |
| Engineering | Systems engineering, engineering management, Operations Research, and Decision Science: system architecture, lifecycle decisions, reliability, risk, project delivery, optimization, scheduling, queues, resource allocation, and decisions under uncertainty. Approaches include evidence synthesis, comparative studies, modeling, and simulation. Physical laboratory experiments are outside the initial program. |
| Informatics | Bioinformatics, public health and health systems informatics, research informatics, information systems, and Computational Natural Sciences. Computational Natural Sciences includes computational biology, chemistry, physics, and materials modeling within OSRI's organizational structure. Work can include existing-data analysis, knowledge representation, interoperability, information retrieval, data pipelines, computational methods, and virtual experiments. Physical laboratory experiments are outside the initial program. |
| Economics | Health and public economics, incentives, resource allocation, and the economics of research and innovation. Possible approaches include existing-data analysis, evidence synthesis, economic modeling, and simulation. |
| Social and Behavioral Sciences | Human judgment, collaboration, organizational behavior, and how people work with Agentic-Powered-Research. Possible approaches include existing-data analysis, evidence synthesis, and models of behavior and coordination. |
| Public Policy | Policy analysis and evaluation, governance, institutions, technology policy, and public programs. Possible approaches include comparative research, evidence synthesis, existing-data analysis, and scenario modeling. |

Systematic and scoping reviews, meta-analysis, existing-data analysis, computational experiments, and modeling are methods that can be used across the areas. Quantitative pooling should follow the suitability of the evidence for the research question.

## Organization-wide meta-research

OSRI's administrators will study and improve the group's research practices, including reproducibility, evidence quality, collaboration, and the use of Agentic-Powered-Research. This organization-wide meta-research is part of administering OSRI across its repositories. The [research practice and meta-research responsibilities](../meta-research/README.md) describe this shared role.

Meta-research spans the research areas and the shared Simulation Lab. Administrators coordinate this work through research records, shared methods, review practices, and publication tracking.

## Proposed OSRI Simulation Lab

A shared computational laboratory for designing and conducting virtual experiments across the research areas. This is a proposed research capability; it is not a claim that a functioning lab or validated models already exist.

Possible work includes:

- Public health and health systems models: population dynamics, service demand, access, queues, staffing, and policy scenarios.
- Engineering, Operations Research, and Decision Science models: system behavior, reliability, resource constraints, queues, schedules, optimization, and design alternatives.
- Informatics and Computational Natural Sciences models: biological pathways, gene regulation, virtual assays, chemical and physical processes, materials behavior, synthetic datasets, information flows, and computational benchmarks.
- Economics, Public Policy, and behavioral models: incentives, resource tradeoffs, distributional effects, public programs, and organizational coordination.

The lab could support experiments normally associated with laboratory research by modeling the relevant processes and testing defined changes computationally. The connection between the model and the system being studied must be established for the claims a study makes. Existing experimental datasets and published benchmarks can support that assessment without OSRI conducting a new physical experiment.

### Publication route

Computational and simulation studies have established publication routes. The Operational Research Society's [Journal of Simulation](https://www.tandfonline.com/journals/tjsm20/about-this-journal) covers simulation methods and applications in domains including healthcare, manufacturing, and services. [PLOS Computational Biology](https://journals.plos.org/ploscompbiol/s/journal-information) covers computational studies of biological systems. Its scope states that experimental validation is not required for every publication. It emphasizes evidence, reproducibility, and significant insight.

For an initial simulation project, a practical approach is to reproduce a published model. Establish what can be reproduced, then use the model to investigate a clearly defined extension. The study should document its question, assumptions, inputs, implementation checks, comparisons, uncertainty, and results. The [STRESS reporting guidelines](https://www.tandfonline.com/doi/abs/10.1080/17477778.2018.1442155) provide reporting checklists for discrete-event simulation, agent-based simulation, and system dynamics.

The contribution could be a new finding, a method, a justified replication, a benchmark, or an openly documented model. Venue requirements differ. For example, [PLOS ONE's publication criteria](https://journals.plos.org/plosone/s/criteria-for-publication) include technical rigor, reproducible descriptions, and conclusions supported by the results. A completed simulation does not by itself establish a publishable contribution or demonstrate that a prediction holds outside the model.

## Publications and research communication

OSRI's goal is to produce and share research through several forms of publication:

- Journal articles.
- Full conference papers.
- Preprints, including arXiv where the subject fits.
- Substantive research blogs and technical essays.

A research blog can present an analysis, evidence synthesis, method, finding, replication, or developed research argument. Announcements, routine progress updates, and reposts do not add to the research-publication total. Research software, models, and datasets can support publications and can also be the subject of methods papers or substantive technical writeups.

OSRI tracks the publication types below. The shared register records output identity and related research work.

### Publication counts

Track the four publication types separately and report their combined total. Also report the number of distinct research works represented by those outputs.

`Total publication outputs = journal articles + full conference papers + preprints + research blogs/essays`

`Distinct research works = distinct work_id values represented by those public outputs`

For example, a preprint, its journal article, and a substantive companion research blog would appear as three publication outputs associated with one research work. Revised preprint versions, edits, mirrors, and cross-posts remain part of the existing output record.

Record peer-review status separately. An accepted paper awaiting public publication belongs in the pipeline count until it is published. Use the first public publication date for each output's annual count, and retain the date when a manuscript becomes accepted or peer reviewed. Report both calendar-year and all-time counts. A work spanning several research areas counts once in the organization total.

The starter register is [publications.csv](../publications/publications.csv). It contains column headers only. It is not a verified inventory or a current publication count. Each output receives a publication ID, while related outputs share a work ID. Suggested publication types are `journal_article`, `conference_paper`, `preprint`, and `research_blog`. Suggested statuses are `planned`, `draft`, `submitted`, `accepted`, and `published`. A public preprint or blog uses `published` with its peer-review status recorded accurately.
