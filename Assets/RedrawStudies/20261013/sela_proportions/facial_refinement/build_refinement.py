from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,argparse,shutil
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'Assets/RedrawStudies/20261013/sela_proportions/revision_1to1'
OUT=Path(argparse.ArgumentParser().parse_known_args()[1][0]) if len(__import__('sys').argv)>1 else Path(__file__).parent
OUT.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
src=BASE/'sela_structural_idle_view01_f000.png'
assert sha(src)=='53b588b17eae59d3bdebd7190f7cf96e35c297354393dcf34174c49777f41b98'
im=Image.open(src).convert('RGBA'); a=np.array(im)
pal=json.loads((BASE/'palette.json').read_text()); P={p['name']:tuple(bytes.fromhex(p['hex'][1:]))+(255,) for p in pal}; P['transparent']=(0,0,0,0)
# Edits are authored at native integer coordinates; no resampling or generated texture.
common=[(10,17,'transparent','Retract outermost nose projection by one pixel'),(10,18,'transparent','Retract matching black nose underside'),(11,17,'skin_mid','Keep restrained warm nose edge'),(12,17,'skin_mid','Model nasal underside rather than a flat bright ledge'),(16,16,'skin_mid','Connect temple to cheek shadow'),(16,17,'skin_shadow','Separate cheek plane from nose light'),(16,18,'skin_mid','Soften cheek transition'),(16,19,'skin_mid','Retain warm lower cheek'),(12,19,'skin_mid','Soften lower lip-to-chin transition')]
variants={
'A':common+[(11,13,'skin_mid','Expose a narrow far orbital plane for a restrained three-quarter reading'),(12,13,'skin_mid','Warm far brow transition'),(12,14,'hair_mid','One-pixel far eye with lower contrast'),(13,14,'skin_light','Separate far eye and near eye with nose bridge'),(14,14,'deep_brown','Keep compact near eye dark anchor'),(15,14,'skin_mid','Break horizontal lid reading and keep near eye compact'),(14,15,'deep_brown','Two-pixel vertical near-eye socket without white or enlarged eyeball'),(11,15,'skin_shadow','Turn far cheek plane toward viewer'),(12,15,'skin_mid','Bridge to far cheek'),(13,16,'skin_mid','Turn nasal plane inward'),(14,16,'skin_mid','Limit broad flat highlight'),(13,17,'skin_mid','Separate nasal underside from mouth mark'),(14,17,'skin_mid','Blend nasal underside into near cheek'),(13,18,'hair_light','Short warm mouth mark'),(14,18,'skin_shadow','Soft mouth corner'),(15,18,'skin_light','Break horizontal mouth-to-cheek band'),(13,19,'skin_light','Keep lower lip/chin separation')],
'B':common+[(13,14,'deep_brown','Retain single eye and side-facing gaze with a softer dark'),(14,14,'hair_mid','Taper eye end instead of a two-black-pixel bar'),(13,17,'skin_shadow','Suggest compact nasal underside'),(13,18,'hair_light','One-pixel warm mouth mark'),(14,18,'skin_mid','Blend mouth into cheek'),(15,18,'skin_light','Break horizontal mouth-to-cheek band')]
}
allowed=np.zeros(a.shape[:2],dtype=bool)
for y,x0,x1 in [(13,11,16),(14,11,16),(15,11,16),(16,11,16),(17,10,16),(18,10,16),(19,12,16)]:allowed[y,x0:x1+1]=True
Image.fromarray((allowed*255).astype('uint8')).save(OUT/'face_allowed_envelope.png')
results={}; edits={}; masks={}; qa={}; protected={str(p.relative_to(ROOT)):sha(p) for p in BASE.iterdir() if p.is_file()}
shutil.copyfile(src,OUT/'before_native.png')
for k,entries in variants.items():
 b=a.copy(); reasons={}
 for x,y,color,reason in entries:b[y,x]=P[color];reasons[(x,y)]=reason
 mask=np.any(a!=b,axis=2); masks[k]=mask
 rows=[]
 for y,x in zip(*np.where(mask)):rows.append({'x':int(x),'y':int(y),'before':a[y,x].tolist(),'after':b[y,x].tolist(),'reason':reasons[(x,y)]})
 edits[k]=rows; result=Image.fromarray(b);results[k]=result
 result.save(OUT/f'sela_face_{k}_native.png'); result.resize((280,352),Image.Resampling.NEAREST).save(OUT/f'sela_face_{k}_8x.png')
 Image.fromarray((mask*255).astype('uint8')).save(OUT/f'face_mask_{k}.png')
 unchanged=a[~mask].tobytes();ys,xs=np.where(b[:,:,3]>0)
 assert not np.any(mask & ~allowed)
 qa[k]={'all_edits_inside_predeclared_face_envelope':True,'outside_allowed_envelope_exact_equal':bool(np.array_equal(a[~allowed],b[~allowed])),'outside_allowed_envelope_sha256':hashlib.sha256(b[~allowed].tobytes()).hexdigest(),'changed_pixels':len(rows),'changed_bbox_xyxy':list(Image.fromarray((mask*255).astype('uint8')).getbbox()),'outside_mask_exact_equal':bool(np.array_equal(a[~mask],b[~mask])),'outside_mask_before_sha256':hashlib.sha256(unchanged).hexdigest(),'outside_mask_after_sha256':hashlib.sha256(b[~mask].tobytes()).hexdigest(),'top_y':int(ys.min()),'sole_y':int(ys.max()),'chin_row20_exact_unchanged':bool(np.array_equal(a[20],b[20])),'all_rows_outside_13_to_19_exact_equal':bool(np.array_equal(a[list(range(13))+list(range(20,44))],b[list(range(13))+list(range(20,44))])),'binary_alpha':set(np.unique(b[:,:,3]).tolist())=={0,255},'transparent_rgb_zero':bool((b[b[:,:,3]==0,:3]==0).all()),'new_colors':list(set(map(tuple,b.reshape(-1,4)))-set(map(tuple,a.reshape(-1,4)))),'alpha_removed_xy':[[int(x),int(y)] for y,x in zip(*np.where((a[:,:,3]>0)&(b[:,:,3]==0)))]}
