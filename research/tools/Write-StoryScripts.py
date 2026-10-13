"""Write original narrative drafts into the Obsidian vault; never reads/writes game files."""
from pathlib import Path
import json, re, hashlib

ROOT = Path(__file__).resolve().parents[2]
VAULT = ROOT / 'design'
DATE = '2026-10-12'
HASH_FILE = ROOT / 'research/story-generated-note-hashes.json'
old_hashes = json.loads(HASH_FILE.read_text(encoding='utf-8')) if HASH_FILE.exists() else {}
for relative, expected in old_hashes.items():
    target = ROOT / relative
    if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
        raise SystemExit(f'Generated note changed outside the authoring model; preserve and reconcile before regeneration: {relative}')
generated_hashes = {}

def read(name):
    return json.loads((ROOT / 'research' / name).read_text(encoding='utf-8-sig'))

model = read('design-model.json')
main = read('story-main.json') + read('story-main-late.json')
side, daily, dungeons, regions = (read('story-' + k + '.json') for k in ['side', 'daily', 'dungeon', 'regions'])
branches = read('story-branch-lines.json')
network = read('story-network.json')
all_tasks = main + side + daily + dungeons
region_names = {r['id']: Path(r['file']).stem for r in model['regions']}
region_files = {r['id']: r['file'] for r in model['regions']}
task_names = {q['id']: f"台本_{q['id']}_{q['name']}" for q in all_tasks}
lookup = {q['id']: q for q in all_tasks}
paths = {}
english_titles={}
for prefix, titles in [
    ('N',['The Bellless Night','No Headstone on the Ash Embankment','The Light Before the Hearing','The First Blank Debt Note','Three Accounts of the Ferry','The Sealed Page Numbers','The Empty Name in the Quartermaster Ledger','The Fever That Will Not Fade','Evidence on the Table','The Unwritten Witness','The Exchange Outside the Pass','The Missing Still Have Names','The Price of an Answer','A Way Back','An Echo Is Not the Truth','Who Keeps the Embers','The Well of Residual Light','After the Oath']),
    ('SQ',['Harbor Dues and Freedom','The Requisitioned Winter Grain','Bread Without a Royal Banner','A Road That Does Not Sell People','The Ferry and the Names','The Reverse of the Copy','Medicine Is Not Absolution','The Deserter’s Letter']),
    ('DT',['The Last Stretch of the Grain Road','Clean Well Water','An Unclaimed Grave Marker','Clear Ground Before Harvest','Urgent Supplies for the Inn','Signs for the Lost Traveler','A Crate That Should Stay Sealed','Repair the Second Bridge Plank','The Herbs the Apothecary Named','Keep Wolves Away from the Night Watch','Delivery of Two Copies','Repairs at the Old Bell Station','Enough Soup to Share','A Rusted Seal and False Papers','Patrol After Sealing','Those Who Choose Further Care'])]:
    for i,t in enumerate(titles,1): english_titles[prefix+(str(i) if prefix=='N' else f'{i:02}')]=t
for i,t in enumerate(['Old Canal Maintenance Tomb','Broken Bridge Toll Station','Maen Sealed Book Store','Abandoned Academy Test Yard','Basalt Pass Supply Cellar','Ash Infirmary','Flooded Archive Well','Unnamed Monastery Echo Hall','Well of Residual Light'],2): english_titles[f'D{i:02}']=t

def wl(name): return f'[[{name}]]'
def tasklinks(ids): return ' · '.join(wl(task_names[x]) for x in ids) or '无任务硬前置'
def ordinary_lines(text, default):
    roles=['药师助手','运货员','护理者','守墓人','农户','玩家','修桥工','旅人','供应员','接收员','看守','维护者','小贩','掌勺人','巡查员','抄写员']
    result=[]
    for prefix,line in re.findall(r'([^。！？：]+)：‘([^’]+)’',text):
        role=next((r for r in roles if r in prefix),default)
        result.append([role,line])
    return result or [[default,re.findall(r'‘([^’]+)’',text)[-1] if '‘' in text else text]]
