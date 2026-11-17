# SPDX-License-Identifier: MIT
"""Offline, source-keyed translations of the complete generated site.

Catalogs are editable JSON, keyed by the exact English text. No translation
service is contacted by the builder or by a visitor's browser.
"""
from html import escape
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

LANGUAGES = {
    'en': ('English', 'ltr', ''),
    'zh-Hans': ('简体中文', 'ltr', '待审核译稿：机器翻译，尚未经人工核验。请对照英文原文。'),
    'ko': ('한국어', 'ltr', '검토 대기 초안: 기계 번역이며 아직 사람이 검증하지 않았습니다. 영어 원문을 함께 확인하세요.'),
    'es': ('Español', 'ltr', 'Borrador pendiente de revisión: traducción automática sin verificación humana. Consulte el original en inglés.'),
    'fr': ('Français', 'ltr', 'Brouillon à relire : traduction automatique sans vérification humaine. Consultez la version anglaise.'),
    'ar': ('العربية', 'rtl', 'مسودة بانتظار المراجعة: ترجمة آلية لم يتحقق منها مراجع بشري بعد. يرجى الرجوع إلى الأصل الإنجليزي.'),
}
SKIP = {'script', 'style', 'code', 'pre', 'kbd', 'samp', 'svg'}
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
ATTRIBUTES = {'alt', 'title', 'placeholder', 'aria-label'}
EXTRA = ['{shown} of {total} shown', '{count} results', '{count} result', 'all content',
         '{count} matching venues', '{count} of 3 venues selected', 'Compare selected venues ({count}/3)',
         'Compare {name}', 'Remove {name} from comparison', 'Source {count}',
         'Lower reported acceptance rate first. Missing values follow; check each source, period, and population.',
         'Higher reported metric value first. Missing values follow; check each source, period, and population.',
         'Interactive search unavailable. Browse all records below or use your browser’s Find command.']


def prefix(language):
    return '' if language == 'en' else '/' + language.lower()


def local_url(url, language, pages):
    parsed = urlsplit(url)
    if not parsed.scheme and not parsed.netloc and parsed.path in pages:
        return prefix(language) + parsed.path + ('?' + parsed.query if parsed.query else '') + ('#' + parsed.fragment if parsed.fragment else '')
    return url


def language_links(url):
    return ''.join('<a data-language="' + language + '" lang="' + language + '" hreflang="' + language + '" dir="' + direction + '" href="' + prefix(language) + url + '">' + name + '</a>' for language, (name, direction, _) in LANGUAGES.items())


def translatable(text):
    text = text.strip()
    if re.fullmatch(r'[a-fA-F0-9]{12,}|(?:OSRI|RES|PAP|SIM|EX)-[\w-]+', text):
        return False
    return (bool(re.search('[A-Za-z]{2}', text)) and
            not re.fullmatch(r'[^\s]*(?:[/@]|\.[A-Za-z0-9]{2,5}$)[^\s]*', text) and
            not re.match(r'^(?:https?://|[a-f0-9]{40}$|Source commit [a-f0-9]+$)', text)) or text in {
                'Research', 'Resources', 'Guides', 'About', 'Language', 'Search', 'Menu',
                'Publications', 'Activity', 'Licensing', 'Source', 'Documentation',
                'License', 'English', 'Healthcare', 'Engineering', 'Informatics',
                'Economics', 'Translation', 'Topics', 'Standards', 'Collaborate',
                'project', 'topic', 'resource', 'guide', 'publication', 'unknown',
                'supported', 'concerns', 'Charged', 'Compare', 'Remove', 'Clear',
            }


