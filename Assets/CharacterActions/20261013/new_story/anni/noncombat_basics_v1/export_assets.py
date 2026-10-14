from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil,datetime,sys,numpy as np
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',32)
small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',21)
slug=sys.argv[1];o=R/f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1';b=json.loads((o/'production_brief.json').read_text());origins=json.loads((o/'generation_origins.json').read_text());versions=json.loads((o/'selection_versions.json').read_text());logs=[];alpha=[];assets=[];imgs=[]
for p in b['plans']:
 key=p['key'];v=versions[key];raw=o/'raw'/f'{key}_v{v}.png';sel=o/'selected'/f'{key}_transparent.png';shutil.copyfile(raw,sel);im=Image.open(sel);assert im.mode=='RGBA';a=np.array(im.getchannel('A'));bbox=im.getbbox();alpha.append({'key':key,'mode':im.mode,'size':im.size,'alpha_zero_pixels':int((a==0).sum()),'alpha_partial_pixels':int(((a>0)&(a<255)).sum()),'alpha_opaque_pixels':int((a==255).sum()),'alpha_bbox':bbox,'corner_alpha':[int(a[0,0]),int(a[0,-1]),int(a[-1,0]),int(a[-1,-1])],'selection_byte_identical_to_raw':True,'processing':'Byte-for-byte copy of generated RGBA. No alpha edit, resizing, cropping, quantization, body drawing, compositing or retouch to selected PNG.'})
 assets.append({'key':key,'title_zh':p['title_zh'],'selected_version':v,'selected':str(sel.relative_to(o)),'selected_sha256':sha(sel),'raw':str(raw.relative_to(o)),'raw_sha256':sha(raw),'status':'author_pass_pending_independent_review','kind':'independent_noncombat_fullbody_keypose','animation_claim':False,'story_state_changes':False});imgs.append(im)
 for rawp in sorted((o/'raw').glob(key+'_v*.png')):
  stem=rawp.stem;prompt=o/'prompts'/f'{stem}.txt';args=o/'prompts'/f'{stem}.tool_args.json';argdata=json.loads(args.read_text());assert argdata['prompt']==prompt.read_text();origin=Path(origins[stem]);assert rawp.read_bytes()==origin.read_bytes();log={'key':key,'version':int(stem.rsplit('_v',1)[1]),'tool':'builtin image_gen.imagegen','original_generated_path':str(origin),'tool_result_keys':['image_url','output_hint'],'raw':str(rawp.relative_to(o)),'raw_sha256':sha(rawp),'raw_bytes':rawp.stat().st_size,'prompt':str(prompt.relative_to(o)),'prompt_sha256':sha(prompt),'tool_args':str(args.relative_to(o)),'tool_args_sha256':sha(args),'prompt_matches_submitted_argument':True,'references':[{'path':str(Path(x).relative_to(R)),'sha256':sha(Path(x))} for x in argdata['referenced_image_paths']],'selected':rawp==raw,'original_copy_verified':True,'hard_error_revision_used':v-1};logs.append(log);(o/'raw'/f'{stem}.receipt.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
 for theme,bg,fg in [('light',(237,233,222),(36,37,35)),('dark',(31,36,42),(237,233,222))]:
  board=Image.new('RGB',(im.width+96,im.height+190),bg);board.paste(im,(48,120),im);d=ImageDraw.Draw(board);d.text((36,22),b['name']+'｜'+p['title_zh'],font=font,fill=fg);d.text((36,68),'独立非战斗全身关键姿势 · 透明原稿原尺寸展示',font=small,fill=fg);d.text((36,board.height-47),'动作概念；不表示交接、续约、付款、治疗或任务完成。',font=small,fill=fg);board.save(o/'review'/f'{key}_{theme}.png')
for theme,bg,fg in [('light',(237,233,222),(36,37,35)),('dark',(31,36,42),(237,233,222))]:
 board=Image.new('RGB',(1920,1050),bg);d=ImageDraw.Draw(board);d.text((34,20),b['name']+'｜母图与两种独立职业动作',font=font,fill=fg);d.text((34,70),b['canonical_id']+' · 两图彼此独立，不代表连续动画或剧情先后',font=small,fill=fg)
 mother=Image.open(R/b['mother_image']['path']);allimgs=[mother]+imgs;labels=['母图 · 身份参考']+[p['title_zh'] for p in b['plans']]
 for i,(im,label) in enumerate(zip(allimgs,labels)):
  n=im.copy();n.thumbnail((590,825),Image.Resampling.NEAREST);board.paste(n,(640*i+(640-n.width)//2,140+(825-n.height)//2),n);d.text((640*i+35,111),label,font=small,fill=fg)
 d.text((34,997),'本人脸、服装与道具沿用母图；不验证装备、连续性、原生像素尺寸或引擎效果。',font=small,fill=fg);board.save(o/'review'/f'{slug}_actions_comparison_{theme}.png')
(o/'alpha_report.json').write_text(json.dumps(alpha,ensure_ascii=False,indent=2));(o/'generation-log.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2));(o/'asset_catalog.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2));shutil.copyfile(__file__,o/'export_assets.py')
print(json.dumps({'slug':slug,'assets':assets,'alpha':alpha},ensure_ascii=False,indent=2))
