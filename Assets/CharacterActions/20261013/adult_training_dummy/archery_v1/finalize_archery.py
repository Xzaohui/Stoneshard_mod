from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,zipfile
p=Path(__file__).resolve().parent;sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
m=json.loads((p/'manifest.json').read_text());m['equipment_preparation']={'bow_extraction':'裁切后清除右下角属于独立箭羽的污染块；无补画弓身','arrow_preparation':'源箭一次固定700px长度、厚度乘0.65以匹配身体像素风；所有帧同一规范箭图，无逐帧缩放','layer_order':['string_state','body_complete','bow_rigid','arrow_rigid','bow_hand_foreground','draw_hand_foreground'],'occlusion_note':'弦置远侧，头/躯干/臂遮住其被身体挡住的段；完整弦图另存，不能以合成图可见线段当全部几何'}
for fr in m['frames']:
 for name in ['body_complete','string_state','bow_rigid','arrow_rigid']:
  q=f"masks/{fr['id']}_{name}_alpha.png";Image.open(p/fr['layers'][name]).getchannel('A').save(p/q);fr['masks']=list(dict.fromkeys(fr['masks']+[q]))
(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',28);board=Image.new('RGB',(1536,850),(35,40,45));d=ImageDraw.Draw(board)
for i,(q,label) in enumerate([(p.parent/'interaction_v1/frames/I0_stand.png','统一站立基准 935px'),(p/'layers/A0_body_complete.png','弓箭准备身体 935px；相同显示倍率')]):
 im=Image.open(q).resize((768,768),Image.Resampling.NEAREST);board.paste(im,(i*768,0),im);d.text((i*768+60,785),label,font=font,fill='white')
board.save(p/'cross_action_scale_review.png')
qa={'status':'author_visual_review_complete_pending_independent','viewed':['raw/A0.png','raw/A1.png','raw/A2.png','raw/equipment.png','frames/A0.png','frames/A1.png','frames/A2.png','frames/A3.png','archery_review_zh.png'],'observations_zh':{'A0':'双臂完整、双靴支撑。预备图已经搭箭并轻拉，并非空箭搭入过程；箭尾在拉弦手边，左手包住弓柄。','A1':'拉手抬至下颌、右肘后收，左持弓手向前；脸五官保持清楚，箭羽在下颌下方。弦中心与箭尾同坐标，身体遮住远侧弦段。','A2':'右手松开向后随势，左手保持弓；箭层为空、弦回直，不存在箭留在掌内或脚边残片。','A3':'复用A0身体但无箭、弦回直。只是恢复关键姿态，不冒称新增完整回收动画。'},'corrections':['弓裁切初版混入右下箭羽，清除后逐图复核','初版箭羽过厚遮嘴，统一规范箭层厚度乘0.65、A1箭尾下降到下颌下方后复核','弦采用远侧遮挡，不穿过脸的可见五官'],'limits':['非原版关节帧；未做引擎兼容、动作判定、射速','刚体弓轮廓不表现弓臂受力曲变，只作基础动作/图层提案','身体原稿小幅轮廓差异：A0高935、A1高938、A2高941px；共享倍率，未以逐帧拉伸伪修正','只有三个真实新身体，四阶段，未补连续插值与多方向']}
(p/'QA-author.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
(p/'README.md').write_text('# 普通木弓基础动作概念\n\n2026-10-13恢复制作，依用户“先继续绘制人物基础动作和人物设定，先不管实际落地”。3张新身体原稿＋1张独立弓箭原稿；四阶段A0搭箭预备（已搭箭轻拉）、A1拉弦瞄准、A2松弦随势（箭离画）、A3回稳（复用A0身体，无新箭）。\n\n1536²画布，站立基准935px；所有身体同一倍率，独立完整身体/木弓/弦/箭/手前遮挡层与mask，弓920px、箭700px不逐帧缩放。几何端点、箭尾、握点见manifest。作者逐图看过，仍待独审；未上传。\n\n原稿、prompt与哈希完整保留。层是原创概念分解，不是恢复原生装备槽/骨骼。固定弓形不模拟弓臂弹性，连续补间、多方向与精确手指钩弦未完成。GIF只播放一次，展示时间不代表游戏射速/命中判定。未改runtime或推送。\n')
files={str(q.relative_to(p)):sha(q) for q in p.rglob('*') if q.is_file() and q.name not in ['SHA256.json','archery_keyframes_review.zip']};(p/'SHA256.json').write_text(json.dumps(files,ensure_ascii=False,indent=2))
with zipfile.ZipFile(p/'archery_keyframes_review.zip','w',zipfile.ZIP_DEFLATED) as z:
 for q in p.rglob('*'):
  if q.is_file() and q.suffix!='.zip':z.write(q,str(q.relative_to(p)))
for name in ['archery_review_zh.png','archery_preview_once.gif','archery_keyframes_review.zip','manifest.json']:
 print(name,sha(p/name))
print('GIF loop',Image.open(p/'archery_preview_once.gif').info.get('loop'))
