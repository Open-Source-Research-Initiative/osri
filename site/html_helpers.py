# SPDX-License-Identifier: MIT
"""Escaped HTML links shared by the generator and page components."""
from html import escape
from urllib.parse import urlsplit

def href(url):
    if urlsplit(url).scheme not in {"", "http", "https", "mailto"}:
        raise ValueError(f"Unsupported link scheme: {url}")
    return escape(url, quote=True)


def link(label, url, **attributes):
    attrs = "".join(f' {key.rstrip("_").replace("_", "-")}="{escape(str(value), quote=True)}"' for key, value in attributes.items())
    return f'<a href="{href(url)}"{attrs}>{escape(label)}</a>'
