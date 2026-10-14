from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path.cwd();P=R/'Assets/CharacterActions/20261013/new_story';D=P/'eleventh_noncombat_weier_ink_moer_delivery_v1';b=json.loads((D/'planning_sources/eleventh_new_character_actions_brief.json').read_text()); cs=[c for c in b['characters'] if c['slug'] in ['weier_ink','moer']]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; F=lambda n:ImageFont.truetype(font,n)
layout={'canvas':[1800,1840],'method':'Complete source canvases, uniform nominal scale 0.5, nearest-neighbor; integer dimensions rounded only. No crop, body stretch, redraw, or anatomy edits.','placements':[],'backgrounds':{'light':[242,236,220,255],'dark':[31,36,44,255]}}
for i,c in enumerate(cs):
 imgs=[(R/c['mother_image']['transparent'],'已审母图（参考）')]+[(R/c['proposed_output_directory']/'selected'/f'{p["key"]}.png',f'A{j+1} {p["title_zh"]}') for j,p in enumerate(c['plans'])]
 for k,(path,label) in enumerate(imgs):
  im=Image.open(path);size=[round(im.width*.5),round(im.height*.5)];xy=[k*600+(600-size[0])//2,178+i*800]
  layout['placements'].append({'source':str(path.relative_to(R)),'source_sha256':sha(path),'source_dimensions':list(im.size),'size':size,'xy':xy,'label':label,'character':c['slug'],'uniform_nominal_scale':0.5})
for mode,bg in layout['backgrounds'].items():
 out=Image.new('RGBA',layout['canvas'],tuple(bg));dr=ImageDraw.Draw(out);fg=(42,39,35,255) if mode=='light' else (239,234,222,255)
 dr.text((40,22),'韦珥 · 摩珥｜基础动作与母图对照',fill=fg,font=F(46))
 dr.text((40,88),'四张独立非战斗关键姿态；完整单人全身、原物件与真实透明背景',fill=fg,font=F(27))
 for i,c in enumerate(cs):
  dr.text((40,135+i*800),f'{c["name"]}  {c["canonical_id"]}',fill=fg,font=F(28))
 for q in layout['placements']:
  dr.text((q['xy'][0]+10,q['xy'][1]-5),q['label'],fill=fg,font=F(25))
  out.alpha_composite(Image.open(R/q['source']).convert('RGBA').resize(q['size'],Image.Resampling.NEAREST),tuple([q['xy'][0],q['xy'][1]+40]))
  q['composite_xy']=[q['xy'][0],q['xy'][1]+40]
 dr.text((40,1780),'静态美术提案；不代表剧情结果、连续动画、装备兼容或游戏运行验收。',fill=fg,font=F(27))
 out.convert('RGB').save(D/f'weier_ink_moer_mother_actions_{mode}.png')
# xy denotes actual composite origin; label origin retained separately.
for q in layout['placements']:q['label_xy']=[q['xy'][0]+10,q['xy'][1]-5];q['xy']=q.pop('composite_xy')
(D/'board_layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n')
print('Built light/dark comparison boards and complete placement metadata.')
