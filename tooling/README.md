# Research tools and agent use

Optional reference. Assessed 13 November 2026.

OSRI's Agentic-Powered-Research is directed by people. A person chooses the question, judges the methods and evidence, and authorizes conclusions and publication. Contributors may use different agents, scientific software, or manual methods. Common records and review criteria make their work comparable. They do not guarantee identical findings.

The [contribution standards](../governance/contribution-standards.md) govern acceptance. This guide adds a small tool protocol. It supports source notes, protocols, evidence reviews, analyses, models, datasets, software, reports, preprints, journal articles, and public explanations.

## Three different capabilities

| Capability | What it provides | What to check |
| --- | --- | --- |
| Agent skill | Written task instructions, sometimes with scripts and templates | Method fit, instructions, dependencies, and the actual output |
| Plugin or connector | A package of capabilities or access to an external service | Available operations, account access, cost, and data sent to the service |
| Scientific software | A computation, model, analysis, or document engine | Version, inputs, assumptions, numerical behavior, and applicable evidence |

The open [Agent Skills format](https://agentskills.io/what-are-skills) packages instructions and optional resources in a folder. Format compatibility does not establish that a workflow works on every host. A plugin can contain skills, connectors, or both. None of these supplies scientific approval.

## Common task protocol

Keep the record with the issue or research files. A short contribution needs a short record. An analysis needs enough detail to reproduce it. The [workflow profiles](workflows.md) describe task-specific inputs, outputs, and checks. The [research task record](../templates/research-task.md) can help document substantive work.

| Stage | Required record or output |
| --- | --- |
| Select the task | Question, human lead, scope, intended output, and checks needed for acceptance. Follow the [topic-selection guide](../topics/README.md) for a new research question. |
| Select the method and tool | Why the method fits; tool and skill source; exact version or commit; local patches; relevant configuration. Record the agent and model identifier when exposed, plus the date when a provider uses a changing alias. |
| Establish inputs and limits | Source or dataset versions, identifiers, access and reuse terms; authorized files, services, compute, and spending. Describe what information will leave the local environment. Keep restricted inputs in their approved location. |
| Do the work | Preserve queries, search dates, transformations, code, parameters, seeds where relevant, and material deviations from the plan. Retain failed checks and unresolved inputs. |
| Check the result | Verify identifiers against real records; read the passages supporting claims. Check calculations and artifacts against the specified method and inputs. Report what ran, what passed or failed, and what was not checked. |
| Review and accept | A named person reviews the claims, evidence, limitations, and contribution credit. Obtain the domain or methods review the work needs. Record self-review accurately. Another agent's review is additional assistance. |
| Share and preserve | Retain editable sources, reusable outputs, an environment record, and a manifest for large or restricted artifacts. Follow the project's human authorization for acceptance and publication. |

Use Markdown or plain text for plans and notes. Use CSV/TSV with a data dictionary for tables, and JSON/YAML for structured records. Use BibTeX, RIS, or CSL JSON for references. Use source code and environment lock files for computations. Use editable model or diagram sources for figures. Use domain formats when they preserve meaning better. Supply readable exports alongside them. A PDF, screenshot, proprietary project file, or agent chat alone is insufficient when the underlying work needs inspection or reuse.

Contributors using different tools submit the same task outputs and undergo the same review. A spreadsheet or written source check can meet the same requirements. Maintainers can turn an issue or attachment into repository files and provide approved execution for contributors who cannot run software. No paid agent, connector, or API account is required to contribute.

## Candidate skills

[MedSci Skills v6.3.0](https://github.com/Aperivue/medsci-skills/tree/e0ea3b0be3bf529aa0b94ee5fd8450e78848932c) is a useful source of research workflows, with a strong medical focus. Inspect and select individual skills rather than adopting the full pipeline as OSRI policy.

| MedSci skills inspected | Potential use | OSRI limit |
| --- | --- | --- |
| [`orchestrate`](https://github.com/Aperivue/medsci-skills/blob/v6.3.0/skills/orchestrate/SKILL.md) | Route a bounded request to a suitable workflow | The project determines stages, permissions, and review. |
| [`search-lit`](https://github.com/Aperivue/medsci-skills/blob/v6.3.0/skills/search-lit/SKILL.md), [`verify-refs`](https://github.com/Aperivue/medsci-skills/blob/v6.3.0/skills/verify-refs/SKILL.md) | Search records, preserve references, detect identifier or metadata mismatches | PubMed coverage is discipline-specific. A metadata match does not establish that a source supports a claim. |
| [`ma-scout`](https://github.com/Aperivue/medsci-skills/blob/v6.3.0/skills/ma-scout/SKILL.md), [`find-cohort-gap`](https://github.com/Aperivue/medsci-skills/blob/v6.3.0/skills/find-cohort-gap/SKILL.md) | Suggest review or cohort questions and investigate feasibility | Clinical cohorts, investigator profiles, heuristic rankings, and publication-tier predictions are unsuitable as general selection rules. A human assesses candidates using the topic-selection guide. |
| [`define-variables`](https://github.com/Aperivue/medsci-skills/blob/v6.3.0/skills/define-variables/SKILL.md), [`design-study`](https://github.com/Aperivue/medsci-skills/blob/v6.3.0/skills/design-study/SKILL.md) | Link measures to source definitions; expose study-design risks | Clinical cutoffs and radiology or medical AI design assumptions need domain-specific review. |
| [`meta-analysis`](https://github.com/Aperivue/medsci-skills/blob/v6.3.0/skills/meta-analysis/SKILL.md), [`check-reporting`](https://github.com/Aperivue/medsci-skills/blob/v6.3.0/skills/check-reporting/SKILL.md) | Prepare review records, reconcile counts, and audit reporting | Select the review method, registry, assessors, and current official reporting instrument for the actual study. Reporting completeness does not establish validity. |

MedSci's project code is MIT licensed. Bundled checklists and citation styles have [separate terms](https://github.com/Aperivue/medsci-skills/blob/v6.3.0/THIRD-PARTY-NOTICES.md); some checklist files are summaries rather than official forms. Preserve those distinctions when reusing material.

Two further candidates cover other needs. [Computable Systems Engineering](https://github.com/ajhcs/computable-systems-engineering) provides model and evidence planning, with bounded queue and fault-model checks. Its alpha status and [execution limits](https://github.com/ajhcs/computable-systems-engineering/blob/2b0ba0a8e3db1d8d7918bd77b03cbaaf46185d5e/docs/technical-guide.md) must stay visible. K-Dense's [hypothesis-generation](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/hypothesis-generation/SKILL.md) and [literature-review](https://github.com/K-Dense-AI/scientific-agent-skills/blob/2d2065fb4520fa3f3f2bcf61cff26ec8b7eba4b5/skills/literature-review/SKILL.md) skills offer broader research guidance. Treat them as candidates that need project-specific review. Their presence does not establish that they are validated research methods.

## Starter catalog and assessment limits

[Browse the tool catalog](https://open-source-research-initiative.github.io/tools/) or [download CSV](research-tools.csv). Its 11 entries record roles, official sources, license or service terms, access costs, dependencies, open outputs, and assessment status. Start with tools the task needs. Possible tools include bibliographic records and source checks, reproducible scripts for computation, and editable writing. A reference manager can help. Skills and commercial connectors are optional.

Selected installed instructions and upstream documentation were inspected. Some workflows use host-specific paths, launchers, services, or native dependencies. Review the selected workflow before using it on another system. The catalog records source versions and assessment limits.

Plugin-directory search found Scite as an optional connector; it was not installed or tested. Its [MCP documentation](https://scite.ai/mcp) requires a paid plan or trial; account access and connector behavior were not tested. The catalog includes public bibliographic services as alternatives for source discovery and metadata checks, with separate source reading still required.

This assessment read local instructions, manifests, receipts, and current primary documentation. It did not install tools, change permissions, execute scientific workflows, analyze datasets, or test service integrations. Earlier runtime receipts are provenance, not checks repeated here. Before adopting a tool for a project, run a small trial on public or synthetic inputs. Retain the outputs and independent checks. Document the supported use and remaining limits.
