"""S86 final eight: basin care and highland maintenance, distinct families, limited real stock and handover.

Validates the authored ashcare/highland sources, their rendering into the eight
design notes, the model integration and preserved prior coverage.
"""
from pathlib import Path
import json, hashlib, re
from ScopedDramaCoverage import matching_additional_source
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
m = read('research/city-campaign.json'); old = read('backups/city-drama-20261012-s86/research/city-campaign.json')
qs = {q['id']: q for q in m['quests']}; oq = {q['id']: q for q in old['quests']}
effects = {e['id']: e for e in m['effects']}; checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
expected = {cid: {'CM-' + cid} | {f'CS-{cid}-{i:02}' for i in range(1, 4)} for cid in ['ASH', 'HIG']}
covered = set.union(*expected.values())
check(m['verified_runtime'] is False, 'not-runtime-verified')
for key in ['effects', 'rules', 'travel', 'verified_runtime']:
    check(m[key] == old[key], 'preserve-all-' + key)
check('ASH' not in old['dramatic_casts'] and 'HIG' not in old['dramatic_casts'], 's86-cities-pending-in-backup')
for qid, q in qs.items():
    for key in ['id', 'city', 'routes', 'requires', 'stages', 'locations', 'need', 'turn', 'title', 'kind']:
        check(q[key] == oq[qid][key], qid + '-structural-' + key)
    if qid not in covered:
        for key in (set(q) | set(oq[qid])):
            if key.startswith('dramatic_'):
                check(q.get(key) == oq[qid].get(key), qid + '-other-city-unchanged-' + key)
for cid, cast in old['dramatic_casts'].items():
    check(m['dramatic_casts'][cid] == cast, cid + '-previous-cast-intact')
casts = {cid: m['dramatic_casts'][cid] for cid in expected}
unique = {a['id'] for c in casts.values() for a in c.values()}
newactors = {a['id']: a for c in casts.values() for a in c.values() if not a['existing']}
check([len(casts[c]) for c in ['ASH', 'HIG']] == [8, 8] and len(unique) == 16 and len(newactors) == 8, '16-distinct-actors-eight-new-cards')
check(not ({a['id'] for a in casts['ASH'].values()} & {a['id'] for a in casts['HIG'].values()}), 'no-basin-highland-identity-clone')
check(not (unique & {a['id'] for cid, c in old['dramatic_casts'].items() for a in c.values()}), 'previous-cities-actors-not-repurposed')
for cid, cast in casts.items():
    check(len({a['id'] for a in cast.values()}) == len(cast), cid + '-unique-local-identities')
    for a in cast.values():
        p = V / a['file']
        check(p.exists() and a['name'] in p.read_text(encoding='utf-8'), a['id'] + '-linked-card-name')
