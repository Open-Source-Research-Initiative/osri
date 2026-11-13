# OSRI website

The website uses Prism and reads its guides and records from this hub. Research, topics, resources, publications, contributor activity, and Chinese draft guides are published as static pages.

The organization site is published from [open-source-research-initiative.github.io](https://github.com/Open-Source-Research-Initiative/open-source-research-initiative.github.io). Its workflow checks out this hub, builds the site, and deploys GitHub Pages. It runs hourly, on publishing-repository changes, and on manual request.

## Build and check

Install the pinned packages in a project environment, then build to a new output directory:

```sh
python3 -m pip install -r site/requirements.txt
python3 site/build.py --output /path/to/new-output
python3 site/check.py /path/to/new-output
python3 -m http.server 8765 --directory /path/to/new-output
```

Edit the hub's Markdown and CSV files to update the public content. `index.html` supplies the homepage body; `styles.css` retains the Prism base styles. `site.css` and `site.js` add navigation, guide layouts, and catalog filters. Essential content remains available without JavaScript.

The activity page uses `community/update.py` directly. It follows the same counting rules as the repository board. Source links identify the exact hub commit used for each build. Registered projects and public outputs appear only when their records are added.

## Source and fonts

The hero vector is extracted from the selected Prism prototype; the logo comes from the [identity kit](../identity/prism/README.md). Inter and IBM Plex Mono files and their SIL Open Font License notices are in `assets/fonts/`.

The build creates a renamed Chinese font subset from `../identity/shared-language/fonts/NotoSansCJKSC-Regular.woff2`. It includes the Chinese guide text and interface labels, checks character coverage, and retains the OFL notice. Draft and review status remain visible.
