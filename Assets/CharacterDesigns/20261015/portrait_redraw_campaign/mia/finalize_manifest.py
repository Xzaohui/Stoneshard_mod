from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review_path=root/'qa/independent_selection_summary.json'
assert review_path.exists(), 'Independent selection required before freeze'
review=json.loads(review_path.read_text())
assert review.get('selection_status')=='candidate_selected_after_independent_visual_review'
manifest=json.loads((root/'manifest.json').read_text())
selected=review['selected_portrait']; assert (root/selected).exists()
manifest.update({'selected_portrait':selected,'selected_portrait_sha256':sha(root/selected),'selected_preview':review['selected_preview'],'image_generation_frozen':True,'source_files_frozen_for_delivery':True,'generation_calls':2,'generation_limit_exhausted':True,'independent_qa':review,'native_art_final_approved':False,'selected_export':{'version':'v2','palette_method':'Pillow MAXCOVERAGE' if 'maxcoverage' in selected else 'Pillow MEDIANCUT','dither':False,'resize':'whole-canvas NEAREST to 74x100','alpha_threshold':128,'shape_painting':False,'native_pixel_authorship_claim':False},'mechanical_export_alternative':json.loads((root/'qa/portrait_v2_maxcoverage_metrics.json').read_text()),'earlier_exports_retained':['candidates/portrait_v1_74x100_candidate.png','candidates/portrait_v2_74x100_candidate.png']})
manifest['files']=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ('manifest.json','SHA256SUMS.txt')]
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(root/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(root)}' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')+'\n')
for e in manifest['files']: assert sha(root/e['path'])==e['sha256']
for e in json.loads((root/'sources/source_manifest.json').read_text()): assert sha(Path(e['source']))==e['sha256']
print(json.dumps({'selected':selected,'sha256':manifest['selected_portrait_sha256'],'all_manifest_hashes_verified':True,'all_original_source_hashes_unchanged':True},ensure_ascii=False))

