#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate the lab CSV records and regenerate their Markdown and BibTeX views."""
import argparse
import csv
from datetime import date
from pathlib import Path
import re
import runpy
import json
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
STATUS = {
    "executed_adaptation": "Executed adaptation",
    "upstream_instructions_checked": "Upstream instructions checked; not run",
    "access_pending": "Artifact access pending",
}


def load(name, key):
    with (ROOT / name).open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    ids = [row[key] for row in rows]
    if len(set(ids)) != len(ids) or not all(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) for value in ids):
        raise ValueError(f"Invalid or duplicate IDs in {name}")
    if not rows or any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError(f"Empty or malformed CSV: {name}")
    return {row[key]: row for row in rows}


def ids(value):
    return value.split(";") if value else []


def validate(tools, papers, examples):
    for collection in (tools, papers, examples):
        for row in collection.values():
            for key, value in row.items():
                if key.endswith("url"):
                    url = urlsplit(value)
                    if url.scheme != "https" or not url.netloc:
                        raise ValueError(f"Expected an HTTPS source: {value}")
                elif key == "checked_date":
                    date.fromisoformat(value)
    for tool in tools.values():
        if not tool["license_summary"] or not tool["role"] or not tool["source_status"]:
            raise ValueError(f"Missing tool assessment: {tool['tool_id']}")
        for reference in ids(tool["paper_ids"]):
            if reference not in papers:
                raise ValueError(f"Unknown paper: {reference}")
        expected = {key for key, row in examples.items() if tool["tool_id"] in ids(row["tool_ids"])}
        if set(ids(tool["example_ids"])) != expected:
            raise ValueError(f"Tool/example links disagree: {tool['tool_id']}")
    for row in examples.values():
        if row["status"] not in STATUS:
            raise ValueError(f"Unknown example status: {row['status']}")
        if not ids(row["paper_ids"]) or not ids(row["tool_ids"]):
            raise ValueError(f"Example needs tool and paper IDs: {row['example_id']}")
        for key, records in (("paper_ids", papers), ("tool_ids", tools)):
            for value in ids(row[key]):
                if value not in records:
                    raise ValueError(f"Unknown {key}: {value}")
        guide = urlsplit(row["guide"])
        path = (ROOT / guide.path).resolve()
        if guide.scheme or not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError(f"Missing local guide: {row['guide']}")
    dois = [row["doi"].lower() for row in papers.values()]
    if len(set(dois)) != len(dois) or not all(value.startswith("10.") and "/" in value for value in dois):
        raise ValueError("Invalid or duplicate DOIs")
    for paper in papers.values():
        if not paper["year"].isdigit() or not paper["verification"] or not paper["reading_status"]:
            raise ValueError(f"Incomplete reference: {paper['id']}")


def catalog(tools, papers, examples, research_routes):
    lines = ["# Simulation tool catalog", "",
             f"{len(tools)} tools with open-source cores, grouped by use. This is a growing inventory; it is not an exhaustive list of all simulators. Some components depend on separately licensed runtimes or assets, as noted below.", "",
             "Read the [example index](examples/README.md), [source notes](source-notes.md), and [verification record](verification.md). Repository availability does not mean a tool was installed or a paper reproduced. A software-description paper establishes context; it is not automatically an application example.", "",
             "Generated from [tools.csv](tools.csv), [papers.csv](papers.csv), and [examples.csv](examples.csv). To contribute, follow the [catalog guide](contributing.md).", ""]
    for domain in dict.fromkeys(row["domain"] for row in tools.values()):
        lines += [f"## {domain}", ""]
        for row in tools.values():
            if row["domain"] != domain:
                continue
            lines += [f"### {row['name']}", "", row["role"] + ".", "",
                      f"[Source]({row['source_url']}) · [Documentation]({row['docs_url']}) · [License]({row['license_url']})", "",
                      f"**Terms:** {row['license_summary']}. {row['dependency_notes']}", ""]
            references = [f"[{papers[key]['title']} ({papers[key]['year']})](bibliography.md#{key})" for key in ids(row["paper_ids"])]
            lines += ["**Literature:** " + ("; ".join(references) if references else "See the research construction route below for a candidate paper and its source assessment.") , ""]
            routes = [f"[{examples[key]['title']}]({examples[key]['guide']}) — {STATUS[examples[key]['status']]}" for key in ids(row["example_ids"])]
            lines += ["**Walkthrough:** " + ("; ".join(routes) if routes else "No OSRI walkthrough yet; start with the official documentation."), "",
                      f"**Research construction route:** [{research_routes[row['tool_id']]['paper']['title']}](research/{research_routes[row['tool_id']]['group']}.md#{row['tool_id']}) — {research_routes[row['tool_id']]['execution']['status'].replace('_', ' ')}. See the source and comparison assessment.", "",
                      f"Source checked {row['checked_date']}; {row['source_status'].replace('_', ' ')}.", ""]
    return "\n".join(lines)


