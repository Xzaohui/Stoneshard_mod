"""Conditional HX projection shared by writers and the design evaluator.

This extension deliberately has no prerequisite or reward interface. Engine
bindings are specifications, not allocated event numbers or executable GML.
"""
from copy import deepcopy


def resolve_keys(net):
    return {k for e in net['heavy_edges'] for k in e['when'] if k.startswith('resolve_')} | {
        'resolve_'+p['task'].replace('-','_') for e in net['heavy_edges'] for p in e['sources']}

# Logical S62 resolve labels remain in the design model; the engine projection
# uses a separate namespace for the twelve incompatible route vocabularies.
ROUTE_TASKS = ('N3','N4','N5','N6','N7','N8','N16','N17','SQ01','SQ02','SQ03','SQ08')
def engine_name(name):
    return 'route_' + name[8:] if name.startswith('resolve_') and name[8:] in ROUTE_TASKS else name

def state_value(value):
    return str(value).lower() if isinstance(value, bool) else value

def condition_map(condition):
    return {engine_name(k): [state_value(v) for v in vs] for k, vs in condition.items()}

def support_stubs(net, *, settlement=False):
    """Executed choices only; settlement=True projects legacy resolve writes separately.

    Neither section plays legacy callbacks or gives rewards.
    """
    out = []
    def add(task, node, sets, when=None, rule='实际处置并确认后提交；预览、关闭、人物守卫失败不写'):
        out.append(dict(event=f'evt_{task}_{node}', script=task, node=node,
                        trigger='on_route_selected', when=when or {},
                        reads=sorted((when or {}).keys()), writes=list(sets), sets=sets,
                        cooldown='once', engine_event=None, rule=rule))
    for task in ROUTE_TASKS:
        for route in net['tasks'][task]['routes']:
            add(task, 'route_'+route['key'], {'route_'+task: route['key']},
                rule='S62 实际路线选择；与旧 choice 独立，不写旧 resolve/callback；HX 回执由 receipt 桩控制，无需新增 callback')
    # Legacy choice stubs only play callbacks. Explicit settlement producers
    # supply values read by HX without changing those historical stubs.
    requested={}
    for edge in net['heavy_edges']:
        for name,values in edge['when'].items():
            if name.startswith('resolve_') and name[8:] not in ROUTE_TASKS:
                requested.setdefault(name,set()).update(values)
    route_end = len(out)
    for name,values in sorted(requested.items()):
        for value in sorted(values):
            add(name[8:], 'settle_'+value, {name:value},
                rule='对应 choice 的实际处置确认提交点；旧 choice 仍只播 callback，不由回执代写结算')
    settlements = out[route_end:]
    del out[route_end:]
    if settlement:
        return settlements
    for name, definition in net['heavy_edge_registry']['variables'].items():
        for task in definition['writer_tasks']:
            for value in definition['write_values']:
                if name == 'custody_signed' and value == definition['default']:
                    continue  # none means no signed confirmation has occurred.
                when = {'custody_intent': [value]} if name == 'custody_signed' else {}
                add(task, name+'_'+str(value).lower(), {name: state_value(value)}, when,
                    definition['commit']+'；仅本节点实际执行对应处置后写入；'+definition['update_mode'])
    for value in ('false','true'):
        add('N12', 'toman_personnel_'+value, {'toman_personnel':value},
            rule='N12 实际交人写 true；实际拒交写 false；须本人在场、存活且授权，不由预览或回执代写')
    return out

