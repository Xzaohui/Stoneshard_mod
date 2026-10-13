#!/usr/bin/env python3
"""Source-guided, designer-masked three-keyframe study. No source/runtime writes."""
from pathlib import Path
import argparse, json, hashlib, platform
import numpy as np
from PIL import Image, ImageDraw, __version__ as pillow_version
from scipy import ndimage
import scipy
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
SOURCE=ROOT/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch66/03_yani_rises_from_stool.png'
SCALE=34/828
# Origins represent the SAME front stool post, not character bounding-box centers.
STARTS=[0,500,1013]
PALETTE=[('outline','#241e1a'),('deep_shadow','#3a2c23'),('hair_shadow','#514238'),('hair_mid','#74604e'),('hair_light','#947b60'),('skin_shadow','#ac6943'),('skin_mid','#d99060'),('skin_light','#efb17d'),('stubble','#8a7761'),('cloak_shadow','#54473f'),('cloak_mid','#776456'),('cloak_light','#93806a'),('tunic_shadow','#3e3c27'),('tunic_mid','#5e5b37'),('tunic_light','#7c754a'),('cuff_shadow','#aa9478'),('cuff_light','#d6c2a0'),('trouser_shadow','#4b403b'),('trouser_mid','#65554a'),('trouser_light','#7e6958'),('leather_shadow','#50341f'),('leather_mid','#795132'),('wood_light','#a57445'),('clasp','#b89552')]
P=np.array([tuple(bytes.fromhex(h[1:])) for _,h in PALETTE],dtype=np.uint8)
# Polygon boundaries deliberately separate the character from a changing generated stool.
# Source-pixel tracing is a design decision, not an automated segmentation certificate.
POLYGONS=[
[(165,352),(164,303),(198,279),(239,272),(295,293),(310,333),(303,373),(284,391),(337,413),(376,504),(396,569),(378,603),(421,602),(435,656),(429,754),(414,770),(416,813),(458,835),(466,864),(389,873),(329,852),(330,818),(327,764),(332,719),(318,687),(265,694),(261,752),(252,770),(250,813),(264,872),(260,899),(202,903),(181,887),(184,855),(190,818),(179,776),(150,765),(137,740),(141,692),(121,690),(108,674),(85,715),(78,752),(53,768),(31,747),(20,714),(35,661),(64,591),(62,529),(85,452),(128,393)],
[(252,225),(260,202),(291,181),(337,183),(390,199),(398,248),(381,277),(391,294),(411,330),(425,421),(420,463),(418,485),(410,515),(413,548),(427,582),(424,630),(420,662),(430,709),(420,757),(410,775),(413,810),(447,832),(459,860),(451,874),(389,871),(326,855),(324,828),(331,794),(327,765),(315,749),(322,683),(286,670),(278,649),(266,632),(259,681),(256,739),(243,767),(249,808),(265,860),(260,899),(199,902),(181,886),(185,850),(196,821),(187,779),(167,765),(158,729),(160,688),(152,673),(108,682),(98,667),(73,651),(72,613),(86,555),(119,472),(126,427),(132,364),(156,321),(214,278),(266,263)],
[(240,126),(249,98),(282,76),(326,71),(365,80),(386,112),(383,156),(376,180),(382,209),(410,234),(425,301),(438,359),(439,417),(450,450),(442,477),(451,503),(448,553),(440,583),(411,587),(411,643),(414,704),(409,754),(397,774),(400,811),(429,830),(448,850),(450,871),(397,878),(337,857),(318,841),(322,811),(327,768),(309,754),(311,695),(312,654),(295,655),(286,694),(281,749),(267,772),(271,811),(278,852),(275,886),(265,901),(207,902),(196,884),(199,850),(206,816),(201,783),(184,762),(183,733),(195,680),(184,666),(147,653),(107,609),(109,567),(124,486),(138,414),(139,379),(140,337),(158,277),(171,227),(219,194),(247,191)]]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def rgba(idx):return tuple(map(int,P[idx]))+(255,)
def preview(im,scale=8):
 a=np.zeros((im.height,im.width,3),np.uint8)
 for y in range(im.height):
  for x in range(im.width):a[y,x]=(104,111,118) if (x//4+y//4)%2 else (125,130,136)
 b=Image.fromarray(a).convert('RGBA');b.alpha_composite(im);return b.convert('RGB').resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
def main(out):
 out.mkdir(parents=True,exist_ok=True)
 src=np.array(Image.open(SOURCE).convert('RGB')); frames=[]; chars=[]; logs=[]; masks=[]; baselines=[]
 # One fixed 3/4 timber stool, designed at target resolution from all source views.
 stool=Image.new('RGBA',(64,64));d=ImageDraw.Draw(stool)
 d.polygon([(21,44),(26,43),(31,44),(31,46),(21,46)],fill=rgba(20))
 d.polygon([(21,44),(26,43),(31,44),(26,45)],fill=rgba(22))
 d.rectangle((21,46,22,49),fill=rgba(21));d.rectangle((24,46,25,51),fill=rgba(21));d.line([(25,46),(25,51)],fill=rgba(22));d.rectangle((29,46,30,49),fill=rgba(20));d.line([(22,49),(24,50)],fill=rgba(21));d.point((24,51),fill=rgba(0))
 stool.save(out/'stool_fixed.png')
 for f,start in enumerate(STARTS):
  a=src[:,start:start+500]; poly=Image.new('L',(500,1024));ImageDraw.Draw(poly).polygon(POLYGONS[f],fill=255)
  bg=(np.ptp(a.astype(int),axis=2)<12)&(a.min(2)>48)
  labels,n=ndimage.label(~bg);counts=np.bincount(labels.ravel());counts[0]=0
  whole=labels==counts.argmax(); mask=whole & (np.array(poly)>0)
  cut=np.dstack([a,mask.astype(np.uint8)*255]);cut[~mask,:3]=0
  Image.fromarray(cut).save(out/f'source_character_{f:02}.png');poly.save(out/f'source_polygon_{f:02}.png')
  # Source pixels mapped to the SAME palette before majority-area sampling.
  flat=a.reshape(-1,3).astype(np.int32)
  dist=((flat[:,None,:]-P.astype(np.int32)[None,:,:])**2).sum(2)
  indices=dist.argmin(1).reshape(a.shape[:2]);native=np.zeros((64,64,4),np.uint8)
  for y in range(64):
   for x in range(64):
    xa,xb=int((x-19)/SCALE),int((x+1-19)/SCALE);ya,yb=int(902+(y-54)/SCALE),int(902+(y+1-54)/SCALE)
    if xa<0 or ya<0 or xb>500 or yb>1024:continue
    m=mask[ya:yb,xa:xb]
    if m.size and m.mean()>=.4:
     index=np.bincount(indices[ya:yb,xa:xb][m],minlength=len(P)).argmax();native[y,x]=rgba(index)
  baseline=Image.fromarray(native.copy());baseline.save(out/f'character_{f:02}_baseline.png');baselines.append(baseline)
  # Declared target-grid readability edits. No pose warp or frame-specific scale.
  edits=[[(29,31,0,'one-pixel eye'),(30,31,7,'face silhouette / nose'),(30,33,8,'grey stubble'),(28,36,23,'shoulder clasp'),(25,40,16,'pale cuff'),(33,40,16,'pale cuff'),(27,41,6,'near forearm'),(28,42,6,'near hand on thigh'),(29,42,7,'near hand highlight'),(29,43,6,'near fingers grouped'),(32,42,6,'far hand on thigh'),(32,43,5,'far fingers grouped'),(30,45,0,'trouser separation'),(27,50,20,'boot shadow')],
         [(33,28,0,'one-pixel eye'),(34,28,7,'face silhouette / nose'),(33,29,8,'grey stubble'),(31,32,23,'shoulder clasp'),(26,37,16,'pale cuff'),(34,37,16,'pale cuff'),(28,39,6,'forearm toward thigh'),(29,40,6,'hand on thigh'),(30,41,5,'grouped fingers'),(34,40,6,'far hand on thigh'),(35,41,5,'grouped far fingers')],
         [(33,23,0,'one-pixel eye'),(34,23,7,'face silhouette / nose'),(33,24,8,'grey stubble'),(31,28,23,'shoulder clasp'),(27,35,16,'pale cuff'),(36,35,16,'pale cuff')]][f]
  flog=[]
  zones=[[(23,38,26,40),(31,38,34,40),(27,38,30,40)],[(25,34,27,36),(33,34,35,36),(28,35,32,39)],[(26,31,28,33),(30,31,33,33),(29,36,34,39)]][f]
  for x0,y0,x1,y1 in zones:
   for yy in range(y0,y1+1):
    for xx in range(x0,x1+1):
     old=native[yy,xx].copy()
     if old[3] and tuple(old[:3]) in {tuple(P[j]) for j in [20,21,22,2,3]}:
      pi=12 if int(old[:3].sum())<230 else 13
      native[yy,xx]=rgba(pi);flog.append(dict(x=xx,y=yy,before=old.tolist(),after=native[yy,xx].tolist(),reason='semantic olive cloth simplification; suppress false leather/hair hue'))
  for x,y,index,reason in edits:
   before=native[y,x].tolist();native[y,x]=rgba(index);flog.append(dict(x=x,y=y,before=before,after=native[y,x].tolist(),reason=reason))
  ch=Image.fromarray(native);ch.save(out/f'character_{f:02}.png');chars.append(ch);logs.append(flog)
  fr=stool.copy();fr.alpha_composite(ch);fr.save(out/f'frame_{f:02}.png');frames.append(fr)
  preview(fr).save(out/f'frame_{f:02}_nearest_8x.png')
 sheet=Image.new('RGBA',(192,64))
 for i,f in enumerate(frames):sheet.paste(f,(i*64,0))
 sheet.save(out/'spritesheet.png');preview(sheet).save(out/'spritesheet_nearest_8x.png')
 anim=[preview(f,6) for f in frames]
 anim[0].save(out/'rise_motion.gif',save_all=True,append_images=anim[1:],duration=[900,450,1300],loop=0,disposal=2)
 # Static contact sheet: source, baseline with same stool, edited native (1x), edited 8x.
 board=Image.new('RGB',(1536,1100),(31,35,39));dd=ImageDraw.Draw(board)
 board.paste(Image.open(SOURCE).resize((960,640),Image.Resampling.NEAREST),(288,25))
 dd.text((12,8),'YANI | SOURCE CONCEPT / SHARED-SCALE 34px BUDGET STUDY | NOT ENGINE-READY',fill='white')
 for i in range(3):
  x=i*512;dd.text((x+10,650),['SEATED','LIFT / FORWARD','UPRIGHT'][i],fill='white')
  b=stool.copy();b.alpha_composite(baselines[i]);board.paste(preview(b,4),(x+5,680));board.paste(preview(frames[i],4),(x+251,680));board.paste(preview(frames[i],1),(x+224,968))
  dd.text((x+10,948),'BASELINE 4x          EDITED 4x',fill='white')
 dd.text((15,1060),'Fixed stool layer; same scale + floor transform. Generated pose drift remains. Standing does not mean recovery or enlistment.',fill='white')
 board.save(out/'comparison.png')
 # Critical-region detail is a nearest-neighbour inspection artifact, never a native sprite.
 detail=Image.new('RGB',(1008,592),(115,121,128));ddetail=ImageDraw.Draw(detail)
 for i,fr in enumerate(frames):
  cr=fr.crop((19,19,40,54)).resize((336,560),Image.Resampling.NEAREST);detail.paste(cr,(i*336,24),cr);ddetail.text((i*336+4,5),f'frame {i}: head / cuff / knee / stool / boot',fill='white')
 detail.save(out/'critical_details_nearest_16x.png')
 dump(out/'palette.json',[dict(index=i,name=n,hex=h) for i,(n,h) in enumerate(PALETTE)])
 dump(out/'pixel_edits.json',dict(character_edits=logs,stool='Entire single shared target-grid layer redrawn; coordinates and colors in build_pilot.py. Hidden areas are a design reconstruction, not source evidence.',masks='Three hand-traced source polygons remove changing stool; saved full-size masks. Background rejection threshold plus largest component.'))
 measurements=[]
 for i,(ch,fr) in enumerate(zip(chars,frames)):
  a=np.array(fr);c=np.array(ch);ys,xs=np.nonzero(c[:,:,3]);colors=np.unique(a[a[:,:,3]>0,:3],axis=0)
  assert set(np.unique(a[:,:,3]))=={0,255};assert not a[a[:,:,3]==0,:3].any()
  assert all(tuple(col) in set(map(tuple,P)) for col in colors)
  assert int(ys.max())==53
  assert (a[47:51,31,3]==0).all(), 'lower-leg negative space closed'
  assert (a[47:49,23,3]==0).all(), 'stool aperture closed'
  measurements.append(dict(lower_leg_gap_probe_clear=True,stool_aperture_probe_clear=True,frame=i,canvas=[64,64],character_bbox=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],character_visible_height=int(ys.max()-ys.min()+1),opaque_colors=len(colors),foot_lowest_row=int(ys.max()),binary_alpha=True,transparent_rgb_zero=True))
 # Test whether each silhouette can be explained by mere translation: best full-grid IoU.
 motion=[]
 for i in range(2):
  a=np.array(chars[i])[:,:,3]>0;b=np.array(chars[i+1])[:,:,3]>0;best=(0,None)
  for dy in range(-14,15):
   for dx in range(-10,11):
    moved=ndimage.shift(a.astype(np.uint8),(dy,dx),order=0,mode='constant')>0
    iou=(moved&b).sum()/max(1,(moved|b).sum())
    if iou>best[0]:best=(iou,[dx,dy])
  motion.append(dict(pair=[i,i+1],best_translation_iou=float(best[0]),best_translation=best[1],not_identical_under_translation=bool(best[0]<1)))
 source_files=[SOURCE,ROOT/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch01/02_yani_dialogue_poses.png',ROOT/'design/06_支线/城市支线/台本_CS-BRY-15_招募告示的背面.md',ROOT/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch66/manifest.json',ROOT/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch66/QA.json']
 manifest=dict(status='source_guided_designer_masked_pixel_study',source_files=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in source_files],uniform_scale=SCALE,standing_height_budget=34,canvas=[64,64],panel_source_x_offsets=STARTS,scene_anchor=dict(name='fixed scene registration, not engine origin',canvas_reference=[24,54],source_reference_per_frame=[[s+121.7647,902] for s in STARTS],definition='x=24 is a scene reference at the fixed front stool post; y=54 is the exclusive floor edge beneath the nearest boot. All frames use x_native=19+(x_source-panel_offset)*scale, y_native=54+(y_source-902)*scale.'),stool_layer_sha256=sha(out/'stool_fixed.png'),palette_size=len(P),dither=False,measurements=measurements,translation_test=motion,origin=None,collision=None,engineReady=False,runtimeVerified=False,dependencies=dict(python=platform.python_version(),pillow=pillow_version,numpy=np.__version__,scipy=scipy.__version__),outputs={p.name:sha(p) for p in sorted(out.iterdir()) if p.suffix in ['.png','.gif','.json'] and p.name not in ['manifest.json','QA-producer.json','QA-visual.json','QA-reproduction.json']})
 dump(out/'manifest.json',manifest)
 dump(out/'QA-producer.json',dict(binary_alpha=True,shared_palette=True,fixed_stool_layer=True,shared_scale=True,independent_bbox_normalization=False,measurements=measurements,translation_test=motion,visual_review='See QA-visual.json for explicit post-build visual inspection; programmatic checks do not certify anatomy or style.',limitations=['Source three poses change head angle, clothing folds and limb proportions; registration cannot repair all anatomy.','Three keyframes establish readable beat only; timing, balance, weight transfer and intermediate motion unverified.','Shared stool is a native design reconstruction; character masks and pixel readability edits are not automatic accurate extraction.','No healing, service acceptance, payout, invitation consent or state transition proven.']))
 print(json.dumps(dict(out=str(out),measurements=measurements,translation_test=motion),ensure_ascii=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=HERE);main(p.parse_args().out)
