from pathlib import Path
import json,hashlib,datetime
r=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((r/'manifest.json').read_text())
s=json.loads((r/'selection.json').read_text())
m.update({'selected_portrait':s['selected_portrait'],'selected_portrait_sha256':sha(r/s['selected_portrait']),'independent_qa':s['independent_qa'],'generation_calls':len(list((r/'tool_returns').glob('portrait_v*.json'))),'max_attempts':2})
inputs=[]
for p in sorted((r/'prompts').glob('portrait_v*.json')):
 args=json.loads(p.read_text());entries=[]
 for ref in args['referenced_image_paths']:
  rp=Path(ref);entries.append({'path':str(rp.relative_to(r)),'sha256':sha(rp),'bytes':rp.stat().st_size})
 inputs.append({'prompt_path':str(p.relative_to(r)),'prompt_sha256':sha(p),'inputs':entries,'tool':'image_gen__imagegen','transparent_background':args['transparent_background']})
m['generation_input_hashes']=inputs
m['files']=[{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(r.rglob('*')) if p.is_file() and p.name not in ('manifest.json','SHA256SUMS.txt')]
(r/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2));(r/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(r)}' for p in sorted(r.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')+'\n')
assert all(sha(r/f['path'])==f['sha256'] for f in m['files'])
print(json.dumps({'selected':m['selected_portrait'],'sha256':m['selected_portrait_sha256'],'listed_files':len(m['files']),'decision':m['independent_qa']},ensure_ascii=False))
