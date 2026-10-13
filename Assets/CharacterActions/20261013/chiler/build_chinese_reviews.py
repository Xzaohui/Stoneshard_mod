from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,zipfile
base=Path('Stoneshard_mod/Assets/CharacterActions/20261013/chiler');font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';f=ImageFont.truetype(font,24);title=ImageFont.truetype(font,32);small=ImageFont.truetype(font,21)
p=base/'startle_v1';im=Image.open(p/'originals/R1_startle_raw_imagegen.png').convert('RGBA');im.putalpha(im.getchannel('A').point(lambda x:0 if x<16 else x));im.resize((1536,1536),Image.Resampling.NEAREST).save(p/'frames/R1_startle.png');shutil.copy2(base/'idle_v1/frames/I0_still.png',p/'frames/R0_still.png');shutil.copy2(base/'idle_v1/frames/I0_still.png',p/'frames/R2_return_reuse_R0.png')
for dirname,files,labels,heading,sub,note,out in [
('walk_v1',['W0_support.png','W1_swing.png','W2_contact.png'],['① 支撑：双脚站稳','② 摆步：一脚离地','③ 落脚：前脚接触'],'齐勒 · 原创短步关键帧','同一人物 / 单一视角 / 共享画布','只展示一步的关键阶段；还不是完整交替步行循环。脸与发簇仍有轻微重绘差异。','chiler_walk_review_zh.png'),
('startle_v1',['R0_still.png','R1_startle.png','R2_return_reuse_R0.png'],['① 静站','② 受惊：收肩、手护胸','③ 回稳：复用静站帧'],'齐勒 · 受惊回稳关键帧','原创表演提案 / 不表示剧情受伤','3个逻辑阶段、2张不同图片；回稳复用首帧。不是原版受击动画或受伤设定。','chiler_startle_review_zh.png')]:
 p=base/dirname;sheet=Image.new('RGB',(1536,730),(35,39,43));d=ImageDraw.Draw(sheet);d.text((30,18),heading,font=title,fill=(244,230,194));d.text((30,62),sub,font=small,fill=(163,183,188))
 for i,file in enumerate(files):
  im=Image.open(p/'frames'/file);c=im.resize((512,512),Image.Resampling.NEAREST);sheet.paste(c,(i*512,112),c);d.line((i*512,572,i*512+511,572),fill=(57,105,115));d.line((i*512+256,563,i*512+256,585),fill=(190,164,69));d.text((i*512+44,608),labels[i],font=f,fill=(241,233,214))
 d.text((30,666),note,font=small,fill=(205,210,212));d.text((30,696),'青线仅为制作基准；未验证原生尺寸、换装兼容或游戏内运行。',font=small,fill=(145,165,173));sheet.save(p/out)
 if dirname=='startle_v1':
  seq=[]
  for file in files:
   im=Image.open(p/'frames'/file);bg=Image.new('RGBA',im.size,(35,39,43,255));bg.alpha_composite(im);seq.append(bg.convert('RGB').resize((768,768),Image.Resampling.NEAREST))
  seq[0].save(p/'chiler_startle_preview_once.gif',save_all=True,append_images=seq[1:],duration=[650,900,1100])
  m={'asset_id':'ALD-NPC-CHILER_STARTLE_CONCEPT_V1','logical_canvas':[1536,1536],'foot_anchor':[768,1380],'engine_origin':None,'collision':None,'native_timing':None,'runtime_verified':False,'equipment_compatibility_verified':False,'scope':'non-injurious original startled performance; not combat hurt','processing':'R1 built-in imagegen1254 square normalized whole canvas to1536 nearest-neighbor; alpha<16 removed; no local warp.','preview':'one-shot3 stages/2unique images; no interpolation; R2 exact reuse R0','frames':[{'id':file[:2],'path':'frames/'+file,'sha256':hashlib.sha256((p/'frames'/file).read_bytes()).hexdigest(),'reuse_of':'R0' if i==2 else None} for i,file in enumerate(files)]};(p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
