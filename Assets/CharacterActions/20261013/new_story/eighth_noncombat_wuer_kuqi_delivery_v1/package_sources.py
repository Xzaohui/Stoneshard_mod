from pathlib import Path
import json,hashlib,zipfile,zlib,sys,datetime
root=Path(__file__).resolve().parents[5];group=Path(__file__).resolve().parent;stage=sys.argv[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
chars=[root/'Assets/CharacterActions/20261013/new_story'/s/'noncombat_basics_v1' for s in ['wuer','kuqi']]
for d in chars:
 files=[{'path':str(p.relative_to(d)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(d.rglob('*')) if p.is_file() and p not in [d/'manifest.json',d/'FINAL_STATUS.json']]
 content=json.dumps({'schema_version':1,'character':d.parent.name,'files':files,'excludes':['manifest.json (self)','FINAL_STATUS.json (freeze receipt references this manifest)'],'all_generated_attempts_retained':True},ensure_ascii=False,indent=2)+'\n'
 if (d/'FINAL_STATUS.json').exists() and json.loads((d/'FINAL_STATUS.json').read_text()).get('status')=='final_clean_and_presentation_pass':assert (d/'manifest.json').read_text()==content, 'Frozen manifest would change'
 else:(d/'manifest.json').write_text(content)
paths=[]
for d in chars:paths += [p for p in sorted(d.rglob('*')) if p.is_file()]
paths += [p for p in sorted(group.rglob('*')) if p.is_file() and 'package_candidates' not in p.parts and p.suffix!='.zip' and p.name not in ['package_manifest.json','candidate_package_manifest.json','freeze_receipt.json','package_QA_independent.json']]
seen=set();paths=[p for p in paths if not (str(p) in seen or seen.add(str(p)))];entries=[]
for p in paths:
 b=p.read_bytes(); entries.append({'path':str(p.relative_to(root)),'bytes':len(b),'sha256':sha(b),'compressed_estimate':len(zlib.compress(b,9))+len(str(p))*2+400,'data':b})
# Greedy deterministic packing into <18 MiB independent ordinary ZIPs.
bins=[];cur=[];sz=0
for e in entries:
 if cur and sz+e['compressed_estimate']>17*1024*1024:bins.append(cur);cur=[];sz=0
 cur.append(e);sz+=e['compressed_estimate']
if cur:bins.append(cur)
outdir=group/'package_candidates' if stage=='candidate' else group;outdir.mkdir(exist_ok=True)
packages=[]
for i,part in enumerate(bins,1):
 p=outdir/f'wuer_kuqi_complete_sources_part{i:02d}_of_{len(bins):02d}.zip'
 with zipfile.ZipFile(p,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for e in part:z.writestr(e['path'],e['data'])
  z.writestr('PACKAGE_CONTENTS.json',json.dumps({'part':i,'total_parts':len(bins),'stage':stage,'members':[{k:v for k,v in e.items() if k not in ['data','compressed_estimate']} for e in part]},ensure_ascii=False,indent=2)+'\n')
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  for e in part:assert sha(z.read(e['path']))==e['sha256']
 assert p.stat().st_size<18*1024*1024
 packages.append({'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'mib':p.stat().st_size/(1024*1024),'sha256':sha(p.read_bytes()),'member_count':len(part)+1,'crc_and_member_sha_verified':True,'members':[{k:v for k,v in e.items() if k not in ['data','compressed_estimate']} for e in part]})
manifest={'schema_version':1,'stage':stage,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selected_count':4,'initial_calls':4,'revision_calls':0,'full_tool_returns_with_image_payload':4,'all_attempts_kept':True,'all_files_count':len(entries),'packages':packages,'exclusion_scope':'ZIP archives, previous candidate packages and external package audit/freeze receipts are not recursively packed. All art, prompts, parameters, returned image payloads, raw, alpha-cleaned sources, visual reviews, copied planning sources, QA, source provenance, and current character statuses/manifests are included.'}
(group/('candidate_package_manifest.json' if stage=='candidate' else 'package_manifest.json')).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in manifest.items() if k!='packages'},ensure_ascii=False));print(json.dumps([{k:v for k,v in x.items() if k!='members'} for x in packages],ensure_ascii=False,indent=2))
