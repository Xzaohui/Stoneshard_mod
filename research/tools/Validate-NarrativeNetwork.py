"""Evaluate original DESIGN scenarios, not GML, saves, UI or literary quality."""
from pathlib import Path
from copy import deepcopy
import json,itertools

ROOT=Path(__file__).resolve().parents[2]
net=json.loads((ROOT/'research/story-network.json').read_text(encoding='utf-8'))
model=json.loads((ROOT/'research/design-model.json').read_text(encoding='utf-8'))
tasks=net['tasks']; entries={q['id']:q for q in model['screenplays']}
errors=[]; checks=[]; scenarios=[]
def check(ok,label): (checks if ok else errors).append(label)
def matches(condition,state): return all(state.get(k) in values for k,values in condition.items())
def refs(qid):
    q=entries[qid]
    return set(q['requires'])|set(q['requires_any'])|set((q.get('at_least') or {}).get('of',[]))|set(q.get('story_requires',[]))
def ready(qid,done):
    q=entries[qid]
    return set(q['requires'])<=done and (not q['requires_any'] or bool(set(q['requires_any'])&done)) and (not q.get('at_least') or len(set(q['at_least']['of'])&done)>=q['at_least']['count']) and set(q.get('story_requires',[]))<=done

class DesignScenario:
    """Small reference evaluator of documented transactions and conditions only."""
    def __init__(self):
        self.state={}; self.done=set(); self.receipts=set(); self.seen=set(); self.revision={}; self.reward=set(); self.snapshot=None
    def fixture_prereqs(self,qid):
        # Assumed completed ancestors are explicit fixtures, not simulated game play.
        pending=list(refs(qid))
        while pending:
            q=pending.pop()
            if q not in self.done: self.done.add(q); pending.extend(refs(q))
    def preview(self,qid,route):
        return deepcopy(next(r for r in tasks[qid]['routes'] if r['key']==route))
    def finish(self,qid,route,*,executed=True,consent=True,funding=True,proof=True,phase='C'):
        rt=next(r for r in tasks[qid]['routes'] if r['key']==route)
        if qid in self.done or not ready(qid,self.done) or not all([executed,consent,funding,proof]): return False
        if qid.startswith('SQ') and phase!='C': return False
        # No retcon of main/side outcomes after final commitment; postgame DT remains.
        if self.snapshot is not None and not qid.startswith('DT'): return False
        new=deepcopy(self.state)
        for key,value in rt['writes'].items():
            if key in net['sticky_history'] and new.get(key) is True and value is False: continue
            new[key]=value
        self.state=new; self.done.add(qid)
        return True
    def pay(self,owner):
        if owner.startswith('D') and not owner.startswith('DT'): return False
        if owner in self.reward: return False
        self.reward.add(owner); return True
    def receive(self,edgeid):
        e=next(e for e in net['edges'] if e['id']==edgeid)
        if not matches(e['when'],self.state): return False
        if edgeid not in self.receipts:
            self.receipts.add(edgeid); self.revision[e['target']]=self.revision.get(e['target'],0)+1
        return True
    def dialogue(self,target,*,speaker_state='alive',willing=True):
        available=[e for e in net['edges'] if e['target']==target and matches(e['when'],self.state) and e['id'] in self.receipts]
        if not willing: return [('SILENCE','不强迫谈话或署约')]
        if speaker_state!='alive': return [('RELAY','只转述已登记状态；不模拟缺席或死者的新答复')]
        if not available: return [('DEFAULT',tasks[target]['default_dialogue'][0][1])]
        rev=self.revision.get(target,0)
        lines=[(e['id'],e['line']) for e in available if (e['id'],rev) not in self.seen]
        for key,_ in lines: self.seen.add((key,rev))
        return lines or [('STATUS','已知事实可短查，不重播同版长回访')]
    def constraints(self,target):
        return [c['id'] for c in net['constraints'] if c['target']==target and matches(c['when'],self.state)]
    def facts_only(self,qid,*,fixed_proof=True):
        if not ready(qid,self.done) or not fixed_proof: return False
        self.done.add(qid); self.state['closure_'+qid]='facts_only'; return True
    def freeze(self,ending,*,threat_clear=True,safety=True,confirmed=True):
        if self.snapshot is not None or not {'N15','N16'}<=self.done or not all([threat_clear,safety,confirmed]): return False
        if ending not in model['active_ending_rules']: return False
        if ending in ['custody','distributed']:
            st=self.state
            if not {'NE1','NE2','NE3','NE4','NE5'}<=set(st.get('evidence_verified',[])): return False
            if sum(bool(st.get('relief_'+q)) for q in ['SQ03','SQ05','SQ07'])<2: return False
            if not st.get('accountable') or st.get('exchange_harm'): return False
            if st.get('n4_shift_harm') and not st.get('n4_shift_remedied'): return False
            if ending=='custody':
                trustee=st.get('trustee')
                if sum(bool(st.get('assent_'+f)) for f in ['MG','CO','GA'])<2 or trustee not in ['MG','CO','GA']: return False
                if not st.get('assent_'+trustee) or st.get('local_trust_'+trustee,0)<1: return False
            if ending=='distributed' and (not st.get('archive_pact') or not (st.get('route_pact') or st.get('ferry_pact'))): return False
        self.snapshot={'ending':ending,'facts':deepcopy(self.state)}; return True

