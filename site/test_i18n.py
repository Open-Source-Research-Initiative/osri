# SPDX-License-Identifier: MIT
"""Behavioral checks for translation boundaries, fallback and review freshness."""
import unittest

import i18n


class Translation(unittest.TestCase):
    def render(self, text, messages=None, language='ar'):
        parser = i18n.Translator(set(), messages or {}, language, {'/', '/start/', '/search/'})
        parser.feed(text)
        return parser, ''.join(parser.output)

    def test_language_direction_routes_and_identifiers(self):
        parser, text = self.render('<html lang="en"><body><h1 id="research">Research</h1><a href="/start/?step=1#evidence">Start here</a><a data-language="es" href="/es/start/">Español</a><a href="https://example.org/a">Official source</a><code>Research OSRI-0001</code><script type="application/json">{"status":"draft"}</script></body></html>', {'Research': 'بحث', 'Start here': 'ابدأ هنا', 'Official source': 'المصدر الرسمي'})
        self.assertIn('lang="ar" dir="rtl"', text)
        self.assertIn('id="research">بحث', text)
        self.assertIn('href="/ar/start/?step=1#evidence"', text)
        self.assertIn('href="/es/start/">Español', text)
        self.assertIn('href="https://example.org/a"', text)
        self.assertIn('<code>Research OSRI-0001</code>', text)
        self.assertIn('{"status":"draft"}', text)
        self.assertEqual(parser.missing, set())

    def test_accessible_attributes_and_visible_fallback(self):
        parser, text = self.render('<h1>New guide</h1><input placeholder="Search guides"><img src="/diagram.svg" alt="Research stages"><p translate="no">Original title</p>', {'Search guides': 'Buscar guías', 'Research stages': 'Etapas de investigación'}, 'es')
        self.assertIn('placeholder="Buscar guías"', text)
        self.assertIn('alt="Etapas de investigación"', text)
        self.assertIn('<h1>New guide</h1>', text)
        self.assertEqual(parser.missing, {'New guide'})
        self.assertNotIn('Original title', parser.messages)

    def test_review_invalidated_by_source_or_translation_change(self):
        review = {'language': 'ko', 'url': '/start/', 'source_digest': 'source1', 'translation_digest': 'translation1', 'reviewer': 'Fluent reviewer', 'review_date': '2026-11-17', 'domain_reviewer': 'Subject reviewer', 'review_url': 'https://example.org/review'}
        self.assertEqual(i18n.page_review([], 'ko', '/start/', 'source1', 'translation1'), ('draft', 'unassigned'))
        self.assertEqual(i18n.page_review([review], 'ko', '/start/', 'source1', 'translation1')[0], 'reviewed')
        self.assertEqual(i18n.page_review([review], 'ko', '/start/', 'source2', 'translation1')[0], 'needs-update')
        self.assertEqual(i18n.page_review([review], 'ko', '/start/', 'source1', 'translation2')[0], 'needs-update')
        del review['domain_reviewer']
        with self.assertRaisesRegex(ValueError, 'Incomplete human'):
            i18n.page_review([review], 'ko', '/start/', 'source1', 'translation1')

    def test_all_languages_have_page_preserving_links(self):
        links = i18n.language_links('/guides/governance/translation/')
        for language in i18n.LANGUAGES:
            self.assertIn('href="' + i18n.prefix(language) + '/guides/governance/translation/"', links)
            self.assertIn('hreflang="' + language + '"', links)

    def test_identifiers_are_not_translated(self):
        for identifier in ['OSRI-0001', 'RES-001', '107a7d081ddf4e128db74b340317ff42', '30fe2233583fbd25c51579b7ba389a7bc081ead4']:
            self.assertFalse(i18n.translatable(identifier))

    def test_locale_metadata_and_asset_urls(self):
        _, text = self.render('<html lang="en"><head><link rel="canonical" href="https://open-source-research-initiative.github.io/start/"><link rel="alternate" hreflang="ko" href="https://open-source-research-initiative.github.io/ko/start/"></head><body><img src="/assets/diagram.svg" alt=""></body></html>')
        self.assertIn('rel="canonical" href="https://open-source-research-initiative.github.io/ar/start/"', text)
        self.assertIn('hreflang="ko" href="https://open-source-research-initiative.github.io/ko/start/"', text)
        self.assertIn('src="/assets/diagram.svg"', text)


if __name__ == '__main__':
    unittest.main()
