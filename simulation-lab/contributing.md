# Add a tool or literature example

A useful contribution can be small: identify a published model, locate its code, improve a setup step, or report a failed run. A browser is enough to propose a source. Follow the [shared standards](../governance/contribution-standards.md).

## Catalog records

The editable sources are [tools.csv](tools.csv), [papers.csv](papers.csv), and [examples.csv](examples.csv). IDs are stable lowercase names separated by hyphens; lists of IDs use semicolons. Keep a tool's example IDs consistent with the example's tool IDs.

For a tool, record its purpose, official source and documentation, source-code license, separate runtime/data/asset terms, source availability, and the date actually checked. Do not equate a free download with open source or describe repository availability as maintenance or execution evidence. Include scene tools and optimization frameworks when useful, while identifying their role accurately.

For a reference, verify title, authors, year, publication type, and DOI against a primary record. Record full-text access and the passages actually inspected separately from metadata verification. A software paper can support the tool's description; an application walkthrough needs an identifiable model, method, equation, listing, benchmark, or experiment.

For an example, add a guide that gives the research question, exact paper connection, code/archive version, environment, input terms, commands or concrete execution route, expected output files, and comparison measures. Explain differences from the paper. Use one status:

| Status in CSV | Required evidence |
| --- | --- |
| `executed_adaptation` | Included teaching code ran; retain parameters, environment, outputs, and actual checks. This does not assert paper reproduction. |
| `upstream_instructions_checked` | Source files and upstream run instructions inspected; execution still pending. |
| `access_pending` | Citation or article located, but a needed artifact cannot yet be inspected. State exactly what is missing. |

Use the [run-record template](run-record-template.md) for a new run. A claim that a published result was reproduced also needs a specified target, matched methods and inputs, an explicit comparison and tolerance, and human scientific review. Keep substantive new studies in their own research repositories.

## Research routes for the complete catalog

The [paper-to-code route inventory](research/README.md) records construction plans separately from the accepted teaching-example catalog. Edit `research/routes.json` and preserve the primary metadata record, the paper location, code-to-paper relationship, immutable version where available, input access, construction commands, comparison target, execution evidence, and unresolved gaps.

A paper result candidate identifies what to reproduce; a software-paper example or related tutorial has a narrower relationship to the research. Do not upgrade an execution status without a run record. A published-target comparison needs matched inputs and methods, an explicit observable and tolerance, and retained numerical evidence. Human scientific review remains separate.

Run `python3 simulation-lab/research.py --write` before regenerating the main catalog. This validates one route per catalog tool and generates the six domain guides and downloadable route inventory. New substantive research belongs in a study repository; this inventory is shared learning and reproduction planning.

## Author-code attempts and numerical comparisons

The [candidate campaign](reproductions/README.md) has one record for each of the 21 selected tools. Keep original failures, publication/document versions, matched input settings, native outputs and hashes, and any changes to code or environment. An author-code run, a maintained third-party replication, an adaptation, an archive analysis, and a passing selected paper comparison have different evidence requirements.

Declare the observable and comparison rule before producing the numerical result. Revised extraction or post-hoc comparison remains exploratory even if a deterministic rerun follows it. Paper targets need source locations and justified precision or uncertainty; a current fixture or archived-output match must retain that narrower scope. Check solver convergence and feasibility separately from process exit status. Record human scientific review as pending until actually performed.

Edit `reproductions/campaign.json` and its original guide templates, then regenerate with `python3 simulation-lab/reproduce.py --write`. Share only explicitly reusable outputs and preserve per-file asset, model and runtime terms. New successful examples use `executed_author_code` or, for a passing selected target with its evidence, `published_target_compared`. Saved-output analyses use `analysed_saved_output`. These statuses never assert whole-paper reproduction or human acceptance.

## Regenerate and check

From the hub root, using Python 3.10 or newer:

```sh
python3 simulation-lab/reproduce.py --write
python3 simulation-lab/research.py --write
python3 simulation-lab/catalog.py --write
python3 simulation-lab/catalog.py
```

This checks identifiers, references, dates, source-link formats, local guide files, and generated-file freshness. It does not contact external sites or verify scientific claims. Follow the [site build instructions](../site/README.md) to check rendered links and layout when changing pages.

Submit a pull request with the sources you checked, commands you ran, outcomes, remaining limitations, material agent assistance, and the responsible human. Do not upload library PDFs unless their redistribution terms permit it. A DOI and a precise passage location are enough to cite a restricted article; use the [resource-request route](../governance/resource-requests.md) when access is needed.
