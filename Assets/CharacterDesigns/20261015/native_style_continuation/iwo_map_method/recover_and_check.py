"""Mechanical grid recovery and inspection only; never authors body/face pixels.
Fixed full-canvas 35x44 cells. No crop, fit, warp, manual palette, or per-pixel edits.
"""
from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter
import numpy as np
import json,hashlib
R=Path(__file__).resolve().parent
REPO=R.parents[4]
NATIVE=REPO/'Assets/ReferenceAudit/20261013/originals/s_npc_carpenter_0.png'
OLD=REPO/'Assets/CharacterDesigns/20261015/native_style_pilot/iwo/raw/map_v2_raw_imagegen.png'
OLD_SMALL=REPO/'Assets/CharacterDesigns/20261015/native_style_pilot/iwo/candidates/map_v2_35x44_candidate.png'
RAW=R/'raw/map_method_v1_raw_imagegen.png'
SIZE=(35,44)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def labels(im):
    a=np.asarray(im);p=im.convert('RGB').quantize(colors=20,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    q=np.asarray(p).astype('int16');q[a[:,:,3]<128]=-1
    return q,np.array(p.getpalette(),dtype='uint8').reshape(-1,3)
def analyze_grid(im,export=False):
    q,palette=labels(im);cdom=[];fdom=[];out=np.zeros((44,35,4),dtype='uint8');cells=[]
    for y in range(44):
        for x in range(35):
            x0,x1=round(x*im.width/35),round((x+1)*im.width/35)
            y0,y1=round(y*im.height/44),round((y+1)*im.height/44)
            b=q[y0:y1,x0:x1];dx=(x1-x0)//4;dy=(y1-y0)//4
            c=b[dy:b.shape[0]-dy,dx:b.shape[1]-dx]
            vals,cts=np.unique(c,return_counts=True);idx=int(vals[np.argmax(cts)])
            opaque_fraction=float((c>=0).sum()/c.size)
            if idx>=0:out[y,x,:3]=palette[idx];out[y,x,3]=255
            active=opaque_fraction>.5
            cd=float(cts.max()/c.size);fd=float(np.unique(b,return_counts=True)[1].max()/b.size)
            if active:cdom.append(cd);fdom.append(fd)
            if export:cells.append({'x':x,'y':y,'source_cell':[x0,y0,x1,y1],'center_dominance':round(cd,6),'full_cell_dominance':round(fd,6),'center_opaque_fraction':round(opaque_fraction,6),'chosen_palette_index':idx})
    report={'raw_size':list(im.size),'fixed_grid':[35,44],'source_cell_width':im.width/35,'source_cell_height':im.height/44,'active_center_cells':len(cdom),'center_dominance_mean':float(np.mean(cdom)),'center_dominance_p10':float(np.percentile(cdom,10)),'full_cell_dominance_mean':float(np.mean(fdom))}
    report['grid_consistency_gate']=report['center_dominance_mean']>=.90 and report['center_dominance_p10']>=.80 and report['full_cell_dominance_mean']>=.80
    return Image.fromarray(out),report,cells

def info(p):
    im=Image.open(p).convert('RGBA');a=np.asarray(im);vis=a[:,:,3]>0
    rgb=np.unique(a[vis,:3],axis=0);alpha=np.unique(a[:,:,3]);box=im.getchannel('A').getbbox()
    return {'path':str(p),'sha256':sha(p),'size':list(im.size),'visible_bbox':list(box) if box else None,'visible_size':[box[2]-box[0],box[3]-box[1]] if box else None,'alpha_ge128_bbox':list(im.getchannel('A').point(lambda v: 255 if v>=128 else 0).getbbox()),'visible_rgb_colors':len(rgb),'alpha_levels':len(alpha),'binary_alpha':set(alpha.tolist())<={0,255},'transparent_nonzero_rgb':int(((a[:,:,3]==0)&(a[:,:,:3]!=0).any(axis=2)).sum())}
raw=Image.open(RAW).convert('RGBA');out,metrics,cells=analyze_grid(raw,True)
outpath=R/'derived/map_method_v1_fixed_grid_35x44_experimental.png';out.save(outpath)
native=Image.open(NATIVE).convert('RGBA');_,nmetrics,_=analyze_grid(native.resize((1120,1408),Image.Resampling.NEAREST))
_,ometrics,_=analyze_grid(Image.open(OLD).convert('RGBA'))
operation={'input':str(RAW.relative_to(R)),'output':str(outpath.relative_to(R)),'full_canvas_recovery':True,'crop':False,'fit':False,'grid':[35,44],'color_quantization':'Pillow MEDIANCUT to 20 colors, no dither, whole RGB canvas','alpha_threshold_before_recovery':128,'representative_per_cell':'Most frequent quantized label (including transparency) in central half-width/half-height rectangle. Ties: lowest label. One output pixel per fixed cell.','transparent_rgb':'zero','manual_character_pixel_edits':False,'generation':'Built-in imagegen, one initial experiment, no revisions','native_reference_usage':'Read-only grid/style/proportion reference; not edit target. Edit target was our own previous failed sprite.'}
qa={'operation':operation,'grid_gate_definition':{'center_dominance_mean_min':.9,'center_dominance_p10_min':.8,'full_cell_dominance_mean_min':.8,'scope':'Diagnostic coarse-grid rejection criterion, not proof of artistic quality. Quantization can hide color variance. Must also inspect raw, face clusters and 1x image.'},'grid_results':{'native_control':nmetrics,'previous_failed_raw_control':ometrics,'experiment_v1':metrics},'images':[info(RAW),info(outpath)],'visual_grade':'fail; producer and independent visual QA agree','independent_visual_qa':'Auditor viewed raw and 1x/12x comparison. Eyes remain vertical dark columns joined to brow/hair; jaw and collar are congested. Fixed-cell mode is reproducible resampling, not recovered native design. No defensible targeted revision identified. Separate auditor measurement/report follows in audit directory.','producer_visual_review':'Face dark-column severity is reduced and visible size is 20x34, but raw does not maintain the requested 35x44 grid. Fixed-grid extraction changes pixel clusters; vertical eyes and lower-face/collar congestion remain. Not a native-qualified map sprite.','native_qualified':False,'runtime_integrated':False}
(R/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
(R/'grid_cells.json').write_text(json.dumps(cells,ensure_ascii=False,indent=2))
board=Image.new('RGB',(1220,690),(107,107,107));d=ImageDraw.Draw(board)
d.text((20,12),'READ-ONLY NATIVE | PREVIOUS FAILED IVO | NEW FIXED-GRID EXPERIMENT',fill='white')
d.text((20,32),'1x at top, 12x nearest-neighbor below. New output is experimental, not approved.',fill='white')
for x,im,title in [(20,native,'Native reference'),(420,Image.open(OLD_SMALL).convert('RGBA'),'Previous failed v2'),(820,out,'New experiment v1')]:
    d.text((x,62),title,fill='white')
    for i,bg in enumerate([(15,15,17),(107,107,107),(235,235,225)]):
        t=Image.new('RGBA',im.size,bg+(255,));t.alpha_composite(im);board.paste(t.convert('RGB'),(x+i*55,90))
    large=im.resize((420,528),Image.Resampling.NEAREST);board.paste(large,(x-10,150),large)
board.save(R/'review/native_old_new_1x_12x.png')
# Raw image scaled only for review, no output manufacturing.
view=Image.new('RGB',(730,1030),(107,107,107));rr=raw.copy();rr.thumbnail((700,970));view.paste(rr,((730-rr.width)//2,40),rr);ImageDraw.Draw(view).text((10,10),'RAW imagegen: 1070x1470, not a native-size file',fill='white');view.save(R/'review/raw_view.png')
files=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(R.rglob('*')) if p.is_file() and p.name!='manifest.json']
(R/'manifest.json').write_text(json.dumps({'date':'2026-10-15','character':'Ivo / NPC-N-IVO / n1_ivo','operation':operation,'native_qualified':False,'files':files},ensure_ascii=False,indent=2))
print(json.dumps({'grid_results':qa['grid_results'],'images':qa['images']},indent=2))
