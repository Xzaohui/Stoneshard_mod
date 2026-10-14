"""Verify standalone archive integrity and each packaged production PNG SHA."""
from pathlib import Path
import argparse,hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013'
def main(date='2026-10-13'):
    rows=[]
    for f in sorted(P.rglob('HD2D-*.zip')):
        with zipfile.ZipFile(f) as z:
            assert z.testzip() is None,f
            m=json.loads(z.read('manifest.json'));v=json.loads(z.read('validation.json'))
            assert v['passed'],f
            for a in m['assets']:assert hashlib.sha256(z.read(a['path'])).hexdigest()==a['sha256'],a['path']
            rows.append(dict(batch=m['batch'],path=f.relative_to(ROOT).as_posix(),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),files=len(z.namelist()),production_pngs=len(m['assets']),zip_crc_and_asset_sha_verified=True,runtime_verified=False))
    report=dict(date=date,scope='Packaged files only, independent of newer project source or game data',passed=True,archives=rows)
    (ROOT/f"artifacts/hd2d-package-integrity-{date.replace('-','')}.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--date',default='2026-10-13');args=ap.parse_args();main(args.date)
