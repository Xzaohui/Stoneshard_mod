from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); BR=R/'Assets/CharacterDesigns/20261013/expressive/briefs/town_work_pose_candidates_01.json'; brief=json.loads(BR.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
for slug,ids,labels in [('emo',['E1','E2'],['原锚：持衬布','轻展一折察边','指腹压回原折边','返回原锚']),('geli',['G1'],['原锚：持小木试片','轻转察原曲率','返回原锚'])]:
 c=next(x for x in brief['characters'] if x['slug']==slug); D=R/'Assets/CharacterActions/20261013'/slug/c['branch_proposal']
 shutil.copy2(R/c['current_anchor']['path'],D/'raw/anchor.png')
 raws=[D/'raw/anchor.png']+[D/f'raw/{x}_imagegen.png' for x in ids]
 transforms=[]; frames=[]
 for i,p in enumerate(raws):
  im=Image.open(p).convert('RGBA'); a=im.getchannel('A'); a=a.point(lambda x:0 if x<=8 else x); im.putalpha(a); bb=a.getbbox()
  # Allowed presentation only: fixed common 1/2 nearest scale and whole-frame foot alignment. Never resculpt or stretch anatomy.
  im=im.resize((im.width//2,im.height//2),Image.Resampling.NEAREST); b=im.getchannel('A').getbbox(); pos=(320-(b[0]+b[2])//2,730-b[3]); canvas=Image.new('RGBA',(640,780));canvas.alpha_composite(im,pos); out=D/f'frames/{i:02d}_{"anchor" if i==0 else ids[i-1]}.png';canvas.save(out);frames.append(canvas)
  transforms.append({'input':str(p.relative_to(R)),'input_sha256':sha(p),'original_size':list(Image.open(p).size),'alpha_bbox':list(bb),'alpha_cleanup':'alpha <= 8 made transparent; RGB and remaining alpha untouched','common_scale':0.5,'interpolation':'nearest','translation_xy':list(pos),'foot_baseline':730,'output':str(out.relative_to(R)),'output_sha256':sha(out)})
 frames.append(frames[0].copy());shutil.copy2(D/'frames/00_anchor.png',D/f'frames/{len(frames)-1:02d}_return_anchor.png')
 title=f'{c["name"]}｜职业基础动作候选'
 for theme,bg,fg in [('light',(239,234,221),(44,40,36)),('dark',(39,43,49),(237,232,218))]:
  board=Image.new('RGB',(640*len(frames),880),bg);dr=ImageDraw.Draw(board);dr.text((28,18),title,font=ImageFont.truetype(font,30),fill=fg)
  dr.text((28,60),'独立姿态与稀疏阶段示意 · 非工序完成、非技术认证、非游戏落地',font=ImageFont.truetype(font,22),fill=fg)
  for j,im in enumerate(frames):
   board.paste(im,(j*640,80),im);dr.text((j*640+28,826),f'{j+1:02d}  {labels[j]}',font=ImageFont.truetype(font,24),fill=fg)
  board.save(D/f'contact_sheet_{theme}.png')
 # Discrete sparse stages; omission of GIF loop extension means one playback only.
 gifs=[]
 for im in frames:
  bg=Image.new('RGBA',im.size,(239,234,221,255));bg.alpha_composite(im);gifs.append(bg.convert('RGB'))
 gifs[0].save(D/'stages_once.gif',save_all=True,append_images=gifs[1:],duration=[900]+[1200]*len(ids)+[900],disposal=2)
 qa={'status':'author_checked_pending_independent_review','pixels_inspected':['raw/anchor.png']+[f'raw/{x}_imagegen.png' for x in ids], 'identity':'逐张目检：脸型、发帽或辫、衣装及成年比例同系；低头带来颈部投影变化，未机械拉伸。','anatomy':'双手各有连贯前臂，未见多手；头脚完整。','prop_continuity':'通过作者目检：同一块小衬布，仅一折轻展开及指腹回压，未添针剪刀。' if slug=='emo' else '通过作者目检：一块小木试片两端均持握，抬转而非掰弯，无裂纹、弓弦或新器械。','notes':['这是稀疏阶段图，不是逐帧流畅动画。','生成重绘存在微小轮廓和衣褶变化，细像素概念并非原生精灵。','独审仍须复核持物尺寸、曲率或折层；若未通过，应停止GIF使用、保留静态候选。'],'story_boundary':c['story_forbidden']}
 (D/'QA-author.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
 m={'schema_version':1,'canonical_id':c['canonical_id'],'name':c['name'],'status':'candidate_pending_independent_review','generator':'builtin image_gen.imagegen','created_utc':'2026-10-13','source_brief':str(BR.relative_to(R)),'source_brief_sha256':sha(BR),'source_anchor':c['current_anchor'],'source_cards':c['source_cards'],'authorization':'Root dispatched 2 Emo new poses and 1 Geli new pose after user requested continuation of character actions and designs, without runtime work. Prior brief planning-only status is historical.','new_generated_pose_count':len(ids),'sequence':['anchor']+ids+['anchor'],'anchor_reuse':True,'transform_policy':'Only common nearest 0.5 scaling and whole-frame foot alignment / layout. No anatomy generation by scripts, stretching, inpainting, or morph interpolation.','frames':transforms,'gif':{'path':'stages_once.gif','single_play':True,'loop_extension':False,'author_prop_continuity':'pass_pending_independent_review','warning':'稀疏阶段切换，非连续运动或工序证明'},'prompts':[{'path':f'prompts/{x}.txt','sha256':sha(D/f'prompts/{x}.txt')} for x in ids],'author_qa':qa,'outputs':[]}
 for p in sorted(D.rglob('*')):
  if p.is_file() and p.name!='manifest.json':m['outputs'].append({'path':str(p.relative_to(D)),'sha256':sha(p)})
 (D/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 print(slug,sha(D/'manifest.json'))
 print('GIF frames',Image.open(D/'stages_once.gif').n_frames,'loop',Image.open(D/'stages_once.gif').info.get('loop','absent'))
