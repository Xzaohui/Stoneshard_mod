"""Validate the S174 rollback runbook against the live backup set and record."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard')
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
facts = json.loads((R / 'rollback-runbook.json').read_text(encoding='utf-8'))
dep = json.loads((ROOT / 'artifacts/direct-deployment.json').read_text(encoding='utf-8-sig'))
bk = Path(facts['backup']['dir'])
check(bk.exists(), 'backup-exists')
check(set(facts['backup']['files']) == {x.name for x in bk.iterdir()}, 'backup-files-live')
before = json.loads((bk / 'before.json').read_text(encoding='utf-8-sig'))
check(facts['backup']['data_sha256'] == sha(bk / 'data.win'), 'backup-data-sha-live')
check(facts['backup']['data_sha256'] == str(before['beforeDataSha256']).upper(), 'backup-data-matches-before-json')
check(facts['backup']['sml_sha256'] == sha(bk / 'EmbersAndOaths.sml'), 'backup-sml-sha-live')
check(facts['live']['data_sha256'] == sha(GAME / 'data.win'), 'live-data-sha-live')
check(facts['live']['data_matches_record'] == (sha(GAME / 'data.win') == str(dep['deployedDataSha256']).upper()), 'live-match-flag')
check(facts['live']['deployed_sml_sha256'] == sha(GAME / 'msl/Mods/EmbersAndOaths.sml'), 'live-sml-sha-live')
check(facts['record']['backup'] == dep['backup'] and facts['record']['game'] == dep['game'], 'record-fields-live')
us = facts['user_side']
sp = Path(us['settings_path'])
check(sp.exists() == us['settings_exists'], 'settings-exists-live')
if sp.exists():
    check(us['settings_sha256'] == sha(sp), 'settings-sha-live')
    live_mods = json.loads(sp.read_text(encoding='utf-8-sig')).get('EnableMods', [])
    check(us['enable_mods'] == live_mods, 'settings-mods-live')
    check(us['mod_enabled'] == ('EmbersAndOaths' in live_mods), 'mod-enabled-live')
ud = Path(us['user_dir'])
check(us['user_files_now'] == len([x for x in ud.rglob('*') if x.is_file()]) if ud.exists() else us['user_files_now'] == 0, 'user-files-live')
card = (V / '11_管理/部署与回滚运行手册.md').read_text(encoding='utf-8')
check('## 用户侧前置状态（只读）' in card, 'card-user-side-section')
check(us['settings_path'] in card and str(us['user_files_now']) in card, 'card-user-side-values')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 部署步骤（放行后执行）', '## 回滚步骤（必要时执行）', '## 现状核对（只读）', '## 风险与边界'):
    check(sec in card, 'section-' + sec)
check(facts['record']['backup'] in card, 'card-backup-path')
check(facts['backup']['data_expected'][:16] in card, 'card-before-hash')
check('不保证无损卸载' in card and '用户数据一律不动' in card, 'card-caveats')
check('本轮未执行任何部署或回滚' in card, 'card-not-executed')
for step in ('`data.win.eao-pending`', 'userFilesChecked', 'direct-deployment.json'):
    check(step in card, 'card-step-' + step)
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('ROLLBACK-S174:BEGIN' in plan and '[[部署与回滚运行手册]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('ROLLBACK-S174:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'rollback-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S174 rollback runbook: backup set files and hashes recomputed, record fields, steps and caveats on the page, chain; nothing executed',
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(R / 'rollback-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
