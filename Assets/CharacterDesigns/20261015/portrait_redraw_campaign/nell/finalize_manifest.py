from pathlib import Path
import json,hashlib,sys,base64
p=Path(sys.argv[1]);who=p.name
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
review=json.loads((p/'qa/independent_selection_summary.json').read_text())
selected=review['selected_portrait']
m=json.loads((p/'manifest.json').read_text())
m.update({'source_commit':'4df549adfb9fd133399adc4702791727bac4bd08','scope':'One standalone dialogue portrait; not map sprite, body, equipment layer or game integration','selected_portrait':selected,'selected_portrait_sha256':sha(p/selected),'selected_preview':review['selected_preview'],'generation_calls':2,'max_attempts':2,'generation_limit_exhausted':True,'image_generation_frozen':True,'source_files_frozen_for_delivery':True,'independent_qa':{'selection_status':'candidate_selected_after_independent_visual_review','native_art_final_approved':False,'runtime_verified':False,'review_summary_file':'qa/independent_selection_summary.json','formal_report':review.get('formal_report','separate independent first-batch QA report')},'selected_export':{'version':'v2','palette_method':review.get('palette_method','Pillow MAXCOVERAGE'),'dither':False,'resize':'whole-canvas NEAREST to 74x100','alpha_threshold':128,'crop':None,'shape_painting':False,'native_pixel_authorship_claim':False},'earlier_exports_retained':[a['target']['path'] for a in m['assets'] if a['target']['path']!=selected], 'notes':review['limitations']})
# Verify unchanged raw payloads and all input snapshots before freezing metadata.
verification=[]
for i in ('v1','v2'):
 ret=json.loads((p/'tool_returns'/f'portrait_{i}.json').read_text()); raw=p/'raw'/f'portrait_{i}_raw_imagegen.png'
 original_path=ret['output_hint'].split(' as ',1)[1].split(' by default.',1)[0]
 verification.append({'version':i,'raw':str(raw.relative_to(p)),'sha256':sha(raw),'matches_tool_return':raw.read_bytes()==base64.b64decode(ret['image_url'].split(',',1)[1]),'matches_original_generated_file':raw.read_bytes()==Path(original_path).read_bytes(),'original_generated_file':original_path})
 inputs=json.loads((p/'sources/source_manifest.json').read_text())
 for arg in json.loads((p/'prompts'/f'portrait_{i}.json').read_text())['referenced_image_paths']:
  pp=Path(arg); rel=str(pp.relative_to(p.resolve()))
  expected=next((a['sha256'] for a in inputs if a['snapshot']==rel), None)
  verification.append({'version':i,'image_input':rel,'sha256':sha(pp),'source_snapshot_matches_record':sha(pp)==expected if expected else None,'note':'Revision raw input is preserved and hashed above' if not expected else ''})
(p/'qa/provenance_verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2))
m['files']=[{'path':str(q.relative_to(p)),'bytes':q.stat().st_size,'sha256':sha(q)} for q in sorted(p.rglob('*')) if q.is_file() and q.name not in ('manifest.json','SHA256SUMS.txt')]
(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(p/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(q)}  {q.relative_to(p)}' for q in sorted(p.rglob('*')) if q.is_file() and q.name!='SHA256SUMS.txt')+'\n')
print(json.dumps({'actor':who,'selected':selected,'sha256':sha(p/selected),'files':len(m['files']),'raw_verified':all(x.get('matches_tool_return',True) and x.get('matches_original_generated_file',True) for x in verification)},ensure_ascii=False))
