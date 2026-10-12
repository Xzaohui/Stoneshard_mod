"""Normalize recorded visual reviews and advertise the saved S74 gallery."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'research/city-art-results.json';data=json.loads(p.read_text(encoding='utf-8'))
reviews={
'MNS':'已目视：葡架、苗地与酒窖构图可辨，主景和周边面板清楚；未核游戏尺度与碰撞。',
'ALD':'已目视v2：水岸与船改为干燥工艺料场，甲作、护理衬布和旅人侧院有区别；未核游戏碰撞。',
'MAE':'已目视v2：蓝色旗帜与阵营徽记移除，寒地残庭仍有人护理与生活；未核游戏碰撞。',
'SKO':'已目视：炉火、冷却沟与有限炭堆并置，周边住户与工场分开；未核产能或碰撞。'}
for r in data['records']:
 if r['id'] in reviews:r['review']=reviews[r['id']]
 r['review']=r['review'].replace('人工查看生成图','已目视生成图')
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=ROOT/'README.md';text=p.read_text(encoding='utf-8-sig')
start='<!-- CITY-ART-S74:BEGIN -->';end='<!-- CITY-ART-S74:END -->'
block=start+'\n2026-10-12：已保存15张参考原素材生成的像素概念板，包含33个周边聚落构图。入口 [原素材参考与城市概念图](design/12_美术参考/原素材参考与城市概念图.md)，图片见各城市/聚落笔记；原参考、完整提示词和版本哈希保存在research/city-art-*.json。全部仍是美术草稿，未新增游戏地图或更新游戏包。\n'+end+'\n'
if start in text:text=re.sub(re.escape(start)+'.*?'+re.escape(end)+r'\s*',lambda _:block,text,flags=re.S)
else:text=text.rstrip()+'\n\n'+block
p.write_text(text,encoding='utf-8')
print('Selected visual reviews and README S74 entry updated.')
