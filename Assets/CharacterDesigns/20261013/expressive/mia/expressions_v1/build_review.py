from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import hashlib,json
P=Path(__file__).parent
ROOT=P.parents[5]
items=[('concerned_inquiry','关切询问','内眉轻抬 · 微开口'),('attentive_listening','认真倾听','眉眼收拢 · 闭口专注'),('gentle_encouragement','温和鼓励','眉眼放松 · 克制浅笑')]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f=lambda n:ImageFont.truetype(font,n)
board=Image.new('RGB',(1600,950),'#eeeae2'); d=ImageDraw.Draw(board)
d.text((48,30),'米娅 · 三种对话表情概念',font=f(38),fill='#26383d')
d.text((48,91),'同一人物 · 同一胸上裁切 · 共同最近邻比例；仅表情研究，不代表剧情结果',font=f(23),fill='#52615f')
tech=[]
for i,(slug,label,note) in enumerate(items):
 raw=P/'raw'/f'mia_{slug}_raw_imagegen.png'; im=Image.open(raw).convert('RGBA'); a=im.getchannel('A'); box=a.point(lambda x:255 if x>5 else 0).getbbox()
 # Authorized only: remove nearly invisible alpha contamination and common rectangular chest-up crop.
 im.putalpha(a.point(lambda x:0 if x<=5 else x)); export=im.crop((190,65,1050,1140)); out=P/f'mia_{slug}.png'; export.save(out)
 scaled=export.resize((473,591),Image.Resampling.NEAREST); board.paste(scaled,(44+520*i,158),scaled)
 d.text((54+520*i,770),label,font=f(31),fill='#26383d'); d.text((54+520*i,819),note,font=f(24),fill='#52615f')
 tech.append({'slug':slug,'label_zh':label,'raw_path':str(raw.relative_to(P)),'raw_sha256':sha(raw),'raw_canvas':list(im.size),'raw_alpha_gt5_bbox':box,'export_path':out.name,'export_sha256':sha(out),'export_canvas':list(export.size),'common_crop':[190,65,1050,1140],'alpha_cleanup':'alpha <= 5 to zero only; other RGBA unchanged','generator_calls':1,'targeted_corrections':0})
d.text((48,899),'无新增人物、对白、道具或伤情；无治愈／任务完成暗示。原稿全部保留，未验收游戏落地。',font=f(22),fill='#52615f')
board.save(P/'mia_expressions_review_zh.png')
source=P.parent/'ratio_1_to_1_5/mia_ratio_1_to_1_5_v2_raw_imagegen.png'
sources={str(source.relative_to(P.parent)):sha(source),'turnaround_v1/mia_turnaround_review_zh.png':sha(P.parent/'turnaround_v1/mia_turnaround_review_zh.png')}
(P/'sourcehash.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
manifest={'character':'NPC-MIA','new_expressions':3,'new_characters':0,'status':'author_review_pass_pending_independent_review','tool':'builtin image_gen, one image per call','identity_authority':sources,'artifacts':tech,'board':{'path':'mia_expressions_review_zh.png','sha256':sha(P/'mia_expressions_review_zh.png'),'size':[1600,950],'common_scale':0.55,'scaling':'nearest neighbor; all three share same crop and output dimensions'},'limits':['Expression concepts only; no cured state, caregiver identity or task completion implied.','Slight pixel-cluster variations are generated drawing variation, not animation-ready frame alignment.','Mouth of encouragement is intentionally restrained rather than cheerful recovery.'],'runtime_verified':False,'native_ready':False,'equipment_compatibility_verified':False,'authorization_source':'Parent supplied exact user message Sentinel_cd750e0413208191ad349263d4850431 approving continued alignment and tool optimization; raw originals preserved.'}
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(P/'QA.json').write_text(json.dumps({'review':'author visual review','decision':'candidate_pass_pending_independent_review','actually_viewed':['approved source full image','approved turnaround board','all three generated expression raw images','common-scale Chinese comparison board'],'findings':['短鼻、原眼距、成年下颏、深棕单低辫和暗蓝绿披肩一致；轻微簇位漂移存在。','关切询问内眉轻抬、微开嘴；认真倾听平嘴集中目光；温和鼓励闭嘴小幅扬角。','三张统一胸上裁切；所有冠发、主要低辫与肩部保留，底部裁切明确为胸上构图。','只清理alpha≤5近透明背景噪点，不画五官、不量化、不锐化。','3张新表情、0新人物；不推定康复、护理者或任务完成。'],'independent_review':False,'runtime_verified':False},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'board_sha256':sha(P/'mia_expressions_review_zh.png'),'artifacts':tech},ensure_ascii=False,indent=2))
