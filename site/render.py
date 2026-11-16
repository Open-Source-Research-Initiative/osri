# SPDX-License-Identifier: MIT
"""Reusable semantic page components. Editorial records remain in Markdown/JSON/CSV."""
from html import escape
import json
from html_helpers import link
from records import STAGES, project_status


def project_url(key):
    return '/research/' + key.lower() + '/'


def status_badge(summary):
    return '<span class="status" data-activity="' + escape(summary['activity']) + '">' + escape(project_status(summary)) + '</span>'


def project_card(site, project):
    key = project['project_id']
    summary = site.summaries.get(key)
    title = summary.get('short_title', project['title']) if summary else project['title']
    status = status_badge(summary) if summary else '<span class="status">Summary pending</span>'
    text = summary['summary'] if summary else 'Read the project’s public repository for its question and current research state.'
    note = '<p class="small">' + escape(summary['hold_reason']) + '</p>' if summary and summary['activity'] == 'on_hold' else ''
    destination = project_url(key) if summary else project['repository_url']
    return f'''<article class="project-card"><div class="project-meta"><span>{escape(key)}</span>{status}</div><h3>{link(title, destination)}</h3><p>{escape(text)}</p>{note}<div class="card-bottom"><span>Human lead: {escape(project['human_lead'])}</span>{link('Explore project →', destination)}</div></article>'''


def home(site):
    cards = ''.join(project_card(site, row) for row in site.projects)
    if not cards:
        cards = '<p>No projects are registered yet. Bring a question to ' + link('Ideas', site.forum + '/new?category=ideas') + '.</p>'
    directory, _ = site.venue_snapshot()
    overview = json.loads((directory / 'build-receipt.json').read_text())['summary']
    venue_count = overview['verified_free_core_documented']
    field_options = ''.join('<option value="' + escape(f['subfield']) + '">' + escape(f['name']) + '</option>' for f in overview['coverage'])
    venue_preview = f'''<section class="home-section venue-preview" id="find-venues"><div class="section-heading"><h2>Find where your research fits.</h2>{link('Open directory →', '/venues/')}</div><p>Start with {venue_count} verified free routes with core editorial standards documented. AI use is permitted under each venue’s conditions.</p><form action="/venues/" method="get" class="venue-entry"><label>Search venues and scope<input name="query" type="search" placeholder="e.g. public health or simulation"></label><label>Research subfield<select name="subfield"><option value="">All subfields</option>{field_options}</select></label><button class="button primary" type="submit">Find venues</button></form><p class="small">Check author costs and disclosure instructions, then compare up to three venues.</p></section>'''
    areas = ''.join(f'<li>{link(name + " ↗", site.docs[f"areas/{slug}.md"])}</li>' for slug, name, _ in site.areas)
    steps = [
        ('Question', 'Frame the question; agree its scope.', '/start/'),
        ('Evidence', 'Find sources; record provenance and gaps.', '/resources/'),
        ('Analysis', 'Choose methods; inspect results and assumptions.', site.docs['tooling/workflows.md']),
        ('Human review', 'People evaluate claims and request changes.', site.docs['docs/find-help.md'] + '#request-review'),
        ('Writing', 'Connect claims, evidence, limits and credit.', site.docs['governance/writing-style.md']),
        ('Publication', 'People authorize a version for sharing.', site.docs['publications/publish.md'])
    ]
    journey = ''.join(f'<details class="journey-step" {'id="publication-title"' if i == 5 else ""} {"open" if i == 0 else ""}><summary><span class="step-number">0{i+1}</span>{escape(title)}</summary><p>{escape(text)} {link("Guide ↗", url)}</p></details>' for i, (title, text, url) in enumerate(steps))
    return f'''<section class="home-hero"><div class="hero-copy"><p class="eyebrow">Open Source Research Initiative</p><h1 id="hero-title">Research, shaped<br>by people.<br><span>Open to possibility.</span></h1><p>We bring people across fields together to develop research in the open and submit it through publication routes that are free to authors.</p><div class="hero-actions">{link('Find free publication venues', '/venues/', class_='button primary')}{link('Explore research ↗', '/research/', class_='button')}</div></div><div class="hero-art"><img class="prism-entrance" src="/assets/images/hero-prism.svg" alt="Crisp Prism facets meeting around an open diamond" width="620" height="460"><span class="art-caption">Different perspectives. Shared inquiry.</span></div></section>
{venue_preview}
<section class="home-section" id="research" data-reveal><div class="section-heading"><h2 id="research-title">Current research</h2>{link('All research →', '/research/')}</div><div class="project-grid">{cards}</div></section>
<section class="home-section areas-section" data-reveal><div class="section-heading"><h2>Six areas. Connected questions.</h2>{link('Explore topics →', '/topics/')}</div><ul class="area-links">{areas}</ul></section>
<section class="home-section" id="research-journey" data-reveal><div class="section-heading"><h2 id="methods-title">From question to contribution.</h2>{link('Research journey ↗', site.docs['identity/prism/research-journey.md'])}</div><p class="section-deck">Explore each stage. The path repeats as evidence changes. People direct the work and authorize publication.</p><div class="journey-grid">{journey}</div></section>
<section class="collaboration-banner" data-reveal><div><p class="eyebrow">Bring your perspective</p><h2 id="invitation-title">Good research takes many kinds of expertise.</h2><p>Review a source, contribute code, improve a draft or help translate. Choose a bounded task with a human lead. Use Discussions or email Cole to agree a next step.</p></div>{link('Find your contribution ↗', '/contribute/', class_='button primary')}</section>'''


