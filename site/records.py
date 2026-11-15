# SPDX-License-Identifier: MIT
"""Validate editorial summaries and venue plans independently of publication counts."""
import csv
from datetime import date
import json
import re
from urllib.parse import urlsplit


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
        for field in ['question', 'summary', 'status', 'status_detail', 'methods', 'contribution', 'outputs', 'sources']:
            if not summary.get(field):
                raise ValueError(key + ': missing ' + field)
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
