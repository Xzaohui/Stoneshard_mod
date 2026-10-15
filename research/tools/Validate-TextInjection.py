"""Validate the S176 text-injection conventions against the live sources."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
facts = json.loads((R / 'text-injection.json').read_text(encoding='utf-8'))
dlg = (ROOT / 'src/EmbersAndOaths/NativeDialogue.cs').read_text(encoding='utf-8')
docs = (ROOT / 'src/EmbersAndOaths/NativeDocuments.cs').read_text(encoding='utf-8')
step = (ROOT / 'src/EmbersAndOaths/Codes/controller_step.gml').read_text(encoding='utf-8')
def has_line(text, needle, line):
    lines = text.splitlines()
    return line <= len(lines) and needle in lines[line - 1]
ev = facts['evidence']
check(has_line(dlg, 'variable_struct_set(global.__dialogue_flow_data', ev['flow_injection']['line']), 'flow-line-live')
check(has_line(dlg, 'ds_map_set(global.npc_lines_map', ev['line_injection']['line']), 'lines-line-live')
check(has_line(dlg, 'global.language == 3', ev['language_slot']['line']), 'lang-line-live')
check(has_line(step, '__dialogue_flow_data', ev['struct_guard']['line']), 'guard-line-live')
check(has_line(docs, 'Quote', ev['quote_helper']['line']), 'quote-line-live')
# slot order: index 0 ASCII (EN), index 1 CJK (CN)
lines_block = dlg.split('var lines = new Dictionary<string, string[]>', 1)[1] if 'var lines = new Dictionary<string, string[]>' in dlg else dlg
pair = re.search(r'\["EAO_intro"\] = new\[\] \{ "([^"]+)", "([^"]+)" \}', lines_block)
check(pair is not None, 'sample-pair-live')
if pair:
    en, cn = pair.group(1), pair.group(2)
    check(all(ord(c) < 128 for c in en), 'slot0-is-en')
    check(any('\u4e00' <= c <= '\u9fff' for c in cn), 'slot1-is-cn')
    check(facts['sample']['en'][:20] == en[:20] and facts['sample']['cn'][:16] == cn[:16], 'sample-matches')
count = len(re.findall(r'^\s*\["[^"]+"\] = new\[\] \{ "[^"]+", "[^"]+" \},', lines_block, re.M))
check(facts['sample_line_count'] == count, 'sample-line-count-live')
card = (V / '11_管理/文本注入与本地化口径.md').read_text(encoding='utf-8')
stems = {p.stem for p in V.rglob('*.md')}
for sec in ('## 机制（含证据行）', '## 口径', '## 本Mod内容将走同一机制', '## 边界'):
    check(sec in card, 'section-' + sec)
check('索引 0＝EN、1＝CN' in card or '索引 0＝EN、1＝CN' in card, 'card-slot-order')
check(f"{facts['our_content']['dialogue_lines']:,}" in card, 'card-line-total')
check('未接线、未构建、未部署' in card, 'card-not-wired')
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('TEXT-INJECT-S176:BEGIN' in plan and '[[文本注入与本地化口径]]' in plan, 'plan-block')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-' + lm.group(1))
check('TEXT-INJECT-S176:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = json.loads((R / 'text-inject-note-hashes.json').read_text(encoding='utf-8'))
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel).lower() == exp.lower(), rel + '-hash')
for p in sorted(R.glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel).lower() == exp.lower(), rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S176 text injection: five evidence lines re-checked, EN/CN slot order verified from a live sample pair, page and chain; read-only',
              sample_lines=count, checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(R / 'text-inject-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
