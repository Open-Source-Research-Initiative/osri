# Prism identity kit

Prism is the selected visual direction for the Open Source Research Initiative (OSRI). The kit provides editable sources and PNG exports for the organization, the hub, and project repositories. The [visual identity guide](../../governance/visual-identity.md) explains how to use them.

| Material | Files |
| --- | --- |
| Logo system | [Arrangements](previews/01-logo-system.png); [symbol](sources/logo-symbol.svg), [wordmark](sources/logo-wordmark.svg), [full name](sources/logo-full-name.svg), [horizontal](sources/logo-horizontal.svg), [stacked](sources/logo-stacked.svg), [compact](sources/logo-compact.svg), [monochrome](sources/logo-monochrome.svg) |
| Avatar | [512 px PNG](previews/avatar-512.png) and [SVG](sources/avatar-512.svg); [size comparison](previews/02-avatar-comparison.png); 128, 64, and 32 px exports in `previews/` |
| Visual style | [Style sheet PNG](previews/03-style-sheet.png) and [editable SVG](sources/03-style-sheet.svg) |
| README headers | Organization [PNG](previews/header-org.png) / [SVG](sources/header-org.svg); hub [PNG](previews/header-hub.png) / [SVG](sources/header-hub.svg); project template [PNG](previews/header-project.png) / [SVG](sources/header-project.svg) |
| README layout | [Layout specimen](previews/05-readme-layout.png), [Markdown](README-specimen.md), and [HTML](README-specimen.html); the current repository READMEs remain the content authority |
| Social previews | Organization `.github` [PNG](previews/social-org.png) / [SVG](sources/social-org.svg); hub [PNG](previews/social-hub.png) / [SVG](sources/social-hub.svg); project template [PNG](previews/social-project.png) / [SVG](sources/social-project.svg) |
| Research journey | [Diagram and text explanation](research-journey.md); [editable SVG](sources/07-research-journey.svg) |
| Multilingual specimens | [Latin and Arabic](previews/08-multilingual.png) / [SVG](sources/08-multilingual.svg); [long headings and other scripts](previews/08b-long-headings.png) / [SVG](sources/08b-long-headings.svg); [desktop HTML specimen](multilingual-specimen.html) |

The social PNGs are 1280 × 640 and under 1 MB. GitHub's organization avatar and repository social previews are settings: adding the files to a repository does not install them. Use `avatar-512.png` for the organization avatar and the matching social PNG for each repository.

## Fonts and translation

The SVGs retain editable text and load fonts from the adjacent [`fonts/`](fonts/) directory. The long-heading specimen also uses the adjacent [`shared-language/fonts/`](../shared-language/fonts/) directory. Keep those directories and their license notices together when moving the kit. Inter, IBM Plex Mono, and the Noto fonts are distributed under the SIL Open Font License; their notices accompany the files.

Translated strings in the specimens are layout examples, not reviewed translations. Follow the [translation guide](../../governance/translation.md) and obtain fluent human review before using them as published text.

## Provenance and reuse

The founder selected direction 10, Prism, on 13 November 2026. The initial identity study was produced by Codex Sol 6.1 subagents and lightly refined by Codex Astra Max subagents. Codex applied the system to the repository materials using Ingenium 0.1.0. The source and export hashes are recorded in [manifest.json](manifest.json).

The existing [repository license](../../LICENSE.md) describes the terms for starter prose, code, and configuration. Separate terms for reuse of the Prism identity artwork have not yet been recorded; contact OSRI before reusing the marks or implying affiliation. Font licenses remain separate.
