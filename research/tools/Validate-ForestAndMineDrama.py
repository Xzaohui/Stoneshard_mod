"""S82 exact authored forest/mine tasks, limited rights, safe rescue and old-edge preservation."""
from pathlib import Path
import json,hashlib
from ScopedDramaCoverage import matching_additional_source
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read('research/city-campaign.json');old=read('backups/city-drama-20261012-s82/city-campaign.json');qs={q['id']:q for q in m['quests']};oq={q['id']:q for q in old['quests']};effects={e['id']:e for e in m['effects']};checks=[];errors=[]
def check(ok,label):(checks if ok else errors).append(label)
expected={cid:{'CM-'+cid}|{f'CS-{cid}-{i:02}' for i in range(1,4)} for cid in ['EED','FOR']};covered=set.union(*expected.values())
check(m['verified_runtime'] is False,'not-runtime-verified')
for key in ['effects','rules','travel','verified_runtime']:check(m[key]==old[key],'preserve-all-'+key)
for qid,q in qs.items():
 for key in ['id','city','routes','requires','stages','locations','need','turn','title','kind']:check(q[key]==oq[qid][key],qid+'-structural-'+key)
 if q['city'] in ['OSB','RAT','KOR','PAS'] and 'dramatic_scenes' in q:
  check(matching_additional_source(ROOT,q),qid+'-exact-later-scoped-source');continue
 if qid not in covered:
  for key in set(q)|set(oq[qid]):
   if key.startswith('dramatic_'):check(q.get(key)==oq[qid].get(key),qid+'-other-city-unchanged-'+key)
for cid,cast in old['dramatic_casts'].items():check(m['dramatic_casts'][cid]==cast,cid+'-previous-cast-intact')
casts={cid:m['dramatic_casts'][cid] for cid in expected};unique={a['id'] for c in casts.values() for a in c.values()};newactors={a['id']:a for c in casts.values() for a in c.values() if not a['existing']}
check([len(casts[c]) for c in ['EED','FOR']]==[10,8] and len(unique)==18 and len(newactors)==10,'18-distinct-actors-ten-new-cards')
check(not ({a['id'] for a in casts['EED'].values()} & {a['id'] for a in casts['FOR'].values()}),'no-forest-or-mine-identity-clone')
check(not (unique & {a['id'] for cid,c in old['dramatic_casts'].items() for a in c.values()}),'previous-cities-actors-not-repurposed')
for cid,cast in casts.items():
 check(len({a['id'] for a in cast.values()})==len(cast),cid+'-unique-local-identities')
 for a in cast.values():
  p=V/a['file'];check(p.exists() and a['name'] in p.read_text(encoding='utf-8'),a['id']+'-linked-card-name')
