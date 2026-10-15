from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.load(open(r/'manifest.json'));s=json.load(open(r/'selection.json'))
m.update(s)
m['selected_portrait_sha256']=sha(r/s['selected_portrait'])
m['selected_raw_sha256']=sha(r/s['selected_raw'])
m['candidate_status']=s['status']
m['image_generation_frozen']=True
m['source_files_frozen_for_delivery']=True
m['generation_calls']=len(list((r/'tool_returns').glob('portrait_v*.json')))
m['completed_generation_versions']=[p.stem for p in sorted((r/'tool_returns').glob('portrait_v*.json'))]
m['superseded_unexecuted_prompt_drafts']=[str(p.relative_to(r)) for p in sorted((r/'prompts').glob('*not_executed.json'))]
m['actual_source_hash_validation']='qa/source_preservation.json'
m['generation_ledger']='qa/generation_ledger.json'
m['mechanical_reproduction']='qa/reproducibility.json'
m['independent_qa']=json.load(open(r/'qa/independent_selection_summary.json'))
m['native_authored']=False
m['native_art_final_approved']=False
m['runtime_integrated']=False
m['runtime_verified']=False
m['selected_export']={'version':s['selected_version'],'raw':s['selected_raw'],'palette_method':'Pillow '+s['palette_method'],'dither':False,'resize':'whole-canvas NEAREST to 74x100','alpha_threshold':128,'shape_painting':False,'native_pixel_authorship_claim':False}
m['mechanical_alternate_exports']=[json.load(open(p)) for p in sorted((r/'qa').glob('*mediancut_metrics.json'))]
m['files']=[{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(r.rglob('*')) if p.is_file() and p.name not in ('manifest.json','SHA256SUMS.txt')]
(r/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(r/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(r)}\n' for p in sorted(r.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt'))
print(r.name,m['generation_calls'],m['selected_portrait_sha256'])
