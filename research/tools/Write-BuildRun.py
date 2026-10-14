"""S170: record the local build run (candidate only, no deployment).

Reads the artifacts produced by tools/Build-Mod.ps1 (package, candidate patch,
validation reports) and writes the run registry. Also states the new
candidate-versus-deployed relationship so the implementation snapshot page can
report it truthfully.
"""
from pathlib import Path
import hashlib, json, datetime
ROOT = Path(__file__).resolve().parents[2]; R = ROOT / 'research'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while True:
            b = f.read(1 << 20)
            if not b: break
            h.update(b)
    return h.hexdigest().upper()
def mtime(p): return datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
art = ROOT / 'artifacts'
sml, cand = art / 'EmbersAndOaths.sml', art / 'direct-data.win'
val = json.loads((art / 'direct-validation.json').read_text(encoding='utf-8-sig'))
dep = json.loads((art / 'direct-deployment.json').read_text(encoding='utf-8-sig'))
msl = Path('D:/SteamLibrary/steamapps/common/Stoneshard/msl/Mods/EmbersAndOaths.sml')
run = dict(date=datetime.date.today().isoformat(),
           scope='Local build snapshot from current combination; deployed relationship verified by hashes. Runtime observations are recorded separately.',
           command='tools/Build-Mod.ps1（不带 -Deploy）',
           built_at=dict(package=mtime(sml), candidate=mtime(cand)),
           package=dict(path='artifacts/EmbersAndOaths.sml', bytes=sml.stat().st_size, sha256=sha(sml)),
           candidate=dict(path='artifacts/direct-data.win', bytes=cand.stat().st_size, sha256=sha(cand)),
           input_sha256=val['inputSha256'], stage=val['stage'], mod_version=val['modVersion'],
           checks=dict(mouseDialogueWired=val['mouseDialogueWired'], nativeNpcInherited=val['nativeNpcInherited'],
                       nativeDialogueFlowRegistered=val['nativeDialogueFlowRegistered'],
                       customInputLocksRemoved=val['customInputLocksRemoved'],
                       originalCodeUnchangedExceptEao=val['originalCodeUnchangedExceptEao'],
                       eaoFunctionLinkageChecked=val['eaoFunctionLinkageChecked'],
                       duplicatePatchRefused=val['duplicatePatchRefused'],
                       originalIdentityPreserved=val['originalIdentityPreserved'],
                       originalCodeEntries=val['originalCodeEntries'],
                       runtimeVerified=val['runtimeVerified']),
           deployed=dict(package_sha256=dep['packageSha256'], msl_copy_sha256=sha(msl) if msl.exists() else '',
                         msl_copy_matches_candidate=bool(msl.exists() and sha(msl) == sha(sml))),
           suites=['compiledCallbackScenarios', 'rooms', 'teleport', 'story'] + (['dev'] if (art / 'dev-validation.json').exists() else []),
           deployed_this_run=sha(cand) == dep['deployedDataSha256'] and sha(sml) == dep['packageSha256'])
(R / 'build-run.json').write_text(json.dumps(run, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(package=run['package']['sha256'][:16], candidate=run['candidate']['sha256'][:16],
                      deployed=run['deployed']['package_sha256'][:16],
                      matches=run['deployed']['msl_copy_matches_candidate'],
                      runtime=run['checks']['runtimeVerified']), ensure_ascii=False))
