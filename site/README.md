# OSRI website

The public site uses Prism, the existing Python generator and GitHub Pages. Markdown and CSV remain the source for guides, catalogs, translations, registered projects, public outputs and activity.

The publishing repository, [open-source-research-initiative.github.io](https://github.com/Open-Source-Research-Initiative/open-source-research-initiative.github.io), checks out **hub `main`**, builds and checks it, then deploys Pages. Its hourly schedule can publish a hub merge without another action. Obtain authorization for the reviewed **merge and publication together**.

## Build, check and preview

Use the pinned packages in `requirements.txt` in a project environment. The output directory must be new:

```sh
python site/build.py --output /workspace/build/builderbob/osri-preview
python site/check.py /workspace/build/builderbob/osri-preview
python -m unittest discover -s site -p 'test_*.py'
python -m http.server 8769 --directory /workspace/build/builderbob/osri-preview
```

Tests use temporary fixture directories; set `TMPDIR` to the permitted workspace scratch directory on hosts that restrict working-data placement. The checks cover local routes and anchors, metadata, immutable source links, translation notices, SVG fonts and search coverage. Fixtures cover empty and multiple-project collections, invalid references and selection records, and unchanged output/work counting.

## Content and templates

- `build.py` reads sources, resolves routes and links, generates pages and creates `search-index.json` and `build-info.json`.
- `render.py` holds reusable homepage, project, About, collaboration and venue components. The homepage no longer extracts or substitutes strings in a prototype. `index.html` is the retained historical Prism prototype, outside the build input.
- `records.py` checks the structured editorial collections. Project IDs must already be registered in `projects/projects.csv`.
- `projects/summaries.json` adds source-checked questions, status, methods, materials, a bounded task and proposed output plans. `short_title` supports compact cards. Public `stage` and `activity` use a dated human-lead `status_decision`; execution checkpoints remain separate. See `projects/website-summaries.md`.
- `publications/targets.json` stores venue comparisons, rationale, recommendations, official sources and verification dates, separately from `publications/publications.csv`. Status is `candidate` or `selected`. A selected target also needs `selected_by`, `selected_on` and a public `selection_reference`; it records intent, never submission, acceptance or publication.
- `styles.css` provides the Prism foundation. `site.css` covers page templates. `site.js` adds mobile navigation, catalog filtering and brief section entrances; `search.js` adds indexed search, content filters, counts, reset and shareable query URLs.

The activity page still calls `community/update.py` directly. Publication targets never enter that function or its CSV registers. Existing publication-counting behavior, CSV downloads, routes, linked anchors and translation notices are preserved. `/about/`, `/research/<lowercase-project-id>/` and `/search/` are additional routes. `/contribute/` adds collaboration routes and retains the full guide and its anchors in native disclosure content; its dedicated guide remains at `/guides/contributing/`.

`/venues/` embeds the reviewed directory fragment inside the shared OSRI layout. The snapshot pins the source commit and hashes every exported file; altered HTML, data, CSS or JavaScript blocks the build. The standalone HTML remains offline-capable. Scoped directory CSS inherits the host typography and leaves global navigation intact. The homepage preview derives its count and subfields from the same verified snapshot.

The default browsing mode requires free author costs, peer review, compatible substantive AI use and documented core standards. Expanded modes include incomplete quality checks or all 146 directory records. Up to three venues can be compared; URL parameters retain filters and canonical IDs through refresh, browser history and sharing. No account or backend is needed. The underlying evidence, CSV and JSON retain their source values.

The venue directory and collaboration page link the short evidence/use-report forms and six starter issues. `community/venue-starter-tasks.md` is the public task index; `docs/venue-directory-demo.md` is the walkthrough and transcript. Its video, poster and optional WebVTT captions live in `site/assets/demos/`. The dedicated video component keeps raw HTML disabled in general Markdown. Links to existing `site/assets/` files resolve to the site's copied assets.

To refresh the silent 90-second recording, serve a built preview and run `site/tools/record-venue-demo.cjs` with an existing Playwright installation. Set `OSRI_SITE_URL`, `OSRI_PLAYWRIGHT_MODULE`, optional `OSRI_CHROMIUM`, and an absolute `OSRI_DEMO_OUTPUT` outside the checkout. Use a permitted, short workspace `TMPDIR` on Linux so Chromium's socket path fits. Inspect the recording and metadata, then copy the final WebM, poster and VTT into the demo asset folder and rebuild. This scripted demonstration is not an external researcher-use result.

Long guides generate a native, collapsible on-page contents list and linked headings. Essential content, menus, materials, targets and journey stages work without JavaScript. Search falls back to the complete linked index and browser Find. If animation or JavaScript fails, reading content remains visible. Reduced motion bypasses entrance effects.

The Simulation Lab reads `simulation-lab/tools.csv`, `papers.csv`, and `examples.csv`. The build validates their references and generated Markdown/BibTeX through `simulation-lab/catalog.py`. After editing those records, run `python3 simulation-lab/catalog.py --write` before building. The lab page, global search records, and downloadable CSV files use the same records. The complete paper-to-code planning inventory lives in `simulation-lab/research/routes.json`; regenerate its six domain guides and CSV with `python3 simulation-lab/research.py --write` before regenerating the catalog. The site links every tool to its route, and the catalog validator checks complete coverage and generated-file freshness. Research routes have separate execution and paper-relationship fields and do not change the original teaching-run counts.

## Graphics, fonts and provenance

Prism’s approved logo geometry is unchanged. The hero retains its existing vector planes, removing washed-out overlay polygons. Guide images with matching editable Prism SVG masters use those local vectors. Fonts declared by SVG masters are embedded from the identity kit during the build so SVG image documents resolve their own fonts. The generated files retain editable text, titles and descriptions; guides retain textual explanations.

Inter, IBM Plex Mono and Noto font licenses remain alongside local assets. The renamed Chinese subset is built and checked for guide and interface character coverage. Page-specific descriptions, canonical URLs and immutable hub source links are generated for every page. `build-info.json` records the exact committed source; review previews built with uncommitted edits are provisional and must be rebuilt from the final reviewed commit before release verification.

The 21-candidate campaign uses `simulation-lab/reproductions/campaign.json`, original `.md.in` guide templates, compact run records and selected reusable outputs. Run `python3 simulation-lab/reproduce.py --write` before the other lab generators. The catalog entry point validates complete candidate coverage, publication-target claim fields and public-output hashes. Markdown files inside downloadable bundles are source files; their canonical guide pages are generated outside the bundle directories.
