"""Validate the S143 implementation-side snapshot against live files (read-only)."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard')
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while True:
            b = f.read(1 << 20)
            if not b: break
            h.update(b)
    return h.hexdigest().upper()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
st = read('research/impl-state.json'); base = read('research/local-baseline.json')
art = ROOT / 'artifacts/EmbersAndOaths.sml'; msl = GAME / 'msl/Mods/EmbersAndOaths.sml'
data = GAME / 'data.win'; vanilla = GAME / 'vanilla.win'
for label, key, path in (('artifact', 'artifact', art), ('msl', 'msl_copy', msl),
                         ('data', 'data_win', data), ('vanilla', 'vanilla_win', vanilla)):
    check(path.exists(), 'exists-' + label)
    if path.exists():
        check(st[key]['sha256'] == sha(path), 'sha-live-' + label)
        check(st[key]['bytes'] == path.stat().st_size, 'size-live-' + label)
card_text = (V / '11_管理/实现侧现状核对.md').read_text(encoding='utf-8')
rel = st['relationships']
check(rel['artifact_is_deployed'] == (st['artifact']['sha256'] == st['msl_copy']['sha256']), 'relationship-deployed-live')
check(rel['artifact_is_recorded'] == (st['artifact']['sha256'] == st['recorded']['package_sha256']), 'relationship-recorded-live')
check(st['msl_copy']['sha256'] == str(st['recorded']['package_sha256']).upper(), 'deployed-copy-matches-record')
check(('本地候选较新' in card_text) or rel['artifact_is_deployed'], 'candidate-newer-stated')
check(st['data_win']['sha256'] == st['recorded']['deployed_data_sha256'], 'data-vs-record')
check(st['vanilla_win']['sha256'] == base['candidate_baseline']['sha256'], 'vanilla-vs-baseline')
check(st['recorded']['runtime_verified'] is False, 'runtime-not-verified')
codes = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob('src/**/Codes/*.gml'))
check(st['sources']['gml_codes'] == len(codes), 'gml-count-live')
check(st['sources']['codes'] == codes, 'gml-list-live')
tools = sorted(p.name for p in (ROOT / 'tools').glob('*.ps1'))
check(st['sources']['tools'] == tools, 'tools-list-live')
card = card_text
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 文件指纹', '## 与记录的比对', '## 源码与工具', '## 与本轮设计的关系', '## 边界'):
    check(sec in card, 'section-' + sec)
for k in ('artifact', 'msl_copy', 'data_win', 'vanilla_win'):
    check(st[k]['sha256'][:16] in card and f"{st[k]['bytes']:,}" in card, 'card-fingerprint-' + k)
check(st['recorded']['version'] in card, 'card-version')
check('runtimeVerified' in card and 'false' in card, 'card-runtime-flag')
check(str(st['sources']['gml_codes']) in card, 'card-gml-count')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('IMPL-STATE-S143:BEGIN' in plan and '[[实现侧现状核对]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('IMPL-STATE-S143:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/impl-state-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S143 implementation snapshot: package/deployed copy/data.win/vanilla hashes recomputed read-only, record cross-checks, source counts, page and chain; no build or deployment',
              gml_codes=len(codes), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/impl-state-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
