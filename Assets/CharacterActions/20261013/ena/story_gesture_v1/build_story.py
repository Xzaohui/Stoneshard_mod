from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();F=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
for c,name,keys,labels in [('nara','纳拉',['D1_seated_boundary_round2','D2_seated_explanation'],['坐姿抬掌拒绝代签','坐着说明能力范围']),('ena','灰堤艾娜',['D1_coat_guard','D2_limited_advocacy_round2'],['抱紧外套等待','低掌阻止越权'])]:
 p=R/f'Assets/CharacterActions/20261013/{c}/story_gesture_v1';anchor=R/f'Assets/CharacterDesigns/20261013/expressive/{c}/{c}_v2_raw_imagegen.png';shutil.copy2(anchor,p/'raw/D0_anchor_source.png');frames=[];rec=[]
 for i,k in enumerate(['D0_anchor_source',*keys]):
  src=p/f'raw/{k}.png';a=np.array(Image.open(src).convert('RGBA')); removed=int(((a[:,:,3]>0)&(a[:,:,3]<128)).sum());a[:,:,3]=np.where(a[:,:,3]>=128,255,0).astype('uint8');a[a[:,:,3]==0,:3]=0;im=Image.fromarray(a);bb=im.getbbox()
  # Translate the complete raster only. Match the midpoint between the outer boot silhouettes in the bottom 100 pixels.
  ys,xs=np.where(a[max(bb[3]-100,0):bb[3],:,3]>0);cx=(int(xs.min())+int(xs.max())+1)//2;dx=600-cx;dy=1450-bb[3];out=Image.new('RGBA',(1200,1600));out.alpha_composite(im,(dx,dy));fid='D0_anchor' if i==0 else ('D1_boundary' if i==1 else 'D2_explanation');fp=p/f'frames/{fid}.png';out.save(fp);frames.append(out);rec.append(dict(id=fid,new_drawing=i>0,raw=str(src.relative_to(R)),raw_sha256=sha(src),raw_size=list(im.size),source_bbox=list(bb),common_scale=1,translation=[dx,dy],alpha_threshold=128,low_alpha_removed=removed,output=str(fp.relative_to(R)),sha256=sha(fp),bbox=list(out.getbbox())))
 shutil.copy2(p/'frames/D0_anchor.png',p/'frames/D3_anchor_reuse.png');frames.append(frames[0].copy());rec.append(dict(id='D3_anchor_reuse',new_drawing=False,byte_identical_to_D0=True,sha256=sha(p/'frames/D3_anchor_reuse.png')))
 boards=[]
 for theme,bg,fg in [('light',(240,237,227),(38,40,47)),('dark',(38,42,49),(242,238,226))]:
  b=Image.new('RGB',(1600,590),bg);d=ImageDraw.Draw(b);d.text((24,14),f'{name}｜剧情关键姿态｜2张新绘，首末复用原锚',font=F(28),fill=fg)
  for i,(im,label) in enumerate(zip(frames,['D0 原锚',f'D1 {labels[0]}',f'D2 {labels[1]}','D3 复用原锚'])):
   t=im.resize((300,400),Image.Resampling.NEAREST);b.paste(t,(i*400+50,66),t);d.text((i*400+18,480),label,font=F(23),fill=fg)
  d.text((24,538),'共同1:1比例与整图平移；本板统一1/4最近邻。稀疏示意，非连续补间动画。',font=F(23),fill=fg);b.save(p/f'previews/story_{theme}.png');boards.append(b)
 board=Image.new('RGB',(1600,1340),(240,237,227));board.paste(boards[0],(0,0));board.paste(boards[1],(0,590));d=ImageDraw.Draw(board)
 d.text((24,1200),'坐姿、原凳与伤腿夹板保留；靴形/凳形仍有生成漂移，精确接地点未锁。' if c=='nara' else '同一灰堤艾娜；外套有衣襟与袖口，非裹尸布。边缘及比例仍有细小漂移。',font=F(25),fill=(38,40,47))
 d.text((24,1250),'只表现当下说话与边界；不代表签署、返营、死亡、赔付或任何任务结案。',font=F(24),fill=(38,40,47));board.save(p/'story_gesture_review_zh.png')
 gs=[]
 for im in frames:
  im=im.resize((600,800),Image.Resampling.NEAREST);bg=Image.new('RGB',im.size,(38,42,49));bg.paste(im,(0,0),im);gs.append(bg)
 gs[0].save(p/'story_gesture_once.gif',save_all=True,append_images=gs[1:],duration=[800,1100,1100,900],disposal=2,optimize=False)
 strip=Image.new('RGBA',(4800,1600))
 for i,im in enumerate(frames):strip.alpha_composite(im,(i*1200,0))
 strip.save(p/'story_gesture_transparent_strip.png');brief=json.loads((p/'source_brief.json').read_text())
 limitations=['4阶段、3种不同状态、2张新绘，不是完整连续动画','按整图平移统一底线，未独立缩放、拉伸或拼接身体','生成稿仍有衣褶、靴形和轮廓漂移；非原生精灵或游戏运行验收']
 if c=='nara':limitations.append('靴与凳的逐像素接地点未与原锚完全固定，须独审判断是否需进一步重绘；不声称硬锁通过')
 m=dict(status='awaiting_independent_review',canonical_id=brief['canonical_id'],name=name,tool='builtin imagegen',new_characters=0,new_key_poses=2,unique_states=3,phases=4,anchor=brief['current_anchor'],source_brief_sha256=sha(p/'source_brief.json'),source_cards=brief['source_cards'],story_sources=brief['related_main_scripts'],story_boundaries=brief['story_boundaries'],raw_rounds={'selected':keys,'superseded':['D1_seated_boundary'] if c=='nara' else ['D2_limited_advocacy']},processing='Only alpha threshold 128, RGB zero for alpha zero, common scale 1.0, complete-raster x/y translation, shared nearest preview reduction and board/GIF assembly. No body drawing/warping/compositing.',canvas=[1200,1600],frames=rec,gif_duration_ms=[800,1100,1100,900],gif_loop_extension=False,runtime_integrated=False,roster_modified=False,limitations=limitations)
 (p/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 (p/'README.md').write_text(f'# {name} 剧情动作 v1\n\n2新关键姿态、0新人，D0和D3复用原锚。原始输出与退选版本均保留，完整提示词见prompts，输入来源见source_brief和manifest。\n\n待独立视觉审查，作者不替代独审。未上传、未封最终包、未改roster或runtime。\n\n'+'\n'.join('- '+s for s in limitations)+'\n')
 shutil.copy2('/tmp/build_story.py',p/'build_story.py')
 print(c,[r.get('bbox') for r in rec])
