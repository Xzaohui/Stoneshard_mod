"""Save two original concept boards, scene mappings and provenance. Never writes game files."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil,re,sys
from TaskArtLinks import add_task_art
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def wl(p):return '[['+Path(p).stem+']]'
model=load('research/city-campaign.json');quests={q['id']:q for q in model['quests']};cities={c['id']:c for c in model['cities']}
specs=[
 dict(id='SKO',name='斯孔弗特',slug='skonfert',version=1,source=sys.argv[1],
 theme='炉火维持生计，赎款牵住等待；回来的人也有拒绝替别人偿还期望的权利。',
 review='已查看生成图：A—F完整，寄柜、归乡棚、料廊、炭份台、冷沟和暖手屋各有不同构图。E的人物位于干侧观察区，未出现饮水或浸泡；F的火势偏旺，制作需改为合适暖火。柜格、钱筹、炭与旧坯均不可按图计量。',
 panels=[
 ('A','SKO-D02-A','双承诺兑筹柜',['CM-SKO','CS-SKO-01'],'款已兑与人已到是两件事；已做工钱不能被家属赎约挤掉。','三种筹袋与兑筹逐项核，普通返街不锁。缺席者不因玩家付款而出现。'),
 ('B','SKO-S02-3','归人留包棚',['CM-SKO','CS-SKO-02'],'父亲想把归来讲成荣誉，归来者想先过自己的日子。','博赫与雷哈是本案父子；博赫不是妮莎仍未归的弟弟。包由本人保管，拒公开仍保生活出口。'),
 ('C','SKO-D04-A','旧坯定量料廊',['CM-SKO'],'卖出有限非必需旧坯能够偿部分旧欠，也会减少下一批可卖料。','普通修理材料先留；采购款按实际支付记，同一份钱或坯不能向两城重复许诺。'),
 ('D','SKO-S01-3','预付炭份台',['CS-SKO-01','CS-SKO-03'],'工钱、炉料预款与维护款各有用途，封开一袋不代表全部问题解决。','只核已授权份额；运输与维修由普通工班实际做，不追加玩家搬炭循环。'),
 ('E','SKO-D03-A','冷沟取样台',['CS-SKO-03'],'仍戴护符的工人可以要求安全用水；信仰不是拒绝护理的理由。','仅安全观察固定渣槽与旧样；处置由维护者执行，不再接触可疑水取证，不从水色判全因。'),
 ('F','SKO-D01-B','停班暖手屋',['CS-SKO-02'],'接普通工作不等于同意公开战伤、受勋或再出征。','保暖、休息和普通接续独立于宣传；炉火与两条退路需另核像素、遮挡和碰撞。')]),
 dict(id='YOS',name='约斯特文',slug='yostwayne',version=2,source=sys.argv[2],
 theme='家纹是积累也是控制；留冬羊毛、真实欠款与下一份工作的署名必须分别协商。',
 review='已查看v1与v2：六面板、羊毛织染和两条排水路径可区分；v2在B补出本人可取的行李，A两组样布的间隔更明显。沿用其余构图。上游／工段的水力隔离、正门通达、样布归属标记与库存尺寸仍须生产图核验。',
 panels=[
 ('A','YOS-D01-A','家纹对色廊',['CM-YOS'],'家族真的积累过声誉，染工也真的做出自己的颜色；二者不能相互吞掉。','两组样布分别准用，旧家纹留在旧品；画中的纹样不是最终商标或本案授权凭据。'),
 ('B','YOS-D02-B','离坊收包间',['CS-YOS-02'],'老师教过技术不因此拥有徒弟去留；实际未做预款仍可另谈。','先保普通出入、返本人行李和路费，再谈自愿延期；开门不等于欠款清零或已抵远城。'),
 ('C','YOS-S01-3','代工与排管台',['CS-YOS-02','CS-YOS-03'],'夜班亲历可以说明交班和本段管序，不能把所有迁来工人都当嫌疑人。','普通排管与换水由实际工班做；口供只限亲历，管道图还需独立平面，不安排搬十桶任务。'),
 ('D','YOS-S02-3','留冬称捆台',['CS-YOS-01'],'大订单有利润，早许给家庭的冬料也是真承诺；替代衣物可以被拒绝。','保留本户授权底量，替代须真有货且合用；不索病史或感谢，不把画中羊群变无限奖励。'),
 ('E','YOS-D03-A','分流洗毛台',['CS-YOS-03'],'下游受过影响不代表其排斥所有迁来者就正确；本段责任需查具体开管。','固定管序与安全旧样可比；停管或分流要实际执行。水色不能证明全因，也不需安排全员道歉。'),
 ('F','YOS-D04-B','师徒分署台',['CM-YOS'],'共署与独立都是可谈方案，真实旧欠不能变永久身契。','采购人莉葵与SKO属同一身份及有限资产账；只知自己的实占款和交付，不自动知别人的病史或私事。')])]
records=[]
for s in specs:
    cid=s['id'];dest=V/f"12_美术参考/城市概念/{cid}-任务场所-v{s['version']}.png";src=Path(s['source']).resolve()
    if dest.exists():
        if sha(dest)!=sha(src):raise SystemExit('Refusing candidate overwrite: '+str(dest))
    else:shutil.copy2(src,dest)
    c=cities[cid];note=f"design/12_美术参考/{s['name']}任务场所概念与台本映射.md"
    refs=[f"design/12_美术参考/城市概念/{cid}-概念-v1.png",'stoneshard-assets-sample/atlas-099.png','stoneshard-assets-sample/atlas-020.png']
    prompts=[f"research/{s['slug']}-task-art-prompt-20261012.txt"]
    if cid=='YOS':prompts.append('research/yostwayne-task-art-edit-20261012.txt')
    links=['design/'+c['file']]+['design/'+x['file'] for x in c['satellites']]+['design/'+q['file'] for q in model['quests'] if q['city']==cid]+[f"design/02_世界与地图/任务空间/空间_{cid}_{s['name']}.md"]
    rec=dict(id=cid,name=s['name'],selected=dest.relative_to(ROOT).as_posix(),sha256=sha(dest),dimensions=list(Image.open(dest).size),source_path=str(src),note=note,linked_notes=links,
        references=[dict(path=p,sha256=sha(ROOT/p),role='style and material reference only') for p in refs],prompts=[dict(path=p,sha256=sha(ROOT/p)) for p in prompts],panels=[dict(label=a,space=n,name=place,quests=qs) for a,n,place,qs,_,_ in s['panels']],review=s['review'])
    if cid=='YOS':
        prior=V/'12_美术参考/城市概念/YOS-任务场所-v1.png';rec['previous']=dict(path=prior.relative_to(ROOT).as_posix(),sha256=sha(prior));rec['actual_edit_reference']=rec['previous'].copy()
    else:rec['actual_generation_references']=refs
    rec['generation_baseline']=dict(city_model_sha256=sha(ROOT/'research/city-campaign.json'),dialogue_draft_source=f"research/{s['slug']}-drama.json",dialogue_draft_sha256=sha(ROOT/f"research/{s['slug']}-drama.json"))
    records.append(rec)
    text=f'''---
title: "{s['name']}任务场所概念与台本映射"
id: ART-{cid}-TASK-20261012
type: art-reference
status: draft
canon: mod-original
baseline: "0.9.4.25-modbranch"
updated: 2026-10-12
tags: [stoneshard, art, task-spaces, {cid}]
aliases: []
---

# {s['name']}任务场所概念与台本映射

所属 {wl(c['file'])}，空间依据 [[空间_{cid}_{s['name']}]]，总览见 [[原素材参考与城市概念图]]。主题：{s['theme']}

![{s['name']}六处任务场所](城市概念/{dest.name})

> [!info] 原创构图与当前稿
> 参考已查看的本城总览、用户atlas-099普通工坊与室内、atlas-020石木建筑；原图集只读，未复制入库。A—F是画板位置，不是相邻关系或任务顺序。正文任务仍按各台本生效；对应逐角色稿以现行台本为准，图片不能把它标成已完成、已批准或已实现。

## 场所、任务与交互

|面板|稳定空间ID／地点|关联任务|矛盾与人物弧线|交互边界与制作要求|
|---|---|---|---|---|
'''
    for a,n,place,qs,dilemma,boundary in s['panels']:
        text+=f"|{a}|`{n}` {place}|"+' · '.join(wl(quests[q]['file']) for q in qs)+f"|{dilemma}|{boundary}|\n"
    text+='''
## 多解与网状后果

这些场所只支持各台本已有解法，不要求把六处全部游历才收束主章。观察、对话、模型预览不结案；实际支付、交还、授权、工作或专业处置发生后，才按本案规则再次确认。回执只传许可范围内的结果，死亡、缺席与拒绝优先。晚到结果只改变未来能做的事，不倒改已付钱、旧伤害、奖励或N17快照。

跨城采购人的钱、旧坯、衣料与在途占用必须同账去重；采购合同不复制人物到两城同时出场。图中小人物仅供比例与站位，不对应最终脸像；本轮没有建立新交易接口或存档变量。

## 生成、选稿与检查

'''+s['review']+f"\n\n内置image_gen生成；原始／编辑完整提示词分别见"+'、'.join('`'+p+'`' for p in prompts)+"。原参考、输入／输出SHA256、候选版本、台本定位及尺寸记录在`research/city-task-art-20261012.json`。旧总览及YOS v1均保留。\n\n制作仍需拆图层、核格尺寸、原点、门与回程、遮挡及安全操作距离；托盘标识、样布归属和库存上限不能从成图推定。尚无独立碰撞地图、最终精灵或游戏运行验收。\n\n[[任务空间与地点关联审查]] · [[城市美术与图片目录]] · [[城市与聚落设计总索引]]\n"
    if (V/'11_管理/斯孔弗特与约斯特文人物演出审查.md').exists():text+='\n逐角色台本、同一采购人和前后次序见[[斯孔弗特与约斯特文人物演出审查]]。\n'
    (ROOT/note).write_text(text,encoding='utf-8')
manifest=dict(date='2026-10-12',status='draft',canon='mod-original',tool='built-in image_gen',boards=records,runtimeVerified=False,scope='two companion task-location boards, twelve panels; no game or player data changes')
(ROOT/'research/city-task-art-20261012.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
changed=[]
hash_files=['research/city-generated-note-hashes.json','research/city-space-note-hashes.json']
hashes={p:load(p) for p in hash_files}
for rec in records:
    for rel in rec['linked_notes']:
        p=ROOT/rel;old=p.read_text(encoding='utf-8-sig')
        for h in hashes.values():
            if rel in h and sha(p)!=h[rel]:raise SystemExit('Untracked edit: '+rel)
        new=add_task_art(ROOT,rel.removeprefix('design/'),old)
        if new!=old:p.write_text(new,encoding='utf-8');changed.append(rel)
        for h in hashes.values():
            if rel in h:h[rel]=sha(p)
for p,h in hashes.items():(ROOT/p).write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rule='\n<!-- CITY-TASK-ART-20261012:BEGIN -->\n2026-10-12：斯孔弗特／约斯特文各新增六面板任务场所概念，入口design/12_美术参考/原素材参考与城市概念图.md，逐项映射与原参考／提示词／候选SHA见research/city-task-art-20261012.json。保留原总览、YOS v1；人物、库存、排水、门与格尺寸须再制作核验。图只为原创草稿，不改变原回执、任务完成状态或游戏包。TaskArtLinks.py维持任务／聚落／空间双链；修改后跑原三项设计检查及图片来源检查。\n<!-- CITY-TASK-ART-20261012:END -->\n'
for p in [ROOT/'AGENTS.md',V/'AGENTS.md']:
    t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-TASK-ART-20261012:BEGIN -->.*?<!-- CITY-TASK-ART-20261012:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
print(json.dumps(dict(boards=2,panels=12,linked_notes=sum(len(r['linked_notes']) for r in records),changed_notes=len(changed),runtimeVerified=False),ensure_ascii=False))
