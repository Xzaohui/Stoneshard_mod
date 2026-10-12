"""S76 authored dialogue replaces the emitted S63 sketch for covered quests only."""
from pathlib import Path
import json

def sources(root):
 return (json.loads((root/'research/brynn-drama.json').read_text(encoding='utf-8')),
         json.loads((root/'research/brynn-feedback.json').read_text(encoding='utf-8')))

def apply_city_drama(root,model):
 data,feedback=sources(root);qs={q['id']:q for q in model['quests']};existing={}
 for c in model['cities']:
  for name,role,arc,pid in c['people']:existing[pid]=f'04_人物/城市人物/人物_{pid}_{name}.md'
  for sat in c['satellites']:existing[sat['resident']['id']]=sat['resident']['file']
 cast={}
 for key,a in data['cast'].items():
  a=dict(a);a['file']=existing[a['id']] if a['existing'] else f"04_人物/城市人物/人物_{a['id']}_{a['name']}.md"
  cast[key]=a
 model['dramatic_cast']=cast;model['dramatic_source']='research/brynn-drama.json'
 model['dramatic_scope']='S76 active BRY dialogue; stages retain S63 geographical sketch, not active lines for covered quests.'
 for qid,spec in data['quests'].items():
  q=qs[qid];assert q['city']=='BRY' and len(spec['scenes'])==len(q['locations'])
  assert set(spec['followups'])==set(spec['route_guards'])=={r['key'] for r in q['routes']}
  q['dramatic_scenes']=spec['scenes'];q['dramatic_stage_note']=spec.get('stage_note','')
  q['dramatic_followups']=spec['followups'];q['dramatic_guards']=spec['route_guards'];q['dramatic_exceptions']=spec['exceptions']
  q['dramatic_feedback']=[]
 effects={e['id']:e for e in model['effects']}
 def add(eid,speaker,early,late,action):
  e=effects[eid];assert e['target'] in data['quests'] and speaker in cast
  qs[e['target']]['dramatic_feedback'].append(dict(effect=eid,speaker=speaker,known_fact=e['receipt'],early_line=early,late_line=late,
    early_action=action,late_scope='Only future dialogue/arrangements; never reselect resolved method, reverse damage, duplicate stock or payment, or unfreeze N17.'))
 for source,routes in feedback['main_receipts'].items():
  for method,(early,late,action) in routes.items():add('LX-'+source+'-'+method,'re',early,late,action)
 for target,profiles in feedback['after_main'].items():
  speaker=profiles['speaker']
  for method in ['civic','separate','patron']:
   early,action=profiles[method]
   add('MG-'+target+'-'+method,speaker,early,feedback['after_main_late'][target][method],action)
 for eid,speaker,early,late in feedback['external']:add(eid,speaker,early,late,effects[eid]['change'])
 from AdditionalCityDrama import apply_additional_city_drama
 apply_additional_city_drama(root,model,existing)
 return model

def actor(cast,key):return '玩家' if key=='玩家' else '[['+Path(cast[key]['file']).stem+']]'
def line(cast,key,words):return actor(cast,key)+'：「'+words+'」\n\n'

def render_scenes(q,model):
 cast=model.get('dramatic_casts',{}).get(q['city'],model['dramatic_cast']);b='## 场次与对白（'+q.get('dramatic_revision','S76')+'当前稿）\n\n'
 b+='以下替换S63三句询问模板，模型中的stages只保留原地理骨架。场景是可复入的对白素材，不是一口气自动播放的独白；玩家可先到后场看固定物，未获信息改用询问，不预知秘密。每句只在说话者存活、在场且具该句来源时显示。私下场另问授权；不生成第二个同名角色凑场。\n\n'
 if q['dramatic_stage_note']:b+='**时序修订**：'+q['dramatic_stage_note']+'\n\n'
 for i,s in enumerate(q['dramatic_scenes'],1):
  b+=f"### 场{i}：{s['title']}\n\n位置 `{s['space']}`；所属原场节点 `{q['locations'][i-1]}`。\n\n**调度**：{s['setup']}\n\n**知情边界**：{s['basis']}\n\n"
  for who,words in s['lines']:b+=line(cast,who,words)
  b+='**玩家可选询问与现场行动**：\n\n'
  for key,label,mode,who,answer in s['choices']:
   b+=f'- `{q["id"]}-S{i}-{key}` 「{label}」：`{mode}`，'+actor(cast,who)+'回应「'+answer+'」。\n'
  b+='- 「先停在这里」：关闭会话，保已核事实，不代缺席者答应、不写resolve或paid。\n\n'
  b+='ask只获此人允许说的范围；inspect须实际完成对应安全观察且有权限，没看过不能抢先念核验答复。preview只展开已有方法条款，pause只关闭。以上都不提交解决方法、不把口头愿意写成款/人/物已到。\n\n'
 return b