class Translator(HTMLParser):
    def __init__(self, messages, catalog=None, language='en', pages=()):
        super().__init__(convert_charrefs=True)
        self.messages, self.catalog, self.language, self.pages = messages, catalog, language, set(pages)
        self.stack, self.output, self.missing = [], [], set()

    def text(self, value):
        key = value.strip()
        if not translatable(key):
            return value
        self.messages.add(key)
        translated = self.catalog.get(key, '') if self.catalog is not None else key
        if not translated:
            self.missing.add(key)
            translated = key
        return value[:len(value)-len(value.lstrip())] + translated + value[len(value.rstrip()):]

    def handle_decl(self, decl):
        self.output.append('<!' + decl + '>')

    def handle_comment(self, value):
        self.output.append('<!--' + value + '-->')

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        skip = any(self.stack) or tag in SKIP or attrs.get('translate') == 'no' or 'data-language' in attrs
        if tag not in VOID:
            self.stack.append(skip)
        if self.language != 'en':
            if tag == 'html':
                attrs.update(lang=self.language, dir=LANGUAGES[self.language][1])
            if not skip:
                for key in ATTRIBUTES & attrs.keys():
                    attrs[key] = self.text(attrs[key])
                if 'data-search' in attrs:
                    del attrs['data-search']  # Search the translated visible text.
            if tag in {'a', 'form'} and 'data-language' not in attrs:
                for key in {'href', 'action'} & attrs.keys():
                    attrs[key] = local_url(attrs[key], self.language, self.pages)
            if tag == 'link' and attrs.get('rel') == 'canonical' or tag == 'meta' and attrs.get('property') == 'og:url':
                key = 'href' if tag == 'link' else 'content'
                attrs[key] = attrs[key].replace('https://open-source-research-initiative.github.io', 'https://open-source-research-initiative.github.io' + prefix(self.language), 1)
            if tag == 'meta' and (attrs.get('name') == 'description' or attrs.get('property') in {'og:title', 'og:description'}):
                attrs['content'] = self.text(attrs['content'])
        else:
            if not skip:
                for key in ATTRIBUTES & attrs.keys():
                    self.text(attrs[key])
            if tag == 'meta' and (attrs.get('name') == 'description' or attrs.get('property') in {'og:title', 'og:description'}):
                self.text(attrs['content'])
        self.output.append('<' + tag + ''.join(' ' + key + ('="' + escape(value, quote=True) + '"' if value is not None else '') for key, value in attrs.items()) + '>')

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag not in VOID and self.stack:
            self.stack.pop()
        self.output.append('</' + tag + '>')

    def handle_data(self, value):
        self.output.append(value if any(self.stack) else escape(self.text(value)))


def protected_terms(hub):
    """Original titles and scientific/source identifiers remain in their source language."""
    import csv
    terms = {'OSRI', 'Agentic-Powered-Research', 'Open Source Research Initiative', 'GitHub', 'CC BY 4.0', 'MIT'}
    for path in ['simulation-lab/papers.csv', 'simulation-lab/tools.csv', 'resources/resources.csv', 'projects/projects.csv']:
        with (hub / path).open() as stream:
            for row in csv.DictReader(stream):
                for key in ['title', 'name', 'authors']:
                    if row.get(key):
                        terms.add(row[key])
    def visit(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {'title', 'name', 'doi', 'issn', 'id'} and isinstance(item, str):
                    terms.add(item)
                else:
                    visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)
    visit(json.loads((hub / 'publications/venues/venues.json').read_text()))
    return terms


def extra_messages(hub):
    messages = set(EXTRA)
    captions = (hub / 'site/assets/demos/venue-directory-demo.vtt').read_text()
    messages.update(block.split('\n', 1)[1] for block in captions.strip().split('\n\n')[1:])
    # Include directory evidence shown only after filtering or expanding a record.
    def visit(value):
        if isinstance(value, str) and translatable(value):
            messages.add(value)
            messages.add(value.replace('_', ' '))
        elif isinstance(value, dict):
            for key, item in value.items():
                if translatable(key.replace('_', ' ')):
                    messages.add(key.replace('_', ' '))
                visit(item)
        elif isinstance(value, list):
            for item in value:
                visit(item)
    visit(json.loads((hub / 'publications/venues/venues.json').read_text()))
    script = (hub / 'publications/venues/directory.js').read_text()
    for match in re.finditer(r"'([^'\n\\]*)'", script):
        value = match[1]
        if '<' not in value and '>' not in value and translatable(value):
            messages.add(value)
    for value in re.findall(r'>([^<>]+)<', script):
        if not re.search(r'[$}{`]|\|\||\.join\(|\)\)|escapeText', value) and translatable(value):
            messages.add(value)
    return {message.strip() for message in messages}


