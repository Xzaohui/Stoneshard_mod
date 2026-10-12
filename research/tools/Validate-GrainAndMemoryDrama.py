"""S83 exact grain/memory scenes, distinct families, limited actual stock and current protection."""
from pathlib import Path
import json,hashlib
from ScopedDramaCoverage import matching_additional_source
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read('research/city-campaign.json');old=read('backups/city-drama-20261012-s83/city-campaign.json');qs={q['id']:q for q in m['quests']};oq={q['id']:q for q in old['quests']};effects={e['id']:e for e in m['effects']};checks=[];errors=[]
def check(ok,label):(checks if ok else errors).append(label)
expected={cid:{'CM-'+cid}|{f'CS-{cid}-{i:02}' for i in range(1,4)} for cid in ['OSB','RAT']};covered=set.union(*expected.values())
check(m['verified_runtime'] is False,'not-runtime-verified')
for key in ['effects','rules','travel','verified_runtime']:check(m[key]==old[key],'preserve-all-'+key)
for qid,q in qs.items():
 for key in ['id','city','routes','requires','stages','locations','need','turn','title','kind']:check(q[key]==oq[qid][key],qid+'-structural-'+key)
 if q['city'] in ['KOR','PAS'] and 'dramatic_scenes' in q:
  check(matching_additional_source(ROOT,q),qid+'-exact-later-S84-source');continue
 if qid not in covered:
  for key in set(q)|set(oq[qid]):
   if key.startswith('dramatic_'):check(q.get(key)==oq[qid].get(key),qid+'-other-city-unchanged-'+key)
for cid,cast in old['dramatic_casts'].items():check(m['dramatic_casts'][cid]==cast,cid+'-previous-cast-intact')
casts={cid:m['dramatic_casts'][cid] for cid in expected};unique={a['id'] for c in casts.values() for a in c.values()};newactors={a['id']:a for c in casts.values() for a in c.values() if not a['existing']}
check([len(casts[c]) for c in ['OSB','RAT']]==[11,8] and len(unique)==19 and len(newactors)==11,'19-distinct-actors-eleven-new-cards')
check(not ({a['id'] for a in casts['OSB'].values()} & {a['id'] for a in casts['RAT'].values()}),'no-grain-or-memory-identity-clone')
check(not (unique & {a['id'] for cid,c in old['dramatic_casts'].items() for a in c.values()}),'previous-cities-actors-not-repurposed')
for cid,cast in casts.items():
 check(len({a['id'] for a in cast.values()})==len(cast),cid+'-unique-local-identities')
 for a in cast.values():
  p=V/a['file'];check(p.exists() and a['name'] in p.read_text(encoding='utf-8'),a['id']+'-linked-card-name')
