from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json, hashlib, shutil

r = Path(__file__).resolve()
while r.name != 'Stoneshard_mod':
    r = r.parent
b = r / 'Assets/CharacterActions/20261013/new_story'
delivery = b / 'sixth_noncombat_erwei_chenger_delivery_v1'
delivery.mkdir(exist_ok=True)
font = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f_title = ImageFont.truetype(font, 43)
f_label = ImageFont.truetype(font, 29)
f_note = ImageFont.truetype(font, 25)
width, row_height, top, bottom, cell_width = 2240, 790, 150, 80, 720
board = Image.new('RGB', (width, top + 4 * row_height + bottom), '#f4efe3')
d = ImageDraw.Draw(board)
d.text((40, 24), '珥薇 / 埕珥 · 日常基础动作', font=f_title, fill='#2b2c28')
d.text((40, 86), '母图与动作浅底 / 深底对照 · 4 张独立全身关键姿态', font=f_note, fill='#535650')
characters = [
    ('erwei', '珥薇', [('erwei_A1_low_lift_pot_by_two_ears_v1', '双手握两耳低提旧锅'), ('erwei_A2_smooth_right_apron_patch_v2', '右掌按平围裙赭补片')]),
    ('chenger', '埕珥', [('chenger_A1_press_left_outer_blanket_v1', '坐姿按稳左上臂外毯'), ('chenger_A2_seated_reach_grounded_lantern_ring_v1', '坐稳侧俯握原灯环')]),
]
placements = []
row = 0
for slug, name, actions in characters:
    mother = r / f'Assets/CharacterDesigns/20261013/expressive/new_story/{slug}/concept_v1/{slug}_transparent.png'
    images = [(mother, '母图 · 身份锚')] + [(b / slug / 'noncombat_basics_v1/exports' / f'{key}_transparent.png', title) for key, title in actions]
    # The same factor is used for mother and every action. No body crop, warping, or pose-normalization.
    scale = 0.47
    for tone, color, ink in [('浅底', (239, 233, 219), (43, 44, 40)), ('深底', (29, 34, 38), (242, 235, 219))]:
        y0 = top + row * row_height
        d.rectangle((0, y0, width, y0 + row_height - 1), fill=color)
        for col, (path, title) in enumerate(images):
            x0 = 40 + col * cell_width
            label = f'{name} · {tone} · {title}'
            d.text((x0 + 12, y0 + 17), label, font=f_label, fill=ink)
            im = Image.open(path).convert('RGBA')
            size = (round(im.width * scale), round(im.height * scale))
            preview = im.resize(size, Image.Resampling.NEAREST)
            xy = (x0 + (cell_width - size[0]) // 2, y0 + row_height - 16 - size[1])
            board.paste(preview, xy, preview)
            placements.append({'row': row, 'column': col, 'character': slug, 'tone': tone, 'label': label, 'source': str(path.relative_to(r)), 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'source_size': list(im.size), 'scale': scale, 'resample': 'NEAREST', 'target_size': list(size), 'paste_xy': list(xy), 'body_crop_or_stretch': False})
        row += 1
d.text((40, board.height - 57), '日常动作概念；非连续动画，不代表游戏内落地或剧情结果。', font=f_note, fill='#535650')
out = delivery / '珥薇_埕珥_母图动作浅深对照.png'
board.save(out)
layout = {'board': str(out.relative_to(r)), 'board_size': list(board.size), 'sha256': hashlib.sha256(out.read_bytes()).hexdigest(), 'placements': placements, 'method': 'Exact RGBA source composited on true light/dark backgrounds at one shared isotropic factor using nearest-neighbor; labels only.'}
for slug, _, _ in characters:
    p = b / slug / 'noncombat_basics_v1'
    shutil.copyfile(out, p / 'review' / out.name)
    (p / 'review/board_layout.json').write_text(json.dumps(layout, ensure_ascii=False, indent=2) + '\n')
(delivery / 'board_layout.json').write_text(json.dumps(layout, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'board': str(out), 'size': board.size, 'sha256': layout['sha256']}))
