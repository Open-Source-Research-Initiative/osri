# SPDX-License-Identifier: MIT
"""Guard against missing tools and unsupported status changes in research records."""
import copy
import csv
import json
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parent
validate = runpy.run_path(str(ROOT / 'research.py'))['validate']


class ResearchRecordTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'research/routes.json').read_text())
        with (ROOT / 'tools.csv').open(newline='') as stream:
            self.tools = {row['tool_id']: row for row in csv.DictReader(stream)}

    def test_current_records_cover_catalog(self):
        validate(self.data, self.tools)

    def test_missing_and_duplicate_tools_rejected(self):
        for mutation in ('missing', 'duplicate'):
            data = copy.deepcopy(self.data)
            if mutation == 'missing':
                data['records'].pop()
            else:
                data['records'].append(copy.deepcopy(data['records'][0]))
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, 'coverage'):
                validate(data, self.tools)

    def test_execution_status_needs_evidence(self):
        self.data['records'][0]['execution'].update(status='executed_example', evidence='')
        with self.assertRaisesRegex(ValueError, 'needs evidence'):
            validate(self.data, self.tools)

    def test_published_target_needs_explicit_comparison(self):
        row = self.data['records'][0]
        row['execution'] = {'status': 'reproduced_target', 'evidence': 'run.json', 'result': 'claimed match'}
        with self.assertRaisesRegex(ValueError, 'Published-target claim'):
            validate(self.data, self.tools)

    def test_unknown_status_and_non_https_sources_rejected(self):
        for mutation in ('status', 'source'):
            data = copy.deepcopy(self.data)
            if mutation == 'status':
                data['records'][0]['execution']['status'] = 'probably_reproduced'
            else:
                data['records'][0]['evidence'][0]['url'] = 'http://example.org/source'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate(data, self.tools)


if __name__ == '__main__':
    unittest.main()
