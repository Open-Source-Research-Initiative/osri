# Contributor activity

The [activity board](ACTIVITY.md) shows accepted contributions and recorded research outputs. It credits questions, evidence, data and methods, analysis, review, writing, translation, and community work.

## Count work consistently

- Record one task per row in [contributions.csv](contributions.csv), with a stable ID and an evidence link.
- Count a task after a human maintainer accepts it. Record the acceptance date and maintainer.
- Update the same record for corrections and revisions. Commits and messages do not create extra tasks.
- A shared task counts once in the organization total and once for each credited person.
- The board ranks people by accepted-task count; ties share a place. Work types remain visible. This count does not determine research quality or authorship.

Publication outputs and distinct research works are counted separately using the [publication rules](../publications/README.md). The board covers recorded work only. Earlier activity is not automatically added.

## Add a contribution

Ask a maintainer to record the accepted task, its evidence, and your chosen public credit name. You do not need to edit CSV or use an agent.

Maintainers use these fields:

- `contribution_id`: unique task ID; `contributors`: consistent credit names or handles, separated by semicolons.
- `project_id`: a registered project ID, or blank for shared OSRI work.
- `kind`: `question`, `evidence`, `data_method`, `analysis`, `review`, `writing`, `translation`, or `community`.
- `summary` and `evidence_url`: the task and its public supporting record.
- `status`: `pending`, `accepted`, or `withdrawn`; `accepted_on`: `YYYY-MM-DD`; `accepted_by`: the human maintainer.

Keep material agent assistance in the linked work record. For restricted research, use an approved public summary.

Rebuild the board after changing its source registers:

```sh
python3 community/update.py
python3 community/update.py --check
```

Python's standard library is sufficient. Repository history retains earlier snapshots.