def render_method(q,r,model):
 cast=model.get('dramatic_casts',{}).get(q['city'],model['dramatic_cast']);key=r['key']
 b='**本方法实际门槛**：'+q['dramatic_guards'][key]+'\n\n'
 b+='**执行与提交**：逐项列出已核事实、本人范围、真实可用钱/料/班次及未付欠项 → 单独预览代价 → 玩家二次确认 → 对应实际交接/安全处置发生后提交本案唯一方法。缺一项即保pending，不捏造到账。预览可退，已结案不显示重选。\n\n'
 b+='**实际完成后分角色回访**（人不在或死亡时停本人句；同意范围改变只影响未来）：\n\n'
 for who,words in q['dramatic_followups'][key]:b+=line(cast,who,words)
 return b

def render_exceptions(q,model):
 cast=model.get('dramatic_casts',{}).get(q['city'],model['dramatic_cast'])
 b='## 本案中断与到达顺序（'+q.get('dramatic_revision','S76')+'）\n\n'
 for key,title in [('dead','死亡'),('refusal','拒绝／缺席'),('before_city','先做本案'),('after_city','城市章已结后做')]:b+='**'+title+'**：'+q['dramatic_exceptions'][key]+'\n\n'
 b+='## 有限回执的具体回应（'+q.get('dramatic_revision','S76')+'）\n\n'
 b+='必须来源方法实际完成、有可核回执且本人允许本次转述；接收者存活/在场/准接收。死亡、拒绝、保密、缺席优先，未收回执不演对应台词，不倒推出其它家庭秘密。接受回执不发奖、不移库存、不替当事人新签。目标未结只调整以后可做的有限行动；已结仅演晚到回访，不重选resolve、不改paid、不退回伤害史或N17快照。\n\n'
 for f in q['dramatic_feedback']:
  b+='### '+f['effect']+'\n\n**本次可知**：'+f['known_fact']+'。\n\n**本案未结时**：'+f['early_action']+'\n\n'
  b+=line(cast,f['speaker'],f['early_line'])
  b+='**本案已结时，仅下一次回应**：\n\n'+line(cast,f['speaker'],f['late_line'])
 return b

