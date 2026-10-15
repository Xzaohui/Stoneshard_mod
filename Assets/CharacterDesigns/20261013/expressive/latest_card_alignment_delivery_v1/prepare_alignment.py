from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,numpy as np
base=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod/Assets/CharacterDesigns/20261013/expressive')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
notes={
'buya':('布娅','右手皮手套，左手保持裸露','询问侧目、原脸与梅灰绿旅行衣保留；铜牌/清单可收纳，未见不判缺失。'),
'yani':('雅尼','成人坐姿，右腿外支具与左袖补片','右腿完整裤腿外为金属/皮带支具；不是义肢，不证明康复。下巴旧疤被胡须遮挡，未核。'),
'oder':('奥德','短打水手褂与绳腰带','原翻领排扣去除；肤色、宽体态与表情保留。左小指半截在本图不可确认，仍待核。')}
for slug,(name,title,note) in notes.items():
 d=base/slug/'latest_card_alignment_v1';raw=d/f'{slug}_v1_raw_imagegen.png';im=Image.open(raw).convert('RGBA');a=np.array(im);n=int(((a[:,:,3]>0)&(a[:,:,3]<8)).sum());a[a[:,:,3]<8]=0;a[a[:,:,3]==0,:3]=0;clean=Image.fromarray(a);out=d/f'{slug}_v1_transparent.png';clean.save(out)
 for mode,bg,fg in [('light',(241,236,223,255),(48,43,38)),('dark',(35,39,47,255),(237,232,221))]:
  board=Image.new('RGBA',(1000,1540),bg);fit=clean.copy();fit.thumbnail((960,1320),Image.Resampling.NEAREST);board.alpha_composite(fit,((1000-fit.width)//2,120));draw=ImageDraw.Draw(board);draw.text((40,28),name+' · 最新角色卡补绘 v1',font=ImageFont.truetype(font,32),fill=fg);draw.text((40,76),title,font=ImageFont.truetype(font,25),fill=fg);draw.text((40,1470),'外观概念 · 非游戏落地验证',font=ImageFont.truetype(font,24),fill=fg);board.convert('RGB').save(d/f'{slug}_v1_{mode}_board.png')
 qa={'character':name,'status':'author_pass_with_cautions','method':'builtin image_gen identity-preserving edit','generation_count':1,'hard_error_revisions':0,'visually_inspected_original_and_output':True,'result':note,'current_card_gap_resolution':title,'limitations':['概念图，不是原生游戏精灵/动画/装备验证','source与旧母图不改，roster及历史QA/manifest不改'],'alpha_cleanup':{'threshold':'alpha < 8 set to RGBA(0,0,0,0); hidden RGB zeroed','low_nonzero_alpha_pixels_removed':n,'visible_body_redrawn_by_script':False,'board_layout':'uniform nearest-neighbor thumbnail only'},'raw_sha256':sha(raw),'transparent_sha256':sha(out)}
 (d/'QA-author.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 files=[{'path':str(p.relative_to(d)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(d.rglob('*')) if p.is_file() and p.name!='manifest.json']
 (d/'manifest.json').write_text(json.dumps({'schema_version':1,'character':name,'frozen':True,'scope':'latest_card_alignment_v1 standalone additions; no roster replacement','selected_raw':raw.name,'selected_transparent':out.name,'review_status':'author_complete_independent_pending','files':files},ensure_ascii=False,indent=2))
 print(slug, 'raw',sha(raw),'transparent',sha(out),'alpha cleaned',n)