def venue_demo(site, title, guide):
    body = site.heading('Directory walkthrough', title, 'Choose a field, inspect costs and AI disclosure, then save a comparison.')
    body += '<video controls preload="metadata" playsinline width="1280" style="max-width:100%;height:auto" poster="/assets/demos/venue-directory-poster.jpg" aria-label="Captioned OSRI venue-directory walkthrough"><source src="/assets/demos/venue-directory-demo.webm" type="video/webm"><track kind="captions" src="/assets/demos/venue-directory-demo.vtt" srclang="en" label="English">Your browser cannot play this video. Follow the written walkthrough below.</video>'
    return body + site.markdown(guide, 'docs/venue-directory-demo.md')


def collaborate(site):
    routes = [
        ('01', 'Domain review', 'Check the interpretation and limits of a research claim.', site.docs['docs/find-help.md'] + '#request-review', 'Request or offer review'),
        ('02', 'Evidence work', 'Find a research project and agree a bounded source-check task with its human lead.', '/research/', 'Find research tasks'),
        ('03', 'Data and code', 'Agree a small data, analysis or reproducibility task in Q&A.', site.forum + '/new?category=q-a', 'Offer data or code help'),
        ('04', 'Writing', 'Make a claim clearer and keep its supporting evidence traceable.', site.docs['governance/writing-style.md'], 'Read the writing guide'),
        ('05', 'Translation', 'Help review a draft translation or propose another language.', site.docs['governance/translation.md'], 'Read the translation guide')
    ]
    body = site.heading('Collaborate', 'Bring what you know.', 'Choose a route, agree a bounded task and keep a person responsible. A browser is enough to begin.')
    body += '<section class="contact-panel" id="venue-tasks"><h2>Help improve the venue directory</h2><p>Try a shortlist, check an author-cost or AI policy, or trace one source. Six starter tasks take about 10–30 minutes for a first attempt. Submit a short note; maintainers handle data-file changes. No code or installation is required.</p><div class="text-actions">' + link('Choose a starter task', site.docs['community/venue-starter-tasks.md'], class_='button primary') + link('Report a source or correction ↗', 'https://github.com/Open-Source-Research-Initiative/free-publication-directory/issues/new?template=venue-evidence.yml') + link('Try the walkthrough', site.docs['docs/venue-directory-demo.md']) + '</div><p class="small">Comment to volunteer; Cole / @ajhcs confirms the claim and reviews acceptance. Public credit is optional. Without a GitHub account, ' + link('email Cole', 'mailto:cole.lyons@pennmedicine.upenn.edu?subject=OSRI%20venue%20directory%20task') + '.</p></section>'
    body += '<div class="collaboration-grid">' + ''.join(f'<article><span class="eyebrow">{number}</span><h2>{escape(title)}</h2><p>{escape(text)}</p>{link(action + " ↗", url)}</article>' for number, title, text, url, action in routes) + '</div>'
    body += '<section class="home-section"><h2>Research tasks</h2>'
    for project in site.projects:
        summary = site.summaries.get(project['project_id'])
        if summary:
            body += project_card(site, project)
            body += '<p>' + escape(summary['contribution']['summary']) + ' ' + link(summary['contribution']['title'] + ' ↗', summary['contribution']['url']) + '</p>'
    body += '</section>'
    body += '<section class="contact-panel"><h2>Start a conversation</h2><p>Use GitHub Discussions for public questions and offers of help. For private matters, email Cole.</p><div class="text-actions">' + link('Open Q&A ↗', site.forum + '/new?category=q-a') + link('Email Cole ↗', 'mailto:cole.lyons@pennmedicine.upenn.edu') + link('Full contribution guide', '/guides/contributing/') + '</div></section>'
    return body


