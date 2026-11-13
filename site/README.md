# OSRI Prism landing page

This static page implements the selected Prism direction with accessible HTML, local fonts, and links to the existing OSRI research resources. The Simulation Lab remains described as proposed. No hosting or deployment is configured here.

To preview it from this directory, run `python3 -m http.server 8765` and open `http://localhost:8765/`. The page needs no build step or JavaScript.

## Source and fonts

The hero vector is extracted from the selected Prism prototype; the logo comes from the [identity kit](../identity/prism/README.md). Inter and IBM Plex Mono files and their SIL Open Font License notices are in `assets/fonts/`.

The small `OSRI-CJK-link-subset.woff2` is a renamed subset of Noto Sans CJK SC for the Chinese navigation label only. Its OFL notice is included. The original full font remains in `../identity/shared-language/fonts/`. If the label changes, update the `text` value and rebuild with `python3 tools/build-cjk-subset.py` using an environment with FontTools and Brotli. The script checks coverage for the selected label; the subset is not a general Chinese font.
