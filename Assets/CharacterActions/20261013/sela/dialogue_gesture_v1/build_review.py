from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, hashlib, shutil
P=Path(__file__).resolve().parent
R=next(p for p in P.parents if (p/'AGENTS.md').exists())
G=R/'Assets/RedrawStudies/20261013/sela_proportions/facial_refinement/redesign_G/sela_G_raw_imagegen.png'
S=[G,P/'raw/01_open_palm_raw_imagegen.png',P/'raw/02_serious_confirm_raw_imagegen.png',G]
names=['01_rest_G','02_open_palm','03_serious_confirm','04_return_G']
labels=['01 待机 · 批准G复用','02 摊掌说明 · 新姿态','03 收手确认 · 新姿态','04 回待机 · 批准G复用']
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def f(n):return ImageFont.truetype(font,n)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
entries=[]; aligned=[]
for source,name,label in zip(S,names,labels):
 im=Image.open(source).convert('RGBA'); box=im.getchannel('A').point(lambda a: 255 if a>=128 else 0).getbbox(); crop=im.crop(box)
 # Same 0.5 nearest-neighbor scale across all poses, no body reshaping.
 crop=crop.resize((round(crop.width*.5),round(crop.height*.5)),Image.Resampling.NEAREST)
 canvas=Image.new('RGBA',(560,700)); footbox=im.getchannel('A').point(lambda a:255 if a>=128 else 0).crop((0,box[3]-90,im.width,box[3])).getbbox(); shoe_center=(footbox[0]+footbox[2])/2; x=round(280-(shoe_center-box[0])*.5);y=620-crop.height
 canvas.alpha_composite(crop,(x,y)); canvas.save(P/(name+'_aligned.png'));aligned.append(canvas)
 rawcopy=P/(name+'.png');shutil.copyfile(source,rawcopy)
 entries.append({'name':name,'label':label,'source':str(source.relative_to(R)),'sha256':sha(source),'export':rawcopy.name,'export_sha256':sha(rawcopy),'source_size':im.size,'alpha_bbox_threshold_128':box,'shoe_center_x':shoe_center,'visible_height':box[3]-box[1],'common_nearest_scale':.5,'aligned_size':[560,700],'paste':[x,y],'foot_bottom':620,'alpha_extrema':im.getchannel('A').getextrema()})
board=Image.new('RGB',(2240,890),'#eeebe4');d=ImageDraw.Draw(board)
d.text((40,25),'瑟拉 · 对话动作稀疏关键帧',font=f(40),fill='#243638')
d.text((40,85),'BRY-NPC-SELA  /  两张新姿态 + 批准G首末复用  /  同一0.50最近邻尺度，鞋底对齐',font=f(26),fill='#526161')
for i,im in enumerate(aligned):
 board.paste(im,(i*560,120),im);d.text((i*560+30,760),labels[i],font=f(25),fill='#243638')
d.text((40,824),'只演说话姿态，不代表付款、签字、授权或任务完成；已校验关键姿态概念。',font=f(25),fill='#526161')
board.save(P/'sela_dialogue_review_zh.png')
for bg,n in [('#ffffff','white'),('#000000','black')]:
 b=Image.new('RGB',(2240,700),bg)
 for i,im in enumerate(aligned):b.paste(im,(i*560,0),im)
 b.save(P/('qa_'+n+'_background.png'))
# GIF is a presentation of four held keys; omit loop extension for single playback.
frames=[]
for i,im in enumerate(aligned):
 b=Image.new('RGB',(560,780),'#eeebe4'); b.paste(im,(0,0),im); dr=ImageDraw.Draw(b)
 dr.text((20,695),labels[i],font=f(25),fill='#243638');dr.text((20,735),'稀疏关键帧 · 非连续动画验收',font=f(22),fill='#526161');frames.append(b)
frames[0].save(P/'sela_dialogue_once.gif',save_all=True,append_images=frames[1:],duration=[850,1100,1100,900],disposal=2,optimize=False)
manifest={'character':'BRY-NPC-SELA','status':'author_review_pending_independent','new_pose_count':2,'reused_pose_count':2,'new_character_count':0,'generator':'builtin imagegen','approved_source_sha256':sha(G),'poses':entries,'sequence':[e['name'] for e in entries],'gif':{'path':'sela_dialogue_once.gif','single_playback':True,'loop_extension':False,'durations_ms':[850,1100,1100,900],'note':'四个停留关键帧，非补间、连续动画或游戏帧表'},'operations':['original raw byte copies','alpha>=128 bbox crop only, preserve contained alpha; no alpha edits','common 0.5 nearest-neighbor scaling','shoe-center and foot-bottom translation','board and GIF presentation'],'runtime_verified':False,'animation_verified':False,'equipment_compatibility_verified':False,'files':{p.name:sha(p) for p in P.iterdir() if p.suffix in ['.png','.gif']}}
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(P/'sourcehash.json').write_text(json.dumps({'approved_G':{'path':str(G.relative_to(R)),'sha256':sha(G)},'character_card':{'path':'design/04_人物/城市人物/人物_BRY-NPC-SELA_瑟拉.md','sha256':sha(R/'design/04_人物/城市人物/人物_BRY-NPC-SELA_瑟拉.md')}},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(entries,ensure_ascii=False,indent=2))
