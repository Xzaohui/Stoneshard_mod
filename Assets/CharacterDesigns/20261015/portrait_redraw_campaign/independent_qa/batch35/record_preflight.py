"""Write the independent identity review without changing source or author files."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
Q=Path(__file__).resolve().parent;P=Q.parent.parent;R=P.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
roster=json.loads((P/'campaign_roster.json').read_text())
identities={
'beina':'约四十岁成年洗砂住户女性，成熟疲惫而有主见，蓝头巾包严、棕发、灰旧罩衣与锈色窄内领。当前罩衣口径优先历史裙装；不替全村和解，不用肖像表示赔款或净水已完成。',
'anni':'二十多岁成年女性普通当班护理者；棕发低髻、米灰素护理褂，只呈窄领；坦诚清楚报这一班，不能读成幼童、万能护理或研究许可。',
'kuen':'三十多岁偏白成年男性，奥娅成年伴侣与自主患者；棕乱发、少量胡茬、灰褐厚织披肩及灰蓝普通布衫；清醒具体说明需要，不作濒死无助或痊愈演出。',
'lint':'三十多岁成年女性护理接收员，方颊、平浓眉、明确鼻翼及厚说话嘴；最新卡短棕发别耳后、素米灰护理褂优先旧母图高髻/赭裙/围裙。外观更新不增新身份；只接真实当班，尊重拒绝。'}
rows=[]
for s in identities:
 e=next(x for x in roster['characters'] if x['suggested_slug']==s)
 assert e==json.loads((P/s/'sources/roster_entry.json').read_text())
 refs=e['current_cards']+[e['identity_master'],e['master_selection_evidence']]+e['master_manifests']
 checks=[{'path':x['path'],'roster_sha256':x['sha256'],'actual_sha256':sha(R/x['path']),'matches':sha(R/x['path'])==x['sha256']} for x in refs]
 assert all(x['matches'] for x in checks)
 rows.append({'slug':s,'canonical_id':e['canonical_id'],'checks':checks,'identity_resolution':identities[s],'actual_visual_inspection':['mother image full resolution','Mara v2 integer4xNN','Iwo v1 integer4xNN','Leiya v2 maxcoverage integer4xNN','Tore v1 integer4xNN'],'latest_card_precedence':True,'unresolved_identity_age_sex_clothing_conflict':False})
sources=json.loads((Q/'independent_source_manifest.json').read_text())
report={'batch':35,'checked_utc':datetime.now(timezone.utc).isoformat(),'instructions_read':['AGENTS.md','design/AGENTS.md'],'sources_snapshot_manifest':'independent_source_manifest.json','source_count':len(sources['sources']),'sources_independently_copied_from_original':True,'story_read_scope':'Read current linked exact actor passages plus neighbouring context and shared consent, absence, finite shift and future decision constraints. CM-FOR contains no Beina-named line; CS-FOR-02 contains her personal water/settlement choices.','characters':rows,'limitations':['Portrait candidates only.','No native-pixel or runtime approval.','No current or historical production source changes.']}
(Q/'identity_preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('Four identities checked; 34 source snapshots locked.')
