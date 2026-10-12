"""S81 source/rendering, safe receiving and distinct craft identities verification."""
from pathlib import Path
import json,hashlib
from ScopedDramaCoverage import matching_additional_source
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read('research/city-campaign.json');old=read('backups/city-drama-20261012-s81/city-campaign.json');qs={q['id']:q for q in m['quests']};oq={q['id']:q for q in old['quests']};effects={e['id']:e for e in m['effects']};checks=[];errors=[]
def check(ok,label):(checks if ok else errors).append(label)
expected={cid:{'CM-'+cid}|{f'CS-{cid}-{i:02}' for i in range(1,4)} for cid in ['DEN','MNS']};covered=set.union(*expected.values())
check(m['verified_runtime'] is False,'not-runtime-verified')
for key in ['effects','rules','travel','verified_runtime']:check(m[key]==old[key],'preserve-all-'+key)
for qid,q in qs.items():
 for key in ['id','city','routes','requires','stages','locations','need','turn','title','kind']:check(q[key]==oq[qid][key],qid+'-structural-'+key)
 if q['city'] in ['EED','FOR','OSB','RAT','KOR','PAS'] and 'dramatic_scenes' in q:
  check(matching_additional_source(ROOT,q),qid+'-exact-later-scoped-source');continue
 if qid not in covered:
  for key in set(q)|set(oq[qid]):
   if key.startswith('dramatic_'):check(q.get(key)==oq[qid].get(key),qid+'-other-city-unchanged-'+key)
for cid,cast in old['dramatic_casts'].items():check(m['dramatic_casts'][cid]==cast,cid+'-previous-cast-intact')
casts={cid:m['dramatic_casts'][cid] for cid in expected};unique={a['id'] for c in casts.values() for a in c.values()};newactors={a['id']:a for c in casts.values() for a in c.values() if not a['existing']}
check([len(casts[c]) for c in ['DEN','MNS']]==[10,8] and len(unique)==18 and len(newactors)==10,'18-distinct-actors-ten-new-cards')
check(not ({a['id'] for a in casts['DEN'].values()} & {a['id'] for a in casts['MNS'].values()}),'no-wine-or-shore-identity-clone')
check(not (unique & {a['id'] for cid,c in old['dramatic_casts'].items() for a in c.values()}),'previous-cities-actors-not-repurposed')
for cid,cast in casts.items():
 check(len({a['id'] for a in cast.values()})==len(cast),cid+'-unique-local-identities')
 for a in cast.values():
  p=V/a['file'];check(p.exists() and a['name'] in p.read_text(encoding='utf-8'),a['id']+'-linked-card-name')
scene_count=utterances=choice_count=method_count=0;all_feedback=[]
for cid,slug in [('DEN','denbrie'),('MNS','mannshire')]:
 src=read(f'research/{slug}-drama.json');fs=read(src['feedback_source']);cast=casts[cid];nodes={n['id']:n for c in m['cities'] if c['id']==cid for n in c['nodes']};source_feedback={f[0]:f for f in fs}
 check(set(src['quests'])==expected[cid],cid+'-one-main-three-sides')
 check(len(fs)==len(source_feedback)==15,cid+'-authored-feedback-unique')
 for qid in sorted(expected[cid]):
  q=qs[qid];text=(V/q['file']).read_text(encoding='utf-8');spec=src['quests'][qid]
  check(matching_additional_source(ROOT,q),qid+'-exact-current-authored-source')
  check('场次与对白（S81当前稿）' in text and '有限回执的具体回应（S81）' in text,qid+'-current-render-markers')
  check('你希望我现在具体做哪一件？' not in text and '合影' not in text,qid+'-old-template-and-anachronism-absent')
  check(len(q['dramatic_scenes'])==len(q['locations'])==3,qid+'-three-planned-scenes')
  check(set(q['dramatic_exceptions'])=={'dead','refusal','before_city','after_city'} and all(q['dramatic_exceptions'].values()),qid+'-case-specific-fallbacks')
  for field in q['dramatic_exceptions'].values():check(field in text,qid+'-fallback-rendered')
  check(q['dramatic_stage_note']==spec.get('stage_note',''),qid+'-stage-note-preserved')
  for i,s in enumerate(q['dramatic_scenes']):
   scene_count+=1;base=q['locations'][i];sid=qid+f'-S{i+1}'
   check(s['space'] in nodes and s['space'] in [base,base+'-A',base+'-B'],sid+'-actual-location')
   check(bool(s['setup']) and bool(s['basis']) and s['setup'] in text and s['basis'] in text,sid+'-staging-and-knowledge-rendered')
   check(len({who for who,_ in s['lines'] if who!='玩家'})>=2,sid+'-distinct-people')
   for who,line in s['lines']:
    utterances+=1;check(who=='玩家' or who in cast,sid+'-scoped-speaker');check(bool(line.strip()) and line in text,sid+'-rendered-line')
   keys=[]
   for key,label,mode,who,answer in s['choices']:
    choice_count+=1;keys.append(key);check(who in cast and mode in ['ask','inspect','preview','pause'],sid+'-read-only-option');check(label in text and answer in text,sid+'-specific-choice-response')
   check(len(keys)==len(set(keys))==2,sid+'-two-unique-options')
  check(set(q['dramatic_guards'])==set(q['dramatic_followups'])=={r['key'] for r in q['routes']},qid+'-all-old-methods')
  for r in q['routes']:
   method_count+=1;check(q['dramatic_guards'][r['key']] in text,qid+'-actual-action-gate')
   pairs=q['dramatic_followups'][r['key']];check(len({who for who,_ in pairs})>=2,qid+'-distinct-completion-voices')
   for who,line in pairs:utterances+=1;check(who in cast and line in text,qid+'-completion-speaker')
  for f in q['dramatic_feedback']:
   all_feedback.append(f['effect']);e=effects[f['effect']];row=source_feedback.get(f['effect'])
   check(e['target']==qid and f['known_fact']==e['receipt'],f['effect']+'-same-limited-receipt')
   check(row==[f['effect'],f['speaker'],f['early_line'],f['late_line'],f['early_action']],f['effect']+'-exact-authored-feedback-row')
   check(f['speaker'] in cast and f['early_line']!=f['late_line'],f['effect']+'-different-timing-voices')
   check(all(f[k] in text for k in ['early_line','late_line','early_action']),f['effect']+'-rendered-timing-actions')
   check('never reselect' in f['late_scope'] and 'unfreeze N17' in f['late_scope'],f['effect']+'-no-history-rollback')
  check('二次确认' in text and '不写resolve或paid' in text and '死亡、拒绝、保密、缺席优先' in text,qid+'-no-automatic-commit')
 incoming={e['id'] for e in m['effects'] if e['target'] in expected[cid]};check(set(source_feedback)==incoming,cid+'-every-old-incoming-edge-authored')
