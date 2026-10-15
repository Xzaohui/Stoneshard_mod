"""Create diagnostic-only edge crops; no actor image is changed."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
Q=Path(__file__).resolve().parent;CAMP=Q.parent.parent
src=CAMP/'reha/raw/portrait_v2_raw_imagegen.png';im=Image.open(src).convert('RGBA');x=im.width-1
pixels=[{'x':x,'y':y,'rgba':list(im.getpixel((x,y)))} for y in range(im.height) if im.getpixel((x,y))[3]>5]
opaque=[p for p in pixels if p['rgba'][3]>=128]
record={'actor':'reha','decision':'held_source_clipping','source':str(src.relative_to(CAMP)),'raw_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'dimensions':list(im.size),'rightmost_x':x,'right_edge_alpha_gt5_pixels':pixels,'right_edge_alpha_ge128_pixels':opaque,'right_edge_alpha_ge128_count':len(opaque),'right_edge_max_alpha':max(im.getpixel((x,y))[3] for y in range(im.height)),'visual_finding':'The right hair curl terminates against the original source canvas. Inset export merely adds external target padding and cannot restore missing hair.','no_third_generation':True,'v1_not_approved_as_fallback':True,'diagnostic_crop_box':[930,450,1078,610],'diagnostic_scale':4,'image_method':'Crop only for evidence, composite on light/dark background, integer NEAREST x4. The red line is OUTSIDE the original right canvas boundary. No source pixels redrawn.'}
assert len(opaque)==16 and [p['y'] for p in opaque]==list(range(531,547))
(Q/'reha_v2_edge_pixels.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
patch=im.crop((930,450,1078,610));board=Image.new('RGB',(1260,780),(64,64,64));d=ImageDraw.Draw(board)
d.text((20,12),'REHA V2 - HELD: original right hair reaches/crosses source boundary',fill='white')
d.text((20,32),f'Raw {im.width}x{im.height}; x={x}; alpha>=128: 16 pixels, y=531..546; max alpha=254',fill='white')
d.text((20,52),'Diagnostic crops: x930..1077 / y450..609; exact 4x NN; red line OUTSIDE original boundary',fill='white')
for ox,color,label in [(20,(235,230,219),'LIGHT'),(640,(18,18,20),'DARK')]:
 bg=Image.new('RGBA',patch.size,(*color,255));bg.alpha_composite(patch);panel=bg.resize((592,640),Image.Resampling.NEAREST).convert('RGB');board.paste(panel,(ox,96));d.text((ox,78),label,fill='white');d.line([(ox+592,96),(ox+592,735)],fill=(255,70,70),width=3)
 # An outside marker identifies the opaque edge span without painting the evidence.
 y1=96+(531-450)*4;y2=96+(546-450+1)*4-1;d.line([(ox+599,y1),(ox+599,y2)],fill=(255,220,40),width=4)
d.text((20,752),'No source alteration. The candidate inset border is not a repair. See reha_v2_edge_pixels.json for exact RGBA.',fill='white')
board.save(Q/'reha_v2_right_edge_evidence.png')
print(json.dumps({'raw_sha256':record['raw_sha256'],'opaque_edge_pixels':len(opaque),'evidence_image_sha256':hashlib.sha256((Q/'reha_v2_right_edge_evidence.png').read_bytes()).hexdigest()}))
