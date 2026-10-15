from pathlib import Path
import json,hashlib,shutil,datetime
R=Path(__file__).resolve().parents[5]
C=R/'Assets/CharacterDesigns/20261015/portrait_redraw_campaign'
roster=json.load(open(C/'campaign_roster.json'))
style=[(x,Path(y)) for x,y in [('mara','Assets/CharacterDesigns/20261015/native_style_pilot/mara/assets/portrait_v2_74x100.png'),('iwo','Assets/CharacterDesigns/20261015/native_style_pilot/iwo/candidates/portrait_v1_74x100_candidate.png'),('leiya','Assets/CharacterDesigns/20261015/native_style_continuation/leiya/candidates/portrait_v2_maxcoverage_74x100_candidate.png'),('tore','Assets/CharacterDesigns/20261015/native_style_continuation/tore/candidates/portrait_v1_74x100_candidate.png')]]
for slug in ['biluo','evan']:
 W=C/slug
 for folder in ['sources','prompts','tool_returns','raw','candidates','previews','qa']:(W/folder).mkdir(exist_ok=True)
 entry=next(x for x in roster['characters'] if x['suggested_slug']==slug)
 (W/'sources/roster_entry.json').write_text(json.dumps(entry,ensure_ascii=False,indent=2)+'\n')
 sourcepairs=[(entry['current_cards'][0]['path'],'character_card.md','current identity card',entry['current_cards'][0]['sha256']), (entry['identity_master']['path'],'identity_reference.png','identity master; actually viewed',entry['identity_master']['sha256']), (entry['master_selection_evidence']['path'],'master_QA.json','identity master QA; actually read',entry['master_selection_evidence']['sha256']),(entry['master_manifests'][0]['path'],'master_manifest.json','historical manifest',entry['master_manifests'][0]['sha256']),('AGENTS.md','AGENTS.md','project instructions',None)]
 sourcepairs += [(str(p),n+'_style_reference.png','approved style reference only; actually viewed',None) for n,p in style]
 stories=['design/06_支线/城市支线/台本_CS-KOR-03_寄存的陌生画.md' if slug=='biluo' else 'design/05_主线/城市篇章/台本_CM-KOR_不是你的姓.md','design/11_管理/考德与柏石关人物演出审查.md','design/04_人物/人物细描与随身物.md']
 sourcepairs +=[(p,f'story_{i+1}.md','current story; relevant passages inspected',None) for i,p in enumerate(stories)]
 if slug=='evan':sourcepairs.append(('Assets/CharacterDesigns/20261013/expressive/evan/spec_lock.json','historical_spec_lock.json','documents older card without S89 appearance additions',None))
 items=[]
 for op,snap,role,expected in sourcepairs:
  src=R/op;dst=W/'sources'/snap;shutil.copyfile(src,dst);h=hashlib.sha256(dst.read_bytes()).hexdigest();d={'original_path':op,'snapshot_path':'sources/'+snap,'sha256':h,'role':role}
  if expected:d['roster_sha256_matches']=h==expected
  items.append(d)
 note='Current source card hash matches campaign snapshot. Historical card did not include S89 fine details. Current card age/hat/early gray temples take precedence over older bare-headed master; preserve remaining master identity and garment palette. Parent confirmed this is an appearance update, not identity conflict.' if slug=='evan' else 'Current source card hash matches campaign snapshot. Thirty-something woman, master burgundy garment/gray shawl and swept-back tied brown wavy hair; no identity conflict. Bracelet is outside head-only portrait framing.'
 (W/'sources/source_manifest.json').write_text(json.dumps({'actor_id':entry['canonical_id'],'character':entry['name'],'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'identity_conflict':False,'reconciliation':note,'items':items},ensure_ascii=False,indent=2)+'\n')
 for script in ['derive_portrait.py','finalize_manifest.py']:shutil.copyfile(C/'niv'/script,W/script)
 print(slug,len(items),note)