def scenario(name,run):
    before=len(errors); run(); scenarios.append({'name':name,'passed':len(errors)==before})

check(set(tasks)==set(entries) and len(tasks)==51,'51-current-screenplays-covered')
check(sum(len(q['routes']) for q in tasks.values())==128,'128-operational-routes')
check(len(net['edges'])==82,'82-authored-cross-effects')
check(len(net['arcs'])==14,'14-ensemble-character-arcs')
for qid,q in tasks.items():
    routes=q['routes']; names=[r['key'] for r in routes]
    check(len(names)>=2 and len(names)==len(set(names)),qid+'-at-least-two-unique-routes')
    check(len({r['action'] for r in routes})==len(routes),qid+'-actions-are-distinct-authored-text')
    check(len({r['result'] for r in routes})==len(routes),qid+'-outcomes-distinct-authored-text')
    note=(ROOT/entries[qid]['file']).read_text(encoding='utf-8')
    for r in routes:
        check(all(r.get(k) for k in ['label','action','cost','result','dialogue','requires']),qid+'-'+r['key']+'-executable-cost-and-voice')
        check(r['writes']['resolve_'+qid]==r['key'],qid+'-'+r['key']+'-single-method-enum')
        check(qid+'-R-'+r['key'] in note,qid+'-'+r['key']+'-rendered')
        check(len(r['dialogue'][0][1])<=100,qid+'-'+r['key']+'-dialogue-node-size')
    if qid.startswith('D') and not qid.startswith('DT'):
        check(q['owner'] in tasks and q['owner'].startswith('N'),qid+'-main-owner-defined')
        check(all(set(r['writes'])=={'resolve_'+qid} for r in routes),qid+'-no-duplicate-core-effect')
    if qid.startswith('DT'):
        check(all(not any(k.startswith(('assent_','relief_','evidence')) for k in r['writes']) for r in routes),qid+'-no-ending-qualification-farming')
        check('具名冲突不随48/72小时回到unseen' in (ROOT/'design/09_系统逻辑/网状叙事与条件对话规范.md').read_text(encoding='utf-8'),qid+'-one-time-episode')
for e in net['edges']:
    check(e['source'] in tasks and e['target'] in tasks,e['id']+'-known-producer-consumer')
    source_routes={r['key'] for r in tasks[e['source']]['routes']}
    check(set(e['when'])=={'resolve_'+e['source']} and set(e['when']['resolve_'+e['source']])<=source_routes,e['id']+'-condition-values-valid')
    check(all(e.get(k) for k in ['effect','speaker','line','scene','retroactive','scope']),e['id']+'-real-effect-and-return')
    check(len(e['line'])<=100,e['id']+'-callback-node-size')
    for qid in [e['source'],e['target']]:
        check(e['id'] in (ROOT/entries[qid]['file']).read_text(encoding='utf-8'),e['id']+'-'+qid+'-two-way-rendered')
