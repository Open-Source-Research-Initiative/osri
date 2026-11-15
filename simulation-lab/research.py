#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate complete paper-to-code coverage and generate readable research routes."""
import argparse
import csv
from collections import Counter
from datetime import date
import io
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
TIERS = {
    'paper_result_candidate': 'Paper result candidate',
    'paper_model_adaptation': 'Paper model adaptation',
    'software_paper_example': 'Software paper example',
    'related_tutorial_only': 'Related tutorial only',
    'unresolved': 'Unresolved',
}
STATES = {
    'not_run': 'Not run',
    'attempted_blocked': 'Attempted; blocked',
    'executed_example': 'Example executed',
    'analysed_saved_output': 'Saved author outputs analysed; simulator not run',
    'reproduced_target': 'Published target compared',
}
GROUPS = {
    'scenes-robotics': 'Scenes and robotics',
    'robotics-fem-cfd': 'Robotics, finite elements, and fluid dynamics',
    'multiphysics': 'Multiphysics and water networks',
    'finance-economics': 'Finance, economics, and policy',
    'agents-operations': 'Agents, operations, and computing',
    'energy-natural-sciences': 'Energy and natural sciences',
}


def validate(data, tools):
    if data['schema_version'] != 1:
        raise ValueError('Unknown research route schema')
    date.fromisoformat(data['checked_date'])
    rows = data['records']
    actual = [r['tool_id'] for r in rows]
    if len(actual) != len(set(actual)) or set(actual) != set(tools):
        raise ValueError(f'Research route coverage differs from tool catalog: missing={set(tools)-set(actual)}, extra={set(actual)-set(tools)}')
    for row in rows:
        key = row['tool_id']
        if row['group'] not in GROUPS:
            raise ValueError(f'Unknown research group: {key}')
        if not row['question'] or not isinstance(row['gaps'], list):
            raise ValueError(f'Missing question or gaps: {key}')
        paper, artifact, construction, execution = (row[k] for k in ('paper', 'artifact', 'construction', 'execution'))
        if construction['reproduction_tier'] not in TIERS or execution['status'] not in STATES:
            raise ValueError(f'Unknown evidence tier or execution status: {key}')
        if not isinstance(paper['metadata_verified'], bool) or not isinstance(artifact['inspected'], bool):
            raise ValueError(f'Invalid verification flags: {key}')
        for field in ('title', 'authors', 'year', 'identifier', 'url', 'metadata_url', 'access', 'locator'):
            if field not in paper:
                raise ValueError(f'Missing paper {field}: {key}')
        for field in ('url', 'relation_to_paper', 'ref', 'commit', 'files', 'license'):
            if field not in artifact:
                raise ValueError(f'Missing artifact {field}: {key}')
        for field in ('environment', 'inputs', 'commands', 'expected_outputs', 'comparison', 'compute', 'data_access', 'blockers', 'next_action'):
            if field not in construction:
                raise ValueError(f'Missing construction {field}: {key}')
        if not isinstance(construction['commands'], list):
            raise ValueError(f'Commands must be an array: {key}')
        if execution['status'] != 'not_run' and not execution['evidence']:
            raise ValueError(f'Execution claim needs evidence: {key}')
        if execution['status'] == 'reproduced_target':
            if not paper['metadata_verified'] or not artifact['inspected'] or not construction['comparison'] or not execution.get('target_comparison'):
                raise ValueError(f'Published-target claim needs verified inputs and comparison: {key}')
        if not row['evidence'] or row['confidence'] not in {'high', 'medium', 'low'}:
            raise ValueError(f'Missing source assessment: {key}')
        urls = [paper['url'], paper['metadata_url'], artifact['url']]
        for source in row['evidence']:
            date.fromisoformat(source['inspected_on'])
            if not source['supports']:
                raise ValueError(f'Empty source assessment: {key}')
            urls.append(source['url'])
        for value in urls:
            if value and (urlsplit(value).scheme != 'https' or not urlsplit(value).netloc):
                raise ValueError(f'Expected HTTPS source: {key}: {value}')


