#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build OSRI's public website from this hub's Markdown and CSV records."""

import argparse
import csv
from datetime import datetime
from html import escape
from html.parser import HTMLParser

from html_helpers import href, link
from records import project_data
import render
import json
from pathlib import Path, PurePosixPath
import re
import runpy
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

HUB = Path(__file__).resolve().parents[1]
SITE = HUB / "site"
ORIGIN = "https://open-source-research-initiative.github.io"
GITHUB = "https://github.com/Open-Source-Research-Initiative"
FORUM = "https://github.com/orgs/Open-Source-Research-Initiative/discussions"
ALIASES = {"START_HERE.md": "/start/", "CONTRIBUTING.md": "/guides/contributing/", "community/ACTIVITY.md": "/activity/", "README.md": "/guides/osri/"}
NAV = [("Research", "/research/"), ("Simulation Lab", "/simulation-lab/"), ("Resources", "/resources/"), ("Guides", "/guides/"), ("About", "/about/")]
AREAS = [("healthcare", "Healthcare", "Nonclinical public health and health systems research."), ("engineering", "Engineering", "Systems Engineering, Engineering Management, Operations Research, and Decision Science. Initial work excludes physical laboratory experiments."), ("informatics", "Informatics", "Bioinformatics, information systems, and Computational Natural Sciences. Initial work excludes physical laboratory experiments."), ("economics", "Economics", "Resources, incentives, public economics, research, and innovation."), ("social-behavioral-sciences", "Social and Behavioral Sciences", "Judgment, collaboration, organizations, and behavior."), ("public-policy", "Public Policy", "Policy analysis, evaluation, institutions, and governance.")]


