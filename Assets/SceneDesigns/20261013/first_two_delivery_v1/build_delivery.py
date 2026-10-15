from pathlib import Path
import json,hashlib,shutil,zipfile
from PIL import Image,ImageDraw,ImageFont
out=Path(__file__).resolve().parent;b=out.parent
sources=[b/'first_two/sq05_r02_well_pilot_v1',b/'sq08_r04_camp_pilot_v1']
raws=['raw/sq05_r02_well_raw_v2.png','raw_v2.png']
names=['01_渡民岸井_v2.png','02_退役营地避风棚_v2.png']
sha=lambda x:hashlib.sha256(x).hexdigest()
before={str(p):sha(p.read_bytes()) for s in sources for p in s.rglob('*') if p.is_file()}
for item in json.loads((sources[0]/'frozen_file_integrity.json').read_text()):assert sha((sources[0]/item['path']).read_bytes())==item['sha256']
for fn,h in json.loads((sources[1]/'SHA256SUMS.json').read_text()).items():assert sha((sources[1]/fn).read_bytes())==h
for s,r,n in zip(sources,raws,names):shutil.copy2(s/r,out/n)
board=Image.new('RGB',(1600,810),'#202723');d=ImageDraw.Draw(board);font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def t(x,y,txt,size=24,col='#e5e3d5'):d.text((x,y),txt,font=ImageFont.truetype(font,size,index=2),fill=col)
t(32,18,'新地点场景｜两张风格试稿',38);t(32,73,'粗簇简化候选 · 待用户审美选择 · 非游戏地图',24,'#b9c2b3')
for i,n in enumerate(names):
 im=Image.open(out/n).convert('RGB');assert im.size==(1536,1024);im=im.resize((768,512),Image.Resampling.NEAREST);board.paste(im,(24+i*784,132))
t(24,658,'渡民岸井  SQ05 / R02-well',27);t(808,658,'退役营地避风棚  SQ08 / R04-camp',27)
t(24,704,'三岸点、分柜与干岸回程',22,'#b9c2b3');t(808,704,'干燥会谈位、闭合小包与回程',22,'#b9c2b3')
t(24,757,'道具与地景颗粒仍有差异；不认证剧情结果或原生瓦片。两幅原图均为 1536 × 1024。',22,'#b9c2b3')
board.save(out/'03_两景联合浏览板_中文.png')
zip_reports=[]
for i,s in enumerate(sources):
 zpath=out/(f'0{i+4}_'+['渡民岸井','退役营地避风棚'][i]+'_完整源.zip')
 files=sorted(p for p in s.rglob('*') if p.is_file())
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in files:z.write(p,s.name+'/'+str(p.relative_to(s)))
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None;expected={s.name+'/'+str(p.relative_to(s)) for p in files};assert set(z.namelist())==expected
  members=[]
  for p in files:
   n=s.name+'/'+str(p.relative_to(s));h=sha(z.read(n));assert h==before[str(p)];members.append({'member':n,'bytes':p.stat().st_size,'sha256':h})
 zip_reports.append({'path':zpath.name,'member_count':len(files),'all_member_sha_match':True,'missing_or_extra_members':[],'members':members})
originals=json.loads((b/'first_two_scene_pilot_sources.json').read_text())['public_visual_sources'];orig_sha={x['sha256'] for x in originals}
assert not orig_sha.intersection(before.values())
after={str(p):sha(p.read_bytes()) for s in sources for p in s.rglob('*') if p.is_file()};assert before==after
attachments=[]
for p in sorted(out.iterdir()):
 if p.suffix in ['.png','.zip']:
  assert p.stat().st_size<18*1024*1024;item={'path':p.name,'bytes':p.stat().st_size,'mib':round(p.stat().st_size/1024/1024,3),'sha256':sha(p.read_bytes())}
  if p.suffix=='.png':item['dimensions']=list(Image.open(p).size)
  attachments.append(item)
assert len(attachments)==5
(out/'delivery.json').write_text(json.dumps({'status':'prepared_not_uploaded','selected_version':'v2 for both scenes','user_aesthetic_approved':False,'native_pixel_style_accepted':False,'runtime_verified':False,'sources':[str(s.relative_to(b)) for s in sources],'attachments':attachments,'notes':['Two raw selected PNGs are byte-identical source copies.','Chinese board uses proportional 50% nearest-neighbour copies only.','Source ZIPs contain every frozen author file, including historical v1 materials.','SQ08 historical presentation_zh.png is v1; selected presentation is presentation_v2_zh.png, per FINAL_STATUS.','No original game screenshots are included.']},ensure_ascii=False,indent=2))
(out/'FINAL_DELIVERY_QA.json').write_text(json.dumps({'status':'awaiting_actual_board_view','attachment_count':5,'all_under_18_mib':True,'source_frozen_hashes_verified':True,'source_directories_unchanged':before==after,'original_screenshot_sha_absent':True,'selected_pngs_byte_identical':True,'all_zip_members_verified':True,'zips':zip_reports,'board':'03_两景联合浏览板_中文.png','board_actual_viewed':False,'upload_performed':False,'git_uploaded':False},ensure_ascii=False,indent=2))
print(json.dumps(attachments,ensure_ascii=False,indent=2))
