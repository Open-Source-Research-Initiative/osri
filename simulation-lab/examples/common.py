# SPDX-License-Identifier: MIT
"""Small helpers for portable, inspectable teaching runs."""
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform


def output_directory(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=False)
    return path


def save_record(output, example, packages, parameters, results, checks, sources):
    record = {
        "example": example,
        "scope": "Educational adaptation; not a reproduction of a published result",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "software": {name: version(name) for name in packages},
        "parameters": parameters,
        "sources": sources,
        "results": results,
        "checks": checks,
        "files_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sorted(output.iterdir()) if p.is_file()},
        "code_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(Path(__file__).parent.glob('*.py'))},
    }
    (output / "run.json").write_text(json.dumps(record, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"example": example, "results": results, "checks": checks}, indent=2))
    if not all(checks.values()):
        raise SystemExit("A recorded check failed; inspect run.json")
