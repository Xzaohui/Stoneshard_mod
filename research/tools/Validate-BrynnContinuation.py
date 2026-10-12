"""S85 scoped design evaluation; never opens or writes a game or player save."""
from pathlib import Path
import copy,hashlib,json,re

ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
m=read(ROOT/'research/brynn-continuation.json');b=read(ROOT/'research/city-campaign.json')
q={x['id']:x for x in m['quests']};base={x['id']:x for x in b['quests']}
legacy=read(ROOT/'research/design-model.json')['active_story']
targets={**base,**{x['id']:x for x in legacy},**q};errors=[];checks=[];scenarios=[]
def check(ok,label):(checks if ok else errors).append(label)
check(set(q)=={f'CS-BRY-{i}' for i in range(11,17)},'six-continuation-IDs-do-not-replace-original-eleven')
check(len(base)==73 and len(b['effects'])==314,'baseline-73-and-314-preserved')
check(len(m['effects'])==15 and len(q)+len(base)==79,'combined-registry-79-tasks-fifteen-bridge-groups')
check(b.get('continuation_registries',[{}])[0].get('file')=='brynn-continuation.json','supplement-discoverable-from-authoritative-baseline')
check(not m['runtime_verified'] and m['status']=='draft','design-only')
check(len(m['actors'])==7 and len({x['id'] for x in m['actors']})==7,'seven-distinct-original-persons')
check(len(m['spaces'])==6 and len({x['id'] for x in m['spaces']})==6,'six-distinct-mod-space-designs')
actors={a['id'] for a in m['actors']}|{a['id'] for a in b['dramatic_cast'].values()}
actors|={a['id'].removeprefix('BRY-NPC-') for a in m['actors']};actors.add('玩家')
scene_ids=[];line_ids=[]
for x in q.values():
    t=(V/x['file']).read_text(encoding='utf-8')
    check(not x['requires'] and not x['repeatable'],x['id']+'-independent-single-event')
    check(len(x['scenes'])==3 and len(x['routes'])==3,x['id']+'-three-scenes-three-actions')
    check(len({r['action'] for r in x['routes']})==3,x['id']+'-distinct-real-actions')
    check(x['reward_owner']==x['id'],x['id']+'-local-unique-reward-owner')
    check(all(w in t for w in ['## R：','X：','死亡优先','不同到达顺序','N17安全快照','询问、预览、读纸、关闭均不写']),x['id']+'-policy-in-screenplay')
    check(any(e['source']==x['id'] for e in m['effects']),x['id']+'-concrete-later-payoff')
    for i,s in enumerate(x['scenes']):
        scene_ids.append((x['id'],i))
        check(s['guard'] and s['choices'] and s['blocking'],x['id']+'-scene-knowledge-and-execution')
        for l in s['lines']:
            line_ids.append(l['id'])
            check(l['speaker'] in actors,l['id']+'-actual-known-speaker')
            check(l['text'] in t and l['guard'] in t,l['id']+'-emitted-guarded-dialogue')
    for r in x['routes']:
        check(all(r.get(k) for k in ['action','cost','result','line','receipt']),x['id']+'-'+r['key']+'-cost-and-limited-knowledge')
        check(r['line'] in t and r['action'] in t and r['receipt'] in t,x['id']+'-'+r['key']+'-active-full-method')
check(len(scene_ids)==18 and len(line_ids)==len(set(line_ids)),'eighteen-scenes-and-unique-dialogue-line-identities')
check(all(e['source'] in q and e['target'] in targets for e in m['effects']),'all-bridges-have-existing-targets')
for e in m['effects']:
    check(set(e['routes'])=={r['key'] for r in q[e['source']]['routes']},e['id']+'-all-three-source-methods-pay-off')
    check(set(e['route_dialogue'])==set(e['routes']),e['id']+'-three-specific-spoken-payoffs')
    check(len({p['early'] for p in e['route_dialogue'].values()})==3 and len({p['late'] for p in e['route_dialogue'].values()})==3,e['id']+'-not-one-generic-congratulation')
    check(e['early']!=e['late']!=e['missing'],e['id']+'-early-late-unknown-different')
    check(len(e['guard'])==4 and '不重复' in e['reward'] and '不改N17' in e['timing'],e['id']+'-scope-and-history')
    for endpoint in [e['source'],e['target']]:
        rel=targets[endpoint]['file'];p=ROOT/rel if rel.startswith('design/') else V/rel
        t=p.read_text(encoding='utf-8')
        check(e['id'] in t,endpoint+'-'+e['id']+'-bidirectional-integration')
        if endpoint not in q:
            check(e['early'] in t and e['late'] in t and e['missing'] in t,endpoint+'-'+e['id']+'-actual-target-side-lines')
            for pair in e['route_dialogue'].values():check(pair['early'] in t and pair['late'] in t,endpoint+'-'+e['id']+'-specific-spoken-route-variants-emitted')

