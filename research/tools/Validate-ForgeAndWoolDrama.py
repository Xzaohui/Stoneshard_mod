"""S80 source/rendering, shared identity and preserved narrative contract verification."""
from pathlib import Path
import json,hashlib
from ScopedDramaCoverage import matching_additional_source
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read('research/city-campaign.json');old=read('backups/city-drama-20261012-s80-art-followup/city-campaign.json');qs={q['id']:q for q in m['quests']};oq={q['id']:q for q in old['quests']};effects={e['id']:e for e in m['effects']};checks=[];errors=[]
def check(ok,label):(checks if ok else errors).append(label)
expected={cid:{'CM-'+cid}|{f'CS-{cid}-{i:02}' for i in range(1,4)} for cid in ['SKO','YOS']};covered=set.union(*expected.values())
check(m['verified_runtime'] is False,'not-runtime-verified')
for key in ['effects','rules','travel','verified_runtime']:check(m[key]==old[key],'preserve-all-'+key)
for qid,q in qs.items():
 for key in ['id','city','routes','requires','stages','locations','need','turn','title','kind']:check(q[key]==oq[qid][key],qid+'-structural-'+key)
 if q['city'] in ['DEN','MNS','EED','FOR','OSB','RAT','KOR','PAS'] and 'dramatic_scenes' in q:
  check(matching_additional_source(ROOT,q),qid+'-separate-exact-s81-source')
 elif qid not in covered:
  for key in set(q)|set(oq[qid]):
   if key.startswith('dramatic_'):check(q.get(key)==oq[qid].get(key),qid+'-other-city-unchanged-'+key)
for cid,cast in old['dramatic_casts'].items():check(m['dramatic_casts'][cid]==cast,cid+'-previous-cast-intact')
casts={cid:m['dramatic_casts'][cid] for cid in expected};unique={a['id'] for c in casts.values() for a in c.values()};newactors={a['id']:a for c in casts.values() for a in c.values() if not a['existing']}
check([len(casts[c]) for c in ['SKO','YOS']]==[8,9] and len(unique)==16 and len(newactors)==8,'17-scoped-slots-16-identities-eight-new-cards')
check({a['id'] for a in casts['SKO'].values()} & {a['id'] for a in casts['YOS'].values()}=={'TRADE-NPC-LIQUI'},'only-shared-identity-is-liqui')
check(casts['SKO']['li']['file']==casts['YOS']['li']['file'] and casts['YOS']['li']['existing'] and casts['SKO']['li']['shared_cities']==['SKO','YOS'],'one-shared-trader-card-and-source')
check(not (unique & {a['id'] for cid,c in old['dramatic_casts'].items() for a in c.values()}),'previous-cities-actors-not-repurposed')
for cid,cast in casts.items():
 check(len({a['id'] for a in cast.values()})==len(cast),cid+'-unique-local-identities')
 for a in cast.values():
  p=V/a['file'];check(p.exists() and a['name'] in p.read_text(encoding='utf-8'),a['id']+'-linked-card-name')
