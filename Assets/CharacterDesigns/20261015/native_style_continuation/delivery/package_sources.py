#!/usr/bin/env python3
"""Package a frozen source snapshot; omit commercial reference pixels."""
from pathlib import Path
import hashlib
import json
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE_DIRS = ['leiya', 'tore', 'iwo_map_method', 'independent_qa']
EXCLUDED = {
    'leiya/sources/user_style_reference.png': 'User-supplied commercial style reference; retain citation and hash only.',
    'tore/sources/user_style_reference.png': 'User-supplied commercial style reference; retain citation and hash only.',
    'iwo_map_method/review/native_old_new_1x_12x.png': 'Comparison contains native commercial carpenter sprite; retain citation and hash only.',
}
DELIVERY_FILES = ['README_验收说明.md', 'review_config.json', 'layout_verification.json', 'build_review.py', 'package_sources.py', 'native_style_continuation_review_20261015.png', 'leiya_portrait_v2_74x100_candidate.png', 'tore_portrait_v1_74x100_candidate.png']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    sources = sorted(p for folder in SOURCE_DIRS for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    frozen = {str(p.relative_to(ROOT)): sha(p) for p in sources}
    entries = []
    omitted = []
    for p in sources:
        rel = str(p.relative_to(ROOT))
        item = {'path':rel,'size_bytes':p.stat().st_size,'sha256':sha(p)}
        if rel in EXCLUDED:
            item['omission_reason'] = EXCLUDED[rel]
            omitted.append(item)
        else:
            entries.append((p, rel, item))
    for name in DELIVERY_FILES:
        p=HERE/name
        assert p.is_file(), p
        rel='delivery/'+name
        entries.append((p,rel,{'path':rel,'size_bytes':p.stat().st_size,'sha256':sha(p)}))
    manifest = {
        'date':'2026-10-15', 'purpose':'Complete continuation source snapshot with explicitly documented commercial-reference omissions',
        'source_roots':SOURCE_DIRS, 'files':[item for _,_,item in entries], 'excluded_reference_files':omitted,
        'portrait_status':'candidate; not native_final; pending user aesthetic approval',
        'map_method_status':'fail; one generation; stopped; derived experimental image is not a qualified map asset',
        'runtime_integrated':False, 'runtime_verified':False,
        'no_commit_or_push':True,
        'reference_note':'Original commercial game pixels are not redistributed. Source manifests and prompts retain read-only reference paths, names and hashes; they may not resolve outside the original environment.'
    }
    manifest_bytes=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
    (HERE/'package_manifest.json').write_bytes(manifest_bytes)
    out=HERE/'native_style_continuation_sources_20261015.zip'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p,rel,_ in entries:
            z.write(p,'native_style_continuation/'+rel)
        z.writestr('native_style_continuation/delivery/package_manifest.json',manifest_bytes)
    checks=[]
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for p,rel,item in entries:
            name='native_style_continuation/'+rel
            payload=z.read(name)
            assert hashlib.sha256(payload).hexdigest()==item['sha256'],name
            info=z.getinfo(name)
            checks.append({'path':rel,'sha256':item['sha256'],'crc32':f'{info.CRC:08x}','size_bytes':info.file_size})
        assert all('native_style_continuation/'+rel not in z.namelist() for rel in EXCLUDED)
    assert frozen=={str(p.relative_to(ROOT)):sha(p) for p in sources}, 'Sources changed during packaging'
    assert out.stat().st_size < 18*1024*1024, 'Archive must be split below 18 MiB'
    report={'archive':out.name,'size_bytes':out.stat().st_size,'sha256':sha(out),'zip_crc_pass':True,'all_archived_sha256_match':True,'source_snapshot_unchanged':True,'archive_entries':len(checks)+1,'reference_pixels_excluded':omitted,'entries':checks}
    (HERE/'archive_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    deliverables=[HERE/name for name in DELIVERY_FILES if name.endswith('.png')]+[out]
    (HERE/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in deliverables))
    (HERE/'delivery_manifest.json').write_text(json.dumps({'date':'2026-10-15','files':[{'file_name':p.name,'size_bytes':p.stat().st_size,'sha256':sha(p)} for p in deliverables],'archive_verification':'archive_verification.json','layout_verification':'layout_verification.json','runtime_verified':False,'committed':False,'pushed':False},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['entries','reference_pixels_excluded']},ensure_ascii=False))

if __name__=='__main__':
    main()
