from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,zipfile,base64
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
deliv=Path(__file__).resolve().parent
brief=json.loads((root/'Assets/EnemyDesigns/20261013/second_six/action_continuation_brief_v1.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',21)
small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',17)
board=Image.new('RGB',(1320,1870),(226,222,211));draw=ImageDraw.Draw(board)
draw.text((22,15),'敌人动作续绘 007–008｜相邻关键阶段 · 浅底 / 深底',font=font,fill='#22262b')
draw.text((22,52),'单张关键阶段概念；不代表连续动画、锚点、碰撞、装备绑定或游戏运行通过。',font=small,fill='#33373b')
attachments=[];checks=[]
labels=[['母图','旧：举盾稳守','旧：收盾提斧','新：短斧前送斜劈'],['母图','旧：平弩瞄准','旧：低位持弩','新：低姿撤步换重心']]
for i,item in enumerate(brief['items'][:2]):
 p=root/item['planned_output_directory'];final=json.loads((p/'FINAL_STATUS.json').read_text());manifest=json.loads((p/'manifest.json').read_text())
 assert sha(p/'manifest.json')==final['manifest_sha256']
 for f,s in manifest['files'].items():assert sha(p/f)==s,(p/f,'manifest mismatch')
 snap=json.loads((p/'source_snapshot.json').read_text())
 for f in snap['files']:
  assert sha(p/f['snapshot_path'])==f['sha256']
  assert sha(root/f['source_path'])==f['sha256'],('source changed',f['source_path'])
 for ap in sorted((p/'calls').glob('arguments_v*.json')):
  v=ap.stem.split('_')[-1];args=json.loads(ap.read_text());assert args['prompt']==(p/'calls'/f'prompt_{v}.txt').read_text()
  ret=json.loads((p/'calls'/f'tool_return_{v}.json').read_text());raw=p/'raw'/f'{item["slug"]}_{item["pose_id"]}_{v}_raw_imagegen.png'
  assert hashlib.sha256(base64.b64decode(ret['image_url'].split(',',1)[1])).hexdigest()==sha(raw)
 if final['selected']:
  src=p/final['selected_file'];assert sha(src)==final['selected_sha256']
  dst=deliv/f'{7+i:03d}_{item["pose_id"]}_selected.png';shutil.copy2(src,dst);attachments.append(dst)
 else:src=None
 zy=95+i*870;draw.text((22,zy),f'{7+i:03d} {item["working_name"]} · '+('已正选' if src else '未正选，需复核'),font=font,fill='#22262b')
 refs=[root/r['source_path'] for r in item['source_images']]+([src] if src else [])
 for row,bg in enumerate([(239,233,219,255),(29,33,37,255)]):
  for j,zp in enumerate(refs):
   x=10+j*325;y=zy+38+row*395;draw.rectangle((x,y,x+320,y+386),fill=bg[:3])
   z=Image.open(zp).convert('RGBA');s=min(299/z.width,333/z.height);z=z.resize((round(z.width*s),round(z.height*s)),Image.Resampling.NEAREST)
   panel=Image.new('RGBA',z.size,bg);panel.alpha_composite(z);board.paste(panel.convert('RGB'),(x+(320-z.width)//2,y+43))
   draw.text((x+9,y+9),labels[i][j],font=small,fill=('#24282b' if row==0 else '#e8e4dd'))
 note='肩胸前送、肘展开，左前脚接重；短斧、圆盾与身体保持分离。' if i==0 else '髋后坐、右后腿接重、左前脚卸重；双手仍前托后握，未画装填。'
 if not src:note='首稿与一次硬错修订均保留于源包；本项未选为完成稿。'
 draw.text((22,zy+834),note,font=small,fill='#34383b')
 archive=deliv/f'{7+i:03d}_{item["pose_id"]}_complete_sources.zip'
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for f in sorted(p.rglob('*')):
   if f.is_file():z.write(f,f.relative_to(p))
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  expected={str(f.relative_to(p)) for f in p.rglob('*') if f.is_file()};assert set(z.namelist())==expected
  for name in expected:assert hashlib.sha256(z.read(name)).hexdigest()==sha(p/name)
 assert archive.stat().st_size<18*1024*1024
 attachments.append(archive)
 checks.append({'id':item['concept_id'],'status':final['status'],'selected':final['selected'],'selected_sha256':final.get('selected_sha256'),'input_sources_unchanged':True,'all_manifest_hashes_verified':len(manifest['files']),'complete_source_archive_files':len(expected),'archive_under_18MiB':True,'all_archived_bytes_match':True})
draw.text((22,1844),'真实RGBA浅深合成；等比最近邻排板，旧图未改。隐藏RGB不作为可见缺陷。',font=small,fill='#34383b')
boardpath=deliv/'007_008_adjacent_key_stages_light_dark.png';board.save(boardpath);attachments.append(boardpath)
for p in attachments: assert p.stat().st_size<18*1024*1024
records=[{'name':p.name,'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in attachments]
(deliv/'delivery_manifest.json').write_text(json.dumps({'attachments':records,'attachment_count':len(records),'checks':checks,'runtimeVerified':False,'continuous_animation_verified':False,'old_sources_changed':False},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'attachments':records,'checks':checks},ensure_ascii=False,indent=2))
