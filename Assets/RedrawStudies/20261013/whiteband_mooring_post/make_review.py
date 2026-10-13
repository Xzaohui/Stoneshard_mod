from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent; R=P.parents[3]
native=Image.open(P/'native_32x48.png').convert('RGBA')
oldpath=R/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch01/04_dock_landmark_props.png'
old=Image.open(oldpath).convert('RGBA'); oldcrop=old.crop((58,152,320,758))
oldcrop.save(P/'old04_left_crop_review.png')
board=Image.new('RGB',(1050,580),'#77766e');draw=ImageDraw.Draw(board)
def put(im,xy,size=None):
 if size:im=im.resize(size,Image.Resampling.NEAREST)
 board.paste(im,xy,im if im.mode=='RGBA' else None)
draw.text((16,12),'OLD 04 LEFT ONLY / detail concept',fill='white');put(oldcrop,(35,45),(187,433))
draw.text((270,12),'NEW / 32x48 canvas / 8x nearest',fill='white');put(native,(295,45),(256,384))
draw.text((610,12),'SAME MAGNIFICATION REFERENCES / 8x',fill='white')
refs=R/'Assets/ReferenceAudit/20261013/originals'
bar=Image.open(refs/'Barrel_0.png').convert('RGBA');put(bar,(620,155),(200,216))
npc=Image.open(refs/'s_npc_carpenter_0.png').convert('RGBA');put(npc,(790,75),(280,352))
draw.text((620,390),'Historical barrel / Jurg reference',fill='white')
draw.text((620,414),'Not a matching vanilla mooring post.',fill='white')
draw.text((620,438),'42px visible post is a scale trial.',fill='white')
draw.text((16,503),'Old crop is fitted for review, NOT same scale. New / barrel / Jurg are exactly 8x.',fill='white')
draw.text((16,525),'Wood/camera reference only. No engine dimensions, collision, ownership or permission implied.',fill='white')
draw.text((16,548),'One return-shore marker: pale band, rope knot, dark tide stain. No dock/boat/characters in asset.',fill='white')
board.save(P/'old_new_reference_comparison.png')
sheet=Image.new('RGB',(860,380),'#77766e'); d=ImageDraw.Draw(sheet)
d.text((10,10),'Native candidate 1x / 8x; shallow top and timber material references',fill='white')
sheet.paste(native,(25,70),native);sheet.paste(native.resize((256,384),Image.Resampling.NEAREST),(70,0),native.resize((256,384),Image.Resampling.NEAREST))
book=Image.open(refs/'Bookshelf_0.png').convert('RGBA');sheet.paste(book.resize((264,256),Image.Resampling.NEAREST),(330,75),book.resize((264,256),Image.Resampling.NEAREST))
env=Image.open(refs/'Frid_environ.png').convert('RGB');sheet.paste(env,(580,55));d.text((580,342),'Environment only; scale/version unknown',fill='white');sheet.save(P/'material_camera_review.png')
meta=json.loads((R/'Assets/ReferenceAudit/20261013/original-reference-metadata.json').read_text())
sourcepaths=[oldpath,R/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/manifest.json',R/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch01/PROMPTS.md',R/'design/02_世界与地图/任务空间/空间_BRY-X11_低潮侧泊棚.md',R/'design/06_支线/城市支线/台本_CS-BRY-11_不写船名的夜泊.md']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'schema_version':1,'date':'2026-10-13','candidate_count':1,'imagegen_calls':1,'tool':'built-in image_gen.imagegen','full_prompt':(P/'prompt.txt').read_text(),'input_images_to_generator':[],'references_inspected_by_author':True,'sources':[{'path':str(p.relative_to(R)),'sha256':sha(p)} for p in sourcepaths], 'visual_references':[x for x in meta['references'] if x['name'] in ['Barrel_0.png','Bookshelf_0.png','Frid_environ.png','Jurg']], 'source_limits':['同材质与相机参照，不是同物原版匹配','Historical wiki props not verified against installed 0.9.4.25','No direct original mooring-post sprite located; no invented engine resource name or dimensions','Reference art retained for review only, no runtime packaging or reuse license assumed'],'narrative_limits':['白带仅是回岸地标，不是所有权、自由出入许可、自动出航或任务完成证明','不加入载重刻度；实际回岸路径需要后续场景放置验证','只做一根站立木桩；不生成码头或其他物件'],'runtime_integrated':False,'engine_ready':False,'outputs':[]}
for p in sorted(P.iterdir()):
 if p.is_file() and p.name!='manifest.json':manifest['outputs'].append({'path':p.name,'sha256':sha(p)})
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
