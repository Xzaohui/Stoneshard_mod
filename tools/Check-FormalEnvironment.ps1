param()
$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskSnapshot = Get-Content -LiteralPath (Join-Path $taskRoot 'test-env\manifests\formal-before.json') -Raw | ConvertFrom-Json
$taskUserRoot = 'C:\Users\83912\AppData\Local\StoneShard'
$taskProblems = [Collections.Generic.List[string]]::new()
foreach ($taskEntry in $taskSnapshot.resources) {
    if ((Get-FileHash -LiteralPath (Join-Path $taskSnapshot.formalGame $taskEntry.name) -Algorithm SHA256).Hash -ne $taskEntry.sha256) { $taskProblems.Add('Formal game resource changed: ' + $taskEntry.name) }
}
$taskExpected = @{}
foreach ($taskEntry in $taskSnapshot.formalUserData) {
    $taskExpected[$taskEntry.relative] = $true
    $taskPath = Join-Path $taskUserRoot $taskEntry.relative
    if (!(Test-Path -LiteralPath $taskPath -PathType Leaf)) { $taskProblems.Add('Formal user file missing.') ; continue }
    if ((Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash -ne $taskEntry.sha256) { $taskProblems.Add('Formal user file changed.') }
    $taskBackupFile = Join-Path (Join-Path $taskSnapshot.backup 'formal-userdata') $taskEntry.relative
    if ((Get-FileHash -LiteralPath $taskBackupFile -Algorithm SHA256).Hash -ne $taskEntry.sha256) { $taskProblems.Add('Backup does not match original snapshot.') }
}
foreach ($taskFile in (Get-ChildItem -LiteralPath $taskUserRoot -Recurse -File)) {
    $taskRelative = $taskFile.FullName.Substring($taskUserRoot.Length + 1)
    if (!$taskExpected.ContainsKey($taskRelative)) { $taskProblems.Add('New formal user file appeared.') }
}
$taskReport = [ordered]@{ checked=(Get-Date -Format o); gameResourcesChecked=$taskSnapshot.resources.Count; userFilesChecked=$taskSnapshot.formalUserData.Count; backupMatchesSnapshot=($taskProblems.Count -eq 0); formalFilesUnchanged=($taskProblems.Count -eq 0); errors=@($taskProblems) }
$taskReport | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $taskRoot 'test-env\manifests\formal-after.json') -Encoding utf8NoBOM
$taskReport | ConvertTo-Json -Depth 4
if ($taskProblems.Count) { throw 'Formal environment check failed. Do not automatically restore files; investigate external changes first.' }
