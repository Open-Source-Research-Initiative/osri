# SPDX-License-Identifier: MIT
"""Regression checks for editorial data, route contracts and output accounting."""
from contextlib import contextmanager
import copy
import csv
import json
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest
from unittest.mock import patch

import build
from check import check, Page
from records import project_data, project_status
import render

ROOT = build.HUB


class Records(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for directory in ['projects', 'publications', 'community']:
            shutil.copytree(ROOT / directory, self.root / directory)
        self.summaries = json.loads((self.root / 'projects/summaries.json').read_text())
        self.targets = json.loads((self.root / 'publications/targets.json').read_text())

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        (self.root / 'projects/summaries.json').write_text(json.dumps(self.summaries))
        (self.root / 'publications/targets.json').write_text(json.dumps(self.targets))

    def test_current_records(self):
        projects, summaries, targets = project_data(self.root)
        self.assertEqual(len(projects), 1)
        self.assertEqual(len(targets), 3)
        self.assertEqual(project_status(summaries['OSRI-0001']), 'Active · Research')

    def test_stage_and_activity_validation(self):
        for key in ['stage','activity']:
            original=self.summaries[0][key]; self.summaries[0][key]='batch_paused'; self.save()
            with self.assertRaisesRegex(ValueError,'stage or activity'): project_data(self.root)
            self.summaries[0][key]=original

    def test_whole_project_hold_requires_lead_and_reason(self):
        s=self.summaries[0]; s['activity']='on_hold'; self.save()
        with self.assertRaisesRegex(ValueError,'hold needs a reason'): project_data(self.root)
        s['hold_reason']='Human lead paused the whole project for a scheduled review.'; self.save()
        self.assertEqual(project_status(project_data(self.root)[1]['OSRI-0001']),'On hold · Research')
        s['status_decision']['by']='Agent'; self.save()
        with self.assertRaisesRegex(ValueError,'registered human lead'): project_data(self.root)

    def test_batch_notes_do_not_pause_project_or_advance_stage(self):
        self.summaries[0]['status_detail']='A batch is paused and human review is pending.'; self.save()
        self.assertEqual(project_status(project_data(self.root)[1]['OSRI-0001']),'Active · Research')

    def test_stages_can_repeat_without_publication_claims(self):
        for stage in ['writing_review','research','planning','publication']:
            self.summaries[0]['stage']=stage; self.save(); project_data(self.root)
        self.assertEqual(self.summaries[0]['activity'],'active')

    def test_unknown_project_rejected(self):
        self.summaries[0]['project_id'] = 'OSRI-9999'
        self.save()
        with self.assertRaisesRegex(ValueError, 'Unknown'):
            project_data(self.root)

    def test_target_reference_rejected(self):
        self.targets[0]['project_id'] = 'OSRI-9999'
        self.save()
        with self.assertRaisesRegex(ValueError, 'reference'):
            project_data(self.root)

    def test_missing_attribution_rejected(self):
        self.targets[0]['sources'] = []
        self.save()
        with self.assertRaisesRegex(ValueError, 'sources'):
            project_data(self.root)

    def test_invalid_verification_date_rejected(self):
        self.summaries[0]['verified_on'] = 'yesterday'
        self.save()
        with self.assertRaises(ValueError):
            project_data(self.root)

    def test_selected_target_requires_human_decision(self):
        self.targets[0]['status'] = 'selected'
        self.save()
        with self.assertRaisesRegex(ValueError, 'human decision'):
            project_data(self.root)
        self.targets[0].update(selected_by='Cole / @ajhcs', selected_on='2026-11-15', selection_reference='https://example.org/human-decision')
        self.save()
        self.assertEqual(project_data(self.root)[2][0]['status'], 'selected')

    def test_empty_registers(self):
        (self.root / 'projects/projects.csv').write_text('project_id,title,repository_url,areas,human_lead\n')
        self.summaries, self.targets = [], []
        self.save()
        self.assertEqual(project_data(self.root), ([], {}, []))

    def test_duplicate_target_rejected(self):
        self.targets.append(copy.deepcopy(self.targets[0]))
        self.save()
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            project_data(self.root)

    def test_targets_do_not_change_counts(self):
        activity = runpy.run_path(str(ROOT / 'community/update.py'))['build']
        before = activity(self.root)
        self.targets[0].update(status='selected', selected_by='Cole', selected_on='2026-11-15', selection_reference='https://example.org/decision')
        self.save()
        self.assertEqual(before, activity(self.root))
        self.assertIn('| Published outputs | 0 |', before)

    def test_related_outputs_count_as_one_work(self):
        activity = runpy.run_path(str(ROOT / 'community/update.py'))['build']
        path = self.root / 'publications/publications.csv'
        with path.open() as stream:
            fields = next(csv.reader(stream))
        with path.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fields); writer.writeheader()
            for index, kind in enumerate(['preprint', 'journal_article', 'research_blog']):
                row = dict.fromkeys(fields, '')
                row.update(publication_id=f'P{index}', project_id='OSRI-0001', work_id='W1', publication_type=kind, status='published', url='https://example.org/work', first_published_date='2026-11-15')
                writer.writerow(row)
        result = activity(self.root)
        self.assertIn('| Published outputs | 3 |', result)
        self.assertIn('| Distinct published works | 1 |', result)


