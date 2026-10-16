"""Read-only S201 heavy-edge design validation; no reports or game writes."""
from pathlib import Path
from copy import deepcopy
import hashlib
import json
import re
import sys
from HeavyEdges import project, support_stubs

ROOT = Path(__file__).resolve().parents[2]
KEYS = {'ferry_depot_claim', 'custody_intent', 'custody_signed',
        'n8_relief', 'sylang_state', 'n4_shift_remedied'}
ACTS = {'I', 'II', 'III', 'IV'}

def support_section_errors(route, settlements, base_by_key):
    errors=[]
    def check(ok,label):
        if not ok: errors.append(label)
    for stub in route:
        check(all(not k.startswith('resolve_') for k in stub['writes']), stub['event']+'-no-legacy-resolve')
    for stub in settlements:
        check(bool(stub['writes']) and set(stub['sets']) == set(stub['writes']) and all(k.startswith('resolve_') and k in base_by_key and v in base_by_key[k]['values'] for k,v in stub['sets'].items()), stub['event']+'-legacy-settlement-only')
    return errors

def validate(net, model):
    errors = []
    def check(ok, label):
        if not ok:
            errors.append(label)
    registry = net['heavy_edge_registry']
    variables = registry['variables']
    edges = net['heavy_edges']
    check(set(variables) == KEYS, 'six-state-keys')
    documents = {p: (ROOT / p).read_text(encoding='utf-8') for p in registry['edge_sources']}
    expected = [table_id or heading_id for text in documents.values()
                for table_id, heading_id in re.findall(r'^\| (HX\d+) \||^## (HX\d+)\s*$', text, re.M)]
    check(len(edges) == len(expected) == len(set(expected)) and
          {e['id'] for e in edges} == set(expected), 'HX-source-registration-unique')
    source = (ROOT / registry['source']).read_text(encoding='utf-8')
    ending = (ROOT / registry['ending_source']).read_text(encoding='utf-8')
    dictionary = (ROOT / 'design/09_系统逻辑/当前任务依赖与状态字典.md').read_text(encoding='utf-8')
    tables = [(ROOT / p).read_text(encoding='utf-8') for p in (
        'design/09_系统逻辑/状态键映射总表.md',
        'design/11_管理/引擎键名前缀与遗留键登记.md')]
    reference_domains = {
        'ferry_depot_claim': ['none', 'refused', 'MG', 'CO', 'GA'],
        'custody_intent': ['none', 'MG', 'CO', 'GA', 'dispersed'],
        'custody_signed': ['none', 'MG', 'CO', 'GA', 'dispersed'],
        'n8_relief': ['unseen', 'accepted', 'refused'],
        'sylang_state': ['alive', 'dead'], 'n4_shift_remedied': [False, True]}
    def member(value, domain):
        return any(type(value) is type(v) and value == v for v in domain)
    for key, definition in variables.items():
        check(definition['values'] == reference_domains[key], key + '-canonical-domain')
        check(member(definition['default'], definition['values']), key + '-default')
        check(definition['engine_key'] == 'EAO_' + key, key + '-engine-prefix')
        check(key in dictionary, key + '-existing-dictionary')
        check(all(member(value, definition['values']) for value in definition['write_values']), key + '-transaction-domain')
        check(definition['requires_execution'] is True and all(q in net['tasks'] for q in definition['writer_tasks']), key + '-transaction-owner')
        for text in tables:
            row = next((line for line in text.splitlines() if line.startswith('| `' + key + '` |')), '')
            cells = re.findall(r'`([^`]+)`', row)
            check(len(cells) == 4 and cells[1] == definition['engine_key'], key + '-document-row')
            if len(cells) == 4:
                check(json.loads(cells[2]) == definition['values'] and
                      type(json.loads(cells[3])) is type(definition['default']) and
                      json.loads(cells[3]) == definition['default'], key + '-document-domain')
    # Match the upstream S200 enumerations, not merely two copies of our table.
    for key in ['ferry_depot_claim', 'custody_signed', 'n8_relief', 'sylang_state']:
        match = re.search(r'`' + key + r'`[^\n;；]*?∈\s*\{([^}]+)\}', dictionary)
        check(bool(match) and set(match[1].replace(' ', '').split(',')) == set(variables[key]['values']), key + '-S200-domain')
    check(variables['custody_signed'].get('copy_from') == 'custody_intent' and
          variables['custody_signed'].get('freeze_event') == 'N17_existing_confirmation' and
          variables['custody_signed'].get('preserve_supervision') is True, 'signed-atomic-freeze')
    check(variables['n4_shift_remedied'].get('reuse') is True and
          variables['n4_shift_remedied'].get('preserve_history') == ['n4_shift_harm'], 'remedy-keeps-history')
    check('custody_intent' in ending and 'N17' in ending, 'intent-confirmation-source')
    counts = {act: set() for act in ACTS}
    for edge in edges:
        ident = edge['id']
        receiver_source = edge.get('receiver_source')
        edge_source = documents.get(receiver_source, source)
        if receiver_source:
            section = re.search(r'^## ' + ident + r'\n(.*?)(?=^## HX|<!-- OPT-S201:END -->)', edge_source, re.M | re.S)
            row = section[1] if section else ''
        else:
            row = next((line for line in source.splitlines() if line.startswith('| ' + ident + ' |')), '')
        check(bool(row) and (('L2。' in row) if receiver_source else ('| ' + edge['level'] + ' |') in row), ident + '-source-tier')
        if receiver_source:
            check(edge['level'] == 'L2', ident + '-city-return-tier')
        check(edge['level'] in {'L2', 'L3'}, ident + '-tier')
        check(set(edge['acts']) <= ACTS and len(edge['acts']) == len(set(edge['acts'])), ident + '-acts')
        check(bool(edge['sources']) and bool(edge['targets']), ident + '-endpoints')
        for endpoint in edge['sources'] + edge['targets']:
            path = ROOT / endpoint['file']
            check(path.is_relative_to(ROOT / 'design') and path.is_file(), ident + '-file-' + endpoint['task'])
            if path.is_file():
                text = path.read_text(encoding='utf-8')
                check('台本_' + endpoint['task'] + '_' in path.name, ident + '-task-file')
                if receiver_source and endpoint in edge['targets']:
                    check('接收：[[' + path.stem + ']]' in row, ident + '-receiver-registration')
                elif receiver_source:
                    block = re.search(r'<!-- OPT-S201:BEGIN -->(.*?)<!-- OPT-S201:END -->', text, re.S)
                    check(bool(block) and ident in block[1] and '来源：[[' + path.stem + ']]' in row, ident + '-city-source-block')
                else:
                    check(ident in text or '<!-- OPT-S200:BEGIN -->' in text, ident + '-rendered-' + endpoint['task'])
        # Registered acts must be real source/receiver acts, not padded counters.
        def act(q):
            if re.fullmatch(r'N\d+', q):
                number = int(q[1:])
                return 'I' if number <= 4 else 'II' if number <= 9 else 'III' if number <= 13 else 'IV'
            return None
        available = {act(p['task']) for p in edge['sources'] + edge['targets']}
        # SQ08 spans II/III; its L2 entry never contributes to the L3 quota.
        check(set(edge['acts']) <= available | ({'II'} if ident == 'HX11' else set()), ident + '-actual-acts')
        if edge['level'] == 'L3':
            for stage in edge['acts']:
                if stage in counts:
                    counts[stage].add(ident)
        check(all(edge['guards'].get(k) is True for k in
                  ['alive', 'present', 'willing', 'authorized', 'receipt_required']), ident + '-person-guards')
        check(bool(edge['fallback']) and bool(edge['retroactive']), ident + '-recovery')
        for conditions in [edge['when']] + list(edge.get('branches', {}).values()):
            for key, values in conditions.items():
                if key in variables:
                    check(all(member(v, variables[key]['values']) for v in values), ident + '-condition-domain-' + key)
                elif key.startswith('resolve_'):
                    task = key[len('resolve_'):].replace('_', '-')
                    candidates = [p for p in edge['sources'] + edge['targets'] if p['task'] == task]
                    check(bool(candidates), ident + '-route-task-' + task)
                    for candidate in candidates:
                        text = (ROOT / candidate['file']).read_text(encoding='utf-8')
                        for value in values:
                            check(task + '-R-' + value in text or task + '-C-' + value in text or
                                  bool(re.search(r'^### ' + re.escape(value) + r'：', text, re.M)),
                                  ident + '-real-route-' + str(value))
                else:
                    check(key == 'toman_personnel' and values == [False], ident + '-known-condition-' + key)
        for key, value in edge['writes'].items():
            check(key in variables and member(value, variables[key]['values']), ident + '-write-domain-' + key)
        check(not edge['evidence_writes'] and not edge['snapshot_writes'] and not edge['ending_rule_writes'], ident + '-protected-writes')
        check(set(edge['writes']) <= {'sylang_state'}, ident + '-no-NE-or-snapshot-write')
    for stage, ids in counts.items():
        check(len(ids) >= 3, stage + '-L3-at-least-three')
    for key, digest in registry['protected_model_sha256'].items():
        check(key in {'active_ending_rules', 'active_evidence_producers'} and
              hashlib.sha256(json.dumps(model[key], sort_keys=True, ensure_ascii=False).encode()).hexdigest() == digest,
              key + '-protected-baseline')
    check(set(registry['protected_model_sha256']) == {'active_ending_rules', 'active_evidence_producers'}, 'protected-fields-complete')
    check(all(registry.get(k) is True for k in ['no_new_evidence', 'mainline_unlocked', 'frozen_N17_unchanged']), 'global-protection')
    base_keys=json.loads((ROOT/'research/state-keys.json').read_text(encoding='utf-8'))['keys']
    expected_effects, expected_stubs, expected_keys = project(net,base_keys)
    check(model.get('conditional_influences') == expected_effects, 'HX-model-projection')
    for filename, field, expected in [('event-stubs.json','heavy_edge_stubs',expected_stubs),
                                      ('state-keys.json','heavy_edge_keys',expected_keys)]:
        data=json.loads((ROOT/'research'/filename).read_text(encoding='utf-8'))
        check(data.get(field)==expected, 'HX-'+field+'-projection')
    state_data=json.loads((ROOT/'research/state-keys.json').read_text(encoding='utf-8'))
    check(state_data.get('heavy_edge_families') == {'route':12, 'state':len(expected_keys)-12}, 'HX-family-counts')
    hooks=json.loads((ROOT/'research/hook-mapping.json').read_text(encoding='utf-8'))
    bindings=hooks.get('heavy_edge_bindings',[])
    check(bindings==[dict(event=s['event'],trigger=s['trigger'],hook=s['trigger'],engine_event=None, when=s['when']) for s in expected_stubs], 'HX-hook-bindings')
    known={k['key'] for k in expected_keys}
    base_by_key={k['key']:k for k in base_keys}
    for key in expected_keys:
        if key['key'] in base_by_key:
            check(key['values']==base_by_key[key['key']]['values'],key['key']+'-canonical-shared-domain')
    for stub in expected_stubs:
        check(set(stub['reads']+stub['writes'])<=known,stub['event']+'-keys')
        check(stub['trigger'] in hooks['hooks'],stub['event']+'-native-hook')
    event_data=json.loads((ROOT/'research/event-stubs.json').read_text(encoding='utf-8'))
    actual_support=event_data.get('route_state_stubs', [])
    check(actual_support == support_stubs(net), 'route-state-projection')
    check(hooks.get('route_state_bindings') == [dict(event=s['event'], trigger=s['trigger'], hook=s['trigger'], engine_event=None, when=s['when']) for s in actual_support], 'route-state-bindings')
    settlements=event_data.get('resolve_settle_stubs', [])
    check(settlements == support_stubs(net, settlement=True), 'resolve-settle-projection')
    check(hooks.get('resolve_settle_bindings') == [dict(event=s['event'], trigger=s['trigger'], hook=s['trigger'], engine_event=None, when=s['when']) for s in settlements], 'resolve-settle-bindings')
    errors.extend(support_section_errors(actual_support, settlements, base_by_key))
    check(not any(s['event']=='evt_N17_custody_signed_none' for s in actual_support), 'no-empty-signature-producer')
    domains={k['key']: k['values'] for k in base_keys+expected_keys}
    writers={k['key']:{k['default']} for k in expected_keys}
    check('none' in writers.get('custody_signed',set()), 'unsigned-default-readable-without-producer')
    all_stubs=event_data['stubs']+event_data.get('heavy_edge_stubs',[])+actual_support+settlements
    check(len({s['event'] for s in all_stubs}) == len(all_stubs), 'all-event-names-unique')
    for stub in all_stubs:
        sets=dict(stub.get('sets', {}))
        # Historical choice stubs describe their selected value in route(value).
        route=re.fullmatch(r'route\(([A-Za-z0-9_]+)\)', str(stub['when']))
        if route:
            for key in stub['writes']:
                if key.startswith('resolve_'): sets[key]=route[1]
        for key,value in sets.items():
            check(key in domains and value in domains[key], stub['event']+'-write-domain-'+key)
            check(key in stub['writes'], stub['event']+'-declares-write-'+key)
            writers.setdefault(key,set()).add(value)
    for stub in event_data.get('heavy_edge_stubs',[])+actual_support+settlements:
        for key,values in stub['when'].items():
            check(key in writers, stub['event']+'-has-writer-'+key)
            for value in values:
                check(value in writers.get(key,set()), stub['event']+'-reachable-'+key+'='+str(value))
    # HX endpoints must never be installed as hard prerequisite references.
    entries={q['id']:q for q in model['screenplays']}
    authored={}
    for name in ['story-main.json','story-main-late.json','story-side.json','story-daily.json','story-dungeon.json']:
        for q in json.loads((ROOT/'research'/name).read_text(encoding='utf-8')): authored[q['id']]=q
    for qid,q in entries.items():
        original=authored[qid]
        for field in ['requires','requires_any','story_requires','at_least']:
            check(q.get(field, [] if field!='at_least' else None)==original.get(field, [] if field!='at_least' else None),qid+'-unchanged-'+field)
    visiting=set(); visited=set()
    def visit(qid):
        if qid in visiting:
            check(False,'hard-dependency-cycle-'+qid); return
        if qid in visited: return
        visiting.add(qid)
        q=entries[qid]
        for parent in q['requires']+q['requires_any']+q.get('story_requires',[])+(q.get('at_least') or {}).get('of',[]):
            if parent in entries: visit(parent)
        visiting.remove(qid); visited.add(qid)
    for qid in entries: visit(qid)
    for rel in ['09_系统逻辑/事件桩映射总表.md','09_系统逻辑/状态键映射总表.md','11_管理/触发器接线点映射.md']:
        text=(ROOT/'design'/rel).read_text(encoding='utf-8')
        for e in edges: check(e['id'] in text,e['id']+'-rendered-'+rel)
    return errors, {stage: sorted(ids) for stage, ids in sorted(counts.items())}

