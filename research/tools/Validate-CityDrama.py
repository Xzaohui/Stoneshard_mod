"""S76 referential, speaker-role and sequence regressions; no literary/runtime certification."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
m=read(ROOT/'research/city-campaign.json');old=read(ROOT/'backups/city-drama-20261012-s76/research/city-campaign.json')
source=read(ROOT/'research/brynn-drama.json');fs=read(ROOT/'research/brynn-feedback.json');cast=m['dramatic_cast']
qs={q['id']:q for q in m['quests']};oq={q['id']:q for q in old['quests']};effects={e['id']:e for e in m['effects']}
covered=[q for q in m['quests'] if q['city']=='BRY' and 'dramatic_scenes' in q];errors=[];checks=[]
def check(ok,label):(checks if ok else errors).append(label)
expected={'CM-BRY'}|{f'CS-BRY-{i:02}' for i in range(1,11)}
check({q['id'] for q in covered}==set(source['quests'])==expected,'main-plus-ten-brynn-sides-covered')
check(m['effects']==old['effects'] and m['rules']==old['rules'] and m['travel']==old['travel'],'314-receipts-ending-ownership-and-travel-unchanged')
check(m['verified_runtime'] is False,'not-runtime-verified')
check(len(cast)==20 and len({a['id'] for a in cast.values()})==20,'20-distinct-cast-identities')
check(sum(not a['existing'] for a in cast.values())==13,'13-new-supporting-characters')
for key,a in cast.items():
 check((V/a['file']).exists(),a['id']+'-linked-card-exists')
 check(a['name'] in (V/a['file']).read_text(encoding='utf-8'),a['id']+'-card-name')
for qid,q in qs.items():
 for key in ['routes','requires','stages','locations','need','turn','title','kind']:
  check(q[key]==oq[qid][key],qid+'-structural-'+key+'-preserved')
 if qid not in expected and q['city'] not in ['ALD','MAE','SKO','YOS','DEN','MNS','EED','FOR','OSB','RAT','KOR','PAS','ASH','HIG']:check('dramatic_scenes' not in q,qid+'-not-falsely-covered')
 if q['city'] in ['SKO','YOS','DEN','MNS','EED','FOR','OSB','RAT','KOR','PAS'] and 'dramatic_scenes' in q:
  from ScopedDramaCoverage import matching_additional_source
  check(matching_additional_source(ROOT,q),qid+'-separate-exact-authored-source')
 if q['city'] in ['ASH','HIG'] and 'dramatic_scenes' in q:
  from ScopedDramaCoverage import matching_additional_source
  check(matching_additional_source(ROOT,q),qid+'-separate-exact-S86-authored-source')
 if q['city']=='MAE' and 'dramatic_scenes' in q:check(q.get('dramatic_source')=='research/maen-drama.json' and q.get('dramatic_revision')=='S79',qid+'-separate-authored-city-source')
 if q['city']=='ALD' and 'dramatic_scenes' in q:check(q.get('dramatic_source')=='research/aldwynn-drama.json' and q.get('dramatic_revision')=='S78',qid+'-separate-authored-city-source')
utterances=0;choice_answers=0;feedbacks=0;scene_ids=[]
for q in covered:
 c=next(c for c in m['cities'] if c['id']==q['city']);nodes={n['id']:n for n in c['nodes']};text=(V/q['file']).read_text(encoding='utf-8')
 check('你希望我现在具体做哪一件？' not in text,q['id']+'-old-three-question-template-not-emitted')
 check('场次与对白（S76当前稿）' in text,q['id']+'-active-dialogue-marker')
 check(set(q['dramatic_followups'])==set(q['dramatic_guards'])=={r['key'] for r in q['routes']},q['id']+'-every-existing-method-has-guard-and-followup')
 check(set(q['dramatic_exceptions'])=={'dead','refusal','before_city','after_city'},q['id']+'-case-specific-exceptions-and-order')
 for i,s in enumerate(q['dramatic_scenes']):
  sid=q['id']+f'-S{i+1}';scene_ids.append(sid);base=q['locations'][i]
  check(s['space'] in nodes and (s['space']==base or s['space'] in [base+'-A',base+'-B']),sid+'-room-belongs-to-actual-scene')
  check(bool(s['setup']) and bool(s['basis']),sid+'-staging-and-knowledge-boundary')
  check(len({who for who,_ in s['lines'] if who!='玩家'})>=2,sid+'-dialogue-has-distinct-persons')
  for who,line in s['lines']:
   utterances+=1;check(who=='玩家' or who in cast,sid+'-known-speaker')
   check(bool(line.strip()) and line in text,sid+'-authored-line-rendered')
  keys=[]
  for key,label,mode,who,answer in s['choices']:
   choice_answers+=1;keys.append(key)
   check(mode in {'ask','inspect','preview','pause'},sid+'-'+key+'-no-implicit-resolve')
   check(who in cast and bool(label) and answer in text,sid+'-'+key+'-attributed-response')
  check(len(keys)==len(set(keys)),sid+'-unique-choice-ids')
 for method,pairs in q['dramatic_followups'].items():
  for who,line in pairs:
   utterances+=1;check(who in cast and line in text,q['id']+'-'+method+'-attributed-actual-completion-response')
 for f in q['dramatic_feedback']:
  feedbacks+=1;e=effects.get(f['effect'])
  check(e is not None and e['target']==q['id'],f['effect']+'-real-targeted-existing-receipt')
  check(f['known_fact']==e['receipt'],f['effect']+'-no-expanded-knowledge-payload')
  check(f['speaker'] in cast and f['early_line'] in text and f['late_line'] in text,f['effect']+'-early-and-late-response-rendered')
  check(f['early_line']!=f['late_line'],f['effect']+'-late-response-distinct')
  check('never reselect' in f['late_scope'] and 'unfreeze N17' in f['late_scope'],f['effect']+'-late-only-future-scope')
 check('不预知秘密' in text and '不生成第二个同名角色' in text,q['id']+'-single-body-and-unknown-fact-rules')
check(len(scene_ids)==len(set(scene_ids))==35,'35-unique-active-scenes')
check(feedbacks==56,'56-authored-receipt-responses')
# Domain regressions found by reading the prior script, rather than testing counts alone.
main=qs['CM-BRY']['dramatic_scenes']
check(not any(who=='he' for who,_ in main[1]['lines']) and any(who=='he' for who,_ in main[2]['lines']),'herlin-only-found-in-old-sail-scene-not-duplicated-at-workshop')
check('不知道其疼到哪' in main[1]['basis'],'apprentice-observed-motion-does-not-know-private-pain')
for qid,person in [('CS-BRY-01','pl'),('CS-BRY-03','an'),('CS-BRY-07','ip'),('CS-BRY-08','ml'),('CS-BRY-06','vi')]:
 check(any(who==person for s in qs[qid]['dramatic_scenes'] for who,_ in s['lines']),qid+'-actual-subject-speaks-instead-of-broker')
check('控制历史保留' in qs['CS-BRY-10']['dramatic_guards']['mandates'],'patron-control-must-actually-end-and-history-persists')
check('不重复' in qs['CS-BRY-09']['dramatic_guards']['homes'],'same-watergate-safety-action-not-rewarded-twice')
check('未到' in qs['CS-BRY-05']['dramatic_exceptions']['after_city'] or '独立采购' in qs['CS-BRY-05']['dramatic_exceptions']['after_city'],'post-city-grain-still-requires-independent-supply')
check('未归' in qs['CS-BRY-08']['dramatic_exceptions']['after_city'],'living-herlin-not-proof-of-unreturned-sailor-outcome')
for name in ['brynn-generated-note-hashes.json','city-generated-note-hashes.json']:
 for rel,h in read(ROOT/'research'/name).items():check(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel+'-authoring-hash')
report=dict(date='2026-10-12',scope='S76 emitted dialogue, scene ownership, actor roles, limited receipts and preservation of existing models; not artistic quality, a runnable dialogue tree, numeric economy or game runtime',
 quests=len(covered),scenes=35,actors=len(cast),dialogue_utterances=utterances,choice_answers=choice_answers,early_late_pairs=feedbacks,
 checks_passed=len(checks),errors=errors,passed=not errors)
(ROOT/'research/brynn-drama-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False));raise SystemExit(1 if errors else 0)
