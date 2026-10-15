#!/usr/bin/env python3
"""Read-only source, argument and full-return validation for this frozen batch."""
from pathlib import Path
from PIL import Image
import base64, hashlib, json

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def validate_sources(root, repo):
    data=json.loads((root/'sources/source_manifest.json').read_text())
    rows=data.get('items',data.get('sources',[])); assert rows
    checks=[]
    for item in rows:
        original=repo/item.get('original_path',item.get('source_path'))
        snapshot=root/item.get('snapshot_path',item.get('local_path'))
        assert sha(snapshot)==item['sha256'],snapshot
        derived=item.get('derived_from_sha256')
        if derived:
            assert sha(original)==derived
            src=Image.open(original).convert('RGBA');copy=Image.open(snapshot).convert('RGBA')
            expected=src.resize((src.width*8,src.height*8),Image.Resampling.NEAREST)
            assert copy.size==expected.size and copy.tobytes()==expected.tobytes()
        else: assert sha(original)==item['sha256'],original
        checks.append({'original':str(original.relative_to(repo)),'snapshot':str(snapshot.relative_to(root)),'sha256':item['sha256'],'original_sha256':sha(original),'derived_8x_NN':bool(derived),'original_and_snapshot_identical':not bool(derived),'verified':True})
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
        checks.append({'version':v,'full_prompt_and_actual_arguments_retained':True,'text_file_present':txt.exists(),'text_matches_argument':True if txt.exists() else None,'references':refs,'raw_tool_return_byte_identical':True,'raw_sha256':sha(raw),'return_sha256':sha(root/'tool_returns'/f'{v}.json')})
    assert len(list((root/'tool_returns').glob('portrait_v[12].json')))==2
    failure=root/'tool_returns/portrait_v2_validation_failure.json'
    if failure.exists():
        f=json.loads(failure.read_text());assert f['images_generated']==0 and len(f['request']['referenced_image_paths'])==6
    return checks
