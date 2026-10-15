#!/usr/bin/env python3
"""Read immutable delivery selections and construct the v2 catalog map."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
BASE=HERE.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def ref(p):return {'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size}
s=json.loads((BASE/'catalog_v1/selected_sources.json').read_text())
labels=['收矛回重心','下挥中段','前压扣抓末端','探手回束','回爪后承重','侧移换重心','短斧前送斜劈','低姿撤步换重心','双手斧高位蓄劈','探剑后屈肘回收','喉胸前送释放','手铃外摆端点']
versions=[2,None,1,1,1,1,1,2,1,1,2,1]
paths=[
'first_six/continuation_001_002_delivery_v1/border_spear_rebel_spear_retract_weight_back_transparent.png',None,
'first_six/continuation_003_004_delivery_v1/canal_tomb_restless_reach_clasp_end_transparent.png',
'first_six/continuation_003_004_delivery_v1/crypt_drifter_wraith_spectral_hand_recoil_transparent.png',
'first_six/continuation_005_006_delivery_v1/blood_hunger_mutant_claw_retract_rear_load_transparent.png',
'first_six/continuation_005_006_delivery_v1/debt_ritual_warden_guard_lateral_weight_transfer_transparent.png',
'second_six/continuation_007_008_delivery_v1/007_axe_forward_cut_selected.png',
'second_six/continuation_007_008_delivery_v1/008_crossbow_backstep_load_selected.png',
'second_six/continuation_009_010_delivery_v1/009_锈甲斧亡卒_双手斧高位蓄劈.png',
'second_six/continuation_009_010_delivery_v1/010_残盾哨影_探剑后屈肘回收.png',
'second_six/continuation_011_012_delivery_v1/011_喉胸前送释放.png',
'second_six/continuation_011_012_delivery_v1/012_手铃外摆端点.png']
evidence={}
def evidence_add(p):
 p=Path(p);r=ref(p);evidence[r['path']]=r;return r
for p in [BASE/'catalog_v1/selected_sources.json',BASE/'catalog_v1/FINAL_CATALOG_QA.json',BASE/'catalog_v1/build_catalog.py']:
 evidence_add(p)
for batch in ['first_six','second_six']:
 evidence_add(BASE/batch/'ACTION_CONTINUATION_DELIVERY_INDEX.md')
 evidence_add(BASE/batch/'INDEX.md')
 for p in (BASE/batch).glob('continuation_*_delivery_v1/*.json'):
  if p.name in ['delivery_manifest.json','independent_package_audit.json','QA_DELIVERY_INDEPENDENT.json','FINAL_STATUS.json','DELIVERY_RECEIPT.json']:evidence_add(p)
 for p in (BASE/batch).rglob('FINAL_STATUS.json'):
  if '/sources/' not in str(p):evidence_add(p)
 for p in (BASE/batch).rglob('*QA*.json'):
  if '/sources/' not in str(p) and ('action_continuation_v1' in str(p) or 'independent_action_continuation' in p.name):evidence_add(p)
for i,e in enumerate(s['enemies']):
 for j,a in enumerate([e['idle']]+e['actions']):
  p=ROOT/a['path'];assert sha(p)==a['sha256'];a['bytes']=p.stat().st_size
  a['slot']='static' if j==0 else f'original_action_{j}'
  if j==0:a['label']='静态母图';a['version']='idle_style_v2' if e['id'] in ['009','012'] else 'idle_v1'
 if paths[i]:
  p=BASE/paths[i];a={**ref(p),'label':labels[i],'version':versions[i],'slot':'continuation','status':'passed_selected_independent_keypose'}
  manifest=p.parent/'delivery_manifest.json';assert a['sha256'] in manifest.read_text(),p
  a['delivery_manifest']=evidence_add(manifest)
  finalfiles=list((BASE/('first_six' if i<6 else 'second_six')/e['role']/'action_continuation_v1').rglob('FINAL_STATUS.json'))
  finalfiles=[p for p in finalfiles if '/sources/' not in str(p)];assert len(finalfiles)==1
  final=finalfiles[0];assert a['sha256'] in final.read_text(),final
  a['final_status']=evidence_add(final)
  e['continuation']=a
 else:
  e['continuation']=None;e['missing_stage']={'label':labels[i],'status':'failed_no_selected_revision_budget_exhausted','selected':None,'note':'v1、v2均未通过；缺项，不展示失败稿，不计入完成。','final_status':evidence_add(BASE/'first_six/canal_club_brigand/action_continuation_v1/FINAL_STATUS.json')}
 e['selected_image_count']=4 if paths[i] else 3
 e['independent_action_count']=3 if paths[i] else 2
 e['catalog_page']=i+3
 if i==0:e['selection_caveat']='原两动作沿用已通过自然前握替代；原始握法要求未过。跨姿矛长未验证。'
 elif i in [3,9]:e['selection_caveat']='保留原审定半透明和完整画布；未提高不透明度。'
 elif i==10:e['selection_caveat']='续姿使用通过的 v2；保留原 RGBA 与四边 64 像素透明留边。'
 elif i==11:e['selection_caveat']='母图用 idle_style_v2；续姿保留原交付 alpha 阈值处理与留边。'
 elif i==8:e['selection_caveat']='母图沿用已选 idle_style_v2；续姿为高位蓄劈 v1。'
 elif i==1:e['selection_caveat']='下挥中段 v1、v2 均未通过；本页第四格保留缺项。'
 else:e['selection_caveat']='原两动作与续姿均沿用既有选稿；展示比例不代表游戏尺寸。'
all_images=[a for e in s['enemies'] for a in [e['idle']]+e['actions']+([e['continuation']] if e['continuation'] else [])]
assert len(all_images)==47 and len({a['sha256'] for a in all_images})==47
for a in all_images:
 im=Image.open(ROOT/a['path']);assert im.mode=='RGBA';a['dimensions']=list(im.size)
 a['rgba_decoded_sha256']=hashlib.sha256(im.tobytes()).hexdigest()
s.update({'schema_version':2,'catalog_version':'v2','status':'approved_selected_sources_locked','date_utc':'2026-10-14','counts':{'static':12,'original_actions':24,'previously_delivered_continuations':11,'independent_actions':35,'unique_selected_images':47,'missing_continuation':1,'newly_generated_images_this_task':0},'selection_note':'The v1 36-source selection is unchanged. Add only 11 previously delivered continuations. 002 remains failed/missing; original count is not increased by duplicate appearances.','evidence_refs':list(evidence.values())})
dump(HERE/'selected_sources.json',s)
for e in evidence.values():
 dst=HERE/'evidence'/e['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/e['path'],dst)
shutil.copyfile(BASE/'catalog_v1/FONT_LICENSE.txt',HERE/'FONT_LICENSE.txt')
print('47 unique sources; evidence files',len(evidence))
