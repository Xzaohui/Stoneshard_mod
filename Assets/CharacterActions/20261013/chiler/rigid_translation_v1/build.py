from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
p=Path('Stoneshard_mod/Assets/CharacterActions/20261013/chiler/rigid_translation_v1');src=Image.open(p.parent/'idle_v1/frames/I0_still.png').convert('RGBA');a=np.array(src);a[a[:,:,3]==0]=0;src=Image.fromarray(a);src.save(p/'layers/body_master.png');font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';f=ImageFont.truetype(font,25);h=ImageFont.truetype(font,32);s=ImageFont.truetype(font,21)
def frame(dx):
 o=Image.new('RGBA',(1536,1536));o.alpha_composite(src,(dx,0));return o
def scene(dx):
 o=Image.new('RGBA',(1536,1536),(35,39,43,255));d=ImageDraw.Draw(o);d.line((0,1382,1536,1382),fill=(90,113,121),width=3)
 for x in range(96,1536,96):d.line((x,1380,x,1404),fill=(90,113,121),width=3)
 o.alpha_composite(frame(dx));d.text((48,48),'齐勒 · 主体刚性位移检视',font=h,fill=(240,229,205));d.text((48,102),'1个独立主体 / 位置采样 / 无新增腿部绘制',font=f,fill=(166,188,193));d.text((48,1450),f'root x={768+dx}  y=1380   ·   时间为展示设定',font=f,fill=(180,194,198));return o.convert('RGB')
seq=[];records=[]
for i,dx in enumerate(range(-180,109,24)):
 o=frame(dx);records.append({'sample':i,'root':[768+dx,1380],'translation':[dx,0],'time_ms':i*40,'new_pose':False});seq.append(scene(dx).resize((768,768),Image.Resampling.NEAREST))
keys=[-180,-84,12,108];sheet=Image.new('RGB',(1536,690),(35,39,43));d=ImageDraw.Draw(sheet);d.text((25,18),'齐勒 · 刚性位移表现研究',font=h,fill=(246,230,192));d.text((25,68),'同一主体平移：角色外貌、握棒与装备附着保持一致',font=f,fill=(183,204,208))
for i,dx in enumerate(keys):
 im=frame(dx);im.save(p/'frames'/f'T{i}.png');sm=im.resize((384,384),Image.Resampling.NEAREST);sheet.paste(sm,(i*384,120),sm);d.line((i*384,466,(i+1)*384,466),fill=(90,113,121),width=2);d.text((i*384+18,520),['起点','位移 1','位移 2','到位'][i],font=f,fill=(240,230,210));d.text((i*384+18,558),f'root x={768+dx}',font=s,fill=(170,195,201))
d.text((25,605),'1个独立主体，4个检视位置；GIF含13个平移采样，无插值新绘姿态。',font=s,fill=(204,212,215));d.text((25,642),'参考官方位置变化表现；不是完整步态，不授予齐勒冲刺技能或原生引擎参数。',font=s,fill=(172,190,198));sheet.save(p/'chiler_rigid_translation_review_zh.png');seq[0].save(p/'chiler_rigid_translation_once.gif',save_all=True,append_images=seq[1:],duration=[400]+[40]*11+[650],disposal=2)
checks=[]
for i,dx in enumerate(keys):
 im=Image.open(p/'frames'/f'T{i}.png');back=Image.new('RGBA',src.size);back.alpha_composite(im,(-dx,0));checks.append({'id':f'T{i}','inverse_translation_equals_master':np.array_equal(np.array(back),np.array(src)),'alpha0_RGB_zero':bool(np.all(np.array(im)[np.array(im)[:,:,3]==0]==0))})
(p/'manifest.json').write_text(json.dumps({'unique_body_images':1,'key_positions':4,'gif_position_samples':13,'new_drawn_poses':0,'logical_canvas':[1536,1536],'engine_origin':None,'native_fps':None,'complete_gait_cycle':False,'root_trajectory':records,'checks':checks,'body_sha256':hashlib.sha256((p/'layers/body_master.png').read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
(p/'README.md').write_text('''# 齐勒刚性位移表现研究\n\n沿用已审原稿，共1个独立主体；4张PNG只是同一主体平移后的检视位置，GIF为13次整数像素位置采样，不计新增绘制。无人物镜像、腿部重绘或武器替换。\n\n参考：2020-03-15官方Athletics Devlog中Dash示例可见紧凑主体位移和拖尾（本项目ReferenceAudit/20261013/actions/REFERENCE_AUDIT.md）。这里只借鉴“主体位置变化”表现，未复制第三方图像，也未给齐勒添加战斗冲刺技能；本样例不含拖尾。\n\n1536²为研究画布，root工作点从(588,1380)到(876,1380)，y固定。GIF中移动采样40ms，首尾400/650ms，单次播放无回跳；这些都是检视设定，不是游戏速度。足底随主体在地面上平移，明确存在滑移，这是刚性表现演示，不能叫完整交替步行、无滑步或物理接触验收。\n\n此前walk_cycle_v2/v3_rig/v4_guided均保留研究。两轮局部生成仍未解决K1支撑重心和远腿髋膝踝可读性，独审建议停止扩展；没有完成完整循环。\n\n换装兼容、原生origin、碰撞、事件、方向、游戏内播放均未验收。\n''')
print(checks)
