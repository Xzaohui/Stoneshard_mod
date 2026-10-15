"""Read-only verification of the 2026-10-15 publication and replay mapping.

This validates published bytes and recoverability, not artistic approval,
legacy SHA-list portability, build correctness, or game runtime behavior.
"""
from pathlib import Path
import hashlib
import json
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
manifest = json.loads((HERE / 'PUBLISH_MANIFEST.json').read_text(encoding='utf-8'))
exclusions = json.loads((HERE / 'EXCLUDED_LOCAL_FILES.json').read_text(encoding='utf-8'))
errors = []
for item in manifest['files']:
    path = ROOT / item['path']
    if not path.is_file():
        errors.append({'path': item['path'], 'error': 'missing published file'})
        continue
    data = path.read_bytes()
    if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
        errors.append({'path': item['path'], 'error': 'size or SHA-256 mismatch'})
    if len(data) >= 100 * 1024 * 1024:
        errors.append({'path': item['path'], 'error': 'GitHub 100 MiB limit'})
    if path.suffix.lower() == '.zip':
        with zipfile.ZipFile(path) as archive:
            bad = archive.testzip()
            if bad:
                errors.append({'path': item['path'], 'error': 'ZIP CRC failure', 'member': bad})
recoverable = 0
for item in exclusions['files']:
    alternative = item.get('retained_alternative')
    if not alternative:
        continue
    path = ROOT / alternative
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        errors.append({'path': item['path'], 'error': 'retained alternative missing or hash mismatch', 'alternative': alternative})
    else:
        recoverable += 1
print(json.dumps({'published_files_checked': len(manifest['files']), 'replay_paths_recoverable': recoverable, 'errors': errors, 'passed': not errors, 'scope': 'Publication bytes, ZIP CRC and replay recovery mapping only; no visual approval, build or runtime claim.'}, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