def project(net, base_keys=()):
    variables = net['heavy_edge_registry']['variables']
    effects, stubs, keys = [], [], {}
    base = {x['key']: x for x in base_keys}
    def key(name, values, default, owner):
        keys[name] = dict(key=name, engine_key='EAO_' + name, values=values,
                          default=default, script=owner, source='research/story-network.json')
    for name, v in variables.items():
        key(name, v['values'], v['default'], '/'.join(v['writer_tasks']))
    for e in net['heavy_edges']:
        ident = e['id']; receipt = 'receipt_' + ident
        key(receipt, [False, True], False, ident)
        conditions = [e['when']] + list(e.get('branches', {}).values())
        reads = set(k for c in conditions for k in c)
        reads.update('resolve_' + p['task'].replace('-', '_') for p in e['sources'])
        if ident == 'HX07':
            key('order_HX07', ['none', 'N6', 'N7', 'N8'], 'none', ident)
            reads.add('order_HX07')
        for name in reads:
            if name not in keys:
                values = list(dict.fromkeys(v for c in conditions for v in c.get(name, [])))
                if name.startswith('resolve_'):
                    task = name[8:].replace('_', '-')
                    if task in net['tasks']:
                        values = [r['key'] for r in net['tasks'][task]['routes']]
                    elif name in base:
                        values = [v for v in base[name]['values'] if v != 'none']
                    key(name, ['none'] + values, 'none', task)
                else:
                    key(name, [False, True], False, ident)
        effect = deepcopy(e)
        effect.update(kind='conditional_influence', hard_requires=[], receipt_key=receipt,
                      order_rule='last_completed_of_N6_N7_N8' if ident == 'HX07' else None)
        effects.append(effect)
        for phase, trigger, writes in [('receipt', 'on_state_change', [receipt]),
                                        ('evaluate', 'on_state_read', []),
                                        ('commit', 'on_route_selected', list(e['writes']))]:
            stubs.append(dict(event=f'evt_{ident}_{phase}', script=ident, node=phase,
                              trigger=trigger, when=deepcopy(e['when']),
                              reads=sorted(reads | {receipt}), writes=writes,
                              cooldown='once' if phase != 'evaluate' else 'repeatable',
                              sources=[p['task'] for p in e['sources']],
                              targets=[p['task'] for p in e['targets']],
                              guards=deepcopy(e['guards']), engine_event=None,
                              rule=('源实际结算后交付有限回执' if phase == 'receipt' else
                                    '只重评未来参数；人物守卫失败走固定物证/基础出口' if phase == 'evaluate' else
                                    '仅实际源处置提交历史后果；不以回执或预览提交')))
    for task in ROUTE_TASKS:
        key('resolve_'+task, ['none']+[r['key'] for r in net['tasks'][task]['routes']], 'none', task)
    for item in keys.values():
        item['key'] = engine_name(item['key'])
        item['engine_key'] = 'EAO_' + item['key']
        item['values'] = [state_value(v) for v in item['values']]
        item['default'] = state_value(item['default'])
        if item['key'].startswith('route_'): item['kind'] = 'route'
        if item['default'] in ('none', 'unseen') or item['key'].startswith('receipt_') or item['key'] in ('n4_shift_remedied', 'toman_personnel'):
            item['note'] = '缺省值代表未发生；初始化即提供该可读值，无需默认值生产者。'
        if item['key'] == 'toman_personnel':
            item['note'] += 'false 表示尚未交人，也可由实际拒交写入；初始 false 不证明拒交事件发生。'
        if item['key'] == 'sylang_state':
            item['note'] = 'alive 是初始生存状态，不代表死亡或其他处置发生。'
    for stub, effect in zip(stubs, [e for e in effects for _ in range(3)]):
        stub['when'] = condition_map(stub['when'])
        stub['reads'] = sorted(engine_name(k) for k in stub['reads'])
        stub['writes'] = [engine_name(k) for k in stub['writes']]
        stub['sets'] = ({'receipt_'+stub['script']: 'true'} if stub['node'] == 'receipt' else
                        {engine_name(k): state_value(v) for k,v in effect['writes'].items()} if stub['node'] == 'commit' else {})
    return effects, stubs, sorted(keys.values(), key=lambda x: x['key'])


def matches(condition, state):
    return all(any(type(state.get(k)) is type(v) and state.get(k) == v for v in vs)
               for k, vs in condition.items())


def receive(s, e, *, delivered=True):
    if not delivered or not matches(e['when'], s.state):
        return False
    if e['id'] == 'HX07' and s.state.get('order_HX07') not in ['N6', 'N7', 'N8']:
        return False
    s.receipts.add(e['id'])
    return True


def evaluate(s, e, target, *, alive=True, present=True, willing=True, authorized=True):
    if target not in {p['task'] for p in e['targets']}:
        return None
    if e['id'] not in s.receipts or not matches(e['when'], s.state):
        return None
    if e['id'] == 'HX07' and s.state.get('order_HX07') != target:
        return None
    if not all([alive, present, willing, authorized]):
        return dict(mode='fallback', effect=e['fallback'], writes={})
    return dict(mode='local_callback' if s.snapshot is not None or target in s.done else 'future_parameters',
                effect=e['effect'], branches=[b for b, c in e.get('branches', {}).items() if matches(c, s.state)],
                writes={})


def commit(s, effects, source, *, executed=True):
    if not executed or s.snapshot is not None:
        return False
    for e in effects:
        if source in {p['task'] for p in e['sources']} and matches(e['when'], s.state):
            s.state.update(deepcopy(e['writes']))
    # The last of the three actually completed routes gets the late variant.
    if source in ['N6', 'N7', 'N8'] and {'N6', 'N7', 'N8'} <= s.done:
        s.state.setdefault('order_HX07', source)
    return True
