from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import json,hashlib,shutil
D=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();q=D/'QA-independent.json'
assert sha(q)=='a6413a9bef192b32f2e848be1894335a015685f0d7bda9ecb7894f90de7e46ac'
qa=json.loads(q.read_text())
for n,s in qa['artifacts'].items(): assert sha(D/n)==s
S=D/'pre_gif_review';S.mkdir(exist_ok=True);shutil.copy2(D/'manifest.json',S/'manifest.json')
f=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n);frames=[]
for name,title in [('00_anchor.png','原锚 · 提柄低提'),('01_K1.png','提柄不松、空手托底'),('02_K2.png','双手腹前低抱'),('03_anchor.png','原锚 · 提柄低提')]:
 c=Image.new('RGB',(410,750),'#efeade');d=ImageDraw.Draw(c);d.text((18,12),'奇恩 · 小闭箱换握',font=f(23),fill='#282828');d.text((18,46),title,font=f(18),fill='#282828');im=Image.open(D/'frames'/name);c.paste(im,(0,70),im);d.text((18,716),'稀疏姿态示意 · 非连续动画',font=f(16),fill='#282828');frames.append(c)
sheet=Image.new('RGB',(410,3000))
for i,im in enumerate(frames):sheet.paste(im,(0,750*i))
pal=sheet.quantize(colors=256,method=Image.Quantize.MEDIANCUT);indexed=[pal.crop((0,750*i,410,750*(i+1))) for i in range(4)];g=D/'kien_sample_box_regrip_sparse_once.gif';durations=[1100,1500,1500,1100]
indexed[0].save(g,save_all=True,append_images=indexed[1:],duration=durations,disposal=2,optimize=False)
i=Image.open(g);assert i.n_frames==4 and 'loop' not in i.info;first=i.convert('RGB').copy();observed=[]
for n in range(4):i.seek(n);observed.append(i.info['duration'])
assert observed==durations;assert ImageChops.difference(first,i.convert('RGB')).getbbox() is None
for n,s in qa['artifacts'].items(): assert sha(D/n)==s
status={'status':'single_pass_gif_created_pending_delta_review','source_independent_qa_sha256':sha(q),'pre_gif_manifest_sha256':sha(S/'manifest.json'),'raw_transparent_frames_boards_prompts_old_qa_unchanged':True,'gif':{'path':g.name,'bytes':g.stat().st_size,'sha256':sha(g),'frame_count':4,'loop_extension':False,'durations_ms':durations,'first_last_pixels_equal':True,'description':'原锚→K1→K2→原锚单次稀疏关键姿态'},'limitations':['箱厚/框宽仍有概念漂移，未锁定精确固定三维几何','非连续搬运动画、真实受力验证或游戏运行'],'runtime_integrated':False}
(D/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
m=json.loads((S/'manifest.json').read_text());m.update({'status':'independent_sparse_concept_pass_gif_pending_delta_review','gif_created':True,'gif_gate':'独审允许制作，产物已做4帧/无loop/时长/首尾相同检查；待增量复核','delta_record':'FINAL_STATUS.json','independent_review':{'path':'QA-independent.json','sha256':sha(q)},'limitations':status['limitations']});m['files']=[{'path':str(p.relative_to(D)),'sha256':sha(p)} for p in sorted(D.rglob('*')) if p.is_file() and p!=D/'manifest.json'];(D/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(json.dumps(status,ensure_ascii=False))
