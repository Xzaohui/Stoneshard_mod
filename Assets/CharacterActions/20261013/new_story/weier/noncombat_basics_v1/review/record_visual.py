from pathlib import Path
import json,sys
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';e=a/'independent_sixth_new_character_actions_evidence'
key,status,note=sys.argv[1:4];p=e/f'{key}_byte_audit.json';d=json.loads(p.read_text());d['verdict']=status;d['visual_note']=note;d['actual_viewed']=['raw','transparent','true_rgba_light','true_rgba_dark','mother_at_plan_gate'];d['revision_requested']=status=='hard_error_revision_needed';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
j=a/'independent_sixth_new_character_actions_20261014.json';jr=json.loads(j.read_text());jr['pose_reviews']=[x for x in jr['pose_reviews'] if x['pose_version']!=key]+[d];jr['selected_pose_count']=sum(x['verdict']=='pass' for x in jr['pose_reviews']);jr['status']='pose_review_in_progress';j.write_text(json.dumps(jr,ensure_ascii=False,indent=2)+'\n');print(key,status)
