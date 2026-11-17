#!/usr/bin/env bash
set -euo pipefail
if [[ $# != 2 ]]; then
    echo "Usage: bash run.sh WORK_DIR NEW_EVIDENCE_DIR" >&2
    exit 2
fi
packet=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
work=$(cd -- "$1" && pwd)
mkdir -- "$2"
out=$(cd -- "$2" && pwd)
export TMPDIR="$work/tmp" XDG_CACHE_HOME="$work/cache"
export LC_ALL=C TZ=UTC
unset R_HOME R_LIBS R_LIBS_SITE R_LIBS_USER
python3 - "$work" "$packet" <<'PY'
import hashlib
import json
from pathlib import Path
import sys
work, packet = map(Path, sys.argv[1:])
pins = json.loads((packet / 'inputs.lock.json').read_text())['sources']
source = work / 'sources/replication.R'
if hashlib.sha256(source.read_bytes()).hexdigest() != pins[source.name]['sha256']:
    raise SystemExit('Publisher supplement does not match the SHA-256 pin.')
PY
status=0
"$work/env/bin/Rscript" --vanilla "$packet/run.R" "$work" "$out" "$packet" \
    2>&1 | tee "$out/run.log" || status=$?
(
    cd -- "$out"
    find . -maxdepth 1 -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS
)
exit "$status"
