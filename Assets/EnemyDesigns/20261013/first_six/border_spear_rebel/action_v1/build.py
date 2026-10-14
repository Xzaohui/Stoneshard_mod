from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
ROOT=Path(__file__).resolve().parent
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def savej(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
poses=['spear_ready','spear_short_thrust']; reports=[]
for pose in poses:
 d=ROOT/pose; raw=d/f'border_spear_rebel_{pose}_v2_raw_imagegen.png'; dst=d/f'border_spear_rebel_{pose}_transparent.png'
 im=Image.open(raw).convert('RGBA'); a=np.array(im); b=a.copy();b[a[:,:,3]<=8]=0;Image.fromarray(b).save(dst)
 r={'pose_id':pose,'raw_sha256':SHA(raw),'transparent_sha256':SHA(dst),'size':list(im.size),'raw_alpha_min':int(a[:,:,3].min()),'raw_alpha_max':int(a[:,:,3].max()),'raw_alpha_zero':int((a[:,:,3]==0).sum()),'raw_low_alpha_1_to_8':int(((a[:,:,3]>0)&(a[:,:,3]<=8)).sum()),'all_raw_alpha_gt8_RGBA_unchanged':bool(np.array_equal(a[a[:,:,3]>8],b[a[:,:,3]>8])),'hidden_rgb_zeroed':True,'transparent_bbox':list(Image.fromarray(b).getbbox()),'processing':'Only RGBA zero where alpha<=8. All alpha>8 pixels byte-for-byte unchanged. No redraw, palette quantization, rescale or crop of transparent masters.'}; savej(d/'alpha_QA.json',r);reports.append(r)
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; f=ImageFont.truetype(font,28);small=ImageFont.truetype(font,23)
items=[(ROOT/'sources/border_spear_rebel_transparent.png','静态母图｜已独审通过',280,1520,0,500),(ROOT/'spear_ready/border_spear_rebel_spear_ready_transparent.png','预备 v2｜替代握法待独审',45,980,500,950),(ROOT/'spear_short_thrust/border_spear_rebel_spear_short_thrust_transparent.png','短直刺 v2｜替代握法待独审',50,947,1450,950)]
for name,bg,fg in [('light',(231,227,214,255),(36,35,32)),('dark',(28,33,39,255),(235,234,227))]:
 board=Image.new('RGBA',(2400,1050),bg);draw=ImageDraw.Draw(board)
 draw.text((35,20),'001 边地长矛手｜两个独立关键姿势研究',font=f,fill=fg)
 draw.text((35,65),'按人物发顶—靴底近似等比对齐；非统一游戏网格。长矛及身体未拉伸。',font=small,fill=fg)
 draw.text((35,102),'H1前握／H2后握为自然替代提案；不冒称原brief后握通过。无帧序、运行或连续性承诺。',font=small,fill=fg)
 for path,label,crown,sole,x,w in items:
  im=Image.open(path).convert('RGBA');scale=600/(sole-crown);out=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);xx=x+(w-out.width)//2;yy=round(910-sole*scale);board.alpha_composite(out,(xx,yy));draw.text((x+25,142),label,font=f,fill=fg)
 draw.text((35,988),'比较重点：脸衣左右、双手握持、矛头与金属尾端、双脚承重，以及前送幅度。',font=small,fill=fg)
 board.convert('RGB').save(ROOT/f'border_spear_rebel_action_{name}_board.png')
savej(ROOT/'alpha_QA.json',reports)
print(json.dumps(reports,ensure_ascii=False,indent=2))
