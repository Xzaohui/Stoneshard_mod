from pathlib import Path
import json,hashlib,shutil,zipfile
R=Path.cwd();D=R/'Assets/CharacterActions/20261013/delivery_belo_kien_work_v1';S=D/'source_tree';O=D/'deliverables';S.mkdir(exist_ok=True);O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[('belo','hoop_edge_check_v1','73d1d92c5085d7fc0350d64609a802b8743845f6404a5feb05225e4e8dad7269','belo_hoop_edge_check_sparse_once.gif'),('kien','sample_box_regrip_v1','c63b6d4a84f548a2636823ce273f941a2979b5468b34781a44fd4e3284f362b7','kien_sample_box_regrip_sparse_once.gif')]
source_paths=[];changed=[]
for slug,branch,qsha,gif in records:
 A=R/f'Assets/CharacterActions/20261013/{slug}/{branch}';q=A/'QA-independent.json';assert sha(q)==qsha
 hist=A/'pre_final_status';hist.mkdir(exist_ok=True)
 for n in ['manifest.json','FINAL_STATUS.json']:shutil.copy2(A/n,hist/n)
 status=json.loads((A/'FINAL_STATUS.json').read_text());status.update({'status':'independent_review_pass_sparse_concept','current_independent_qa':{'path':'QA-independent.json','sha256':qsha},'final_delivery_scope':'已审人物基础动作与单次稀疏GIF；非游戏运行或连续动画','historical_status_snapshot':'pre_final_status/FINAL_STATUS.json'});(A/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
 m=json.loads((A/'manifest.json').read_text());m.update({'status':'independent_review_pass_sparse_concept','independent_review':{'path':'QA-independent.json','sha256':qsha},'gif_gate':'已通过独立增量复核；仅单次稀疏关键姿态概念','final_status':'FINAL_STATUS.json'});m['files']=[{'path':str(p.relative_to(A)),'sha256':sha(p)} for p in sorted(A.rglob('*')) if p.is_file() and p!=A/'manifest.json'];(A/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 target=S/A.relative_to(R);shutil.copytree(A,target,dirs_exist_ok=True)
 for src in m['sources']:
  p=R/src['path'];assert sha(p)==src['sha256'];out=S/src['path'];out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out);source_paths.append(src)
 for p in [A/f'{slug}_review_zh_light.png',A/gif]:shutil.copy2(p,O/p.name)
 changed.append({'character':slug,'current_qa_sha256':qsha,'current_manifest_sha256':sha(A/'manifest.json')})
readme='''贝洛与奇恩：城镇职业／日常基础动作第二组\n\n贝洛：1张新姿态，抬箍检查箍缘；指腹实际触前／外缘，不断言内缘。\n奇恩：2张新姿态，提柄不松、空手托底；双手腹前低抱。\n两人共3新姿态；复用锚形成3／4展示阶段，不是3／4张新图。\nGIF各单次播放且无loop扩展；属于稀疏关键姿态示意，不是连续工序动画。\n独审为概念通过；奇恩箱厚／框宽有漂移，未验证精确三维尺寸或受力。\n非交货、验收、来源合法化、改箍获认可、原谅或署名结果；没有游戏集成与运行验证。\n\nAssets/CharacterActions下保留raw、透明帧、双底图、完整提示词、脚本、当前manifest和FINAL_STATUS、作者QA、当前独审及历史独审、审前快照。\nAssets/CharacterDesigns下保留精确原始锚字节与brief；design下保留人物来源卡。\n以当前QA-independent.json与FINAL_STATUS.json为最终结论；pre_目录及历史QA保存当时状态，不替代当前结论。\n生成提示词与build_review/finalize_review脚本为生产记录，不应直接覆盖运行已交付文件；需要重跑请在副本操作。\n\n所有人物姿态由内置imagegen生成，脚本仅透明清理、共同nearest等比缩放、接地平移与排板/GIF，没有脚本造身体或非等比拉伸。\n'''
(S/'README_zh.txt').write_text(readme);shutil.copy2(Path(__file__),S/'package_sources.py')
files=[p for p in sorted(S.rglob('*')) if p.is_file() and p.name!='SOURCE_MEMBER_HASHES.json'];memberhash=[{'path':str(p.relative_to(S)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files];(S/'SOURCE_MEMBER_HASHES.json').write_text(json.dumps(memberhash,ensure_ascii=False,indent=2)+'\n')
z=O/'belo_kien_work_poses_source_v1.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for p in sorted(S.rglob('*')):
  if p.is_file():f.write(p,p.relative_to(S))
assert z.stat().st_size<18*1024*1024
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for rec in memberhash:assert hashlib.sha256(f.read(rec['path'])).hexdigest()==rec['sha256']
 expected={str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()};assert set(f.namelist())==expected
inventory={'deliverables':[{'path':str(p.relative_to(R)),'absolute_path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(O.iterdir()) if p.is_file()],'verified':{'exact_deliverable_count':5,'zip_crc_pass':True,'all_member_sha256_match':True,'zip_member_count':len(expected),'zip_below_18_mib':True},'current_review_states':changed,'source_inputs':source_paths,'uploaded':False}
assert len(inventory['deliverables'])==5
(D/'DELIVERY_INVENTORY.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n');print(json.dumps(inventory,ensure_ascii=False,indent=2))
