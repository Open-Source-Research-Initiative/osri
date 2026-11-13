#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build OSRI's public website from this hub's Markdown and CSV records."""

import argparse
import csv
from datetime import datetime
from html import escape
import json
from pathlib import Path, PurePosixPath
import re
import runpy
import shutil
import subprocess
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

HUB = Path(__file__).resolve().parents[1]
SITE = HUB / "site"
ORIGIN = "https://open-source-research-initiative.github.io"
GITHUB = "https://github.com/Open-Source-Research-Initiative"
FORUM = "https://github.com/orgs/Open-Source-Research-Initiative/discussions"
ALIASES = {"START_HERE.md": "/start/", "CONTRIBUTING.md": "/contribute/", "community/ACTIVITY.md": "/activity/", "README.md": "/guides/osri/"}
NAV = [("Start here", "/start/"), ("Research", "/research/"), ("Contribute", "/contribute/"), ("Resources", "/resources/"), ("Activity", "/activity/"), ("Guides", "/guides/"), ("Discussions ↗", FORUM)]
AREAS = [("healthcare", "Healthcare", "Nonclinical public health and health systems research."), ("engineering", "Engineering", "Systems Engineering, Engineering Management, Operations Research, and Decision Science. Initial work excludes physical laboratory experiments."), ("informatics", "Informatics", "Bioinformatics, information systems, and Computational Natural Sciences. Initial work excludes physical laboratory experiments."), ("economics", "Economics", "Resources, incentives, public economics, research, and innovation."), ("social-behavioral-sciences", "Social and Behavioral Sciences", "Judgment, collaboration, organizations, and behavior."), ("public-policy", "Public Policy", "Policy analysis, evaluation, institutions, and governance.")]


def read_csv(path):
    with (HUB / path).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def href(url):
    if urlsplit(url).scheme not in {"", "http", "https", "mailto"}:
        raise ValueError(f"Unsupported link scheme: {url}")
    return escape(url, quote=True)


def link(label, url, **attributes):
    attrs = "".join(f' {key.rstrip("_").replace("_", "-")}="{escape(str(value), quote=True)}"' for key, value in attributes.items())
    return f'<a href="{href(url)}"{attrs}>{escape(label)}</a>'


def route(path):
    if path in ALIASES:
        return ALIASES[path]
    if path.startswith("translations/zh-Hans/"):
        tail = path.removeprefix("translations/zh-Hans/")
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


