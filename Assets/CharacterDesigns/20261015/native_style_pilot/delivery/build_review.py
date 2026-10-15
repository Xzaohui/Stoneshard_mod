#!/usr/bin/env python3
"""Layout-only review sheet. Never paints, retouches or mutates source assets."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size, index=2)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

PORTRAITS = [
    ('玛拉', 'v2', ROOT / 'mara/assets/portrait_v2_74x100.png', 'mara_portrait_v2_74x100_candidate.png',
     ['鼻翼、颧骨与担忧表情', '可读；待确认整体画风。', '', '仍需审视：', '眼睛略大、侧边发卷偏密。']),
    ('伊沃', 'v1', ROOT / 'iwo/candidates/portrait_v1_74x100_candidate.png', 'iwo_portrait_v1_74x100_candidate.png',
     ['帽子、成年面貌与', '鼻颧体积可读。', '', '仍需审视：', '脸部占比与像素色阶。']),
]
MAPS = [
    ROOT / 'mara/assets/map_v2_35x44.png',
    ROOT / 'iwo/candidates/map_v2_35x44_candidate.png',
]

def main():
    HERE.mkdir(exist_ok=True)
    inputs = [p[2] for p in PORTRAITS] + MAPS
    before = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    for _, _, src, dest, _ in PORTRAITS:
        with Image.open(src) as im:
            assert im.size == (74, 100)
        shutil.copyfile(src, HERE / dest)
        assert sha(src) == sha(HERE / dest)
    canvas = Image.new('RGBA', (1420, 1320), '#141619')
    d = ImageDraw.Draw(canvas)
    white, gray, amber, red = '#f0eee7', '#afb4bd', '#dfc78f', '#ed9c89'

    def text(x, y, value, size=22, color=white, bold=False):
        d.text((x, y), value, font=font(size, bold), fill=color)

    placements = []
    def asset(path, x, y, scale):
        src = Image.open(path).convert('RGBA')
        preview = src if scale == 1 else src.resize((src.width * scale, src.height * scale), Image.Resampling.NEAREST)
        for yy in range(y, y + preview.height, 8):
            for xx in range(x, x + preview.width, 8):
                c = '#17191c' if ((xx-x)//8 + (yy-y)//8) % 2 else '#22252a'
                d.rectangle((xx, yy, min(xx+7, x+preview.width-1), min(yy+7, y+preview.height-1)), fill=c)
        canvas.alpha_composite(preview, (x, y))
        placements.append({'source': str(path.relative_to(ROOT)), 'position': [x, y], 'integer_scale': scale, 'resampling': 'NEAREST', 'source_size': list(src.size)})

    text(40, 30, '首批原版风格试制 · 验收总览', 36, bold=True)
    text(40, 90, '头像：2张候选，待审美验收   |   地图小人：2项未通过', 23, amber)
    d.line((40, 142, 1380, 142), fill='#3c4149', width=2)
    text(40, 158, '头像候选  ·  candidate', 25, amber, True)
    text(954, 158, '失败记录  ·  不作正式选用', 25, red, True)
    d.line((920, 158, 920, 1128), fill='#3c4149', width=2)

    for i, (name, version, path, dest, notes) in enumerate(PORTRAITS):
        top = 200 + i * 480
        text(40, top, f'{name}  /  头像 {version}', 25, white, True)
        text(80, top+42, '1×', 20, gray)
        text(250, top+42, '4× nearest', 20, gray)
        asset(path, 80, top+174, 1)
        asset(path, 250, top+70, 4)
        text(586, top+88, '74 × 100 px', 24, amber, True)
        text(586, top+132, '二值透明 PNG', 20, gray)
        for j, line in enumerate(notes):
            text(586, top+202+j*31, line, 20, gray)
        map_top = top
        d.rounded_rectangle((950, map_top, 1380, map_top+415), radius=10, fill='#211e20', outline='#62443f', width=1)
        text(970, map_top+16, f'{name}地图  /  v1、v2 均未通过', 21, red, True)
        text(970, map_top+55, '下图为 v2 失败预览', 19, gray)
        text(982, map_top+96, '1×', 18, gray)
        text(1080, map_top+96, '4× nearest', 18, gray)
        asset(MAPS[i], 982, map_top+181, 1)
        asset(MAPS[i], 1080, map_top+130, 4)
        notes_map = (['缩小后仍有大眼娃娃感，', '轮廓偏瘦长；未达到目标比例。'] if i == 0 else
                     ['缩小后眼部暗块合并、下脸过黑；', '像素组织与身体比例仍不符。'])
        for j, line in enumerate(notes_map):
            text(970, map_top+332+j*30, line, 19, gray)

    d.line((40, 1165, 1380, 1165), fill='#3c4149', width=2)
    text(40, 1182, '说明', 22, amber, True)
    text(108, 1182, '原图由高分辨率生成，再派生到目标尺寸；候选不等于 native_final。', 22, gray)
    text(108, 1220, '尺寸、色数与透明检查通过，不证明原生逐像素制作；未接入游戏或运行验收。', 22, gray)
    text(108, 1258, '本页只布局原图与整数 nearest 放大，没有补画、重绘或改变角色形体。', 20, gray)
    out = HERE / 'native_style_pilot_review_20261015.png'
    canvas.convert('RGB').save(out)
    assert before == {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    for _, _, src, dest, _ in PORTRAITS:
        assert sha(src) == sha(HERE / dest)
    (HERE / 'layout_verification.json').write_text(json.dumps({
        'layout_only': True, 'source_assets_unchanged': True, 'portrait_copies_byte_identical': True,
        'overview_size': [1420, 1320], 'source_sha256': before, 'placements': placements,
        'notes': '1x and integer nearest enlarged source assets are alpha-composited on a checkerboard without image editing.'
    }, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'overview': str(out), 'size': [1420, 1320], 'sha256': sha(out)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
