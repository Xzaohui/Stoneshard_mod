from pathlib import Path
from PIL import Image
import hashlib, json, sys, base64, subprocess
r=Path(__file__).resolve().parent
repo=r.parents[4]
selected=sys.argv[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n")
entry=json.loads((r/"sources/roster_entry.json").read_text())
target=r/"candidates"/f"{selected}_74x100_candidate.png"
assert target.is_file()
sources=json.loads((r/"sources/source_manifest.json").read_text())["sources"]
source_checks=[]
for s in sources:
 snap=r/s["snapshot_path"]; original=repo/s["original_path"]
 source_checks.append({"snapshot":s["snapshot_path"],"original":s["original_path"],"recorded_sha256":s["sha256"],"snapshot_sha256":sha(snap),"original_sha256":sha(original),"snapshot_matches":sha(snap)==s["sha256"],"old_original_unchanged":sha(original)==s["sha256"]})
raw_checks=[]
for v in ["portrait_v1","portrait_v2"]:
 ret=r/"tool_returns"/f"{v}.json";raw=r/"raw"/f"{v}_raw_imagegen.png"
 data=base64.b64decode(json.loads(ret.read_text())["image_url"].split(",",1)[1])
 raw_checks.append({"version":v,"raw_path":str(raw.relative_to(r)),"raw_sha256":sha(raw),"tool_return_path":str(ret.relative_to(r)),"tool_return_sha256":sha(ret),"raw_equals_decoded_tool_return":raw.read_bytes()==data,"raw_dimensions":list(Image.open(raw).size)})
outputs=[p for folder in ["raw","candidates","previews","qa","prompts"] for p in (r/folder).glob("*") if p.is_file() and p.name!="reproducibility_and_source_integrity.json"]
before={str(p.relative_to(r)):sha(p) for p in outputs}
commands=[["python","derive_portrait.py"],["python","export_maxcoverage.py","portrait_v1"],["python","export_maxcoverage.py","portrait_v2"],["python","export_containment.py","portrait_v2"],["python","export_containment.py","portrait_v2","MEDIANCUT"]]
for cmd in commands:subprocess.run(cmd,cwd=r,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
after={str(p.relative_to(r)):sha(p) for p in outputs}
repro={"sources":source_checks,"raw_and_tool_returns":raw_checks,"commands":[" ".join(c) for c in commands],"rerun_outputs_identical":before==after,"mismatches":[k for k in before if before[k]!=after[k]],"all_sources_unchanged":all(s["snapshot_matches"] and s["old_original_unchanged"] for s in source_checks),"all_raw_match_tool_return":all(s["raw_equals_decoded_tool_return"] for s in raw_checks)}
write(r/"qa/reproducibility_and_source_integrity.json",repro)
assert repro["rerun_outputs_identical"] and repro["all_sources_unchanged"] and repro["all_raw_match_tool_return"]
metric=json.loads((r/"qa"/f"{selected}_metrics.json").read_text())
feedback=r/"qa/independent_final_feedback.json"
manifest={"schema_version":1,"actor_id":entry["canonical_id"],"name":entry["name"],"slug":r.name,"date":"2026-10-15","selected_portrait":str(target.relative_to(r)),"selected_sha256":sha(target),"status":"independent_visual_pass_candidate_awaiting_batch_hash_audit" if feedback.exists() else "candidate_awaiting_independent_selection","generation_calls_completed":2,"generation_call_budget":2,"parameter_validation_failures":1,"validation_failure_produced_image":False,"native_authored":False,"native_pixel_approved":False,"runtime_integrated":False,"runtime_verified":False,"old_assets_preserved":True,"method":"Built-in imagegen substantive redraw, one draft and one focused revision. Full raw nearest-neighbor derived export, binary alpha, temporary <=32 work colors. Selected containment export fits full raw aspect-preservingly within 72x98 (actual 72x97), centered at (1,1) on 74x100. No geometry redrawn, content restored or painted by script. Not native pixel authorship.","selected_export":metric["derivation"],"selected_target_metrics":metric["target"],"raw_provenance":raw_checks,"source_manifest":"sources/source_manifest.json","identity_lock":"spec_lock.md","exact_generation_arguments":["prompts/portrait_v1.json","prompts/portrait_v2.json"],"tool":"image_gen.imagegen built-in","model_size_quality_seed":"Not exposed by built-in tool; no fabricated values.","independent_qa":"../independent_qa/batch11/FINAL_SELECTION.json","independent_technical_audit":"../independent_qa/batch11/technical_audit.json","independent_final_feedback":"qa/independent_final_feedback.json" if feedback.exists() else None,"independent_batch_artifacts_pending_at_freeze":True,"reproduction":[" ".join(c) for c in commands]+[f"python finalize_manifest.py {selected}"],"reproduction_audit":"qa/reproducibility_and_source_integrity.json","previews":{"1x":str(target.relative_to(r)),"8x":f"previews/{selected}_8x.png","1x_on_3_backgrounds_plus_8x":f"previews/{selected}_1x_8x.png"},"limitations":["Pixel-style imagegen original is not natively authored 74x100 pixel art.","Temporary 32-color ceiling is a technical working limit, not production approval.","Containment preserves sampled raw silhouette and adds border transparency; it does not establish or restore hypothetical detail outside raw canvas.","No old asset, card, gameplay code or runtime package changed. No commit or push."]}
manifest["visual_notes"] = json.loads(feedback.read_text())["notes"] if feedback.exists() else "Awaiting independent review"
write(r/"manifest.json",manifest)
(r/"README.md").write_text(f"# {entry['name']} / {entry['canonical_id']}\n\n选稿：{manifest['selected_portrait']}\nSHA-256：{manifest['selected_sha256']}\n\n本目录为全人物对白头像重绘新候选。保留原始生图、两个完整工具返回、准确参数、来源快照及SHA、首稿与唯一修订、两种技术量化对照和透明边导出。先实看现卡、旧母版与四核心风格；现卡年龄/收发/衣色优先。\n\n方法：内置imagegen实质绘制；NN、二值alpha及≤32临时工作色是明示技术派生，不是原生逐像素作者稿。未集成或验证游戏运行，不覆盖旧素材。\n\n重现：\n"+"\n".join(manifest["reproduction"])+"\n\n四边透明安全框只增加留边，不补画原图外内容。独立最终批次QA见manifest链接。\n")
with (r/"README.md").open("a") as f:f.write("\n视觉备注："+manifest["visual_notes"]+"\n")
files=sorted(p for p in r.rglob("*") if p.is_file() and p.name!="SHA256SUMS" and "__pycache__" not in p.parts)
(r/"SHA256SUMS").write_text("".join(f"{sha(p)}  {p.relative_to(r).as_posix()}\n" for p in files))
print(json.dumps({"slug":r.name,"selected":manifest["selected_portrait"],"selected_sha256":sha(target),"manifest_sha256":sha(r/"manifest.json"),"source_manifest_sha256":sha(r/"sources/source_manifest.json"),"reproduction":repro["rerun_outputs_identical"],"source_unchanged":repro["all_sources_unchanged"],"raw_tool":raw_checks},ensure_ascii=False))