def about(site):
    body = site.heading('About OSRI', 'Shared questions.<br>Human direction.'.replace('<br>', ' '), 'Open Source Research Initiative brings people across fields together to conduct human-driven Agentic-Powered-Research.')
    body += '<p>OSRI helps people develop research and submit it through credible publication routes that are free to authors. The ' + link('venue directory', '/venues/') + ' records fee evidence, conditions, and comparisons within research subfields.</p>'
    body += '<div class="about-grid"><section><h2>Our mission</h2><p>Make research easier to enter, inspect and build on. People choose questions, check evidence and decide what is ready to share. Agents can assist within the methods and scope people agree.</p><p>Contributions include questions, sources, domain review, writing, data, code and translation. No paid agent, academic credential or coding experience is required to begin.</p></section><section><h2>Leadership</h2><p>' + link('Cole / @ajhcs', 'https://github.com/ajhcs') + ' is the founder and initial administrator named in the adopted contribution standards, and the registered human lead of Medical XR.</p><p>OSRI is in its founder-only stage. Self-review and agent checks are recorded as such; independent human review remains a separate step.</p></section><section><h2>How we organize</h2><p>The hub maintains shared guides, catalogs and records. Each research project has its own repository and human lead. Administrators coordinate project maintainers and use meta-research to improve shared practices.</p><p>Six research areas connect projects across disciplines. The initial Healthcare scope is nonclinical.</p></section><section><h2>Open, with a record</h2><p>Sources, methods, decisions and versions stay traceable. Repository acceptance, human scientific review and external peer review are recorded separately. People authorize publication.</p><div class="text-actions">' + link('Shared standards', site.docs['governance/contribution-standards.md']) + link('Research practice', site.docs['meta-research/README.md']) + '</div></section></div>'
    body += '<p class="source-note">Leadership and structure checked against the ' + link('adopted standards', site.source_url('governance/contribution-standards.md')) + ' and ' + link('project register', site.source_url('projects/projects.csv')) + ' on 15 November 2026. No additional leadership appointments are inferred.</p>'
    return body


