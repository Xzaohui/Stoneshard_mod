"""Validate the S87 original dialogue inventory against its probe report and baseline fingerprint."""
from pathlib import Path
import json, hashlib
ROOT = Path(__file__).resolve().parents[2]
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
inv = read('research/original-dialogue-inventory.json')
key_index = read('research/original-key-index.json')
baseline = read('research/local-baseline.json')
expected = {'scene': 326, 'greeting': 446, 'chat': 125, 'npc': 227, 'follower': 8}
for fam, n in expected.items():
    check(inv['families'].get(fam, {}).get('count') == n == len(inv['families'][fam]['entries']), fam + '-count')
check(inv['sha256'] == key_index['sha256'] == baseline['candidate_baseline']['sha256'].upper(), 'sha-matches-baseline')
check(key_index.get('dialogue_inventory') == expected, 'probe-report-counts')
total = 0; with_speaker = 0
for fam, data in inv['families'].items():
    for e in data['entries']:
        total += 1
        check(isinstance(e.get('index'), int) and isinstance(e.get('key'), str) and e['key'], fam + '-entry-shape')
        check(isinstance(e.get('parts'), int) and isinstance(e.get('zh'), bool) and isinstance(e.get('len'), int), fam + '-entry-fields')
        if e.get('speaker'):
            with_speaker += 1
            check(e['speaker'] in dict(inv['speaker_histogram']), fam + '-speaker-in-histogram')
check(total == sum(expected.values()), 'inventory-total')
check(len(inv['speaker_histogram']) == 72 and key_index.get('dialogue_speakers') == 72, 'seventy-two-speakers')
check(all(isinstance(n, str) and n and c > 0 for n, c in inv['speaker_histogram']), 'speaker-histogram-shape')
check(inv['speaker_histogram'] == sorted(inv['speaker_histogram'], key=lambda kv: -kv[1]), 'speaker-histogram-sorted')
report = dict(date='2026-10-12', scope='S87 dialogue inventory: counts, fingerprint, entry shape and speaker histogram; locators only, no text; not runtime validation',
              families=expected, total=total, speakers=len(inv['speaker_histogram']), entries_with_speaker=with_speaker,
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/original-dialogue-inventory-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
