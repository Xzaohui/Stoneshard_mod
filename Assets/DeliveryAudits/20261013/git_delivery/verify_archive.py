#!/usr/bin/env python3
"""Read-only verification of the original art archive after cloning."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
manifest = json.loads((HERE / "asset_bytes_manifest.json").read_text(encoding="utf-8"))
failures = []
for entry in manifest["files"]:
    path = ROOT / entry["path"]
    if not path.is_file():
        failures.append({"path": entry["path"], "error": "missing"})
        continue
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    if path.stat().st_size != entry["bytes"] or digest.hexdigest() != entry["sha256"]:
        failures.append({"path": entry["path"], "error": "bytes or SHA-256 mismatch"})
print(json.dumps({"checked_files": len(manifest["files"]), "checked_bytes": manifest["asset_bytes"], "failures": failures}, ensure_ascii=False, indent=2))
raise SystemExit(bool(failures))
