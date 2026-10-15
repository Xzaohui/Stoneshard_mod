#!/usr/bin/env python3
"""Layout only: byte-identical candidate copies and integer nearest previews."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size, index=2)

def main():
    config = json.loads((HERE / 'review_config.json').read_text())
    portraits = config['portraits']
    before = {p['source']: sha(ROOT / p['source']) for p in portraits}
    canvas = Image.new('RGBA', (1380, 1130), '#14171b')
    d = ImageDraw.Draw(canvas)
    white, gray, amber = '#eeeae1', '#b1b7bf', '#dec497'
    placements = []
    text_boxes = []

    def text(x, y, value, size=22, color=white, bold=False):
        f = font(size, bold)
        box = d.textbbox((x, y), value, font=f)
        assert box[2] <= 1340 and box[3] <= 1110, (value, box)
        d.text((x, y), value, font=f, fill=color)
        text_boxes.append({'text': value, 'bbox': list(box)})

    def asset(path, x, y, scale):
        src = Image.open(path).convert('RGBA')
        assert src.size == (74, 100)
        scaled = src if scale == 1 else src.resize((74 * scale, 100 * scale), Image.Resampling.NEAREST)
        for yy in range(y, y + scaled.height, 8):
            for xx in range(x, x + scaled.width, 8):
                c = '#1a1d22' if ((xx-x)//8 + (yy-y)//8) % 2 else '#272b32'
                d.rectangle((xx, yy, min(xx+7, x+scaled.width-1), min(yy+7, y+scaled.height-1)), fill=c)
        canvas.alpha_composite(scaled, (x, y))
        placements.append({'source': str(path.relative_to(ROOT)), 'position': [x, y], 'integer_scale': scale, 'source_size': [74,100], 'resampling': 'NEAREST'})

    text(40, 28, '蕾雅与托雷 · 续作头像验收', 38, bold=True)
    text(40, 92, '两张 74 × 100 候选  /  独立 QA：candidate  /  待用户审美确认', 24, amber)
    for i, p in enumerate(portraits):
        x = 40 + 670*i
        path = ROOT / p['source']
        assert sha(path) == p['sha256']
        shutil.copyfile(path, HERE / p['delivery_name'])
        assert sha(path) == sha(HERE / p['delivery_name'])
        d.rounded_rectangle((x,160,x+630,916), radius=12, fill='#1c2026', outline='#39414b', width=2)
        text(x+24, 180, p['title'], 29, bold=True)
        text(x+24, 228, p['identity'], 20, gray)
        text(x+44, 388, '原尺寸 1×', 20, gray)
        text(x+210, 254, '整数 5× · nearest', 20, gray)
        asset(path, x+52, 448, 1)
        asset(path, x+210, 290, 5)
        text(x+24, 815, p['notes'][0], 21, amber)
        text(x+24, 852, p['notes'][1], 21, gray)
    d.rounded_rectangle((40,944,1340,1030), radius=8, fill='#2a2021', outline='#674b45', width=1)
    text(60, 954, '伊沃地图新方法：1 次实验未通过，已停止生成。', 23, '#edaf9c', True)
    text(60, 992, '失败过程与独立 QA 保留在源码包中，不计为合格地图素材。', 21, gray)
    text(40, 1050, '头像由高分辨率生成图机械派生，不是 native_final；未接入游戏或完成运行验收。', 21, gray)
    text(40, 1080, '本页仅布局原尺寸图与整数 nearest 放大；没有补画、重绘或修改候选像素。', 20, gray)
    out = HERE / 'native_style_continuation_review_20261015.png'
    canvas.convert('RGB').save(out)
    assert before == {p['source']: sha(ROOT / p['source']) for p in portraits}
    report = {'layout_only': True, 'source_assets_unchanged': True, 'candidate_copies_byte_identical': True, 'overview_size': [1380,1130], 'source_sha256': before, 'placements': placements, 'text_boxes': text_boxes, 'overview_sha256': sha(out), 'visual_review': 'pending'}
    (HERE / 'layout_verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'overview':str(out),'sha256':sha(out)},ensure_ascii=False))

if __name__ == '__main__':
    main()
