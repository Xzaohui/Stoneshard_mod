#!/usr/bin/env python3
"""Copy frozen candidates and compose a board; never modify portrait pixels."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,hashlib,shutil
D=Path(__file__).resolve().parent;R=D.parent.parent
ORDER=['tio','kaino'];NAMES={'tio':'提奥','kaino':'凯诺'}
LIMITS={'tio':'颈仍稍长、发线偏细；仅为技术派生候选','kaino':'肤色稍暖；只选 70×96 safe 技术导出'}
ROLES={'tio':'二十多岁 · 酿酒学徒','kaino':'五十岁上下 · 箍桶工'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
F=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');B=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
font=lambda s,b=False:ImageFont.truetype(str(B if b else F),s)
gate=json.loads((D/'freeze_gate.json').read_text());assert gate['approved_to_package'] is True
assert gate['qualified_candidate_count']==2 and gate['held_count']==2
for rel,h in gate['qa_files'].items():assert sha(R/'independent_qa/batch30'/rel)==h,rel
selection=[]
for c in ORDER:
 m=json.loads((R/c/'manifest.json').read_text());source=R/c/m['selected_portrait'];h=sha(source)
 ref=next(x for x in gate['characters'] if x['slug']==c)
 assert (R/ref['selected_portrait']).resolve()==source.resolve() and ref['selected_sha256']==h
 assert sha(R/c/'manifest.json')==ref['production_manifest_sha256']
 im=Image.open(source).convert('RGBA');assert im.size==(74,100)
 alpha=sorted(set(im.getchannel('A').getdata()));assert set(alpha)<={0,255}
 colors=len(set(px[:3] for px in im.getdata() if px[3]));assert colors<=32
 out=D/f'{c.upper()}_{NAMES[c]}_74x100_candidate.png'
 if out.exists():assert sha(out)==h,'Refuse replacing a differing delivery copy'
 else:shutil.copyfile(source,out)
 assert sha(out)==h
 selection.append({'actor':c,'name':NAMES[c],'source':source.relative_to(R).as_posix(),'source_sha256':h,'delivery_file':out.name,'delivery_sha256':sha(out),'dimensions':[74,100],'visible_rgb_colors':colors,'alpha_values':alpha,'selected_version':source.name.split('_74x100')[0],'derivation_metrics':f'{c}/qa/{source.name.split("_74x100")[0]}_metrics.json','quantization':'MAXCOVERAGE','limitations':LIMITS[c],'native_authored':False,'runtime_integrated':False,'runtime_verified':False})
W,HEADER,ROW,HELD,FOOT=680,154,466,180,166
board=Image.new('RGB',(W,HEADER+ROW*2+HELD+FOOT),(22,24,28));draw=ImageDraw.Draw(board)
text=(237,230,216);muted=(180,178,174);accent=(217,183,130)
draw.text((28,21),'头像重绘 · 第三十批 2 人',font=font(32,True),fill=text)
draw.text((28,71),'原尺寸 74×100  +  4 倍最近邻放大',font=font(23),fill=accent)
draw.text((28,110),'2026.10.15  ·  冻结候选  ·  赛芙、布泽暂缓，不计成功',font=font(19),fill=muted)
checks=[]
for i,item in enumerate(selection):
 c=item['actor'];y=HEADER+i*ROW;bg=(31,32,37) if i%2==0 else (26,28,32)
 draw.rectangle((16,y,663,y+ROW-12),fill=bg)
 draw.text((36,y+24),f'{i+1:02d}  {NAMES[c]}',font=font(30,True),fill=text)
 draw.text((36,y+73),c.upper(),font=font(20),fill=accent)
 draw.text((36,y+102),ROLES[c],font=font(16),fill=muted)
 draw.text((36,y+130),'原尺寸 1×',font=font(19),fill=muted)
 im=Image.open(D/item['delivery_file']).convert('RGBA')
 for scale,x,yy in [(1,87,y+172),(4,328,y+15)]:
  src=im if scale==1 else im.resize((74*scale,100*scale),Image.Resampling.NEAREST)
  board.paste(src,(x,yy),src);expect=Image.new('RGB',src.size,bg);expect.paste(src,(0,0),src)
  assert board.crop((x,yy,x+src.width,yy+src.height)).tobytes()==expect.tobytes()
  checks.append({'actor':c,'scale':scale,'resampling':'NEAREST' if scale>1 else 'none','box':[x,yy,x+src.width,yy+src.height],'composited_pixels_exact':True})
 draw.text((36,y+288),'74 × 100 PNG',font=font(18),fill=muted)
 draw.text((36,y+319),f'{item["visible_rgb_colors"]} 色 · 透明底',font=font(18),fill=muted)
 draw.text((36,y+416),LIMITS[c],font=font(19),fill=muted)
y=HEADER+ROW*2
draw.rectangle((16,y,663,y+HELD-12),fill=(46,34,31))
draw.text((32,y+18),'暂缓 · 赛芙 SAIFU / 布泽 BUZE',font=font(26,True),fill=(236,183,153))
draw.text((32,y+61),'赛芙：紧脸短颈、暗眼与谨慎表情未达标。',font=font(22),fill=text)
draw.text((32,y+101),'布泽：眼白偏亮，裸颈衣领占幅；风格暂缓。',font=font(20),fill=muted)
draw.text((32,y+136),'两人各版原始稿、完整回包与失败记录在源包 B。',font=font(19),fill=muted)
y+=HELD
draw.text((28,y+11),'高分辨率生图经最近邻缩放与无抖动量化。',font=font(21),fill=text)
draw.text((28,y+47),'非原生手工逐像素终稿；尚未集成或实机验证。',font=font(21),fill=text)
draw.text((28,y+88),'32 色为临时技术上限；透明留边不补回未知内容。',font=font(18),fill=muted)
draw.text((28,y+123),'原始生图、提示词、工具返回、来源与 QA 随源包保留。',font=font(18),fill=muted)
out=D/'batch30_两人头像总览_1x_4x.png';board.save(out,optimize=True)
js(D/'selected_delivery_manifest.json',{'batch':'30','date':'2026-10-15','qualified_candidate_count':2,'held_count':2,'characters':selection,'held':gate['held'],'board':{'file':out.name,'sha256':sha(out),'dimensions':list(board.size),'portrait_checks':checks,'manual_painting':False,'native_art_final_approved':False,'held_portrait_not_displayed':True},'source_limitations':'Commercial native-reference pixels are excluded. All four generated production folders, including held saifu and buze evidence, are retained; held is not counted as success.'})
print(json.dumps({'board':str(out),'size':board.size,'board_sha256':sha(out),'individuals':[x['delivery_file'] for x in selection]},ensure_ascii=False,indent=2))