def targets(site, key):
    rows = [row for row in site.targets if row['project_id'] == key]
    body = '<section id="publication-targets" class="record-section"><h2>Intended outputs and venues</h2><ul>' + ''.join('<li>' + escape(text) + '</li>' for text in site.summaries[key]['outputs']) + '</ul><p class="notice">Output plans are proposals for Cole’s review. A selected target records intent; submission, acceptance and publication are separate events. Targets do not count as published outputs.</p>'
    if not rows:
        return body + '<p>No venue candidates have been recorded for this project.</p></section>'
    body += '<div class="target-list">'
    for row in rows:
        status = 'Candidate—under review' if row['status'] == 'candidate' else 'Selected target'
        decision = '<p class="small">Selected by ' + escape(row['selected_by']) + ' on ' + escape(row['selected_on']) + ' · ' + link('Decision record', row['selection_reference']) + '</p>' if row['status'] == 'selected' else ''
        body += f'<article><p class="status">{status}</p>{decision}<h3>{escape(row["venue"])}</h3><p>{escape(row["rationale"])}</p><p><strong>Recommendation:</strong> {escape(row["recommendation"])}</p><details><summary>Compare scope, methods, fees and AI policy</summary><dl>'
        for title, field in [('Audience', 'audience'), ('Scope', 'scope'), ('Article types', 'article_types'), ('Methodological expectations', 'methods'), ('Overlapping work', 'overlap'), ('Open-access costs', 'cost'), ('AI disclosure', 'ai_disclosure')]:
            value = row[field]
            if isinstance(value, list):
                value = '; '.join(str(v) for v in value)
            body += f'<dt>{title}</dt><dd>{escape(str(value))}</dd>'
        body += '</dl><ul class="source-list">' + ''.join('<li>' + link(source['title'], source['url']) + ' · checked ' + escape(source['checked_on']) + '</li>' for source in row['sources']) + '</ul></details><p class="small">Verified ' + escape(row['verified_on']) + '</p></article>'
    comparison = site.docs.get('publications/medical-xr-venue-comparison.md') if key == 'OSRI-0001' else None
    body += '</div><p>' + (link('Read the sourced venue comparison →', comparison) if comparison else link('Publication planning guide →', site.docs['publications/publish.md'])) + '</p></section>'
    return body


def project(site, row):
    key = row['project_id']
    record = site.summaries[key]
    body = '<nav class="breadcrumbs" aria-label="Breadcrumb">' + link('Research', '/research/') + ' / ' + escape(key) + '</nav>'
    body += site.heading(key + ' · ' + row['areas'].replace(';', ' / '), row['title'], record['summary'])
    body += '<div class="text-actions">' + link('View materials ↓', '#materials') + link('Find a contribution task ↗', record['contribution']['url']) + '</div>'
    body += '<div class="project-facts"><p><strong>Human lead</strong> ' + escape(row['human_lead']) + '</p><p><strong>Research status</strong> ' + status_badge(record) + '</p><p><strong>Status updated</strong> ' + escape(record['status_decision']['on']) + '</p></div>'
    if record['activity'] == 'on_hold':
        body += '<p class="notice">' + escape(record['hold_reason']) + '</p>'
    body += '<ol class="project-stages" aria-label="Project stages">' + ''.join('<li' + (' aria-current="step"' if stage == record['stage'] else '') + '>' + escape(label) + '</li>' for stage, label in STAGES.items()) + '</ol>'
    body += '<div class="project-layout"><div><section id="question"><h2>The question</h2><blockquote>' + escape(record['question']) + '</blockquote></section><details id="current-status"><summary>Research checkpoint · source checked ' + escape(record['verified_on']) + '</summary><p>' + escape(record['status_detail']) + '</p></details><section id="methods"><h2>Methods and limits</h2><p>' + escape(record['methods']) + '</p></section></div><aside class="materials-panel" id="materials"><h2>Available materials</h2><ul>' + ''.join('<li>' + link(material['title'] + ' ↗', material['url']) + '</li>' for material in record['materials']) + '</ul>' + link('Open research repository ↗', row['repository_url']) + '<section id="contribution-task"><h3>One way to help</h3><p>' + escape(record['contribution']['summary']) + '</p>' + link(record['contribution']['title'] + ' ↗', record['contribution']['url']) + '</section></aside></div>'
    body += targets(site, key)
    body += '<details class="source-details"><summary>Public sources and verification dates</summary><ul>' + ''.join('<li>' + link(source['title'], source['url']) + ' · checked ' + escape(source['checked_on']) + '</li>' for source in record['sources']) + '</ul></details>'
    return body