scene_count = utterances = choice_count = method_count = 0; all_feedback = []
for cid, slug in [('ASH', 'ashcare'), ('HIG', 'highland')]:
    src = read(f'research/{slug}-drama.json'); fs = read(src['feedback_source']); cast = casts[cid]
    nodes = {n['id']: n for c in m['cities'] if c['id'] == cid for n in c['nodes']}
    source_feedback = {f[0]: f for f in fs}
    check(set(src['quests']) == expected[cid], cid + '-one-main-three-sides')
    check(len(fs) == len(source_feedback) == ({'ASH': 16, 'HIG': 15}[cid]), cid + '-authored-feedback-unique')
    for qid in sorted(expected[cid]):
        q = qs[qid]; text = (V / q['file']).read_text(encoding='utf-8'); spec = src['quests'][qid]
        check(matching_additional_source(ROOT, q), qid + '-exact-current-authored-source')
        check('场次与对白（S86当前稿）' in text and '有限回执的具体回应（S86）' in text, qid + '-current-render-markers')
        check('你希望我现在具体做哪一件？' not in text and '合影' not in text, qid + '-old-template-and-anachronism-absent')
        check(len(q['dramatic_scenes']) == len(q['locations']) == 3, qid + '-three-planned-scenes')
        check(set(q['dramatic_exceptions']) == {'dead', 'refusal', 'before_city', 'after_city'} and all(q['dramatic_exceptions'].values()), qid + '-case-specific-fallbacks')
        for field in q['dramatic_exceptions'].values():
            check(field in text, qid + '-fallback-rendered')
        check(q['dramatic_stage_note'] == spec.get('stage_note', ''), qid + '-stage-note-preserved')
        for i, s in enumerate(q['dramatic_scenes']):
            scene_count += 1; base = q['locations'][i]; sid = qid + f'-S{i+1}'
            check(s['space'] in nodes and s['space'] in [base, base + '-A', base + '-B'], sid + '-actual-location')
            check(bool(s['setup']) and bool(s['basis']) and s['setup'] in text and s['basis'] in text, sid + '-staging-and-knowledge-rendered')
            check(len({who for who, _ in s['lines'] if who != '玩家'}) >= 2, sid + '-distinct-people')
            for who, line in s['lines']:
                utterances += 1
                check(who == '玩家' or who in cast, sid + '-scoped-speaker')
                check(bool(line.strip()) and line in text, sid + '-rendered-line')
            keys = []
            for key, label, mode, who, answer in s['choices']:
                choice_count += 1; keys.append(key)
                check(who in cast and mode in ['ask', 'inspect', 'preview', 'pause'], sid + '-read-only-option')
                check(label in text and answer in text, sid + '-specific-choice-response')
            check(len(keys) == len(set(keys)) == 2, sid + '-two-unique-options')
        check(set(q['dramatic_guards']) == set(q['dramatic_followups']) == {r['key'] for r in q['routes']}, qid + '-all-old-methods')
        for r in q['routes']:
            method_count += 1
            check(q['dramatic_guards'][r['key']] in text, qid + '-actual-action-gate')
            pairs = q['dramatic_followups'][r['key']]
            check(len({who for who, _ in pairs}) >= 2, qid + '-distinct-completion-voices')
            for who, line in pairs:
                utterances += 1
                check(who in cast and line in text, qid + '-completion-speaker')
        for f in q['dramatic_feedback']:
            all_feedback.append(f['effect']); e = effects[f['effect']]; row = source_feedback.get(f['effect'])
            check(e['target'] == qid and f['known_fact'] == e['receipt'], f['effect'] + '-same-limited-receipt')
            check(row == [f['effect'], f['speaker'], f['early_line'], f['late_line'], f['early_action']], f['effect'] + '-exact-authored-feedback-row')
            check(f['speaker'] in cast and f['early_line'] != f['late_line'], f['effect'] + '-different-timing-voices')
            check(all(f[k] in text for k in ['early_line', 'late_line', 'early_action']), f['effect'] + '-rendered-timing-actions')
            check('never reselect' in f['late_scope'] and 'unfreeze N17' in f['late_scope'], f['effect'] + '-no-history-rollback')
        check('二次确认' in text and '不写resolve或paid' in text and '死亡、拒绝、保密、缺席优先' in text, qid + '-no-automatic-commit')
        check('[[寒凉盆地与修院山地人物演出审查]]' in text and '[[文书_ASH-HIG_钥匙与班次短记]]' in text, qid + '-audit-and-world-links')
    incoming = {e['id'] for e in m['effects'] if e['target'] in expected[cid]}
    check(set(source_feedback) == incoming, cid + '-every-old-incoming-edge-authored')
