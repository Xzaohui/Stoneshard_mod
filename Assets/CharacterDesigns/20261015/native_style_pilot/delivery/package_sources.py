#!/usr/bin/env python3
"""Freeze the reviewed files into a lossless, hash-verified source archive."""
from pathlib import Path
import hashlib
import json
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    for actor in ('mara', 'iwo'):
        manifest = json.loads((ROOT / actor / 'manifest.json').read_text())
        for entry in manifest['files']:
            p = ROOT / actor / entry['path']
            assert p.is_file(), p
            assert p.stat().st_size == entry['bytes'], p
            assert sha(p) == entry['sha256'], p
    assert (ROOT / 'independent_qa/QA_REPORT.md').is_file()
    assert (ROOT / 'independent_qa/measurements.json').is_file()
    names = ['native_style_pilot_review_20261015.png',
             'mara_portrait_v2_74x100_candidate.png',
             'iwo_portrait_v1_74x100_candidate.png',
             'README_验收说明.md', 'layout_verification.json',
             'build_review.py', 'package_sources.py']
    inputs = sorted(p for sub in ('mara', 'iwo', 'independent_qa') for p in (ROOT / sub).rglob('*') if p.is_file())
    inputs += [HERE / name for name in names]
    records = [{'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in inputs]
    package_manifest = {
        'date': '2026-10-15',
        'release_status': '2 portrait candidates; both map assets failed; no native_final',
        'independent_qa_included': True,
        'generation_method': 'high-resolution image generation then deterministic target-size derivation',
        'runtime_integrated': False, 'runtime_verified': False,
        'archive_method': 'ZIP_DEFLATED, lossless; byte hashes checked after packing',
        'files': records,
    }
    manifest_path = HERE / 'package_manifest.json'
    manifest_path.write_text(json.dumps(package_manifest, ensure_ascii=False, indent=2) + '\n')
    inputs.append(manifest_path)
    out = HERE / 'native_style_pilot_sources_20261015.zip'
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in inputs:
            z.write(p, 'native_style_pilot/' + str(p.relative_to(ROOT)))
    assert out.stat().st_size < 18 * 1024 * 1024
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for p in inputs:
            assert hashlib.sha256(z.read('native_style_pilot/' + str(p.relative_to(ROOT)))).hexdigest() == sha(p)
    for r in records:
        assert sha(ROOT / r['path']) == r['sha256']
    outputs = [HERE / n for n in names[:3]] + [out]
    file_records = []
    from PIL import Image
    for p in outputs:
        r = {'file_name': p.name, 'local_path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p)}
        if p.suffix == '.png':
            with Image.open(p) as im:
                r['dimensions'] = list(im.size)
                r['mode'] = im.mode
        file_records.append(r)
    delivery_manifest = {
        'delivery_status': 'ready_for_library_upload',
        'independent_qa': str((ROOT / 'independent_qa/QA_REPORT.md').relative_to(ROOT)),
        'independent_qa_sha256': sha(ROOT / 'independent_qa/QA_REPORT.md'),
        'source_file_count': len(inputs), 'archive_crc_pass': True, 'archive_sha256_roundtrip_pass': True,
        'files': file_records,
    }
    (HERE / 'delivery_manifest.json').write_text(json.dumps(delivery_manifest, ensure_ascii=False, indent=2) + '\n')
    (HERE / 'SHA256SUMS.txt').write_text(''.join(f"{r['sha256']}  {r['file_name']}\n" for r in file_records))
    print(json.dumps(delivery_manifest, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
