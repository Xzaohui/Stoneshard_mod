from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import json,hashlib,shutil
D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=D/'QA-independent.json'; assert sha(q)=='0db0e4c10872bfbdcc349967d82a489c18f2dd975e7ed18065d822db881abf04'
S=D/'pre_text_correction';S.mkdir(exist_ok=True)
for n in ['manifest.json','belo_review_zh_light.png','belo_review_zh_dark.png','build_review.py']:
 if not (S/n).exists():shutil.copy2(D/n,S/n)
f=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
checks={}
for theme,bg,fg in [('light','#efeade','#282828'),('dark','#252a30','#efe8d6')]:
 name=f'belo_review_zh_{theme}.png';old=Image.open(S/name).convert('RGB');im=old.copy();dr=ImageDraw.Draw(im);dr.rectangle((0,0,1229,145),fill=bg)
 dr.text((25,16),'贝洛 · 抬箍检查箍缘',font=f(29),fill=fg);dr.text((25,60),'1 张新姿态 · 原锚首末复用 · 人物基础动作概念',font=f(19),fill=fg)
 for n,t in enumerate(['原锚 · 体侧持箍','抬箍检查箍缘','原锚复用 · 结束示意']):dr.text((n*410+25,105),t,font=f(21),fill=fg)
 assert ImageChops.difference(old.crop((0,146,1230,820)),im.crop((0,146,1230,820))).getbbox() is None
 im.save(D/name);checks[name]={'all_pixels_y146_through819_unchanged':True,'sha256':sha(D/name)}
# Only presentation text changes; figures, raw files, frames and prior reviews stay untouched.
p=D/'build_review.py';s=p.read_text().replace('抬箍触检内缘','抬箍检查箍缘');p.write_text(s)
frames=[]
for n,(name,t) in enumerate([('00_anchor.png','原锚 · 体侧持箍'),('01_B1.png','抬箍检查箍缘'),('02_anchor.png','原锚 · 体侧持箍')]):
 c=Image.new('RGB',(410,750),'#efeade');d=ImageDraw.Draw(c);d.text((18,12),'贝洛 · 箍缘检查',font=f(23),fill='#282828');d.text((18,46),t,font=f(18),fill='#282828');im=Image.open(D/'frames'/name);c.paste(im,(0,70),im);d.text((18,716),'稀疏姿态示意 · 非连续动画',font=f(16),fill='#282828');frames.append(c)
# Shared palette, no loop extension: a single traversal with anchor at both ends.
sheet=Image.new('RGB',(410,2250))
for i,im in enumerate(frames):sheet.paste(im,(0,750*i))
pal=sheet.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
indexed=[pal.crop((0,750*i,410,750*(i+1))) for i in range(3)]
g=D/'belo_hoop_edge_check_sparse_once.gif';indexed[0].save(g,save_all=True,append_images=indexed[1:],duration=[1100,1800,1100],disposal=2,optimize=False)
i=Image.open(g);assert i.n_frames==3 and 'loop' not in i.info;i.seek(0);first=i.convert('RGB').copy();i.seek(2);assert ImageChops.difference(first,i.convert('RGB')).getbbox() is None
status={'status':'text_corrected_and_single_pass_gif_created_pending_delta_review','source_independent_qa_sha256':sha(q),'correction':'抬箍触检内缘 → 抬箍检查箍缘；指腹实际触前/外缘','images_unchanged':checks,'raw_and_transparent_frames_unchanged':True,'gif':{'path':g.name,'bytes':g.stat().st_size,'sha256':sha(g),'frame_count':3,'loop_extension':False,'durations_ms':[1100,1800,1100],'first_last_pixels_equal':True,'description':'原锚→新姿→原锚的单次稀疏关键姿态，不是连续触检动画'},'previous_reviews_preserved':True,'runtime_integrated':False}
(D/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
m=json.loads((S/'manifest.json').read_text());m.update({'status':'independent_visual_pass_text_corrected_gif_pending_delta_review','action_title':'抬箍检查箍缘','gif_created':True,'gif_gate':'独审允许制作，产物已做3帧/无loop/首尾一致检查；待独审增量核验','delta_record':'FINAL_STATUS.json','independent_review':{'path':'QA-independent.json','sha256':sha(q)}});m['files']=[{'path':str(p.relative_to(D)),'sha256':sha(p)} for p in sorted(D.rglob('*')) if p.is_file() and p!=D/'manifest.json'];(D/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(status,ensure_ascii=False))
