"""S176: text injection and localization conventions (read-only extraction).

Reads the implemented C#/GML to document how dialogue and document text reach
the game, the language slot order, and how much of our content would use it.
Planning only: no code change.
"""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'TEXT-INJECT-S176'
CARD = '11_管理/文本注入与本地化口径.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
dlg = (ROOT / 'src/EmbersAndOaths/NativeDialogue.cs').read_text(encoding='utf-8')
docs = (ROOT / 'src/EmbersAndOaths/NativeDocuments.cs').read_text(encoding='utf-8')
step = (ROOT / 'src/EmbersAndOaths/Codes/controller_step.gml').read_text(encoding='utf-8')
def line_of(text, needle):
    for i, l in enumerate(text.splitlines(), 1):
        if needle in l:
            return dict(line=i, code=l.strip()[:120])
    return None
# language slot: index 1 when global.language == 3
lang = line_of(dlg, 'global.language == 3')
# sample pair: first ASCII (EN), second CJK (CN)
lines_block = dlg.split('var lines = new Dictionary<string, string[]>', 1)[1] if 'var lines = new Dictionary<string, string[]>' in dlg else dlg
pair = re.search(r'\["EAO_intro"\] = new\[\] \{ "([^"]+)", "([^"]+)" \}', lines_block)
sample = dict(en=pair.group(1)[:40], cn=pair.group(2)[:24]) if pair else {}
counts = dict(
    dialogue_lines=len(re.findall(r'^\s*\["[^"]+"\] = new\[\] \{ "[^"]+", "[^"]+" \},', lines_block, re.M)),
    flow_keys=sorted(set(re.findall(r'\["(\w+)"\] = new\[\]', dlg)))[:6],
)
# how much of our content needs injection
def count_json(path, key):
    d = json.loads((R / path).read_text(encoding='utf-8'))
    v = d.get(key)
    return len(v) if isinstance(v, list) else (len(v) if isinstance(v, dict) else 0)