check(len(all_feedback) == len(set(all_feedback)) == 31 and set(all_feedback) == {e['id'] for e in m['effects'] if e['target'] in covered}, 'all-31-receipts-exactly-once')
check(scene_count == 24 and method_count == 16 and choice_count == 48, '24-scenes-16-methods-48-answers')
# Thematic safeguards actually authored in the sources.
check('SQ07 patron有普通护理而无正式relief' in qs['CM-ASH']['dramatic_guards']['localcare'] and '两接收点不造第三床' in qs['CM-ASH']['dramatic_guards']['distributedcare'], 'basin-main-ordinary-care-not-upgraded-to-relief-or-third-bed')
check('屋钥不被扣换' in qs['CS-ASH-01']['dramatic_guards']['b'] and '旧共住权分别核' in qs['CS-ASH-01']['dramatic_guards']['a'], 'nicole-keys-and-shared-home-separate')
check('SQ07 independent尚需原任务控制交出等真实条件' in qs['CS-ASH-02']['dramatic_guards']['a'] and '不逼全家连续替班' in qs['CS-ASH-02']['dramatic_guards']['b'], 'shift-care-no-invented-relief-or-forced-kin-duties')
check('不认证NE4、accountable或relief' in qs['CS-ASH-03']['dramatic_guards']['a'] and '不再用人体填空格' in qs['CS-ASH-03']['dramatic_guards']['b'], 'observation-unbundled-from-care-and-no-body-calibration')
check('CM不授全山支持或第二安全认证' in qs['CM-HIG']['dramatic_guards']['maintenance'] and '不能用专业费买NE/资格' in qs['CM-HIG']['dramatic_guards']['minimal'], 'highland-no-second-safety-certification')
check('未到账不先开' in qs['CS-HIG-01']['dramatic_guards']['a'] and '普通通路不能成玩家日常维修循环' in qs['CS-HIG-01']['dramatic_guards']['b'], 'stop-board-until-real-work-and-no-daily-repair-loop')
check('不自动提交N15或NE5' in qs['CS-HIG-02']['dramatic_guards']['a'] and '拒听回声仍可原旁路认证' in qs['CS-HIG-02']['dramatic_guards']['b'], 'gauge-recheck-not-ne5-and-echo-refusal-keeps-bypass')
check('N17原威胁后安全桌已真实冻结' in qs['CS-HIG-03']['dramatic_guards']['a'] and '不关普通回程、不强免费班' in qs['CS-HIG-03']['dramatic_guards']['b'], 'key-return-after-freeze-real-handover-and-open-return')
hig3 = (V / qs['CS-HIG-03']['file']).read_text(encoding='utf-8')
check('正式一次事件只在N17真实威胁后安全桌冻结后触发' in hig3 and '不能演离任结算或井关句' in hig3, 'hig-03-late-trigger-note-rendered')
check('赫斯若死亡/敌对/不可安全约见不生成新会面' in qs['CM-HIG']['dramatic_exceptions']['dead'], 'hers-death-or-hostility-no-new-meeting')
# World text and audit note.
world = V / '05_主线/城市篇章/文书_ASH-HIG_钥匙与班次短记.md'; wt = world.read_text(encoding='utf-8')
check(all(s in wt for s in ['S86-KEY', 'S86-SHIFT', 'S86-BOWL', 'S86-STOP', 'S86-MARK', 'S86-KEYBACK']), 'six-short-texts-single-doc')
check(all(s in wt for s in ['仅本人实际准许范围的副件可留背包', '原件交出不仍持有', '不卖全户地址']), 'short-note-copy-lifecycle')
check('[[寒凉盆地与修院山地人物演出审查]]' in wt and '[[文书与现场文本台本]]' in wt, 'world-text-backlinks')
audit = V / '11_管理/寒凉盆地与修院山地人物演出审查.md'; at = audit.read_text(encoding='utf-8')
check('24场、16原方法、48组现场问答、31组早/晚回访' in at and '共79篇现在都有逐角色初稿' in at, 'audit-counts-current')
check('[[文书_ASH-HIG_钥匙与班次短记]]' in at and '[[城市与聚落设计总索引]]' in at, 'audit-navigation-links')
for rel, marker in [('02_世界与地图/城市与聚落/聚落_ASH_寒凉盆地与护理村.md', 'S86护理与山地人物演出'), ('02_世界与地图/城市与聚落/聚落_HIG_无名修院山地.md', 'S86护理与山地人物演出'), ('02_世界与地图/任务空间/空间_ASH_寒凉盆地与护理村.md', 'S86护理与山地人物演出'), ('02_世界与地图/任务空间/空间_HIG_无名修院山地.md', 'S86护理与山地人物演出')]:
    check(marker in (V / rel).read_text(encoding='utf-8'), rel + '-summary-attached')
for cid in ['ASH', 'HIG']:
    for a in casts[cid].values():
        card = (V / a['file']).read_text(encoding='utf-8')
        if a['existing']:
            check('## S86同一人物的地域事件' in card, a['id'] + '-existing-card-s86-block')
        else:
            check('原创人物' in card and '[[寒凉盆地与修院山地人物演出审查]]' in card, a['id'] + '-new-card-audit-link')
# Hash manifests all reconcile.
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    h = read('research/' + p.name)
    if not isinstance(h, dict) or not all(isinstance(x, str) for x in h.values()):
        continue
    for rel, expected_sha in h.items():
        check((ROOT / rel).exists() and sha(ROOT / rel) == expected_sha, rel + '-authoring-hash')
check(len(read('research/care-highland-generated-note-hashes.json')) == 10, 'eight-cards-one-world-text-one-audit-generated')
coverage = sum('dramatic_scenes' in q for q in m['quests'])
check(coverage == 73 and coverage - 73 == 0, '73-baseline-authored-no-pending')
check('all 73 baseline quests have current authored scenes' in m.get('dramatic_scope', ''), 'model-scope-claims-final-eight')
report = dict(date='2026-10-12', scope='S86 final eight: exact source/rendering, care/research separation, real stop-board/handover and preserved original methods/receipts; not literary quality, numeric economy, collision or runtime', quests=8, scenes=scene_count, methods=method_count, unique_actors=len(unique), new_cards=len(newactors), dialogue_utterances=utterances, choice_answers=choice_count, early_late_pairs=len(all_feedback), world_texts=1, covered_city_quests=coverage, pending_city_quests=73 - coverage, checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/care-highland-drama-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