class Rendering(unittest.TestCase):
    @contextmanager
    def fixture(self, empty=False):
        with tempfile.TemporaryDirectory() as temp:
            hub = Path(temp) / 'hub'
            shutil.copytree(ROOT, hub, ignore=shutil.ignore_patterns('.git', '__pycache__'))
            if empty:
                (hub / 'projects/projects.csv').write_text('project_id,title,repository_url,areas,human_lead\n')
                (hub / 'projects/summaries.json').write_text('[]')
                (hub / 'publications/targets.json').write_text('[]')
            else:
                with (hub / 'projects/projects.csv').open('a') as stream:
                    stream.write('OSRI-0002,Second study,https://example.org/study,Engineering,Second human\n')
                summaries = json.loads((hub / 'projects/summaries.json').read_text())
                second = copy.deepcopy(summaries[0]); second['project_id'] = 'OSRI-0002'; second['short_title'] = 'Second study'; second['summary'] = 'Second question with a separate human lead.'; second['stage'] = 'planning'; second['status_decision']['by'] = 'Second human'
                summaries.append(second)
                (hub / 'projects/summaries.json').write_text(json.dumps(summaries))
            output = Path(temp) / 'built'
            with patch.object(build, 'HUB', hub), patch.object(build, 'SITE', hub / 'site'), patch.object(build.subprocess, 'check_output', side_effect=[('a' * 40), '2026-11-15T12:00:00+00:00']):
                site = build.Website(output)
                site.build()
                check(output)
                yield site, output

    def test_multiple_projects_end_to_end(self):
        with self.fixture() as (site, output):
            second = (output / 'research/osri-0002/index.html').read_text()
            self.assertIn('Second human', second)
            self.assertIn('No venue candidates', second)
            self.assertNotIn('Candidate—under review', second)
            self.assertEqual(len([r for r in site.search_records.values() if r['type'] == 'project' and r['language'] == 'en']), 2)
            browser = (output / 'venues/index.html').read_text()
            self.assertIn('href="/data/publications-venues-venues.csv"', browser)
            self.assertIn('href="/data/publications-venues-venues.json"', browser)
            self.assertNotIn('href="${escapeText(p)}"', browser)
            self.assertIn('/free-publication-directory/blob/', browser)
            self.assertEqual((output / 'data/publications-venues-venues.json').read_bytes(), (ROOT / 'publications/venues/venues.json').read_bytes())
            self.assertEqual(browser.count('<main '),1)
            self.assertIn('class="site-header wrap"',browser)
            self.assertIn('data-provenance-base="https://github.com/',browser)
            self.assertIn('/venue-directory.js',browser)
            self.assertIn('name="subfield"',(output / 'index.html').read_text())
            for route in ['index.html','research/index.html','contribute/index.html','research/osri-0001/index.html']:
                text=(output / route).read_text()
                self.assertIn('Active · Research',text)
                self.assertNotIn('screening remains paused',text)
            self.assertIn('aria-current="step">Research',(output / 'research/osri-0001/index.html').read_text())

    def test_tampered_directory_assets_rejected(self):
        for asset in ['directory.css','directory.js','browser-fragment.html','venues.json']:
            with tempfile.TemporaryDirectory() as temp:
                directory=Path(temp)/'publications/venues'
                shutil.copytree(ROOT/'publications/venues',directory)
                (directory/asset).write_text('altered')
                site=object.__new__(build.Website)
                with patch.object(build,'HUB',Path(temp)):
                    with self.assertRaisesRegex(ValueError,'reviewed snapshot'):site.venue_snapshot()

    def test_explicit_project_hold_shows_reason_on_project_page(self):
        with self.fixture() as (site, output):
            record=site.summaries['OSRI-0001']
            record.update(activity='on_hold',hold_reason='Whole-project hold requested by the human lead.')
            text=render.project(site,site.projects[0])
            self.assertIn('On hold · Research',text)
            self.assertIn(record['hold_reason'],text)
            self.assertIn('data-activity="on_hold"',text)

    def test_tampered_venue_browser_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp) / 'publications/venues'
            directory.mkdir(parents=True)
            shutil.copy2(ROOT / 'publications/venues/snapshot.json', directory / 'snapshot.json')
            (directory / 'browser.html').write_text('<html>unreviewed replacement</html>')
            site = object.__new__(build.Website)
            with patch.object(build, 'HUB', Path(temp)):
                with self.assertRaisesRegex(ValueError, 'reviewed snapshot'):
                    site.render_venue_directory()

    def test_empty_projects_end_to_end(self):
        with self.fixture(empty=True) as (site, output):
            self.assertIn('No projects are registered', (output / 'index.html').read_text())
            self.assertIn('No public outputs', (output / 'publications/index.html').read_text())
            self.assertFalse(any(r['type'] == 'project' for r in site.search_records.values()))

    def test_selected_target_display(self):
        with self.fixture() as (site, output):
            selected = site.targets[0]
            selected.update(status='selected', selected_by='Cole / @ajhcs', selected_on='2026-11-15', selection_reference='https://example.org/decision')
            text = render.targets(site, 'OSRI-0001')
            self.assertIn('Selected target', text)
            self.assertIn('Selected by Cole / @ajhcs on 2026-11-15', text)
            self.assertIn('https://example.org/decision', text)
            self.assertIn('Targets do not count as published outputs', text)

    def test_legacy_routes(self):
        self.assertEqual(build.route('translations/zh-Hans/CONTRIBUTING.md'), '/zh-hans/contribute/')
        self.assertEqual(build.route('START_HERE.md'), '/start/')
        self.assertEqual(build.route('community/ACTIVITY.md'), '/activity/')


if __name__ == '__main__':
    unittest.main()
