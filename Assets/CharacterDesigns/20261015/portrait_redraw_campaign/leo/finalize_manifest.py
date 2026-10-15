from pathlib import Path
import hashlib,json,sys
root=Path(sys.argv[1]);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((root/'manifest.json').read_text())
m['selected_portrait']='candidates/portrait_v2_74x100_candidate.png'
m['selected_sha256']=sha(root/m['selected_portrait'])
m['selected_preview']='previews/portrait_v2_1x_8x.png'
m['selected_integer_preview']='previews/portrait_v2_8x.png'
m['production_status']='frozen_candidate_visual_selected_technical_qa_pending'
m['independent_qa']={'visual':'v2_selected_as_candidate','technical':'pending_frozen_asset_recheck','selection_summary':'qa/independent_selection_summary.json'}
m['generation_calls']=2
m['tool_invocations']=3 if root.name=='hers' else 2
m['nonrendering_rejections']=1 if root.name=='hers' else 0
m['rejected_call_note']='The initial v2 call with six references failed parameter validation before image generation. Full parameters and exact error preserved.' if root.name=='hers' else None
m['selected_version_rationale']='v2 broadens grey hair masses and consolidates stubble; preserves older lean identity and controlled narrow gaze.' if root.name=='hers' else 'v2 removes heavy continuous beard, restores short stubble, reduces neck exposure and simplifies hair; preserves mature brown-haired blue-steel identity.'
m['full_prompt_parameters']=['prompts/portrait_v1.json','prompts/portrait_v2.json']
m['source_manifest']='sources/source_manifest.json'
m['source_hash_verification']='qa/source_hash_verification.json'
m['author_visual_review']='qa/author_visual_review.json'
m['old_art_modified']=False;m['character_cards_modified']=False;m['code_modified']=False;m['commit_performed']=False;m['push_performed']=False
m['files']=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ('manifest.json','SHA256SUMS.txt')]
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(root/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(root)}' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')+'\n')
print(json.dumps({'root':str(root),'selected_sha256':m['selected_sha256'],'files':len(m['files'])},ensure_ascii=False))
