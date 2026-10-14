from pathlib import Path
import json,hashlib,datetime,sys
A=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod/Assets/CharacterDesigns/20261013/expressive/new_story_audit');E=A/'independent_seventh_new_character_actions_evidence';root=A.parents[4];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def record(slug,key,verdict,findings,required_revision=None,remaining_revisions=0,nonissues=None):
 p=E/(key+'_byte_audit.json');j=json.loads(p.read_text());j['verdict']=verdict;j['visual_review']={'actual_viewed':['raw','selected_transparent','true_light_composite','true_dark_composite'],'findings':findings,'required_revision':required_revision,'nonissues':nonissues or [],'remaining_revisions':remaining_revisions}
 p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');m=A/'independent_seventh_new_character_actions_20261014.json';d=json.loads(m.read_text());d['status']='generation_in_progress';d['pose_results']=[x for x in d['pose_results'] if x['pose_version']!=key];d['pose_results'].append({'character':slug,'pose_version':key,'verdict':verdict,'evidence':str(p.relative_to(root)),'evidence_sha256':sha(p),'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});m.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(p,sha(p))
if __name__=='__main__':record(**json.load(sys.stdin))
