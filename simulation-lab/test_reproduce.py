# SPDX-License-Identifier: MIT
"""Guard campaign completeness, target claims and immutable public outputs."""
import copy
import json
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(ROOT / 'reproduce.py'))
validate = MODULE['validate']


class ReproductionRecordTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'reproductions/campaign.json').read_text())
        self.tools = set(self.data['selected_tool_ids'])

    def test_campaign_covers_original_21_candidates(self):
        validate(self.data, self.tools)

    def test_selection_cannot_silently_drop_candidate(self):
        key = self.data['selected_tool_ids'].pop()
        self.data['records'] = [r for r in self.data['records'] if r['tool_id'] != key]
        with self.assertRaisesRegex(ValueError, '21 reviewed candidates'):
            validate(self.data, self.tools)

    def test_target_claim_needs_rule_before_numerical_run(self):
        row = next(r for r in self.data['records'] if r['execution']['status'] == 'target_compared')
        row['target']['declared_before_run'] = False
        with self.assertRaisesRegex(ValueError, 'declared target'):
            validate(self.data, self.tools)

    def test_unperformed_comparison_cannot_pass(self):
        row = self.data['records'][0]
        row['comparison'].update(performed=False, passed=True)
        with self.assertRaisesRegex(ValueError, 'Unperformed comparison'):
            validate(self.data, self.tools)

    def test_published_outputs_must_match_recorded_bytes(self):
        output = next(o for r in self.data['records'] for o in r['outputs'] if o.get('published'))
        output['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Public output changed'):
            validate(self.data, self.tools)

    def test_external_guide_source_rejected(self):
        self.data['records'][0]['guide_source'] = '../../README.md'
        with self.assertRaisesRegex(ValueError, 'Guide source outside'):
            validate(self.data, self.tools)


if __name__ == '__main__':
    unittest.main()
