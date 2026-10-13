"""S84 exact grain/memory scenes, distinct families, limited actual stock and current protection."""
from pathlib import Path
import json,hashlib
from ScopedDramaCoverage import matching_additional_source
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read('research/city-campaign.json');old=read('backups/city-drama-20261012-s84/city-campaign.json');qs={q['id']:q for q in m['quests']};oq={q['id']:q for q in old['quests']};effects={e['id']:e for e in m['effects']};checks=[];errors=[]
def check(ok,label):(checks if ok else errors).append(label)
expected={cid:{'CM-'+cid}|{f'CS-{cid}-{i:02}' for i in range(1,4)} for cid in ['KOR','PAS']};covered=set.union(*expected.values())
check(m['verified_runtime'] is False,'not-runtime-verified')
for key in ['effects','rules','travel','verified_runtime']:check(m[key]==old[key],'preserve-all-'+key)
for qid,q in qs.items():
 for key in ['id','city','routes','requires','stages','locations','need','turn','title','kind']:check(q[key]==oq[qid][key],qid+'-structural-'+key)
 if qid not in covered:
  if q['city'] in ['ASH','HIG'] and q.get('dramatic_revision')=='S86':
   check(matching_additional_source(ROOT,q),qid+'-separate-exact-S86-authored-source')
  else:
   for key in set(q)|set(oq[qid]):
    if key.startswith('dramatic_'):check(q.get(key)==oq[qid].get(key),qid+'-other-city-unchanged-'+key)
for cid,cast in old['dramatic_casts'].items():check(m['dramatic_casts'][cid]==cast,cid+'-previous-cast-intact')
casts={cid:m['dramatic_casts'][cid] for cid in expected};unique={a['id'] for c in casts.values() for a in c.values()};newactors={a['id']:a for c in casts.values() for a in c.values() if not a['existing']}
check([len(casts[c]) for c in ['KOR','PAS']]==[11,9] and len(unique)==20 and len(newactors)==12,'20-distinct-actors-twelve-new-cards')
check(not ({a['id'] for a in casts['KOR'].values()} & {a['id'] for a in casts['PAS'].values()}),'no-custody-or-pass-identity-clone')
check(not (unique & {a['id'] for cid,c in old['dramatic_casts'].items() for a in c.values()}),'previous-cities-actors-not-repurposed')
for cid,cast in casts.items():
 check(len({a['id'] for a in cast.values()})==len(cast),cid+'-unique-local-identities')
 for a in cast.values():
  p=V/a['file'];check(p.exists() and a['name'] in p.read_text(encoding='utf-8'),a['id']+'-linked-card-name')
