#!/usr/bin/env python3
"""Layout/copy/verify frozen candidates only. Does not draw or alter portrait pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,hashlib,shutil,sys
D=Path(__file__).resolve().parent
R=D.parent.parent
ORDER=['maler','maris','miro','oder']
NAMES={'maler':'麦勒','maris':'玛莉丝','miro':'米罗','oder':'奥德'}
LIMITS={'maler':'灰须亮暗条稍细；旧眼镜压痕弱可读','maris':'笑意很轻、仍偏克制；无确切年龄设定','miro':'礼貌眼笑含蓄；灰鬓不明显','oder':'胡须仍有细条；眉盐霜未能逐点确认'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
F=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
B=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
font=lambda s,b=False:ImageFont.truetype(str(B if b else F),s)
selection=[]
gate=json.loads((D/'freeze_gate.json').read_text()); assert gate['approved_to_package'] is True
final_path=R/gate['selection_file']; assert sha(final_path)==gate['selection_sha256']
final=json.loads(final_path.read_text())
comparison=final['actors']; comparison=[dict(x,slug=k,selected_portrait=x['selected_candidate']) for k,x in comparison.items()] if isinstance(comparison,dict) else comparison
assert final['approved_for_candidate_packaging'] is True
for c in ORDER:
 m=json.loads((R/c/'manifest.json').read_text())
 source=R/c/m['selected_portrait']; h=sha(source)
 independent=next(x for x in comparison if x['slug']==c)
 assert (R/c/independent['selected_portrait']).resolve()==source.resolve() and independent['selected_sha256']==h,c
 assert sha(R/c/'manifest.json')==independent['frozen_manifest_sha256']
 im=Image.open(source); assert im.size==(74,100),c
 rgba=im.convert('RGBA'); alpha=set(rgba.getchannel('A').getdata()); assert alpha<={0,255}
 colors=len(set(px[:3] for px in rgba.getdata() if px[3])); assert colors<=32
 out=D/f'{c.upper()}_{NAMES[c]}_74x100_candidate.png'
 if out.exists(): assert sha(out)==h, 'Refuse replacing a differing delivery copy'
 else: shutil.copyfile(source,out)
 assert sha(out)==h
 selection.append({'actor':c,'name':NAMES[c],'source':source.relative_to(R).as_posix(),'source_sha256':h,'delivery_file':out.name,'delivery_sha256':sha(out),'dimensions':[74,100],'visible_rgb_colors':colors,'alpha_values':sorted(alpha),'selected_version':source.name.split('_74x100')[0],'quantization':'MAXCOVERAGE' if '_maxcoverage_' in source.name else 'MEDIANCUT','limitations':LIMITS[c],'native_authored':False,'runtime_integrated':False,'runtime_verified':False})
# The board uses intact source pixels at 1x and integer 4x nearest-neighbor only.
W,HEADER,ROW,FOOT=680,154,466,128
board=Image.new('RGB',(W,HEADER+ROW*4+FOOT),(22,24,28)); draw=ImageDraw.Draw(board)
text=(237,230,216); muted=(180,178,174); accent=(217,183,130)
draw.text((28,21),'头像重绘 · 第七批 4 人',font=font(32,True),fill=text)
draw.text((28,71),'原尺寸 74×100  +  4 倍最近邻放大',font=font(23),fill=accent)
draw.text((28,110),'2026.10.15  ·  冻结候选  ·  仅排版，不补画',font=font(19),fill=muted)
checks=[]
for i,item in enumerate(selection):
 c=item['actor']; y=HEADER+i*ROW; bg=(31,32,37) if i%2==0 else (26,28,32)
 draw.rectangle((16,y,663,y+ROW-12),fill=bg)
 draw.text((36,y+24),f'{i+1:02d}  {NAMES[c]}',font=font(30,True),fill=text)
 draw.text((36,y+73),c.upper(),font=font(20),fill=accent)
 draw.text((36,y+102),{'maler':'男 · 六十余岁老楼房主','maris':'女 · 精灵扣件匠商','miro':'男 · 五十岁上下联络员','oder':'男 · 五十余岁船主'}[c],font=font(16),fill=muted)
 draw.text((36,y+130),'原尺寸 1×',font=font(19),fill=muted)
 im=Image.open(D/item['delivery_file']).convert('RGBA')
 for scale,x,yy in [(1,87,y+172),(4,328,y+15)]:
  src=im if scale==1 else im.resize((74*scale,100*scale),Image.Resampling.NEAREST)
  board.paste(src,(x,yy),src)
  expect=Image.new('RGB',src.size,bg); expect.paste(src,(0,0),src)
  assert board.crop((x,yy,x+src.width,yy+src.height)).tobytes()==expect.tobytes()
  checks.append({'actor':c,'scale':scale,'resampling':'NEAREST' if scale>1 else 'none','box':[x,yy,x+src.width,yy+src.height],'composited_pixels_exact':True})
 draw.text((36,y+288),'74 × 100 PNG',font=font(18),fill=muted)
 draw.text((36,y+319),f'{item["visible_rgb_colors"]} 色 · 透明底',font=font(18),fill=muted)
 draw.text((36,y+416),LIMITS[c],font=font(19),fill=muted)
y=HEADER+ROW*4
draw.text((28,y+11),'高分辨率生图经最近邻缩放与无抖动量化。',font=font(21),fill=text)
draw.text((28,y+47),'非原生手工逐像素终稿；尚未集成或实机验证。',font=font(21),fill=text)
draw.text((28,y+88),'原始生图、提示词、工具返回、来源与 QA 随源包保留。',font=font(18),fill=muted)
out=D/'batch07_四人头像总览_1x_4x.png'
board.save(out,optimize=True)
js(D/'selected_delivery_manifest.json',{'batch':'07','date':'2026-10-15','characters':selection,'board':{'file':out.name,'sha256':sha(out),'dimensions':list(board.size),'portrait_checks':checks,'manual_painting':False,'native_art_final_approved':False},'source_limitations':'Commercial native-reference pixels are excluded from delivery archives. Generated identity/style source references are retained.'})
print(json.dumps({'board':str(out),'size':board.size,'board_sha256':sha(out),'individuals':[x['delivery_file'] for x in selection]},ensure_ascii=False,indent=2))
