from pathlib import Path
import json, hashlib, sys
r=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
selected=sys.argv[1] if len(sys.argv)>1 else "portrait_v2_maxcoverage"
entry=json.loads((r/"sources/roster_entry.json").read_text())
files=[{"path":str(p.relative_to(r)),"sha256":sha(p),"bytes":p.stat().st_size} for p in sorted(r.rglob("*")) if p.is_file() and p.name not in {"manifest.json","SHA256SUMS"}]
metrics=[json.loads(p.read_text()) for p in sorted((r/"qa").glob("portrait_v*_metrics.json"))]
p=r/"candidates"/f"{selected}_74x100_candidate.png"
manifest={"schema_version":1,"actor_id":entry["canonical_id"],"name":entry["name"],"date":"2026-10-15","selected_portrait":str(p.relative_to(r)),"selected_sha256":sha(p),"status":"awaiting_independent_visual_QA","generation_calls":len(list((r/"tool_returns").glob("portrait_v*.json"))),"max_attempts":2,"native_authored":False,"native_pixel_approved":False,"runtime_integrated":False,"runtime_verified":False,"independent_qa":None,"old_assets_preserved":True,"color_budget_note":"At most 32 visible RGB colors is a temporary working ceiling, not proof of native pixel art.","method":"Built-in imagegen substantive redraw. Whole-canvas NEAREST resize, binary alpha threshold 128 and no-dither quantization are explicitly derived candidates, not native authored pixel finals.","source_manifest":"sources/source_manifest.json","spec_lock":"spec_lock.md","reproduction":["python derive_portrait.py","python export_maxcoverage.py portrait_v1","python export_maxcoverage.py portrait_v2","python finalize_manifest.py "+selected],"assets":metrics,"files":files}
(r/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
(r/"SHA256SUMS").write_text("".join(f"{sha(p)}  {p.relative_to(r)}\n" for p in sorted(r.rglob("*")) if p.is_file() and p.name!="SHA256SUMS"))
print(json.dumps({"actor":entry["canonical_id"],"selected":str(p.relative_to(r)),"sha256":sha(p),"generation_calls":manifest["generation_calls"]},ensure_ascii=False))