# A separate minimal state machine exercises authorization and finite occupancy,
# not native GML. Commit requires both real execution AND final confirmation.
class Case:
    def __init__(self):
        self.resolve=None;self.history=[];self.paid=False;self.receipt=None
        self.authorized=False;self.alive=True;self.present=True;self.willing=True
        self.done=False;self.frozen={'N17':'sealed-original'};self.stock={'one-slot':1};self.held=[]
    def execute(self,method,actual=False,confirmation=False):
        if self.resolve or not actual or not confirmation:return False
        self.resolve=method;self.history.append(method);return True
    def share(self,scope,authorized=False):
        if not self.resolve or not authorized:return False
        self.receipt=scope;self.authorized=True;return True
    def respond(self,e):
        if not(self.alive and self.present and self.willing and self.authorized and self.receipt):return None
        return dict(line=e['route_dialogue'][self.resolve]['late' if self.done else 'early'],scope=self.receipt,
                    limit=e['routes'][self.resolve],future=e['action'])
    def reward(self):
        if not self.resolve or self.paid:return False
        self.paid=True;return True
    def hold(self):
        if self.stock['one-slot']<1:return False
        self.stock['one-slot']-=1;self.held.append('one-slot');return True

for e in m['effects']:
    for route in q[e['source']]['routes']:
        c=Case();key=route['key'];label=e['id']+'/'+key
        check(not c.execute(key) and not c.execute(key,confirmation=True),label+'-preview-reading-close-no-commit')
        check(not c.execute(key,actual=True),label+'-action-awaits-separate-confirmation')
        check(not c.share(route['receipt'],True),label+'-unearned-receipt-refused')
        check(c.execute(key,True,True) and c.hold(),label+'-confirmed-single-resource-action')
        check(not c.hold(),label+'-finite-occupied-resource-cannot-be-promised-twice')
        check(not c.share(route['receipt']) and c.respond(e) is None,label+'-refuse-sharing-no-secret-knowledge')
        check(c.share(route['receipt'],True),label+'-limited-scope-actually-shared')
        answer=c.respond(e);check(answer['scope']==route['receipt'] and answer['limit']==e['routes'][key],label+'-specific-method-scope')
        for field in ['alive','present','willing','authorized']:
            setattr(c,field,False);check(c.respond(e) is None,label+'-'+field+'-suppresses-new-lines');setattr(c,field,True)
        check(c.reward() and not c.reward(),label+'-reward-owner-once')
        before=copy.deepcopy((c.history,c.stock,c.frozen,c.resolve));c.done=True
        check(c.respond(e)['line']==e['route_dialogue'][key]['late'] and before==(c.history,c.stock,c.frozen,c.resolve),label+'-late-only-future-no-retcon-or-unfreeze')
        check(not c.execute('other',True,True),label+'-closed-route-not-reselected')
        scenarios.append(dict(effect=e['id'],method=key,scope=route['receipt'],future=e['routes'][key]))

# Hand-reviewed thematic counterexamples, independent of renderer iteration.
check('不能断言' in q['CS-BRY-11']['turn'] and '租船' in q['CS-BRY-11']['turn'],'no-official-night-ships-mystery-solution')
check('小科雷昂' in q['CS-BRY-13']['turn'] and '旧市长' in q['CS-BRY-13']['turn'],'dead-historian-and-old-murder-are-not-retconned')
check('计时' in q['CS-BRY-14']['hook'] and '不重置' in q['CS-BRY-14']['hook'],'native-boar-timer-and-services-preserved')
check('没有证据' in q['CS-BRY-14']['turn'],'missing-brother-not-declared-original-dead-guard')
e08=next(e for e in m['effects'] if e['id']=='BC85-08')
check('礼昂与雅尼明确是不同人' in e08['action'] and '普通连续' in e08['action'],'passgate-identity-test-not-replaced-by-brynn-wages')
final=q['CS-BRY-16']['scenes']
for l in final[1]['lines']:
    if l['speaker'] in ['MARIS','YANI','DARAN']:check(bool(l.get('fallback')) and 'CS-BRY' in l['guard'],l['id']+'-no-unearned-confession')
check(final[2]['lines'][0].get('fallback') and '旧CM' in final[2]['lines'][0]['guard'],'rena-old-deletion-confession-is-conditional')
local=read(ROOT/'research/brynn-local-lore-locators.json')
check(local['input'].lower().endswith('vanilla.win') and len(local['input_sha256'])==64,'original-input-provenance-not-modded-combination')
check(all(not x['original_text_saved'] and 'text_sha256' in x for x in local['rows']),'local-corpus-not-retained')
official=read(ROOT/'research/brynn-official-lore-source-fingerprints.json')
check(len(official)==2 and all(x['chars']>7000 and x['contents_sha256'] for x in official),'two-official-full-read-fingerprints')
for rel,h in read(ROOT/'research/brynn-continuation-note-hashes.json').items():
    check(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel+'-authoring-hash')
report=dict(date='2026-10-12',scope='S85 design notes, provenance, scoped receipt evaluator and hand-reviewed regressions; not literature approval, numeric economy or game runtime',
    additional_quests=6,combined_city_quests=79,baseline_single_method_receipts=314,additional_bridge_groups=15,additional_method_variants=45,scenes=18,methods=18,
    actors=7,spaces=6,bridges=15,method_payoff_cases=len(scenarios),checks_passed=len(checks),
    errors=errors,passed=not errors,scenarios=scenarios)
(ROOT/'research/brynn-continuation-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='scenarios'},ensure_ascii=False))
raise SystemExit(1 if errors else 0)
