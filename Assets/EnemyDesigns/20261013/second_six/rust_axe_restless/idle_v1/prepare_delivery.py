from PIL import Image
import numpy as np,json,hashlib,pathlib,datetime
root=pathlib.Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
for slug,id,revision in [('rust_axe_restless','009',False),('broken_shield_wraith','010',True)]:
 d=root/'Assets/EnemyDesigns/20261013/second_six'/slug/'idle_v1'; raw=d/(slug+('_idle_v2_raw_imagegen.png' if revision else '_idle_raw_imagegen.png')); im=Image.open(raw).convert('RGBA');a=np.asarray(im).copy();zero=a[:,:,3]==0;hidden=int(np.any(a[:,:,:3][zero]!=0,axis=1).sum()); a[zero,:3]=0;out=Image.fromarray(a);out.save(d/(slug+'_idle_transparent.png'))
 for bg,name in [((239,235,222,255),'light'),((27,31,39,255),'dark')]:
  board=Image.new('RGBA',im.size,bg);board.alpha_composite(out);board.convert('RGB').save(d/(slug+'_idle_preview_'+name+'.png'))
 small=out.copy(); small.thumbnail((256,320),Image.Resampling.NEAREST);b=Image.new('RGBA',(640,384),(239,235,222,255));b.alpha_composite(small,(int((320-small.width)/2),int((384-small.height)/2))); r=Image.new('RGBA',(320,384),(27,31,39,255));r.alpha_composite(small,(int((320-small.width)/2),int((384-small.height)/2)));b.alpha_composite(r,(320,0));b.convert('RGB').save(d/(slug+'_idle_review_board.png'))
 stats={'mode':im.mode,'size':im.size,'alpha_min':int(a[:,:,3].min()),'alpha_max':int(a[:,:,3].max()),'zero_alpha_pixels':int(zero.sum()),'partial_alpha_pixels':int(((a[:,:,3]>0)&(a[:,:,3]<255)).sum()),'bbox_alpha_nonzero':im.getbbox(),'hidden_rgb_pixels_cleaned':hidden,'alpha_unchanged':True,'visible_rgba_unchanged':True,'processing':'Only RGB at alpha=0 set to zero; full-size alpha composites; nearest aspect-preserving small-board layout. No painted body, threshold, RGB chromakey, or silhouette editing.'}
 (d/'alpha_audit.json').write_text(json.dumps(stats,indent=2)+'\n')
 qa=('009作者检查：双手在连续斧柄上有分开的完整握点；斧头、柄尾、头盔与双脚完整。塌肩裂甲及锈色可读，肉脸/耳/颊与腿肉保留，非纯骷髅。破靴露趾属于残靴造型。相较003的裸身空手C形，披甲方块上躯与斜斧是结构差异。首稿细纹理较密，属概念层像素美术，不声称低分辨率游戏精灵合格。' if id=='009' else '010作者检查：v1长而细的尾违背短钝尾核心，因此唯一一次定向修订为v2。v2盔冠降低，双短碎尾分离，无实体脚。持剑拳、护手、柄及完整剑刃连续；盾侧可见握手，盾无悬空误读。冷灰青剑盾、平残盔、短尾和004长兜帽袍形成结构差异。v1/v2 raw中的背景辉光实际在隐藏RGB；浅底alpha合成无该雾，未以颜色抠图。尾端仍有少量角形尖簇，核心长度已缩短。')
 (d/'AUTHOR_QA.md').write_text('# 作者检查\n\n'+qa+'\n\n状态：待独立审查；不是游戏落地、剧情身份或用户验收。\n',encoding='utf-8')
 files=[{'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(d.iterdir()) if p.is_file() and p.name!='manifest.json']
 m={'schema_version':1,'concept_id':'EAO-CONCEPT-ENEMY-'+id,'working_name_only':True,'generator':'builtin image_gen.imagegen','generation_calls':2 if revision else 1,'hard_error_revisions_used':int(revision),'hard_error_revision_cap':1,'candidate_raw':str(raw.relative_to(root)),'candidate_transparent':str((d/(slug+'_idle_transparent.png')).relative_to(root)),'status':'frozen_candidate_pending_independent_review','runtimeIntegrated':False,'runtimeVerified':False,'delivered':False,'alpha_audit':stats,'files':files,'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 (d/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 print(id,stats)
