from pathlib import Path
from PIL import Image
import hashlib,json,subprocess
D=Path(__file__).resolve().parent;P=D.parent;R=P.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before={p.name:sha(p) for p in D.iterdir() if p.suffix=='.png'}
subprocess.run(['python',str(D/'build_revision.py')],check=True,capture_output=True)
subprocess.run(['python',str(D/'build_comparison.py')],check=True,capture_output=True)
assert all(sha(D/n)==s for n,s in before.items())
a=Image.open(D/'segmented_before_edits.png').convert('RGBA');b=Image.open(D/'liqui_native_1to1.png');start=list(a.getdata());l=json.loads((D/'pixel_edit_log.json').read_text())
for e in l['edits']:
 assert list(a.getpixel((e['x'],e['y'])))==e['before'];a.putpixel((e['x'],e['y']),tuple(e['after']))
assert list(a.getdata())==list(b.getdata())
assert sha(P/'liqui_native_v1.png')=='92d1abb4d4087634f0b994ba3613052362cfc62e673fdd1cf34d45a3cc689ddf'
assert sha(P/'v2/liqui_native_v2.png')=='695a1979420abe0fc88e0046d478b6b246c87cf3ca55ae312b8fdca41c5526c1'
sources=[P/'liqui_structure_concept_v2.png',P/'liqui_native_v1.png',P/'v2/liqui_native_v2.png',P/'prompt_v2.txt',R/'design/04_人物/城市人物/人物_TRADE-NPC-LIQUI_莉葵.md',R/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch47/177_trade_liqui_cast.png']+[R/'Assets/ReferenceAudit/20261013/originals'/n for n in ['s_peasantfemale_09_0.png','s_npc_merchant01_0.png']]
m={'date':'2026-10-13','character_id':'TRADE-NPC-LIQUI','status':'near-1to1-structure-independently-reviewed-style-open','style_pass':False,'native_production_pass':False,'runtimeVerified':False,'new_generation':False,'author_anatomy_claim':{'top_y':4,'lower_jaw_y':19,'actual_visible_chin_y':20,'neck_y':21,'bottom_y':37,'head_inclusive_rows':17,'remainder_inclusive_rows':17,'basis':'Author anatomy and independent actual PNG row inspection agree on chin20; conservative chin19 interpretation is 16:18','exclude_braid_and_neck_from_head':True},'technical':{'canvas':list(b.size),'alpha_bbox':list(b.getbbox()),'alpha_values':sorted(set(b.getchannel('A').getdata())),'opaque_colors':len({p for p in b.getdata() if p[3]}),'available_palette_colors':18,'operations':len(l['edits']),'unique_coordinates':len({(e['x'],e['y']) for e in l['edits']}),'net_changed_pixels':sum(x!=y for x,y in zip(start,b.getdata())),'rebuild_verified':True,'log_replay_verified':True,'v1_v2_unchanged':True},'sources':[{'path':str(p.relative_to(R)),'sha256':sha(p)} for p in sources],'outputs':[{'file':p.name,'sha256':sha(p)} for p in sorted(D.iterdir()) if p.is_file() and p.name!='manifest.json' and not p.name.startswith('QA-')]}
(D/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2));print(json.dumps(m['technical'],indent=2));print(sha(D/'liqui_native_1to1.png'))