def ordinary_setup(text):
    return re.sub(r'[^。！？：]+：‘[^’]+’','',text).strip('。； ') or '人物在公告指定的现场核对结果，工作完成后回民用服务点交付。'
def front(title, ident, kind, tags='story-script'):
    return f'---\ntitle: "{title}"\nid: {ident}\ntype: {kind}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: {DATE}\ntags: [stoneshard, {tags}, screenplay]\naliases: []\n---\n\n# {title}\n\n'
def write(rel, text):
    from CityLinks import add_city_links
    text = add_city_links(ROOT,rel,text)
    p=VAULT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
    generated_hashes['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return 'design/' + rel
def preserve_foreign(rel, text):
    # Wholesale-regenerated notes keep registry blocks owned by later phases.
    p=VAULT / rel
    if not p.exists(): return text
    old=p.read_text(encoding='utf-8-sig')
    blocks=[m.group(0) for m in re.finditer(r'<!--\s*[A-Za-z0-9-]+:BEGIN\s*-->.*?<!--\s*[A-Za-z0-9-]+:END\s*-->', old, re.S)]
    return text.rstrip()+'\n\n'+'\n\n'.join(blocks)+'\n' if blocks else text
def supplement(name, body):
    found=list(VAULT.rglob(name + '.md'))
    if len(found)!=1: raise ValueError(f'Expected one note: {name}')
    p=found[0]; text=p.read_text(encoding='utf-8-sig')
    begin='<!-- STORY-SCRIPT-20261011:BEGIN -->'; end='<!-- STORY-SCRIPT-20261011:END -->'
    block=begin+'\n## 2026-10-12台本修订（当前优先）\n\n'+body+'\n'+end+'\n\n'
    if begin in text:
        text=re.sub(re.escape(begin)+r'.*?'+re.escape(end)+r'\s*', lambda _:block, text, flags=re.S)
    else:
        text=re.sub(r'(?m)^(# [^\n]+\n)', lambda m:m.group(1)+'\n'+block, text, count=1)
    p.write_text(text, encoding='utf-8')

for group, folder in [(main,'05_主线/台本'),(side,'06_支线/台本'),(daily,'07_日常任务/台本'),(dungeons,'08_副本/台本')]:
    for q in group:
        qid=q['id']; name=task_names[qid]
        b=front(name,'SCRIPT-'+qid,'screenplay')
        b+='> [!info] 创作与实现口径\n> S61用户要求先写台本。本页全部为Mod原创对白与设计变量；原作背景约束来自关联基线，未新增核验网页。'+('N1已有0.3.0逻辑小样，本稿新增细节与对白不等于已经编入游戏。' if qid=='N1' else '本页尚未实现为可玩任务。')+'\n\n'
        b+='## 任务定位与触发\n\n'+f"设计ID：{qid}；工作英文标题：{english_titles[qid]}（Mod原创译题，非官方任务名）。\n\n"+q['premise']+'\n\n'
        b+='区域：'+wl(region_names[q['region']])+'；方向入口：'+wl('任务台本总索引')+'。\n\n'
        b+='前置：'+tasklinks(q.get('requires',[]))+'。'
        if q.get('at_least'): b+=f"另须以下完成至少{q['at_least']['count']}项："+tasklinks(q['at_least']['of'])+'。'
        if q.get('requires_any'): b+='以下任一完成：'+tasklinks(q['requires_any'])+'。'
        if q.get('secondary_region'): b+='后段可进入'+wl(region_names[q['secondary_region']])+'，从N5公开路线，不依赖N8完成。'
        if q.get('story_requires'): b+='故事内段另须'+tasklinks(q['story_requires'])+'，此前仅普通外围。'
        b+='\n\n'+wl('台本编写规则与对白口径')+'规定接取、事实、执行、回访分开；章节无隐藏全局倒计时。询问、预览、拒绝与关闭对白均不自动结算。\n\n'
        nq=network['tasks'][qid]
        b+='## 当前网状叙事与对话树（S62优先）\n\n'
        b+='> [!important] 2026-10-12修订\n> 以下方案、条件回应与人物后果是当前实现依据。下方S61场次保留为场面素材，不是无条件按顺序播放的对话；旧选择表仅作初稿对照，不进入当前选项菜单。'+('本日常ID现对应一次人物事件，不按冷却重演。' if q in daily else '')+'\n\n'
        b+='**目标**：'+nq['goal']+'\n\n**人物冲突**：'+nq['conflict']+'\n\n'+nq['commit']+'\n\n'
        b+='### 可执行解法\n\n| 路线键 | 玩家意图 | 执行与核验 | 真实成本 | 结果与人物变化 |\n| --- | --- | --- | --- | --- |\n'
        for rt in nq['routes']:
            b+=f"| {qid}-R-{rt['key']} | {rt['label']} | {rt['action']} | {rt['cost']} | {rt['result']} |\n"
        b+='\n共用会话入口：未知事实→询问与现场核验→显示当前可行方案、成本和替代→确认执行→核结果→只提交一次→按当前人物处境回访。只看见选项不写resolve_'+qid+'；该字段记录实际完成方法，不代表本人存活、同意或某份证据已认证。\n\n'
        for rt in nq['routes']:
            b+='执行守卫（'+qid+'-R-'+rt['key']+'）：'+'；'.join(rt['requires'])+'。\n\n'
            b+=f"**{qid}-R-{rt['key']}-L01｜{rt['dialogue'][0][0]}**：「{rt['dialogue'][0][1]}」\n\n播放条件：resolve_{qid}={rt['key']}且说话者在场、存活并愿谈；否则用柜员说明已记录结果，不复刻死者的新回答。\n\n"
        b+='### 前事怎样改变本场对话与行动\n\n'
        incoming=[e for e in network['edges'] if e['target']==qid]
        if not incoming:
            b+='这是新冲突的起点，不假定玩家已完成其他支线。默认问题从本人的需要开始。\n\n'
        for e in incoming:
            keys=', '.join(e['when'][f"resolve_{e['source']}"])
            b+=f"**{e['id']}**｜来源{wl(task_names[e['source']])}；条件resolve_{e['source']}∈[{keys}]且目标已收到本案有限回执或玩家告知后核验、说话者存活在场愿谈；场次：{e['scene']}。\n\n实际影响：{e['effect']}\n\n**{e['id']}-L01｜{e['speaker']}**：「{e['line']}」\n\n先后顺序：{e['retroactive']}\n\n"
        b+='默认回应（没有上述相关已知事实时）：'+f"**{qid}-DEFAULT｜{nq['default_dialogue'][0][0]}**：「{nq['default_dialogue'][0][1]}」\n\n"
        b+='### 本任务影响的后事\n\n'
        outgoing=[e for e in network['edges'] if e['source']==qid]
        b+=('\n'.join(f"- {e['id']} → {wl(task_names[e['target']])}：{e['effect']}" for e in outgoing) if outgoing else '独立冲突结果写入地方履约记录；不凭空授予政治承诺。')+'\n\n'
        b+='对话条件、缺席替代、迟到信息与路线提交规则见'+wl('网状叙事与条件对话规范')+'；人物多阶段变化见'+wl('人物弧光与关系转折')+'；边与场景验收见'+wl('叙事交叉影响矩阵')+'。\n\n'
        constraints=[c for c in network['constraints'] if c['target']==qid]
        if constraints:
            b+='### 路径资源重评\n\n'+'\n'.join(f"- {c['id']}｜{c['when']} → {c['route']}的{c['parameter']}：{c['change']}" for c in constraints)+'\n\n'
        policies=[k for k,v in network['policy_nodes'].items() if qid in v['tasks']]
        if policies:
            b+='### 解法之外的处置节点\n\n'
            for p in policies:
                rule=network['policy_nodes'][p]
                b+='- '+p+'：'+rule['default']+'；另可选'+ '／'.join(rule['options'])+'。条件：'+rule['guard']+'。\n'
            b+='\n这些是授权与处置选择，不充作第二套解法数量。\n\n'
        if q in daily:
            b+='## 一次人物事件与普通服务\n\n'+q['deadline']+'旧计划冷却值'+str(q['cooldown'])+'小时仅保留为历史字段，不刷新同一冲突。\n\n'+q['state']+'\n\n'
            first=re.search(r'玩家：‘([^’]+)’',q.get('field') or '')
            open_line=first.group(1) if first else '我先听两边。接受调查，不等于已经替你们选了办法。'
            mid_line=q.get('player_mid') or '事实查清后，成本和谁能拒绝也要讲清。'
            close_line=q.get('player_close') or '这次怎样做，留在回执里。以后再见面也不能当作没发生。'
            q['scenes']=[
                {'name':'当事人提出互相冲突的需要','place':region_names[q['region']],'beat':'起','stage':'unseen→active','setup':'两方各讲自己拥有的权利与缺口，不用柜员派送货清单。','lines':[[q['speaker'],q['opening']],['玩家',open_line]],'exit':'明确接受本人物事件；拒绝不重置他人的生活或强制刷新相同受害者。'},
                {'name':'事实与解法预览','place':'本案现场与中立会谈点','beat':'承与转','stage':'active→事实可核','setup':nq['conflict'],'lines':[['玩家',mid_line]],'exit':'采用上方路线核验；非玩家专业劳务由有限付费服务执行。'},
                {'name':'选择后的关系','place':'本案回访点','beat':'合','stage':'事实可核→resolved','setup':'按实际路线播放上方R键对白，不同时播放两条互斥结果。','lines':[['玩家',close_line]],'exit':'任务ID唯一提交；后续按X边读取结果，不重播初次冲突。'}]
        if q in dungeons:
            b+='## 几何、进出与危险\n\n'+q['shape']+'\n\n通路：'+q['route']+'\n\n危险：'+q['hazard']+'\n\n关联主线：'+tasklinks(q['main'])+'；支线：'+tasklinks(q['side'])+'。副本环境台本不再次发同一主线奖励。\n\n'
        b+='## 逐场素材（按上方条件剪裁）\n\n下列镜头不组成自动播完的直线；互斥台词、死者答复与未经本人授权的去向必须按S62规范替换。\n\n'
        for n,s in enumerate(q['scenes'],1):
            sid=f'{qid}-S{n:02}'
            b+=f"### {sid} {s['name']}\n\n场所：{s['place']}；段落：{s['beat']}；状态：{s['stage']}。\n\n场面调度：{s['setup']}\n\n"
            for j,(who,line) in enumerate(s['lines'],1):
                b+=f'**{sid}-L{j:02}｜{who}**：「{line}」\n\n'
            b+='出口与执行：'+s['exit']+'\n\n'
        if q.get('choices'):
            b+='## S61旧选择对照（停用，保留修订依据）\n\n这些键不与S62解法同时出现在菜单中；有效原有状态的映射另见网状规范，绝不读取旧表自动提交新路线。\n\n| 旧选择键 | 初稿选项 | 初稿设想（需按S62核验） |\n| --- | --- | --- |\n'
            for key,label,effect in q['choices']: b+=f'| {qid}-C-{key} | {label} | {effect} |\n'
            b+='\n意向选择与实际执行分开；需要回到指定场所确认的结果，不在选择预览里提交。\n\n'
            for key,_,_ in q['choices']:
                if key in branches.get(qid,{}):
                    who,line=branches[qid][key]
                    b+=f'**{qid}-B-{key}｜{who}**：「{line}」\n\n'
        if q in daily:
            b+='## 拒绝、缺席与不可重复冲突\n\n'+q['failure']+'\n\n'+q['variants']+'\n\n丢失已登记绑定副件可同号补领使旧副件失效；不靠道具补领重新结算。\n\n'
        else:
            b+='## 结案、回访与恢复\n\n'+q['outcome']+'\n\n'+q['recovery']+'\n\n'
        b+='## 文书、奖励与状态边界\n\n'
        evid=q.get('evidence',[])
        b+='证据：'+('、'.join(evid) if evid else '不新增核心证据认证')+'；口供、幻象或单个原件不得自动成为verified。参照'+wl('当前任务依赖与状态字典')+'、'+wl('当前证据链与结局条件')+'。\n\n'
        b+='奖励：'+q['reward'].rstrip('。')+'。B为'+wl('经济与奖励')+'的待校准难度档基准，不是已确定冠数。'
        if qid.startswith('SQ'): b+=f'结算键分别为{qid}-A/B/C；C的协议／救济只能写一次。'
        elif qid.startswith('DT'): b+='结算键为人物事件ID；不产生正式承诺、终局救济或唯一装备。不能按冷却再次结算同一事件。'
        elif qid.startswith('N'): b+='结算键为任务ID；无第二次回访金币。'
        else: b+='故事层仅登记dungeon_story_state；任务费由关联任务提交，普通战利品不含关键证据。'
        b+='\n\n长条款与记录在'+wl('文书与现场文本台本')+'保存；现阶段为文本草稿，未来才映射物品。调查登记后丢失可恢复不售副件，不能固定要求每章集齐三份纸。\n\n'
        nxt=[t['id'] for t in main+side if qid in t.get('requires',[])+t.get('requires_any',[])+t.get('at_least',{}).get('of',[])]
        b+='后续／可选关联：'+(tasklinks(nxt) if nxt else '无强制后续任务')+'。\n\n'
        links=q.get('links',[])+['台本新增人物与知识边界','新区域设计与任务总表']
        b+=' · '.join(wl(x) for x in dict.fromkeys(links))+'。\n'
        paths[qid]=write(folder+'/'+name+'.md',preserve_foreign(folder+'/'+name+'.md',b))

# Add semantic backlinks to existing entity cards; prior logic is explicitly historical.
back={}
for q in all_tasks:
    for name in q.get('links',[]): back.setdefault(name,[]).append(task_names[q['id']])
for name, linked in back.items():
    supplement(name,'当前逐场台本：'+' · '.join(wl(x) for x in linked)+'。采用'+wl('当前任务依赖与状态字典')+'及'+wl('当前证据链与结局条件')+'；下方旧MQ编号、前置与开发记录保留为历史，冲突时以上述新稿为准。')
for q in daily:
    card=next(x for x in model['daily_templates'] if x['id']==q['id'])
    supplement(Path(card['file']).stem,'对应完整短台本：'+wl(task_names[q['id']])+'。当前前置采用新N编号；下方旧MQ前置为历史。期限和冷却以台本及'+wl('日常委托规则')+'为准。')
supplement('开篇_无钟之夜','补充完整台本：'+wl(task_names['N1'])+'。0.3.0已有执行逻辑与本稿新增对白分开；没有再次编译或部署游戏包。后续按'+wl('当前任务依赖与状态字典')+'接入。')
for card in model['main_quests']:
    if card['id'] in ['MQ01','MQ02']: continue
    idx=int(card['id'][2:])
    repl=['N2','N4'] if idx in [3,4] else ['N'+str(idx)]
    supplement(Path(card['file']).stem,'本页为历史蓝图，不继续按旧前置实现。叙事功能当前由'+tasklinks(repl)+'承担；不是存档自动迁移。当前总入口：'+wl('任务台本总索引')+'。')

for r in regions:
    tasks=[q['id'] for q in all_tasks if q['region']==r['id'] or q.get('secondary_region')==r['id']]
    english_region={'R01':'Bryn Outer Harbor and Old Canal','R02':'Denbrie West Road and Ferry','R03':'Maen Outskirts','R04':'Royal Pass and Border Settlement','R05':'Ash Basin and Infirmary Villages','R06':'Unnamed Monastery Highlands'}
    b=f"设计ID：{r['id']}；工作英文区域名：{english_region[r['id']]}（新增区域译题，非官方地图名）。\n\n当前区域主题：**"+r['theme']+'**。\n\n'
    for h,k in [('设计理念','concept'),('视觉与情绪','mood'),('空间玩法','movement')]: b+=f'### {h}\n\n{r[k]}\n\n'
    b+='### 功能节点与通路\n\n节点是设计预算，不是已铺设世界方块；子房间不重复算节点。\n\n| ID | 地点 | 类型 | 叙事与玩法职责 |\n| --- | --- | --- | --- |\n'
    for nid,name,kind,role in r['nodes']: b+=f"| {r['id']}-{nid} | {name} | {kind} | {role} |\n"
    labels={n[0]:n[1] for n in r['nodes']}
    b+='\n双向可走边：\n\n'+ '\n'.join('- '+labels[a]+' ↔ '+labels[z] for a,z in r['edges'])+'\n\n'
    for h,k in [('服务与原作接口','services'),('危险与预警','danger'),('回程及敌对替代','return'),('任务后的可见变化','change'),('美术制作与生图需求','art'),('原作设定边界','boundary')]: b+=f'### {h}\n\n{r[k]}\n\n'
    b+='### 关联任务台本\n\n'+tasklinks(tasks)+'。\n\n'+wl('新区域设计与任务总表')+' · '+wl('地图扩张总图')+' · '+' · '.join(wl(x) for x in r['links'])+'。\n\n下方区域初稿与旧MQ分配保留为历史；本节是当前任务与节点安排。'
    supplement(region_names[r['id']],b)

index=front('任务台本总索引','SCRIPT-INDEX','index')
index+='S62已按网状叙事复核：51篇台本覆盖18主线、8支线链（24阶段）、16一次地方人物事件、9个有效副本环境故事。每页顶部是当前多解路径和跨任务条件回应；S61场次作素材，旧选择停用。故事结构仍有四幕安全骨架，幕内路线、人物议题和后续接应互相影响，不冒称完全无序沙盒。旧MQ01/MQ02与D01退役。\n\n'+wl('叙事逻辑校验与修订记录')+' · '+wl('网状叙事与条件对话规范')+' · '+wl('人物弧光与关系转折')+' · '+wl('叙事交叉影响矩阵')+' · '+wl('台本编写规则与对白口径')+' · '+wl('新区域设计与任务总表')+' · '+wl('当前任务依赖与状态字典')+' · '+wl('当前证据链与结局条件')+' · '+wl('文书与现场文本台本')+' · '+wl('台本新增人物与知识边界')+'。\n\n'
for title,group in [('主线四幕',main),('支线三阶段',side),('日常短台本',daily),('副本环境故事',dungeons)]:
    index+='## '+title+'\n\n| ID | 台本 | 区域 | 入口与制作状态 |\n| --- | --- | --- | --- |\n'
    for q in group:
        req=','.join(q.get('requires',[])) or '见台本条件'
        if q.get('at_least'): req+='；N6/7/8任二'
        if q.get('requires_any'): req+='；'+ '/'.join(q['requires_any'])+'任一'
        index+=f"| {q['id']} | {wl(task_names[q['id']])} | {wl(region_names[q['region']])} | {req}；"+('逻辑小样已部署，新增对白草稿' if q['id']=='N1' else '台本草稿，未实现')+' |\n'
    index+='\n'
index+='## 阅读顺序与历史\n\n先读N1—N5，再任选调查路线读N6/N7/N8，接N9—N18；支线可在对应主线前置后插入。台本中的选项键、场次键和对白键稳定，标题可改。\n\n历史开发见'+wl('剧情重构与旧任务退役')+'，故事总览见'+wl('剧情总纲')+'。\n'
write('00_导航/任务台本总索引.md',preserve_foreign('00_导航/任务台本总索引.md',index))
area=front('新区域设计与任务总表','MAP-SCRIPT-INDEX','index','region')
area+='六个原创区域包共54功能节点。它们是可走关系与场所预算，不是当前安装已经新增54格或六座城市。地图审美与场景用途见各区当前修订节；旧渡口为R02的入门故事点，三个子场景不重复计世界节点。\n\n| 区域 | 设计主题 | 节点 | 主线 | 支线 | 日常 | 副本 |\n| --- | --- | --- | --- | --- | --- | --- |\n'
for r in regions:
    def col(group): return tasklinks([q['id'] for q in group if q['region']==r['id'] or q.get('secondary_region')==r['id']])
    area+=f"| {wl(region_names[r['id']])} | {r['theme']} | {len(r['nodes'])} | {col(main)} | {col(side)} | {col(daily)} | {col(dungeons)} |\n"
area+='\n入口：原作商队→R02旧渡口入门点；N1结案→R01灰堤；N4完成→R02西路；N5公开R03/R04/R05路线；N13后剧情指引上R06。道路可先探索普通区，关键故事段只随任务生成，不能提前删掉后续证人。\n\n'
area+='原世界图坐标尚未核验，R01—R06只表示功能拓扑，不能据它推断原作政治疆界。推荐等级是调试目标：N1入门点6–9，其余R02调查9–15；R01调查6–10、R03 12–20、R04 13–21、R05 16–24、R06 22–28。主线不承诺单独提供全部升级经验。\n\n'
area+='退役D01预算改作工营／听审与工坊组合中的地表叙事空间；R01由2副本改为1副本，不再用旧封账仓硬凑10个有效副本。其余功能预算按本次节点表，全球格数另定。\n\n'+wl('任务台本总索引')+' · '+wl('地图扩张总图')+' · '+wl('旧渡口_场景与通路')+' · '+wl('地点设定核对与冲突修订')+'。\n'
write('02_世界与地图/新区域设计与任务总表.md',preserve_foreign('02_世界与地图/新区域设计与任务总表.md',area))

model['active_story']=[{'id':q['id'],'name':q['name'],'region':q['region'],'requires':q['requires'],'at_least':q.get('at_least'),'stage':('0.3.0 logic deployed; S62 routes and dialogue pending' if q['id']=='N1' else 'S62 screenplay draft only'),'file':paths[q['id']]} for q in main]
model['active_narrative_network']={'file':'research/story-network.json','date':DATE,'routes':sum(len(q['routes']) for q in network['tasks'].values()),'cross_effects':len(network['edges']),'ensemble_arcs':len(network['arcs']),'implemented':False}
model['legacy_graph_status']='Historical MQ01–18 blueprint; new N1–18 screenplay supersedes it; no save migration'
model['screenplays']=[{'id':q['id'],'kind':('main' if q in main else 'side' if q in side else 'daily' if q in daily else 'dungeon'),'region':q['region'],'secondary_region':q.get('secondary_region'),'requires':q.get('requires',[]),'requires_any':q.get('requires_any',[]),'story_requires':q.get('story_requires',[]),'at_least':q.get('at_least'),'file':paths[q['id']],'scenes':len(q['scenes'])} for q in all_tasks]
model['active_evidence_producers']={'NE1':['N4'],'NE2':['N6'],'NE3':['N7'],'NE4':['N8','N13'],'NE5':['N15']}
model['active_region_layouts']=regions
model['active_region_edges']=[['BASE','R01'],['BASE','R02'],['R01','R02'],['R02','R03'],['R02','R04'],['R03','R04'],['R03','R05'],['R04','R05'],['R05','R06']]
model['active_ending_rules']={
    'sealed':{'requires_quest':'N15','containment_ready':True},
    'custody':{'all_evidence':True,'relief_min':2,'accountable':True,'no_exchange_harm':True,'shift_harm_absent_or_remedied':True,'assents_min':2,'trustee_assent':True,'trustee_trust_min':1},
    'distributed':{'all_evidence':True,'relief_min':2,'accountable':True,'no_exchange_harm':True,'shift_harm_absent_or_remedied':True,'archive_pact':True,'transport_pacts_any':['route','ferry']},
    'seized':{'requires_quest':'N15','explicit_choice':True}}
(ROOT/'research/design-model.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
HASH_FILE.write_text(json.dumps(generated_hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'screenplays':len(all_tasks),'scenes':sum(len(q['scenes']) for q in all_tasks),'regional_nodes':sum(len(r['nodes']) for r in regions),'scope':'original drafts only; game files untouched'},ensure_ascii=False))
