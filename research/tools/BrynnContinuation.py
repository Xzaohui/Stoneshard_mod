"""Emit and reconcile the authoritative S85 design supplement; no game writes."""
from pathlib import Path
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[2]
V=ROOT/'design'
MARK='BRYNN-CONTINUATION-S85'
INDEX='布林续篇任务与伏笔回收总表'
LORE='布林背景复核与续篇创作边界'
AUDIT='布林续篇逻辑与人物弧光审查'
ITEMS='布林续篇物件与短文本'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wl(p):return '[['+Path(p).stem+']]'
def front(title,ident,kind,canon='mod-original'):
    return f'''---
title: "{title}"
id: {ident}
type: {kind}
status: draft
canon: {canon}
baseline: "0.9.4.25-modbranch; official lore 2021 separate from current availability"
updated: 2026-10-12
tags: [stoneshard, brynn, S85]
aliases: []
---

# {title}

'''

def replace_block(t,body):
    start=f'<!-- {MARK}:BEGIN -->';end=f'<!-- {MARK}:END -->'
    block=start+'\n'+body.rstrip()+'\n'+end+'\n'
    if start in t:return re.sub(re.escape(start)+'.*?'+re.escape(end),lambda _:block.rstrip(),t,flags=re.S)
    return t.rstrip()+'\n\n'+block

