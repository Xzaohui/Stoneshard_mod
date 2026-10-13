from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[5]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
F=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
for char,name,ids,labels in [('tor','托雷',['D1_question','D2_weigh'],['空左手略摊质询','收掌权衡']),('rhea','蕾雅',['D1_remind','D2_resolve'],['空右掌轻示提醒','收回胸前坚定说明'])]:
 if char != Path(__file__).resolve().parent.parent.name: continue
 P=Path(__file__).resolve().parent
 source=ROOT/('Assets/CharacterDesigns/20261013/expressive/tor/period_costume_v2/tor_period_costume_v2_transparent.png' if char=='tor' else 'Assets/CharacterDesigns/20261013/expressive/rhea/rhea_raw_imagegen.png')
 shutil.copy2(source,P/'raw/D0_anchor_source.png')
 paths=[P/'raw/D0_anchor_source.png',*[P/f'raw/{k}.png' for k in ids]]
 frames=[];records=[];sole=None
 for i,src in enumerate(paths):
  a=np.array(Image.open(src).convert('RGBA'));rawsize=[a.shape[1],a.shape[0]]
  removed=int(((a[:,:,3]>0)&(a[:,:,3]<128)).sum());a[:,:,3]=np.where(a[:,:,3]>=128,255,0).astype('uint8');a[a[:,:,3]==0,:3]=0
  clean=Image.fromarray(a);bbox=clean.getbbox()
  if sole is None:sole=bbox[3]
  dy=sole-bbox[3];im=Image.new('RGBA',clean.size);im.alpha_composite(clean,(0,dy))
  key='D0_stand' if i==0 else ids[i-1];out=P/f'frames/{key}.png';im.save(out);frames.append(im)
  records.append(dict(id=key,new_drawing=i>0,source=str(src.relative_to(ROOT)),source_sha256=sha(src),frame_sha256=sha(out),raw_size=rawsize,raw_clean_bbox=bbox,scale=1.0,translation=[0,dy],visible_bbox=im.getbbox(),low_alpha_pixels_removed=removed,transparent_rgb_nonzero=int(np.count_nonzero(np.array(im)[np.array(im)[:,:,3]==0,:3]))))
 shutil.copy2(P/'frames/D0_stand.png',P/'frames/D3_stand_reuse_D0.png');frames.append(frames[0].copy());records.append(dict(id='D3_stand_reuse_D0',new_drawing=False,source='frames/D0_stand.png',frame_sha256=sha(P/'frames/D3_stand_reuse_D0.png'),byte_identical_to_D0=True))
 # A common 1/4 nearest-neighbor preview scale applies equally to every source; no per-frame stretching.
 thumbs=[im.resize((round(im.width/4),round(im.height/4)),Image.Resampling.NEAREST) for im in frames]
 for theme,col,fg in [('light',(239,237,227),'#292b31'),('dark',(39,43,51),'#f0eee7')]:
  board=Image.new('RGB',(1600,560),col);d=ImageDraw.Draw(board)
  d.text((25,15),f'{name}｜对话动作四阶段｜3个不同身体状态，2张新绘',font=F(29),fill=fg)
  for i,(im,label) in enumerate(zip(thumbs,['D0 原站姿复用',f'D1 {labels[0]}',f'D2 {labels[1]}','D3 复用D0回稳'])):
   board.paste(im,(i*400+(400-im.width)//2,75),im);d.text((i*400+18,445),label,font=F(21),fill=fg)
  d.text((25,497),'原比例1:1清理与鞋底平移；本板统一1/4最近邻缩放。四个稀疏姿态，不是补间动画。',font=F(22),fill=fg)
  board.save(P/f'previews/dialogue_{theme}.png')
  if theme=='light':light=board
  else:dark=board
 review=Image.new('RGB',(1600,1270),(239,237,227));review.paste(light,(0,0));review.paste(dark,(0,560));d=ImageDraw.Draw(review)
 d.text((25,1140),('右手始终持闭账本；左手为空，衣装保持直边无翻领。' if char=='tor' else '左臂始终抱普通卷毯，右手为空；卷毯不是婴儿。'),font=F(25),fill='#30353d')
 d.text((25,1190),'动作不写任务状态，不表示结案／逃离／免责；沿用概念锚，未声称用户逐人批准。',font=F(24),fill='#30353d')
 review.save(P/'dialogue_gesture_review_zh.png')
 gif=[]
 for im in frames:
  im=im.resize((round(im.width/2),round(im.height/2)),Image.Resampling.NEAREST);bg=Image.new('RGB',im.size,(39,43,51));bg.paste(im,(0,0),im);gif.append(bg)
 gif[0].save(P/'dialogue_gesture_once.gif',save_all=True,append_images=gif[1:],duration=[750,1000,1000,900],disposal=2,optimize=False)
 strip=Image.new('RGBA',(frames[0].width*4,frames[0].height))
 for i,im in enumerate(frames):strip.alpha_composite(im,(im.width*i,0))
 strip.save(P/'dialogue_gesture_transparent_strip.png')
 limitations=['四个稀疏关键姿态，不是连续补间或原生动画','衣褶、轮廓边缘和鞋型有细小生成漂移，未逐帧重绘修正','共同比例与鞋底地线不等于骨长、脚轨迹已锁定','未做原生尺寸、碰撞、装备换装或游戏运行验收']
 m=dict(status='awaiting_independent_review',character=char,character_zh=name,tool='builtin imagegen',classification='original_fullbody_dialogue_keypose_concept',new_characters=0,new_body_images=2,unique_body_states=3,phase_count=4,anchor=str(source.relative_to(ROOT)),anchor_sha256=sha(source),common_scale=1.0,processing='alpha threshold128; transparent RGB zero; common scale 1.0; sole-only vertical translation; no body construction/mirror/warp/interpolation',canvas=list(frames[0].size),sole_baseline=sole,frames=records,gif_duration_ms=[750,1000,1000,900],gif_loop_extension=False,narrative_sources=['design/04_人物/人物_玛拉与伊沃.md','design/05_主线/台本/台本_N1_无钟之夜.md'],runtime_verified=False,native_ready=False,user_individual_character_approval_claimed=False,limitations=limitations)
 (P/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 qa=dict(status='author_visual_check_pass_pending_independent_review',checked_images=['raw/D0_anchor_source.png',*[f'raw/{k}.png' for k in ids],'dialogue_gesture_review_zh.png'],checks={'identity_and_head_body_ratio_retained':True,'actual_arm_pose_changes':True,'two_new_fullbody_images':True,'feet_visible_and_planted':True,'original_prop_continuity':True,'no_new_props_or_people':True,'no_weapon_draw':True,'D0_D3_byte_identical':sha(P/'frames/D0_stand.png')==sha(P/'frames/D3_stand_reuse_D0.png'),'no_loop_extension':'loop' not in Image.open(P/'dialogue_gesture_once.gif').info,'four_gif_frames':Image.open(P/'dialogue_gesture_once.gif').n_frames==4,'transparent_rgb_zero':all(r.get('transparent_rgb_nonzero',0)==0 for r in records)},limitations=limitations)
 (P/'QA-author.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
 (P/'README.md').write_text(f'# {name}：对话动作 v1\n\n原站姿 → {labels[0]} → {labels[1]} → 原站姿。共4展示阶段、3不同身体状态、2新绘、0新人物。\n\n使用builtin imagegen，提示词在prompts；raw完整原始输出及锚副本不改写。透明导出仅alpha清理、透明RGB归零、共同1:1比例、按鞋底垂直平移。首末PNG字节相同。GIF单次播放无loop扩展。\n\n中文板和previews双底供目检；作者检查不代替独立审查或用户逐人批准。没有上传或封包，没有修改runtime。\n\n本图只表现对白姿态，询问／意向不代表结案、免责、逃离或任何N1路线提交。\n\n'+ '\n'.join('- '+s for s in limitations)+'\n')
 (P/'spec_lock.md').write_text(f'# {name} 对话动作约束\n\n沿用manifest指定的现行概念锚的全身、头身、神态与衣装。{labels[0]} → {labels[1]}。\n'+('左手空手，右手闭账本不打开；直边衣装不回西装领，禁止新增道具或裁决。' if char=='tor' else '左臂抱普通卷毯，右手空手；不抱送任何人、不代表撤离成功。')+'\n单次4阶段，首末复用；不以姿态表示结案、逃离、免责。\n')
 hashes={str(p.relative_to(P)):sha(p) for p in sorted(P.rglob('*')) if p.is_file() and p.name!='SHA256.json'}
 (P/'SHA256.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n')
 print(char,qa['checks'])