def bibliography(papers):
    lines = ["# Simulation bibliography", "",
             "DOI metadata was checked against Crossref on 2026-11-15. Reading status is separate: only the passages identified below were inspected for the example mappings. This curated bibliography is not a systematic literature review.", "",
             "Download [CSV](papers.csv) or [BibTeX](references.bib). See the [example index](examples/README.md) for runnable code and upstream routes.", ""]
    for key, row in papers.items():
        lines += [f"## {key}", "", f"{row['authors']} ({row['year']}). **{row['title']}**. *{row['venue']}*. [{row['doi']}]({row['url']}).", "",
                  f"Publication type: {row['publication_type']}. [Metadata record]({row['metadata_url']}).", "",
                  f"Reading status: {row['reading_status']}.", "", f"Verification: {row['verification']}.", ""]
    return "\n".join(lines)


def bibtex(papers):
    def tex(value):
        return value.replace("&", "\\&").replace("%", "\\%").replace("_", "\\_")
    entries = []
    kinds = {"proceedings-article": "inproceedings", "book-chapter": "incollection", "book": "book"}
    for key, row in papers.items():
        kind = kinds.get(row["publication_type"], "article")
        fields = {"title": row["title"], "author": " and ".join(row["authors"].split("; ")), "year": row["year"], "doi": row["doi"], "url": row["url"]}
        if kind != "book":
            fields["journal" if kind == "article" else "booktitle"] = row["venue"]
        entries.append("@" + kind + "{" + key + ",\n" + ",\n".join("  " + name + " = {" + tex(value) + "}" for name, value in fields.items()) + "\n}\n")
    return "\n".join(entries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write generated views; otherwise check them")
    args = parser.parse_args()
    tools, papers, examples = load("tools.csv", "tool_id"), load("papers.csv", "id"), load("examples.csv", "example_id")
    validate(tools, papers, examples)
    research = runpy.run_path(str(ROOT / "research.py"), run_name="osri_research")
    data = json.loads((ROOT / "research/routes.json").read_text())
    research["validate"](data, tools)
    for name, content in research["outputs"](data, tools).items():
        path = ROOT / "research" / name
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            raise SystemExit(f"Generated research route differs: {name}; run research.py --write")
    routes = {row["tool_id"]: row for row in data["records"]}
    outputs = {"catalog.md": catalog(tools, papers, examples, routes), "bibliography.md": bibliography(papers), "references.bib": bibtex(papers)}
    for name, content in outputs.items():
        path = ROOT / name
        if args.write:
            path.write_text(content, encoding="utf-8")
        elif not path.is_file() or path.read_text(encoding="utf-8") != content:
            raise SystemExit(f"Generated file differs: {name}; run catalog.py --write")
    print(f"Validated {len(tools)} tools, {len(papers)} references, {len(examples)} example routes")


if __name__ == "__main__":
    main()
