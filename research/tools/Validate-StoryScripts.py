"""Validate the authored document graph and current screenplay coverage, not the game."""
from pathlib import Path
import json, re

ROOT=Path(__file__).resolve().parents[2]
def read(name): return json.loads((ROOT/'research'/name).read_text(encoding='utf-8-sig'))
model=read('design-model.json')
groups={'main':read('story-main.json')+read('story-main-late.json'),'side':read('story-side.json'),'daily':read('story-daily.json'),'dungeon':read('story-dungeon.json')}
regions=read('story-regions.json'); branches=read('story-branch-lines.json')
errors=[]; checks=[]
def check(condition,label):
    (checks if condition else errors).append(label)
def ready(q,done):
    if any(x not in done for x in q.get('requires',[])): return False
    alt=q.get('at_least')
    if alt and len(set(alt['of']) & done)<alt['count']: return False
    anyreq=q.get('requires_any')
    return not anyreq or bool(set(anyreq)&done)
def reach(skip):
    done=set()
    while True:
        new={q['id'] for q in groups['main'] if q['id']!=skip and ready(q,done)}-done
        if not new: return done
        done|=new

expected={'main':18,'side':8,'daily':16,'dungeon':9}
for kind,number in expected.items(): check(len(groups[kind])==number,f'{kind}-coverage-{number}')
allq=[q for g in groups.values() for q in g]
ids=[q['id'] for q in allq]
check(len(ids)==len(set(ids))==51,'unique-current-task-ids-51')
entries={e['id']:e for e in model['screenplays']}
check(set(entries)==set(ids),'manifest-matches-authored-screenplays')
scene_ids=[]; choice_ids=[]; lines=0
for kind,qs in groups.items():
    for q in qs:
        ident=q['id']; entry=entries[ident]
        note=(ROOT/entry['file']).read_text(encoding='utf-8')
        check('id: SCRIPT-'+ident+'\n' in note,f'{ident}-stable-note-id')
        for req in q.get('requires',[])+q.get('requires_any',[])+q.get('story_requires',[])+q.get('at_least',{}).get('of',[]):
            check(req in ids and not req.startswith('MQ'),f'{ident}-current-prerequisite-{req}')
        check(q['region'] in {r['id'] for r in regions},f'{ident}-known-region')
        count=3 if kind=='daily' else len(q['scenes'])
        check(entry['scenes']==count,f'{ident}-scene-manifest')
        for n in range(1,count+1):
            sid=f'{ident}-S{n:02}'; scene_ids.append(sid)
            check('### '+sid+' ' in note,f'{sid}-rendered')
        if kind=='daily':
            check(all(q.get(k) for k in ['opening','field','closing','failure','variants','state','deadline','reward']),f'{ident}-success-failure-repeat-complete')
            check(q['cooldown'] in (48,72),f'{ident}-game-time-cooldown')
            check('不产生正式承诺、终局救济或唯一装备' in note,f'{ident}-no-political-farming')
            for who,line in re.findall(r'\*\*DT\d+-S\d+-L\d+｜([^*]+)\*\*：「([^」]+)」',note):
                lines+=1
                check(bool(who) and len(line)<=100,f'{ident}-rendered-ordinary-dialogue-{lines}')
        else:
            check(bool(q.get('recovery')) and bool(q.get('outcome')),f'{ident}-recovery-and-epilogue')
            for s in q['scenes']:
                check(all(s.get(k) for k in ['name','place','beat','stage','setup','lines','exit']),f'{ident}-{s["name"]}-scene-complete')
                for who,line in s['lines']:
                    lines+=1
                    check(bool(who) and 0<len(line)<=100,f'{ident}-dialogue-{lines}-fits-one-node')
            keys=[c[0] for c in q['choices']]
            check(len(keys)==len(set(keys)),f'{ident}-choices-unique')
            for key,label,effect in q['choices']:
                cid=f'{ident}-C-{key}'; choice_ids.append(cid)
                check(cid in note and bool(label) and bool(effect),f'{cid}-explicit-effect')
                if kind in ('main','side'):
                    check(key in branches.get(ident,{}),f'{cid}-distinct-branch-dialogue')
                    if key in branches.get(ident,{}):
                        who,line=branches[ident][key]; lines+=1
                        check(len(line)<=100 and f'{ident}-B-{key}' in note,f'{cid}-branch-rendered')
        check('结算键' in note or '故事层仅登记' in note,f'{ident}-reward-owner-explicit')
