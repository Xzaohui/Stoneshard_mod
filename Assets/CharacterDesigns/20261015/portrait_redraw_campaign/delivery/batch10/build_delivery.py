#!/usr/bin/env python3
"""Layout/copy/verify frozen candidates only. Does not draw or alter portrait pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,hashlib,shutil,sys
D=Path(__file__).resolve().parent
R=D.parent.parent
ORDER=['vit','wolen','yani','rukan']
NAMES={'vit':'薇特·灰','wolen':'沃伦','yani':'雅尼','rukan':'鲁坎'}
LIMITS={'vit':'少量平行发亮条与单像素过渡；左右仅 1 像素余量','wolen':'发须细亮条仍稍多；保留分瓣须与裸下巴','yani':'等比留边不补画；窄领偏暖，脸须层次略平','rukan':'等比留边不补画；窄领偏暖，脸须层次略平'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
F=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
B=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
font=lambda s,b=False:ImageFont.truetype(str(B if b else F),s)
selection=[]
gate=json.loads((D/'freeze_gate.json').read_text()); assert gate['approved_to_package'] is True
final_path=R/gate['selection_file']; assert sha(final_path)==gate['selection_sha256']
final=json.loads(final_path.read_text())
comparison=[dict(x,selected_portrait=x['selected_candidate']) for x in final['characters']]
independent_gate=json.loads((R/gate['independent_gate_file']).read_text()); assert independent_gate['candidate_delivery_pass'] and independent_gate['all_technical_checks_complete'] and not independent_gate['hard_errors'] and not independent_gate['pending']; assert sha(R/gate['independent_gate_file'])==gate['independent_gate_sha256']
for c in ORDER:
 m=json.loads((R/c/'manifest.json').read_text())
 source=R/c/m.get('selected_portrait',m.get('selected_candidate')); h=sha(source)
 independent=next(x for x in comparison if x['slug']==c)
 assert (R/independent['selected_portrait']).resolve()==source.resolve() and independent['selected_sha256']==h,c
 assert sha(R/c/'manifest.json')==independent['production_manifest_sha256']
 im=Image.open(source); assert im.size==(74,100),c
 rgba=im.convert('RGBA'); alpha=set(rgba.getchannel('A').getdata()); assert alpha<={0,255}
 colors=len(set(px[:3] for px in rgba.getdata() if px[3])); assert colors<=32
 out=D/f'{c.upper()}_{NAMES[c]}_74x100_candidate.png'
 if out.exists(): assert sha(out)==h, 'Refuse replacing a differing delivery copy'
 else: shutil.copyfile(source,out)
 assert sha(out)==h
 selection.append({'actor':c,'name':NAMES[c],'source':source.relative_to(R).as_posix(),'source_sha256':h,'delivery_file':out.name,'delivery_sha256':sha(out),'dimensions':[74,100],'visible_rgb_colors':colors,'alpha_values':sorted(alpha),'selected_version':source.name.split('_74x100')[0],'resize':[72,97] if '_containment_' in source.name else [74,100],'paste_offset':[1,1] if '_containment_' in source.name else [0,0],'quantization':'MEDIANCUT' if '_mediancut_' in source.name else ('MAXCOVERAGE' if any(x in source.name for x in ['_maxcoverage_','_containment_']) else 'MEDIANCUT'),'limitations':LIMITS[c],'native_authored':False,'runtime_integrated':False,'runtime_verified':False})
# The board uses intact source pixels at 1x and integer 4x nearest-neighbor only.
W,HEADER,ROW,FOOT=680,154,466,166
board=Image.new('RGB',(W,HEADER+ROW*4+FOOT),(22,24,28)); draw=ImageDraw.Draw(board)
text=(237,230,216); muted=(180,178,174); accent=(217,183,130)
draw.text((28,21),'头像重绘 · 第十批 4 人',font=font(32,True),fill=text)
draw.text((28,71),'原尺寸 74×100  +  4 倍最近邻放大',font=font(23),fill=accent)
draw.text((28,110),'2026.10.15  ·  冻结候选  ·  仅排版，不补画',font=font(19),fill=muted)
checks=[]
for i,item in enumerate(selection):
 c=item['actor']; y=HEADER+i*ROW; bg=(31,32,37) if i%2==0 else (26,28,32)
 draw.rectangle((16,y,663,y+ROW-12),fill=bg)
 draw.text((36,y+24),f'{i+1:02d}  {NAMES[c]}',font=font(30,True),fill=text)
 draw.text((36,y+73),c.upper(),font=font(20),fill=accent)
 draw.text((36,y+102),{'vit':'女 · 五十多岁退役值夜者','wolen':'男 · 五十岁副工场修铆师傅','yani':'男 · 三十多岁成年退役者','rukan':'男 · 四十多岁灰堤领班'}[c],font=font(16),fill=muted)
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
draw.text((28,y+88),'雅尼、鲁坎：等比留边只改善派生边距，不补画。',font=font(18),fill=muted)
draw.text((28,y+123),'原始生图、提示词、工具返回、来源与 QA 随源包保留。',font=font(18),fill=muted)
out=D/'batch10_四人头像总览_1x_4x.png'
board.save(out,optimize=True)
js(D/'selected_delivery_manifest.json',{'batch':'10','date':'2026-10-15','characters':selection,'board':{'file':out.name,'sha256':sha(out),'dimensions':list(board.size),'portrait_checks':checks,'manual_painting':False,'native_art_final_approved':False},'source_limitations':'Commercial native-reference pixels are excluded from delivery archives. Generated identity/style source references are retained.'})
print(json.dumps({'board':str(out),'size':board.size,'board_sha256':sha(out),'individuals':[x['delivery_file'] for x in selection]},ensure_ascii=False,indent=2))
