from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent
slug=P.parent.name
selected={'dalan':2,'erlan':1}[slug]
raw=P/'raw'/f'{slug}_v{selected}_raw_imagegen.png'
i=Image.open(raw).convert('RGBA'); a=np.array(i);before=a.copy();mask=a[:,:,3]<=8;a[mask]=0
im=Image.fromarray(a);im.save(P/f'{slug}_transparent.png')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f=ImageFont.truetype(font,28);small=ImageFont.truetype(font,19)
name={'dalan':'妲兰 · FX-HRP','erlan':'珥兰 · FX-HNT'}[slug]
notes={'dalan':['三十出头女子 · 哈比巢下猎人','弓不拉弦 · 肩背箭囊 · 脸部旧痕','旧痕左右与终点仅本稿可逆提案'], 'erlan':['三十多岁女子 · 猎场设陷者','双腿皮护 · 后侧腰三根短木桩','目光向下 · 低手提醒「看脚下」']}[slug]
board=Image.new('RGB',(1500,1150),'#ede5d4'); d=ImageDraw.Draw(board);d.rectangle((750,0,1499,1149),fill='#242a2d')
scale=min(670/i.width,900/i.height);sz=(round(i.width*scale),round(i.height*scale));thumb=im.resize(sz,Image.Resampling.NEAREST)
for x,c in [(0,'#282925'),(750,'#eee9dd')]:
 d.text((x+30,20),name,font=f,fill=c);d.text((x+30,66),'单人全身概念 · '+('浅底' if x==0 else '深底'),font=small,fill=c)
 board.paste(thumb,(x+(750-sz[0])//2,108),thumb)
 for n,line in enumerate(notes):d.text((x+30,1030+n*30),line,font=small,fill=c)
board.save(P/f'{slug}_review_zh.png')
for color,label in [((239,231,214,255),'light'),((36,42,45,255),'dark')]:
 bg=Image.new('RGBA',i.size,color);bg.alpha_composite(i);bg.convert('RGB').save(P/'qa'/f'raw_selected_{label}.png')
report={'selected_raw':str(raw.relative_to(P)),'size':i.size,'raw_alpha_min':int(before[:,:,3].min()),'raw_alpha_max':int(before[:,:,3].max()),'raw_zero_alpha_pixels':int((before[:,:,3]==0).sum()),'raw_hidden_rgb_nonzero_pixels':int(((before[:,:,3]==0)&(before[:,:,:3]!=0).any(axis=2)).sum()),'cleared_alpha_1_to_8_pixels':int(((before[:,:,3]>0)&(before[:,:,3]<=8)).sum()),'preserved_alpha_gt8_rgba_exact':bool(np.array_equal(a[~mask],before[~mask])),'transparent_bbox':im.getbbox(),'method':'Only alpha<=8 and hidden RGB set to zero; no cropping, retouch, palette quantization, body drawing or nonuniform scaling. Board uses uniform nearest-neighbor display.'}
(P/'qa'/'alpha_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(slug,json.dumps(report))
