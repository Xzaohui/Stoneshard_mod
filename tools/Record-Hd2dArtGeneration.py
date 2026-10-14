"""Record prompt/input fingerprints before generation, or copy a returned raw master."""
from pathlib import Path
import argparse,json,hashlib,re,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--batch',required=True);ap.add_argument('--id',required=True);ap.add_argument('--input',action='append',default=[]);ap.add_argument('--output');ap.add_argument('--transparent',action='store_true');args=ap.parse_args()
    parent=ROOT/'src/Art/hd2d_26x26_20261013/batches';p=(parent/args.batch).resolve();assert p.is_relative_to(parent.resolve());assert re.fullmatch(r'[a-z0-9-]+',args.id)
    path=p/'generation-log.json';log=json.loads(path.read_text(encoding='utf-8')) if path.exists() else dict(skill_commit='33d891c421a9ad3608f5a09af97271388ca923af',generation_count=0,records=[],reuse_sources=[])
    old=next((x for x in log['records'] if x['id']==args.id),None)
    if args.output:
        assert old and not old.get('output_sha256'),'Record before generating; completed masters are immutable'
        source=Path(args.output);out=p/'raw'/f'{args.id}.png';assert source.is_file() and not out.exists();shutil.copyfile(source,out)
        old.update(output=out.relative_to(p).as_posix(),output_sha256=sha(out),original_size=list(Image.open(out).size),selected=True);log['generation_count']=sum(bool(x.get('output_sha256')) for x in log['records'])
    else:
        assert old is None,'Do not duplicate or overwrite a generation request'
        prompt=p/'notes'/f'prompt-{args.id}.txt';lock=p/'spec_lock.md';text=prompt.read_text(encoding='utf-8');lock_text=lock.read_text(encoding='utf-8')
        assert set(re.findall(r'#[0-9A-Fa-f]{6}',text))<=set(re.findall(r'#[0-9A-Fa-f]{6}',lock_text)),'Prompt uses a color outside the lock'
        old=dict(id=args.id,method='built-in image_gen',prompt=prompt.relative_to(p).as_posix(),prompt_sha256=sha(prompt),spec_lock_sha256=sha(lock),inputs=[dict(path=n,sha256=sha(ROOT/n)) for n in args.input],transparent_background=args.transparent,selected=False)
        log['records'].append(old)
    path.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(id=args.id,record=old) if args.output else dict(id=args.id,prompt=(p/old['prompt']).read_text(encoding='utf-8'),input_paths=[str(ROOT/x['path']) for x in old['inputs']],record=old),ensure_ascii=False))
if __name__=='__main__':main()
