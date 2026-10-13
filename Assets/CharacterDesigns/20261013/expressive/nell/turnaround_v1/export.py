from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,numpy as np
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); E=R/'Assets/CharacterDesigns/20261013/expressive'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(src,dst):
 im=Image.open(src).convert('RGBA');arr=np.array(im);a=arr[:,:,3];n=int(((a>0)&(a<8)).sum());a[a<8]=0;arr[:,:,3]=a;Image.fromarray(arr).save(dst)
 return {'source':str(src.relative_to(R)),'output':str(dst.relative_to(R)),'source_sha256':sha(src),'output_sha256':sha(dst),'operation':'Only alpha values 1..7 set to zero; RGB bytes unchanged; alpha >=8 unchanged. No body/face edits, resampling, palette reduction or interpolation.','cleared_alpha_pixels':n,'canvas':im.size,'bbox':Image.fromarray(arr).getbbox()}
def board(items,out,title,dark=False):
 bg='#252933' if dark else '#f2eee5';fg='#eee8dd' if dark else '#30323b';im=Image.new('RGB',(1500,920),bg);d=ImageDraw.Draw(im);F=lambda n:ImageFont.truetype(font,n);d.text((38,22),title,font=F(30),fill=fg);d.text((38,68),'现行比例补设定 · 旧稿已有背面 · 未知结构为设计推定 · 非游戏动画',font=F(20),fill=fg)
 for i,(p,label) in enumerate(items):
  a=Image.open(p).convert('RGBA');a=a.crop(a.getbbox());s=min(420/a.width,660/a.height);wh=(round(a.width*s),round(a.height*s));a=a.resize(wh,Image.Resampling.NEAREST);x=i*500+(500-wh[0])//2;y=790-wh[1];im.paste(a,(x,y),a);d.text((i*500+38,818),label,font=F(23),fill=fg)
 d.text((38,874),'全图等比 nearest 排版；原始稿与处理记录随包保留。正面为原锚复用，不计新增。',font=F(18),fill=fg);im.save(out)
for c,name in [('nell','妮尔'),('sel','塞尔')]:
 o=E/c/'turnaround_v1';shutil.copy2(__file__,o/'export.py');logs=[]
 choices={'left_side':'raw_left_side_v2.png' if c=='sel' else 'raw_left_side.png','back':'raw_back.png'}
 for v,raw in choices.items():logs.append(clean(o/raw,o/'selected'/f'{c}_{v}.png'))
 logs.append(clean(E/c/f'{c}_v2_raw_imagegen.png',o/'selected'/f'{c}_front_anchor_reused.png'))
 items=[(o/'selected'/f'{c}_front_anchor_reused.png','正面锚｜复用对照'),(o/'selected'/f'{c}_left_side.png','身体左侧｜朝画面右'),(o/'selected'/f'{c}_back.png','正背面｜衣层设计推定')]
 for dark in [False,True]:board(items,o/f'{c}_turnaround_zh_{"dark" if dark else "light"}.png',f'{name}｜现行衣装侧背补设定',dark)
 (o/'processing_log.json').write_text(json.dumps({'alpha_cleanup':logs,'review_board':'Uniform whole-figure nearest-neighbor fit within 420x660, composited on solid review backgrounds. No body part stretching.','raws_preserved':True,'new_views':2,'new_people':0,'new_expressions':0,'runtime_verified':False,'revision_count':1 if c=='sel' else 0,'revision_reason':'Initial Sel face was side profile but torso/apron remained front three-quarter; v2 reduces apron to profile, one near upper tab, overlapping legs.' if c=='sel' else None},ensure_ascii=False,indent=2))
 qa={'status':'author_visual_pass_pending_independent_final','character':c,'source_sha_verified':True,'views_actually_inspected':['current_anchor','historical_pair_v2','raw_left_side','raw_back']+(['raw_left_side_v2'] if c=='sel' else []),'selected':choices,'checks':['Full head and shoes; same mature identity/short-body proportions','Side faces right with near anatomical left side; back has no face','Props retained on original anatomical side, no duplicated/new equipment','Nell short shawl/left waist cloth separate, no bag' if c=='nell' else 'Sel narrow nape neck strap consistent; red shirt back, front-only apron; empty hands separate from left-front pliers'],'design_inference':'Short triangular rear shawl and fringe continuity, no new knots.' if c=='nell' else 'Minimal U neck-loop joins front apron tabs; not previously validated in current anchor.','history_disclosure':'20261012 older long-proportion paired boards already included back views. These are current-proportion updates, not first-ever rear views.','limitations':['Static concept only, not engine-ready animation','No runtime, equipment or garment modularity verification']}
 (o/'authorQA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 (o/'README_zh.md').write_text(f'# {name}：现行衣装侧背补设定\n\n新增2张静态设定，0新人。正面原锚复用只用于比对。旧比例配对板已有背面；本轮更新现行比例。未知背部结构为可撤回的Mod原创设计推定。\n\n选稿：'+str(choices)+'\n\n身体左侧面朝画面右；正背不回头。保留全部原稿、输入锚、人物卡、N3/N4台本、brief、完整提示词和处理日志。只有alpha 1—7低透明噪点清零，RGB不改；排版全图等比nearest，不拉伸身体、不绘制脸或内插磨皮。非最终游戏资产。\n')
 # Freeze all author-side evidence; later independent QA and FINAL_STATUS must not mutate this manifest.
 files=[{'path':str(p.relative_to(o)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(o.rglob('*')) if p.is_file() and p.name not in ['manifest.json','FINAL_STATUS.json','QA-independent.json']]
 manifest={'schema_version':1,'status':'frozen_author_deliverable_pending_independent_QA','character':c,'new_unique_views':2,'new_characters':0,'reused_front_anchor':True,'method':'Built-in image_gen; final face and body generated, not drawn by scripts','selected':choices,'files':files,'processing_log_sha256':sha(o/'processing_log.json'),'runtime_verified':False}
 (o/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print(c,'manifest',sha(o/'manifest.json'),'files',len(files))