scene_count=utterances=choice_count=method_count=0;all_feedback=[]
for cid,slug in [('SKO','skonfert'),('YOS','yostwayne')]:
 src=read(f'research/{slug}-drama.json');fs=read(src['feedback_source']);cast=casts[cid];nodes={n['id']:n for c in m['cities'] if c['id']==cid for n in c['nodes']};source_feedback={f[0]:f for f in fs}
 check(set(src['quests'])==expected[cid],cid+'-one-main-three-sides')
 check(len(fs)==len(source_feedback)==(14 if cid=='SKO' else 16),cid+'-authored-feedback-unique')
 for qid in sorted(expected[cid]):
  q=qs[qid];text=(V/q['file']).read_text(encoding='utf-8');spec=src['quests'][qid]
  check(matching_additional_source(ROOT,q),qid+'-exact-current-authored-source')
  check('场次与对白（S80当前稿）' in text and '有限回执的具体回应（S80）' in text,qid+'-current-render-markers')
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
check('另一户已归者' in qs['CM-SKO']['dramatic_stage_note'] and '弟弟仍未归' in qs['CM-SKO']['dramatic_stage_note'],'boher-is-not-nishas-missing-brother')
check('真实可用未占款实际支付' in qs['CM-SKO']['dramatic_guards']['sale'] and '不售归人劳力' in qs['CM-SKO']['dramatic_guards']['sale'],'billet-sale-needs-free-cash-and-no-personal-sale')
check('独立炉料资金缺则延后' in qs['CS-SKO-01']['dramatic_guards']['a'] and '同笔不两次抵押' in qs['CS-SKO-01']['dramatic_guards']['a'],'ransom-and-wages-not-funded-twice')
check('本人当前拒公开' in qs['CS-SKO-02']['dramatic_guards']['b'] and '普通住处' in qs['CS-SKO-02']['dramatic_exceptions']['refusal'],'quiet-home-life-is-a-valid-exit')
check('保私人护符' in qs['CS-SKO-03']['dramatic_guards']['a'] and '不重复碰水取证' in qs['CS-SKO-03']['dramatic_guards']['b'],'faith-not-care-gate-and-no-harm-reenactment')
check('同一身体跨CS-YOS-02' in qs['CM-YOS']['dramatic_stage_note'],'one-adult-dyer-apprentice-in-two-tasks')
check('实际归本人路费' in qs['CS-YOS-02']['dramatic_guards']['a'] and '路费先实际交本人保管' in qs['CS-YOS-02']['dramatic_guards']['b'],'bag-and-money-returned-before-stay-consent')
check('拒不合用衣保底量限售出口' in qs['CS-YOS-01']['dramatic_exceptions']['refusal'] and '同衣同毛不两案承诺' in qs['CS-YOS-01']['dramatic_guards']['b'],'unsuitable-clothing-refusal-has-finite-winter-fallback')
check('阿洛是一个本地' in qs['CS-YOS-03']['dramatic_scenes'][0]['basis'] and '不全罚迁户' in qs['CS-YOS-03']['dramatic_guards']['a'],'specific-local-act-not-migrant-collective-guilt')
check('源责任未知待查' in qs['CS-YOS-03']['dramatic_guards']['b'] and '旧排斥' in qs['CS-YOS-03']['dramatic_exceptions']['after_city'],'safe-stop-preserves-unknowns-and-past-harm')
li=(V/casts['SKO']['li']['file']).read_text(encoding='utf-8');check(all(t in li for t in ['同一身体','同一笔周转','两市都不能同时','撤单只释放未执行段','旧坯未卖出不能当收益']),'shared-trader-finite-assets-and-physical-location')
for file in ['forge-wool-generated-note-hashes.json','city-generated-note-hashes.json','city-space-note-hashes.json']:
 for rel,h in read('research/'+file).items():check(sha(ROOT/rel)==h,rel+'-authoring-hash')
check(len(read('research/forge-wool-generated-note-hashes.json'))==9,'eight-new-cards-and-one-audit')
coverage=sum('dramatic_scenes' in q for q in m['quests']);check(coverage==33+sum(q['city'] in ['DEN','MNS','EED','FOR','OSB','RAT','KOR','PAS'] and 'dramatic_scenes' in q for q in m['quests']),'scoped-authored-coverage-no-false-full-coverage')
report=dict(date='2026-10-12',scope='S80 exact authoring/rendering, scoped actors and spaces, existing branches/receipts and stated domain regressions; not literary quality, numeric economy, collision or game runtime',quests=8,scenes=scene_count,methods=method_count,unique_actors=len(unique),new_cards=len(newactors),dialogue_utterances=utterances,choice_answers=choice_count,early_late_pairs=len(all_feedback),covered_city_quests=coverage,pending_city_quests=73-coverage,checks_passed=len(checks),errors=errors,passed=not errors,runtimeVerified=False)
(ROOT/'research/forge-wool-drama-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