scene_count=utterances=choice_count=method_count=0;all_feedback=[]
for cid,slug in [('OSB','osbrook'),('RAT','ratten')]:
 src=read(f'research/{slug}-drama.json');fs=read(src['feedback_source']);cast=casts[cid];nodes={n['id']:n for c in m['cities'] if c['id']==cid for n in c['nodes']};source_feedback={f[0]:f for f in fs}
 check(set(src['quests'])==expected[cid],cid+'-one-main-three-sides')
 check(len(fs)==len(source_feedback)==(15 if cid=='OSB' else 14),cid+'-authored-feedback-unique')
 for qid in sorted(expected[cid]):
  q=qs[qid];text=(V/q['file']).read_text(encoding='utf-8');spec=src['quests'][qid]
  check(matching_additional_source(ROOT,q),qid+'-exact-current-authored-source')
  check('场次与对白（S83当前稿）' in text and '有限回执的具体回应（S83）' in text,qid+'-current-render-markers')
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
check('CS-OSB-03蔻芙／德娅为另一家庭' in qs['CM-OSB']['dramatic_stage_note'] and casts['OSB']['fu']['id']!=casts['OSB']['co']['id'],'two-adult-daughters-and-families-not-collapsed')
check('不默认退出户贡献' in qs['CM-OSB']['dramatic_guards']['seed'] and '合法旧债另核' in qs['CM-OSB']['dramatic_guards']['seed'],'seed-needs-real-voluntary-grain-not-total-debt-erasure')
check('限一季数量预购' in qs['CM-OSB']['dramatic_guards']['advance'] and '不买全部土地／未来劳动' in qs['CM-OSB']['dramatic_guards']['advance'],'one-season-not-land-or-lifetime-sale')
check('先实际释放本案可播底种与撤新增强制磨工' in qs['CM-OSB']['dramatic_guards']['advance'] and any('还没落到手就还没交' in line for who,line in qs['CM-OSB']['dramatic_scenes'][2]['lines']),'both-grain-methods-release-seed-and-previews-do-not-invent-handover')
check('路费实交本人保管不先抵父债' in qs['CS-OSB-01']['dramatic_guards']['a'] and '不给父亲新代签权' in qs['CS-OSB-01']['dramatic_guards']['b'],'travel-money-first-and-real-stay-alternative')
check(casts['OSB']['lo']['name']=='洛珊' and '洛珊本人自愿有限修筐班实际教收口／接篾' in qs['CS-OSB-01']['dramatic_guards']['b'] and any(who=='lo' for who,_ in qs['CS-OSB-01']['dramatic_scenes'][1]['lines']),'named-present-mentor-and-specific-real-lesson')
check('不将退出户自动计主章共粮贡献' in qs['CS-OSB-02']['dramatic_guards']['a'] and '先实际保各户普通出入与钥' in qs['CS-OSB-02']['dramatic_guards']['b'],'exit-and-keys-before-renewal-no-forced-grain')
check('公共取水分别限核' in qs['CS-OSB-03']['dramatic_guards']['a'] and '普通公共用水、村路与服务保' in qs['CS-OSB-03']['dramatic_guards']['b'],'marriage-land-water-distinct-and-safe-refusal')
check('伪响与当前普通野兽为两条实因' in qs['CM-RAT']['dramatic_stage_note'] and '不强夜战或击杀计数' in qs['CM-RAT']['dramatic_stage_note'],'fake-sound-does-not-cancel-current-protection')
check('不宣布爵士新生死／旧兽复活' in qs['CM-RAT']['dramatic_guards']['addendum'] and '不把私下记忆当自动无限赔付' in qs['CM-RAT']['dramatic_guards']['family'],'historical-uncertainty-and-finite-multiple-memory')
check('不将芬罗未做冒领写成已领' in qs['CS-RAT-01']['dramatic_guards']['a'] and '不放畜重演' in qs['CS-RAT-01']['dramatic_guards']['b'],'new-loss-real-name-and-no-manufactured-crime-or-harm')
check('不预支未售新章' in qs['CS-RAT-02']['dramatic_guards']['a'] and '不动原爵士史实' in qs['CS-RAT-02']['dramatic_guards']['b'],'replica-price-refund-needs-real-money-not-history-rewrite')
check('实际撤出席／购章／信仰换基本给付' in qs['CS-RAT-03']['dramatic_guards']['a'] and '未安全修铃则停用保普通路' in qs['CS-RAT-03']['dramatic_guards']['b'],'basic-aid-not-ceremony-ticket-and-real-safe-road')
for file in ['grain-memory-generated-note-hashes.json','city-generated-note-hashes.json','city-space-note-hashes.json']:
 for rel,h in read('research/'+file).items():check(sha(ROOT/rel)==h,rel+'-authoring-hash')
check(len(read('research/grain-memory-generated-note-hashes.json'))==12,'eleven-new-cards-and-one-audit')
coverage=sum('dramatic_scenes' in q for q in m['quests']);check(coverage==57+sum(q['city'] in ['KOR','PAS'] and 'dramatic_scenes' in q for q in m['quests']),'scoped-authored-coverage-no-false-full-coverage')
report=dict(date='2026-10-12',scope='S83 exact source/rendering, distinct adult families, current risk and limited actual resource guards, unchanged existing methods/receipts; not literary quality, numeric economy, collision or runtime',quests=8,scenes=scene_count,methods=method_count,unique_actors=len(unique),new_cards=len(newactors),dialogue_utterances=utterances,choice_answers=choice_count,early_late_pairs=len(all_feedback),covered_city_quests=coverage,pending_city_quests=73-coverage,checks_passed=len(checks),errors=errors,passed=not errors,runtimeVerified=False)
(ROOT/'research/grain-memory-drama-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False));raise SystemExit(0 if report['passed'] else 1)
