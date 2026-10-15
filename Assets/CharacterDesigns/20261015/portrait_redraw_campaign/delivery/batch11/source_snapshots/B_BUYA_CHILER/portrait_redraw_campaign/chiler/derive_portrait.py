from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter
import base64, hashlib, json, sys
root=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(p):
 im=Image.open(p).convert("RGBA"); px=list(im.getdata()); colors=Counter(p[:3] for p in px if p[3]); a=Counter(p[3] for p in px)
 return {"path":str(p.relative_to(root)),"sha256":sha(p),"size":list(im.size),"mode":Image.open(p).mode,"visible_rgb_colors":len(colors),"alpha_values":sorted(a),"binary_alpha":set(a)<={0,255},"alpha_bbox":im.getchannel("A").getbbox(),"visible_pixels":sum(colors.values()),"partial_alpha_pixels":sum(n for v,n in a.items() if v not in (0,255)),"palette_by_frequency":[{"rgb":rgb,"pixels":n} for rgb,n in colors.most_common()] if len(colors)<=32 else None}
for ret in sorted((root/"tool_returns").glob("portrait_v*.json")):
 name=ret.stem; result=json.loads(ret.read_text()); data=base64.b64decode(result["image_url"].split(",",1)[1]); raw=root/"raw"/f"{name}_raw_imagegen.png"; raw.write_bytes(data)
 im=Image.open(raw).convert("RGBA").resize((74,100),Image.Resampling.NEAREST)
 alpha=im.getchannel("A").point(lambda x:255 if x>=128 else 0)
 visible=[p[:3] for p,a in zip(im.getdata(),alpha.getdata()) if a]
 strip=Image.new("RGB",(len(visible),1));strip.putdata(visible)
 pal=strip.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 q=im.convert("RGB").quantize(palette=pal,dither=Image.Dither.NONE).convert("RGBA");q.putalpha(alpha);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
 out=root/"candidates"/f"{name}_74x100_candidate.png";q.save(out)
 big=q.resize((592,800),Image.Resampling.NEAREST);big.save(root/"previews"/f"{name}_8x.png")
 board=Image.new("RGB",(1030,1050),(105,105,105));d=ImageDraw.Draw(board);d.text((16,14),f"{json.loads((root/'sources/roster_entry.json').read_text())['suggested_slug'].upper()} / {name} / 74x100 / NN + QUANTIZED DERIVATIVE",fill="white");d.text((16,38),"1x on black, gray, light | 8x below | NOT native-pixel final",fill="white")
 for i,bg in enumerate([(12,12,15),(105,105,105),(235,235,229)]):
  tile=Image.new("RGBA",(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert("RGB"),(16+100*i,65))
 board.paste(big,(16,200),big)
 for i,(f,label) in enumerate([("mara_style_reference.png","Mara v2"),("iwo_style_reference.png","Iwo v1"),("leiya_style_reference.png","Leiya v2"),("tore_style_reference.png","Tore v1")]):
  x=650+(i%2)*180;y=200+(i//2)*280; ref=Image.open(root/"sources"/f).convert("RGBA").resize((148,200),Image.Resampling.NEAREST);board.paste(ref,(x,y),ref);d.text((x,y+210),label,fill="white")
 board.save(root/"previews"/f"{name}_1x_8x.png")
 m={"raw":metrics(raw),"target":metrics(out),"raw_equals_full_tool_return":raw.read_bytes()==data,"native_target_generation":False,"derivation":{"resize":"Pillow NEAREST entire canvas","crop":None,"alpha_threshold":128,"quantization":"Pillow MEDIANCUT from opaque sampled RGB, 32 colors, no dithering","transparent_rgb":"zeroed for alpha 0","character_geometry_redrawn_by_script":False},"checks":{"dimensions":q.size==(74,100),"binary_alpha":set(q.getchannel("A").getdata())<={0,255},"visible_color_budget":len(set(p[:3] for p in q.getdata() if p[3]))<=32}}
 (root/"qa"/f"{name}_metrics.json").write_text(json.dumps(m,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps({"candidate":str(out),"size":m["target"]["size"],"colors":m["target"]["visible_rgb_colors"],"sha256":sha(out)}))
