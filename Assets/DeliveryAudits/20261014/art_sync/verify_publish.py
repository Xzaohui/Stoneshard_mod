"""Read-only verification of the 2026-10-14 art publication manifest."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
manifest = json.loads((HERE / 'PUBLISH_MANIFEST.json').read_text(encoding='utf-8'))
errors = []
items = manifest['files'] + manifest['archives']
for item in items:
    path = ROOT / item['path']
    if not path.is_file():
        errors.append({'path': item['path'], 'error': 'missing'})
        continue
    data = path.read_bytes()
    if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
        errors.append({'path': item['path'], 'error': 'size or SHA-256 mismatch'})
    if len(data) >= 100 * 1024 * 1024:
        errors.append({'path': item['path'], 'error': 'GitHub 100 MiB limit'})
    if path.suffix == '.zip':
        with zipfile.ZipFile(path) as archive:
            bad = archive.testzip()
            if bad:
                errors.append({'path': item['path'], 'error': 'ZIP CRC failure', 'member': bad})
print(json.dumps({'checked': len(items), 'errors': errors, 'passed': not errors}, ensure_ascii=False, indent=2))
sys.exit(bool(errors))
