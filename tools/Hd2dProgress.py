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
    for a in m['assets']:assert sha(folder/a['path'])==a['sha256'],a['path']
    for p,h in m['source_sha256'].items():assert sha(ROOT/p)==h,'Source changed: '+p
    progress=read(P/'progress.json');prefix=folder.relative_to(P).as_posix()+'/'
    outputs={prefix+a['path']:a['sha256'] for a in m['assets']}
    for key,path in m['inventory_requests'].items():
        old=progress['requests'].get(key)
        assert not old or old['batch']==m['batch'],'A different art batch owns '+key
        progress['requests'][key]=dict(batch=m['batch'],status='static_export_verified',path=prefix+path,
            outputs=outputs,source_sha256=m['source_sha256'],runtime_verified=False)
    write(P/'progress.json',progress)
def reconcile():
    subprocess.run([sys.executable,str(ROOT/'tools/Build-Hd2dInventory.py')],check=True)
    inv=read(P/'inventory.json');batches={}
    for f in [P/'manifest.json',*sorted((P/'batches').glob('*/manifest.json'))]:
        if not f.exists():continue
        m=read(f);log=read(f.parent/'generation-log.json');v=read(f.parent/'validation.json')
        batches[m['batch']]=dict(path=f.parent.relative_to(P).as_posix(),production_pngs=len(m['assets']),
            generated_master_files=log['generation_count'],static_passed=v['passed'],runtime_verified=False)
    production=sum(b['production_pngs'] for b in batches.values());masters=sum(b['generated_master_files'] for b in batches.values())
    state=dict(date='2026-10-13',scope='Scene art only; NPC files/events are owned by the other model',
        initial_view_slots=inv['initial_view_slots'],fulfilled_view_slots=inv['fulfilled_view_slots'],remaining_view_slots=inv['remaining_view_slots'],
        production_pngs=production,generated_master_files=masters,batches=batches,runtime_verified=False)
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
    ap=argparse.ArgumentParser();ap.add_argument('--batch');args=ap.parse_args()
    if args.batch:register(args.batch)
    reconcile()
