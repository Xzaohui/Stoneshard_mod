import json,hashlib,zipfile,re
from pathlib import Path
from datetime import datetime,timezone
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); O=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/third_new_character_actions_sources'
sha=lambda b:hashlib.sha256(b).hexdigest()
C=re.compile(r'(?i)(?<![a-z])(kuen|sune|tian|lein)(?![a-z])|枯恩|苏奈|缇安|蕾因')
K=re.compile(r'(?i)shawl|披肩|粉笔|chalk|绑腿|calf.wrap|key.cord|钥绳|charcoal.pencil|炭笔|record.board|记录板|empty.bowl|空碗|seat.edge|椅沿|torso.turn|转身')
files=[]; meta=[]; zips=[]; hits=[]; sem=[]
for p in sorted((R/'Assets/CharacterActions').rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes(); rel=str(p.relative_to(R)); rec={'path':rel,'bytes':len(b),'sha256':sha(b)};files.append(rec)
 source=any(x in p.parts for x in ['sources','source','source_tree','files'])
 if p.suffix.lower() in ['.json','.md','.txt']:
  text=b.decode('utf-8',errors='replace');m={**rec,'copied_source_context':source};meta.append(m)
  if C.search(rel+'\n'+text):hits.append({**m,'matching_tokens':sorted(set(m.group(0) for m in C.finditer(rel+'\n'+text)))})
  if K.search(text) and not source:
   contexts=[]
   for ma in K.finditer(text):
    c=text[max(0,ma.start()-140):min(len(text),ma.end()+240)]
    if c not in contexts: contexts.append(c)
   sem.append({**m,'contexts':contexts[:30]})
 if p.suffix.lower()=='.zip':
  zr={**rec,'members':[],'text_members_read':0,'candidate_matches':[],'semantic_matches':[],'errors':[]}
  try:
   with zipfile.ZipFile(p) as z:
    for inf in z.infolist():
     if inf.is_dir():continue
     mr={'path':inf.filename,'bytes':inf.file_size,'crc32':format(inf.CRC,'08x')};zr['members'].append(mr)
     tx=''
     if Path(inf.filename).suffix.lower() in ['.json','.md','.txt']:
      tx=z.read(inf).decode('utf-8',errors='replace');zr['text_members_read']+=1
     if C.search(inf.filename+'\n'+tx):zr['candidate_matches'].append({'path':inf.filename,'tokens':sorted(set(x.group(0) for x in C.finditer(inf.filename+'\n'+tx)))})
     if tx and K.search(tx):zr['semantic_matches'].append({'path':inf.filename,'tokens':sorted(set(x.group(0) for x in K.finditer(tx)))})
  except Exception as e:zr['errors'].append(str(e))
  zips.append(zr)
d={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Local Assets/CharacterActions full recursive file inventory; all .json/.md/.txt decoded; ZIP member paths and all text metadata contents read. Source copies and planning references do not count as completed actions. No external or remote absence claim.','candidate_pattern':C.pattern,'semantic_pattern':K.pattern,'file_count':len(files),'metadata_count':len(meta),'zip_count':len(zips),'files':files,'metadata':meta,'candidate_matches':hits,'primary_semantic_contexts':sem,'zips':zips,'candidate_own_action_directories':{s:[str(x.relative_to(R)) for x in (R/'Assets/CharacterActions').rglob(s) if x.is_dir()] for s in ['kuen','sune','tian','lein']}}
(O/'action_tree_scan.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print({k:d[k] for k in ['file_count','metadata_count','zip_count','candidate_own_action_directories']})
print('candidate hits',len(hits),'non-source',len([x for x in hits if not x['copied_source_context']]))
print('zip candidate matches',sum(len(z['candidate_matches']) for z in zips),'errors',[z['errors'] for z in zips if z['errors']]);print('semantic primary files',len(sem))
for x in hits:
 if not x['copied_source_context']:print('CANDIDATE',x['path'],x['matching_tokens'])
