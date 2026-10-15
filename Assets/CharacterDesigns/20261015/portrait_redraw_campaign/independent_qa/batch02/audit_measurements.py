"""Independent read-only inspection; writes only next to this script.

Reconstructs the declared whole-canvas nearest-neighbor / alpha128 / median-cut
or maximum-coverage derivative without running author scripts or changing any
production source. The mode is explicit per author export, not auto-selected
for a better-looking or matching result.
"""
from pathlib import Path
from PIL import Image
from collections import Counter
from datetime import datetime, timezone
from io import BytesIO
import base64
import hashlib
import json

OUT = Path(__file__).resolve().parent
CAMPAIGN = OUT.parent.parent
REPO = CAMPAIGN.parents[3]
EXPECTED_DISPATCH = 'd72109a69feb3f797904b91a7befb80348a33c3e8fb4184b91c1a1e24e87e143'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def measure(p):
    with Image.open(p) as opened:
        mode = opened.mode
        im = opened.convert('RGBA')
    pixels = list(im.getdata())
    alphas = Counter(v[3] for v in pixels)
    colors = Counter(v[:3] for v in pixels if v[3])
    occupied = {(i % im.width, i // im.width) for i, p in enumerate(pixels) if p[3]} if im.width*im.height <= 10000 else set()
    connectivity = {}
    for neighborhood in [4,8]:
        sizes=[]
        unseen=set(occupied)
        while unseen:
            seed=unseen.pop(); todo=[seed]; size=1
            while todo:
                x,y=todo.pop()
                offsets=[(a,b) for a in [-1,0,1] for b in [-1,0,1] if (a or b) and (neighborhood==8 or abs(a)+abs(b)==1)]
                for a,b in offsets:
                    n=x+a,y+b
                    if n in unseen:
                        unseen.remove(n);todo.append(n);size+=1
            sizes.append(size)
        connectivity[neighborhood]=sorted(sizes,reverse=True) if im.width*im.height<=10000 else None
    return {
        'path': str(p.relative_to(REPO)), 'sha256': sha(p), 'size': list(im.size),
        'mode': mode, 'visible_rgb_colors': len(colors), 'alpha_values': sorted(alphas),
        'visible_pixels': sum(colors.values()), 'partial_alpha_pixels': sum(n for a,n in alphas.items() if a not in [0,255]),
        'alpha_bbox': im.getchannel('A').getbbox(),
        'transparent_rgb_nonzero_pixels': sum(1 for p in pixels if not p[3] and p[:3] != (0,0,0)),
        'alpha_connected_component_sizes_4way': connectivity[4],
        'alpha_connected_component_sizes_8way': connectivity[8],
    }

def independent_derivative(raw, quantizer):
    sampled = Image.open(raw).convert('RGBA').resize((74,100), Image.Resampling.NEAREST)
    alpha = sampled.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
    opaque_rgb = [p[:3] for p,a in zip(sampled.getdata(), alpha.getdata()) if a]
    strip = Image.new('RGB', (len(opaque_rgb),1))
    strip.putdata(opaque_rgb)
    palette = strip.quantize(colors=32, method=quantizer, dither=Image.Dither.NONE)
    result = sampled.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
    result.putalpha(alpha)
    result.putdata([p if p[3] else (0,0,0,0) for p in result.getdata()])
    return result

def source_checks(dispatch):
    entries = list(dispatch['style_references'])
    for c in dispatch['characters']:
        entries += c['current_cards'] + [c['identity_master'],c['master_selection_evidence']] + c['master_manifests'] + c['historical_boards']
    results = []
    for entry in entries:
        p = REPO / entry['path']
        results.append({'path':entry['path'], 'exists':p.exists(), 'sha256':sha(p) if p.exists() else None,
                        'expected_sha256':entry['sha256'], 'hash_match':p.exists() and sha(p)==entry['sha256']})
    return results

dispatch_path = CAMPAIGN / 'batch_02_next.json'
dispatch = json.loads(dispatch_path.read_text())
result = {'inspected_utc':datetime.now(timezone.utc).isoformat(), 'dispatch_revision':dispatch['frozen_dispatch_revision'],
          'dispatch_sha256':sha(dispatch_path), 'dispatch_hash_match':sha(dispatch_path)==EXPECTED_DISPATCH,
          'source_checks':source_checks(dispatch), 'characters':[],
          'method_limits':['Technical checks do not establish visual approval or native pixel authorship.',
                           'All source images are read-only. Derived checks write only into independent_qa/batch02.',
                           'The 32-color ceiling is temporary for this batch.']}
for c in dispatch['characters']:
    slug = c['suggested_slug']
    root = CAMPAIGN / slug
    entry = {'slug':slug, 'canonical_id':c['canonical_id'], 'name':c['name'], 'candidates':[]}
    for target in sorted((root/'candidates').glob('portrait_v*_74x100_candidate.png')):
        stem = target.name.split('_74x100_')[0]
        raw = root/'raw'/f'{stem}_raw_imagegen.png'
        returned = root/'tool_returns'/f'{stem}.json'
        m = {'target':measure(target), 'raw':measure(raw) if raw.exists() else None}
        m['tool_return_path'] = str(returned.relative_to(REPO))
        if returned.exists():
            ret = json.loads(returned.read_text())
            data = base64.b64decode(ret['image_url'].split(',',1)[1])
            m['tool_return_sha256'] = sha(returned)
            m['tool_return_decoded_image_sha256'] = hashlib.sha256(data).hexdigest()
            m['raw_equals_decoded_tool_return'] = raw.read_bytes()==data
        if raw.exists():
            quantizer = Image.Quantize.MAXCOVERAGE if slug in ['lyd','morlen'] else Image.Quantize.MEDIANCUT
            m['independent_quantizer'] = 'MAXCOVERAGE' if slug in ['lyd','morlen'] else 'MEDIANCUT'
            reproduced = independent_derivative(raw, quantizer)
            reproduced_path = OUT / f'{slug}_{stem}_independently_reproduced.png'
            reproduced.save(reproduced_path)
            m['independent_export_path'] = str(reproduced_path.relative_to(REPO))
            m['independent_export_sha256'] = sha(reproduced_path)
            m['reproduced_pixels_equal'] = reproduced.tobytes()==Image.open(target).convert('RGBA').tobytes()
            m['reproduced_png_bytes_equal'] = reproduced_path.read_bytes()==target.read_bytes()
        tm = m['target']
        m['technical_pass'] = tm['size']==[74,100] and tm['visible_rgb_colors']<=32 and set(tm['alpha_values'])<={0,255} and m.get('raw_equals_decoded_tool_return',False) and m.get('reproduced_pixels_equal',False)
        entry['candidates'].append(m)
    manifest = root/'manifest.json'
    if manifest.exists():
        declared = json.loads(manifest.read_text())
        checks=[]
        for f in declared.get('files',[]):
            p=root/f['path']
            checks.append({'path':f['path'],'exists':p.exists(),'hash_match':p.exists() and sha(p)==f['sha256']})
        entry['manifest_sha256']=sha(manifest)
        entry['manifest_file_checks']=checks
        entry['declared_selected_portrait']=declared.get('selected_portrait')
        entry['declared_generation_calls']=declared.get('generation_calls')
        entry['declared_native_authored']=declared.get('native_authored')
        entry['manifest_all_file_hashes_match']=all(f['hash_match'] for f in checks)
        selected=declared.get('selected_portrait')
        if selected:
            selected_path=root/selected
            entry['selected_path_exists']=selected_path.exists()
            entry['selected_sha256']=sha(selected_path) if selected_path.exists() else None
            selected_hash=declared.get('selected_sha256', declared.get('selected_portrait_sha256'))
            entry['selected_hash_matches_manifest']=selected_path.exists() and sha(selected_path)==selected_hash
        entry['tool_return_count']=len(list((root/'tool_returns').glob('portrait_v*.json')))
        entry['generation_count_matches_returns']=entry['tool_return_count']==declared.get('generation_calls')
        entry['within_two_generation_limit']=entry['tool_return_count']<=2
    sources=root/'sources'/'source_manifest.json'
    if sources.exists():
        s=json.loads(sources.read_text())
        copy_checks=[]
        for item in s.get('sources',s.get('inputs',[])):
            copied=item.get('copy',item.get('snapshot'))
            if not all(k in item for k in ['source','sha256']) or not copied:
                continue
            original=REPO/item['source']; copy=root/copied
            copy_checks.append({'source':item['source'],'copy':copied,'source_hash_match':original.exists() and sha(original)==item['sha256'], 'copy_hash_match':copy.exists() and sha(copy)==item['sha256'], 'copy_bytes_equal_source':original.exists() and copy.exists() and original.read_bytes()==copy.read_bytes()})
        entry['source_copy_checks']=copy_checks
        entry['source_copy_count']=len(copy_checks)
        entry['source_copies_all_match']=bool(copy_checks) and all(i['source_hash_match'] and i['copy_hash_match'] and i['copy_bytes_equal_source'] for i in copy_checks)
        current=s.get('current_authoritative_assignment')
        if current:
            entry['source_manifest_dispatch_matches_frozen']=current.get('revision')==2 and current.get('sha256')==EXPECTED_DISPATCH
        elif 'dispatch_sha256' in s:
            entry['source_manifest_dispatch_matches_frozen']=s.get('revision')==2 and s.get('dispatch_sha256')==EXPECTED_DISPATCH
    sums=root/'SHA256SUMS.txt'
    if sums.exists():
        bad=[]
        for line in sums.read_text().splitlines():
            if not line.strip():continue
            h,relative=line.split('  ',1)
            p=root/relative
            if not p.exists() or sha(p)!=h: bad.append(relative)
        entry['sha256sums_mismatches']=bad
        entry['sha256sums_all_match']=not bad
    result['characters'].append(entry)
out=OUT/'independent_measurements.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'output':str(out.relative_to(REPO)), 'dispatch_hash_match':result['dispatch_hash_match'],
                  'all_source_hashes_match':all(s['hash_match'] for s in result['source_checks']),
                  'candidates':[{'slug':c['slug'],'targets':[{'sha256':m['target']['sha256'],'size':m['target']['size'],'colors':m['target']['visible_rgb_colors'],'technical_pass':m['technical_pass'],'reproduced_bytes_equal':m.get('reproduced_png_bytes_equal')} for m in c['candidates']], 'manifest_files_match':c.get('manifest_all_file_hashes_match')} for c in result['characters']]},ensure_ascii=False,indent=2))