def apply(root=ROOT):
    root=Path(root);v=root/'design';src=root/'research/brynn-continuation.json'
    if not src.exists():return
    m=read(src);base=read(root/'research/city-campaign.json')
    qs={q['id']:q for q in base['quests']};qs.update({q['id']:q for q in m['quests']})
    old=read(root/'research/design-model.json')
    for q in old['active_story']:qs[q['id']]=dict(file=str(Path(q['file']).relative_to('design')))
    newactors={a['id'].removeprefix('BRY-NPC-'):a for a in m['actors']}
    newactors.update({a['id']:a for a in m['actors']})
    for a in base['dramatic_cast'].values():newactors[a['id']]=a
    spaces={s['id'].removeprefix('BRY-X'):s for s in m['spaces']}
    def ql(qid):return wl(qs[qid]['file'])
    def al(key):return '玩家' if key=='玩家' else wl(newactors[key]['file'])
    # Every protected note is checked before any mutation. Updates change only our block.
    manifests={}
    for p in (root/'research').glob('*note-hashes.json'):
        h=read(p)
        if not isinstance(h,dict) or not all(isinstance(x,str) for x in h.values()):continue
        manifests[p]=h
    ours=root/'research/brynn-continuation-note-hashes.json'
    protected={rel:h for hs in manifests.values() for rel,h in hs.items()}
    changed=set();emitted={}
    def verify(p):
        rel=p.relative_to(root).as_posix()
        if p.exists() and rel in protected and sha(p)!=protected[rel]:
            raise RuntimeError('Preserve edited note before regeneration: '+rel)
    # Check complete protected state before writing any output.
    for rel in protected:verify(root/rel)
    def write(rel,text):
        p=v/rel;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text,encoding='utf-8');k=p.relative_to(root).as_posix()
        changed.add(k);emitted[k]=sha(p)
    def attach(rel,body):
        p=v/rel
        if not p.exists():raise RuntimeError('Missing integration endpoint: '+rel)
        t=replace_block(p.read_text(encoding='utf-8-sig'),body)
        p.write_text(t,encoding='utf-8');changed.add(p.relative_to(root).as_posix())

    common='''死亡优先，其次缺席、拒绝与用途授权；最后才检查有限回执和当前目标状态。询问、预览、读纸、关闭均不写resolve。实际行动及交接验毕、费用来源核过，再确认才写唯一resolve。反悔只重评未来，不回滚已发生付款、曝光、伤害与责任。本人缺席不创建第二个身体，未授权代理不替其签字。

本案是一次人物事件，不按日刷新、不做普通运输/修理/清运委托。拒做保原生服务与主线；没有完成全部布林任务的门槛。有限调查费只由本案paid记一次，金额仍待经济核算；受助者的工资/退款不是玩家奖金，接收边不另结奖。N17安全快照独立冻结；本案不发NE或accountable，不为N16买资格。
'''
    for q in m['quests']:
        t=front(Path(q['file']).stem,q['id'],'city-screenplay')
        t+=f"英文工作题：{q['english']}（Mod原创）。地点：[[聚落_BRY_布林]]。入口：[[{INDEX}]]。\n\n"
        t+='## R：方法与提交；X：后续回收\n\n'
        t+='R：'+ ' / '.join(r['key'] for r in q['routes'])+'；实际执行后唯一提交。X：'+ ' · '.join(e['id'] for e in m['effects'] if e['source']==q['id'] or e['target']==q['id'])+'。\n\n'
        t+=f"**原作锚点**：{', '.join(q['source'])}，逐项定位与边界见[[{LORE}]]。新人物、物件、原因、结局均原创，不能倒写成官方已发生剧情。\n\n"
        t+=f"## 入口与反转\n\n{q['hook']}\n\n**转折**：{q['turn']}\n\n前置：无其他新增支线硬前置；未做旧案先用本地固定线索。旧任务进行中不得写其原变量；物件可选，不以全部纸张齐备开主线。\n\n"
        t+='## 场次与条件对白\n\n场号是素材定位，不是自动按顺序播放。先到后场：公开物可看；缺知识改成询问，私密页不显。问过不等于同意行动。返回已看场时，只播放当前知识/处置回应，不再生成箱、款或人物。\n\n'
        for i,s in enumerate(q['scenes'],1):
            t+=f"### 场{i}：{s['title']}\n\n位置：{wl(spaces[s['space']]['file'])}。显示条件：{s['guard']}。\n\n调度：{s['blocking']}\n\n"
            for l in s['lines']:
                t+=f"**{l['id']}｜{al(l['speaker'])}**：「{l['text']}」\n\n条件：{l['guard']}\n\n"
                if l.get('fallback'):t+=f"知识不足且本人在场愿谈时，替代：「{l['fallback']}」；死亡/缺席只留有限记录，不演替代句。\n\n"
            t+='玩家选项：\n\n'+'\n'.join('- '+c for c in s['choices'])+'\n\n'
        t+='## 三种实际行动解法\n\n'
        for r in q['routes']:
            t+=f"### {q['id']}-R-{r['key']}：{r['label']}\n\n行动：{r['action']}\n\n成本与失去：{r['cost']}\n\n结果：{r['result']}\n\n本人回访 {al(r['speaker'])}：「{r['line']}」\n\n显示：resolve={r['key']}、本人存活在场愿谈；每项“实领/实赔/真接收”还须其独立交接事实，不能只凭resolve假造新事实。\n\n可传范围：{r['receipt']}。玩家另选传/不传，用途撤回保已经披露历史。\n\n"
        t+='## 状态、资源与奖励\n\n'+common+'\n'
        t+=f"设计字段：resolve_{q['id'].replace('-','_')}、paid_{q['id'].replace('-','_')}、actual_action、handover、disclosure_scope、sticky_history、receipts。均为未实现设计字段；commit需要实际行动/交接和最后确认，保pending失败点，重复读纸不重结。\n\n"
        t+='## 中断与恢复\n\n'+q['interruption']+'\n\n物件与长短文本：'+q['items']+f' 见[[{ITEMS}]]。\n\n'
        t+='## 伏笔、回收与不同到达顺序\n\n'
        for e in m['effects']:
            if e['source']==q['id'] or e['target']==q['id']:
                t+=f"- `{e['id']}` {ql(e['source'])} → {ql(e['target'])}；逐路线可用范围、早/晚台词与未做出口见[[{INDEX}#{e['id']}]]。\n"
        t+=f'\n[[{AUDIT}]] · [[城市篇章与跨区域任务网]] · [[网状叙事与条件对话规范]]\n'
        write(q['file'],t)

    for a in m['actors']:
        related=[q for q in m['quests'] if any(l['speaker'] in (a['id'],a['id'].removeprefix('BRY-NPC-')) for s in q['scenes'] for l in s['lines']) or any(r['speaker'] in (a['id'],a['id'].removeprefix('BRY-NPC-')) for r in q['routes'])]
        t=front(Path(a['file']).stem,'CITY-NPC-'+a['id'],'character')
        t+=f"所属：[[聚落_BRY_布林]]。原创身份：{a['role']}。不是原作领袖/官方机构的现任代表。\n\n口吻：{a['voice']}\n\n跨任务弧光：{a['arc']}\n\n当前台本："+' · '.join(ql(q['id']) for q in related)+f'。\n\n[[{INDEX}]] · [[{AUDIT}]]\n\n'+common
        write(a['file'],t)
    for s in m['spaces']:
        related=[q for q in m['quests'] if any(x['space']==s['id'].removeprefix('BRY-X') for x in q['scenes'])]
        t=front(Path(s['file']).stem,s['id'],'location')
        t+=f"四区背景接入：{s['quarter']}；拟定叙事接点 {s['anchor']}，不是原生坐标或同名原房间。\n\n空间理念：{s['layout']}\n\n拒入与回程：{s['alternative']}\n\n关联：[[聚落_BRY_布林]] · [[空间_BRY_布林]] · "+' · '.join(ql(q['id']) for q in related)+f' · [[{INDEX}]]。\n\n新增六处独立场景只计相对布局；既有132室内为基线，新增六处不冒称已有138运行房间。概念板仅风貌参考，比例平面/碰撞/资源绑定尚未做；无全访前置。\n'
        write(s['file'],t)

    t=front(INDEX,'NAV-BRYNN-CONTINUATION-S85','navigation')
    t+=f"当前续篇登记：research/brynn-continuation.json。原11篇布林主章/支线保留，追加六篇CS-BRY-11—16；布林共1主章+16支线=17篇。十五城基线73篇与本批6篇分开保存，合计79篇；原314条单方法回执保留，新增15组回收桥含45方法版本，两种计数单位不混加称分支数。基线65篇已有逐角色稿，本批六篇新增为71篇，尚8篇基础场次待同等深化。原51篇晶石任务另外计，不重复发奖。\n\n[[{LORE}]] · [[{AUDIT}]] · [[{ITEMS}]] · [[城市与聚落设计总索引]] · [[聚落_BRY_布林]]\n\n"
    t+='## 第一大城的节奏\n\n初入可先遇侧泊、断扣、外棚三种实物事件；原生服务和原任务优先保留。中段可独立接装帧与支款，两者不会靠前案标记强制揭隐私。听席可早到，只有本次有限议题，不在屏幕上列“清完前五案”检查表。离城后经有限授权回执再回访，每一次未来邀请仍问本人。三势力领袖不替地方案盖全国政策章。\n\n'
    t+='## 原作延续与任务\n\n|任务|原作锚点|新增矛盾与后期回收|\n|---|---|---|\n'
    descriptions={11:'官方夜船悬念旁的一次民间渡船；接N14真实回程与15支款，不解官方夜船谜底。',
                  12:'新会/进口竞争旁的一批改装断扣；接SKO新炉议价与14自查责任，非族群真伪审判。',
                  13:'围城史物旁的战后添页；接N13原物/披露/认证的区别，不代解旧市长死案。',
                  14:'原工具铺危机旁的家属误认和新棚危险；接N14有限料/工位，原任务服务仍按原条件。',
                  15:'招募许诺旁的一袋实际薪款；接PAS分用途核人，雅尼与礼昂非同人。',
                  16:'三势力的承诺旁的逐人新交接；接N16监督与资金的区别、N18不能代替缺席者点头。'}
    for q in m['quests']:t+=f"|{ql(q['id'])}|{', '.join(q['source'])}|{descriptions[int(q['id'][-2:])]}|\n"
    t+='\n## 原十一案的接入\n\n学徒之印（03）影响安菈愿否署名，报纸（04）影响乔彤是否愿承认版面代价；退役旧案（06）与雅尼是不同身体，不转移同班历史；旧帆空席（08）不因一位退役者上岸证明未归水手回来。CM-BRY租屋选择不作为听席前置，蕾娜的删记承认只有原案已核且她愿承认才显示。具体双链已写回旧案。\n\n'
    t+='## 实际伏笔回收\n\n所有边都是设计补充，不是原作变量。每条三路线都有限知情版本；目标未开始可改变将来的问法/资源报价，已结只改变回访未来，N17冻结不重开。未做/保密绝不锁主线。\n\n'
    for e in m['effects']:
        t+=f"### {e['id']}\n\n{ql(e['source'])} → {ql(e['target'])}；发言人：{e['receiver']}。\n\n**前期埋下**：{e['plant']}\n\n**后来重新理解**：{e['reinterpret']} 只以实际完成的某一路线获准回执为准，不是按任务计数给好坏值。\n\n"
        t+='|来源方案|后来能认的事与代价|\n|---|---|\n'
        for r,detail in e['routes'].items():t+=f'|{r}|{detail}|\n'
        t+='\n每路线在共用问候后另接以下条件句，不把所有版本同时播放：\n\n'
        for r,pair in e['route_dialogue'].items():
            t+=f"- `{r}` 早到：「{pair['early']}」；晚到：「{pair['late']}」。只知对应回执，现实资源变化须现场复核；句中说已付/已接只限已有实际交接。\n"
        t+=f"\n实际影响：{e['action']}\n\n早到：「{e['early']}」\n\n晚到：「{e['late']}」\n\n未做/未知/拒传：「{e['missing']}」；保持目标本地独立方法。\n\n这三句只给当前存活/在场/愿谈的指定发言人；死亡或缺席不播放其新句。隐私被撤回则仅能讨论自己已有公开范围，授权不能由高声望代替。{e['knowledge']} {e['timing']} {e['reward']}\n\n"
    write('00_导航/'+INDEX+'.md',t)

    t=front(LORE,'LORE-BRYNN-CONTINUATION-S85','research-note','mixed')
    t+='''实际调查日期：2026-10-12。只读原vanilla.win；当前组合data.win未作为原作证据。2021官方设定稿说明背景/计划，不证明本版领袖可对话；本地文本存在不证明当前存档可达。没有保存官方全文、整页Wiki或游戏完整对白。

## 官方背景，分别限定用途

- **STEAM-BRY-I**：2021-04-05 [Brynn Lore – Part I](https://store.steampowered.com/news/app/625960/view/2998808931065913303)。通过官方Steam GetNewsForApp API读完整正文（页面抓取只返回图片）；正文长度/哈希/文章gid另存research/brynn-official-lore-source-fingerprints.json。自由城市传统、战后难民、围城与停战提供社会背景；白银商帮、前锋、新会的利益并不一致。可设计个体落差，不宣称当前已经完成全国政体变革。
- **STEAM-BRY-II**：2021-05-23 [Brynn Lore: Part II – Leaders](https://store.steampowered.com/news/app/625960/view/3034842167056230351)。同一官方API全文读取。登瓦尔的工匠支持与进口敌意、耶昂的商贸关系、迪·贝罗的军事声望是动机锚点。旧市长死亡的责任未定，夜船货物/用途也未揭晓；六案不代作者盖谜底，人物对他人动机的猜测不能改写成事实。

## 社区地理与任务核对

- **WIKI-BRY-MAP**：[Brynn](https://stoneshard.com/wiki/Brynn)，2026-10-12读取，页面编辑记录2026-04-29；社区整理。四区是西北铸币广场、东北老塔、西南工会区、东南码头。这里只用于区位接入；钱庄、大学、会馆在列表里，不证明室内可进入。新增场景均在原创外台/副坊，不擅开这些原生建筑。
- **WIKI-BRY-BOAR**：[布林狩猎奇闻](https://www.stoneshardwiki.com/zh/quests/brynn-boar-hunt/)，2026-10-12完整读取正文，页面标0.9.4.25；非官方。工具铺地窖事件有独立启动/计时/战斗/回报/服务阶段；本批14只接外棚事件，不重置原任务，不借完成新案发原赠礼或跨过原商店条件。本文不把社区读取当游戏实测。

## 本地逐项定位

research/brynn-local-lore-locators.json记录输入SHA、64个同键命中元数据（含名称/描述/正文/非对白定义，不等于64段剧情）。下表仅用明确读过的STRG行；字段2英文/3中文，索引和偏移可复查。同键别行不可混称同一段。表内摘要不是保存全文。

|定位键／STRG索引|包内证据或说话者立场|设计边界|
|---|---|---|
|LOCAL-NewGuild / 15280|中文名新会|非“新公会”新造势力|
|LOCAL-AzureHouse / 15289|碧罗商馆，英文Trading House of the Azure Thread|玛莉丝为独立匠商，不冒任原商馆负责人|
|LOCAL-SilverLeague / 15292|中文名白银商帮|不以新译名另设第二商帮|
|LOCAL-magistrateCapital / 15453|文本称前锋维护布林与郊区，不提供独立佣兵契约|文本承诺不证明每个角落安全；本案支款席为民间限权|
|LOCAL-lorebook_nistra / 16503|描述小科雷昂死于围城，遗稿流传|不复活；新增残本原页归属unknown，后添页全原创|
|LOCAL-siegecamp_letter / 16514|物件描述围城信与王廷蜡封|不凭一封信确定全部阵营责任|
|LOCAL-treatise_geo1 / 16590|百年前大学语言研究笔记的描述|不把它当今日教师在场/晶石认证|
|LOCAL-order_toolshop / 16716|处分令自称依法处置，并叙卫兵死亡|制度文本，不代办新审判；英文placed on trial，中文提审定罪较强，司法阶段有译差；达兰弟弟不被认作公告死者|
|LOCAL-leaflet_limerick / 16718|嘲讽三领袖的诗歌|讽刺观点，不确认阴谋；迪·贝罗爵位英中译差留待核|
|LOCAL-leaflet_brynn02 / 16719|白银商帮的精灵保护公告|机构宣示，不保证所有本地人无排挤|
|LOCAL-leaflet_brynn01 / 16720|前锋征募许诺公平付薪，并指博恩在老塔|许诺不是实际薪款；中文博恩，不另造贝恩同职位|
|LOCAL-leaflet_brynn00 / 16721|欢迎告示将工匠/商人/从军者指到不同区|宣传屋檐不等于每户已接住房|
|LOCAL-bern_letter / 16743|博恩军需信限定介绍/支持|不发全国任命、免责或新重复信件|
|LOCAL-emissarletter / 16749|特使里柯特·德·欧佛拜恩抱怨村中待遇并索曼郡酒，自称知维博与耶昂不和|特使的偏见/自称，不确认所有农人粗鄙；不据此开重复送酒任务|

## 连续性与未核验

每案原创内容明确：夜泊为另一只民间租船，断扣为本批拆装/扩孔，残本为未知原页+战后添页，外棚为新危险而非第二食尸鬼，支款为一班民间经手，听席为本批交接。各领导原谜、原作地窖、原角色权限、当前存档任务阶段保留；原版逐NPC全量双语核对尚属后续计划，不能由这批背景研究冒称完成。

'''
    t+=f'[[{INDEX}]] · [[{AUDIT}]] · [[来源登记]] · [[城市设计与原作避让审查]]\n'
    write('01_原作基线/'+LORE+'.md',t)

    t=front(ITEMS,'DOC-BRYNN-CONTINUATION-S85','story-documents')
    t+='这些是Mod原创可选物件的正文草稿，不是游戏现有物品。只装准许内容，不把长资料塞进对白或做六份纸齐收门槛。物件在原柜复核/现场见证可替代；副件授权和原件去向分别记账。\n\n'
    texts={11:('侧泊运价摘记','这一趟的载重和回岸记号已核。姓名与病史没有记在这面。费用按本趟分栏；白日另租不抹夜渡原欠。'),
           12:('断扣试验图','孔边是装配时扩开的；扣件亦曾拆装。试过才填写低载结果；买断可只记批次去向，未试的载荷留空。任何结果不保所有来货。'),
           13:('装帧方法短图','纸纹不同，订线先后也不同。后添页可以被检，原页作者仍待核。姓名背页须本人允许再看。'),
           14:('外棚试走记号','这座外棚的省撑痕留着。补撑且试走后才填核验范围；封棚/分户迁位另填实际去向，不称已补撑。原工具铺地窖与未归者不是此记号的结论。'),
           15:('本班领取短单','本人已领数、原余欠和过桥偿付各列一栏，不能同笔再领。领取不含重新受雇，公开金额另问本人。'),
           16:('分项交接短单','到场、授权、实收各记。空椅未签；出席不是永久续约。赞助只在本批范围，监督另查。')}
    for q in m['quests']:
        num=int(q['id'][-2:]);name,body=texts[num]
        t+=f"## BC85-DOC-{num}：{name}\n\n所属：{ql(q['id'])}。\n\n可选正文：「{body}」\n\n"
        t+='生成条件：实际处置/观察范围已有记录，物主准许副件；这里只给文字模板，未做到的字段不填写、不将其他路线费用自动打勾。拿到短单不触发解锁/领奖。寄存/交售的原件离开背包，未授权私页不复制。\n\n'
    t+=f'[[{INDEX}]] · [[{AUDIT}]]\n'
    write('06_支线/城市支线/'+ITEMS+'.md',t)

    t=front(AUDIT,'AUDIT-BRYNN-CONTINUATION-S85','design-review')
    t+='本轮六篇仍为逐角色设计草稿；检查为文档/状态参考模型，不能证明文学质量、数值平衡或游戏运行。\n\n'
    t+='## 人物跨案弧光\n\n|人物|开始/掩饰|实际选择后的变化|后期压力与不能抹去的事|\n|---|---|---|---|\n'
    for a in m['actors']:t+=f"|{wl(a['file'])}|{a['role']}；{a['voice']}|{a['arc']}|拒绝、伤害、曝光、债与分责按实际留史；后续单问，不把帮助买作立场。|\n"
    t+='\n## 纸面反例审查\n\n- 雅尼不与原维松、礼昂、雷奥莫伦合并；此轮七新角色共享自身ID，场次归本人，不强制同场。\n- 达兰弟弟未归不认定原工具铺死者；原食尸鬼不再刷第二只作续作。\n- 瑟拉夜渡只是一次民船；不宣称迪·贝罗官方神秘夜船均装支具。\n- 玛莉丝不是碧罗商馆首领，不为全族保证质量；ロ安的羞辱与实际扩孔可同时有责。\n- 艾伦不授晶石认证；名人残页存疑，不解官方旧市长被害悬案。\n- 支款实领不等于军役重签；米罗的担保/赞助与监察资格不同。\n- 听席可独立进入；六案不是主线清单；每次授权逐用途，空椅不计同意。\n- 船、余料、柜位、工位、款袋不通过三条方法同时发；实际钱到手才paid，回访不再奖。\n- 原S76蕾娜删记承认与玛莉丝实赔等句必须有各自来源，未做旧案显示询问而不强认。\n\n'
    t+='## 所有权与收尾\n\n原73篇/314单方法回执保留为基线；本批6篇/15组桥（45方法版本）为登记扩展，合计79篇。桥组与单方法回执计数单位不同，分别列。既有65逐角色稿+6新稿=71篇，原8篇仍待深化。原51篇晶石任务另计；数字经济、时间轴、比例地图与游戏对话树继续待制作。design根与项目根AGENTS分别登记；后续NPC计划仍排在城市与全局收尾后。\n\n'
    t+=f'验收入口：research/tools/Validate-BrynnContinuation.py，并运行原三项及城市/空间检查。实际结果以research/brynn-continuation-validation.json为准，不提前标通过。\n\n[[{INDEX}]] · [[{LORE}]] · [[{ITEMS}]] · [[特殊地点与野外NPC对白扩展计划]]\n'
    write('11_管理/'+AUDIT+'.md',t.replace('ロ安','罗安'))

    # Add all conditional bridges to both endpoints, with full target-visible detail.
    endpoints={}
    for e in m['effects']:
        if e['target'] in [q['id'] for q in m['quests']]:continue  # New notes already carry their X links.
        endpoints.setdefault(qs[e['target']]['file'],[]).append(e)
    for rel,edges in endpoints.items():
        body=f'## S85布林续篇条件回收\n\n[[{INDEX}]]为现行补充，未实现。原任务资格/方法/奖励/冻结保留；回执只改未来问法/报价，不做硬前置。\n\n'
        for e in edges:
            body+=f"### {e['id']} 本地接收\n\n来源：{ql(e['source'])}，发言人{e['receiver']}；本人存活/在场/愿谈、实际来源已结、获准有限回执且原目标前置满足才可用。{e['action']}\n\n"
            for key,text in e['routes'].items():body+=f'- 来源 `{key}`：{text}\n'
            body+='\n实际方法另接具体条件台词：\n\n'
            for key,pair in e['route_dialogue'].items():
                body+=f"- `{key}` 早到：「{pair['early']}」；晚到：「{pair['late']}」。本次仅播放实际来源这一版本；当前资源和交接未核不说已经领取/接收。\n"
            body+=f"\n早到：「{e['early']}」\n\n晚到：「{e['late']}」\n\n未做/未授权：「{e['missing']}」\n\n{e['timing']} {e['reward']}\n\n"
        attach(rel,body)
    # Explicit old Brynn anchors, with finite actor knowledge and timing rules.
    anchors={
     'CM-BRY':'[[台本_CS-BRY-16_空椅不是赞成]]接蕾娜已实际承认的删记；未知旧案不演认错句。CM租屋方法不变，后听席未做也可进；新邀请不是旧租约重签。',
     'CS-BRY-03':'[[台本_CS-BRY-12_两种火候]]可问安菈愿否署本批检测名；旧案获得署名不买永久合作，离坊/拒参只用固定试块与中立单班，不克隆她。',
     'CS-BRY-04':'[[台本_CS-BRY-13_页边的另一个名字]]让同一乔彤另问方法页/私页/展期，过去已刊泄露仍在；未知版面选择不自动授公开许可。',
     'CS-BRY-06':'[[台本_CS-BRY-15_招募告示的背面]]的雅尼是另一位原创退役者；薇特、维松旧同班结果不转给他。愿传去名追索方法可先问，未传保本地支款入口。',
     'CS-BRY-08':'[[台本_CS-BRY-11_不写船名的夜泊]]不证明未归水手归来；旧帆席位仍按奥德/米蕾的旧实际方法占用，另一民船不得免费占那个席位。',
     'CS-BRY-10':'[[台本_CS-BRY-16_空椅不是赞成]]只处理新交接，不是重开夜会旧选择。旧赞助控制史保留；后来有钱不删强制历史，未准新议题不出具政治支持。'}
    for qid,b in anchors.items():attach(qs[qid]['file'],'## S85续篇接入\n\n'+b+f'\n\n[[{INDEX}]] · [[{LORE}]]')
    shared_actor_ids={'BRY-NPC-RENA','BRY-NPC-MIRO','BRY-NPC-JOTIN','BRY-NPC-ANLA'}
    for a in base['dramatic_cast'].values():
        if a['id'] in shared_actor_ids:
            attach(a['file'],f'## S85同一人物的续篇\n\n[[{INDEX}]]新增事件复用本人的ID/身体；每案对款、署名、私页、来席逐项再问。原弧光/伤害史保留，未做原案不演旧承认。[[{AUDIT}]]。')
    core_links=f'## S85布林新增六案（当前登记）\n\n[[{INDEX}]] · [[{LORE}]] · [[{AUDIT}]]。布林追加6支线，原1主章+10支线保留，现共17篇；城市总计基线73+扩展6=79篇；原314单方法回执与新增15组回收桥/45方法版本分别计；71篇逐角色草稿，8篇待深化。原51篇晶石任务另计。原作神秘夜船/旧市长案不揭底，六案独立入口，不是N16/主线前置；本轮不部署。\n'
    for name in ['城市与聚落设计总索引','任务台本总索引','新区域设计与任务总表','城市篇章与跨区域任务网','城市扩展验收记录','设计总览','当前任务依赖与状态字典','当前证据链与结局条件','叙事交叉影响矩阵','来源登记','城市设计与原作避让审查','人物弧光与关系转折']:
        p=next(v.rglob(name+'.md'));attach(p.relative_to(v).as_posix(),core_links)
    attach('02_世界与地图/城市与聚落/聚落_BRY_布林.md',core_links+'\n新任务：'+' · '.join(ql(q['id']) for q in m['quests'])+'\n')
    attach('02_世界与地图/任务空间/空间_BRY_布林.md',core_links+'\n六处拟定场景：'+' · '.join(wl(s['file']) for s in m['spaces'])+'\n\n分四原区及中立院外接入，主视图原132室内不重编号；新六场景尚无比例图。')
    # The main model carries a registry pointer rather than silently dropping supplements.
    base['continuation_registries']=[dict(id='BRYNN-S85',file='brynn-continuation.json',quests=6,effects=15,status='draft')]
    (root/'research/city-campaign.json').write_text(json.dumps(base,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rule=f'\n<!-- {MARK}:BEGIN -->\n2026-10-12 S85：用户追加布林续篇；research/brynn-continuation.json登记六案、18场/18方法、七原创人物、六场景、15组有限条件桥/45方法版本。入口design/00_导航/{INDEX}.md，原作复核另卡；原73篇/314单方法回执基线不删除，合计79篇、71逐角色草稿/8待深化；桥组与旧单方法回执分别计。官方2021正文经Steam API读，本地64命中只存定位/哈希/摘要，不存全文。夜船/旧市长谜底、原商店/地窖/领袖权限保留，礼昂与雅尼分人；空椅不作同意，N17不改/NE不加/奖去重。本轮不部署；Validate-BrynnContinuation.py＋原三项设计检查，数字/比例/游戏尚未验收。\n<!-- {MARK}:END -->\n'
    for p in [root/'AGENTS.md',v/'AGENTS.md',root/'README.md']:
        body=rule.split(f'<!-- {MARK}:BEGIN -->\n',1)[1].split(f'\n<!-- {MARK}:END -->')[0]
        p.write_text(replace_block(p.read_text(encoding='utf-8-sig'),body),encoding='utf-8')
    for p,hs in manifests.items():
        if p==ours:continue
        for rel in changed & hs.keys():hs[rel]=sha(root/rel)
        p.write_text(json.dumps(hs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    ours.write_text(json.dumps(emitted,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (root/'research/brynn-continuation-integration.json').write_text(json.dumps(dict(
        date='2026-10-12',source_sha256=sha(src),baseline_tasks=73,added_tasks=6,combined_tasks=79,
        baseline_single_method_receipts=314,added_bridge_groups=15,added_method_variants=45,generated=emitted,
        updated_existing={p:sha(root/p) for p in sorted(changed-emitted.keys())},
        changes='Existing endpoint bodies preserved; own S85 blocks reconciled; native game untouched.'),
        ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(generated=len(emitted),integrated_existing=len(changed-emitted.keys()),quests=6,effects=15),ensure_ascii=False))

if __name__=='__main__':apply()
