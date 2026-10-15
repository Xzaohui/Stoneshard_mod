from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,hashlib,zipfile,shutil,datetime
D=Path(__file__).resolve().parent;B=D.parent
items=[('turi','图里','turi_A2_turn_angle_gauge','近身托起量角器转看'),('cuoer','锉珥','cuoer_A2_crouch_tap_rail','屈膝闭钳轻敲轨顶')]
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',28);small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',23);title=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',36)
board=Image.new('RGBA',(1800,2050),(239,235,222,255))
for i,(slug,zh,key,label) in enumerate(items):
 p=B/slug/'noncombat_basics_v1';dst=p/'selected'/f'{key}_transparent.png';shutil.copy2(dst,D/'delivery'/dst.name)
 for col,(bg,fg) in enumerate([((239,235,222,255),(30,30,30,255)),((37,43,49,255),(240,240,240,255))]):
  panel=Image.new('RGBA',(900,970),bg);dr=ImageDraw.Draw(panel);dr.text((30,20),f'{zh} · {label}',font=font,fill=fg)
  im=Image.open(dst).convert('RGBA');im=im.crop(im.getbbox());im.thumbnail((820,830),Image.Resampling.NEAREST);panel.alpha_composite(im,((900-im.width)//2,95+(830-im.height)//2));board.alpha_composite(panel,(900*col,100+970*i))
draw=ImageDraw.Draw(board);draw.text((30,14),'图里与锉珥 · 非战斗独立关键姿态 · 浅深对照',font=title,fill=(25,25,25));draw.text((30,61),'仅A2两张通过；两项A1未通过，完整首稿/修订归档保留。非连续动画，未游戏验证。',font=small,fill=(45,45,45));board.convert('RGB').save(D/'delivery/图里_锉珥_非战斗独立动作_浅深对照.png')
files=[]
# Two ordinary ZIP archives partition both complete source trees. Extract both to one directory.
import zlib
entries=[]
for slug,_,_,_ in items:
 p=B/slug/'noncombat_basics_v1'
 for f in sorted(p.rglob('*')):
  if f.is_file():
   data=f.read_bytes();entries.append({'source':f,'path':str(Path(slug)/'noncombat_basics_v1'/f.relative_to(p)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'estimate':len(zlib.compress(data,9))})
parts=[[],[]];sizes=[0,0]
for e in sorted(entries,key=lambda e:-e['estimate']):
 i=0 if sizes[0]<=sizes[1] else 1;parts[i].append(e);sizes[i]+=e['estimate']
index={'instructions':'将 part1of2 和 part2of2 两个普通ZIP解压到同一目录；两包合起来恢复图里与锉珥的完整冻结源树。单包不完整，不是分卷压缩，不删任何raw/失败候选/原始返回。','parts':[]}
for i,part in enumerate(parts):
 index['parts'].append({'archive':f'turi_cuoer_full_sources_part{i+1}of2.zip','files':[{k:v for k,v in e.items() if k not in ['source','estimate']} for e in sorted(part,key=lambda e:e['path'])]})
ib=(json.dumps(index,ensure_ascii=False,indent=2)+'\n').encode();(D/'FULL_SOURCE_INDEX.json').write_bytes(ib)
for i,part in enumerate(parts):
 z=D/'delivery'/f'turi_cuoer_full_sources_part{i+1}of2.zip'
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,9) as zz:
  zz.writestr('FULL_SOURCE_INDEX.json',ib)
  zz.writestr('解压说明.txt',index['instructions'])
  for e in sorted(part,key=lambda e:e['path']):zz.write(e['source'],e['path'])
 assert z.stat().st_size<18*1024*1024,z
 with zipfile.ZipFile(z) as zz:
  assert zz.testzip() is None
  for e in part:assert hashlib.sha256(zz.read(e['path'])).hexdigest()==e['sha256'],e['path']
for p in sorted((D/'delivery').iterdir()):
 files.append({'filename':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'native_attachment_intended':True})
manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'planned_actions':4,'accepted_actions':2,'failed_actions':2,'attachments':files,'attachment_count':len(files),'expected_original_seven_not_met':'Only two accepted actions. No failed image sent as an accepted PNG. Two PNG + one board + two full-source ZIP = five files.','runtime_verified':False,'animation':False}
(D/'delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
