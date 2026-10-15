from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import hashlib, json

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'Assets/CharacterActions/20261013/new_story').is_dir())
BASE = ROOT / 'Assets/CharacterActions/20261013/new_story'
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
F = ImageFont.truetype(FONT, 30)
S = ImageFont.truetype(FONT, 22)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
selection = {'deru': [('deru_A1_check_blunt_chisel', 2), ('deru_A2_gather_apron_crouch', 1)], 'hoer': [('hoer_A1_press_workworn_palm', 2), ('hoer_A2_brace_thighs_listen', 1)]}

def place(canvas, img, box):
    x, y, w, h = box
    n = img.copy()
    n.thumbnail((w, h), Image.Resampling.NEAREST)
    canvas.alpha_composite(n, (x + (w-n.width)//2, y+(h-n.height)//2))

for slug, plans in selection.items():
    d = BASE/slug/'noncombat_basics_v1'
    if not d.exists():
        continue
    brief = json.loads((d/'sources/second_new_character_actions_brief.json').read_text())
    c = next(x for x in brief['characters'] if x['slug'] == slug)
    assets = []
    images = []
    for (key, version), p in zip(plans, c['plans']):
        raw = d/'raw'/f'{key}_v{version}.png'
        img = Image.open(raw).convert('RGBA')
        a = np.array(img)
        old = a.copy()
        a[:,:,3] = np.where(a[:,:,3] >= 128, 255, 0)
        a[a[:,:,3] == 0, :3] = 0
        img = Image.fromarray(a)
        out = d/'exports'/f'{key}_transparent.png'
        img.save(out)
        assets.append({'key': key, 'title_zh':p['title_zh'], 'selected_version':version, 'raw':str(raw.relative_to(d)), 'raw_sha256':sha(raw), 'export':str(out.relative_to(d)), 'export_sha256':sha(out), 'raw_size':list(img.size), 'mode':'RGBA', 'processing':'Alpha threshold 128 only, hidden RGB set to zero. No visible RGB edits, body drawing, scaling, cropping, quantization, rotations or deformation.', 'alpha_values':[0,255], 'alpha_bbox':img.getbbox(), 'opaque_pixels':int(np.sum(a[:,:,3]==255)), 'alpha_zero_pixels':int(np.sum(a[:,:,3]==0)), 'visible_rgb_unchanged':bool(np.array_equal(a[a[:,:,3]>0,:3],old[a[:,:,3]>0,:3])), 'story_state_change':False, 'animation':False, 'runtime_verified':False, 'independent_review':'pending'})
        images.append(img)
        for theme, bg, fg in [('light',(237,233,222,255),(35,35,35)),('dark',(31,36,42,255),(237,233,222))]:
            board=Image.new('RGBA',(img.width+120,img.height+190),bg)
            board.alpha_composite(img,(60,125))
            draw=ImageDraw.Draw(board)
            draw.text((32,18),c['name']+'｜'+p['title_zh'],font=F,fill=fg)
            draw.text((32,66),'独立动作关键姿态 · 透明像素概念',font=S,fill=fg)
            draw.text((32,board.height-47),'仅为身体动作提案，不表示任务完成或游戏验证。',font=S,fill=fg)
            board.convert('RGB').save(d/'review'/f'{key}_{theme}.png')
    for theme,bg,fg in [('light',(237,233,222,255),(35,35,35)),('dark',(31,36,42,255),(237,233,222))]:
        board=Image.new('RGBA',(1800,1120),bg)
        draw=ImageDraw.Draw(board)
        draw.text((28,16),c['name']+'｜母图与两种独立动作',font=F,fill=fg)
        allimages=[Image.open(d/'sources'/f'{slug}_anchor.png').convert('RGBA')]+images
        labels=['母图 · 身份与衣装参照']+[p['title_zh'] for p in c['plans']]
        for i,(img,label) in enumerate(zip(allimages,labels)):
            draw.text((i*600+25,70),label,font=S,fill=fg)
            place(board,img,(i*600+25,120,550,915))
        draw.text((28,1068),'两张独立姿态；不构成连续动画，不声明剧情进展或引擎落地。',font=S,fill=fg)
        board.convert('RGB').save(d/'review'/f'{slug}_comparison_{theme}.png')
    (d/'asset_catalog.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n')
    (d/'selection_versions.json').write_text(json.dumps(dict(plans),ensure_ascii=False,indent=2)+'\n')
    print(slug, json.dumps(assets,ensure_ascii=False))
