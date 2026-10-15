from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,zipfile,datetime,shutil
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');F=R/'Assets/EnemyDesigns/20261013/first_six';D=F/'restless_wraith_actions_delivery_v1';D.mkdir(exist_ok=True)
S=['canal_tomb_restless','crypt_drifter_wraith'];poses=[('canal_tomb_restless','drag_step','渠墓腐尸 · 拖步'),('canal_tomb_restless','slow_reach','渠墓腐尸 · 慢伸抓'),('crypt_drifter_wraith','forward_drift','墓龛游魂 · 前漂'),('crypt_drifter_wraith','spectral_reach','墓龛游魂 · 单手探出')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def rec(p):return {'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size}
for s in S:assert (F/s/'action_v1/FINAL_STATUS.json').exists(),s+' not finalized'
for mode,bg,fg in [('light',(237,234,222,255),(45,48,47,255)),('dark',(25,31,39,255),(226,231,226,255))]:
 im=Image.new('RGBA',(1800,1100),bg);dr=ImageDraw.Draw(im);font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
 dr.text((52,36),'渠墓腐尸与墓龛游魂｜基础动作',font=ImageFont.truetype(bold,48),fill=fg)
 dr.text((54,112),'拖步、伸抓、前漂、探手。保持同一形象，让动作从重心、手臂和碎尾中读出来。',font=ImageFont.truetype(font,26),fill=fg)
 for i,(s,p,label) in enumerate(poses):
  sprite=Image.open(F/s/'action_v1'/p/(s+'_'+p+'_transparent.png')).convert('RGBA');sprite=sprite.resize((430,645),Image.Resampling.NEAREST);im.alpha_composite(sprite,(20+i*445,225));dr.text((32+i*445,906),label,font=ImageFont.truetype(bold,25),fill=fg)
 dr.text((54,1005),'四张独立动作概念稿；尚未制作连续动画，也未接入游戏。',font=ImageFont.truetype(font,25),fill=fg)
 im.save(D/('restless_wraith_actions_overview_'+mode+'.png'))
shutil.copy2('/tmp/package_003_004.py',D/'package_delivery.py')
zips=[]
for s in S:
 root=F/s/'action_v1';zp=D/(s+'_action_v1_complete_sources.zip');before={str(p):sha(p) for p in root.rglob('*') if p.is_file()}
 with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(root.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(F)))
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None;members=[]
  for a in z.infolist():
   data=z.read(a.filename);members.append({'member':a.filename,'bytes':a.file_size,'compressed_bytes':a.compress_size,'crc32':f'{a.CRC:08x}','sha256':hashlib.sha256(data).hexdigest()})
 assert zp.stat().st_size<18*1024*1024
 assert before=={str(p):sha(p) for p in root.rglob('*') if p.is_file()}
 zips.append({**rec(zp),'members':members,'source_unchanged_during_packaging':True})
attachments=[F/s/'action_v1'/p/(s+'_'+p+'_transparent.png') for s,p,l in poses]+[D/'restless_wraith_actions_overview_light.png']+[R/z['path'] for z in zips]
put(D/'delivery.json',{'schema_version':1,'frozen':True,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'keypose_count':4,'first_drafts':4,'hard_error_revisions':0,'continuous_animation':False,'runtimeIntegrated':False,'runtimeVerified':False,'attachments':[rec(p) for p in attachments],'zip_packages':zips,'note':'004原冻结prompt_v1.txt缺失由实际调用恢复的prompt_evidence_addendum.json补全；两者均随包保留。','files':[rec(p) for p in sorted(D.iterdir()) if p.is_file() and p.name not in ['delivery.json','FINAL_DELIVERY_QA.json']]})
print(json.dumps({'directory':str(D),'attachments':[rec(p) for p in attachments]},ensure_ascii=False,indent=2))
