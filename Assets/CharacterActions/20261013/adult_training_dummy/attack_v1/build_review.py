from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
p=Path('Stoneshard_mod/Assets/CharacterActions/20261013/adult_training_dummy/attack_v1');font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';f=ImageFont.truetype(font,24);s=ImageFont.truetype(font,21);h=ImageFont.truetype(font,32)
# Equal scale for every phase, to leave room for forward sword reach.
for name in ['D0_guard','D1_windup','D2_forward']:
 im=Image.open(p/'originals'/f'{name}_raw_imagegen.png').convert('RGBA');im.putalpha(im.getchannel('A').point(lambda x:0 if x<16 else x));im=im.resize((1536,1536),Image.Resampling.NEAREST)
 if name=='D0_guard':
  t=Image.new('RGBA',(1536,1536));t.alpha_composite(im,(0,-24));im=t
 # 0.85 scale about common nominal root (768,1380).
 im=im.resize((1306,1306),Image.Resampling.NEAREST);out=Image.new('RGBA',(1536,1536));dx=115+(106 if name=='D2_forward' else 0);out.alpha_composite(im,(dx,207));out.save(p/'frames'/f'{name}.png')
files=['D0_guard.png','D1_windup.png','D2_forward.png'];sheet=Image.new('RGB',(1536,750),(35,39,43));d=ImageDraw.Draw(sheet);d.text((30,16),'无身份训练样板 · 原创攻击关键帧',font=h,fill=(244,230,194));d.text((30,64),'同一木质练习剑 / 单一视角 / 仅动作研究，不属于齐勒',font=s,fill=(163,183,188))
for i,file in enumerate(files):
 im=Image.open(p/'frames'/file);c=im.resize((512,512),Image.Resampling.NEAREST);sheet.paste(c,(512*i,112),c);d.line((512*i,572,512*i+511,572),fill=(57,105,115));d.text((512*i+45,607),['① 预备：低位持剑','② 蓄势：举剑','③ 挥出：向前下方'][i],font=f,fill=(240,231,212))
d.text((30,665),'3张不同姿态；不是原版逐帧还原，也未完成挥后回收和无缝循环。',font=s,fill=(205,210,212));d.text((30,697),'画布与足线仅为制作约定；握点、剑长、支撑轨迹仍需独审，未验证引擎或换装。',font=s,fill=(145,165,173));sheet.save(p/'dummy_attack_review_zh.png')
seq=[]
for file in files:
 im=Image.open(p/'frames'/file);bg=Image.new('RGBA',im.size,(35,39,43,255));bg.alpha_composite(im);seq.append(bg.convert('RGB').resize((768,768),Image.Resampling.NEAREST))
seq[0].save(p/'dummy_attack_preview_once.gif',save_all=True,append_images=seq[1:],duration=[700,700,1300])
m={'asset_id':'UNNAMED_ADULT_TRAINING_MODEL_ATTACK_V1','not_a_story_character':True,'not_chiler':True,'logical_canvas':[1536,1536],'foot_reference':[768,1380],'engine_origin':None,'collision':None,'native_fps':None,'runtime_verified':False,'equipment_compatibility_verified':False,'scope':'original articulated limb-action study; NOT native Stoneshard frame reproduction','rendering':'flattened body plus weapon, no recoverable layered equipment master','processing':'imagegen1254-square originals normalized to1536 then every phase uniformly scaled1306/1536 about root(768,1380) to allow sword reach. D0 registrationy-24; D2 x+106 in final canvas compensates generator framing drift; no per-limb warping, no interpolation.','preview':'one-shot three genuine generated poses, not loop; no recovery phase','handedness':'same visible screen-right sword hand, anatomical side unverified','frames':[{'id':file[:2],'path':'frames/'+file,'sha256':hashlib.sha256((p/'frames'/file).read_bytes()).hexdigest()} for file in files],'review_status':'awaiting independent review','limits':['minor face and silhouette regeneration drift','sword geometric and ground contact precision need review','not a gameplay hit-confirm window']};(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
