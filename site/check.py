#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check generated pages, links, attribution, metadata and search coverage."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from i18n import LANGUAGES
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids = [], set()
        self.headings = 0
        self.language = None
        self.direction = None
        self.missing_alt = False
        self.canonical = None
        self.description = None
        self.source_commit = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'html':
            self.language = attrs.get('lang')
            self.direction = attrs.get('dir', 'ltr')
        if tag == 'h1':
            self.headings += 1
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                raise ValueError('Duplicate HTML ID: ' + attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = attrs.get('content')
        for key in ['href', 'src']:
            if key in attrs:
                self.links.append(attrs[key])
                if re.search(r'github.com/Open-Source-Research-Initiative/osri/(blob|tree)/[a-f0-9]{40}', attrs[key]):
                    self.source_commit = True
        if tag == 'img' and 'alt' not in attrs:
            self.missing_alt = True


def check(root):
    pages = {}
    metadata = json.loads((root / 'build-info.json').read_text())
    origin = 'https://open-source-research-initiative.github.io'
    for path in root.rglob('*.html'):
        page = Page()
        page.feed(path.read_text(encoding='utf-8'))
        if page.headings != 1 or page.missing_alt or page.language not in LANGUAGES:
            raise ValueError(f'{path.relative_to(root)}: check heading, language, or image alternatives')
        if page.direction != LANGUAGES[page.language][1]:
            raise ValueError(f'{path.relative_to(root)}: incorrect text direction')
        relative = path.relative_to(root).as_posix()
        url = '/' + (relative[:-10] if relative.endswith('index.html') else relative)
        if page.canonical != origin + url or not page.description or not page.source_commit:
            raise ValueError(f'{relative}: missing canonical, page description or immutable hub source')
        if metadata['source_commit'] not in path.read_text():
            raise ValueError(f'{relative}: source commit differs from build record')
        pages[path.resolve()] = page

    def check_link(path, url):
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc:
            return False
        target = root / unquote(parsed.path.lstrip('/')) if parsed.path.startswith('/') else path.parent / unquote(parsed.path)
        if not parsed.path:
            target = path
        if target.is_dir() or parsed.path.endswith('/'):
            target = target / 'index.html'
        target = target.resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            raise ValueError(f'{path.relative_to(root)}: broken local link {url}')
        if parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
            raise ValueError(f'{path.relative_to(root)}: missing anchor {url}')
        return True

    checked_links = sum(check_link(path, url) for path, page in pages.items() for url in page.links)
    for css in root.glob('*.css'):
        for url in re.findall(r'url\([\'\"]?([^\)\'\"]+)', css.read_text()):
            path = root / url.lstrip('/') if url.startswith('/') else css.parent / url
            if not path.is_file():
                raise ValueError(f'{css.name}: missing asset {url}')
    for vector in (root / 'assets/identity').glob('*.svg'):
        if '../fonts/' in vector.read_text():
            raise ValueError('Unresolved SVG font: ' + vector.name)
    for language in LANGUAGES:
        if language == 'en':
            continue
        for page in root.glob(language.lower() + '/**/index.html'):
            if not re.search(r'data-translation-status="(?:draft|reviewed|needs-update)"', page.read_text()):
                raise ValueError(f'{page}: translation draft notice missing')
    if len(pages) != len(metadata['pages']):
        raise ValueError('Page count does not match the build record')
    records = json.loads((root / 'search-index.json').read_text())
    urls = [row['url'] for row in records]
    if len(set(urls)) != len(urls) or sorted(urls) != metadata['search_urls'] or len(records) != metadata['search_records']:
        raise ValueError('Search index does not match build coverage')
    if not (set(metadata['pages']) - {'/search/', '404.html'}).issubset(urls):
        raise ValueError('Generated page missing from search index')
    for row in records:
        if row['type'] not in {'project', 'topic', 'resource', 'guide', 'publication'} or not row['title'] or not row['text']:
            raise ValueError('Invalid search entry')
        if not row['url'].startswith('/'):
            raise ValueError('Search result must use a local route')
        check_link(root / 'index.html', row['url'])
    project_pages = [url for url in metadata['pages'] if re.fullmatch(r'/research/osri-\d+/', url)]
    if len(project_pages) != metadata['project_summaries']:
        raise ValueError('Project summary missing its route')
    print(f'Checked {len(pages)} pages, {checked_links} local links, {len(records)} search records, metadata, attribution, SVG fonts and translation notices')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    check(parser.parse_args().directory.resolve())
