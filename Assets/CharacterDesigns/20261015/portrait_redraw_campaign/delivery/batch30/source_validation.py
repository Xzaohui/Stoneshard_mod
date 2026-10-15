#!/usr/bin/env python3
"""Read-only source, argument and full-return validation for this frozen batch."""
from pathlib import Path
from PIL import Image
import base64, hashlib, json, subprocess

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def validate_sources(root, repo):
    data=json.loads((root/'sources/source_manifest.json').read_text())
    rows=data.get('items',data.get('sources',[])); assert rows
    checks=[]
    for item in rows:
        original_ref=item.get('original_path',item.get('source_path',item.get('source')))
        original=repo/original_ref
        snapshot=root/item.get('snapshot_path',item.get('local_path',item.get('snapshot')))
        assert sha(snapshot)==item['sha256'],snapshot
        derived=item.get('derived_from_sha256')
        if derived:
            assert sha(original)==derived
            src=Image.open(original).convert('RGBA');copy=Image.open(snapshot).convert('RGBA')
            expected=src.resize((src.width*8,src.height*8),Image.Resampling.NEAREST)
            assert copy.size==expected.size and copy.tobytes()==expected.tobytes()
        elif original_ref.startswith('git '):
            ref=original_ref.removeprefix('git ')
            b=subprocess.run(['git','show',ref],cwd=repo,check=True,capture_output=True).stdout
            assert hashlib.sha256(b).hexdigest()==item['sha256'],original_ref
        else: assert sha(original)==item['sha256'],original
        checks.append({'original':original_ref,'snapshot':str(snapshot.relative_to(root)),'sha256':item['sha256'],'original_sha256':item['sha256'] if original_ref.startswith('git ') else sha(original),'derived_8x_NN':bool(derived),'original_and_snapshot_identical':not bool(derived),'verified':True})
    return checks

def validate_prompts(root):
    checks=[]
    for v in ['portrait_v1','portrait_v2']:
        args=json.loads((root/'prompts'/f'{v}.json').read_text())
        assert isinstance(args['prompt'],str) and args['prompt'].strip()
        txt=root/'prompts'/f'{v}.txt'
        if txt.exists(): assert args['prompt'].strip()==txt.read_text().strip()
        assert args['transparent_background'] is True and 0<len(args['referenced_image_paths'])<=5
        refs=[]
        for path in args['referenced_image_paths']:
            ref=Path(path);assert ref.is_file() and ref.is_relative_to(root)
            refs.append({'path':ref.relative_to(root).as_posix(),'sha256':sha(ref)})
        ret=json.loads((root/'tool_returns'/f'{v}.json').read_text())
        raw=root/'raw'/f'{v}_raw_imagegen.png'
        assert raw.read_bytes()==base64.b64decode(ret['image_url'].split(',',1)[1])
        checks.append({'version':v,'full_prompt_and_actual_arguments_retained':True,'text_file_present':txt.exists(),'text_matches_argument':args['prompt']==txt.read_text() if txt.exists() else None,'text_matches_argument_ignoring_terminal_newline':args['prompt'].rstrip('\n')==txt.read_text().rstrip('\n') if txt.exists() else None,'references':refs,'raw_tool_return_byte_identical':True,'raw_sha256':sha(raw),'return_sha256':sha(root/'tool_returns'/f'{v}.json')})
    assert len(list((root/'tool_returns').glob('portrait_v[12].json')))==2
    rejection=root/'tool_returns/portrait_v2_validation_rejection.json'
    if rejection.exists():
        f=json.loads(rejection.read_text()); assert f['generation_started'] is False and f['image_generated'] is False
        preflight=json.loads((root/'prompts/portrait_v2_six_reference_preflight.json').read_text())
        assert len(preflight['referenced_image_paths'])==6
    failure=root/'tool_returns/portrait_v2_validation_failure.json'
    if failure.exists():
        f=json.loads(failure.read_text());assert f['images_generated']==0 and len(f['request']['referenced_image_paths'])==6
    rejected=root/'tool_returns/portrait_v2_validation_error.json'
    if rejected.exists():
        f=json.loads(rejected.read_text()); assert f['output_image_returned'] is False
        attempt=json.loads((root/f['submitted_arguments']).read_text()); assert len(attempt['referenced_image_paths'])==6
    rejected=root/'tool_returns/portrait_v2_rejected_6ref.json'
    if rejected.exists():
        f=json.loads(rejected.read_text()); assert f['successful_generation'] is False
        attempt=json.loads((root/'prompts/portrait_v2_rejected_6ref.json').read_text()); assert len(attempt['referenced_image_paths'])==6
    for retname,argname,key in [('portrait_v2_rejected_request_error.json','portrait_v2_rejected_request.json','generated_image'),('portrait_v2_argument_validation_error.json','portrait_v2_rejected_before_generation.json','image_generated')]:
        rejected=root/'tool_returns'/retname
        if rejected.exists():
            rejected_data=json.loads(rejected.read_text());assert rejected_data[key] is False
            rejected_args=json.loads((root/'prompts'/argname).read_text());assert len(rejected_args['referenced_image_paths'])==6
    return checks