def add_drama_links(relative,text,model):
 if model.get('dramatic_casts',{}).get('ASH') and model.get('dramatic_casts',{}).get('HIG'):
  q=next((q for q in model['quests'] if q['file']==relative),None)
  relevant=(q and q['city'] in ['ASH','HIG']) or any(c['id'] in ['ASH','HIG'] and c['file']==relative for c in model['cities']) or any(a['file']==relative for cid in ['ASH','HIG'] for a in model['dramatic_casts'][cid].values())
  if relevant:return text+'\n患者／陪护／地方水路与山地实测／停工／离任的当前逐角色稿见[[寒凉盆地与修院山地人物演出审查]]；S86是原创设计，照护非研究许可、校表非NE5、离任不回滚N17。\n'
 if model.get('dramatic_casts',{}).get('KOR') and model.get('dramatic_casts',{}).get('PAS'):
  q=next((q for q in model['quests'] if q['file']==relative),None)
  relevant=(q and q['city'] in ['KOR','PAS']) or any(c['id'] in ['KOR','PAS'] and c['file']==relative for c in model['cities']) or any(a['file']==relative for cid in ['KOR','PAS'] for a in model['dramatic_casts'][cid].values())
  if relevant:
   text+='\n寄存与关口两地的逐角色稿、缺席者／同人／原任务复用见[[考德与柏石关人物演出审查]]；S84为Mod原创初稿，未导入游戏。\n'
   if q and q['id']=='CS-PAS-03':text+='\n本封信与口信的私密文本、背包副件及交接规则见[[文书_PAS_列梵的家书与口信]]。\n'
   return text
 if model.get('dramatic_casts',{}).get('OSB') and model.get('dramatic_casts',{}).get('RAT'):
  q=next((q for q in model['quests'] if q['file']==relative),None)
  relevant=(q and q['city'] in ['OSB','RAT']) or any(c['id'] in ['OSB','RAT'] and c['file']==relative for c in model['cities']) or any(a['file']==relative for cid in ['OSB','RAT'] for a in model['dramatic_casts'][cid].values())
  if relevant:return text+'\n粮村与纪念地域的逐角色对白、两户女儿、现时护栏和有限给付见[[奥斯布鲁克与拉滕人物演出审查]]；S83为Mod原创初稿，未导入游戏。\n'
 if model.get('dramatic_casts',{}).get('EED') and model.get('dramatic_casts',{}).get('FOR'):
  q=next((q for q in model['quests'] if q['file']==relative),None)
  relevant=(q and q['city'] in ['EED','FOR']) or any(c['id'] in ['EED','FOR'] and c['file']==relative for c in model['cities']) or any(a['file']==relative for cid in ['EED','FOR'] for a in model['dramatic_casts'][cid].values())
  if relevant:return text+'\n林地与矿区的逐角色对白、有限料款与身体边界见[[伊德斯与佛尔霍特人物演出审查]]；S82为Mod原创初稿，未导入游戏。\n'
 if model.get('dramatic_casts',{}).get('DEN') and model.get('dramatic_casts',{}).get('MNS'):
  q=next((q for q in model['quests'] if q['file']==relative),None)
  relevant=(q and q['city'] in ['DEN','MNS']) or any(c['id'] in ['DEN','MNS'] and c['file']==relative for c in model['cities']) or any(a['file']==relative for cid in ['DEN','MNS'] for a in model['dramatic_casts'][cid].values())
  if relevant:return text+'\n丹布里与曼郡的逐角色对白、实际接收与来源交叉见[[丹布里与曼郡人物演出审查]]；S81为Mod原创初稿，未导入游戏。\n'
 for cid in ['SKO','YOS']:
  current=model.get('dramatic_casts',{}).get(cid,{})
  current_q=next((q for q in model['quests'] if q['file']==relative),None)
  if current and ((current_q and current_q['city']==cid) or any(c['id']==cid and c['file']==relative for c in model['cities']) or any(a['file']==relative for a in current.values())):
   return text+'\n当前冶炼／羊毛两地逐角色对白、共同采购人及实际去留见[[斯孔弗特与约斯特文人物演出审查]]；S80为原创初稿，不是已运行任务。\n'
 if model.get('dramatic_casts',{}).get('MAE'):
  mae_cast=model['dramatic_casts']['MAE'];mae_q=next((q for q in model['quests'] if q['file']==relative),None)
  if (mae_q and mae_q['city']=='MAE') or any(c['id']=='MAE' and c['file']==relative for c in model['cities']) or any(a['file']==relative for a in mae_cast.values()):
   return text+'\n当前曼恩逐角色对白、共用人物与先后顺序回应见[[曼恩人物对白与去留交叉审查]]；S79为原创台本初稿，未导入游戏。\n'
 if model.get('dramatic_casts',{}).get('ALD'):
  ald_cast=model['dramatic_casts']['ALD']
  ald_q=next((q for q in model['quests'] if q['file']==relative),None)
  if (ald_q and ald_q['city']=='ALD') or any(c['id']=='ALD' and c['file']==relative for c in model['cities']) or any(a['file']==relative for a in ald_cast.values()):
   return text+'\n当前奥尔德文逐角色对白、先后顺序回应与演出范围见[[奥尔德文人物对白与交叉演出审查]]；S78为原创台本初稿，未导入游戏。\n'
 if not model.get('dramatic_cast'):return text
 q=next((q for q in model['quests'] if q['file']==relative),None)
 relevant=(q is not None and 'dramatic_scenes' in q) or any(c['id']=='BRY' and c['file']==relative for c in model['cities'])
 relevant=relevant or any(a['file']==relative for a in model['dramatic_cast'].values())
 if relevant:text+='\n<!-- CITY-DRAMA-S76:BEGIN -->\n当前布林逐角色对白、条件回访、演员位置与未终审范围见[[布林人物对白与网状演出审查]]。S76为Mod原创台本，未导入游戏。\n<!-- CITY-DRAMA-S76:END -->\n'
 if relevant and (Path(__file__).resolve().parents[2]/'design/12_美术参考/布林任务场所概念与台本映射.md').exists():
  text+='\n六处场所的原素材参考图与逐任务用途见[[布林任务场所概念与台本映射]]；画板分格不是任务必访顺序。\n'
 return text
