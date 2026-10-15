from pathlib import Path
import json, hashlib,sys
r=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
entry=json.loads((r/"sources/roster_entry.json").read_text())
selected=sys.argv[1] if len(sys.argv)>1 else "portrait_v1"
review_path=r/"qa/independent_selection_summary.json"
review=json.loads(review_path.read_text()) if review_path.exists() else None
assets=[json.loads(p.read_text()) for p in sorted((r/"qa").glob("portrait_v*_metrics.json"))]
manifest={"schema_version":1,"actor_id":entry["canonical_id"],"name":entry["name"],"date":"2026-10-15","selected_portrait":f"candidates/{selected}_74x100_candidate.png","status":"candidate_selected_with_disclosed_limitations" if review else "candidate_pending_independent_review","generation_calls":len(list((r/"tool_returns").glob("portrait_v*.json"))),"max_attempts":2,"native_authored":False,"native_pixel_approved":False,"runtime_integrated":False,"runtime_verified":False,"independent_qa":review if review else "pending","old_assets_preserved":True,"color_budget_note":"32 visible RGB colors is a temporary working ceiling for this batch; quantization is not evidence of native pixel authorship or artistic approval.","method":"Built-in imagegen actual redraw; raw and full response preserved. Whole-canvas nearest-neighbor resize plus alpha threshold and no-dither quantization is an explicit derivative, not a native final.","source_manifest":"sources/source_manifest.json","spec_lock":"spec_lock.md","reproduction":["python derive_portrait.py","python export_maxcoverage.py portrait_v2",f"python finalize_manifest.py {selected}"],"assets":assets,"files":[{"path":str(p.relative_to(r)),"sha256":sha(p),"bytes":p.stat().st_size} for p in sorted(r.rglob("*")) if p.is_file() and p.name not in ("manifest.json","SHA256SUMS.txt")]}
(r/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
(r/"SHA256SUMS.txt").write_text("".join(f"{sha(p)}  {p.relative_to(r)}\n" for p in sorted(r.rglob("*")) if p.is_file() and p.name!="SHA256SUMS.txt"))
print(json.dumps({"character":entry["name"],"selected":manifest["selected_portrait"],"files":len(manifest["files"])}))
