from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,shutil,zipfile,datetime
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');N=R/'Assets/CharacterActions/20261013/new_story';out=N/'first_noncombat_anni_gura_delivery_v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not out.exists(), 'Do not overwrite an existing delivery'
roots=[N/s/'noncombat_basics_v1' for s in ['anni','gura']]
for root in roots:
 assert (root/'FINAL_STATUS.json').is_file(), 'Wait for sole-writer freeze'
out.mkdir();(out/'delivery').mkdir();D=out/'delivery';copied=[];imgs=[];labels=[]
for root in roots:
 m=json.loads((root/'manifest.json').read_text())
 for a in m['artifacts']:
  p=root/a['selected'];assert sha(p)==a['selected_sha256'];dst=D/p.name;shutil.copyfile(p,dst);imgs.append(Image.open(dst));labels.append(('安妮' if m['slug']=='anni' else '古菈')+' · '+a['title_zh']);copied.append({'path':str(dst.relative_to(out)),'source':str(p.relative_to(R)),'sha256':sha(dst),'bytes':dst.stat().st_size})
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',38);small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',25)
board=Image.new('RGB',(2600,2260));d=ImageDraw.Draw(board)
for row,(bg,fg,theme) in enumerate([((237,233,222),(36,37,35),'浅底'),((31,36,42),(237,233,222),'深底')]):
 y0=row*1130;d.rectangle((0,y0,2600,y0+1130),fill=bg);d.text((38,y0+20),'安妮与古菈｜四个独立职业动作 · '+theme,font=font,fill=fg);d.text((38,y0+78),'扣袖带、合簿、折短单、收稳短撬棍；各图独立，不代表连续动画或剧情先后。',font=small,fill=fg)
 for i,(im,label) in enumerate(zip(imgs,labels)):
  n=im.copy();n.thumbnail((600,920),Image.Resampling.NEAREST);board.paste(n,(i*650+(650-n.width)//2,y0+160+(920-n.height)//2),n);d.text((i*650+32,y0+124),label,font=small,fill=fg)
 d.text((38,y0+1088),'本人自有物件的整理提案；不表示交接、续约、付款、治疗、任务完成或游戏已实现。',font=small,fill=fg)
bp=D/'安妮_古菈_独立职业动作_浅深对照.png';board.save(bp);copied.append({'path':str(bp.relative_to(out)),'sha256':sha(bp),'bytes':bp.stat().st_size,'role':'Chinese light/dark board; unmodified selected subject pixels, nearest-neighbor layout only'})
zip_checks=[]
for root in roots:
 slug=root.parent.name;zp=D/f'{slug}_noncombat_basics_v1_full_source.zip';files=sorted(p for p in root.rglob('*') if p.is_file());before={str(p.relative_to(root)):sha(p) for p in files}
 with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in files:z.write(p,str(Path(slug+'_noncombat_basics_v1')/p.relative_to(root)))
 assert zp.stat().st_size<18*1024*1024
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  archive={str(Path(x).relative_to(slug+'_noncombat_basics_v1')):hashlib.sha256(z.read(x)).hexdigest() for x in z.namelist()}
 assert before==archive
 for p in files:assert sha(p)==before[str(p.relative_to(root))]
 rec={'path':str(zp.relative_to(out)),'sha256':sha(zp),'bytes':zp.stat().st_size,'members':len(files),'all_members_sha256_verified':True,'archive_matches_frozen_source_tree':True,'member_sha256':before};zip_checks.append(rec);copied.append({k:rec[k] for k in ['path','sha256','bytes','members']})
qa={'status':'packaged_pending_visual_delivery_review','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'attachment_count':7,'art_png_count':4,'board_count':1,'full_source_zip_count':2,'zip_limit_bytes':18*1024*1024,'files':copied,'zip_validation':zip_checks,'source_frozen_checks':[{'path':str(root.relative_to(R)),'manifest_sha256':sha(root/'manifest.json'),'FINAL_STATUS_sha256':sha(root/'FINAL_STATUS.json')} for root in roots],'not_performed':['upload','git','engine deployment'],'animation_claim':False}
(out/'FINAL_DELIVERY_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));(out/'delivery_manifest.json').write_text(json.dumps({'status':qa['status'],'files':copied},ensure_ascii=False,indent=2));(out/'README.md').write_text('# 安妮与古菈｜独立职业动作\n\n交付7件：4张原生透明PNG、1张中文浅深对照板、2个单人完整来源ZIP。PNG为所选生图逐字节副本；浅深板仅透明合成与统一最近邻展示。\n\n这是4个彼此独立的动作概念，不是连续动画，也不表示剧情交接、续约、付款、治疗、任务结算或游戏落地。安妮扣袖带首稿左右手反向，已在唯一返修中修正，首稿完整保留。古菈收工具图中的短单藏在原有肩袋内，未增加夹层。\n\n作者与独审记录、完整提示词、工具参数与真实返回摘要、原稿及版本选择、来源SHA和终态在各全源ZIP内；全成员哈希已经与冻结作者目录逐一比对。未上传，未执行git。\n');shutil.copyfile(__file__,out/'package_delivery.py');print(json.dumps({'delivery_root':str(out),'attachments':copied},ensure_ascii=False,indent=2))