def main():
    net = json.loads((ROOT / 'research/story-network.json').read_text(encoding='utf-8'))
    model = json.loads((ROOT / 'research/design-model.json').read_text(encoding='utf-8'))
    errors, counts = validate(net, model)
    if '--self-test' in sys.argv:
        event_data=json.loads((ROOT/'research/event-stubs.json').read_text(encoding='utf-8'))
        base_by_key={k['key']:k for k in json.loads((ROOT/'research/state-keys.json').read_text(encoding='utf-8'))['keys']}
        for label, section, key, value in [
                ('route-resolve-leak','route_state_stubs','resolve_N11','trace'),
                ('settle-route-leak','resolve_settle_stubs','route_N3','any'),
                ('settle-old-domain','resolve_settle_stubs','resolve_N11','invented')]:
            altered=deepcopy(event_data)
            altered[section][0]['sets']={key:value}; altered[section][0]['writes']=[key]
            if not support_section_errors(altered['route_state_stubs'],altered['resolve_settle_stubs'],base_by_key):
                errors.append('negative-section-not-rejected-'+label)
        mutations = [lambda n: n['heavy_edges'][0]['writes'].update(NE6=True),
                     lambda n: n['heavy_edges'][0]['guards'].update(alive=False),
                     lambda n: n['heavy_edges'][0]['sources'][0].update(file='design/missing.md'),
                     lambda n: n['heavy_edge_registry']['variables']['n8_relief']['values'].append('free'),
                     lambda n: [e.update(level='L2') for e in n['heavy_edges'] if 'IV' in e['acts']],
                     lambda n: n['heavy_edges'][0]['when'].update(resolve_N3=['invented']),
                     lambda n: n['heavy_edges'][0]['snapshot_writes'].append('ending')]
        for label, mutate_model in [
                ('missing-model', lambda m: m['conditional_influences'].pop()),
                ('hard-gate', lambda m: m['screenplays'][1]['requires'].append('N17')),
                ('protected-effect', lambda m: m['conditional_influences'][0]['writes'].update(NE6=True))]:
            altered_model=deepcopy(model); mutate_model(altered_model)
            rejected,_=validate(net,altered_model)
            if not (set(rejected)-set(errors)): errors.append('negative-model-not-rejected-'+label)
        for index, mutate in enumerate(mutations):
            altered = deepcopy(net)
            mutate(altered)
            try:
                rejected, _ = validate(altered, model)
            except (KeyError, ValueError, OSError):
                rejected = {'fixture-invalid-' + str(index)}
            if not (set(rejected) - set(errors)):
                errors.append('negative-fixture-not-rejected-' + str(index))
    print(json.dumps({'scope': 'S201 design only; read-only, no runtime certification',
                      'heavy_edges': len(net['heavy_edges']), 'L3_by_act': counts,
                      'errors': errors, 'passed': not errors}, ensure_ascii=False, indent=2))
    return bool(errors)

if __name__ == '__main__':
    raise SystemExit(main())
