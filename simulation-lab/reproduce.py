#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate evidence from the 21-candidate campaign and generate its Lab guides."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
DIRECTORY = ROOT / 'reproductions'
EXPECTED_TOOLS = frozenset(('blender', 'gz-sim', 'bullet3', 'carla', 'precice', 'dolfinx', 'dealii', 'ngspice', 'dualsphysics', 'engine', 'hark', 'tax-calculator', 'simmer', 'pandapower', 'calliope', 'sumo', 'tellurium', 'brian2', 'ns-3-dev-git', 'simgrid', 'dynare'))
STATUS = {
    'target_compared': 'Published target compared',
    'author_code_executed': 'Author code executed',
    'adapted_run': 'Adapted run executed',
    'analysed_saved_output': 'Saved outputs analysed; simulation not rerun',
    'attempted_blocked': 'Attempted; blocked',
}


def text(value):
    if value is None or value == '':
        return 'Not established.'
    if isinstance(value, list):
        return '; '.join(text(item) for item in value) or 'None recorded.'
    if isinstance(value, dict):
        return '; '.join(f'{key}: {text(item)}' for key, item in value.items())
    return str(value)


def validate(data, tools, directory=DIRECTORY):
    if data['schema_version'] != 1:
        raise ValueError('Unknown reproduction evidence schema')
    selected = data['selected_tool_ids']
    if set(selected) != EXPECTED_TOOLS:
        raise ValueError('Campaign selection differs from the 21 reviewed candidates')
    ids = [row['tool_id'] for row in data['records']]
    if len(ids) != len(set(ids)) or set(ids) != set(selected) or len(selected) != len(set(selected)):
        raise ValueError('Campaign coverage must match the selected tools exactly')
    if set(ids) - set(tools):
        raise ValueError('Campaign contains unknown tools')
    for row in data['records']:
        key = row['tool_id']
        for field in ('title', 'question', 'paper', 'source', 'inputs', 'environment', 'commands', 'target', 'execution', 'comparison', 'outputs', 'blockers', 'next_action', 'relationship_to_paper'):
            if field not in row:
                raise ValueError(f'Missing {field}: {key}')
        if row.get('guide_source'):
            template = (directory / row['guide_source']).resolve()
            if not template.is_relative_to(directory.resolve()) or not template.is_file():
                raise ValueError(f'Guide source outside campaign or missing: {key}')
        status = row['execution']['status']
        if status not in STATUS or row['human_scientific_review'] != 'pending':
            raise ValueError(f'Unknown status or unsupported human review claim: {key}')
        for url in (row['paper']['url'], row['source']['url']):
            if urlsplit(url).scheme != 'https' or not urlsplit(url).netloc:
                raise ValueError(f'Expected HTTPS primary source: {key}')
        comparison = row['comparison']
        if not isinstance(comparison['performed'], bool) or (comparison['passed'] is not None and not isinstance(comparison['passed'], bool)):
            raise ValueError(f'Invalid comparison assessment: {key}')
        if comparison['passed'] is not None and not comparison['performed']:
            raise ValueError(f'Unperformed comparison cannot have a pass/fail outcome: {key}')
        if status == 'target_compared':
            if row['target']['declared_before_run'] is not True or not comparison['performed'] or not comparison['measurements'] or not row['target']['reference'] or row['target']['tolerance'] in ('', None):
                raise ValueError(f'Published-target comparison lacks a declared target and measured evidence: {key}')
        if status in {'target_compared', 'author_code_executed', 'adapted_run'}:
            if row['execution'].get('converged') is False:
                raise ValueError(f'Unconverged principal solve cannot be a successful example: {key}')
            if row['execution']['exit_code'] != 0 or not row['outputs']:
                raise ValueError(f'Executed example lacks successful run or retained output: {key}')
        if not row.get('evidence_files'):
            raise ValueError(f'Missing execution evidence: {key}')
        for output in row['outputs']:
            if not re.fullmatch(r'[a-f0-9]{64}', output['sha256']):
                raise ValueError(f'Invalid output digest: {key}')
            if not output.get('published', False):
                continue
            path = (directory / output['path']).resolve()
            if not path.is_relative_to(directory.resolve()) or not path.is_file():
                raise ValueError(f'Public output missing or outside campaign: {key}')
            if hashlib.sha256(path.read_bytes()).hexdigest() != output['sha256'] or path.stat().st_size != output['bytes']:
                raise ValueError(f'Public output changed: {key}: {path.name}')