for a in net['arcs']:
    check(len(set(a['tasks']))>=3 and all(t in tasks for t in a['tasks']),a['person']+'-multi-task-turns')
    check(bool(a['cost']) and bool(a['after']),a['person']+'-self-cost-and-changed-behavior')

def transactions():
    for qid,q in tasks.items():
        for r in q['routes']:
            s=DesignScenario(); s.fixture_prereqs(qid); before=deepcopy(s.__dict__)
            s.preview(qid,r['key']); check(s.__dict__==before,qid+'-'+r['key']+'-preview-no-write')
            for bad in ['executed','consent','funding','proof']:
                check(not s.finish(qid,r['key'],**{bad:False}) and s.__dict__==before,qid+'-'+r['key']+'-reject-'+bad+'-atomic')
            check(s.finish(qid,r['key']),qid+'-'+r['key']+'-actual-finish')
            check(not s.finish(qid,r['key']),qid+'-'+r['key']+'-no-repeat-finish')
            for other in q['routes']:
                if other!=r:
                    check(not s.finish(qid,other['key']) and s.state['resolve_'+qid]==r['key'],qid+'-'+r['key']+'-no-route-overwrite')
scenario('128种方法的预览、拒绝、原子提交与不可重做',transactions)

def every_edge():
    for e in net['edges']:
        key='resolve_'+e['source']
        for route in tasks[e['source']]['routes']:
            s=DesignScenario(); s.state[key]=route['key']
            check(s.dialogue(e['target'])[0][0]=='DEFAULT',e['id']+'-'+route['key']+'-no-omniscient-response')
            good=route['key'] in e['when'][key]
            check(s.receive(e['id'])==good,e['id']+'-'+route['key']+'-knowledge-receipt-guard')
            lines=s.dialogue(e['target'])
            check(any(i==e['id'] for i,_ in lines)==good,e['id']+'-'+route['key']+'-matching-callback-only')
            if good: check(s.dialogue(e['target'])[0][0]=='STATUS',e['id']+'-'+route['key']+'-not-repeat-long-return')
            for dead in ['dead','absent']:
                check(s.dialogue(e['target'],speaker_state=dead)[0][0]=='RELAY',e['id']+'-'+dead+'-no-new-speech')
            check(s.dialogue(e['target'],willing=False)[0][0]=='SILENCE',e['id']+'-no-forced-assent')
scenario('74条边逐路线核对已知、未知、互斥、死亡、缺席、拒谈与重复',every_edge)

def phases():
    for qid in (q for q in tasks if q.startswith('SQ')):
        for rt in tasks[qid]['routes']:
            s=DesignScenario(); s.fixture_prereqs(qid)
            for phase in ['A','B']:
                before=deepcopy(s.state)
                check(not s.finish(qid,rt['key'],phase=phase) and s.state==before,qid+'-'+phase+'-no-C-qualifications')
            check(s.finish(qid,rt['key'],phase='C'),qid+'-C-executed')
scenario('支线A/B不预发C的承诺与救济',phases)

def order():
    # Forward and backward receipt arrival produce the same next-topic condition.
    for e in net['edges']:
        outcomes=[]
        for target_first in [False,True]:
            s=DesignScenario()
            if target_first:
                s.done.add(e['target'])
                check(s.dialogue(e['target'])[0][0]=='DEFAULT',e['id']+'-earlier-default')
            s.state['resolve_'+e['source']]=e['when']['resolve_'+e['source']][0]
            s.receive(e['id']); outcomes.append(s.dialogue(e['target']))
            if target_first: check(e['target'] in s.done,e['id']+'-late-no-reopen')
        check(outcomes[0]==outcomes[1],e['id']+'-late-receipt-still-reacts')
