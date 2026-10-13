from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];out=Path(__file__).parent
im=Image.new('RGB',(1800,1600),'#f2eee5');d=ImageDraw.Draw(im);F=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
d.text((35,20),'妮尔 / 塞尔｜现行衣装侧背补设定',font=F(34),fill='#30323b');d.text((35,75),'新增4个静态视图 · 0新人 · 正面为原锚复用 · 旧比例已有背面，本轮更新现行比例',font=F(23),fill='#30323b')
for row,(c,name) in enumerate([('nell','妮尔'),('sel','塞尔')]):
 for col,(view,label) in enumerate([('front_anchor_reused','正面锚｜复用'),('left_side','身体左侧｜朝右'),('back','正背面｜结构推定')]):
  a=Image.open(R/c/'turnaround_v1/selected'/f'{c}_{view}.png').convert('RGBA');a=a.crop(a.getbbox());s=min(440/a.width,590/a.height);a=a.resize((round(a.width*s),round(a.height*s)),Image.Resampling.NEAREST);x=col*600+(600-a.width)//2;y=735+row*710-a.height;im.paste(a,(x,y),a);d.text((col*600+65,748+row*710),name+' · '+label,font=F(25),fill='#30323b')
d.text((35,1540),'短披肩/腰布分层；围裙后颈最小连接。未知结构为原创设计推定；非游戏动画或装备拆层。',font=F(22),fill='#30323b');im.save(out/'nell_sel_turnaround_joint_zh_light.png')