scene_count=utterances=choice_count=method_count=0;all_feedback=[]
for cid,slug in [('EED','eeders'),('FOR','forholt')]:
 src=read(f'research/{slug}-drama.json');fs=read(src['feedback_source']);cast=casts[cid];nodes={n['id']:n for c in m['cities'] if c['id']==cid for n in c['nodes']};source_feedback={f[0]:f for f in fs}
 check(set(src['quests'])==expected[cid],cid+'-one-main-three-sides')
 check(len(fs)==len(source_feedback)==(14 if cid=='EED' else 15),cid+'-authored-feedback-unique')
 for qid in sorted(expected[cid]):
  q=qs[qid];text=(V/q['file']).read_text(encoding='utf-8');spec=src['quests'][qid]
  check(matching_additional_source(ROOT,q),qid+'-exact-current-authored-source')
  check('场次与对白（S82当前稿）' in text and '有限回执的具体回应（S82）' in text,qid+'-current-render-markers')
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
check(len(all_feedback)==len(set(all_feedback))==29 and set(all_feedback)=={e['id'] for e in m['effects'] if e['target'] in covered},'all-29-receipts-exactly-once')
check(scene_count==24 and method_count==16 and choice_count==48,'24-scenes-16-methods-48-answers')
check('不擅拆仍住人的梁' in qs['CM-EED']['dramatic_guards']['oldstock'] and '未付留欠不伪到账' in qs['CM-EED']['dramatic_guards']['localfirst'],'limited-orders-not-homes-or-fictitious-refunds')
check('健康林不补单' in qs['CS-EED-01']['dramatic_guards']['a'] and '不以家门名单换图样' in qs['CS-EED-01']['dramatic_guards']['b'],'disease-limit-not-family-or-tech-gate')
check('路费先实际到位' in qs['CS-EED-02']['dramatic_guards']['a'] and '未安置不拆住梁' in qs['CS-EED-02']['dramatic_guards']['a'],'real-housing-before-demolition')
check('其它登记旧材真实未占量' in qs['CS-EED-02']['dramatic_guards']['b'] and '不做玩家搬梁循环' in qs['CS-EED-02']['dramatic_guards']['b'],'independent-finite-timber-not-hauling-loop')
check('不保证旧地址无人知道' in qs['CS-EED-03']['dramatic_guards']['a'] and '不销真实旧债' in qs['CS-EED-03']['dramatic_guards']['a'],'future-privacy-keeps-leak-and-debt-history')
check('不以还款或交家名换巡林' in qs['CS-EED-03']['dramatic_guards']['b'] and '不生成永驻无限班' in qs['CS-EED-03']['dramatic_guards']['b'],'independent-finite-patrol-and-valid-alerts')
check('祁铎若未救出仍在井下不在此发言' in qs['CM-FOR']['dramatic_scenes'][0]['setup'] and all(who!='qi' for who,_ in qs['CM-FOR']['dramatic_scenes'][0]['lines']),'injured-miner-not-at-surface-before-rescue')
check('安全救援立即进行' in qs['CM-FOR']['dramatic_stage_note'] and '实际出井且自愿会面' in qs['CM-FOR']['dramatic_scenes'][2]['setup'],'rescue-before-political-resolution-and-real-position')
check('会面前已启动' in qs['CM-FOR']['dramatic_scenes'][0]['setup'] and '制度结案不关闭未完救援' in qs['CM-FOR']['dramatic_guards']['workerstop'],'rescue-is-already-active-and-has-separate-lifecycle')
check(any('水费若已付' in line and '没付的还只是承诺' in line for who,line in qs['CM-FOR']['dramatic_scenes'][2]['lines']),'main-first-does-not-invent-paid-water-side')
check('不索全病例' in qs['CM-FOR']['dramatic_guards']['external'] and '不要求伤者复井' in qs['CM-FOR']['dramatic_guards']['workerstop'],'inspection-no-medical-omniscience-or-reentry-price')
check('不授新骑卫效忠' in qs['CS-FOR-01']['dramatic_guards']['a'] and '拒公开保普通服务' in qs['CS-FOR-01']['dramatic_guards']['b'],'historical-cup-no-active-cavalry-or-publicity-gate')
check('拒和解不取消基本替水' in qs['CS-FOR-02']['dramatic_guards']['b'] and '不重复占底薪池' in qs['CS-FOR-02']['dramatic_guards']['a'],'water-before-settlement-and-single-budget')
check('不自动捐回工资池' in qs['CS-FOR-03']['dramatic_guards']['b'] and '共同份与主章已占段不重复造份' in qs['CS-FOR-03']['dramatic_guards']['a'],'share-sale-is-not-double-wages-or-automatic-donation')
for file in ['forest-mine-generated-note-hashes.json','city-generated-note-hashes.json','city-space-note-hashes.json']:
 for rel,h in read('research/'+file).items():check(sha(ROOT/rel)==h,rel+'-authoring-hash')
check(len(read('research/forest-mine-generated-note-hashes.json'))==11,'ten-new-cards-and-one-audit')
coverage=sum('dramatic_scenes' in q for q in m['quests']);check(coverage==49+sum(q['city'] in ['OSB','RAT','KOR','PAS'] and 'dramatic_scenes' in q for q in m['quests']),'scoped-authored-coverage-no-false-full-coverage')
report=dict(date='2026-10-12',scope='S82 exact source/rendering, forest/mine identities, actual rescue and finite resource guards, preserved existing branches/receipts; not literary quality, numeric economy, collision or runtime',quests=8,scenes=scene_count,methods=method_count,unique_actors=len(unique),new_cards=len(newactors),dialogue_utterances=utterances,choice_answers=choice_count,early_late_pairs=len(all_feedback),covered_city_quests=coverage,pending_city_quests=73-coverage,checks_passed=len(checks),errors=errors,passed=not errors,runtimeVerified=False)
(ROOT/'research/forest-mine-drama-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
