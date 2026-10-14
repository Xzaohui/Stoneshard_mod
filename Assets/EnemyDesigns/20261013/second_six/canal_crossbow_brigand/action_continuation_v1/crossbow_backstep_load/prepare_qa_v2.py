from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib, sys, shutil
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
d=json.loads((root/'Assets/EnemyDesigns/20261013/second_six/action_continuation_brief_v1.json').read_text())
idx=int(sys.argv[1]); item=d['items'][idx]
p=root/item['planned_output_directory']; slug=item['slug']; pose=item['pose_id']
raw=p/'raw'/f'{slug}_{pose}_v2_raw_imagegen.png'
dest=p/f'{slug}_{pose}_v2_transparent.png'
im=Image.open(raw).convert('RGBA')
# No visible-pixel edits. Only canonicalize invisible alpha-zero RGB.
pix=im.load(); cleared=0
for y in range(im.height):
 for x in range(im.width):
  r,g,b,a=pix[x,y]
  if a==0 and (r or g or b): pix[x,y]=(0,0,0,0);cleared+=1
im.save(dest)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for kind,col in [('light',(239,233,219,255)),('dark',(29,33,37,255))]:
 out=Image.new('RGBA',im.size,col);out.alpha_composite(im);out.convert('RGB').save(p/'qa'/f'v2_{kind}.png')
a=im.getchannel('A'); hist=a.histogram()
qa={'raw':str(raw.relative_to(root)),'raw_sha256':sha(raw),'candidate':str(dest.relative_to(root)),'candidate_sha256':sha(dest),'mode':'RGBA','size':list(im.size),'alpha_bbox':a.getbbox(),'alpha_zero_pixels':hist[0],'alpha_partial_pixels':sum(hist[1:255]),'alpha_255_pixels':hist[255],'alpha_zero_hidden_RGB_cleared':cleared,'visible_rgba_pixels_unchanged':True,'processing':'Only alpha=0 hidden RGB normalized to 0. No thresholding of alpha>0, no body edits, no crop, no resize.','actual_view_raw':True,'selected':False,'independent_review_pending':True}
(p/'qa/alpha_QA_v2.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
refs=[root/r['source_path'] for r in item['source_images']]+[dest]
labels=['母图', '旧阶段：'+item['source_images'][1]['pose_id'], '旧阶段：'+item['source_images'][2]['pose_id'], '新候选：'+item['label']]
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',18);sm=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',15)
w,h=1320,1000; board=Image.new('RGB',(w,h),(226,222,211));dr=ImageDraw.Draw(board);dr.text((22,16),item['concept_id']+' '+item['working_name']+'｜相邻关键阶段对照',font=font,fill='#24242a')
dr.text((22,45),'仅关键姿态概念；非连续动画、非锚点或游戏运行验收。每张等比最近邻缩放，旧图不改。',font=sm,fill='#34343a')
for row,bg in enumerate([(239,233,219,255),(29,33,37,255)]):
 for j,src in enumerate(refs):
  x=10+j*325;y=80+row*445
  ImageDraw.Draw(board).rectangle((x,y,x+320,y+438),fill=bg[:3])
  z=Image.open(src).convert('RGBA')
  # Common quarter-size view preserves native aspect; same source canvases use same factor.
  s=min(300/z.width,365/z.height); z=z.resize((round(z.width*s),round(z.height*s)),Image.Resampling.NEAREST)
  panel=Image.new('RGBA',z.size,bg);panel.alpha_composite(z)
  board.paste(panel.convert('RGB'),(x+(320-z.width)//2,y+48))
  lab=labels[j];textc=(38,40,44) if row==0 else (230,228,220)
  ImageDraw.Draw(board).text((x+7,y+10),lab[:33],font=sm,fill=textc)
dr.text((22,979),'浅/深底均通过真实 RGBA alpha_composite；alpha=0 的隐藏 RGB 不作为可见光晕。',font=sm,fill='#34343a')
board.save(p/'qa/v2_neighbor_board.png')
(p/'manifest_candidate_v2.json').write_text(json.dumps({'concept_id':item['concept_id'],'pose_id':pose,'status':'candidate_pending_independent_actual_view','generator':'builtin image_gen.imagegen','first_drafts':1,'hard_error_revisions_used':1,'max_hard_error_revisions':1,'runtimeIntegrated':False,'runtimeVerified':False,'continuous_animation_verified':False,'files':{str(q.relative_to(p)):sha(q) for q in [raw,dest,p/'calls/prompt_v2.txt',p/'calls/arguments_v2.json',p/'calls/tool_return_v2.json',p/'qa/alpha_QA_v2.json',p/'qa/v2_neighbor_board.png',p/'qa/v2_light.png',p/'qa/v2_dark.png']}},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(qa,ensure_ascii=False))

