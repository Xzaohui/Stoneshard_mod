from pathlib import Path
from PIL import Image
from collections import Counter
import json,hashlib,base64,datetime,sys
root=Path(__file__).resolve().parent
repo=next(p for p in root.parents if (p/'AGENTS.md').exists())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
selected=sys.argv[1] if len(sys.argv)>1 else 'portrait_v1'
roster=json.loads((root/'sources/roster_entry.json').read_text())
source=json.loads((root/'sources/source_manifest.json').read_text())
preservation=[]
for s in source:
 p=repo/s['original_path']; q=root/s['snapshot_path']
 preservation.append({**s,'current_original_sha256':sha(p),'snapshot_sha256':sha(q),'original_unchanged':sha(p)==s['sha256'],'snapshot_matches_original':sha(p)==sha(q)})
(root/'qa/source_preservation.json').write_text(json.dumps({'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_original_sources_unchanged':all(x['original_unchanged'] and x['snapshot_matches_original'] for x in preservation),'checks':preservation,'roster_card_sha_matches':sha(repo/roster['current_cards'][0]['path'])==roster['current_cards'][0]['sha256'],'roster_identity_sha_matches':sha(repo/roster['identity_master']['path'])==roster['identity_master']['sha256']},ensure_ascii=False,indent=2))
ledger=[];reproduction=[];assets=[]
for p in sorted((root/'tool_returns').glob('portrait_v*.json')):
 name=p.stem;ret=json.loads(p.read_text());raw=root/'raw'/f'{name}_raw_imagegen.png';prompt=root/'prompts'/f'{name}.json';target=root/'candidates'/f'{name}_74x100_candidate.png'
 raw_data=base64.b64decode(ret['image_url'].split(',',1)[1]);args=json.loads(prompt.read_text())
 ledger.append({'version':name,'built_in_tool':'image_gen.imagegen','tool_parameters':str(prompt.relative_to(root)),'prompt_sha256':sha(prompt),'tool_return':str(p.relative_to(root)),'tool_return_sha256':sha(p),'raw':str(raw.relative_to(root)),'raw_sha256':sha(raw),'raw_equals_full_tool_return':raw.read_bytes()==raw_data,'tool_output_hint':ret.get('output_hint'),'reference_inputs':[{'path':ref,'sha256':sha(Path(ref))} for ref in args.get('referenced_image_paths',[])],'transparent_background':args.get('transparent_background'),'target_generation_native_resolution':False})
 im=Image.open(raw).convert('RGBA').resize((74,100),Image.Resampling.NEAREST);alpha=im.getchannel('A').point(lambda a:255 if a>=128 else 0);visible=[px[:3] for px,a in zip(im.getdata(),alpha.getdata()) if a]
 strip=Image.new('RGB',(len(visible),1));strip.putdata(visible);pal=strip.quantize(colors=32,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE)
 q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha);q.putdata([px if px[3] else (0,0,0,0) for px in q.getdata()])
 actual=Image.open(target).convert('RGBA');reproduction.append({'version':name,'dimensions_match':q.size==actual.size,'pixel_rgba_exact_match':q.tobytes()==actual.tobytes(),'source_raw_sha256':sha(raw),'target_sha256':sha(target),'method':'Pillow NEAREST full canvas 74x100; alpha threshold128; opaque RGB MAXCOVERAGE palette32; NONE dithering; transparent RGB0'})
 assets.append(json.loads((root/'qa'/f'{name}_metrics.json').read_text()))
(root/'qa/generation_ledger.json').write_text(json.dumps({'maximum_successful_generated_versions':2,'successful_image_generations':len(ledger),'input_validation_failures':1,'total_tool_request_attempts':len(ledger)+1,'validation_failure_record':'qa/v2_validation_retry.json','no_extra_image_generation':len(ledger)<=2,'generations':ledger},ensure_ascii=False,indent=2))
(root/'qa/reproducibility.json').write_text(json.dumps({'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_derivatives_pixel_exact':all(x['pixel_rgba_exact_match'] for x in reproduction),'generator_not_deterministic':True,'checks':reproduction},ensure_ascii=False,indent=2))
ind=root/'qa/independent_selection_summary.json'; independent=json.loads(ind.read_text()) if ind.exists() else {'decision':'pending','native_art_final_approved':False,'runtime_verified':False}
manifest={'schema_version':1,'actor_id':roster['canonical_id'],'name':roster['name'],'date':'2026-10-15','selected_version':selected,'selected_portrait':f'candidates/{selected}_74x100_candidate.png','selected_portrait_sha256':sha(root/'candidates'/f'{selected}_74x100_candidate.png'),'selected_raw':f'raw/{selected}_raw_imagegen.png','selected_raw_sha256':sha(root/'raw'/f'{selected}_raw_imagegen.png'),'selected_preview':f'previews/{selected}_1x_8x.png','generation_calls':len(ledger),'generation_calls_definition':'successful image-producing calls; rejected input validation is separately recorded','total_tool_request_attempts':len(ledger)+1,'maximum_successful_generated_versions':2,'native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'status':independent['decision'],'independent_qa':independent,'color_budget_note':'32 visible RGB colors is this batch temporary ceiling, not a project-wide hard lock; numerical quantization does not prove designed ramp quality','method':'Built-in imagegen full raw preserved; full-canvas NEAREST resize, binary alpha threshold128, nondithered MAXCOVERAGE <=32-color derivative. No manual pixel painting.','assets':assets,'generation_ledger':'qa/generation_ledger.json','mechanical_reproduction':'qa/reproducibility.json','actual_source_hash_validation':'qa/source_preservation.json','source_files_frozen_for_delivery':independent['decision']!='pending','image_generation_frozen':independent['decision']!='pending','residuals':independent.get('notes',[])}
manifest['files']=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS.txt']]
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(root/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(root)}' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')+'\n')
print(json.dumps({'slug':root.name,'status':manifest['status'],'selected':selected,'source_unchanged':all(x['original_unchanged'] for x in preservation),'reproduced':all(x['pixel_rgba_exact_match'] for x in reproduction),'calls':len(ledger)},ensure_ascii=False))
