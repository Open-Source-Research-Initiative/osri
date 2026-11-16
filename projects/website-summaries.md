# Website project summaries

The [project register](projects.csv) remains the authority for project IDs, repositories and human leads. The website adds an overview only for a registered ID with a record in [summaries.json](summaries.json).

Check the current public project README, method, checkpoint and task before editing an overview. Keep source links and check dates. Do not convert a provisional assessment, paused task or proposed output into a research result. Proposed output plans on the website require the human lead’s review.

Store candidate or selected venues in the separate [publication-target collection](../publications/targets.json); record public outputs in the existing publication CSV only when their normal requirements are met. Follow the [site maintenance guide](../site/README.md) to build and check updates.

Public progress uses four broad `stage` values: `planning`, `research`, `writing_review`, and `publication`. `activity` is separately `active`, `on_hold`, or `complete`. The `status_decision` records the registered human lead in `by`, a dated `on`, and a short `note`; `on_hold` additionally requires `hold_reason`. A stage may repeat or move backward. Publication is a work stage, not evidence of submission, acceptance or a published output.

Change activity only on an explicit whole-project decision by the human lead. Inactivity, failed runs, a paused batch, pending review and source-access failures never automatically pause a project. Current labels and contribution text are generated from this record on all site surfaces. Keep detailed execution state in the dated `status_detail` checkpoint, separate from the public badge. `verified_on` dates the underlying source check; it is separate from the human status-decision date. Do not add free-form `status` or `status_note` fields.
