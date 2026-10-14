from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,zipfile,shutil,datetime,zlib
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');B=R/'Assets/CharacterDesigns/20261013/expressive/new_story';O=B/'ninth_four_expressions_teman_nier_delivery_v1';assert not O.exists();O.mkdir();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();slugs=['teman','fx_cv4_nier'];characters=[];assets=[];sourcefreezes={}
for slug in slugs:
 D=B/slug/'expressions_v1';m=json.loads((D/'manifest.json').read_text());f=json.loads((D/'FINAL_STATUS.json').read_text());assert m['status']==f['status']=='final_frozen_independent_pass';assert sha(D/'manifest.json')==f['manifest']['sha256']
 for entry in m['files']:assert sha(D/entry['path'])==entry['sha256']
 whole={str(p.relative_to(D)):sha(p) for p in sorted(D.rglob('*')) if p.is_file()};sourcefreezes[slug]={'path':str(D.relative_to(R)),'manifest_sha256':sha(D/'manifest.json'),'FINAL_STATUS_sha256':sha(D/'FINAL_STATUS.json'),'files':whole};c=json.loads((D/'sources/character_brief.json').read_text());characters.append(c)
 for s in m['selected']:
  src=D/s['selected'];assert sha(src)==s['selected_sha256'];dst=O/src.name;shutil.copy2(src,dst);assets.append({'slug':slug,'name':c['name'],'expression':s['expression'],'label_zh':s['label_zh'],'source':str(src.relative_to(R)),'path':dst.name,'sha256':sha(dst),'bytes':dst.stat().st_size})
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';title=ImageFont.truetype(font,40);label=ImageFont.truetype(font,28);small=ImageFont.truetype(font,22);W,H=2600,2300;rowH=1150;board=Image.new('RGBA',(W,H));themes=[('浅色',(242,237,227,255),(54,47,38,255)),('深色',(32,36,41,255),(234,224,203,255))]
for row,(theme,bg,fg) in enumerate(themes):
 panel=Image.new('RGBA',(W,rowH),bg);d=ImageDraw.Draw(panel);d.text((55,24),'忒曼 · 佴珥｜四种表情 · '+theme+'对照',font=title,fill=fg)
 for i,a in enumerate(assets):
  d.text((55+i*650,86),a['name']+' · '+a['label_zh'],font=label,fill=fg);im=Image.open(O/a['path']).convert('RGBA');sc=min(590/im.width,910/im.height);im=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.NEAREST);panel.alpha_composite(im,(30+i*650+(590-im.width)//2,132+(910-im.height)//2))
 d.text((55,1085),'可逆表情概念；未表示任务结案、付款、授权或关系变化。',font=small,fill=fg);board.alpha_composite(panel,(0,row*rowH))
boardpath=O/'忒曼_佴珥_四种表情_浅深对照.png';board.convert('RGB').save(boardpath)
(O/'交付说明.md').write_text('# 忒曼与佴珥：四种表情概念\n\n忒曼 FX-HNY：说蜂会笑、亡巢敛笑。佴珥 FX-CV4：受夸推辞、凝神守望。\n\n四张透明PNG为已独审的完整原图逐字节副本；浅深对照板仅等比例展示。原图可能包含alpha0隐藏RGB，透明显示须按alpha合成，不能据隐藏RGB判断背景。\n\n请同时下载两份普通ZIP并解压到同一目录：第1包保留忒曼expressions_v1全部文件，第2包保留佴珥expressions_v1全部文件及两人的共享独审证据。两包合起来是完整源集，保留同一层级，无同名覆盖冲突。包含全部raw、prompt、实际调用参数、完整工具返回、母图/卡/台本快照、作者/独立QA、冻结manifest与FINAL_STATUS。无删减、无身体压缩或脚本改脸。\n\n两人各两张独立可逆表情，不代表剧情结果、任务完成、付款、受托、同意、康复或关系变化。只为美术概念，不证明原生像素网格、装备兼容、连续动画或游戏运行。\n')
archives=[];inventories=[];audit=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_expression_independent_details'
mapping={}
for c in characters:
 slug=c['slug'];D=B/slug/'expressions_v1'
 for p in sorted(D.rglob('*')):
  if p.is_file():mapping[f'{slug}/expressions_v1/{p.relative_to(D)}']=p
 for p in sorted(audit.glob(slug+'_*')):
  if p.is_file():mapping['independent_evidence/'+p.name]=p
mapping['independent_evidence/baseline_source_verification.json']=audit/'baseline_source_verification.json'
mapping['交付说明.md']=O/'交付说明.md'
# Two regular ZIPs, preserving each complete character directory together.
# The first holds the full Teman source tree; the second holds the full FX-CV4 Nier tree and all shared independent evidence.
parts=[{},{}]
for arc,p in mapping.items():parts[0 if arc.startswith('teman/') else 1][arc]=p
for idx,part in enumerate(parts,1):
 zp=O/f'忒曼佴珥_完整源集_第{idx}包共2包.zip'
 with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for arc,p in part.items():z.write(p,arc)
 assert zp.stat().st_size<18*1024*1024,(zp,zp.stat().st_size)
 entries=[]
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None;assert set(z.namelist())==set(part)
  for i in z.infolist():
   b=z.read(i.filename);assert hashlib.sha256(b).hexdigest()==sha(part[i.filename]);assert zlib.crc32(b)&0xffffffff==i.CRC;entries.append({'path':i.filename,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'crc32':format(i.CRC,'08x')})
 archives.append({'path':zp.name,'sha256':sha(zp),'bytes':zp.stat().st_size,'members':len(entries),'full_source_set_part':idx,'full_source_set_parts':2,'source_complete_across_two_archives':True,'crc_pass':True,'all_members_sha256_pass':True});inventories.append({'archive':zp.name,'files':entries})
assert set(parts[0]).isdisjoint(set(parts[1])) and set(parts[0])|set(parts[1])==set(mapping)
for slug,f in sourcefreezes.items():
 D=R/f['path'];after={str(p.relative_to(D)):sha(p) for p in sorted(D.rglob('*')) if p.is_file()};assert after==f['files']
attachments=[{k:a[k] for k in ['path','sha256','bytes']} for a in assets]+[{'path':boardpath.name,'sha256':sha(boardpath),'bytes':boardpath.stat().st_size}]+archives;assert len(attachments)==7
(O/'archive_inventory.json').write_text(json.dumps(inventories,ensure_ascii=False,indent=2)+'\n');delivery={'schema_version':1,'status':'packaged_pending_combined_board_visual_review','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'attachment_count':7,'attachments':attachments,'assets':assets,'source_freezes':sourcefreezes,'source_files_unchanged_after_packaging':True,'full_source_tree_inventories_include_nested_manifest_snapshots':True,'zip_integrity':'All members SHA256 and CRC32 verified; testzip passed','not_uploaded':True,'not_committed':True,'not_claimed':['用户已认可','游戏原生网格','装备兼容','动画连续性','runtime通过']};(O/'delivery.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n');shutil.copy2(__file__,O/'package_delivery.py');print(json.dumps({'output':str(O.relative_to(R)),'attachments':attachments},ensure_ascii=False,indent=2))