def prose(value):
    if isinstance(value, list):
        return '; '.join(prose(v) for v in value) or 'None recorded.'
    if isinstance(value, dict):
        return '; '.join(f'{k}: {prose(v)}' for k, v in value.items())
    return str(value) if value not in (None, '') else 'Not established.'


def cell(value):
    return prose(value).replace('|', '\\|').replace('\n', ' ')


def group_page(name, rows):
    lines = [f'# {GROUPS[name]}: paper-to-code routes', '',
             '[All 60 tools](README.md) · [How to contribute](../contributing.md)', '',
             'These are construction routes researched by agents. The execution line reports the bounded work actually performed; the comparison section defines what remains before claiming a published result. Human scientific review is pending.', '']
    for row in rows:
        paper, artifact, plan, run = (row[k] for k in ('paper', 'artifact', 'construction', 'execution'))
        lines += [f"## {row['tool_id']}", '', f"**{row['name']}** — {row['question']}", '',
                  f"**Route:** {TIERS[plan['reproduction_tier']]}. **Execution:** {STATES[run['status']]}. **Source confidence:** {row['confidence']}.", '',
                  f"### Paper for {row['tool_id']}", '',
                  f"{prose(paper['authors'])} ({paper['year']}). [{paper['title']}]({paper['url']}). {paper['identifier']}.", '',
                  f"**Publication type:** {prose(paper.get('publication_type', 'See primary metadata record; not classified here.'))}. [Primary metadata]({paper['metadata_url']}). Metadata verification: {'confirmed' if paper['metadata_verified'] else 'incomplete; follow up before using this citation'}. Full-text access: {prose(paper['access'])}", '',
                  f"**Target in the paper:** {prose(paper['locator'])}", '',
                  f"### Code and inputs for {row['tool_id']}", '',
                  f"[Artifact or upstream source]({artifact['url']}). {prose(artifact['relation_to_paper'])}", '',
                  f"**Source inspected:** {'yes' if artifact['inspected'] else 'no'}. **Ref:** {prose(artifact['ref'])}. **Commit:** {prose(artifact['commit'])}.", '',
                  f"**Files:** {prose(artifact['files'])}", '', f"**Terms:** {prose(artifact['license'])}", '',
                  f"**Environment and compute:** {prose(plan['environment'])} {prose(plan['compute'])}", '',
                  f"**Inputs:** {prose(plan['inputs'])}", '', f"**Data access:** {prose(plan['data_access'])}", '',
                  f"### Construct and compare {row['tool_id']}", '',
                  'The sequence below contains upstream commands and proposed setup instructions, as labeled. Only commands identified in the execution evidence were run here; inspect the pinned source and prerequisites before running.', '',
                  *[f"{i}. `` {prose(command)} ``" for i, command in enumerate(plan['commands'], 1)], '',
                  f"**Expected outputs:** {prose(plan['expected_outputs'])}", '',
                  f"**Comparison with the paper:** {prose(plan['comparison'])}", '',
                  f"**Execution result:** {prose(run['result'])}", '',
                  f"**Execution evidence:** {prose(run['evidence'])}", '',
                  f"**Blockers:** {prose(plan['blockers'])}", '', f"**Next action:** {prose(plan['next_action'])}", '',
                  f"**Gaps:** {prose(row['gaps'])}", '',
                  f"### Sources for {row['tool_id']}", '']
        lines += [f"- [{e['supports']}]({e['url']}) (inspected {e['inspected_on']})." for e in row['evidence']]
        lines.append('')
    return '\n'.join(lines)


