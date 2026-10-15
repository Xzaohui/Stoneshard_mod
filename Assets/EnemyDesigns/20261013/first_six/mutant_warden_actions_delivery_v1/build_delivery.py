from pathlib import Path
import hashlib,json,shutil,zipfile,zlib,datetime
from PIL import Image,ImageDraw,ImageFont
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); base=R/'Assets/EnemyDesigns/20261013/first_six'; D=base/'mutant_warden_actions_delivery_v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[('blood_hunger_mutant','low_coil','饥血潜行体 · 低伏蓄势'),('blood_hunger_mutant','short_claw_extend','饥血潜行体 · 短爪伸展'),('debt_ritual_warden','bar_guard','债契仪式看守 · 横杆拦阻'),('debt_ritual_warden','side_step_guard','债契仪式看守 · 侧步戒备')]
selected=[]
for s,p,label in rows:
 a=base/s/'action_v1';q=a/'independent_action_QA.json'; assert q.exists(),str(q)
 review=json.loads(q.read_text());d=a/p;v=d/'revision_v2' if p=='short_claw_extend' else d
 name=f'{s}_{p}_transparent'+('_v2' if p=='short_claw_extend' else '')+'.png';out=v/name
 entry=next(x for x in review['poses'] if x['pose']==p);assert entry['result']=='pass';assert entry['sha256']==sha(out)
 status={'status':'concept_pass','selected_output':str(out.relative_to(R)),'selected_sha256':sha(out),'selected_manifest':str((v/'manifest.json').relative_to(R)),'manifest_sha256':sha(v/'manifest.json'),'independent_QA':str(q.relative_to(R)),'independent_QA_sha256':sha(q),'author_actual_view':['static anchor','raw','light_dark compositing preview'],'budget':{'first_drafts':1,'hard_error_revisions':int(p=='short_claw_extend'),'max_hard_error_revisions':1},'rejected_v1_reason':'右侧爪外轮廓触边；修订稿已完整留边。' if p=='short_claw_extend' else None,'runtimeIntegrated':False,'runtimeVerified':False,'continuous_animation':False}
 f=d/'FINAL_STATUS.json'; assert not f.exists();f.write_text(json.dumps(status,ensure_ascii=False,indent=2))
 cp=D/f'{s}_{p}_transparent.png';shutil.copy2(out,cp);selected.append((s,p,label,cp))
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';title=ImageFont.truetype(font,42);sub=ImageFont.truetype(font,26);small=ImageFont.truetype(font,22)
for mode,bg,fg in [('light',(239,234,223),(42,38,34)),('dark',(29,33,40),(234,231,219))]:
 board=Image.new('RGB',(1600,1480),bg);draw=ImageDraw.Draw(board);draw.text((48,26),'怪物基础动作 · 饥血潜行体与债契仪式看守',font=title,fill=fg);draw.text((48,90),'四张独立动作定格，沿用既有角色外形与装备。',font=sub,fill=fg)
 for i,(s,p,label,f) in enumerate(selected):
  x=(i%2)*800;y=145+(i//2)*620;draw.text((x+40,y),label,font=sub,fill=fg)
  im=Image.open(f).convert('RGBA');im.thumbnail((735,530),Image.Resampling.NEAREST);board.paste(im,(x+(800-im.width)//2,y+58+(530-im.height)//2),im)
 draw.text((48,1420),'概念动作稿；尚未制作连续动画，也未接入游戏。',font=small,fill=fg);board.save(D/f'actions_overview_{mode}.png')
(D/'README.txt').write_text('饥血潜行体与债契仪式看守：四张基础动作定格。\n浅深底总览便于检查轮廓；四张透明PNG为各姿选稿。\n原始生成、母图、提示词、来源快照、清理脚本、作者检查及独立复核均保留。\n饥血潜行体短爪伸展首稿右爪触边，使用唯一一次修订补齐留边；首稿仍保留作记录。\n本批只完成概念关键姿势，不代表连续动画、碰撞、绑定或游戏实测。\n',encoding='utf-8')
print('Final statuses and preview boards ready; inspect before running seal_delivery.py')
