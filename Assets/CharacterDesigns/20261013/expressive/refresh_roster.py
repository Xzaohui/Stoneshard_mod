#!/usr/bin/env python3
"""Refresh inventory and INDEX only. Never infer visual acceptance from file presence."""
import argparse,collections,datetime,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'design/04_人物').is_dir())
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',help='Validate without writing');args=p.parse_args()
path=HERE/'roster.json';data=json.loads(path.read_text());records=data['characters'];errors=[]
ids=[r['id'] for r in records]
if len(ids)!=len(set(ids)):errors.append('duplicate canonical IDs')
for r in records:
 if not r['sources']:errors.append(r['id']+': no sources')
 for s in r['sources']:
  if not (ROOT/s['path']).is_file():errors.append('missing source '+s['path'])
 for s in r['old_design_paths']:
  if not (ROOT/s).is_file():errors.append('missing old design '+s)
 if r.get('work_directory'):
  folder=ROOT/r['work_directory'];files=[str(p.relative_to(ROOT)) for p in sorted(folder.glob('*.png'))]
  r['new_design_paths']=sorted(set(r['new_design_paths']+files))
  if files and r['status'] in ['queued','generation_assigned']:r['status']='generated_pending_visual_review'
 if r['id'].startswith('NPC') and r['id'] in ['NPC01','NPC02','NPC03'] and not r.get('generation_gate'):errors.append('original character lacks reference gate')
from alias_identity import derive_aliases
identity_owners={}
for r in records:
 expected,_=derive_aliases(r,ROOT)
 if r.get('aliases',[])!=expected:errors.append(r['id']+': aliases differ from verified own-source identities')
 for token in [r['id']]+r.get('aliases',[]):
  if token in identity_owners and identity_owners[token]!=r['id']:errors.append('ambiguous identity alias '+token)
  identity_owners[token]=r['id']
if errors:raise SystemExit('\n'.join(errors))
print(f'Validated {len(records)} unique characters; status counts: {dict(collections.Counter(r["status"] for r in records))}')
if args.check:raise SystemExit()
data['updated_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();data['counts']['deduplicated_characters_in_this_scope']=len(records)
data['counts']['explicitly_user_approved_characters_including_sela']=sum(r['status']=='concept_user_approved' or r.get('user_approval',{}).get('approved',False) for r in records)
data['counts']['expressive_raw_concepts_user_approved']=data['counts']['explicitly_user_approved_characters_including_sela']
data['counts']['expressive_additional_delivered_concept_candidates']=sum(r['status']=='delivered_concept_candidate' for r in records)
data['counts']['expressive_review_displayable_characters']=sum(r['status'] in ['delivered_concept_candidate','design_review_candidate'] for r in records)
data['counts']['expressive_research_only_characters']=sum(r['status']=='research_candidate_not_final_pass' for r in records)
data['counts']['expressive_independently_reviewed_characters']=sum(bool(r.get('review_record')) and (ROOT/r['review_record']).is_file() for r in records)
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
# Render the current snapshot, not historical dispatch prose.
lines=['# 表情化人物概念清单','', '**先读：[当前STYLE_DIRECTION](STYLE_DIRECTION.md)**。不机械强卡1:1或35px。','',f"当前明确范围：{len(records)}名可追溯候选（156城市／聚落卡＋7独立主线＋5台本配角＋4开篇）。不是全游戏总人数。",'',f"已交付{data['counts']['expressive_additional_delivered_concept_candidates']}名新人物概念，Sela G基准另计。返修与打包不重复计人。",'', '用户逐人认可、独审可展示、实际发送与原生／动作／装备验收分别记录。', '', '当前派工：'+data.get('dispatch_control',{}).get('status','unknown'),'','## 当前状态','']
for state,count in sorted(collections.Counter(r['status'] for r in records).items()):lines.append(f'- {state}: {count}')
lines+=['','## 分支与验收边界','', '- [动作覆盖与缺口](../../../CharacterActions/20261013/ACTION_COVERAGE.md)：动作与人物概念当前均继续规划；具体派工优先级见roster dispatch_control。','- 静态外观概念不等于动作已运行；当前动作分支独立处理齐勒非战斗样板与训练dummy攻击，本名册任务不改动作图。','- 装备机制未确立时保持unknown；不从职业／武器／单套服装推入队或永久fixed。','- 原作身份参考待核者不生成替代；Vian工具阻断无输出，不计完成。','- 实际选稿以roster的具体路径、SHA和独立QA为准。','', '## 逐组三人brief','']
by_id={r['id']:r for r in records}
import re
briefs=sorted((HERE/'briefs').glob('*.json'),key=lambda f:int(re.search(r'(\d+)\.json$',f.name).group(1)) if re.search(r'(\d+)\.json$',f.name) else 0)
for f in briefs:
 b=json.loads(f.read_text());cs=b.get('characters',[]);names='／'.join(x['name'] for x in cs);num=re.search(r'(\d+)\.json$',f.name)
 lines.append(f"- {num.group(1) if num else '?'} {names}：[brief](briefs/{f.name})")
 ids=[x.get('id',x.get('canonical_id')) for x in cs]
 lines.append('  '+ '；'.join(cid+' '+by_id[cid]['status'] for cid in ids if cid in by_id))
lines+=['','## 维护与缺口','', '[具体返工／原作参考门槛](REWORK_AND_REFERENCE_GATES.md) · [全部名册](roster.json) · [独立QA同步报告](QA_SYNC_REPORT.json) · [维护说明](ROSTER_MAINTENANCE.md)。','', 'INDEX只映射现存登记，不自动判通过。历史队列变化保留在QUEUE_HOLD与来源记录，当前状态以本页／roster为准。','', '## 人物索引','', '| 稳定ID | 姓名 | 当前状态 | 审看选稿 |','|---|---|---|---|']
for r in records:lines.append(f"| {r['id']} | {r['name']} | {r['status']} | {r.get('reviewed_artifact','')} |")
(HERE/'INDEX.md').write_text('\n'.join(lines)+'\n')
