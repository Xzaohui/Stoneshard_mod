"""Embed selected reference-based concepts in city and satellite authoring output."""
from pathlib import Path
import json,re,os
def _add_city_overview_art(root,relative,text):
 mp=root/'research/city-art-manifest.json'
 if not mp.exists():return text
 m=json.loads(mp.read_text(encoding='utf-8'));key='design/'+relative
 for r in m.get('reference_based_boards',[]):
  if key!=r['city_note'] and key not in r['satellite_notes']:continue
  rel=Path(os.path.relpath(root/r['output'],(root/key).parent)).as_posix()
  sid=Path(relative).stem.split('_')[1] if key in r['satellite_notes'] else None
  body=f"![{r['id']}参考式像素概念板]({rel})\n\n"
  body+=(f'本聚落对应下方 `{sid}` 面板；整板上方是所属城市／地域，不能当本镇规模。' if sid else '上方是代表性核心街区，下方按卫星ID排列周边构图；不是整座城市总平面。')
  body+=' 以用户原素材的材质、轮廓和相机为参考生成；人物、场景组合、灯光/季节属于Mod美术提案，不证明原作地理和阵营。来源、任务对应和制作限制见[[原素材参考与城市概念图]]。'
  start='<!-- CITY-ART-S74:BEGIN -->';end='<!-- CITY-ART-S74:END -->';block=start+'\n## 原素材参考概念（S74）\n\n'+body+'\n'+end+'\n'
  if start in text:return re.sub(re.escape(start)+'.*?'+re.escape(end)+r'\s*',lambda _:block,text,flags=re.S)
  return text.rstrip()+'\n\n'+block
 return text

def add_city_art(root,relative,text):
 from TaskArtLinks import add_task_art
 return add_task_art(root,relative,_add_city_overview_art(root,relative,text))