cov = json.loads((R / 'bilingual-coverage.json').read_text(encoding='utf-8'))
facts = dict(
    date='2026-10-13',
    scope='S176 text injection and localization conventions extracted from the implemented sample; planning only, nothing wired',
    evidence=dict(
        flow_injection=line_of(dlg, 'variable_struct_set(global.__dialogue_flow_data'),
        line_injection=line_of(dlg, 'ds_map_set(global.npc_lines_map'),
        language_slot=lang,
        struct_guard=line_of(step, '__dialogue_flow_data'),
        quote_helper=line_of(docs, 'internal static string Quote'),
    ),
    conventions=dict(
        slots='对白与文书文本以**双语数组**提供：索引 0＝EN，索引 1＝CN；`global.language == 3` 取 CN。',
        flow='`__dialogue_flow_data` 挂 `RootFragment` 结构；`Fragments` 节点指向下一节点、行键或 `@dialogue_end`；`Speakers`／`Specs`（hub/technical/action）／`Scripts`（回调名）随流注册。',
        lines='`npc_lines_map` 逐行挂 `key` 与 `line_text`；文本经 `json_parse` 注入，**不改 STRG、不依赖外部文件**。',
        documents='文书类由 `NativeDocuments` 提供 ReadCheck／CarryCheck／GiveCode／Quote 等原语，阅读与携带状态走原生物品机制。',
    ),
    sample=sample, sample_line_count=counts['dialogue_lines'], flow_key_sample=counts['flow_keys'],
    our_content=dict(dialogue_lines=2717, documents=count_json('field-docs.json', 'docs'),
                     signs=count_json('field-signs.json', 'signs'), field_npc_lines=504,
                     gossip_lines=count_json('ambient-gossip.json', 'lines') + count_json('town-gossip.json', 'lines') + count_json('band-gossip.json', 'lines'),
                     bilingual_pairs=cov['user_pairs']),
)
(R / 'text-injection.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "文本注入与本地化口径"\nid: MGMT-TEXT-INJECT-S176\ntype: guide\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S176, guide, localization]\naliases: []\n---\n\n'
     '# 文本注入与本地化口径\n\n'
     '从已实现小样中提取**文本如何进游戏**的口径（只读），供实现轮沿用同一机制。数据 `research/text-injection.json`。\n\n'
     '## 机制（含证据行）\n\n| 环节 | 做法 | 证据 |\n| --- | --- | --- |\n'
     f"| 对话流注册 | `variable_struct_set(global.__dialogue_flow_data, …)` | `NativeDialogue.cs:{facts['evidence']['flow_injection']['line']}` |\n"
     f"| 逐行文本注册 | `ds_map_set(global.npc_lines_map, _key, _row)` | `NativeDialogue.cs:{facts['evidence']['line_injection']['line']}` |\n"
     f"| 语言槽选择 | `line_text = array_get(_texts, global.language == 3 ? 1 : 0)` | `NativeDialogue.cs:{facts['evidence']['language_slot']['line']}` |\n"
     f"| 运行前置 | 控制器在 `__dialogue_flow_data` 为结构体时才接管 | `controller_step.gml:{facts['evidence']['struct_guard']['line']}` |\n"
     f"| 文书原语 | `ReadCheck`／`CarryCheck`／`GiveCode`／`Quote` | `NativeDocuments.cs:{facts['evidence']['quote_helper']['line']}` |\n\n" 
     f"## 口径\n\n"
     f"- **双语槽序**：数组索引 0＝EN、1＝CN（小样示例：`{facts['sample'].get('en', '')}…` / `{facts['sample'].get('cn', '')}…`）；`global.language == 3` 时取 CN。\n"
     '- **流结构**：`RootFragment` → `Fragments`（节点指向下一节点、行键或 `@dialogue_end`）；`Speakers` 声明发言人；`Specs` 标 hub／technical／action；`Scripts` 绑定 GML 回调名。\n'
     '- **注入方式**：文本以 `json_parse` 内嵌进生成代码——**不改 STRG、不依赖外部文件路径**；与"不复制商业资源"的口径一致。\n'
     '- **文书**：阅读与携带走原生物品机制（ReadCheck／CarryCheck／GiveCode），不另造一套阅读状态。\n\n'
     '## 本Mod内容将走同一机制\n\n'
     '| 内容 | 数量 | 文本来源 |\n| --- | ---: | --- |\n'
     f"| 台本对白行 | {facts['our_content']['dialogue_lines']:,} | `research/story-*.json`、各城 drama／feedback、续篇登记 |\n"
     f"| 野外人物对白 | {facts['our_content']['field_npc_lines']} | `research/field-npc-dialogue.json`（中英成对） |\n"
     f"| 野外文书 | {facts['our_content']['documents']} | `research/field-docs.json`（中英成对） |\n"
     f"| 野外迹象 | {facts['our_content']['signs']} | `research/field-signs.json`（中英成对） |\n"
     f"| 闲谈三池 | {facts['our_content']['gossip_lines']} | `ambient／town／band-gossip.json`（中英成对） |\n"
     f"| 用户可见中英成对 | {facts['our_content']['bilingual_pairs']:,} | [[中英对照覆盖报告]] |\n\n"
     '## 边界\n\n'
     '- 只读提取：**未接线、未构建、未部署**；小样行数与结构只作口径参考。\n'
     '- 语言槽序按小样实测代码判定；若引擎 `global.language` 取值有变，须先核对再批量注入。\n'
     '- 文本字数、界面排版与字体渲染仍待实机（见 [[待办与已知缺口登记]]）。\n\n'
     '[[触发器接线点映射]] · [[事件桩映射总表]] · [[中英对照覆盖报告]] · [[试点批次总表]] · [[实现交接总表]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + "\n## S176文本注入与本地化口径（当前登记）\n\n[[文本注入与本地化口径]]：从 `NativeDialogue.cs`／`NativeDocuments.cs` 提取——双语数组 **索引 0＝EN、1＝CN**（`global.language == 3` 取 CN）、`__dialogue_flow_data`＋`npc_lines_map` 以 `json_parse` 注入、文书走原生物品原语；不改 STRG、不依赖外部文件。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'text-inject-note-hashes.json'
own.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for hp in sorted(R.glob('*note-hashes.json')):
    if hp == own: continue
    try: h = json.loads(hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    touched = False
    for rel in list(h):
        if rel in changed and h[rel] != generated[rel]: h[rel] = generated[rel]; touched = True
    if touched: hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
rule = ('\n<!-- TEXT-INJECT-S176:BEGIN -->\n2026-10-13 S176：文本注入与本地化口径（只读提取）。'
        'NativeDialogue.cs/NativeDocuments.cs 证据：双语数组索引0=EN、1=CN（global.language==3取CN）、__dialogue_flow_data+npc_lines_map以json_parse注入、文书走原生物品原语；不改STRG、不依赖外部文件。'
        '未接线、未构建、未部署。入口design/11_管理/文本注入与本地化口径.md；运行Validate-TextInjection.py及既有检查。\n<!-- TEXT-INJECT-S176:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- TEXT-INJECT-S176:BEGIN -->.*?<!-- TEXT-INJECT-S176:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- TEXT-INJECT-S176:BEGIN -->.*?<!-- TEXT-INJECT-S176:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(lang_line=lang, sample=bool(pair), sample_lines=counts['dialogue_lines'], our_lines=facts['our_content']['dialogue_lines']), ensure_ascii=False))