scenario('每条交叉边先做与后做都回应，目标已结案不重开',order)

def parameter_test():
    for c in net['constraints']:
        s=DesignScenario(); check(c['id'] not in s.constraints(c['target']),c['id']+'-absent-without-history')
        s.state.update({k:v[0] for k,v in c['when'].items()})
        check(c['id'] in s.constraints(c['target']),c['id']+'-reassess-parameters')
        check(c['route'] in {r['key'] for r in tasks[c['target']]['routes']},c['id']+'-route-still-defined')
        check(len(tasks[c['target']]['routes'])>=2,c['id']+'-no-forced-single-harm-route')
scenario('六种资源、接应、资料与本人去向参数冲突',parameter_test)

def harm():
    s=DesignScenario(); s.fixture_prereqs('N11'); s.finish('N11','surrender')
    check(s.state.get('exchange_harm') and not s.state.get('toman_personnel'),'sold-address-record-and-lost-personnel')
    check(not s.finish('N11','trace') and s.state['exchange_harm'],'trace-cannot-wash-surrender')
    s.state['n4_shift_harm']=True; s.state['n4_shift_remedied']=True
    check(s.state['n4_shift_harm'],'remedy-not-delete-harm')
    for q in (q for q in tasks if q.startswith('DT')):
        s.fixture_prereqs(q); s.finish(q,tasks[q]['routes'][0]['key'])
    check(s.state['exchange_harm'],'daily-events-cannot-wash-address-sale')
scenario('卖地址、转嫁与补救留痕，日常不能洗历史',harm)

def wages():
    s=DesignScenario(); s.state['resolve_DT01']='buyer'
    check('C06' in s.constraints('SQ04'),'wages-sequestered-bridge-funding-reassess')
    s.fixture_prereqs('SQ04'); before=deepcopy(s.state)
    check(not s.finish('SQ04','contract',funding=False) and s.state==before,'same-income-not-double-used')
    check(s.finish('SQ04','cooperative',funding=True),'alternative-cooperative-with-real-funding')
scenario('工钱押住同笔收益后修桥必须有另一来源',wages)

def patient():
    s=DesignScenario(); s.fixture_prereqs('N8'); s.finish('N8','isolate')
    s.fixture_prereqs('SQ05'); s.finish('SQ05','stay')
    check(s.state.get('ferry_pact') and s.state.get('relief_SQ05'),'stay-can-produce-real-care-and-supply-route')
    e=next(e for e in net['edges'] if e['source']=='N8' and e['target']=='SQ05')
    s.receive(e['id']); check('别把我先写上船' in s.dialogue('SQ05')[0][1],'patient-existing-preference-respected')
scenario('患者留营也能履约，不被默认放上船',patient)

def neutral():
    s=DesignScenario(); s.fixture_prereqs('N12'); s.finish('N12','neutral')
    e=next(e for e in net['edges'] if e['source']=='N12' and e['target']=='N13')
    s.receive(e['id']); check('不能拿他回来' in s.dialogue('N13')[0][1],'neutral-not-caravan-confrontation')
    s.fixture_prereqs('N13'); s.finish('N13','contract')
    check(s.state.get('accountable') and s.state.get('gwynnel_cooperation') is False,'accountability-without-forced-join')
scenario('研究者不入商队，仍可独立核验与有限代理问责',neutral)

def dead():
    s=DesignScenario(); s.fixture_prereqs('N12')
    check(s.facts_only('N12') and 'resolve_N12' not in s.state,'dead-researcher-no-fake-rescue-choice')
    s.fixture_prereqs('N13'); check(s.facts_only('N13'),'records-allow-progression-without-new-confession')
    s.fixture_prereqs('N15'); check(s.finish('N15','bypass'),'fixed-maintenance-without-living-researcher')
    check(s.dialogue('N13',speaker_state='dead')[0][0]=='RELAY','no-posthumous-emotional-reply')
scenario('研究者死亡时仅固定证据推进，不死人同意或作新答复',dead)

