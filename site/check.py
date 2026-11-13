#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check generated OSRI website pages and local assets."""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.headings = 0
        self.language = None
        self.missing_alt = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "html":
            self.language = attrs.get("lang")
        if tag == "h1":
            self.headings += 1
        if "id" in attrs:
            if attrs["id"] in self.ids:
                raise ValueError("Duplicate HTML ID: " + attrs["id"])
            self.ids.add(attrs["id"])
        for key in ["href", "src"]:
            if key in attrs:
                self.links.append(attrs[key])
        if tag == "img" and "alt" not in attrs:
            self.missing_alt = True


def check(root):
    pages = {}
    for path in root.rglob("*.html"):
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        if page.headings != 1 or page.missing_alt or page.language not in {"en", "zh-Hans"}:
            raise ValueError(f"{path.relative_to(root)}: check heading, language, or image alternatives")
        pages[path.resolve()] = page
    checked_links = 0
    for path, page in pages.items():
        for url in page.links:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc:
                continue
            target = root / unquote(parsed.path.lstrip("/")) if parsed.path.startswith("/") else path.parent / unquote(parsed.path)
            if not parsed.path:
                target = path
            if target.is_dir() or parsed.path.endswith("/"):
                target = target / "index.html"
            target = target.resolve()
            if not target.is_relative_to(root.resolve()) or not target.is_file():
                raise ValueError(f"{path.relative_to(root)}: broken local link {url}")
            if parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                raise ValueError(f"{path.relative_to(root)}: missing anchor {url}")
            checked_links += 1
    for css in root.glob("*.css"):
        for url in re.findall(r"url\(['\"]?([^)'\"]+)", css.read_text()):
            path = root / url.lstrip("/") if url.startswith("/") else css.parent / url
            if not path.is_file():
                raise ValueError(f"{css.name}: missing asset {url}")
    for page in root.glob("zh-hans/**/index.html"):
        if "待审核译稿" not in page.read_text():
            raise ValueError(f"{page}: translation draft notice missing")
    metadata = json.loads((root / "build-info.json").read_text())
    if len(pages) != len(metadata["pages"]):
        raise ValueError("Page count does not match the build record")
    print(f"Checked {len(pages)} pages, {checked_links} local links, CSS assets, and translation notices")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    check(args.directory.resolve())
