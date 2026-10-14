from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np,shutil
R=Path.cwd();B=R/'Assets/EnemyDesigns/20261013/second_six'; b=json.loads((B/'action_continuation_brief_v1.json').read_text());out=B/'continuation_009_010_delivery_v1'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
F=lambda n:ImageFont.truetype(font,n)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
J=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
combined=[]
for i in b['items']:
 if not i['concept_id'].endswith(('009','010')):continue
 n=i['concept_id'][-3:];d=R/i['planned_output_directory'];raw=d/f"{i['slug']}_{i['pose_id']}_raw_v1.png"; im=Image.open(raw).convert('RGBA')
 # Layout-only padding, preserve every original RGBA byte. Never threshold spectral edges or change hidden RGB.
 pad=48;selected=d/f"{i['slug']}_{i['pose_id']}_transparent.png";s=Image.new('RGBA',(im.width+pad*2,im.height+pad*2));s.paste(im,(pad,pad));s.save(selected)
 a=np.asarray(im)[:,:,3]; rgb=np.asarray(im)[:,:,:3]; report={'raw_size':list(im.size),'selected_size':list(s.size),'alpha_zero_pixels':int((a==0).sum()),'partial_alpha_pixels':int(((a>0)&(a<255)).sum()),'alpha_zero_hidden_nonzero_rgb_pixels':int(((a==0)&np.any(rgb!=0,axis=2)).sum()),'alpha_bboxes_diagnostic_only':{str(t):Image.fromarray((a>=t).astype('uint8')*255).getbbox() for t in [1,16,64,128,240,254,255]},'cleanup':'None; hidden RGB and original alpha preserved. Uniform transparent canvas padding 48 px per side only.','raw_byte_rgba_preserved_inside_padding':np.array_equal(np.asarray(s)[pad:-pad,pad:-pad],np.asarray(im)),'alpha_edges_not_automatic_crop_failure':True}
 J(d/'alpha_evidence.json',report)
 for bg,c in [('light',(234,230,220,255)),('dark',(25,31,40,255))]:
  canvas=Image.new('RGBA',s.size,c);canvas.alpha_composite(s);canvas.convert('RGB').save(d/f'preview_{bg}_v1.png')
 refs=[R/x['snapshot_path'] for x in i['source_images']]+[selected]
 labels= ['现行母图','旧：肩外备斧','旧：低位收斧','新增：高位蓄劈'] if n=='009' else ['现行母图','旧：低剑盾防','旧：水平探剑','新增：屈肘收剑']
 # Approximate head-height normalization is for display only, not runtime anchors or body editing.
 heads=[310,282,302,252] if n=='009' else [194,200,203,203]
 target=88 if n=='009' else 78
 cw,ch=470,535; w,h=cw*4,ch*2+110
 board=Image.new('RGB',(w,h),(241,237,228));dr=ImageDraw.Draw(board)
 dr.text((22,10),f"{n} {i['working_name']}｜{i['label']}",font=F(30),fill=(30,35,42))
 dr.text((22,53),'关键阶段概念；非连续动画。按头部近似归一化，仅等比最近邻排版。',font=F(20),fill=(70,74,80))
 entries=[]
 for row,(bg,col,txt) in enumerate([('浅底',(234,230,220),(35,39,45)),('深底',(25,31,40),(225,230,236))]):
  for k,(p,label,hh) in enumerate(zip(refs,labels,heads)):
   x=k*cw;y=95+row*ch;dr.rectangle((x,y,x+cw-1,y+ch-1),fill=col);dr.text((x+15,y+10),label+' · '+bg,font=F(23),fill=txt)
   obj=Image.open(p).convert('RGBA');scale=target/hh;nsize=(round(obj.width*scale),round(obj.height*scale));obj=obj.resize(nsize,Image.Resampling.NEAREST)
   # Whole PNG is kept, including transparent field; no crop of old image pixels.
   pos=(x+(cw-nsize[0])//2,y+62+(ch-78-nsize[1])//2)
   board.paste(obj,pos,obj)
   entries.append({'path':str(p.relative_to(R)),'sha256':sha(p),'label':label,'background':bg,'uniform_display_scale':scale,'display_size':nsize,'position':pos,'approx_reference_head_height_px':hh})
 board.save(d/'adjacent_light_dark_zh.png');combined.append(board)
 J(d/'board_manifest.json',{'method':'RGBA alpha composite onto real light/dark backgrounds; nearest-neighbor uniform scaling, no body drawing or stretch; approximate head-height normalization, not exact anchors.','entries':entries})
 J(d/'execution_log.json',{'tool':'builtin image_gen.imagegen','generation_calls':1,'first_drafts':1,'hard_error_revisions_used':0,'input_images':[{'path':x['snapshot_path'],'sha256':x['sha256'],'actual_viewed':True} for x in i['source_images']],'prompt':{'path':'prompt_v1.txt','sha256':sha(d/'prompt_v1.txt')},'tool_args':{'path':'tool_args_v1.json','sha256':sha(d/'tool_args_v1.json')},'full_tool_return':{'path':'tool_return_v1.json','sha256':sha(d/'tool_return_v1.json')},'raw':{'path':raw.name,'sha256':sha(raw)},'candidate':{'path':selected.name,'sha256':sha(selected)},'postprocessing':'48 px transparent canvas margin only; source RGBA intact.','animation_verified':False,'runtimeVerified':False,'git_or_upload_actions':False})
 shutil.copy2(out/'build_previews.py',d/'build_previews_reference.py')
 print(n,selected.relative_to(R),sha(selected))
allboard=Image.new('RGB',(combined[0].width,sum(x.height for x in combined)),(240,235,225));y=0
for im in combined:allboard.paste(im,(0,y));y+=im.height
allboard.save(out/'009_010_相邻关键姿态_浅深对照.png')
