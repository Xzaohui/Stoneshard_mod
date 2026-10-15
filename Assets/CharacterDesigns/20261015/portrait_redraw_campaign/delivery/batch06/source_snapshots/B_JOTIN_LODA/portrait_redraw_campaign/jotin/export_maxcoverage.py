from pathlib import Path
from PIL import Image,ImageDraw
from collections import Counter
import json,hashlib,sys
r=Path(__file__).resolve().parent
v=sys.argv[1] if len(sys.argv)>1 else "portrait_v2"
raw=r/"raw"/f"{v}_raw_imagegen.png"; im=Image.open(raw).convert("RGBA").resize((74,100),Image.Resampling.NEAREST)
alpha=im.getchannel("A").point(lambda a:255 if a>=128 else 0)
visible=[p[:3] for p,a in zip(im.getdata(),alpha.getdata()) if a]
strip=Image.new("RGB",(len(visible),1));strip.putdata(visible)
palette=strip.quantize(colors=32,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE)
q=im.convert("RGB").quantize(palette=palette,dither=Image.Dither.NONE).convert("RGBA");q.putalpha(alpha);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
name=v+"_maxcoverage"; out=r/"candidates"/f"{name}_74x100_candidate.png";q.save(out)
big=q.resize((592,800),Image.Resampling.NEAREST);big.save(r/"previews"/f"{name}_8x.png")
b=Image.new("RGB",(1030,1050),(105,105,105));d=ImageDraw.Draw(b);d.text((16,14),f"{r.name.upper()} / {name} / 74x100 NN + MAXCOVERAGE DERIVATIVE",fill="white");d.text((16,38),"1x on black, gray, light | 8x below | NOT native-pixel final",fill="white")
for i,bg in enumerate([(12,12,15),(105,105,105),(235,235,229)]):
 t=Image.new("RGBA",(74,100),bg+(255,));t.alpha_composite(q);b.paste(t.convert("RGB"),(16+100*i,65))
b.paste(big,(16,200),big)
for i,(f,label) in enumerate([("mara_style_reference.png","Mara v2"),("iwo_style_reference.png","Iwo v1"),("leiya_style_reference.png","Leiya v2"),("tore_style_reference.png","Tore v1")]):
 x=650+(i%2)*180;y=200+(i//2)*280;ref=Image.open(r/"sources"/f).convert("RGBA").resize((148,200),Image.Resampling.NEAREST);b.paste(ref,(x,y),ref);d.text((x,y+210),label,fill="white")
b.save(r/"previews"/f"{name}_1x_8x.png")
m=json.loads((r/"qa"/f"{v}_metrics.json").read_text()); colors=Counter(p[:3] for p in q.getdata() if p[3]); a=Counter(q.getchannel("A").getdata())
m["target"]={"path":str(out.relative_to(r)),"sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"size":list(q.size),"mode":q.mode,"visible_rgb_colors":len(colors),"alpha_values":sorted(a),"binary_alpha":set(a)<={0,255},"alpha_bbox":q.getchannel("A").getbbox(),"visible_pixels":sum(colors.values()),"partial_alpha_pixels":0,"palette_by_frequency":[{"rgb":rgb,"pixels":n} for rgb,n in colors.most_common()]}
m["derivation"]["quantization"]="Pillow MAXCOVERAGE from opaque sampled RGB, 32 colors, no dithering";m["same_raw_technical_variant"]=True;m["additional_imagegen_call"]=False
(r/"qa"/f"{name}_metrics.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({"candidate":str(out),"sha256":m["target"]["sha256"],"colors":len(colors)}))
