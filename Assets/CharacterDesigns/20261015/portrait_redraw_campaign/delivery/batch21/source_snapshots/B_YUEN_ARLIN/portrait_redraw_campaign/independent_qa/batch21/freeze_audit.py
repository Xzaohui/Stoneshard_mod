#!/usr/bin/env python3
"""Freeze independent batch21 QA. Production sources are strictly read-only."""
from pathlib import Path
import datetime, hashlib, json, re
from PIL import Image, ImageDraw
OUT = Path(__file__).resolve().parent
CAMP = OUT.parent.parent
REPO = CAMP.parents[3]
SLUGS = ('tafei', 'xielan', 'yuen', 'arlin')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())
audit = load(OUT / 'final_technical_audit.json')
replay = load(OUT / 'final_derivation_replay.json')
reviews = load(OUT / 'final_visual_reviews.json')['actors']
preflight = load(OUT / 'preflight_source_checks.json')
assert audit['all_technical_checks_complete'] and replay['pass']
assert set(reviews) == set(SLUGS)
frozen = {
    'schema_version': 1, 'batch': 21,
    'frozen_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'four_derived_candidates_pass_with_notes',
    'native_pixel_approved': False, 'runtime_integrated': False,
    'runtime_verified': False, 'production_asset_replacement': False,
    'third_imagegen_permitted': False, 'read_only_production_inputs': True,
    'write_scope': 'independent_qa/batch21', 'actors': {},
    'evidence': {
        'technical_audit': 'final_technical_audit.json',
        'script_byte_replay': 'final_derivation_replay.json',
        'source_preflight': 'preflight_source_checks.json',
        'concentrated_feedback': 'v1_visual_feedback.json',
        'visual_reviews': 'final_visual_reviews.json',
        'tafei_source_edge_detail': 'tafei_v2_right_source_edge_4x.png'
    }, 'delivery_inventory': []
}
for slug in SLUGS:
    root = CAMP / slug
    a, v, m = audit['actors'][slug], reviews[slug], load(root / 'manifest.json')
    candidate = root / v['selected']
    assert 1 <= len(a['raw_integrity']) <= 2
    assert len(replay['actors'][slug]['versions']) == len(a['candidates'])
    assert sha(root / 'manifest.json') == a['manifest']['sha256']
    assert v['selected'] == m['selected_portrait']
    assert sha(candidate) == v['selected_sha256'] == m['selected_sha256']
    selected_version = re.match(r'portrait_v\d+', candidate.name).group(0)
    selected_raw = next(x for x in a['raw_integrity'] if x['version'] == selected_version)
    assert selected_raw['raw_alpha128_four_borders_clear']
    assert not v['source_semantic_clipping_detected']
    source_recheck = []
    for record in preflight['actors'][slug]['source_checks']:
        path = REPO / record['path']
        source_recheck.append({'path': record['path'], 'sha256': sha(path),
                              'unchanged_from_preflight': sha(path) == record['actual_sha256']})
    assert all(x['unchanged_from_preflight'] for x in source_recheck)
    files = [{'path': str(p.relative_to(CAMP)), 'bytes': p.stat().st_size, 'sha256': sha(p)}
             for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    frozen['actors'][slug] = {
        'id': m['actor_id'], 'name': m['name'], 'status': v['status'],
        'selected_portrait': str(candidate.relative_to(CAMP)), 'selected_sha256': sha(candidate),
        'selected_raw_sha256': selected_raw['tool_payload_sha256'],
        'author_manifest': str((root / 'manifest.json').relative_to(CAMP)),
        'author_manifest_sha256': sha(root / 'manifest.json'),
        'successful_imagegen_payloads': len(a['raw_integrity']),
        'technical_candidate_exports': len(a['candidates']),
        'nongenerating_tool_records': a['nongenerating_tool_records'],
        'raw_selected_four_borders_clear_at_alpha128': True,
        'identity_reconciliation': preflight['actors'][slug]['identity_reconciliation'],
        'limitations': v['limitations'], 'source_recheck': source_recheck,
        'candidate_specification': next(x for x in a['candidates'] if x['path'] == v['selected'])
    }
    frozen['delivery_inventory'].extend(files)
board = Image.new('RGB', (1280, 570), (72, 74, 76))
draw = ImageDraw.Draw(board)
for i, slug in enumerate(SLUGS):
    image = Image.open(CAMP / frozen['actors'][slug]['selected_portrait']).convert('RGBA')
    x = i * 320 + 12
    draw.text((x, 8), slug + ' | selected derived candidate', fill=(245, 245, 245))
    board.paste(image, (x, 30), image)
    large = image.resize((296, 400), Image.Resampling.NEAREST)
    board.paste(large, (x, 145), large)
board.save(OUT / 'selected_four_character_contact.png')
(OUT / 'freeze_manifest.json').write_text(json.dumps(frozen, ensure_ascii=False, indent=2) + '\n')
lines = ['# Batch21 独立审计冻结', '', '冻结时间：' + frozen['frozen_utc'], '',
         '四人状态：带注记的 NN 技术派生候选。没有原生像素或实机终稿批准。', '',
         '## 终选与完整 SHA-256', '']
for slug, actor in frozen['actors'].items():
    lines += [f"- {actor['name']}（{slug}）：{actor['selected_portrait']}",
              f"  SHA-256：{actor['selected_sha256']}"]
lines += ['', '## 独立核验', '',
          '- 当前人物卡、roster、母图、母 QA、母清单与四核心已核；真实打开图像核身份、年龄、衣色和个性。',
          '- 当前源与快照 SHA 一致，冻结时再次确认源卡/母图/母 QA/清单未漂移。',
          '- 完整 imagegen 回包解码字节与 raw 一致；每人成功成图至多2份，无第三份成图。',
          '- 先读作者派生脚本并锁 SHA，再仅在本 QA 目录内复跑。所有候选、1x、8x、三底预览与 metrics 逐字节复现。',
          '- 额外独立实现复验 PNG 字节、74×100、≤32可见RGB色、二值alpha、透明RGB为0、整数NN预览。',
          '- 原raw与候选分别检查实质边界，不用技术padding把真实裁边洗成通过。',
          '- 作者 manifest 和 SHA256SUMS 全文件覆盖核验通过；freeze_manifest 列四角色完整交付文件 SHA。',
          '', '## 保留限制', '']
for slug, actor in frozen['actors'].items():
    lines.append(f"- {actor['name']}：" + '；'.join(actor['limitations']))
lines += ['- 塔斐低帽檐/早白鬓角、尤恩全白发/围巾旧徽、阿霖左眉疤按当前卡更新旧母图外观。',
          '- 塔斐raw右边仅1源像素透明列，暗外轮廓仍闭合。v2_inset只改变等比技术containment，不代表源图修复。',
          '- 全部是高分辨率生图后NN缩小、阈值alpha与量化导出的候选，非原生逐像素定稿。',
          '- 未替换生产旧图、人物卡、游戏代码，未接入游戏或实机验证，未commit/push。',
          '', '## 交付清单', '',
          '- 每角色目录保留来源、规格锁、提示词、完整工具回包、raw、所有候选/技术派生、整数预览、作者QA、manifest、SHA及复跑脚本。',
          '- 本目录含来源预检、每人唯一集中反馈、终选视觉评审、最终技术审计、逐字节复跑、独立复现、四人对照、四核心、源边界特写、冻结清单与全目录SHA。',
          '- 参数校验未生成图片的记录与成功图片回包分开统计。replay/只是审计副本，不增加生图计数。', '']
(OUT / 'README.md').write_text('\n'.join(lines))
files = [p for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'SHA256SUMS' and '__pycache__' not in p.parts]
(OUT / 'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(OUT)}\n' for p in files))
print(json.dumps({'status': frozen['status'],
                  'actors': {k: v['selected_sha256'] for k, v in frozen['actors'].items()},
                  'delivery_inventory_files': len(frozen['delivery_inventory']),
                  'qa_files_hashed': len(files)}, ensure_ascii=False, indent=2))
