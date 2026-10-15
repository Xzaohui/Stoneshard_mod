from PIL import Image
from pathlib import Path
import json,hashlib,shutil,datetime
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); B=R/'Assets/EnemyDesigns/reference/20261013'
brief=json.loads((B/'production_brief_second_six.json').read_text());sources=json.loads((B/'sources_second_six.json').read_text());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for slug,num,raw in [('swollen_throat_bloodkin','011','exec-da43fb12-8700-4a0a-ae15-715838cecf27.png'),('hushed_bell_cultist','012','exec-6c4cce65-2129-437c-bffa-5cad9f65e087.png')]:
 d=R/f'Assets/EnemyDesigns/20261013/second_six/{slug}/idle_v1';c=next(x for x in brief['concepts'] if x['concept_id'].endswith(num)); src=Path('/workspace/scratch/5ed8df2c5d81/generated_images')/raw
 out=d/f'{slug}_idle_raw_imagegen.png';shutil.copy2(src,out)
 im=Image.open(out).convert('RGBA');px=list(im.getdata()); cleaned=[(0,0,0,0) if a<=8 else (r,g,b,a) for r,g,b,a in px];cl=Image.new('RGBA',im.size);cl.putdata(cleaned);cl.save(d/f'{slug}_idle_transparent.png')
 for kind,col in [('light',(238,231,216,255)),('dark',(29,34,40,255))]:
  board=Image.new('RGBA',im.size,col);board.alpha_composite(cl);board.convert('RGB').save(d/f'{slug}_review_{kind}.png')
 rawboard=Image.new('RGBA',im.size,(238,231,216,255));rawboard.alpha_composite(im);rawboard.convert('RGB').save(d/'raw_alpha_on_light.png')
 bbox=cl.getbbox();thumb=cl.crop(bbox);thumb.thumbnail((240,300),Image.Resampling.NEAREST)
 board=Image.new('RGBA',(600,340),(238,231,216,255));board.paste(Image.new('RGBA',(300,340),(29,34,40,255)),(300,0));board.alpha_composite(thumb,((300-thumb.width)//2,(340-thumb.height)//2));board.alpha_composite(thumb,(300+(300-thumb.width)//2,(340-thumb.height)//2));board.convert('RGB').save(d/'reduced_readability.png')
 refs=[x for x in sources['references'] if x['id']=='R06'] if 'references' in sources else []
 snapshot={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_brief':{'path':str((B/'production_brief_second_six.json').relative_to(R)),'sha256':sha(B/'production_brief_second_six.json')},'source_addendum':{'path':str((B/'sources_second_six.json').relative_to(R)),'sha256':sha(B/'sources_second_six.json')},'concept':c,'execution_authority':'Parent explicitly started production of 011/012; original research brief remains read-only.','mother':brief['source_integrity']['mother_images'][4 if num=='011' else 5],'style_references':brief['style']['references'],'actual_artist_visual_inspection':['R06 original Proselytes lineup /tmp/stoneshard_refs/proselytes.png','005 and 006 raw mother images','Sela G and Mia v2 raw style references'],'sha_verified':True,'original_reference_sha256':sha('/tmp/stoneshard_refs/proselytes.png'),'original_reference_persisted':False,'project_sources':{k:brief['source_integrity']['project_sources'][k] for k in c['project_source_keys']},'canon_limits':brief['global_exclusions']}
 (d/'source_snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
 audit={'raw_mode':im.mode,'raw_dimensions':im.size,'raw_alpha_extrema':im.getchannel('A').getextrema(),'raw_zero_alpha_pixels':sum(a==0 for *_,a in px),'cleaning':'Only alpha values <=8 cleared; RGB under resulting zero alpha set to zero. All visible RGB and all alpha >8 exactly preserved. No silhouette/body painting, no black/color deletion.','pixels_cleared_with_positive_alpha':sum(0<a<=8 for *_,a in px),'output_bbox':bbox,'visible_rgb_unchanged':all(p[:3]==q[:3] for p,q in zip(px,cleaned) if q[3]>0),'layout':'Full-size light/dark backgrounds; reduced readability view uses nearest-neighbor aspect-preserving thumbnail.'}
 (d/'alpha_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
 invocation={'tool':'builtin image_gen.imagegen','prompt_file':'prompt_v1.txt','prompt_sha256':sha(d/'prompt_v1.txt'),'transparent_background':True,'referenced_image_paths':'omitted: new generation, visual reference inspection only','num_last_images_to_include':'omitted','returned_saved_path':str(src),'raw_sha256':sha(out),'generation_call_count':1,'hard_error_revisions_used':0,'hard_error_revision_cap':1}
 (d/'generation_call.json').write_text(json.dumps(invocation,indent=2)+'\n')
 (d/'spec_lock.md').write_text('# '+c['working_name']+' / '+c['concept_id']+'\n\n'+json.dumps(c['original_proposal'],ensure_ascii=False,indent=2)+'\n\n原创可逆静态概念。未定剧情身份、阵营、技能或生成地点；未实现运行。只按两臂两腿与自身异化结构审查011，不套正常人比例。\n')
 (d/'authorQA.md').write_text('# 作者视觉QA（独审前）\n\n'+('011：小头完整、尖耳和单短牙；膨喉胸椭圆主形清楚，双臂明显短于005，双足承重；两臂两腿、无背峰和额外口。肉体异常是幻想异化，不绑定患者。肩挂残布与腰布完整。\n' if num=='011' else '012：低圆帽露成年脸，鼻口与侧听目光清楚；短袍与双靴完整。木柄由单拳握住，向下连接钟肩，铃口及小铃舌清楚，铃侧与腿分离。无高兜帽、长杆或教会纹章。整体偏写实紧凑度待独审，不强卡头身比。\n')+'\n原始PNG含真实alpha但零透明RGB有晕影；交付只清alpha<=8与隐藏RGB，不改身体可见像素。浅深板和缩略读形板将实际目视后补核。未称selected/delivered；不改变旧母图或历史QA。\n')
 print(slug,str(d))