def guide(row):
    key, paper, source = row['tool_id'], row['paper'], row['source']
    run, target, comparison = row['execution'], row['target'], row['comparison']
    if row.get('guide_source'):
        template = (DIRECTORY / row['guide_source']).read_text(encoding='utf-8')
        lines = [template.rstrip(), '', '## Download the recorded files', '']
        for output in row['outputs']:
            if output.get('published', False):
                lines.append(f"- [{Path(output['path']).name}]({output['path']}) — {output['role']}.")
        lines += ['', f"[Complete run record](records/{key}.json) · [All candidate attempts](README.md). Human scientific review is pending.", '']
        return '\n'.join(lines)
    lines = [f"# {row['title']}", '', '[All candidate attempts](README.md) · [Simulation Lab](../README.md)', '',
             row['question'], '',
             f"**Execution:** {STATUS[run['status']]}. **Paper comparison:** {'passed' if comparison['passed'] is True else 'did not pass' if comparison['passed'] is False else 'not established'}. Human scientific review is pending.", '',
             '## Paper and author code', '', f"[{paper['title']}]({paper['url']}) ({paper['identifier']}). Publication type: {text(paper['publication_type'])}.", '',
             f"**Paper location:** {text(paper['locator'])}", '',
             f"[Source]({source['url']}); ref: {text(source['ref'])}; commit: {text(source['commit'])}.", '',
             f"**Source files:** {text(source['paths'])}", '', f"**Terms:** {text(source['license'])}", '',
             f"**Relationship to the paper:** {text(row['relationship_to_paper'])}", '',
             '## Inputs and environment', '', text(row['inputs']), '', text(row['environment']), '',
             '## Repeat the run', '',
             'These steps describe the recorded run. Environment reconstruction and any changes to author code are identified above. Downloadable drivers retain the original source references and input hashes.', '']
    lines += [f'{i}. `` {text(command)} ``' for i, command in enumerate(row['commands'], 1)]
    lines += ['', '## Comparison', '',
              f"**Observable:** {text(target['observable'])}", '', f"**Reference:** {text(target['reference'])}", '',
              f"**Rule and basis:** {text(target['tolerance'])}. {text(target['tolerance_basis'])}", '',
              f"**Defined before this run:** {text(target['declared_before_run'])}. **Comparison scope:** {text(target['scope'])}", '',
              'Measured results:', '', '```json', json.dumps(comparison['measurements'], indent=2, ensure_ascii=False), '```', '',
              text(comparison['interpretation']), '', f"**Run result:** {text(run['result'])}", '',
              '## Outputs and evidence', '']
    for output in row['outputs']:
        label = Path(output['path']).name
        if output.get('published', False):
            lines.append(f"- [{label}]({output['path']}) — {output['role']}; SHA256 `{output['sha256']}`.")
        else:
            lines.append(f"- `{label}` — {output['role']}; native file retained with SHA256 `{output['sha256']}`; not repackaged here.")
    lines += ['', f"[Complete run record](records/{key}.json). Native outputs, command logs and failed attempts are retained in the development evidence directory identified by that record.", '',
              '## Limits and next step', '', f"**Blockers:** {text(row['blockers'])}", '', f"**Next action:** {text(row['next_action'])}", '']
    return '\n'.join(lines)


def outputs(data):
    rows = data['records']
    counts = Counter(row['execution']['status'] for row in rows)
    lines = ['# Reproducing 21 paper-linked candidates', '',
             'Author code, accessible inputs, measured outputs, and comparisons from the candidate reproduction campaign. Cole / @ajhcs directed the work; domain agents performed the runs and other agents reviewed the evidence. Human scientific review remains pending.', '',
             'A completed code run and a match to a published target are reported separately. Some paper-linked artifacts differ from the article or no longer supply the required runtime, trained model, data, or reference output. These differences and failed attempts remain part of the record.', '',
             '| Recorded outcome | Tools |', '| --- | ---: |']
    lines += [f'| {label} | {counts[key]} |' for key, label in STATUS.items()]
    lines += ['', 'Pass/fail in the table applies only to the comparison defined in its guide, including exploratory or archived-output checks. A passing selected paper target additionally needs the corresponding execution classification.', '', 'The preCICE and deal.II candidates share one coupled experiment. Counts describe tools; they do not imply independent experiments or reproduction of every result in a paper.', '',
              '| Candidate | Execution | Recorded comparison (scope in guide) |', '| --- | --- | --- |']
    for row in rows:
        passed = row['comparison']['passed']
        result = 'Passed within stated rule' if passed is True else 'Did not pass' if passed is False else 'Not established'
        lines.append(f"| [{row['title'].replace('|', '/')} ]({row['tool_id']}.md) | {STATUS[row['execution']['status']]} | {result} |")
    lines += ['', 'The [structured campaign record](campaign.json) preserves all candidate outcomes. Each guide links numeric outputs and a compact run record; full environments, sources, native results and failed attempts remain in the development evidence directory. Follow the [contribution guide](../contributing.md) when extending a result.', '']
    result = {'README.md': '\n'.join(lines)}
    result.update({row['tool_id'] + '.md': guide(row) for row in rows})
    return result


def main():
    import csv
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    data = json.loads((DIRECTORY / 'campaign.json').read_text())
    with (ROOT / 'tools.csv').open(newline='') as stream:
        tools = {r['tool_id'] for r in csv.DictReader(stream)}
    validate(data, tools)
    for name, content in outputs(data).items():
        path = DIRECTORY / name
        if args.write:
            path.write_text(content, encoding='utf-8')
        elif not path.exists() or path.read_text(encoding='utf-8') != content:
            raise SystemExit(f'Generated reproduction guide differs: {name}; run reproduce.py --write')
    print(f"Validated {len(data['records'])} candidate reproduction records")


if __name__ == '__main__':
    main()
