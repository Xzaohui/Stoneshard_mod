#!/usr/bin/env python3
"""Independent audit. Read-only production inputs; output confined to this folder."""
from pathlib import Path
from PIL import Image
import base64, collections, datetime, hashlib, json, re, sys

OUT = Path(__file__).resolve().parent
CAMP = OUT.parent.parent
REPO = CAMP.parents[3]
SLUGS = ('vit', 'wolen', 'yani', 'rukan')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def metrics(path):
    original = Image.open(path)
    image = original.convert('RGBA')
    pixels = list(image.getdata())
    colors = collections.Counter(p[:3] for p in pixels if p[3])
    alpha = collections.Counter(p[3] for p in pixels)
    strong_alpha = image.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
    strong_bbox = strong_alpha.getbbox()
    return dict(sha256=sha(path), bytes=path.stat().st_size, size=list(image.size),
                mode=original.mode, visible_rgb_colors=len(colors), alpha_values=sorted(alpha),
                alpha128_bbox=strong_bbox,
                alpha128_margins=None if strong_bbox is None else [strong_bbox[0], strong_bbox[1], image.width - strong_bbox[2], image.height - strong_bbox[3]],
                border_max_alpha={
                    'left': max(image.getpixel((0, y))[3] for y in range(image.height)),
                    'right': max(image.getpixel((image.width-1, y))[3] for y in range(image.height)),
                    'top': max(image.getpixel((x, 0))[3] for x in range(image.width)),
                    'bottom': max(image.getpixel((x, image.height-1))[3] for x in range(image.width))},
                partial_alpha_pixels=sum(n for a, n in alpha.items() if a not in (0, 255)),
                alpha_bbox=image.getchannel('A').getbbox(), visible_pixels=sum(colors.values()),
                opaque_frame_edge_pixels={edge: points for edge, points in [('left', [y for y in range(image.height) if image.getpixel((0,y))[3]]), ('right', [y for y in range(image.height) if image.getpixel((image.width-1,y))[3]]), ('top', [x for x in range(image.width) if image.getpixel((x,0))[3]]), ('bottom', [x for x in range(image.width) if image.getpixel((x,image.height-1))[3]])]},
                transparent_rgb_zero=all(p[:3] == (0, 0, 0) for p in pixels if p[3] == 0))