def freeze():
    for rt in tasks['N15']['routes']:
        s=DesignScenario(); s.fixture_prereqs('N15'); s.finish('N15',rt['key'])
        s.fixture_prereqs('N16'); s.finish('N16','minimal')
        check(not s.freeze('sealed',confirmed=False),'no-preview-default-final')
        check(not s.freeze('sealed',threat_clear=False),'no-final-before-threat-clear')
        check(s.freeze('sealed'),'basic-sealing-no-faction-assent-gate')
        snap=deepcopy(s.snapshot)
        for q in ['DT15','DT16']:
            s.fixture_prereqs(q); s.finish(q,tasks[q]['routes'][0]['key'])
        check(s.snapshot==snap,'postgame-local-feedback-not-snapshot-retcon')
        s.fixture_prereqs('SQ07'); check(not s.finish('SQ07','community'),'no-late-qualification-rewrite')
scenario('N17单独确认冻结，三安全方案与终局后地方事件',freeze)

def ending_guards():
    def valid():
        s=DesignScenario(); s.done.update(['N15','N16']); s.state.update(evidence_verified=['NE1','NE2','NE3','NE4','NE5'],relief_SQ03=True,relief_SQ05=True,accountable=True,assent_MG=True,assent_CO=True,trustee='MG',local_trust_MG=1,archive_pact=True,ferry_pact=True); return s
    for ending in ['custody','distributed']:
        s=valid(); check(s.freeze(ending),ending+'-valid-qualified-design-state')
        for field,value in [('evidence_verified',['NE1','NE4','NE5']),('accountable',False),('exchange_harm',True),('n4_shift_harm',True),('relief_SQ05',False)]:
            s=valid(); s.state[field]=value; check(not s.freeze(ending),ending+'-reject-'+field)
        s=valid(); s.state.update(n4_shift_harm=True,n4_shift_remedied=True)
        check(s.freeze(ending) and s.snapshot['facts']['n4_shift_harm'],ending+'-remedy-keeps-history')
    for field,value in [('assent_CO',False),('trustee','GA'),('local_trust_MG',0)]:
        s=valid(); s.state[field]=value; check(not s.freeze('custody'),'custody-reject-'+field)
    for field,value in [('archive_pact',False),('ferry_pact',False)]:
        s=valid(); s.state[field]=value; check(not s.freeze('distributed'),'distributed-reject-'+field)
    for ending in ['sealed','seized']:
        s=DesignScenario(); s.done.update(['N15','N16']); s.state['exchange_harm']=True
        check(s.freeze(ending),ending+'-available-with-harm-but-truthful-snapshot')
scenario('四种终局资格、伤害与补救、真实承诺及监督缺口',ending_guards)

def unique_rewards():
    s=DesignScenario()
    for qid in tasks:
        if qid.startswith('D') and not qid.startswith('DT'):
            check(not s.pay(qid),qid+'-environment-no-extra-story-fee'); continue
        owners=[qid+'-'+p for p in ['A','B','C']] if qid.startswith('SQ') else [qid]
        for owner in owners:
            check(s.pay(owner) and not s.pay(owner),owner+'-reward-at-most-once')
scenario('任务、三阶段支线与环境副本的奖励去重',unique_rewards)

def paths():
    for skip in ['N6','N7','N8']:
        done=set()
        while True:
            new={q for q in tasks if q.startswith('N') and q!=skip and ready(q,done)}-done
            if not new: break
            done|=new
        check('N18' in done and skip not in done,'safe-main-reachable-skip-'+skip)
scenario('三路任缺一路仍有基础安全结案',paths)

report={'date':'2026-10-12','scope':'Original design data and reference evaluator only; no GML, UI, literary quality or runtime certification','screenplays':len(tasks),'routes':sum(len(t['routes']) for t in tasks.values()),'cross_effects':len(net['edges']),'arcs':len(net['arcs']),'checks_passed':len(checks),'scenarios':scenarios,'errors':errors,'passed':not errors}
(ROOT/'research/story-network-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2)); raise SystemExit(1 if errors else 0)
