from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil,datetime
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
bp=root/'Assets/EnemyDesigns/reference/20261013/production_brief_second_six.json';sp=root/'Assets/EnemyDesigns/reference/20261013/sources_second_six.json'
b=json.loads(bp.read_text());s=json.loads(sp.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for idx,slug,gen in [(0,'border_roundshield_rebel','exec-41b2bfb9-ff0c-48f3-bc65-9e1d0f0b6e26.png'),(1,'canal_crossbow_brigand','exec-1f3c76cb-e9fd-4efc-982a-7b1fc55eb9ae.png')]:
 c=b['concepts'][idx];d=root/c['output_directory'];ss=d/'sources';ss.mkdir(exist_ok=True)
 refs=[]
 for r in s['public_visual_references']:
  if r['id'] not in c['reference_ids']:continue
  p=Path(r['local_temporary_path']);refs.append(dict(r,sha256_verified=sha(p),viewed_by_author=True,inspection_scope_author='whole static image actually viewed before generation',copied_to_repository=False))
 local=[s['mother_images_viewed'][idx]]+s['style_references_viewed']
 for r in local:
  p=root/r['path'];dest=ss/p.name;shutil.copy2(p,dest);refs.append(dict(r,sha256_verified=sha(p),source_snapshot=str(dest.relative_to(root)),viewed_by_author=True))
 for p in [bp,sp]:shutil.copy2(p,ss/p.name)
 source={'concept_id':c['concept_id'],'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generation_authorization':'Parent task explicitly started second_six; historical brief false gate retained as source snapshot, not current prohibition.','references':refs,'brief_sha256':sha(bp),'source_addendum_sha256':sha(sp),'no_vanilla_images_copied':True}
 (d/'sources.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n')
 raw=d/(slug+'_idle_raw_imagegen.png');im=Image.open(raw).convert('RGBA');pixels=list(im.getdata());removed=sum(0<a<=1 for r,g,bb,a in pixels)
 im.putdata([(0,0,0,0) if a<=1 else (r,g,bb,a) for r,g,bb,a in pixels]);out=d/(slug+'_idle_transparent.png');im.save(out)
 for label,color in [('light',(231,225,211,255)),('dark',(32,38,45,255))]:
  board=Image.new('RGBA',im.size,color);board.alpha_composite(im);board.convert('RGB').save(d/(slug+'_preview_'+label+'.png'))
 small=im.resize((im.width//3,im.height//3),Image.Resampling.NEAREST);board=Image.new('RGBA',(small.width*2,small.height),(231,225,211,255));board.alpha_composite(small);right=Image.new('RGBA',small.size,(32,38,45,255));right.alpha_composite(small);board.paste(right,(small.width,0));board.convert('RGB').save(d/(slug+'_preview_small.png'))
 arguments={'prompt':(d/'prompt_v1.txt').read_text().rstrip('\n'),'transparent_background':True,'referenced_image_paths':[str(root/s['style_references_viewed'][1]['path']),str(root/s['style_references_viewed'][2]['path']),str(root/s['mother_images_viewed'][idx]['path'])]}
 (d/'imagegen_call_v1.json').write_text(json.dumps({'tool':'builtin image_gen.imagegen','arguments':arguments,'output_path':'/workspace/scratch/5ed8df2c5d81/generated_images/'+gen,'call_index':1,'revision':False},ensure_ascii=False,indent=2)+'\n')
 m={'concept_id':c['concept_id'],'name':c['working_name'],'status':'awaiting_independent_review','generation_calls':1,'hard_error_revisions_used':0,'runtimeIntegrated':False,'runtimeVerified':False,'scope':'original static concept only; no canon, roster, animation or game package changes','raw':raw.name,'transparent':out.name,'alpha_cleanup':{'operation':'Set alpha <=1 to zero and hidden RGB to zero only; all other pixels unchanged','low_alpha_pixels_cleared':removed,'body_or_weapon_redrawn':False},'dimensions':im.size,'alpha_bbox':im.getchannel('A').getbbox(),'files':{p.name:sha(p) for p in d.iterdir() if p.is_file()},'source_snapshots':{str(p.relative_to(d)):sha(p) for p in ss.iterdir()}}
 (d/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 qa=f'''# 作者静态概念自检\n\n{c['concept_id']} {c['working_name']}\n\n- builtin imagegen 首稿一次；未修订，待独审。\n- 实际查看对应001/002母图、Sela G、Mia v2及指定两张原版静态参考；SHA与来源登记一致。原版图片留在/tmp，没有复制进仓库。\n- 成熟成年脸，轻三分之四向左，低魔布/木/皮/铁，完整两腿两臂。\n- {'圆木盾与短单刃斧结构替换长矛，盾侧可见上臂和肘连续至盾后；背带大部分自然遮挡，非浮盾。斧柄握点、刃和双靴完整。' if idx==0 else '瘦身双手横弩区别宽壮短棍母图；纵床、横弓、弦、踏环可辨，双手握点分开，前手托底后手握机柄。双靴完整。'}\n- 原生RGBA透明；alpha=1的近不可见背景残留清零，透明像素隐藏RGB清零。未按颜色删除背景，未重绘身体/武器，其他alpha与颜色原样保留。\n- 浅深底与1/3 nearest缩小板已生成；供独审检查。\n- 无环境/投影/徽章/文字。仅静态美术候选，未动画、未锚点碰撞、未进入游戏。\n'''
 (d/'QA_AUTHOR.md').write_text(qa)
 print(c['concept_id'],d,sha(raw),sha(out),im.getchannel('A').getbbox())
