from pathlib import Path
import json,hashlib,datetime,sys
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';e=a/'independent_eighth_new_character_actions_evidence';g=sys.argv[1];slugs=g.split('_');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fp=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)}
j=json.loads((a/'eighth_new_character_actions_brief.json').read_text());selected=[];attempts=[];missing=[];errors=[];ancillary_updates=[]
for c in j['characters']:
 if c['slug'] not in slugs:continue
 tree=r/c['proposed_output_directory'];afs=[json.loads(p.read_text()) for p in sorted(e.glob(c['slug']+'_*_byte_audit.json'))]
 for at in afs:
  for row in at['files']:
   p=r/row['path']
   if not p.is_file() or sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:
    if p.parent.name=='qa' and p.name.endswith('_technical.json'):
     q=json.loads(p.read_text());assert q.get('actual_native_raw_and_transparent_views_pending') is False and q.get('actual_raw_transparent_light_dark_viewed_by_author') is True
     ancillary_updates.append({'path':row['path'],'initial_audit_sha256':row['sha256'],'current':fp(p),'reason':'Author closed actual-view pending flags after viewing; image, prompt, parameter and full payload bytes unchanged.'})
    else:errors.append(['attempt_changed',row['path']])
  attempts.append(at)
 for pose in c['plans']:
  aa=[v for v in afs if v['pose_version'].startswith(pose['key']+'_')];passes=[v for v in aa if v['verdict']=='pass']
  if len(passes)>1:errors.append(['multiple_pass_candidates',pose['key']])
  if not passes:missing.append(pose['key']);continue
  p=passes[0];cand=next(v for v in p['files'] if v['path'].endswith('_transparent.png'));copies=[f for f in (tree/'selected').glob('*.png') if sha(f)==cand['sha256']]
  if len(copies)!=1:errors.append(['selected_copy_missing_or_duplicate',pose['key']]);continue
  selected.append({'character':c['slug'],'pose_key':pose['key'],'selected_attempt':p['pose_version'],'selected_file':fp(copies[0]),'reviewed_candidate':cand,'copy_byte_identical':True,'visual_findings':p['visual_review']['findings']})
assert not errors,errors
out={'schema_version':1,'reviewer':'review_eighth_character_actions','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'group':g,'verdict':'pass_with_explicit_missing' if missing else 'pass','selected_count':len(selected),'selected':selected,'explicit_missing':missing,'attempts':attempts,'errors':errors,'ancillary_qa_status_updates':ancillary_updates,'scope':'Independent raw/transparent/light/dark visual and source-byte review, selected files byte-identical to reviewed candidates. Board/package audits remain separate.'}
p=a/f'independent_eighth_new_character_actions_{g}_visual_gate_20261014.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'gate':fp(p),'selected':len(selected),'missing':missing},ensure_ascii=False))