class Website:
    def __init__(self, output):
        self.output = output
        self.commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=HUB, text=True).strip()
        self.snapshot = subprocess.check_output(["git", "show", "-s", "--format=%cI", "HEAD"], cwd=HUB, text=True).strip()
        candidates = []
        for path in sorted(HUB.rglob("*.md")):
            rel = path.relative_to(HUB).as_posix()
            if rel.startswith((".git/", ".github/", "site/", "identity/")) and rel != "identity/prism/research-journey.md":
                continue
            candidates.append(rel)
        self.docs = {rel: route(rel) for rel in candidates}
        if len(set(self.docs.values())) != len(self.docs):
            raise ValueError("Duplicate documentation routes")
        self.pages = set()

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
        return parser.renderer.render(tokens, parser.options, {})

    def layout(self, title, content, active="", source=None, chinese=False, document=False, home=False):
        nav = NAV
        if chinese:
            nav = [("开始", "/zh-hans/start/"), ("参与", "/zh-hans/contribute/"), ("研究（英文）", "/research/"), ("资源（英文）", "/resources/"), ("记录（英文）", "/activity/"), ("讨论 ↗", FORUM)]
        navigation = "".join(link(label, url, aria_current="page" if url == active else "false") for label, url in nav)
        translated = "translations/zh-Hans/" + source if source and not source.startswith("translations/") else None
        other = self.docs.get(translated, "/zh-hans/") if not chinese else self.docs.get(source.removeprefix("translations/zh-Hans/"), "/")
        if chinese and source == "translations/zh-Hans/README.md":
            other = "/"
        language = link("简体中文 · 待审核" if not chinese else "English", other, lang="zh-Hans" if not chinese else "en")
        source_note = link("View source on GitHub" if not chinese else "在 GitHub 查看原文", self.source_url(source)) if source else link("Source hub", f"{GITHUB}/osri")
        aside = ""
        if document:
            items = [("Research guide", "/start/"), ("Ways to contribute", "/contribute/"), ("Browser setup", self.docs["docs/browser-setup.md"]), ("Collaborators and review", self.docs["docs/find-help.md"]), ("Research areas", "/research/"), ("Topics to explore", "/topics/"), ("Resources", "/resources/"), ("Tools and skills", "/tools/"), ("Publish and record", self.docs["publications/publish.md"]), ("Writing and standards", "/guides/"), ("Community activity", "/activity/")]
            if chinese:
                items = [("中文首页", "/zh-hans/"), ("研究入门", "/zh-hans/start/"), ("参与方式", "/zh-hans/contribute/"), ("浏览器入门", self.docs["translations/zh-Hans/docs/browser-setup.md"]), ("协作与评审", self.docs["translations/zh-Hans/docs/find-help.md"]), ("发表与登记", self.docs["translations/zh-Hans/publications/publish.md"]), ("贡献规范", self.docs["translations/zh-Hans/governance/contribution-standards.md"]), ("资源申请", self.docs["translations/zh-Hans/governance/resource-requests.md"]), ("写作", self.docs["translations/zh-Hans/governance/writing-style.md"]), ("翻译", self.docs["translations/zh-Hans/governance/translation.md"]), ("视觉识别", self.docs["translations/zh-Hans/governance/visual-identity.md"])]
            aside = '<aside class="guide-sidebar"><nav aria-label="Guide navigation">' + "".join(link(label, url) for label, url in items) + "</nav></aside>"
            content = f'<div class="document-layout">{aside}<article class="document">{content}<p class="source-note">{source_note}</p></article></div>'
        name = escape(title + " · OSRI" if title != "Open Source Research Initiative" else title)
        stamp = datetime.fromisoformat(self.snapshot).strftime("%d %b %Y")
        body_class = "home" if home else "content-page"
        if chinese:
            body_class += " chinese"
        return f'''<!doctype html>
<html lang="{'zh-Hans' if chinese else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="Human-driven Agentic-Powered-Research. Research guides, resources, projects, and community activity from OSRI."><title>{name}</title><link rel="icon" href="/assets/images/logo-symbol.svg" type="image/svg+xml"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/site.css"><meta property="og:title" content="{name}"><meta property="og:type" content="website"><meta property="og:image" content="{ORIGIN}/assets/images/social-org.png"><meta name="twitter:card" content="summary_large_image"><script src="/site.js" defer></script></head>
<body class="{body_class}"><a class="skip-link" href="#main">{'跳到正文' if chinese else 'Skip to content'}</a>
<header class="site-header wrap"><a class="brand" href="/" aria-label="OSRI home"><img src="/assets/images/logo-symbol.svg" alt="" width="48" height="52"><span><strong>OSRI</strong><span>Open Source Research Initiative</span></span></a><nav class="site-nav" aria-label="Primary navigation">{navigation}</nav></header>
<div class="language-bar wrap">{language}</div><main id="main" class="wrap">{content}</main>
<footer class="site-footer wrap"><div><strong>Open Source Research Initiative</strong><span>Human-driven Agentic-Powered-Research.</span><span>{source_note} · Source snapshot {stamp}</span></div><div>{link('GitHub', GITHUB)}{link('Discussions', FORUM)}{link('Licensing', self.docs['LICENSE.md'])}{language}</div></footer></body></html>'''

    def write(self, url, text):
        path = self.output / url.strip("/") / "index.html" if url.endswith("/") else self.output / url.lstrip("/")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        self.pages.add(url)

    def heading(self, label, title, text):
        return f'<header class="page-intro"><p class="eyebrow">{escape(label)}</p><h1>{escape(title)}</h1><p>{escape(text)}</p></header>'

    def filters(self, placeholder, options=None):
        field = '<label>Search<input type="search" name="search" placeholder="' + escape(placeholder, quote=True) + '"></label>'
        if options:
            field += '<label>Listed area<select name="area"><option value="">All areas</option>' + "".join(f'<option value="{escape(value, quote=True)}">{escape(value)}</option>' for value in options) + "</select></label>"
        return f'<form class="filters" role="search">{field}<p class="filter-count" role="status" aria-live="polite"></p></form>'

    def render_home(self):
        original = (SITE / "index.html").read_text()
        main = original.split('<main id="main" class="wrap">', 1)[1].split("</main>", 1)[0]
        main = main.replace('src="assets/', 'src="/assets/')
        main = main.replace('<span>Open / traceable</span>', '<div class="hero-actions">' + link("Start researching", "/start/", class_="button primary") + link("Find a way to help", "/contribute/", class_="button") + "</div>")
        main = main.replace("</p>\n  </section>\n\n  <section class=\"invitation", '</p><p class="section-link">' + link("Browse publications and counting rules", "/publications/") + '</p>\n  </section>\n\n  <section class="invitation')
        main = re.sub(r'href="(https://github.com/Open-Source-Research-Initiative/osri/blob/main/[^"]+)"', lambda match: 'href="' + href(self.rewrite(match.group(1))) + '"', main)
        main = main.replace(f'{GITHUB}/.github/discussions', FORUM)
        paths = f'<section class="explore-links"><h2>Find your next step</h2><div>{link("Find a research topic", "/topics/")}{link("Browse data and resources", "/resources/")}{link("Read the guides", "/guides/")}{link("Follow community activity", "/activity/")}</div></section>'
        self.write("/", self.layout("Open Source Research Initiative", main + paths, home=True))

    def render_research(self):
        body = self.heading("Research", "Questions across disciplines", "Start with a useful question. Connect it to existing evidence and the expertise needed to investigate it.")
        body += '<div class="research-grid">' + "".join(f'<article class="area {color}"><h2>{link(name, self.docs[f"areas/{slug}.md"])}</h2><p>{escape(text)}</p></article>' for (slug, name, text), color in zip(AREAS, ["lavender", "mint", "teal", "gold", "coral", "blue"])) + "</div>"
        body += f'<div class="text-actions">{link("Explore candidate topics", "/topics/")}{link("Bring an existing study", self.docs["projects/README.md"] + "#bring-an-existing-project")}{link("Publication goals and records", "/publications/")}</div>'
        body += '<section class="record-section"><h2>Registered projects</h2>'
        projects = read_csv("projects/projects.csv")
        if projects:
            body += '<div class="record-list">' + "".join(f'<article><p class="eyebrow">{escape(row["project_id"])}</p><h3>{link(row["title"], row["repository_url"])}</h3><p>{escape(row["areas"])}</p><p>Human lead: {escape(row["human_lead"])}</p></article>' for row in projects) + "</div>"
        else:
            body += '<p>No registered project tasks are available to select yet. Existing work can join when its lead is ready.</p><div class="text-actions">' + link("Offer help in Q&A", FORUM + "/new?category=q-a") + link("Try a first source comparison", "/start/#a-first-task-without-code") + '</div>'
        body += '</section><div class="programs"><section class="program simulation"><h2>OSRI Simulation Lab</h2><p class="status">Proposed</p><p>Computational experiments across research areas, with documented assumptions, checks, and limits.</p>' + link("Read the lab guide", self.docs["simulation-lab/README.md"]) + '</section><section class="program practice"><h2>Research practice and meta-research</h2><p>Administrators study and improve research methods, evidence quality, reproducibility, and collaboration.</p>' + link("Read the shared responsibilities", self.docs["meta-research/README.md"]) + "</section></div>"
        self.write("/research/", self.layout("Research", body, active="/research/"))

    def render_resources(self):
        rows = read_csv("resources/resources.csv")
        areas = sorted({value.strip() for row in rows for value in row["areas"].split(";")})
        body = self.heading("Resources", "Find the material you need", "Public data, literature services, research software, and access routes. Read each resource's terms and review notes before use.")
        body += '<div class="text-actions">' + link("Request a resource", self.docs["governance/resource-requests.md"]) + link("Tools and research skills", "/tools/") + link("Download the catalog (CSV)", "/data/resources-resources.csv") + "</div>"
        body += '<section data-filter>' + self.filters("Search resources, formats, or uses", areas) + '<div class="record-list">'
        for row in rows:
            searchable = " ".join(row.values())
            body += f'<article data-filter-item data-search="{escape(searchable, quote=True)}" data-area="{escape(row["areas"], quote=True)}"><p class="eyebrow">{escape(row["id"])} · {escape(row["areas"])}</p><h2>{link(row["name"], row["official_url"])}</h2><p>{escape(row["purpose"])}</p><div class="text-actions">{link("Documentation", row["api_or_docs_url"])}{link("Terms", row["license_or_terms_url"])}</div><details><summary>Access, formats, and review notes</summary><dl>'
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
            body += f'<article id="{escape(row["topic_id"].lower(), quote=True)}" data-filter-item data-search="{escape(" ".join(row.values()), quote=True)}" data-area="{escape(row["area"], quote=True)}"><p class="eyebrow">{escape(row["topic_id"])} · {escape(row["area"])}</p><h2>{escape(row["question"])}</h2><p>{escape(row["initial_approach"])}</p><details><summary>Feasibility, contribution, and example paper</summary><dl>'
            for label, key in [("Access and feasibility", "access_and_feasibility"), ("Skills and compute", "skills_and_compute"), ("Contribution to test", "contribution_to_test"), ("Evidence limits", "evidence_qualification")]:
                body += f'<dt>{label}</dt><dd>{escape(row[key])}</dd>'
            body += '</dl><p>' + link(row["official_source"], row["source_url"]) + '</p><p>Example paper: ' + link(row["example_paper_title"], row["example_paper_url"]) + f' ({escape(row["example_paper_year"])}).</p><p class="small">{escape(row["reference_verification"])}</p></details></article>'
        body += '</div><p class="filter-empty" hidden>No topics match. Try another term or area.</p></section>'
        self.write("/topics/", self.layout("Research topics", body, active="/research/"))

    def render_tools(self):
        body = self.heading("Tools and skills", "Choose tools for the task", "Use your own agents, selected skills, or manual methods. Record versions and actual checks. This catalog is optional.")
        body += '<div class="text-actions">' + link("Tool selection and assessment", self.docs["tooling/README.md"]) + link("Download CSV", "/data/tooling-research-tools.csv") + '</div><div class="record-list">'
        for row in read_csv("tooling/research-tools.csv"):
            urls = [value.strip() for value in row["official_sources"].split(";")]
            body += f'<article><p class="eyebrow">{escape(row["tool_id"])} · {escape(row["kind"])}</p><h2>{link(row["name"], urls[0])}</h2><p>{escape(row["role"])}</p><details><summary>Cost, compatibility, and assessment</summary><dl>'
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
            body += '<div class="record-list">' + "".join(f'<article><p class="eyebrow">{escape(row["publication_type"])} · {escape(row["peer_review_status"])}</p><h2>{link(row["title"], row["url"])}</h2><p>{escape(row["authors"])}</p><p>{escape(row["first_published_date"])} · Work {escape(row["work_id"])}</p></article>' for row in rows) + "</div>"
        else:
            body += '<section class="empty-state"><h2>No public outputs are registered yet</h2><p>This directory covers OSRI records. It does not describe every contributor\'s existing research.</p>' + link("Bring an existing project", self.docs["projects/README.md"] + "#bring-an-existing-project") + "</section>"
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
        for name in ["styles.css", "site.css", "site.js"]:
            shutil.copy2(SITE / name, self.output / name)
        shutil.copy2(HUB / "identity/prism/previews/social-org.png", self.output / "assets/images/social-org.png")
        for path in ["resources/resources.csv", "topics/example-topics.csv", "tooling/research-tools.csv", "projects/projects.csv", "publications/publications.csv", "community/contributions.csv", "translations/status.csv"]:
            destination = self.output / "data" / path.replace("/", "-")
            destination.parent.mkdir(exist_ok=True)
            shutil.copy2(HUB / path, destination)
        shutil.copytree(HUB / "LICENSES", self.output / "licenses", dirs_exist_ok=True)
        self.chinese_font()

    def chinese_font(self):
        from fontTools import subset
        from fontTools.ttLib import TTFont
        characters = "开始参与研究英文资源记录讨论中文首页入门贡献规范申请写作翻译视觉识别跳到正文在查看原文简体待审核"
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
        self.output.mkdir(parents=True, exist_ok=False)
        self.assets()
        activity = runpy.run_path(str(HUB / "community/update.py"), run_name="osri_activity")
        for path, url in self.docs.items():
            text = activity["build"](HUB) if path == "community/ACTIVITY.md" else (HUB / path).read_text()
            title = title_of(text, Path(path).stem)
            if not re.search(r"^# ", text, re.M):
                text = f"# {title}\n\n{text}"
            self.write(url, self.layout(title, self.markdown(text, path), active=url, source=path, chinese=path.startswith("translations/zh-Hans/"), document=True))
        self.render_home()
        self.render_research()
        self.render_resources()
        self.render_topics()
        self.render_tools()
        self.render_publications()
        self.render_guides()
        self.write("404.html", self.layout("Page not found", self.heading("404", "Page not found", "Use the guides or return to the home page.") + '<div class="text-actions">' + link("Home", "/") + link("Find a guide", "/guides/") + "</div>"))
        (self.output / ".nojekyll").write_text("")
        (self.output / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n")
        (self.output / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{ORIGIN}{escape(url)}</loc></url>" for url in sorted(self.pages) if url.endswith("/")) + "</urlset>")
        (self.output / "build-info.json").write_text(json.dumps({"source_repository": f"{GITHUB}/osri", "source_commit": self.commit, "source_snapshot": self.snapshot, "pages": sorted(self.pages), "guides": len(self.docs), "resources": len(read_csv("resources/resources.csv")), "topics": len(read_csv("topics/example-topics.csv"))}, indent=2) + "\n")
        print(f"Built {len(self.pages)} pages from hub {self.commit[:12]}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="A new output directory")
    args = parser.parse_args()
    Website(args.output.resolve()).build()


if __name__ == "__main__":
    main()
