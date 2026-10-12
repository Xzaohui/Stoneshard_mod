"""Shared city-scope backlink block for older screenplay notes."""
from pathlib import Path
import json,re
def add_city_links(root,relative,text):
 p=root/'research/city-campaign.json'
 if not p.exists():return text
 m=json.loads(p.read_text(encoding='utf-8'));stem=Path(relative).stem;body=None
 if stem in ['任务台本总索引','新区域设计与任务总表']:
  body='本页保留S61/S62晶石主线及旧六区连接场景；完整城市范围入口为[[城市与聚落设计总索引]]，双向影响见[[城市篇章与跨区域任务网]]。旧六区54节点不再代表完整世界；新增CM/CS仍为纸面初稿。'
 elif stem.startswith('台本_'):
  qid=stem.split('_')[1]
  if qid in m['legacy_home']:
   bc={c['id']:c for c in m['cities']};bq={q['id']:q for q in m['quests']}
   links=['[['+Path(bc[c]['file']).stem+']]' for c in m['legacy_home'][qid]];targets=[]
   for e in m['effects']:
    other=e['target'] if e['source']==qid else e['source'] if e['target']==qid else None
    if other in bq and other not in targets:targets.append(other)
   relation='接入篇章：'
   if not targets:
    targets=[bc[c]['main_id'] for c in m['legacy_home'][qid]];relation='关联地域章（无直接回执边，不自动读旧案状态）：'
   body='城市／地域：'+' · '.join(links)+'。'+relation+' · '.join('[['+Path(bq[q]['file']).stem+']]' for q in targets)+'。\n\n本任务仍拥有NE、唯一奖和paid；城市章不能代领奖、假定本人授权或重开N17。有限回执与先后顺序见[[城市篇章与跨区域任务网]]。'
 if body is None:return text
 start='<!-- CITY-TASK-S63:BEGIN -->';end='<!-- CITY-TASK-S63:END -->';block=start+'\n## S63城市接入与所有权\n\n'+body+'\n'+end+'\n\n'
 if start in text:return re.sub(re.escape(start)+'.*?'+re.escape(end)+r'\s*',lambda _:block,text,flags=re.S)
 return re.sub(r'(?m)^(# [^\n]+\n)',lambda x:x.group(1)+'\n'+block,text,count=1)
