"""Fit retained imagegen cutouts to frozen building body bounds and palette.

Only export normalization occurs here. The erased apron comes from imagegen;
the released building layout remains the source of collision and origins.
"""
import hashlib
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'src/Art/native-n2-built-v1'
SOURCE = ROOT / 'src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v2'
BATCH = ROOT / 'src/Art/scene-style-repairs-20261015'
# First row of the unwanted baked rectangular apron, inspected in released PNGs.
BODY_END = {'worker_shed': 174, 'winch_shed': 149, 'canal_entry': 200}
# Frozen production framing at 4df549ad, independently inspected from Git blobs.
# R01 source sprites have different padding, so do not derive production bounds
# from those sources or from an already repaired output on a repeated export.
BODY_BOX = {'worker_shed': (9, 20, 251, 174), 'winch_shed': (9, 42, 199, 149), 'canal_entry': (9, 74, 251, 200)}
BASELINE_SHA = {
    'worker_shed': '116525bd9d534e85edde2ce48537d882fa1bb5acc4902b50d8cefbc6b2547ca0',
    'winch_shed': '23d75ba18cde46e198f6230e62e0c78314115731fa49ddf93063ef5ec023bafa',
    'canal_entry': '914710de500bf17f15f7efa3b6e482950bb900318166f21a337375b4d3c81992',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest_path = PACK / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    released = json.loads((SOURCE / 'manifest.json').read_text(encoding='utf-8'))
    colors = [tuple(bytes.fromhex(c)) for c in re.findall(
        r'^  - #([0-9A-F]{6})$', (SOURCE / 'spec_lock.md').read_text(encoding='utf-8'), re.M)]
    assert len(colors) == 128
    palette = Image.new('P', (1, 1))
    palette.putpalette([v for c in colors for v in c] + list(colors[-1]) * 128)
    records = []
    for name, cutoff in BODY_END.items():
        ident = 'r01_' + name
        spec = next(a for a in released['assets'] if a['id'] == ident)
        frozen = SOURCE / spec['path']
        assert sha(frozen) == spec['sha256']
        original = Image.open(frozen).convert('RGBA')
        body_box = BODY_BOX[name]
        raw_path = BATCH / 'raw/facades' / (name + '.png')
        raw = Image.open(raw_path).convert('RGBA')
        alpha = raw.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
        raw_box = alpha.getbbox()
        assert raw_box is not None
        raw.putalpha(alpha)
        body = raw.crop(raw_box).resize((body_box[2] - body_box[0], body_box[3] - body_box[1]), Image.Resampling.NEAREST)
        body_alpha = body.getchannel('A')
        body = body.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
        body.putalpha(body_alpha)
        result = Image.new('RGBA', original.size)
        result.paste(body, body_box[:2], body_alpha)
        assert result.getchannel('A').crop((0, cutoff, result.width, result.height)).getbbox() is None
        entry = next(a for a in manifest['assets'] if a['id'] == 'n2site_' + ident)
        output = PACK / entry['path']
        result.save(output)
        entry['sha256'] = sha(output)
        entry['repair_source'] = raw_path.relative_to(ROOT).as_posix()
        entry['body_bbox'] = list(body_box)
        entry['apron_from_row'] = cutoff
        manifest['source_sha256'][raw_path.relative_to(ROOT).as_posix()] = sha(raw_path)
        records.append(dict(id=entry['id'], source=entry['repair_source'], source_sha256=sha(raw_path), baseline_sha256=BASELINE_SHA[name],
                            raw_size=list(raw.size), raw_bbox=list(raw_box), body_bbox=list(body_box),
                            size=list(result.size), origin=entry['origin'], apron_from_row=cutoff,
                            output=output.relative_to(ROOT).as_posix(), sha256=sha(output)))
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    report = dict(records=records, baseline_commit='4df549adfb9fd133399adc4702791727bac4bd08', palette='R01 128', resample='nearest', alpha='binary, transparent RGB zero',
                  collision='unchanged explicit layout', runtimeVerified=False)
    (BATCH / 'facade-export.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(dict(exported=len(records), outputs=[r['output'] for r in records])))


if __name__ == '__main__':
    main()
