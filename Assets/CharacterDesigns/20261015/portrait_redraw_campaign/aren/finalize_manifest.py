from pathlib import Path
import hashlib,json,base64
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((root/'manifest.json').read_text())
m['selected_portrait']='candidates/portrait_v2_maxcoverage_74x100_candidate.png'
m['selected_raw']='raw/portrait_v2_raw_imagegen.png'
m['generation_calls']=2
m['revision_count']=1
m['generation_method']='built-in image_gen__imagegen'
m['selected_metrics']=json.loads((root/'qa/portrait_v2_maxcoverage_metrics.json').read_text())
m['author_qa']='qa/author_v2_review.json'
qa=root/'qa/independent_final_review.json'
if qa.exists():
 m['independent_qa']='qa/independent_final_review.json'
 m['status']=json.loads(qa.read_text())['status']
else:
 m['independent_qa']='pending'
 m['status']='selected_v2_waiting_independent_final_QA'
m['raw_validation']={}
for v in ['portrait_v1','portrait_v2']:
 raw=root/'raw'/f'{v}_raw_imagegen.png';ret=json.loads((root/'tool_returns'/f'{v}.json').read_text());args=json.loads((root/'prompts'/f'{v}.json').read_text())
 m['raw_validation'][v]={'sha256':sha(raw),'byte_identical_to_full_tool_return':raw.read_bytes()==base64.b64decode(ret['image_url'].split(',',1)[1]),'actual_parameters_file':f'prompts/{v}.json','input_files':args['referenced_image_paths'],'transparent_background':args['transparent_background']}
m['files']=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS.txt']]
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(root/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(root)}' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')+'\n')
print(json.dumps({'slug':root.name,'status':m['status'],'selected':m['selected_portrait'],'sha256':sha(root/m['selected_portrait'])},ensure_ascii=False))
