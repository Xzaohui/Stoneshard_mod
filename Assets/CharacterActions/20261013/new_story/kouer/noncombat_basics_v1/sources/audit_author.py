from PIL import Image
from pathlib import Path
import numpy as np
import json, hashlib, base64

r = Path(__file__).resolve()
while r.name != 'Stoneshard_mod':
    r = r.parent
base = r / 'Assets/CharacterActions/20261013/new_story'
gate = r / 'Assets/CharacterDesigns/20261013/expressive/new_story_audit/independent_fourth_new_character_actions_miloer_kouer_visual_gate_20261014.json'
reviews = {x['pose_version']: x for x in json.loads(gate.read_text())['pose_reviews']}
for slug in ['miloer', 'kouer']:
    p = base / slug / 'noncombat_basics_v1'
    records = []
    for raw in sorted((p / 'raw').glob('*_raw.png')):
        k = raw.name[:-8]
        t = p / 'exports' / f'{k}_transparent.png'
        ret = json.loads((p / 'raw' / f'{k}_tool_return.json').read_text())
        params = json.loads((p / 'prompts' / f'{k}_parameters.json').read_text())
        a, b = np.array(Image.open(raw)), np.array(Image.open(t))
        mask = a[:, :, 3] > 8
        alpha = b[:, :, 3]
        ys, xs = np.where(alpha > 0)
        composites = []
        for tone, color in [('light', (239, 233, 219, 255)), ('dark', (29, 34, 38, 255))]:
            expected = Image.new('RGBA', Image.open(t).size, color)
            expected.alpha_composite(Image.open(t).convert('RGBA'))
            composites.append({'tone': tone, 'exact_true_alpha_composite': bool(np.array_equal(np.array(expected.convert('RGB')), np.array(Image.open(p / 'review' / f'{k}_{tone}.png'))))})
        rec = {'key': k, 'raw_sha256': hashlib.sha256(raw.read_bytes()).hexdigest(), 'transparent_sha256': hashlib.sha256(t.read_bytes()).hexdigest(), 'raw_mode': Image.open(raw).mode, 'transparent_mode': Image.open(t).mode, 'size': list(Image.open(t).size), 'alpha_zero_pixels': int((alpha == 0).sum()), 'alpha_opaque_pixels': int((alpha == 255).sum()), 'alpha_partial_pixels': int(((alpha > 0) & (alpha < 255)).sum()), 'nontransparent_bbox': [int(xs.min()), int(ys.min()), int(xs.max() + 1), int(ys.max() + 1)], 'full_transparent_outer_border': bool(not (alpha[0].any() or alpha[-1].any() or alpha[:, 0].any() or alpha[:, -1].any())), 'full_tool_payload_decodes_exact_raw': base64.b64decode(ret['image_url'].split(',', 1)[1]) == raw.read_bytes(), 'params_prompt_matches_saved_verbatim': params['prompt'] == (p / 'prompts' / f'{k}.txt').read_text(), 'reference_hashes': [{'path': x, 'sha256': hashlib.sha256(Path(x).read_bytes()).hexdigest()} for x in params['referenced_image_paths']], 'visible_body_pixels_unchanged': bool(np.array_equal(a[mask], b[mask])), 'postprocess_only_alpha_le_8_cleanup': bool(np.array_equal(b[~mask], np.zeros_like(b[~mask]))), 'composites': composites, 'actual_viewed_by_author': ['raw', 'transparent', 'light', 'dark'], 'independent_status': reviews[k]['verdict'], 'selected': reviews[k]['verdict'] == 'pass', 'visual_note': reviews[k]['visual_note']}
        assert rec['full_tool_payload_decodes_exact_raw'] and rec['params_prompt_matches_saved_verbatim'] and rec['visible_body_pixels_unchanged'] and all(x['exact_true_alpha_composite'] for x in composites)
        records.append(rec)
    out = {'author': 'draw_miloer_kouer_actions', 'status': 'source_pixel_and_visual_checks_complete', 'visual_gate': str(gate.relative_to(r)), 'visual_gate_sha256': hashlib.sha256(gate.read_bytes()).hexdigest(), 'not_runtime_or_animation': True, 'alpha_zero_rgb_note': 'Fully transparent hidden RGB is not a visual hard error. Only alpha <=8 cleanup used.', 'records': records}
    (p / 'review/QA_author_source_and_pixels.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(slug, len(records), 'source/pixel/true-composite checks pass')
