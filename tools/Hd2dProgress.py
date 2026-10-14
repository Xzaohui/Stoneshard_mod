"""Register validated scene batches and reconcile whole-project art counts."""
from pathlib import Path
import argparse,json,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def register(batch):
    folder=(P/'batches'/batch).resolve();assert folder.is_relative_to((P/'batches').resolve())
    m=read(folder/'manifest.json');v=read(folder/'validation.json');assert v['passed'],batch
    if 'asset_manifest_sha256' in v:assert sha(folder/'manifest.json')==v['asset_manifest_sha256'],'Validation candidate changed'
    for a in m['assets']:assert sha(folder/a['path'])==a['sha256'],a['path']
    for p,h in m['source_sha256'].items():assert sha(ROOT/p)==h,'Source changed: '+p
    progress=read(P/'progress.json');prefix=folder.relative_to(P).as_posix()+'/'
    outputs={prefix+a['path']:a['sha256'] for a in m['assets']}
    replacement=m.get('supersedes')
    if replacement:
        old_folder=P/'batches'/replacement['batch'];old_manifest=read(old_folder/'manifest.json')
        assert sha(old_folder/'manifest.json')==replacement['manifest_sha256'],'Superseded snapshot changed'
        assert sorted(m['inventory_requests'])==replacement['inventory_requests']==sorted(old_manifest['inventory_requests']),'Replacement must preserve the complete old view scope'
        prior={k:progress['requests'][k] for k in m['inventory_requests'] if progress['requests'].get(k,{}).get('batch')==replacement['batch']}
        history=P/'progress-history';history.mkdir(exist_ok=True);snapshot=history/(replacement['batch']+'.json')
        if prior and not snapshot.exists():write(snapshot,dict(batch=replacement['batch'],manifest_sha256=replacement['manifest_sha256'],superseded_by=m['batch'],requests=prior))
    for key,path in m['inventory_requests'].items():
        old=progress['requests'].get(key)
        assert not old or old['batch']==m['batch'] or (replacement and old['batch']==replacement['batch']),'A different art batch owns '+key
        progress['requests'][key]=dict(batch=m['batch'],status='static_export_verified',path=prefix+path,
            outputs=outputs,source_sha256=m['source_sha256'],runtime_verified=False)
    write(P/'progress.json',progress)
def reconcile(date='2026-10-13'):
    subprocess.run([sys.executable,str(ROOT/'tools/Build-Hd2dInventory.py')],check=True)
    inv=read(P/'inventory.json');batches={};master_hashes=set();master_copies=0
    registered={r['batch'] for r in read(P/'progress.json')['requests'].values()}
    for f in [P/'manifest.json',*sorted((P/'batches').glob('*/manifest.json'))]:
        if not f.exists():continue
        m=read(f);log=read(f.parent/'generation-log.json');v=read(f.parent/'validation.json')
        if m['batch'] not in registered or not v['passed'] or m['status']!='static_export_verified_runtime_unverified':continue
        generated=log['records']+log.get('external_generation_records',[])
        assert all(r.get('output_sha256') for r in generated),'Missing master output fingerprint'
        master_hashes.update(r['output_sha256'] for r in generated);master_copies+=len(generated)
        reqs=[r for r in inv['requests'] if r.get('batch')==m['batch']]
        pending=sum(r['status']=='needs_revalidation' for r in reqs)
        batches[m['batch']]=dict(path=f.parent.relative_to(P).as_posix(),production_pngs=len(m['assets']),
            generated_master_files=log['generation_count'],static_passed=v['passed'],source_current=not pending,
            fulfilled_view_slots=sum(r['status']=='static_export_verified' for r in reqs),needs_revalidation_view_slots=pending,runtime_verified=False)
    production=sum(b['production_pngs'] for b in batches.values());masters=len(master_hashes)
    state=dict(date=date,scope='Scene art only; NPC files/events are owned by the other model',
        initial_view_slots=inv['initial_view_slots'],fulfilled_view_slots=inv['fulfilled_view_slots'],remaining_view_slots=inv['remaining_view_slots'],
        exported_view_slots=sum(r['status'] in ['static_export_verified','needs_revalidation'] for r in inv['requests']),
        needs_revalidation_view_slots=sum(r['status']=='needs_revalidation' for r in inv['requests']),
        not_drawn_view_slots=sum(r['status']=='not_drawn' for r in inv['requests']),
        production_pngs=production,generated_master_files=masters,generated_master_batch_copies=master_copies,master_counting='Unique generated output SHA256 across active batches; shared cue master counted once',batches=batches,runtime_verified=False)
    pending={}
    for folder in sorted((P/'batches').iterdir()):
        if folder.name in registered or not (folder/'materials-manifest.json').is_file():continue
        manifests=[read(f) for f in [folder/'materials-manifest.json',folder/'sprite-manifest.json'] if f.is_file()]
        assets={a['id']:a for m in manifests for a in m['assets']};brief=read(folder/'brief.json');log=read(folder/'generation-log.json')
        assert all(sha(folder/a['path'])==a['sha256'] for a in assets.values())
        pending[folder.name]=dict(path=folder.relative_to(P).as_posix(),status='materials_and_sprites_verified_scene_assembly_pending',partial_pngs=len(assets),generated_master_files=sum(bool(r.get('output_sha256')) for r in log['records']),planned_view_slots=len(brief['inventory_requests']),fulfilled_view_slots=0,source_current=all(sha(ROOT/n)==h for n,h in brief['source_sha256'].items()),preview='assets-preview.html',runtime_verified=False)
    state['work_in_progress_batches']=pending
    write(P/'artwork-state.json',state)
    progress=read(P/'progress.json');progress.update(date=state['date'],counting_note=f"{state['fulfilled_view_slots']} verified view slots; {production} production PNGs across registered batches. View slots, raw masters and layer files are separate counts.")
    write(P/'progress.json',progress)
    proposal=read(P/'proposal.json');proposal.update(status='production_in_progress_importable_batches',generation_started=True,
        finished_new_images=production,production_pngs=production,generated_master_files=masters,
        fulfilled_view_slots=state['fulfilled_view_slots'],remaining_view_slots=state['remaining_view_slots'],production_batches=batches)
    write(P/'proposal.json',proposal)
    subprocess.run([sys.executable,str(ROOT/'tools/Write-Hd2dArtIndex.py')],check=True)
    print(json.dumps(state,ensure_ascii=False))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--batch');ap.add_argument('--date',default='2026-10-13');args=ap.parse_args()
    if args.batch:register(args.batch)
    reconcile(args.date)
