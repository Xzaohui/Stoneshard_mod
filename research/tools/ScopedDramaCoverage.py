"""Explicit admission for authored S80/S81 sources; no blanket allowance for new cities."""
import json
def matching_additional_source(root,q):
 specmap={'SKO':('skonfert','S80'),'YOS':('yostwayne','S80'),'DEN':('denbrie','S81'),'MNS':('mannshire','S81'),'EED':('eeders','S82'),'FOR':('forholt','S82'),'OSB':('osbrook','S83'),'RAT':('ratten','S83'),'KOR':('korde','S84'),'PAS':('passgate','S84'),'ASH':('ashcare','S86'),'HIG':('highland','S86')}
 pair=specmap.get(q['city'])
 if not pair:return False
 slug,revision=pair
 source='research/'+slug+'-drama.json'
 if q.get('dramatic_source')!=source or q.get('dramatic_revision')!=revision:return False
 data=json.loads((root/source).read_text(encoding='utf-8'))
 expected={'CM-'+q['city']}|{f"CS-{q['city']}-{i:02}" for i in range(1,4)}
 if set(data['quests'])!=expected or q['id'] not in expected:return False
 spec=data['quests'][q['id']]
 return all(q.get(mk)==spec[sk] for sk,mk in [('scenes','dramatic_scenes'),('followups','dramatic_followups'),('route_guards','dramatic_guards'),('exceptions','dramatic_exceptions')])