def read_csv(path):
    with (HUB / path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def route(path):
    if path in ALIASES:
        return ALIASES[path]
    if path.startswith("translations/zh-Hans/"):
        tail = path.removeprefix("translations/zh-Hans/")
        if tail == "CONTRIBUTING.md":
            return "/zh-hans/contribute/"
        if tail == "README.md":
            return "/zh-hans/"
        return "/zh-hans" + (ALIASES[tail] if tail in ALIASES else route(tail))
    parts = list(PurePosixPath(path).with_suffix("").parts)
    if parts[-1] == "README":
        parts.pop()
    parts = [p.lower().replace("_", "-") for p in parts]
    return "/guides/" + "/".join(parts) + "/"


def title_of(text, fallback):
    found = re.search(r"^# (.+)$", text, re.M)
    return found.group(1).strip() if found else fallback.replace("-", " ").replace("_", " ").capitalize()


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        self.parts.append(data)

def plain(html):
    parser = Text()
    parser.feed(html)
    return ' '.join(' '.join(parser.parts).split())


class Website:
    def __init__(self, output):
        self.output = output
        self.commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=HUB, text=True).strip()
        self.snapshot = subprocess.check_output(["git", "show", "-s", "--format=%cI", "HEAD"], cwd=HUB, text=True).strip()
        candidates = []
        for path in sorted(HUB.rglob("*.md")):
            rel = path.relative_to(HUB).as_posix()
            if rel.startswith("simulation-lab/reproductions/files/"):
                continue
            if rel.startswith((".git/", ".github/", "site/", "identity/")) and rel != "identity/prism/research-journey.md":
                continue
            candidates.append(rel)
        self.docs = {rel: route(rel) for rel in candidates}
        if len(set(self.docs.values())) != len(self.docs):
            raise ValueError("Duplicate documentation routes")
        self.pages = set()
        self.search_records = {}
        self.forum = FORUM
        self.areas = AREAS
        self.projects, self.summaries, self.targets = project_data(HUB)

    def source_url(self, path):
        return f"{GITHUB}/osri/blob/{self.commit}/{path}"

    def rewrite(self, url, source="README.md", image=False):
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc:
            if parsed.netloc == urlsplit(ORIGIN).netloc and parsed.scheme in {"http", "https"}:
                return (parsed.path or "/") + ("?" + parsed.query if parsed.query else "") + ("#" + parsed.fragment if parsed.fragment else "")
            prefix = f"{GITHUB}/osri/blob/main/"
            if url.startswith(prefix):
                return self.rewrite("/" + url[len(prefix):], source, image)
            return url
        if url.startswith("#"):
            return url
        target = parsed.path.lstrip("/") if parsed.path.startswith("/") else str(PurePosixPath(source).parent / unquote(parsed.path))
        parts = []
        for part in PurePosixPath(target).parts:
            if part == "..":
                if not parts:
                    raise ValueError(f"Link leaves repository: {source} -> {url}")
                parts.pop()
            elif part not in {".", ""}:
                parts.append(part)
        target = "/".join(parts)
        suffix = ("?" + parsed.query if parsed.query else "") + ("#" + parsed.fragment if parsed.fragment else "")
        if target in self.docs:
            return self.docs[target] + suffix
        if target.endswith(".csv") and (HUB / target).is_file():
            return "/data/" + target.replace("/", "-") + suffix
        if target.startswith('identity/prism/previews/') and target.endswith('.png'):
            vector = 'identity/prism/sources/' + Path(target).stem + '.svg'
            if (HUB / vector).is_file():
                return '/assets/identity/' + Path(vector).name + suffix
        if target.startswith('identity/prism/sources/') and target.endswith('.svg') and (HUB / target).is_file():
            return '/assets/identity/' + Path(target).name + suffix
        if image and (HUB / target).is_file():
            return f"https://raw.githubusercontent.com/Open-Source-Research-Initiative/osri/{self.commit}/{target}" + suffix
        return self.source_url(target) + suffix

    def markdown(self, text, source):
        parser = MarkdownIt("commonmark", {"html": False}).enable("table")
        tokens = parser.parse(text)
        used = set()
        for index, token in enumerate(tokens):
            if token.type == "heading_open":
                label = tokens[index + 1].content
                slug = re.sub(r"[^\w\s-]", "", label.lower()).strip().replace(" ", "-")
                value, number = slug, 0
                while value in used:
                    number += 1
                    value = f"{slug}-{number}"
                token.attrSet("id", value)
                used.add(value)
            for child in token.children or []:
                if child.type == "link_open":
                    child.attrSet("href", self.rewrite(child.attrGet("href"), source))
                elif child.type == "image":
                    child.attrSet("src", self.rewrite(child.attrGet("src"), source, image=True))
        rendered = parser.renderer.render(tokens, parser.options, {})
        rendered = re.sub(r'<h([2-6]) id="([^"]+)">(.*?)</h\1>', lambda match: '<h' + match[1] + ' id="' + match[2] + '">' + match[3] + '<a class="heading-link" href="#' + match[2] + '" aria-label="Link to ' + escape(plain(match[3]), quote=True) + '">#</a></h' + match[1] + '>', rendered)
        contents = [(token.attrGet('id'), tokens[i + 1].content) for i, token in enumerate(tokens) if token.type == 'heading_open' and token.tag == 'h2']
        if len(contents) >= 3:
            label = '本页内容' if source.startswith('translations/') else 'On this page'
            toc = '<details class="contents" open><summary>' + label + '</summary><nav aria-label="' + label + '"><ol>' + ''.join('<li>' + link(title, '#' + slug) + '</li>' for slug, title in contents) + '</ol></nav></details>'
            rendered = re.sub(r'(</h1>)', lambda match: match[1] + toc, rendered, count=1)
        return rendered

    def layout(self, title, content, active="", source=None, chinese=False, document=False, home=False, description=None):
        navigation = ''.join(link(label, url, aria_current='page' if url == active else 'false') for label, url in NAV)
        translated = 'translations/zh-Hans/' + source if source and not source.startswith('translations/') else None
        other = self.docs.get(translated, '/zh-hans/') if not chinese else self.docs.get(source.removeprefix('translations/zh-Hans/'), '/')
        if chinese and source == 'translations/zh-Hans/README.md':
            other = '/'
        language = link('简体中文 · 待审核' if not chinese else 'English', other, lang='zh-Hans' if not chinese else 'en')
        source_note = link('View source on GitHub' if not chinese else '在 GitHub 查看原文', self.source_url(source)) if source else link('Source commit ' + self.commit[:7], f'{GITHUB}/osri/tree/{self.commit}')
        if document:
            items = [('Research guide', '/start/'), ('Collaborate', '/contribute/'), ('Browser setup', self.docs['docs/browser-setup.md']), ('Collaborators and review', self.docs['docs/find-help.md']), ('Research', '/research/'), ('Topics', '/topics/'), ('Resources', '/resources/'), ('Tools and skills', '/tools/'), ('Publish and record', self.docs['publications/publish.md']), ('Standards', self.docs['governance/contribution-standards.md'])]
            if chinese:
                items = [('中文首页', '/zh-hans/'), ('研究入门', '/zh-hans/start/'), ('参与方式', '/zh-hans/contribute/'), ('贡献规范', self.docs['translations/zh-Hans/governance/contribution-standards.md'])]
            aside = '<aside class="guide-sidebar"><details open><summary>' + ('指南' if chinese else 'Guides') + '</summary><nav aria-label="Guide navigation">' + ''.join(link(label, url) for label, url in items) + '</nav></details></aside>'
            content = f'<div class="document-layout">{aside}<article class="document">{content}<p class="source-note">{source_note}</p></article></div>'
        name = escape(title + ' · OSRI' if title != 'Open Source Research Initiative' else title)
        if description is None:
            first = re.search(r'<p(?: [^>]*)?>(.*?)</p>', content, re.S)
            description = title + ': ' + (plain(first[1]) if first else 'Research, collaboration and open methods from OSRI.')
        description = escape(description[:220], quote=True)
        body_class = ('home' if home else 'content-page') + (' chinese' if chinese else '')
        return f'''<!doctype html>
<html lang="{'zh-Hans' if chinese else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="{description}"><title>{name}</title><link rel="icon" href="/assets/images/logo-symbol.svg" type="image/svg+xml"><link rel="preload" href="/assets/fonts/Inter-Regular.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/site.css"><meta property="og:title" content="{name}"><meta property="og:description" content="{description}"><meta property="og:type" content="website"><meta property="og:image" content="{ORIGIN}/assets/images/social-org.png"><meta name="twitter:card" content="summary_large_image"><script type="module" src="/site.js"></script></head>
<body class="{body_class}"><a class="skip-link" href="#main">{'跳到正文' if chinese else 'Skip to content'}</a>
<header class="site-header wrap"><a class="brand" href="/" aria-label="OSRI home"><img src="/assets/images/logo-symbol.svg" alt="" width="36" height="40"><span><strong>OSRI</strong><span>Open Source Research Initiative</span></span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-menu" hidden>Menu <span aria-hidden="true">☰</span></button><div class="header-links" id="primary-menu"><nav class="site-nav" aria-label="Primary navigation">{navigation}</nav><div class="header-tools">{link('Search', '/search/')}<details class="language-control"><summary>Language</summary><div>{language}</div></details>{link('Collaborate ↗', '/contribute/', class_='button primary')}</div></div></header>
<main id="main" class="wrap" tabindex="-1">{content}</main>
<footer class="site-footer wrap"><div><strong>Open Source Research Initiative</strong><span>{source_note}</span></div><nav aria-label="Secondary navigation">{link('Publications', '/publications/')}{link('Activity', '/activity/')}{link('GitHub ↗', GITHUB)}{link('Discussions ↗', FORUM)}{link('Licensing', self.docs['LICENSE.md'])}{language}</nav></footer></body></html>'''

    def write(self, url, text):
        path = self.output / url.strip('/') / 'index.html' if url.endswith('/') else self.output / url.lstrip('/')
        path.parent.mkdir(parents=True, exist_ok=True)
        canonical = ORIGIN + ('/' + url.lstrip('/'))
        text = text.replace('</head>', f'<link rel="canonical" href="{canonical}"><meta property="og:url" content="{canonical}"></head>')
        path.write_text(text, encoding='utf-8')
        self.pages.add(url)
        if url not in {'/search/', '404.html'}:
            title = plain(re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)[1])
            main = re.search(r'<main[^>]*>(.*?)</main>', text, re.S)[1]
            kind = 'project' if url.startswith('/research/') and url != '/research/' else 'publication' if url == '/publications/' else 'resource' if url in {'/resources/', '/tools/', '/simulation-lab/'} else 'topic' if url == '/topics/' else 'guide'
            self.add_search(url, title, kind, plain(main))

    def add_search(self, url, title, kind, text):
        self.search_records[url] = {'url': url, 'title': title, 'type': kind, 'text': text}

    def heading(self, label, title, text):
        return f'<header class="page-intro"><p class="eyebrow">{escape(label)}</p><h1>{escape(title)}</h1><p>{escape(text)}</p></header>'

    def filters(self, placeholder, options=None, area_label="Listed area", all_label="All areas"):
        field = '<label>Search<input type="search" name="search" placeholder="' + escape(placeholder, quote=True) + '"></label>'
        if options:
            field += '<label>' + escape(area_label) + '<select name="area"><option value="">' + escape(all_label) + '</option>' + "".join(f'<option value="{escape(value, quote=True)}">{escape(value)}</option>' for value in options) + "</select></label>"
        return f'<form class="filters" role="search">{field}<p class="filter-count" role="status" aria-live="polite"></p></form>'

    def render_home(self):
        self.write('/', self.layout('Open Source Research Initiative', render.home(self), home=True, description='Explore OSRI research, meet the people directing it and find a bounded contribution across six research areas.'))

    def render_project_pages(self):
        for row in self.projects:
            if row['project_id'] in self.summaries:
                self.write(render.project_url(row['project_id']), self.layout(row['title'], render.project(self, row), active='/research/', source='projects/summaries.json', description=self.summaries[row['project_id']]['summary']))

    def render_search(self):
        records = sorted(self.search_records.values(), key=lambda row: (row['type'], row['title']))
        options = ''.join(f'<option value="{kind}">{label}</option>' for kind, label in [('project', 'Projects'), ('topic', 'Topics'), ('resource', 'Resources'), ('guide', 'Guides'), ('publication', 'Publications')])
        body = self.heading('Search', 'Follow your question.', 'Search projects, topics, resources, guides and publication records.')
        body += '<section data-site-search><form class="search-form" role="search" action="/search/" method="get"><label for="site-query">Search OSRI</label><div class="query-row"><input id="site-query" name="q" type="search" placeholder="Try Medical XR or source review"><button class="button primary" type="submit">Search</button></div><div class="search-options"><label for="search-type">Content type</label><select id="search-type" name="type"><option value="">All content</option>' + options + '</select><button type="reset" class="button">Clear / reset</button></div></form><noscript><p class="notice">Interactive search needs JavaScript. All indexed records are listed below; use your browser’s Find command or follow a category link.</p></noscript><p id="search-count" role="status" aria-live="polite">' + str(len(records)) + ' results · all content</p><div id="search-results" class="search-results">'
        for row in records:
            body += '<article><p class="eyebrow">' + row['type'] + '</p><h2>' + link(row['title'], row['url']) + '</h2><p>' + escape(row['text'][:200]) + '…</p></article>'
        body += '</div><div id="search-empty" class="empty-state" hidden><h2>No matching results</h2><p>Try fewer words, another content type, or clear the search.</p><div class="text-actions">' + link('Explore research', '/research/') + link('Find a guide', '/guides/') + link('Ask in Q&A ↗', FORUM + '/new?category=q-a') + '</div></div></section>'
        (self.output / 'search-index.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
        self.write('/search/', self.layout('Search OSRI', body, source='site/build.py', description='Search OSRI projects, topics, resources, guides and publications. Filter by content type and share your search URL.'))

    def render_research(self):
        body = self.heading("Research", "Find a study", "Open a research repository to read the question, inspect the work, or find a task. Browse research areas below.")
        body += '<section class="record-section" id="research-repositories"><h2>Research repositories</h2><p>Each study has one repository, named after its paper or working title. Read its README for the question and current state, open Issues for tasks, and use Pull requests to propose changes.</p>'
        if self.projects:
            body += '<div class="project-grid">' + ''.join(render.project_card(self, row) for row in self.projects) + '</div>'
        else:
            body += '<p>No research repositories are registered yet. Existing work can join when its lead is ready.</p><div class="text-actions">' + link('Offer help in Q&A', FORUM + '/new?category=q-a') + link('Try a first source comparison', '/start/#a-first-task-without-code') + '</div>'
        body += '</section><section><h2>Research areas</h2><div class="research-grid">' + "".join(f'<article class="area {color}"><h3>{link(name, self.docs[f"areas/{slug}.md"])}</h3><p>{escape(text)}</p></article>' for (slug, name, text), color in zip(AREAS, ["lavender", "mint", "teal", "gold", "coral", "blue"])) + "</div>"
        body += f'<div class="text-actions">{link("Explore candidate topics", "/topics/")}{link("Bring an existing study", self.docs["projects/README.md"] + "#bring-an-existing-project")}{link("Publication goals and records", "/publications/")}</div></section>'
        body += '<div class="programs"><section class="program simulation"><h2>OSRI Simulation Lab</h2><p>Open-source tools, examples from published research, and runnable teaching code across research areas.</p>' + link("Explore the Simulation Lab", "/simulation-lab/") + '</section><section class="program practice"><h2>Research practice and meta-research</h2><p>Administrators study and improve research methods, evidence quality, reproducibility, and collaboration.</p>' + link("Read the shared responsibilities", self.docs["meta-research/README.md"]) + "</section></div>"
        self.write("/research/", self.layout("Research", body, active="/research/"))

    def render_resources(self):
        rows = read_csv("resources/resources.csv")
        areas = sorted({value.strip() for row in rows for value in row["areas"].split(";")})
        body = self.heading("Resources", "Find the material you need", "Public data, literature services, research software, and access routes. Read each resource's terms and review notes before use.")
        body += '<div class="text-actions">' + link("Request a resource", self.docs["governance/resource-requests.md"]) + link("Simulation Lab", "/simulation-lab/") + link("Tools and research skills", "/tools/") + link("Download the catalog (CSV)", "/data/resources-resources.csv") + "</div>"
        body += '<section data-filter>' + self.filters("Search resources, formats, or uses", areas) + '<div class="record-list">'
        for row in rows:
            self.add_search('/resources/#' + row['id'].lower(), row['name'], 'resource', ' '.join(row.values()))
            searchable = " ".join(row.values())
            body += f'<article id="{escape(row["id"].lower(), quote=True)}" data-filter-item data-search="{escape(searchable, quote=True)}" data-area="{escape(row["areas"], quote=True)}"><p class="eyebrow">{escape(row["id"])} · {escape(row["areas"])}</p><h2>{link(row["name"], row["official_url"])}</h2><p>{escape(row["purpose"])}</p><div class="text-actions">{link("Documentation", row["api_or_docs_url"])}{link("Terms", row["license_or_terms_url"])}</div><details><summary>Access, formats, and review notes</summary><dl>'
            for label, key in [("Access", "access_model"), ("Account or key", "account_or_key"), ("Terms", "license_or_terms"), ("Exchange formats", "exchange_formats"), ("Catalog assessment", "assessment_status"), ("Checked", "checked_date"), ("Notes", "notes")]:
                body += f'<dt>{label}</dt><dd>{escape(row[key])}</dd>'
            body += "</dl></details></article>"
        body += '</div><p class="filter-empty" hidden>No resources match. Try another term or area.</p></section>'
        self.write("/resources/", self.layout("Resources", body, active="/resources/", source="resources/README.md"))

    def render_topics(self):
        rows = read_csv("topics/example-topics.csv")
        body = self.heading("Research topics", "A place to start thinking", "These candidate questions need further scoping, evidence checks, and novelty assessment. Refine one with collaborators before treating it as a research gap.")
        body += '<div class="text-actions">' + link("How to choose a topic", self.docs["topics/README.md"]) + link("Download CSV", "/data/topics-example-topics.csv") + link("Propose a question ↗", FORUM + "/new?category=ideas") + "</div>"
        body += '<section data-filter>' + self.filters("Search topics or methods", sorted({row["area"] for row in rows})) + '<div class="record-list">'
        for row in rows:
            self.add_search('/topics/#' + row['topic_id'].lower(), row['question'], 'topic', ' '.join(row.values()))
            body += f'<article id="{escape(row["topic_id"].lower(), quote=True)}" data-filter-item data-search="{escape(" ".join(row.values()), quote=True)}" data-area="{escape(row["area"], quote=True)}"><p class="eyebrow">{escape(row["topic_id"])} · {escape(row["area"])}</p><h2>{escape(row["question"])}</h2><p>{escape(row["initial_approach"])}</p><details><summary>Feasibility, contribution, and example paper</summary><dl>'
            for label, key in [("Access and feasibility", "access_and_feasibility"), ("Skills and compute", "skills_and_compute"), ("Contribution to test", "contribution_to_test"), ("Evidence limits", "evidence_qualification")]:
                body += f'<dt>{label}</dt><dd>{escape(row[key])}</dd>'
            body += '</dl><p>' + link(row["official_source"], row["source_url"]) + '</p><p>Example paper: ' + link(row["example_paper_title"], row["example_paper_url"]) + f' ({escape(row["example_paper_year"])}).</p><p class="small">{escape(row["reference_verification"])}</p></details></article>'
        body += '</div><p class="filter-empty" hidden>No topics match. Try another term or area.</p></section>'
        self.write("/topics/", self.layout("Research topics", body, active="/research/"))

    def render_simulation(self):
        tools = read_csv("simulation-lab/tools.csv")
        papers = {row["id"]: row for row in read_csv("simulation-lab/papers.csv")}
        examples = {row["example_id"]: row for row in read_csv("simulation-lab/examples.csv")}
        research_routes = {row["tool_id"]: row for row in json.loads((HUB / "simulation-lab/research/routes.json").read_text())["records"]}
        executed = sum(row["status"] in {"executed_adaptation", "executed_author_code", "published_target_compared"} for row in examples.values())
        status = runpy.run_path(str(HUB / "simulation-lab/catalog.py"), run_name="osri_lab")["STATUS"]
        body = self.heading("Simulation Lab", "Learn from a model. Run an experiment.", f"Explore {len(tools)} tools and {len(examples)} examples linked to published research, from robot learning and battery physics to markets, household saving, and public policy.")
        body += '<div class="text-actions">' + link("Browse tools", "#tool-catalog") + link("Run the CPU examples", self.docs["simulation-lab/examples/cpu-walkthroughs.md"]) + link("Read the lab guide", self.docs["simulation-lab/README.md"]) + link("Research routes for all 60 tools", self.docs["simulation-lab/research/README.md"]) + link("Candidate reproduction results", self.docs["simulation-lab/reproductions/README.md"]) + '</div>'
        body += f'<section class="record-section" id="literature-examples"><h2>Start with a published example</h2><p>{executed} examples have recorded executions. Each comparison states the selected paper target, measured output, and remaining limits. Other routes point to inspected upstream instructions. Each guide explains its relationship to the paper.</p><div class="guide-list">'
        for row in examples.values():
            guide = self.rewrite(row["guide"], "simulation-lab/README.md")
            body += f'<article><h3>{link(row["title"], guide)}</h3><p class="small">{escape(row["relationship"])}</p><p class="small">{escape(status[row["status"]])}</p></article>'
        body += '</div><div class="text-actions">' + link("Bibliography and reading status", self.docs["simulation-lab/bibliography.md"]) + link("What was verified", self.docs["simulation-lab/verification.md"]) + '</div></section>'
        body += '<section id="tool-catalog" data-filter><h2>Find a tool</h2><p>A growing inventory of solvers, modeling frameworks, and scene tools. Licenses below describe the source; runtime, data, and asset terms can differ.</p>'
        body += self.filters("Search tools, methods, or licenses", sorted({row["domain"] for row in tools}), "Domain", "All domains") + '<div class="record-list">'
        for row in tools:
            self.add_search("/simulation-lab/#" + row["tool_id"], row["name"], "resource", " ".join(row.values()))
            body += f'<article id="{escape(row["tool_id"], quote=True)}" data-filter-item data-search="{escape(" ".join(row.values()), quote=True)}" data-area="{escape(row["domain"], quote=True)}"><p class="eyebrow">{escape(row["domain"])}</p><h3>{escape(row["name"])}</h3><p>{escape(row["role"])}</p><p class="small">{escape(row["license_summary"])}</p><div class="text-actions">{link("Source", row["source_url"])}{link("Documentation", row["docs_url"])}{link("License", row["license_url"])}</div><details><summary>Literature, examples, and requirements</summary><p>{escape(row["dependency_notes"])}</p>'
            if row["paper_ids"]:
                body += '<p>Literature: ' + "; ".join(link(papers[key]["title"], self.docs["simulation-lab/bibliography.md"] + "#" + key) for key in row["paper_ids"].split(";")) + '</p>'
            else:
                body += '<p>See the construction route below for a candidate paper and its source assessment.</p>'
            if row["example_ids"]:
                body += '<ul>' + "".join('<li>' + link(examples[key]["title"], self.rewrite(examples[key]["guide"], "simulation-lab/README.md")) + ' — ' + escape(status[examples[key]["status"]]) + '</li>' for key in row["example_ids"].split(";")) + '</ul>'
            else:
                body += '<p>No OSRI walkthrough yet; start with the official documentation.</p>'
            route = research_routes[row["tool_id"]]
            body += '<p>Paper-to-code construction: ' + link(route["paper"]["title"], self.docs["simulation-lab/research/" + route["group"] + ".md"] + "#" + row["tool_id"]) + '</p>'
            body += f'<p class="small">Source checked {escape(row["checked_date"])}; {escape(row["source_status"].replace("_", " "))}.</p></details></article>'
        body += '</div><p class="filter-empty" hidden>No tools match. Try another term or domain.</p></section><div class="text-actions">' + link("Download tools (CSV)", "/data/simulation-lab-tools.csv") + link("Download examples (CSV)", "/data/simulation-lab-examples.csv") + link("Add a tool or example", self.docs["simulation-lab/contributing.md"]) + '</div>'
        self.write("/simulation-lab/", self.layout("Simulation Lab", body, active="/simulation-lab/", source="simulation-lab/README.md"))

    def render_tools(self):
        body = self.heading("Tools and skills", "Choose tools for the task", "Use your own agents, selected skills, or manual methods. Record versions and actual checks. This catalog is optional.")
        body += '<div class="text-actions">' + link("Tool selection and assessment", self.docs["tooling/README.md"]) + link("Download CSV", "/data/tooling-research-tools.csv") + '</div><div class="record-list">'
        for row in read_csv("tooling/research-tools.csv"):
            self.add_search('/tools/#' + row['tool_id'].lower(), row['name'], 'resource', ' '.join(row.values()))
            urls = [value.strip() for value in row["official_sources"].split(";")]
            body += f'<article id="{escape(row["tool_id"].lower())}"><p class="eyebrow">{escape(row["tool_id"])} · {escape(row["kind"])}</p><h2>{link(row["name"], urls[0])}</h2><p>{escape(row["role"])}</p><details><summary>Cost, compatibility, and assessment</summary><dl>'
            for label, key in [("Cost and access", "cost_and_access"), ("Terms", "license_or_terms"), ("Inputs and outputs", "open_inputs_outputs"), ("Version reference", "version_reference"), ("Assessment", "assessment_status"), ("Scope and limits", "assessment_scope_and_limits"), ("Portability", "portability_and_dependencies")]:
                body += f'<dt>{label}</dt><dd>{escape(row[key])}</dd>'
            body += "</dl></details></article>"
        body += "</div>"
        self.write("/tools/", self.layout("Tools and skills", body, source="tooling/README.md"))

    def render_publications(self):
        body = self.heading("Publications", "Share and build on the work", "Journal articles, full conference papers, preprints, and substantive research blogs or technical essays. Output type and peer-review status are recorded separately.")
        body += '<div class="text-actions">' + link("Publish and record your research", self.docs["publications/publish.md"]) + link("Counting rules", self.docs["publications/README.md"]) + link("Recorded totals", "/activity/#publication-outputs") + link("Share an output ↗", FORUM + "/categories/show-and-tell") + "</div>"
        rows = [row for row in read_csv("publications/publications.csv") if row["status"] == "published"]
        if rows:
            body += '<div class="record-list">' + "".join(f'<article id="{escape(row["publication_id"].lower())}"><p class="eyebrow">{escape(row["publication_type"])} · {escape(row["peer_review_status"])}</p><h2>{link(row["title"], row["url"])}</h2><p>{escape(row["authors"])}</p><p>{escape(row["first_published_date"])} · Work {escape(row["work_id"])}</p></article>' for row in rows) + "</div>"
        else:
            body += '<section class="empty-state"><h2>No public outputs are registered yet</h2><p>This directory covers OSRI records. It does not describe every contributor\'s existing research.</p>' + link("Bring an existing project", self.docs["projects/README.md"] + "#bring-an-existing-project") + "</section>"
        for row in rows:
            self.add_search('/publications/#' + row['publication_id'].lower(), row['title'], 'publication', ' '.join(row.values()))
        self.write("/publications/", self.layout("Publications", body, active="/research/"))

    def render_guides(self):
        body = self.heading("Guides", "Read, contribute, and keep the evidence", "Start with a small task. Use the detailed guides when your work needs them.")
        first = ["START_HERE.md", "CONTRIBUTING.md", "docs/browser-setup.md", "docs/find-help.md", "topics/README.md", "resources/README.md", "tooling/workflows.md", "publications/publish.md", "publications/README.md"]
        remaining = [path for path in self.docs if path not in first and not path.startswith("translations/") and path not in {"README.md", "community/ACTIVITY.md"}]
        body += '<section data-filter>' + self.filters("Search guides")
        for label, paths in [("Follow the research path", first), ("Reference guides", remaining)]:
            body += f'<h2 class="guide-group-title">{label}</h2><div class="guide-list">'
            for path in paths:
                text = (HUB / path).read_text()
                title = title_of(text, Path(path).stem)
                body += f'<article data-filter-item data-search="{escape(title + " " + path + " " + text[:700], quote=True)}"><h3>{link(title, self.docs[path])}</h3><p class="small">{escape(path.split("/")[0].replace(".md", "").replace("_", " "))}</p></article>'
            body += '</div>'
        body += '<p class="filter-empty" hidden>No guides match. Try another term.</p></section>'
        self.write("/guides/", self.layout("Guides", body, active="/guides/"))

    def assets(self):
        shutil.copytree(SITE / "assets", self.output / "assets", dirs_exist_ok=True)
        for name in ["styles.css", "site.css", "site.js", "search.js"]:
            shutil.copy2(SITE / name, self.output / name)
        shutil.copy2(HUB / "identity/prism/previews/social-org.png", self.output / "assets/images/social-org.png")
        data_paths = ["resources/resources.csv", "topics/example-topics.csv", "tooling/research-tools.csv", "projects/projects.csv", "publications/publications.csv", "community/contributions.csv", "translations/status.csv", "simulation-lab/tools.csv", "simulation-lab/papers.csv", "simulation-lab/examples.csv", "simulation-lab/research/routes.csv"]
        data_paths += [path.relative_to(HUB).as_posix() for path in sorted((HUB / "simulation-lab/research/verification").glob("*.csv"))]
        data_paths += [path.relative_to(HUB).as_posix() for path in sorted((HUB / "simulation-lab/reproductions").rglob("*.csv"))]
        for path in data_paths:
            destination = self.output / "data" / path.replace("/", "-")
            destination.parent.mkdir(exist_ok=True)
            shutil.copy2(HUB / path, destination)
        shutil.copytree(HUB / "LICENSES", self.output / "licenses", dirs_exist_ok=True)
        from fontTools.ttLib import TTFont
        for filename in ['Inter-Regular', 'Inter-Bold', 'IBMPlexMono-Regular']:
            font = TTFont(SITE / 'assets/fonts' / (filename + '.ttf'), recalcTimestamp=False)
            font.flavor = 'woff2'
            font.save(self.output / 'assets/fonts' / (filename + '.woff2'))
        self.chinese_font()
        identity = self.output / 'assets/identity'
        identity.mkdir(exist_ok=True)
        for path in (HUB / 'identity/prism/sources').glob('*.svg'):
            # Embedded font files are resolved inside SVG image documents too.
            import base64
            vector = path.read_text()
            def embed_font(match):
                font = HUB / 'identity/prism/fonts' / match[1]
                if not font.is_file():
                    raise ValueError('Missing SVG font: ' + str(font))
                return "url('data:font/ttf;base64," + base64.b64encode(font.read_bytes()).decode() + "')"
            vector = re.sub(r"url\('\.\./fonts/([^']+)'\)", embed_font, vector)
            (identity / path.name).write_text(vector)

    def chinese_font(self):
        from fontTools import subset
        from fontTools.ttLib import TTFont
        characters = "本页内容指南开始参与研究英文资源记录讨论中文首页入门贡献规范申请写作翻译视觉识别跳到正文在查看原文简体待审核"
        characters += "".join((HUB / source).read_text() for source in self.docs if source.startswith("translations/zh-Hans/"))
        options = subset.Options()
        options.flavor = "woff2"
        options.recalc_timestamp = False
        font = TTFont(HUB / "identity/shared-language/fonts/NotoSansCJKSC-Regular.woff2", recalcTimestamp=False)
        worker = subset.Subsetter(options=options)
        worker.populate(text=characters)
        worker.subset(font)
        names = {1: "OSRI Research Chinese", 2: "Regular", 3: "OSRI Research Chinese 1", 4: "OSRI Research Chinese", 6: "OSRIResearchChinese-Regular", 16: "OSRI Research Chinese", 17: "Regular"}
        for entry in font["name"].names:
            if entry.nameID in names:
                entry.string = names[entry.nameID].encode(entry.getEncoding())
        font.flavor = "woff2"
        output = self.output / "assets/fonts/OSRI-Research-Chinese.woff2"
        font.save(output)
        coverage = TTFont(output).getBestCmap()
        missing = {character for character in characters if '\u3400' <= character <= '\u9fff' and ord(character) not in coverage}
        if missing:
            raise ValueError("Chinese font is missing: " + "".join(sorted(missing)))
        shutil.copy2(HUB / "identity/shared-language/fonts/NOTO-CJK-SC-OFL.txt", self.output / "assets/fonts/NOTO-RESEARCH-CJK-OFL.txt")

    def build(self):
        subprocess.run([sys.executable, str(HUB / "simulation-lab/catalog.py")], check=True)
        self.output.mkdir(parents=True, exist_ok=False)
        self.assets()
        activity = runpy.run_path(str(HUB / "community/update.py"), run_name="osri_activity")
        for path, url in self.docs.items():
            text = activity["build"](HUB) if path == "community/ACTIVITY.md" else (HUB / path).read_text()
            title = title_of(text, Path(path).stem)
            if not re.search(r"^# ", text, re.M):
                text = f"# {title}\n\n{text}"
            self.write(url, self.layout(title, self.markdown(text, path), active=url, source=path, chinese=path.startswith("translations/zh-Hans/"), document=True))
        original_contribution = self.markdown((HUB / 'CONTRIBUTING.md').read_text(), 'CONTRIBUTING.md')
        original_contribution = re.sub(r'<h1(.*?)>(.*?)</h1>', r'<h2\1>\2</h2>', original_contribution, count=1)
        collaboration = render.collaborate(self) + '<details class="contribution-details"><summary>Full contribution guide</summary><div class="document">' + original_contribution + '</div></details>'
        self.write('/contribute/', self.layout('Collaborate', collaboration, source='CONTRIBUTING.md', description='Contribute domain review, evidence work, data, code, writing or translation to OSRI. Find a task, guide or conversation.'))
        self.write('/about/', self.layout('About OSRI', render.about(self), active='/about/', source='governance/contribution-standards.md', description='OSRI’s mission, founder and initial administrator Cole / @ajhcs, human-directed research and project structure.'))
        self.render_project_pages()
        self.render_home()
        self.render_research()
        self.render_resources()
        self.render_topics()
        self.render_simulation()
        self.render_tools()
        self.render_publications()
        self.render_guides()
        self.render_search()
        self.write("404.html", self.layout("Page not found", self.heading("404", "Page not found", "Use the guides or return to the home page.") + '<div class="text-actions">' + link("Home", "/") + link("Find a guide", "/guides/") + "</div>"))
        (self.output / ".nojekyll").write_text("")
        (self.output / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n")
        (self.output / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{ORIGIN}{escape(url)}</loc></url>" for url in sorted(self.pages) if url.endswith("/")) + "</urlset>")
        (self.output / "build-info.json").write_text(json.dumps({"source_repository": f"{GITHUB}/osri", "source_commit": self.commit, "source_snapshot": self.snapshot, "pages": sorted(self.pages), "guides": len(self.docs), "resources": len(read_csv("resources/resources.csv")), "topics": len(read_csv("topics/example-topics.csv")), "simulation_tools": len(read_csv("simulation-lab/tools.csv")), "simulation_examples": len(read_csv("simulation-lab/examples.csv")), "simulation_papers": len(read_csv("simulation-lab/papers.csv")), "project_summaries": len(self.summaries), "publication_targets": len(self.targets), "search_records": len(self.search_records), "search_urls": sorted(self.search_records)}, indent=2) + "\n")
        print(f"Built {len(self.pages)} pages from hub {self.commit[:12]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="A new output directory")
    args = parser.parse_args()
    Website(args.output.resolve()).build()


if __name__ == "__main__":
    main()
