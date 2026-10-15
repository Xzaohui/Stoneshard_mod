"""Conditional HX projection shared by writers and the design evaluator.

This extension deliberately has no prerequisite or reward interface. Engine
bindings are specifications, not allocated event numbers or executable GML.
"""
from copy import deepcopy


def resolve_keys(net):
    return {k for e in net['heavy_edges'] for k in e['when'] if k.startswith('resolve_')} | {
        'resolve_'+p['task'].replace('-','_') for e in net['heavy_edges'] for p in e['sources']}

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
