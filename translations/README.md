# Translations

English is the reference version. The website has machine-translated drafts of every main page and generated guide in five languages. All await fluent human review. Google Translate and local Helsinki-NLP OPUS-MT models prepared the initial catalog text; Codex prepared the catalogs and checked structure and links. Model sources and exact revisions are recorded in [machine provenance](machine-provenance.json). No language or scientific review is claimed.

| Language | Website | Review status |
| --- | --- | --- |
| 简体中文 — Simplified Chinese | [Chinese pages](https://open-source-research-initiative.github.io/zh-hans/) | Draft; reviewer needed |
| 한국어 — Korean | [Korean pages](https://open-source-research-initiative.github.io/ko/) | Draft; reviewer needed |
| Español — Spanish | [Spanish pages](https://open-source-research-initiative.github.io/es/) | Draft; reviewer needed |
| Français — French | [French pages](https://open-source-research-initiative.github.io/fr/) | Draft; reviewer needed |
| العربية — Arabic | [Arabic pages](https://open-source-research-initiative.github.io/ar/) | Draft; reviewer needed |

The language menu keeps the current page. Local navigation, search, guide text, captions, image alternatives, and venue evidence use the selected language. Code, identifiers, original paper and venue names, URLs, and downloadable source records retain their original values. Image artwork, the English demonstration video, and external websites retain their source language. Translated captions and the written walkthrough accompany the video.

## Help with one page

[Reply to the translator discussion](https://github.com/orgs/Open-Source-Research-Initiative/discussions/3) with your language, the page you want to help with, relevant subject experience, and whether you can translate, review, or maintain it. Coding experience is not required. You can suggest a correction directly in the discussion and link the English passage.

Editable catalogs live in `translations/catalogs/`. Each English key has one translated value. A shared phrase updates everywhere it appears. Preserve keys and placeholders such as `{count}`. Keep **OSRI** and **Agentic-Powered-Research** unchanged.

For a smaller review file, build the website, then export a page:

```sh
python site/translations.py /workspace/build/builderbob/osri-preview --page /start/ --language es --export /workspace/build/builderbob/start-es.json
```

Edit only the translated values under `messages`. Import the corrections, rebuild into a new directory, and check coverage:

```sh
python site/translations.py /workspace/build/builderbob/osri-preview --language es --import-file /workspace/build/builderbob/start-es.json
python site/build.py --output /workspace/build/builderbob/osri-translated
python site/check.py /workspace/build/builderbob/osri-translated
python site/translations.py /workspace/build/builderbob/osri-translated --check
```

Export without `--page` to work on the whole catalog. Source text changes create missing keys; the build displays English for those passages and marks affected pages `needs-update`. The coverage check identifies missing translations. Unused keys remain available for comparison until a maintainer removes them. No translation service or paid account is required to build, read, or edit the site.

## Review records

The built [page register](https://open-source-research-initiative.github.io/translation-pages.json) records each page's English route, source commit, source and translation hashes, review state, and missing passages. The [coverage register](https://open-source-research-initiative.github.io/translation-coverage.json) counts translated messages separately from human review.

To record completed human review, a maintainer adds an entry to `translations/reviews.json` with `language`, English `url`, `source_digest`, `translation_digest`, `reviewer`, `review_date`, `domain_reviewer`, and `review_url`. Use the hashes in the current page register. One qualified person may cover both roles. The review link must identify the actual comparison and its scope. Imports never grant review status. Changes to either the source or translated text make a reviewed page `needs-update` until review is renewed.

The older Markdown drafts in `zh-Hans/` and [their page records](status.csv) remain as historical repository translations. The current website uses the catalogs, including at the original Chinese page URLs. The older register also contains records from other repositories; it does not describe current website coverage.

See the [translation guide](../governance/translation.md). Translations retain attribution and the applicable license. Other languages are welcome.