scene_count=utterances=choice_count=method_count=0;all_feedback=[]
for cid,slug in [('KOR','korde'),('PAS','passgate')]:
 src=read(f'research/{slug}-drama.json');fs=read(src['feedback_source']);cast=casts[cid];nodes={n['id']:n for c in m['cities'] if c['id']==cid for n in c['nodes']};source_feedback={f[0]:f for f in fs}
 check(set(src['quests'])==expected[cid],cid+'-one-main-three-sides')
 check(len(fs)==len(source_feedback)==14,cid+'-authored-feedback-unique')
 for qid in sorted(expected[cid]):
  q=qs[qid];text=(V/q['file']).read_text(encoding='utf-8');spec=src['quests'][qid]
  check(matching_additional_source(ROOT,q),qid+'-exact-current-authored-source')
  check('场次与对白（S84当前稿）' in text and '有限回执的具体回应（S84）' in text,qid+'-current-render-markers')
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
check(len(all_feedback)==len(set(all_feedback))==28 and set(all_feedback)=={e['id'] for e in m['effects'] if e['target'] in covered},'all-28-receipts-exactly-once')
check(scene_count==24 and method_count==16 and choice_count==48,'24-scenes-16-methods-48-answers')
check(casts['KOR']['ev']['id']!=casts['KOR']['sa']['id'] and '兰衍为另一未到旅人，不是已经在场的埃文' in qs['CS-KOR-01']['dramatic_scenes'][0]['basis'],'arrived-traveller-missing-brother-and-adult-distinct')
check('赛洛明确为成年' in qs['CS-KOR-02']['dramatic_scenes'][0]['basis'] and '不设未成年人法律系统或隐藏王室' in qs['CS-KOR-02']['dramatic_scenes'][0]['basis'],'adult-and-no-invented-royal-status')
check('拼接全权家属实际撤' in qs['CM-KOR']['dramatic_guards']['limited'] and '不把物柜锁成人身去向' in qs['CM-KOR']['dramatic_guards']['custody'],'item-family-and-room-have-separate-rights')
check('不生永久整月代理' in qs['CS-KOR-01']['dramatic_guards']['b'] and '未付留欠' in qs['CS-KOR-01']['dramatic_guards']['a'],'one-night-and-real-disputed-funds-no-fictitious-arrival')
check('固定本件事实核并实际单件交接' in qs['CS-KOR-02']['dramatic_guards']['b'] and '不含住处、债务、未来劳动／下一件' in qs['CS-KOR-02']['dramatic_guards']['b'],'voluntary-single-item-proxy-not-universal-kinship')
check('拒买不伪成交，不生官方族史' in qs['CS-KOR-03']['dramatic_guards']['a'] and '不要求先找名字' in qs['CS-KOR-03']['dramatic_guards']['b'],'unknown-portrait-remains-unknown-and-has-real-sale-or-custody')
check(casts['PAS']['re']['id']=='NPC-REY' and casts['PAS']['mo']['id']=='NPC-MORREN' and '礼昂为独立普通病例' in qs['CM-PAS']['dramatic_stage_note'],'existing-rey-morren-and-distinct-ordinary-patient')
check('未补民粮与未承诺仍保' in qs['CM-PAS']['dramatic_guards']['joint'] and '不再发N7／SQ02／CO奖励资格' in qs['CM-PAS']['dramatic_guards']['joint'],'new-local-agreement-does-not-upgrade-old-military-result')
check('不附未来作工才兑' in qs['CS-PAS-01']['dramatic_guards']['a'] and '已做旧薪未偿保欠不注销' in qs['CS-PAS-01']['dramatic_guards']['b'],'earned-wages-not-next-labour-and-bypass-keeps-debt')
check('不省N7配对' in qs['CS-PAS-02']['dramatic_guards']['a'] and '一人一床与实给量去重' in qs['CS-PAS-02']['dramatic_guards']['b'],'one-ordinary-patient-not-two-device-partners-or-two-beds')
check('原信实际投递交出' in qs['CS-PAS-03']['dramatic_guards']['a'] and '可信绮伦本人真实在场接本人准句' in qs['CS-PAS-03']['dramatic_guards']['b'],'letter-leaves-inventory-and-oral-message-needs-real-receiver')
check(sha(ROOT/'research/story-network.json')==sha(ROOT/'backups/city-drama-20261012-s84/story-network.json'),'original-N7-SQ02-and-all-legacy-routes-unchanged')
for cid in expected:
 for qid in expected[cid]:
  for s in qs[qid]['dramatic_scenes']:
   spoken=[line for _,line in s['lines']]+[v for _,label,_,_,answer in s['choices'] for v in [label,answer]]
   for line in spoken:
    import re
    check(not re.search(r'\b(?:N\d+|SQ\d+|CO)\b|爵位奖|送一遍奖|resolve|paid',line),qid+'-world-voice-not-backstage-identifier')
letter=V/'05_主线/城市篇章/文书_PAS_列梵的家书与口信.md';lt=letter.read_text(encoding='utf-8')
check(all(s in lt for s in ['PAS-LETTER-LEVAN-ONE','PAS-LETTER-LEVAN-COPY','不仍在玩家背包','只有本人准副件','口信路线','重读不推进']),'letter-and-copy-world-text-real-single-item-lifecycle')
check('[[文书_PAS_列梵的家书与口信]]' in (V/qs['CS-PAS-03']['file']).read_text(encoding='utf-8') and '[[台本_CS-PAS-03_关外的最后一封]]' in lt,'letter-task-bidirectional-links')
for file in ['names-pass-generated-note-hashes.json','city-generated-note-hashes.json','city-space-note-hashes.json']:
 for rel,h in read('research/'+file).items():check(sha(ROOT/rel)==h,rel+'-authoring-hash')
check(len(read('research/names-pass-generated-note-hashes.json'))==14,'twelve-new-cards-one-letter-and-one-audit')
coverage=sum('dramatic_scenes' in q for q in m['quests']);check(coverage==73,'73-authored-no-pending')
report=dict(date='2026-10-12',scope='S84 exact source/rendering, limited identity and real letter/bed/wages, preserved original N7/SQ02 methods and old receipts; not literary quality, numeric economy, collision or runtime',quests=8,scenes=scene_count,methods=method_count,unique_actors=len(unique),new_cards=len(newactors),dialogue_utterances=utterances,choice_answers=choice_count,early_late_pairs=len(all_feedback),world_texts=1,covered_city_quests=coverage,pending_city_quests=73-coverage,checks_passed=len(checks),errors=errors,passed=not errors,runtimeVerified=False)
(ROOT/'research/names-pass-drama-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
