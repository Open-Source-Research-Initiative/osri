#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build the activity board from OSRI's current CSV registers."""

import argparse
from collections import Counter, defaultdict
import csv
from datetime import date
from pathlib import Path
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
KINDS = {
    "question": "Questions",
    "evidence": "Evidence",
    "data_method": "Data and methods",
    "analysis": "Analysis",
    "review": "Review",
    "writing": "Writing",
    "translation": "Translation",
    "community": "Community",
}
OUTPUTS = {
    "journal_article": "Journal articles",
    "conference_paper": "Full conference papers",
    "preprint": "Preprints",
    "research_blog": "Research blogs and technical essays",
}


def read_register(root, path, required, identity):
    with (root / path).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"{path}: missing required columns")
        rows = list(reader)
    seen = set()
    for number, row in enumerate(rows, 2):
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"{path}:{number}: malformed row")
        for key, value in row.items():
            row[key] = value.strip()
        key = row[identity].strip()
        if not key or key in seen:
            raise ValueError(f"{path}:{number}: missing or duplicate {identity}")
        seen.add(key)
    return rows


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def build(root=ROOT):
    projects = read_register(root, "projects/projects.csv", {"project_id"}, "project_id")
    project_ids = {row["project_id"].strip() for row in projects}
    publications = read_register(
        root, "publications/publications.csv",
        {"publication_id", "project_id", "work_id", "publication_type", "status",
         "url", "first_published_date"},
        "publication_id",
    )
    tasks = read_register(
        root, "community/contributions.csv",
        {"contribution_id", "contributors", "project_id", "kind", "summary",
         "evidence_url", "status", "accepted_on", "accepted_by"},
        "contribution_id",
    )
    outputs, works = Counter(), set()
    for row in publications:
        if row["status"] != "published":
            continue
        if row["publication_type"] not in OUTPUTS or not row["work_id"].strip():
            raise ValueError(f"{row['publication_id']}: published output needs a type and work ID")
        if row["project_id"].strip() not in project_ids:
            raise ValueError(f"{row['publication_id']}: project is not registered")
        publication_url = urlparse(row["url"])
        if publication_url.scheme not in {"https", "http"} or not publication_url.netloc:
            raise ValueError(f"{row['publication_id']}: published output needs a public URL")
        if date.fromisoformat(row["first_published_date"]).isoformat() != row["first_published_date"]:
            raise ValueError(f"{row['publication_id']}: publication date must use YYYY-MM-DD")
        outputs[row["publication_type"]] += 1
        works.add(row["work_id"].strip())

    people = defaultdict(lambda: {"tasks": 0, "kinds": Counter(), "latest": ""})
    accepted = 0
    for row in tasks:
        identity = row["contribution_id"]
        if row["status"] not in {"pending", "accepted", "withdrawn"}:
            raise ValueError(f"{identity}: unknown contribution status")
        if row["kind"] not in KINDS:
            raise ValueError(f"{identity}: unknown contribution kind")
        if row["project_id"].strip() and row["project_id"].strip() not in project_ids:
            raise ValueError(f"{identity}: project is not registered")
        if row["status"] != "accepted":
            continue
        names = [name.strip() for name in row["contributors"].split(";")]
        if not all(names) or len(names) != len(set(names)):
            raise ValueError(f"{identity}: missing or repeated contributor")
        if not row["summary"].strip() or not row["accepted_by"].strip():
            raise ValueError(f"{identity}: accepted task needs a summary and human maintainer")
        accepted_on = date.fromisoformat(row["accepted_on"]).isoformat()
        if accepted_on != row["accepted_on"]:
            raise ValueError(f"{identity}: acceptance date must use YYYY-MM-DD")
        evidence = urlparse(row["evidence_url"])
        if evidence.scheme not in {"https", "http"} or not evidence.netloc:
            raise ValueError(f"{identity}: accepted task needs a public evidence URL")
        accepted += 1
        for name in names:
            person = people[name]
            person["tasks"] += 1
            person["kinds"][row["kind"]] += 1
            person["latest"] = max(person["latest"], accepted_on)

    lines = [
        "# OSRI activity", "",
        "Counts cover the current registers. They do not include unregistered projects or unlogged contributions.", "",
        "| Recorded measure | Count |", "| --- | ---: |",
        f"| Research projects | {len(projects)} |",
        f"| Public publication outputs | {sum(outputs.values())} |",
        f"| Distinct published research works | {len(works)} |",
        f"| Accepted contribution tasks | {accepted} |",
        f"| Credited contributors | {len(people)} |", "",
        "## Publication outputs", "",
        "| Type | Count |", "| --- | ---: |",
    ]
    lines.extend(f"| {label} | {outputs[kind]} |" for kind, label in OUTPUTS.items())
    lines += [
        "", "Output type and peer-review status are recorded separately in the [publication register](../publications/publications.csv).", "",
        "## Contributor board", "",
    ]
    if not people:
        lines.append("No accepted contributions have been logged yet. Earlier GitHub activity is not automatically backfilled.")
    else:
        lines += ["| Place | Contributor | Accepted tasks | Work types | Latest acceptance |", "| ---: | --- | ---: | --- | --- |"]
        previous, place = None, 0
        ordered = sorted(people.items(), key=lambda item: (-item[1]["tasks"], item[0].casefold(), item[0]))
        for position, (name, person) in enumerate(ordered, 1):
            if person["tasks"] != previous:
                place = position
            previous = person["tasks"]
            kinds = "; ".join(f"{label}: {person['kinds'][kind]}" for kind, label in KINDS.items() if person["kinds"][kind])
            lines.append(f"| {place} | {cell(name)} | {person['tasks']} | {kinds} | {person['latest']} |")
    lines += [
        "", "A shared task counts once overall and once for each credited person. Ties share a place. Task counts do not determine authorship or research quality.", "",
        "[How to receive credit](README.md) · [Contribution records](contributions.csv) · [Research projects](../projects/projects.csv)",
    ]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report an outdated board without changing it")
    args = parser.parse_args()
    try:
        text = build()
        output = ROOT / "community/ACTIVITY.md"
        if args.check:
            if not output.exists() or output.read_text(encoding="utf-8") != text:
                raise ValueError("Activity board is outdated; run python3 community/update.py")
            print("Activity board matches its source registers.")
        else:
            output.write_text(text, encoding="utf-8")
            print("Updated community/ACTIVITY.md")
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