def catalog(hub, language):
    path = hub / 'translations/catalogs' / (language + '.json')
    return json.loads(path.read_text()) if path.exists() else {'language': language, 'status': 'draft', 'translator': 'unassigned', 'reviewer': 'unassigned', 'messages': {}}


def page_review(reviews, language, url, source_digest, translation_digest):
    record = next((row for row in reviews if row['language'] == language and row['url'] == url), None)
    if record is None:
        return 'draft', 'unassigned'
    required = ['reviewer', 'review_date', 'review_url', 'domain_reviewer', 'source_digest', 'translation_digest']
    if any(not record.get(key) or record[key] == 'unassigned' for key in required):
        raise ValueError('Incomplete human translation review: ' + language + ' ' + url)
    status = 'reviewed' if record['source_digest'] == source_digest and record['translation_digest'] == translation_digest else 'needs-update'
    return status, record['reviewer']


def build_translations(site):
    english_pages = sorted(url for url in site.pages if url.endswith('/'))
    messages = extra_messages(site.hub)
    usage = {}
    documents = {}
    for row in site.search_records.values():
        if not urlsplit(row['url']).fragment:
            continue
        for key in ['title', 'text']:
            if translatable(row[key]):
                messages.add(row[key].strip())
    for url in english_pages:
        text = (site.output / url.lstrip('/') / 'index.html').read_text()
        found = set()
        parser = Translator(found)
        parser.feed(text)
        messages.update(found)
        documents[url] = text
        usage[url] = sorted(found)
        if '<video ' in text:
            captions = (site.hub / 'site/assets/demos/venue-directory-demo.vtt').read_text()
            cues = {block.split('\n', 1)[1].strip() for block in captions.strip().split('\n\n')[1:]}
            usage[url] = sorted(found | cues)
    protected = protected_terms(site.hub)
    messages -= protected
    usage['/venues/'] = sorted(set(usage['/venues/']) | extra_messages(site.hub))
    digest = hashlib.sha256(json.dumps(sorted(messages), ensure_ascii=False).encode()).hexdigest()
    inventory = {'source_commit': site.commit, 'source_digest': digest, 'protected_terms': sorted(protected), 'pages': usage, 'messages': sorted(messages)}
    (site.output / 'translation-source.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + '\n')
    coverage = {}
    page_records = []
    reviews_path = site.hub / 'translations/reviews.json'
    reviews = json.loads(reviews_path.read_text()) if reviews_path.exists() else []
    for language in LANGUAGES:
        if language == 'en':
            continue
        record = catalog(site.hub, language)
        translated = {**record['messages'], **{term: term for term in protected}}
        missing = messages - {key for key, value in translated.items() if value.strip()}
        coverage[language] = {'status': record['status'], 'reviewer': record['reviewer'], 'messages': len(messages), 'missing': len(missing), 'pages': len(english_pages)}
        for url, text in documents.items():
            parser = Translator(set(), translated, language, english_pages)
            parser.feed(text)
            text = ''.join(parser.output)
            if '<video ' in text:
                english_track = '<track kind="captions" src="/assets/demos/venue-directory-demo.vtt" srclang="en" label="English">'
                localized_track = '<track kind="captions" src="' + prefix(language) + '/venue-directory-demo.vtt" srclang="' + language + '" label="' + LANGUAGES[language][0] + '" default>'
                text = text.replace(english_track, localized_track + english_track)
            normalized = documents[url].replace(site.commit, '<source-commit>').replace(site.commit[:7], '<short-commit>')
            source_digest = hashlib.sha256(normalized.encode()).hexdigest()
            translation_digest = hashlib.sha256(json.dumps({key: translated.get(key, '') for key in usage[url]}, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
            status, reviewer = page_review(reviews, language, url, source_digest, translation_digest)
            if parser.missing:
                status = 'needs-update'
            page_records.append({'language': language, 'url': prefix(language) + url, 'english_url': url, 'source_commit': site.commit, 'source_digest': source_digest, 'translation_digest': translation_digest, 'status': status, 'reviewer': reviewer, 'missing': len(parser.missing)})
            label = LANGUAGES[language][2] if status != 'reviewed' else {'zh-Hans': '已完成人工翻译审核。', 'ko': '사람이 번역을 검토했습니다.', 'es': 'Traducción revisada por una persona.', 'fr': 'Traduction relue par une personne.', 'ar': 'راجع شخص هذه الترجمة.'}[language]
            notice = '<aside class="translation-notice" data-translation-status="' + status + '"><p>' + escape(label) + '</p><a href="' + url + '" lang="en" dir="ltr">English</a> · <a href="https://github.com/orgs/Open-Source-Research-Initiative/discussions/3">' + {'zh-Hans': '帮助审核', 'ko': '번역 검토 참여', 'es': 'Ayude a revisar', 'fr': 'Participer à la relecture', 'ar': 'المساعدة في المراجعة'}[language] + '</a>'
            if parser.missing:
                notice += '<p lang="en" dir="ltr">' + str(len(parser.missing)) + ' changed English passages await translation.</p>'
            notice += '</aside>'
            text = text.replace('<main id="main" class="wrap" tabindex="-1">', '<main id="main" class="wrap" tabindex="-1">' + notice)
            text = text.replace('<script type="module" src="/site.js"></script>', '<script src="' + prefix(language) + '/messages.js"></script><script src="/i18n.js" defer></script><script type="module" src="/site.js"></script>')
            site.write(prefix(language) + url, text, translated=True)
        runtime = {key: value for key, value in translated.items() if key != value}
        destination = site.output / language.lower()
        captions = (site.hub / 'site/assets/demos/venue-directory-demo.vtt').read_text()
        for source in re.findall(r'(?m)^([^\n]+)$', captions):
            if source in translated:
                captions = captions.replace(source, translated[source])
        (destination / 'venue-directory-demo.vtt').write_text(captions)
        # JSON cannot terminate a script element; this is an external JS resource.
        (destination / 'messages.js').write_text('window.OSRI_MESSAGES=' + json.dumps(runtime, ensure_ascii=False) + ';\n')
        records = [dict(row, url=prefix(language) + row['url'], language=language) for row in site.search_records.values() if row['language'] == 'en']
        for row in records:
            localized = site.output / urlsplit(row['url']).path.lstrip('/') / 'index.html'
            row['title'] = translated.get(row['title'].strip(), row['title'])
            row['text'] = translated.get(row['text'].strip(), row['text'])
            if localized.exists() and not urlsplit(row['url']).fragment:
                document = localized.read_text()
                from build import plain
                row['title'] = plain(re.search(r'<h1[^>]*>(.*?)</h1>', document, re.S)[1])
                row['text'] = plain(re.search(r'<main[^>]*>(.*?)</main>', document, re.S)[1])
        (destination / 'search-index.json').write_text(json.dumps(records, ensure_ascii=False) + '\n')
    (site.output / 'search-index.json').write_text(json.dumps(list(site.search_records.values()), ensure_ascii=False) + '\n')
    (site.output / 'translation-coverage.json').write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + '\n')
    (site.output / 'translation-pages.json').write_text(json.dumps(page_records, ensure_ascii=False, indent=2) + '\n')
    print('Translation coverage: ' + ', '.join(f'{tag}: {row["messages"]-row["missing"]}/{row["messages"]}' for tag, row in coverage.items()))
