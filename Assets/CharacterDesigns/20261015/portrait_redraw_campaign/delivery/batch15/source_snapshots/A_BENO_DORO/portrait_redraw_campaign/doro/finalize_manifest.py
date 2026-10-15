#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=root/'manifest.json';m=json.loads(p.read_text())
m['files']=[{'path':str(x.relative_to(root)),'bytes':x.stat().st_size,'sha256':sha(x)} for x in sorted(root.rglob('*')) if x.is_file() and x.name not in ('manifest.json','SHA256SUMS.txt')]
m['sha256_inventory_excludes_self']=True
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
(root/'SHA256SUMS.txt').write_text(''.join(f'{sha(x)}  {x.relative_to(root)}\n' for x in sorted(root.rglob('*')) if x.is_file() and x.name!='SHA256SUMS.txt'))
fail=[]
for x in m['files']:
 q=root/x['path']
 if sha(q)!=x['sha256'] or q.stat().st_size!=x['bytes']:fail.append(str(q))
for line in (root/'SHA256SUMS.txt').read_text().splitlines():
 h,n=line.split('  ',1)
 if sha(root/n)!=h:fail.append(n)
print(json.dumps({'root':root.name,'files':len(m['files']),'selected':m['selected_portrait'],'selected_sha256':sha(root/m['selected_portrait']),'manifest_sha256':sha(p),'hash_failures':fail},ensure_ascii=False))
if fail:raise SystemExit(1)
