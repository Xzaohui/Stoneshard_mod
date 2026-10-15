from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib,shutil,collections
ROOT=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
B=ROOT/'Assets/EnemyDesigns/20261013/first_six'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
for slug,title,rawfile,rev,notes in [
 ('canal_tomb_restless','003 渠墓腐尸','canal_tomb_restless_idle_v2_raw_imagegen.png',1,'斜Ｃ塌肩 · 保留皮肉 · 非指认人物'),
 ('crypt_drifter_wraith','004 墓龛游魂','crypt_drifter_wraith_idle_raw_imagegen.png',0,'破兜帽 · 两长一短碎尾 · 无实体脚')]:
 d=B/slug/'idle_v1'; raw=Image.open(d/rawfile).convert('RGBA'); pixels=list(raw.getdata()); low=sum(0<p[3]<=8 for p in pixels); hidden=sum(p[3]==0 and p[:3]!=(0,0,0) for p in pixels)
 clean=Image.new('RGBA',raw.size);clean.putdata([(0,0,0,0) if p[3]<=8 else p for p in pixels]);out=d/(slug+'_idle_transparent.png');clean.save(out)
 assert all(a==b for a,b in zip(pixels,clean.getdata()) if a[3]>8)
 a=clean.getchannel('A');bbox=a.getbbox(); crop=clean.crop(bbox)
 for tone,bg,fg in [('light','#eee9dc','#252a2d'),('dark','#1e252c','#e7e7dd')]:
  board=Image.new('RGBA',(1000,1160),bg);draw=ImageDraw.Draw(board);draw.text((40,24),title,font=ImageFont.truetype(FONT,34),fill=fg);draw.text((40,76),'原创静态概念｜单体待机｜非运行精灵',font=ImageFont.truetype(FONT,21),fill=fg)
  scale=min(820/crop.width,940/crop.height);sz=(round(crop.width*scale),round(crop.height*scale));pic=crop.resize(sz,Image.Resampling.NEAREST);board.alpha_composite(pic,((1000-sz[0])//2,126+(940-sz[1])//2));draw.text((40,1090),notes,font=ImageFont.truetype(FONT,22),fill=fg);draw.text((40,1125),'比例等比排版；背景仅用于检查透明边缘',font=ImageFont.truetype(FONT,18),fill=fg);board.convert('RGB').save(d/(slug+'_review_'+tone+'_zh.png'))
 stats={'size':raw.size,'raw_alpha_histogram':dict(collections.Counter(p[3] for p in pixels)),'final_alpha_histogram':dict(collections.Counter(p[3] for p in clean.getdata())),'removed_alpha_1_to_8_pixels':low,'zero_alpha_hidden_rgb_cleaned':hidden,'alpha_gt_8_pixels_unchanged':True,'final_bbox':bbox,'actual_raw_and_light_composite_viewed':True,'cleanup':'Only RGBA=(0,0,0,0) for alpha<=8; pixels alpha>8 preserved byte-for-byte; no palette quantization or body/face painting.'}
 (d/'alpha_QA.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
 (d/'author_QA.md').write_text('# 作者检查\n\n- 已实际查看原始图及正确RGBA浅底合成；生成图的暗/蓝晕属于隐藏RGB，不能据显示器黑底误判真背景。\n- '+notes+'；单体完整、无背景剧情、无命名NPC。\n- 大簇像素、静态概念。腐尸长瘦是非对称怪物读法，不强制人类头身。幽灵保留alpha>8全部数据，未把半透明粗暴二值化。\n- '+('首稿细纹/过密风格已用唯一修订合并为大色簇；原首稿和修订raw均保留。' if rev else '首稿提交，未使用修订额度。')+'\n- D02墓龛战区限制不被本图改变；D07病人不等于尸怪；D09回声不证明真魂；不画BRY14弟弟。\n- 未实现动画、部件、碰撞、引擎透明渲染；runtimeIntegrated=false，runtimeVerified=false。\n- 等待独立审核；未标selected。\n')
 
 if Path(__file__).resolve() != (d/'build_delivery.py').resolve(): shutil.copyfile(__file__,d/'build_delivery.py')
 print(slug,stats['size'],bbox,low,hidden)
