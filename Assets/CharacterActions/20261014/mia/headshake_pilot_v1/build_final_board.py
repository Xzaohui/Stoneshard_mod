from pathlib import Path
import json,hashlib,shutil,base64,re
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parent
sel=[('K1','K1_v1'),('K2','K2_v2')]
for k,stem in sel:shutil.copyfile(D/'raw'/f'{stem}.png',D/'selected'/f'mia_{k}_selected.png')
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',22)
for theme,bg,fg in [('light',(233,229,218),(35,37,43)),('dark',(32,37,46),(239,235,222))]:
 b=Image.new('RGB',(2240,800),bg);dr=ImageDraw.Draw(b)
 files=['sources/4_mia_ratio_1_to_1_5_v2_raw_imagegen.png','selected/mia_K1_selected.png','selected/mia_K2_selected.png']
 labels=['K0 起势｜复用母图','K1 轻摇头｜新绘左转','K2 反向｜新绘近正面','K3 回稳｜未通过，保留缺项']
 for i,s in enumerate(files):
  im=Image.open(D/s).convert('RGBA').resize((559,704),Image.Resampling.NEAREST);b.paste(im,(i*560,48),im)
 for i,s in enumerate(labels):dr.text((i*560+16,12),s,font=font,fill=fg)
 for y,t in [(320,'收势两稿未锁住鞋形与脚距'),(360,'仅保留原稿和审查证据'),(400,'不计入合格关键帧')]:dr.text((1730,y),t,font=font,fill=fg)
 dr.text((18,763),'米娅抱毯轻摇头·四阶段小样｜2张合格新绘＋1张母图复用＋1缺项｜非完整循环，仍有细微重绘漂移',font=font,fill=fg)
 b.save(D/f'mia_headshake_final_{theme}_zh.png')
readme='''# 米娅抱毯轻摇头：四阶段小样（缺收势）

## 交付口径
2张合格新绘（K1_v1、K2_v2）＋1张批准母图复用（K0）＋K3缺项。共5次真实imagegen调用：K1一次、K2两次、K3两次。不是完整循环、不是游戏精灵，也不表示痊愈。米娅仅替自己回应。

正式对照板为mia_headshake_final_light_zh.png / dark_zh.png，K3留空并标原因。selected/仅含两张真正通过的小样。其他review/candidates板是阶段候选审查证据，不能当正式交付。

K2_v1因发缝与辫子镜像换边未收。K3_v1与v2动作本身可读，但鞋形/脚距漂移不满足固定双脚约束；唯一修订后仍未通过，均不计合格。母图鞋间距77px，K3v1为88px、v2为89px；v2左鞋宽144 vs母139，右124 vs母126，基线1334 vs1328。未脚本移动或拼接修图。

K1/K2仅通过美术概念小样，仍有少量重绘位置漂移，不宣称像素级固定或实机稳定。所有raw、完整含payload返回、预存参数与失败证据均保留。参数为作者侧调用前记录，不是服务端回显。

## 来源与技术
sourcehash.json含原人物卡、批准母图、项目规则和归档工作流SHA。所有选稿直接复制raw，未改变像素。排版统一缩放整张画布，最近邻，不进行逐图裁剪配齐、变形、拼头或插值。无GIF、无Git、未上传、未修改游戏。
'''
(D/'README.md').write_text(readme)
(D/'CALL_RECORD.md').write_text((D/'CALL_RECORD.md').read_text().replace('Four serial','Five serial').replace('K3_v1. K1','K3_v1, K3_v2 (sole hard-error correction for foot geometry). K1')+'\nK3_v2 params were saved before the tool call; the identical object was passed to image_gen. Input 1 was K3_v1 edit target and input 2 approved mother body reference, both visually inspected beforehand. K3_v2 still failed strict foot registration and is not selected.\n')
manifest={'status':'partial_concept_pilot','acceptedNew':2,'reusedMother':1,'missingStages':['K3'],'generationCalls':5,'completeLoop':False,'runtimeVerified':False,'selected':[{'stage':k,'raw':f'raw/{s}.png','file':f'selected/mia_{k}_selected.png','sha256':hashlib.sha256((D/'raw'/f'{s}.png').read_bytes()).hexdigest()}for k,s in sel],'rejected':['raw/K2_v1.png','raw/K3_v1.png','raw/K3_v2.png'],'finalBoards':['mia_headshake_final_light_zh.png','mia_headshake_final_dark_zh.png']}
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
out=[]
for f in sorted((D/'returns').glob('*.json')):
 r=json.loads(f.read_text());raw=D/'raw'/f'{f.stem}.png';payload=base64.b64decode(r['image_url'].split(',')[1]);src=Path(re.findall(r'/workspace/[^\s]+\.png',r['output_hint'])[0]);assert src.read_bytes()==raw.read_bytes()==payload
 out.append({'call':f.stem,'originalToolOutput':str(src),'originalMatchesArchivedRaw':True,'payloadMatchesRaw':True,'sha256':hashlib.sha256(payload).hexdigest()})
(D/'ORIGINAL_OUTPUT_VERIFICATION.json').write_text(json.dumps(out,indent=2))
print('Final two selected; K3 missing.')
