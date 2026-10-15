from PIL import Image,ImageDraw,ImageFont
import pathlib,json,hashlib,shutil,datetime,numpy as np
R=pathlib.Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=R/'Assets/CharacterDesigns/20261013/expressive/new_story'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
if not pathlib.Path(font).exists():font='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
f=ImageFont.truetype(font,32);small=ImageFont.truetype(font,24)
for slug,name,cid,detail in [('lier','栎珥','FX-CV5','五十来岁拾柴人｜双旧绳肩搭｜裤脚麻绳'),('huier','洄珥','FX-CV6','二十多岁谷地行者｜草绳裹靴｜背负探路杆')]:
 o=base/slug/'concept_v1';raw=o/f'{slug}_raw_imagegen.png';im=Image.open(raw).convert('RGBA');a=np.array(im);before=a.copy();low=a[:,:,3]<=8; a[low]=0; out=Image.fromarray(a);out.save(o/f'{slug}_transparent.png')
 stats={'raw_size':list(im.size),'raw_mode':im.mode,'raw_alpha_zero':int((before[:,:,3]==0).sum()),'raw_alpha_1_to_8':int(((before[:,:,3]>0)&(before[:,:,3]<=8)).sum()),'raw_alpha_9_to_254':int(((before[:,:,3]>8)&(before[:,:,3]<255)).sum()),'raw_alpha_255':int((before[:,:,3]==255).sum()),'hidden_rgb_pixels_before':int(((before[:,:,3]==0)&(before[:,:,:3].max(axis=2)>0)).sum()),'visible_pixels_above_8_unchanged':bool(np.array_equal(a[~low],before[~low])),'cleanup':'Only alpha <= 8 zeroed RGBA, hidden RGB cleared. No repaint, no palette quantization, no resizing character.','alpha_bbox':out.getbbox()}
 (o/'technical_qa.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
 w,h=im.size;board=Image.new('RGB',(w*2+100,h+220),'#e9e3d6');dr=ImageDraw.Draw(board);dr.rectangle((w+50,0,w*2+100,h+220),fill='#24282b');
 for x,color,label in [(25,'#282820','浅底'),(w+75,'#f0e9dc','深底')]:
  dr.text((x,20),f'{name} · {cid}｜全身概念 · {label}',font=f,fill=color)
  board.paste(out,(x,100),out);dr.text((x,h+115),detail,font=small,fill=color);dr.text((x,h+155),'原创外观提案｜待独审｜非游戏运行验收',font=small,fill=color)
 board.save(o/f'{slug}_review_board_zh.png')
 for color,label in [('#f1ebdf','light'),('#24282b','dark')]:
  bg=Image.new('RGBA',im.size,color);bg=Image.alpha_composite(bg,out).convert('RGB');bg.save(o/f'{slug}_{label}_composite.png')
 qa=f'''# {name} 作者QA\n\n- 使用 builtin imagegen，transparent_background=true；首稿保留，无重绘。\n- 实际查看 Sela G、Mia v2、Luomin、Miloer 四参考及生成raw；人物来源按原卡、野外对白、关联台本核对。\n- {detail}，符合年龄/性别/职业线索；完整发梢、手、双脚和道具入画，短身成年体态、清晰像素簇与独立情绪。\n- 原稿alpha=0隐藏RGB不能当可见光晕；透明清理仅alpha≤8及隐藏RGB。alpha>8像素逐值未变。\n- 浅深板保持原尺寸，只有背景、中文标签与排版；无脚本重画人物、无裁切修人。\n- 发型、脸型、配色、未定衣装是可逆美术提案，不写回故事。\n- 未添加账本、巨武器、治疗/结算/担保/授权图示。\n- 待独立审查；人物外观概念不等于装备槽、原版帧表、体型兼容或runtime通过。\n'''
 (o/'AUTHOR_QA.md').write_text(qa);shutil.copy2('/tmp/package_lier_huier.py',o/'package_assets.py');shutil.copy2('/tmp/prepare_lier_huier.py',o/'prepare_sources.py')
 print(slug,json.dumps(stats,ensure_ascii=False))
