from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,numpy as np
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); B=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/first_four_production_brief.json'; brief=json.loads(B.read_text()); sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for slug,v,name in [('anni',2,'安妮'),('gura',1,'古菈')]:
 c=next(c for c in brief['characters'] if c['production_brief']['working_slug']==slug); out=R/c['recommended_output_directory']; sources=out/'sources';sources.mkdir(exist_ok=True)
 paths=[c['current_card']['path'],c['fine_details_source']['path'],brief['style']['style_source']['path'],'Assets/CharacterDesigns/20261013/expressive/reference/pixel-asset-master/SKILL.md','Assets/CharacterDesigns/20261013/expressive/reference/STRUCTURE_GUIDED_REDRAW_METHOD.md']
 for link in c['story_links']:
  paths += [str(p.relative_to(R)) for p in (R/'design').rglob(link+'.md')]
 records=[]
 for i,path in enumerate(dict.fromkeys(paths)):
  p=R/path; dest=sources/(f'{i:02d}_'+p.name);shutil.copyfile(p,dest);records.append({'source':path,'snapshot':str(dest.relative_to(out)),'sha256':sha(p)})
 for expected in [c['current_card'],c['fine_details_source'],brief['style']['style_source']]: assert sha(R/expected['path'])==expected['sha256'],expected
 shutil.copyfile(B,sources/'production_brief.json');records.append({'source':str(B.relative_to(R)),'snapshot':'sources/production_brief.json','sha256':sha(B)})
 refs=[]
 for r in brief['style']['references']:
  assert sha(R/r['path'])==r['sha256'];refs.append(r)
 (out/'source_index.json').write_text(json.dumps({'head':brief['snapshot_head'],'sources':records,'viewed_style_references':refs,'reference_use':brief['style']['reference_use']},ensure_ascii=False,indent=2))
 raw=out/f'{slug}_v{v}_raw_imagegen.png';final=out/f'{slug}_transparent.png';src=Image.open(raw).convert('RGBA'); arr=np.array(src); mask=arr[:,:,3]<=8; arr[mask]=0; Image.fromarray(arr).save(final)
 im=Image.open(final).convert('RGBA');a=np.array(im.getchannel('A'));alpha={'mode':im.mode,'size':im.size,'alpha_zero':int((a==0).sum()),'alpha_partial':int(((a>0)&(a<255)).sum()),'alpha_255':int((a==255).sum()),'bbox_alpha_nonzero':im.getbbox(),'operation':'Only RGBA pixels with source alpha <= 8 cleared to zero; alpha > 8 pixels preserved exactly. No crop, stretch, quantize or recolor.', 'cleared_pixel_count':int(mask.sum())}
 (out/'alpha_report.json').write_text(json.dumps(alpha,indent=2))
 font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',32);small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',22)
 for theme,bg,fg in [('light',(237,233,222),(39,40,38)),('dark',(34,39,44),(237,233,221))]:
  board=Image.new('RGB',(1600,1150),bg); d=ImageDraw.Draw(board);d.text((55,32),name+'｜新增剧情人物概念',font=font,fill=fg);d.text((55,82),c['canonical_id']+'  ·  '+c['story_role'],font=small,fill=fg)
  n=im.copy();n.thumbnail((980,950),Image.Resampling.NEAREST);board.paste(n,((1060-n.width)//2,160+(940-n.height)//2),n)
  lines=['外观概念 · 终审见 QA',c['production_brief']['age'],'服色及未定发型为可逆提案','仅展示本人现有随身物','无可读姓名、签名或完成回执','原始生成像素与透明通道保留','装备兼容与游戏运行：未知']
  for k,line in enumerate(lines):d.text((1040,240+65*k),line,font=small,fill=fg)
  d.text((55,1100),'只作人物外观概念；不代表剧情结算、未来承诺或原版资源验证。',font=small,fill=fg);board.save(out/f'{slug}_展示_{theme}.png')
 shutil.copyfile('/tmp/package_anni_gura.py',out/'export_assets.py')
 print(slug,sha(raw),sha(final))