check(len(all_feedback)==len(set(all_feedback))==30 and set(all_feedback)=={e['id'] for e in m['effects'] if e['target'] in covered},'all-30-receipts-exactly-once')
check(scene_count==24 and method_count==16 and choice_count==48,'24-scenes-16-methods-48-answers')
check('各夜每户均有实有安全住处' in qs['CM-DEN']['dramatic_guards']['shared'] and '不写新增可住' in qs['CM-DEN']['dramatic_guards']['shared'],'no-night-outside-or-unbuilt-third-bed')
check('实际有未占位与接收' in qs['CM-DEN']['dramatic_guards']['leases'] and '撤回岗绑住' in qs['CM-DEN']['dramatic_guards']['leases'],'real-receiving-and-no-work-for-door-condition')
check('卡蕾、欧铎、艾蕾三成年人逐人' in qs['CS-DEN-01']['dramatic_guards']['b'],'all-three-adult-passengers-consent')
check('坦瑟仍在原岸' in qs['CS-DEN-01']['dramatic_scenes'][1]['setup'] and all(who!='ta' for who,_ in qs['CS-DEN-01']['dramatic_scenes'][1]['lines']),'injured-worker-not-teleported-to-receiving-scene')
check('不重演孩子遇险' in qs['CS-DEN-02']['dramatic_guards']['a'] and '不罚全部迁户' in qs['CS-DEN-02']['dramatic_guards']['b'],'net-rescue-no-reenactment-or-collective-punishment')
check('已签有限住期保持' in qs['CS-DEN-03']['dramatic_guards']['a'] and '不挤主章第三户床' in qs['CS-DEN-03']['dramatic_guards']['b'],'ritual-refusal-keeps-signed-stay-and-real-care')
check('贝洛是另一位箍桶学徒' in qs['CM-MNS']['dramatic_scenes'][1]['basis'] and casts['MNS']['ti']['id']!=casts['MNS']['be']['id'],'wine-and-barrel-apprentices-distinct')
check('不预支未卖新酒退款' in qs['CM-MNS']['dramatic_guards']['newlabel'] and '逐瓶实际注明新酿' in qs['CM-MNS']['dramatic_guards']['limited'],'no-fake-vintage-or-unearned-refund-cash')
check('拒替代保原款' in qs['CS-MNS-01']['dramatic_guards']['b'] and '不重发SQ07' in qs['CS-MNS-01']['dramatic_guards']['a'],'container-refusal-retains-money-and-no-double-certification')
check('不强试塌' in qs['CS-MNS-02']['dramatic_guards']['a'] and '不抢原工具' in qs['CS-MNS-02']['dramatic_guards']['b'],'safe-empty-test-and-real-independent-tool-rights')
check('限定一季分收' in qs['CS-MNS-03']['dramatic_guards']['a'] and '不把私人约改成全镇地法' in qs['CS-MNS-03']['dramatic_guards']['a'],'one-season-not-all-land-title')
check('专业有限移枝可行且迁居者真愿' in qs['CS-MNS-03']['dramatic_guards']['b'] and '不能强拔' in qs['CS-MNS-03']['dramatic_guards']['b'],'actual-voluntary-feasible-vine-move-and-risk')
for file in ['shore-vine-generated-note-hashes.json','city-generated-note-hashes.json','city-space-note-hashes.json']:
 for rel,h in read('research/'+file).items():check(sha(ROOT/rel)==h,rel+'-authoring-hash')
check(len(read('research/shore-vine-generated-note-hashes.json'))==11,'ten-new-cards-and-one-audit')
coverage=sum('dramatic_scenes' in q for q in m['quests']);check(coverage==41+sum(q['city'] in ['EED','FOR','OSB','RAT','KOR','PAS'] and 'dramatic_scenes' in q for q in m['quests']),'scoped-authored-coverage-no-false-full-coverage')
report=dict(date='2026-10-12',scope='S81 exact authoring/rendering, scoped actors and spaces, existing branches/receipts and stated domain regressions; not literary quality, numeric economy, collision or game runtime',quests=8,scenes=scene_count,methods=method_count,unique_actors=len(unique),new_cards=len(newactors),dialogue_utterances=utterances,choice_answers=choice_count,early_late_pairs=len(all_feedback),covered_city_quests=coverage,pending_city_quests=73-coverage,checks_passed=len(checks),errors=errors,passed=not errors,runtimeVerified=False)
(ROOT/'research/shore-vine-drama-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
