"""S78 authored scene, branch, receipt and city isolation checks; not literary certification."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
m=read('research/city-campaign.json');old=read('backups/city-drama-20261012-s78/city-campaign.json');src=read('research/aldwynn-drama.json');fs=read(src['feedback_source'])
qs={q['id']:q for q in m['quests']};oq={q['id']:q for q in old['quests']};cast=m['dramatic_casts']['ALD'];effects={e['id']:e for e in m['effects']};errors=[];checks=[]
def check(ok,label):(checks if ok else errors).append(label)
expected={'CM-ALD'}|{f'CS-ALD-{i:02}' for i in range(1,7)}
check(set(src['quests'])==expected,'one-main-six-sides')
check(len(cast)==15 and sum(not a['existing'] for a in cast.values())==9,'15-actors-nine-new')
check(len({a['id'] for a in cast.values()})==len(cast),'unique-actor-identities')
check(not ({a['id'] for a in cast.values()} & {a['id'] for a in m['dramatic_cast'].values()}),'brynn-and-aldwynn-actors-not-mixed')
check(m['dramatic_cast']==old['dramatic_cast'],'brynn-cast-intact')
for key in ['effects','rules','travel','verified_runtime']:check(m[key]==old[key],'unchanged-'+key)
for qid,q in qs.items():
 for key in ['id','city','routes','requires','stages','locations','need','turn','title','kind']:check(q[key]==oq[qid][key],qid+'-preserve-'+key)
 if q['city'] in ['SKO','YOS','DEN','MNS','EED','FOR','OSB','RAT','KOR','PAS'] and 'dramatic_scenes' in q:
  from ScopedDramaCoverage import matching_additional_source
  check(matching_additional_source(ROOT,q),qid+'-separate-exact-authored-source')
 elif q['city']=='MAE' and 'dramatic_scenes' in q:
  check(q.get('dramatic_source')=='research/maen-drama.json' and q.get('dramatic_revision')=='S79',qid+'-separate-matching-new-authored-source')
 elif qid not in expected:
  for key in set(q)|set(oq[qid]):
   if key.startswith('dramatic_'):check(q.get(key)==oq[qid].get(key),qid+'-no-other-city-rewrite-'+key)
for key,a in cast.items():
 p=V/a['file'];check(p.exists(),a['id']+'-card-exists')
 if p.exists():check(a['name'] in p.read_text(encoding='utf-8'),a['id']+'-name-in-card')
nodes={n['id']:n for c in m['cities'] if c['id']=='ALD' for n in c['nodes']};scene_count=utterances=choice_count=method_count=0;all_feedback=[]
for qid in sorted(expected):
 q=qs[qid];text=(V/q['file']).read_text(encoding='utf-8');spec=src['quests'][qid]
 check(q.get('dramatic_source')=='research/aldwynn-drama.json' and q.get('dramatic_revision')=='S78',qid+'-current-source')
 check('场次与对白（S78当前稿）' in text and '有限回执的具体回应（S78）' in text,qid+'-current-emission-markers')
 check('你希望我现在具体做哪一件？' not in text,qid+'-old-template-absent')
 for sk,mk in [('scenes','dramatic_scenes'),('followups','dramatic_followups'),('route_guards','dramatic_guards'),('exceptions','dramatic_exceptions')]:check(spec[sk]==q[mk],qid+'-authored-'+sk)
 check(len(q['dramatic_scenes'])==len(q['locations'])==3,qid+'-three-actual-locations')
 check(set(q['dramatic_exceptions'])=={'dead','refusal','before_city','after_city'},qid+'-case-specific-fallback-and-order')
 for i,s in enumerate(q['dramatic_scenes']):
  scene_count+=1;base=q['locations'][i];sid=qid+f'-S{i+1}'
  check(s['space'] in nodes and s['space'] in [base,base+'-A',base+'-B'],sid+'-actual-location')
  check(bool(s['setup']) and bool(s['basis']),sid+'-staging-and-knowledge')
  check(len({who for who,_ in s['lines'] if who!='玩家'})>=2,sid+'-distinct-people')
  for who,line in s['lines']:
   utterances+=1;check(who=='玩家' or who in cast,sid+'-scoped-speaker');check(line in text and bool(line.strip()),sid+'-line-rendered')
  keys=[]
  for key,label,mode,who,answer in s['choices']:
   choice_count+=1;keys.append(key);check(who in cast and mode in ['ask','inspect','preview','pause'],sid+'-choice-read-only-mode')
   check(label in text and answer in text,sid+'-choice-specific-response')
  check(len(keys)==len(set(keys))>=2,sid+'-unique-scene-options')
 check(set(q['dramatic_guards'])==set(q['dramatic_followups'])=={r['key'] for r in q['routes']},qid+'-all-existing-methods')
 for r in q['routes']:
  method_count+=1;check(q['dramatic_guards'][r['key']] in text,qid+'-actual-action-gate')
  pairs=q['dramatic_followups'][r['key']];check(len(pairs)>=2,qid+'-different-completion-voices')
  for who,line in pairs:utterances+=1;check(who in cast and line in text,qid+'-followup-voice')
 for f in q['dramatic_feedback']:
  all_feedback.append(f['effect']);e=effects[f['effect']]
  check(e['target']==qid and f['known_fact']==e['receipt'],f['effect']+'-same-limited-known-fact')
  check(f['speaker'] in cast and f['early_line']!=f['late_line'],f['effect']+'-distinct-timing-voice')
  check(all(f[k] in text for k in ['early_line','late_line','early_action']),f['effect']+'-timing-emitted')
  check('never reselect' in f['late_scope'] and 'unfreeze N17' in f['late_scope'],f['effect']+'-history-boundary')
 check('二次确认' in text and '不写resolve或paid' in text and '死亡、拒绝、保密、缺席优先' in text,qid+'-common-no-automatic-commit')
incoming={e['id'] for e in m['effects'] if e['target'] in expected}
check(set(all_feedback)==incoming=={row[0] for row in fs} and len(all_feedback)==len(set(all_feedback))==32,'all-32-existing-incoming-receipts-exactly-once')
check(scene_count==21 and method_count==15 and choice_count==42,'21-scenes-15-methods-42-options')
check('撤赠不能伪写纯赠已完成' in qs['CS-ALD-03']['dramatic_guards']['a'],'withdrawn-gift-not-claimed-delivered')
check('同项扣去主章已付' in qs['CS-ALD-05']['dramatic_guards']['a'],'same-injury-not-paid-twice')
check('不生成她' in qs['CS-ALD-05']['dramatic_scenes'][1]['setup'],'injured-person-not-cloned-into-village')
check('完整临终' in qs['CS-ALD-02']['dramatic_scenes'][0]['basis'] and '未知' in qs['CS-ALD-02']['dramatic_guards']['a'],'no-invented-dead-person-consent')
check('不公开' in qs['CM-ALD']['dramatic_guards']['open'] and '不索地址' in next(f['early_action'] for f in qs['CM-ALD']['dramatic_feedback'] if f['effect']=='LX-CS-ALD-01-a'),'public-technology-not-private-address')
check('原限制' in qs['CS-ALD-06']['dramatic_guards']['a'] and '货物' in qs['CS-ALD-06']['dramatic_guards']['b'],'drawing-permission-not-import-permission')
for file in ['aldwynn-generated-note-hashes.json','city-generated-note-hashes.json']:
 for rel,h in read('research/'+file).items():check(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel+'-authoring-hash')
report=dict(date='2026-10-12',scope='S78 source/rendering integrity, actor and room scope, existing receipt coverage and branch regressions; not literary, numeric economy or runtime validation',quests=7,scenes=scene_count,actors=len(cast),dialogue_utterances=utterances,choice_answers=choice_count,early_late_pairs=len(all_feedback),checks_passed=len(checks),errors=errors,passed=not errors)
(ROOT/'research/aldwynn-drama-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