def outputs(data, tools):
    rows = data['records']
    states = Counter(r['execution']['status'] for r in rows)
    tiers = Counter(r['construction']['reproduction_tier'] for r in rows)
    lines = ['# Research routes for all 60 Simulation Lab tools', '',
             'Choose a tool, inspect the linked paper and code, and identify the result to compare before launching a run. These routes extend the [existing teaching examples](../examples/README.md).', '',
             f"Researched {data['checked_date']} at Cole / @ajhcs's request by six domain agents, with integration and source review by Codex. Human scientific review is pending. Each record distinguishes paper-associated code, a model adaptation, a software-paper demonstration, and a related tutorial. A route covering a tool does not mean its paper has been reproduced.", '',
             '## Current evidence', '', '[Technical review and checks](verification/review.json). The reviewers were agents; human scientific review remains pending.', '',
             '| Execution status | Tools |', '| --- | ---: |']
    lines += [f'| {label} | {states[key]} |' for key, label in STATES.items()]
    lines += ['', '| Relationship to the paper | Tools |', '| --- | ---: |']
    lines += [f'| {label} | {tiers[key]} |' for key, label in TIERS.items()]
    lines += ['', 'Counts apply to these new research routes. The four original executed teaching examples retain their separate run records.', '',
              '## Build an example', '',
              '1. Select a named figure, table, equation, or benchmark and record its inputs and observable. Prefer the paper\'s archived code over a moving default branch.',
              '2. Pin source commits, environment, datasets, random seeds, and data or asset terms. If an exact environment is unavailable, document the adaptation before interpreting its output.',
              '3. Run in an isolated environment and keep the original outputs, logs, failures, package versions, and hashes. A smoke test establishes only that the selected path runs.',
              '4. Compare the stated observable using a justified tolerance or uncertainty interval. Record deviations and obtain human scientific review before calling it a reproduced research result.', '',
              'The per-tool next action identifies the remaining work. Restricted papers may be supplied through the [resource-request route](../../governance/resource-requests.md); library PDFs stay outside the public repository. Larger studies belong in their own research repositories.', '',
              '## Choose a route', '',
              '[Download the route inventory](routes.csv) · [Structured source records](routes.json)', '',
              '| Tool | Research route | Execution |', '| --- | --- | --- |']
    for row in rows:
        lines.append(f"| [{cell(row['name'])}]({row['group']}.md#{row['tool_id']}) | {TIERS[row['construction']['reproduction_tier']]} | {STATES[row['execution']['status']]} |")
    lines += ['', '## Refresh and check', '',
              'Edit `routes.json`, then run `python3 simulation-lab/research.py --write` and `python3 simulation-lab/catalog.py --write`. Validation enforces complete tool coverage and generated-file consistency; it does not verify scientific claims or contact upstream sources.', '']
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(['tool_id', 'name', 'route', 'paper_title', 'paper_identifier', 'paper_url', 'metadata_verified', 'artifact_url', 'artifact_commit', 'reproduction_tier', 'execution_status', 'confidence', 'next_action'])
    for row in rows:
        writer.writerow([row['tool_id'], row['name'], f"{row['group']}.md#{row['tool_id']}", row['paper']['title'], row['paper']['identifier'], row['paper']['url'], row['paper']['metadata_verified'], row['artifact']['url'], row['artifact']['commit'], row['construction']['reproduction_tier'], row['execution']['status'], row['confidence'], prose(row['construction']['next_action'])])
    result = {'README.md': '\n'.join(lines), 'routes.csv': stream.getvalue()}
    for group in GROUPS:
        result[group + '.md'] = group_page(group, [r for r in rows if r['group'] == group])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    data = json.loads((ROOT / 'research/routes.json').read_text())
    with (ROOT / 'tools.csv').open(newline='') as stream:
        tools = {r['tool_id']: r for r in csv.DictReader(stream)}
    validate(data, tools)
    for name, content in outputs(data, tools).items():
        path = ROOT / 'research' / name
        if args.write:
            path.write_text(content, encoding='utf-8')
        elif not path.is_file() or path.read_text(encoding='utf-8') != content:
            raise SystemExit(f'Generated research route differs: {name}; run research.py --write')
    print(f'Validated research routes for all {len(tools)} tools')


if __name__ == '__main__':
    main()
