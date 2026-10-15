"""Recover omitted, byte-identical QA replay files without overwriting anything.
Default is read-only; add --restore to materialize missing replay paths.
Caches and unrelated local temporary files are deliberately not restored.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--restore', action='store_true', help='Create missing replay files from verified retained copies; never overwrite an existing file.')
args = parser.parse_args()
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
items = json.loads((HERE / 'EXCLUDED_LOCAL_FILES.json').read_text(encoding='utf-8'))['files']
result = {'mode': 'restore' if args.restore else 'dry_run', 'already_present': 0, 'recoverable_missing': 0, 'restored': 0, 'errors': []}
for item in items:
    if 'retained_alternative' not in item:
        continue
    source = (ROOT / item['retained_alternative']).resolve()
    dest = (ROOT / item['path']).resolve()
    if not source.is_relative_to(ROOT) or not dest.is_relative_to(ROOT):
        result['errors'].append({'path': item['path'], 'error': 'path escapes repository'})
        continue
    if not source.is_file():
        result['errors'].append({'path': item['path'], 'error': 'retained source missing'})
        continue
    data = source.read_bytes()
    if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
        result['errors'].append({'path': item['path'], 'error': 'retained source failed checksum'})
        continue
    if dest.exists():
        if not dest.is_file() or hashlib.sha256(dest.read_bytes()).hexdigest() != item['sha256']:
            result['errors'].append({'path': item['path'], 'error': 'existing destination differs; not overwritten'})
        else:
            result['already_present'] += 1
        continue
    result['recoverable_missing'] += 1
    if args.restore:
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as stream:
            stream.write(data)
        result['restored'] += 1
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(bool(result['errors']))
