# SPDX-License-Identifier: MIT
"""Validate editorial summaries and venue plans independently of publication counts."""
import csv
from datetime import date
import json
import re
from urllib.parse import urlsplit

STAGES = {'planning': 'Planning', 'research': 'Research', 'writing_review': 'Writing & review', 'publication': 'Publication'}
ACTIVITIES = {'active': 'Active', 'on_hold': 'On hold', 'complete': 'Complete'}


def project_status(summary):
    return ACTIVITIES[summary['activity']] + ' · ' + STAGES[summary['stage']]


def public_url(value):
    parsed = urlsplit(value)
    if parsed.scheme != 'https' or not parsed.netloc:
        raise ValueError('Expected an attributed HTTPS source: ' + value)


def checked_date(value):
    if date.fromisoformat(value).isoformat() != value:
        raise ValueError('Expected YYYY-MM-DD verification date')


def project_data(root):
    with (root / 'projects/projects.csv').open(newline='', encoding='utf-8') as stream:
        projects = list(csv.DictReader(stream))
    ids = [row['project_id'] for row in projects]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r'OSRI-\d{4,}', key) for key in ids):
        raise ValueError('Missing, duplicate, or unsafe project ID')
    summaries = json.loads((root / 'projects/summaries.json').read_text())
    targets = json.loads((root / 'publications/targets.json').read_text())
    seen = set()
    for summary in summaries:
        key = summary['project_id']
        if key not in ids or key in seen:
            raise ValueError('Unknown or duplicate summary project: ' + key)
        seen.add(key)
        for field in ['question', 'summary', 'status_detail', 'methods', 'contribution', 'outputs', 'sources']:
            if not summary.get(field):
                raise ValueError(key + ': missing ' + field)
        if summary.get('stage') not in STAGES or summary.get('activity') not in ACTIVITIES:
            raise ValueError(key + ': invalid project stage or activity')
        if 'status' in summary or 'status_note' in summary:
            raise ValueError(key + ': public status must use stage and activity')
        decision = summary.get('status_decision', {})
        lead = next(p['human_lead'] for p in projects if p['project_id'] == key)
        if decision.get('by') != lead or not decision.get('note'):
            raise ValueError(key + ': status decision needs the registered human lead and a note')
        checked_date(decision.get('on', ''))
        if summary['activity'] == 'on_hold' and not summary.get('hold_reason', '').strip():
            raise ValueError(key + ': whole-project hold needs a reason')
        if not summary.get('materials'):
            raise ValueError(key + ': missing materials')
        public_url(summary['contribution']['url'])
        for material in summary['materials']:
            public_url(material['url'])
        checked_date(summary['verified_on'])
        for source in summary['sources']:
            public_url(source['url'])
            checked_date(source['checked_on'])
    seen_targets = set()
    for target in targets:
        if target['project_id'] not in seen:
            raise ValueError('Target must reference a project summary')
        if target['target_id'] in seen_targets:
            raise ValueError('Duplicate publication target')
        seen_targets.add(target['target_id'])
        if target['status'] not in {'candidate', 'selected'}:
            raise ValueError('Target status must be candidate or selected')
        if target['status'] == 'selected' and not all(target.get(key) for key in ['selected_by', 'selected_on', 'selection_reference']):
            raise ValueError('Selected target needs a human decision record')
        if target['status'] == 'selected':
            checked_date(target['selected_on'])
            public_url(target['selection_reference'])
        for field in ['venue', 'audience', 'scope', 'article_types', 'methods', 'overlap', 'cost', 'ai_disclosure', 'rationale', 'recommendation', 'sources']:
            if not target.get(field):
                raise ValueError(target['target_id'] + ': missing ' + field)
        checked_date(target['verified_on'])
        for source in target['sources']:
            public_url(source['url'])
            checked_date(source['checked_on'])
    return projects, {row['project_id']: row for row in summaries}, targets