refs=[('Gunda',ROOT/'Assets/ReferenceAudit/20261013/originals/s_peasantfemale_09_0.png'),('Bert',ROOT/'Assets/ReferenceAudit/20261013/originals/s_npc_merchant01_0.png')]
items=[('Before',im),('A',results['A']),('B',results['B'])]+[(n,Image.open(p).convert('RGBA')) for n,p in refs]
# Native artwork is always integer 1x or nearest-neighbor, canvas tops/ground aligned.
for scale in [1,8]:
 cell=44*scale; board=Image.new('RGB',(cell*len(items),44*scale+24),(180,183,172)); d=ImageDraw.Draw(board)
 for i,(name,img) in enumerate(items):
  d.text((i*cell+3,4),name,fill=(20,20,20)); spr=img.resize((img.width*scale,img.height*scale),Image.Resampling.NEAREST);board.paste(spr,(i*cell+(cell-spr.width)//2,24),spr)
 board.save(OUT/f'comparison_originals_{scale}x.png')
board=Image.new('RGB',(5*220,250),(180,183,172));d=ImageDraw.Draw(board)
for i,(name,img) in enumerate(items):
 d.text((i*220+5,5),name,fill=(20,20,20)); crop=img.crop((7,3,29,23)).resize((220,200),Image.Resampling.NEAREST);board.paste(crop,(i*220,30),crop)
board.save(OUT/'face_closeups_10x.png')
jsonwrite=lambda name,obj:(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
jsonwrite('pixel_edits.json',edits);jsonwrite('palette.json',{'source_palette':pal,'new_colors':[],'all_hand_pixels_unchanged':True,'no_global_skin_lightening':True});jsonwrite('QA-producer.json',qa)
assert all(sha(ROOT/p)==h for p,h in protected.items())
jsonwrite('manifest.json',{'source':str(src.relative_to(ROOT)),'source_sha256':sha(src),'method':'Explicit native pixel edits using authorized Pillow. No generative redraw, no palette or whole-body resampling. A gently turns facial planes; B preserves single-eye orientation. Both retract nasal silhouette two pixels. Original reference faces are comparison only, never sampled or copied.','protected_inputs':protected,'references':[{'name':n,'path':str(p.relative_to(ROOT)),'sha256':sha(p),'copied_pixels':False} for n,p in refs],'script_sha256':sha(Path(__file__)),'outputs':{p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='manifest.json'},'runtime_changed':False,'selection':'Pending independent visual review; neither accepted by user.'})
print(json.dumps(qa,ensure_ascii=False,indent=2))
