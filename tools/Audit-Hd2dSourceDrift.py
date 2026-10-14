"""Record detected scene-source drift and concrete missing art, without editing story files."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    cues={
      '台本_N2_灰堤没有墓碑.md':dict(scene_batch='R01-camp-canal-v1',locator=['N2-S01','N2-S02'],required_art=['雇工棚门槛灰圈','轴座下压着的借据存根与小印'],boundaries=['灰圈不生成亡者','借据关联不自动认证采购链'],impact='New observable props are absent in current art; existing empty coffin/jacket/shaft/return geometry remains usable.'),
      '台本_N5_渡口的三种说法.md':dict(scene_batch='R02-river-v1',locator=['N5-S02'],required_art=['税栈墙根新漆井牌','井牌下两只红桶与运水绳结'],boundaries=['观察线索不预写污染结论','保持基础浅滩'],impact='Add independent sign/two-bucket cue; do not regenerate NPCs or close the ford.'),
      '台本_N9_把证据摆上桌.md':dict(scene_batch='R02-river-v1',locator=['X75','X76','N9-S03'],required_art=[],boundaries=['公开编号、日期及跨页对照由引擎文字/物件状态绘制'],impact='Current public table/river windows/separated cabinets fit the current text; no new raster prop identified.'),
      '台本_N18_誓约之后.md':dict(scene_batch='R02-river-v1',locator=['N18-S01'],required_art=['摊边一双编到一半的小绳鞋'],boundaries=['只作有条件回访细节','不替家属表态'],impact='Add a versioned conditional return-visit prop, off by default; no child/NPC image.'),
      '台本_SQ04_一条不卖人的路.md':dict(scene_batch='R02-river-v1',locator=['SQ04-S03'],required_art=['钉在桥头木牌上的字条底图'],boundaries=['拒绝强运且对应回访时才显示','不清旧伤害记录','仍保留浅滩'],impact='Add a conditional blank note layer; readable writing and actual conditions belong to the engine.'),
    }
    rows=[];historical=[]
    active={r['batch'] for r in json.loads((P/'progress.json').read_text(encoding='utf-8'))['requests'].values()}
    for f in sorted((P/'batches').glob('*/manifest.json')):
        m=json.loads(f.read_text(encoding='utf-8'))
        for n,old in m['source_sha256'].items():
            current=sha(ROOT/n)
            if old==current:continue
            detail=cues.get(Path(n).name)
            (rows if m['batch'] in active else historical).append(dict(batch=m['batch'],source=n,export_source_sha256=old,current_source_sha256=current,status='needs_scene_art_sync' if detail and detail['required_art'] else 'needs_reviewed_source_revalidation',review=detail or {'impact':'New source drift, not yet semantically reviewed'}))
    out=dict(date='2026-10-14',scope='Scene sources only; no NPC text/logic edits',comparison='Current source versus exported source fingerprints; git diff consulted as supporting context, not asserted identical to the old exported source snapshot',changed_sources=len(rows),records=rows,original_art_preserved=True,runtime_verified=False)
    out.update(audited_active_batches=sorted(active),historical_snapshots_with_drift=len(historical),historical_records=historical,historical_note='Superseded v1 snapshots are preserved and excluded from the active work queue; their old source hashes are never rewritten')
    (P/'source-sync-queue.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(changed_sources=len(rows),historical_snapshots_with_drift=len(historical),active_batches=sorted(active)),ensure_ascii=False))
if __name__=='__main__':main()