def reproduce(raw, method, containment=False):
    source = Image.open(raw).convert('RGBA')
    if containment:
        scale = min(72 / source.width, 98 / source.height)
        fitted = (round(source.width * scale), round(source.height * scale))
        sampled = source.resize(fitted, Image.Resampling.NEAREST)
        canvas = Image.new('RGBA', (74, 100), (0,0,0,0))
        canvas.paste(sampled, ((74 - fitted[0]) // 2, (100 - fitted[1]) // 2))
        sampled = canvas
    else:
        sampled = source.resize((74, 100), Image.Resampling.NEAREST)
    alpha = sampled.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
    colors = [p[:3] for p, a in zip(sampled.getdata(), alpha.getdata()) if a]
    strip = Image.new('RGB', (len(colors), 1))
    strip.putdata(colors)
    palette = strip.quantize(colors=32, method=getattr(Image.Quantize, method), dither=Image.Dither.NONE)
    result = sampled.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
    result.putalpha(alpha)
    result.putdata([p if p[3] else (0, 0, 0, 0) for p in result.getdata()])
    return result

report = dict(audit_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), scope=list(SLUGS),
              read_only_inputs=True, native_pixel_approval=False, runtime_verified=False,
              actors={}, hard_errors=[], pending=[])
for slug in SLUGS:
    root = CAMP / slug
    actor = dict(sources=[], raw_integrity=[], nongenerating_tool_records=[], candidates=[], manifest={}, errors=[], pending=[])
    report['actors'][slug] = actor
    source_data = json.loads((root / 'sources/source_manifest.json').read_text())
    sources = source_data if isinstance(source_data, list) else source_data.get('sources', source_data.get('items', []))
    sources = [dict(record, source=record.get('source', record.get('source_path', record.get('original_path', record.get('path')))), snapshot=record.get('copy', record.get('snapshot', record.get('snapshot_path')))) for record in sources]
    for record in sources:
        source = REPO / record['source']
        snapshot = root / (record.get('copy') or record['snapshot'])
        row = dict(source=record['source'], snapshot=str(snapshot.relative_to(root)),
                   source_exists=source.exists(), snapshot_exists=snapshot.exists(), expected_sha256=record['sha256'])
        if source.exists() and snapshot.exists():
            row.update(source_sha256=sha(source), snapshot_sha256=sha(snapshot),
                       byte_identical=source.read_bytes() == snapshot.read_bytes(),
                       hash_matches=sha(source) == sha(snapshot) == record['sha256'])
        if not row.get('hash_matches'):
            actor['errors'].append('source mismatch: ' + record['source'])
        actor['sources'].append(row)
    for ret in sorted((root / 'tool_returns').glob('*.json')):
        result = json.loads(ret.read_text())
        if 'image_url' not in result:
            actor['nongenerating_tool_records'].append(dict(path=str(ret.relative_to(root)), sha256=sha(ret), record=result))
            if not ('validation' in ret.stem and 'must contain at most 5' in str(result.get('error', result))):
                actor['errors'].append('unrecognized tool record without image: ' + ret.name)
            continue
        raw = root / 'raw' / (ret.stem + '_raw_imagegen.png')
        data = base64.b64decode(result['image_url'].split(',', 1)[1], validate=True)
        row = dict(version=ret.stem, tool_return_sha256=sha(ret),
                   tool_payload_sha256=hashlib.sha256(data).hexdigest(), raw=str(raw.relative_to(root)),
                   raw_equals_tool_payload_bytes=raw.exists() and raw.read_bytes() == data)
        if raw.exists():
            row['raw_metrics'] = metrics(raw)
        row['tool_originals'] = []
        for name in sorted(set(re.findall(r'/workspace/[^\s]+\.png', result.get('output_hint', '')))):
            path = Path(name)
            original = dict(path=name, exists=path.exists(), sha256=sha(path) if path.exists() else None,
                            equals_tool_bytes=path.exists() and path.read_bytes() == data)
            row['tool_originals'].append(original)
            if path.exists() and not original['equals_tool_bytes']:
                actor['errors'].append('generated original differs: ' + name)
        prompt = root / 'prompts' / (ret.stem + '.json')
        row['prompt_exists'] = prompt.exists()
        if prompt.exists():
            prompt_wrapper = json.loads(prompt.read_text())
            prompt_data = prompt_wrapper.get('arguments', prompt_wrapper)
            row['prompt_sha256'] = sha(prompt)
            row['prompt_reference_checks'] = [dict(path=p, exists=Path(p).exists(), sha256=sha(Path(p)) if Path(p).exists() else None) for p in prompt_data.get('referenced_image_paths', [])]
            row['prompt_reference_paths_exist'] = bool(row['prompt_reference_checks']) and all(x['exists'] for x in row['prompt_reference_checks'])
            row['transparent_background_requested'] = prompt_data.get('transparent_background')
            if not row['prompt_reference_paths_exist']:
                actor['errors'].append('generation reference path missing: ' + ret.stem)
            if row['transparent_background_requested'] is not True:
                actor['errors'].append('transparent background not requested: ' + ret.stem)
        if not row['raw_equals_tool_payload_bytes']:
            actor['errors'].append('raw differs from tool return: ' + ret.stem)
        if not row['prompt_exists']:
            actor['errors'].append('missing generation parameters: ' + ret.stem)
        actor['raw_integrity'].append(row)
    if len(actor['raw_integrity']) > 2:
        actor['errors'].append('more than two generation calls saved')
    for candidate in sorted((root / 'candidates').glob('portrait_v*_74x100_candidate.png')):
        version = re.match(r'portrait_v\d+', candidate.name).group(0)
        raw = root / 'raw' / (version + '_raw_imagegen.png')
        image = Image.open(candidate).convert('RGBA')
        matching = []
        for method in ('MEDIANCUT', 'MAXCOVERAGE'):
            reproduced = reproduce(raw, method, containment='containment' in candidate.name)
            if image.size == reproduced.size and image.tobytes() == reproduced.tobytes():
                matching.append(method)
                destination = OUT / (slug + '_' + candidate.stem + '_independently_reproduced.png')
                reproduced.save(destination)
        row = metrics(candidate)
        row.update(path=str(candidate.relative_to(root)), independently_matching_methods=matching,
                   pixel_reproduction_pass=bool(matching),
                   technical_containment_padding='containment' in candidate.name,
                   specification_pass=row['size'] == [74, 100] and row['visible_rgb_colors'] <= 32 and set(row['alpha_values']) <= {0, 255})
        if matching:
            row.update(reproduced_sha256=sha(destination), png_byte_identical=candidate.read_bytes() == destination.read_bytes())
        preview = root / 'previews' / candidate.name.replace('_74x100_candidate', '_8x')
        row['preview_exists'] = preview.exists()
        row['preview_exact_8x_nearest_neighbor'] = preview.exists() and Image.open(preview).convert('RGBA').size == (592, 800) and Image.open(preview).convert('RGBA').tobytes() == image.resize((592, 800), Image.Resampling.NEAREST).tobytes()
        if not (row['specification_pass'] and row['pixel_reproduction_pass'] and row.get('png_byte_identical') and row['preview_exact_8x_nearest_neighbor']):
            actor['errors'].append('candidate failed: ' + candidate.name)
        actor['candidates'].append(row)
    manifest = root / 'manifest.json'
    if manifest.exists():
        data = json.loads(manifest.read_text())
        checks = []
        records = data.get('files', [])
        if isinstance(records, dict):
            records = [dict(path=key, sha256=value) if isinstance(value, str) else dict(path=key, **value) for key, value in records.items()]
        for item in records:
            path = root / item['path']
            checks.append(dict(path=item['path'], exists=path.exists(),
                               hash_matches=path.exists() and sha(path) == item['sha256'],
                               bytes_match=path.exists() and path.stat().st_size == item.get('bytes', path.stat().st_size)))
        selected = data.get('selected_portrait') or data.get('selected_candidate')
        selected_hash = data.get('selected_portrait_sha256') or data.get('selected_sha256') or data.get('selected_candidate_sha256')
        actor['manifest'] = dict(path=str(manifest.relative_to(CAMP)), sha256=sha(manifest), selected=selected,
                                 recorded_selected_sha256=selected_hash, file_checks=checks,
                                 generation_calls=data.get('generation_calls', data.get('generation', {}).get('attempts')), actual_tool_returns=len(actor['raw_integrity']))
        actor['manifest']['boundary_flags'] = {key: data.get(key, data.get('method', {}).get(key) if isinstance(data.get('method'), dict) else None) for key in ('native_authored', 'native_pixel_approved', 'runtime_integrated', 'runtime_verified')}
        if any(data.get(key) is True for key in ('native_authored', 'native_pixel_approved', 'runtime_integrated', 'runtime_verified')):
            actor['errors'].append('manifest overstates native or runtime approval')
        all_files = {str(x.relative_to(root)) for x in root.rglob('*') if x.is_file() and '__pycache__' not in x.parts}
        exempt = {'manifest.json', 'SHA256SUMS', 'SHA256SUMS.txt'}
        actor['manifest']['files_not_listed'] = sorted(all_files - {x['path'] for x in records} - exempt)
        if actor['manifest']['files_not_listed']:
            actor['pending'].append('manifest omits current files: ' + ', '.join(actor['manifest']['files_not_listed']))
        if selected:
            selected_path = root / selected
            actor['manifest'].update(selected_actual_sha256=sha(selected_path), selected_hash_matches=sha(selected_path) == selected_hash)
            selected_metrics = metrics(selected_path)
            actor['manifest']['selected_has_fully_transparent_frame'] = not any(selected_metrics['border_max_alpha'].values())
            if not actor['manifest']['selected_has_fully_transparent_frame']:
                actor['pending'].append('selected candidate has visible frame-edge pixels')
            if not actor['manifest']['selected_hash_matches']:
                actor['pending' if selected_hash is None else 'errors'].append('manifest selected hash missing or mismatch')
        else:
            actor['errors'].append('manifest missing selected portrait')
        if data.get('generation_calls', data.get('generation', {}).get('attempts')) != len(actor['raw_integrity']):
            actor['errors'].append('manifest generation count mismatch')
        actor['errors'].extend('manifest file mismatch: ' + x['path'] for x in checks if not (x['hash_matches'] and x['bytes_match']))
        input_checks = []
        for generation in data.get('generation_input_hashes', []):
            prompt = root / generation['prompt_path']
            prompt_matches = prompt.exists() and sha(prompt) == generation['prompt_sha256']
            inputs = [dict(path=item['path'], hash_matches=(root / item['path']).exists() and sha(root / item['path']) == item['sha256'], bytes_match=(root / item['path']).exists() and (root / item['path']).stat().st_size == item['bytes']) for item in generation['inputs']]
            input_checks.append(dict(prompt=generation['prompt_path'], prompt_hash_matches=prompt_matches, inputs=inputs))
            if not prompt_matches or not all(x['hash_matches'] and x['bytes_match'] for x in inputs):
                actor['errors'].append('manifest generation input mismatch: ' + generation['prompt_path'])
        actor['manifest']['generation_input_hash_checks'] = input_checks
    else:
        actor['pending'].append('manifest missing')
    sums = root / 'SHA256SUMS.txt'
    if not sums.exists():
        sums = root / 'SHA256SUMS'
    actor['SHA256SUMS'] = []
    if sums.exists():
        for line in sums.read_text().splitlines():
            if not line.strip():
                continue
            expected, name = line.split(maxsplit=1)
            path = root / name.lstrip('*')
            item = dict(path=name, hash_matches=path.exists() and sha(path) == expected)
            actor['SHA256SUMS'].append(item)
            if not item['hash_matches']:
                actor['errors'].append('SHA256SUMS mismatch: ' + name)
    else:
        actor['pending'].append('SHA256SUMS missing')
    if not actor['raw_integrity']:
        actor['pending'].append('raw not yet available')
    if not actor['candidates']:
        actor['pending'].append('candidate not yet available')
    report['hard_errors'].extend(slug + ': ' + x for x in actor['errors'])
    report['pending'].extend(slug + ': ' + x for x in actor['pending'])
report['all_available_technical_checks_pass'] = not report['hard_errors']
report['all_technical_checks_complete'] = not report['hard_errors'] and not report['pending']
target = OUT / (sys.argv[1] if len(sys.argv) > 1 else 'technical_audit.json')
target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({key: report[key] for key in ('audit_utc', 'all_available_technical_checks_pass', 'all_technical_checks_complete', 'hard_errors', 'pending')}, ensure_ascii=False, indent=2))
