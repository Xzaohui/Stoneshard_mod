"""Add scoped city casts; preserve the existing Brynn source and receipt ownership."""
from pathlib import Path
import json

def apply_additional_city_drama(root,model,existing):
 model['dramatic_casts']={'BRY':model['dramatic_cast']}
 for city,slug,revision in [('ALD','aldwynn','S78'),('MAE','maen','S79'),('SKO','skonfert','S80'),('YOS','yostwayne','S80'),('DEN','denbrie','S81'),('MNS','mannshire','S81'),('EED','eeders','S82'),('FOR','forholt','S82'),('OSB','osbrook','S83'),('RAT','ratten','S83'),('KOR','korde','S84'),('PAS','passgate','S84'),('ASH','ashcare','S86'),('HIG','highland','S86')]:
  apply_city(root,model,existing,city,slug,revision)
 model['dramatic_scope']='Active authored cities: '+', '.join(model['dramatic_casts'])+'; stages retain geographical sketch only for covered quests.'

def apply_city(root,model,existing,city,slug,revision):
 path=root/f'research/{slug}-drama.json'
 if not path.exists():return
 data=json.loads(path.read_text(encoding='utf-8'));qs={q['id']:q for q in model['quests']};effects={e['id']:e for e in model['effects']}
 cast={}
 for key,a in data['cast'].items():
  a=dict(a);a['file']=existing[a['id']] if a['existing'] else f"04_人物/城市人物/人物_{a['id']}_{a['name']}.md";cast[key]=a
 model['dramatic_casts'][city]=cast
 for a in cast.values():existing[a['id']]=a['file']
 for qid,spec in data['quests'].items():
  q=qs[qid];assert q['city']==city and len(spec['scenes'])==len(q['locations'])
  assert set(spec['followups'])==set(spec['route_guards'])=={r['key'] for r in q['routes']}
  q['dramatic_revision']=revision;q['dramatic_source']=f'research/{slug}-drama.json'
  for name in ['scenes','followups','exceptions']:q['dramatic_'+name]=spec[name]
  q['dramatic_guards']=spec['route_guards'];q['dramatic_stage_note']=spec.get('stage_note','');q['dramatic_feedback']=[]
 feedback=json.loads((root/f'research/{slug}-feedback.json').read_text(encoding='utf-8'))
 for eid,speaker,early,late,action in feedback:
  e=effects[eid];assert e['target'] in data['quests'] and speaker in cast
  qs[e['target']]['dramatic_feedback'].append(dict(effect=eid,speaker=speaker,known_fact=e['receipt'],early_line=early,late_line=late,early_action=action,
   late_scope='Only future dialogue/arrangements; never reselect resolved method, reverse damage, duplicate stock or payment, or unfreeze N17.'))
