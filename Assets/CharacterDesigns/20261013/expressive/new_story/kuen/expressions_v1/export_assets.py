import pathlib,json,hashlib,shutil,datetime
import numpy as np
from PIL import Image,ImageDraw,ImageFont
R=pathlib.Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); B=json.loads((R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/second_four_expression_brief.json').read_text()); H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
outs=['exec-ed0324f0-1982-4bb2-8094-8b8d597272a6.png','exec-a581ccc7-06e9-4214-bdad-2b24de1aace3.png','exec-64b4a1bc-df88-4533-95fe-d108ce0f4bbf.png','exec-c45c485f-4ed7-4823-bf35-9ecbed7207aa.png']
for ci,c in enumerate(B['characters'][:2]):
 d=R/'Assets/CharacterDesigns/20261013/expressive/new_story'/c['slug']/'expressions_v1'; logs=[]; ars=[]; ims=[]
 for i,e in enumerate(c['expressions']):
  key=e['key']; raw=d/'raw'/f'{key}_initial.png'; shutil.copy2(R.parent/'generated_images'/outs[ci*2+i],raw)
  a=json.loads((d/'prompts'/f"{c['slug']}_{e['id']}_actual_call.json").read_text()); pp=d/'prompts'/f'{key}_initial.txt'; pp.write_text(a['arguments']['prompt'])
  ar=np.array(Image.open(raw).convert('RGBA')); before=ar.copy(); ar[ar[:,:,3]<128]=0; ar[:,:,3]=np.where(ar[:,:,3]>=128,255,0); ar[ar[:,:,3]==0]=0
  im=Image.fromarray(ar); final=d/'selected'/f'{key}_transparent.png'; im.save(final); ims.append(im)
  ars.append({'expression':e['id'],'raw_size':im.size,'alpha_before_unique':len(np.unique(before[:,:,3])),'alpha_after_unique':np.unique(ar[:,:,3]).tolist(),'transparent_pixels':int((ar[:,:,3]==0).sum()),'hidden_rgb_nonzero':int(np.count_nonzero(ar[ar[:,:,3]==0,:3])),'bbox':im.getbbox(),'method':'Preserve model alpha support at alpha >=128; below 128 cleared, remaining alpha 255; hidden RGB zeroed. No drawing, repainting, morphology or anatomy edits.'})
  logs.append({'expression':e['id'],'label_zh':e['label_zh'],'tool':'builtin image_gen.imagegen','variant':'initial','references':[c['source_anchor'][k] for k in ['selected_raw','selected_transparent']],'prompt':str(pp.relative_to(d)),'prompt_sha256':H(pp),'actual_call':f"prompts/{c['slug']}_{e['id']}_actual_call.json",'raw':str(raw.relative_to(d)),'raw_sha256':H(raw),'selected':str(final.relative_to(d)),'selected_sha256':H(final),'revisions_used':0,'maximum_hard_error_revisions':1,'selection_reason':'Author viewed raw; adult identity, props and readable paired facial difference pass.'})
 for mode,bg,fg in [('light','#eee8de','#342b26'),('dark','#242832','#f1e7d7')]:
  board=Image.new('RGB',(1600,1200),bg); dr=ImageDraw.Draw(board); font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; title=ImageFont.truetype(font,40); sub=ImageFont.truetype(font,30)
  dr.text((45,22),c['name']+' · 两种情绪概念',font=title,fill=fg); dr.text((45,78),'独立条件演出 · 非任务完成或游戏实装',font=sub,fill=fg)
  for i,(im,e) in enumerate(zip(ims,c['expressions'])):
   scale=min(740/im.width,1000/im.height); pic=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST); board.paste(pic,(i*800+(800-pic.width)//2,140),pic); dr.text((i*800+230,1150),e['label_zh'],font=sub,fill=fg)
  board.save(d/'review'/f"{c['slug']}_expressions_{mode}.png")
 (d/'generation-log.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)); (d/'alpha_report.json').write_text(json.dumps(ars,ensure_ascii=False,indent=2)); shutil.copy2('/tmp/export_kuen_sune.py',d/'export_assets.py')
 (d/'README.md').write_text(f"# {c['name']}：两种情绪概念\n\n"+'、'.join(e['label_zh'] for e in c['expressions'])+'。\n\n内置 image_gen 逐图参考已通过母图生成，首稿各一次；完整实际调用参数、提示词、原图、卡与台本快照及SHA保留。脚本仅透明alpha/隐藏RGB清理、nearest等比排版；未绘画身体。\n\n仅人物像素概念，不代表原生网格、动画、装备、part/frame/mask/origin或游戏运行；不回写剧情状态。\n')
print('exported')
