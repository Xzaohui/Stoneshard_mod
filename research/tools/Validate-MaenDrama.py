"""S79 authored scene, branch, receipt and city isolation checks; not literary certification."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
m=read('research/city-campaign.json');old=read('backups/city-drama-20261012-s79/city-campaign.json');src=read('research/maen-drama.json');fs=read(src['feedback_source'])
qs={q['id']:q for q in m['quests']};oq={q['id']:q for q in old['quests']};cast=m['dramatic_casts']['MAE'];effects={e['id']:e for e in m['effects']};errors=[];checks=[]
def check(ok,label):(checks if ok else errors).append(label)
expected={'CM-MAE'}|{f'CS-MAE-{i:02}' for i in range(1,7)}
check(set(src['quests'])==expected,'one-main-six-sides')
check(len(cast)==15 and sum(not a['existing'] for a in cast.values())==8,'15-actors-eight-added-cards')
check(len({a['id'] for a in cast.values()})==len(cast),'unique-actor-identities')
check(not ({a['id'] for a in cast.values()} & {a['id'] for a in m['dramatic_cast'].values()}),'brynn-and-maen-actors-not-mixed')
check(m['dramatic_cast']==old['dramatic_cast'],'brynn-cast-intact')
for key in ['effects','rules','travel','verified_runtime']:check(m[key]==old[key],'unchanged-'+key)
for qid,q in qs.items():
 for key in ['id','city','routes','requires','stages','locations','need','turn','title','kind']:check(q[key]==oq[qid][key],qid+'-preserve-'+key)
 if q['city'] in ['SKO','YOS','DEN','MNS','EED','FOR','OSB','RAT','KOR','PAS'] and 'dramatic_scenes' in q:
  from ScopedDramaCoverage import matching_additional_source
  check(matching_additional_source(ROOT,q),qid+'-separate-exact-authored-source')
 elif q['city'] in ['ASH','HIG'] and q.get('dramatic_revision')=='S86':
  from ScopedDramaCoverage import matching_additional_source
  check(matching_additional_source(ROOT,q),qid+'-separate-exact-S86-authored-source')
 elif qid not in expected:
  for key in set(q)|set(oq[qid]):
   if key.startswith('dramatic_'):check(q.get(key)==oq[qid].get(key),qid+'-no-other-city-rewrite-'+key)
for key,a in cast.items():
 p=V/a['file'];check(p.exists(),a['id']+'-card-exists')
 if p.exists():check(a['name'] in p.read_text(encoding='utf-8'),a['id']+'-name-in-card')
nodes={n['id']:n for c in m['cities'] if c['id']=='MAE' for n in c['nodes']};scene_count=utterances=choice_count=method_count=0;all_feedback=[]
for qid in sorted(expected):
 q=qs[qid];text=(V/q['file']).read_text(encoding='utf-8');spec=src['quests'][qid]
 check(q.get('dramatic_source')=='research/maen-drama.json' and q.get('dramatic_revision')=='S79',qid+'-current-source')
 check('场次与对白（S79当前稿）' in text and '有限回执的具体回应（S79）' in text,qid+'-current-emission-markers')
 check('你希望我现在具体做哪一件？' not in text,qid+'-old-template-absent')
 for sk,mk in [('scenes','dramatic_scenes'),('followups','dramatic_followups'),('route_guards','dramatic_guards'),('exceptions','dramatic_exceptions')]:check(spec[sk]==q[mk],qid+'-authored-'+sk)
 check(len(q['dramatic_scenes'])==len(q['locations'])==(5 if qid=='CM-MAE' else 3),qid+'-actual-main-or-side-locations')
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
check(set(all_feedback)==incoming=={row[0] for row in fs} and len(all_feedback)==len(set(all_feedback))==33,'all-33-existing-incoming-receipts-exactly-once')
check(scene_count==23 and method_count==15 and choice_count==46,'23-scenes-15-methods-46-options')
check(cast['ka'].get('legacy_shared') is True and 'N10' in cast['ka']['role'],'same-kaem-as-legacy-not-second-character')
check('不回授' in qs['CM-MAE']['dramatic_stage_note'] and '不回授' in qs['CS-MAE-05']['dramatic_guards']['a'],'no-restored-legacy-certification')
check('同粮两案重复' in qs['CS-MAE-01']['dramatic_guards']['b'],'ordinary-rations-not-promised-twice')
check('两点未验收不发SQ06' in qs['CS-MAE-02']['dramatic_guards']['b'],'no-custody-grant-from-preview')
check('撤投效绑份实际生效' in qs['CS-MAE-03']['dramatic_guards']['a'],'stay-without-vote-needs-actual-condition-removal')
check('撤永久身契' in qs['CS-MAE-04']['dramatic_guards']['a'],'one-batch-is-not-permanent-personal-control')
check('凯姆同段独创摘要实际停售' in qs['CS-MAE-05']['dramatic_guards']['b'],'private-source-needs-actual-wrong-sale-stop')
check('实际到达被接住才结' in qs['CS-MAE-06']['dramatic_guards']['b'],'evacuation-needs-real-reception')
check('不让留城写未获救' in qs['CS-MAE-06']['dramatic_guards']['a'] or '不把留城写未获救' in qs['CS-MAE-06']['dramatic_guards']['a'],'stay-does-not-mean-failed-rescue')
check('不挪同一份粮两边承诺' in qs['CM-MAE']['dramatic_guards']['control'] and '未同意者不入名册' in qs['CM-MAE']['dramatic_guards']['control'],'control-is-finite-opt-in-with-separate-basic-outlet')
for file in ['maen-generated-note-hashes.json','city-generated-note-hashes.json']:
 for rel,h in read('research/'+file).items():check(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel+'-authoring-hash')
report=dict(date='2026-10-12',scope='S79 source/rendering integrity, actor and room scope, existing receipt coverage and branch regressions; not literary, numeric economy or runtime validation',quests=7,scenes=scene_count,actors=len(cast),dialogue_utterances=utterances,choice_answers=choice_count,early_late_pairs=len(all_feedback),checks_passed=len(checks),errors=errors,passed=not errors)
(ROOT/'research/maen-drama-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