check(len(scene_ids)==len(set(scene_ids))==158,'unique-scene-ids-158')
check(len(choice_ids)==len(set(choice_ids)),'choice-ids-unique-across-tasks')
paths=[]
for skip in ['N6','N7','N8','none']:
    done=reach(skip)
    evid={e for e,producers in model['active_evidence_producers'].items() if set(producers)&done}
    check('N18' in done,f'current-main-reaches-N18-skipping-{skip}')
    check({'NE1','NE4','NE5'}<=evid,f'baseline-and-fallback-evidence-skipping-{skip}')
    check(skip=='none' or skip not in done,f'skipped-chapter-not-falsely-complete-{skip}')
    check(all(ready(q,done) for q in groups['side']),f'all-side-entrances-reachable-skipping-{skip}')
    paths.append({'skipped':skip,'reachable':len(done),'reaches_N18':'N18' in done,'evidence':sorted(evid)})
check(model['active_evidence_producers']['NE4']==['N8','N13'],'NE4-independent-fallback-producer')
check(model['active_evidence_producers']['NE5']==['N15'],'tools-do-not-prematurely-certify-safety')
check(model['active_ending_rules']['sealed']=={'requires_quest':'N15','containment_ready':True},'basic-sealing-no-side-faction-or-survival-gate')
check('alive' not in json.dumps(model['active_ending_rules']),'researcher-death-does-not-lock-endings')
for ending in ['custody','distributed']:
    rule=model['active_ending_rules'][ending]
    check(rule.get('all_evidence') and rule.get('no_exchange_harm') and rule.get('shift_harm_absent_or_remedied'),f'{ending}-evidence-and-irreversible-harm-guards')
check(set(model['relief_producers'])=={'SQ03','SQ05','SQ07'},'relief-source-set-remains-unique-story-chains')
region_report=[]
for r in regions:
    nodes={n[0] for n in r['nodes']}; reached={r['entry']}
    check(len(nodes)==len(r['nodes']),r['id']+'-node-ids-unique')
    check(all(a in nodes and b in nodes for a,b in r['edges']),r['id']+'-edges-reference-real-nodes')
    while True:
        new=set(reached)
        for a,b in r['edges']:
            if a in reached: new.add(b)
            if b in reached: new.add(a)
        if new==reached: break
        reached=new
    check(reached==nodes,r['id']+'-all-nodes-walk-connected')
    check(any(n[2]=='服务' for n in r['nodes']),r['id']+'-basic-service')
    check(all(r.get(k) for k in ['services','danger','return','change','art','boundary']),r['id']+'-service-risk-return-art-lore')
    check(len(nodes)==next(m['nodes'] for m in model['regions'] if m['id']==r['id']),r['id']+'-budget-preserved')
    region_report.append({'region':r['id'],'nodes':len(nodes),'all_connected':reached==nodes})
check(sum(len(r['nodes']) for r in regions)==54,'54-functional-node-budget')
global_nodes={'BASE'}|{r['id'] for r in regions}
global_reached={'BASE'}
check(all(a in global_nodes and b in global_nodes for a,b in model['active_region_edges']),'current-global-edges-have-known-regions')
while True:
    new=set(global_reached)
    for a,b in model['active_region_edges']:
        if a in global_reached: new.add(b)
        if b in global_reached: new.add(a)
    if new==global_reached: break
    global_reached=new
check(global_reached==global_nodes,'all-six-current-regions-connected-to-base')
check('D01' not in ids and all('副本_D01_外港封账仓' not in q.get('links',[]) for q in allq),'retired-D01-not-active-dependency')
check([q['id'] for q in model['active_story']]==['N'+str(i) for i in range(1,19)],'manifest-current-main-order')
documents=(ROOT/'design/05_主线/文书与现场文本台本.md').read_text(encoding='utf-8')
docs=re.findall(r'^## (DOC-[^｜\s]+)',documents,re.M)
check(len(docs)==len(set(docs))==12,'12-original-document-ids')
report={'date':'2026-10-12','scope':'S61 scene material and document graph; legacy choices are retained comparison text, not active menus. S62 routes and callbacks have separate validation. Not dialogue UI or game runtime validation','counts':expected,'screenplays':51,'scenes':158,'dialogue_lines_checked':lines,'choices':len(choice_ids),'long_documents':len(docs),'paths':paths,'regions':region_report,'checks_passed':len(checks),'errors':errors,'passed':not errors}
(ROOT/'research/story-script-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
