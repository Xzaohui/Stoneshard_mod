param([string]$GameDirectory = 'D:\SteamLibrary\steamapps\common\Stoneshard')
$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskEnvRoot = Join-Path $taskRoot 'test-env'
$taskOriginalUserData = 'C:\Users\83912\AppData\Local\StoneShard'
if (Get-Process -Name StoneShard -ErrorAction SilentlyContinue) {
    throw 'Game is running. Exit it before creating a consistent backup.'
}
foreach ($taskSource in @($GameDirectory, $taskOriginalUserData)) {
    if (!(Test-Path -LiteralPath $taskSource -PathType Container)) { throw "Missing source: $taskSource" }
    $taskLinks = @(Get-ChildItem -LiteralPath $taskSource -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint })
    if ($taskLinks.Count) { throw "Source has reparse points; review before copying: $taskSource" }
}
if (Test-Path -LiteralPath $taskEnvRoot) { throw 'Test environment already exists; refusing to overwrite it.' }
New-Item -ItemType Directory -Path $taskEnvRoot | Out-Null
$taskStamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$taskBackup = Join-Path $taskEnvRoot "backups\$taskStamp"
New-Item -ItemType Directory -Path $taskBackup | Out-Null
Copy-Item -LiteralPath $taskOriginalUserData -Destination (Join-Path $taskBackup 'formal-userdata') -Recurse
$taskBaselineGame = Join-Path $taskEnvRoot 'baseline\game'
$taskWorkGame = Join-Path $taskEnvRoot 'work\game'
$taskLauncher = Join-Path $taskEnvRoot 'work\launcher'
foreach ($taskDir in @($taskBaselineGame,$taskWorkGame,$taskLauncher,(Join-Path $taskEnvRoot 'userdata'),(Join-Path $taskEnvRoot 'manifests'))) {
    New-Item -ItemType Directory -Path $taskDir -Force | Out-Null
}
# Only required runtime dependencies, never launcher logs or personal data in the game copy.
$taskRuntimeFiles = Get-ChildItem -LiteralPath $GameDirectory -File | Where-Object {
    $_.Name -eq 'StoneShard.exe' -or $_.Name -eq 'options.ini' -or $_.Name -eq 'splash.png' -or
    $_.Extension -eq '.dll' -or $_.Name -match '^audiogroup\d+\.dat$'
}
foreach ($taskRuntimeFile in $taskRuntimeFiles) { Copy-Item -LiteralPath $taskRuntimeFile.FullName -Destination $taskBaselineGame }
Copy-Item -LiteralPath (Join-Path $GameDirectory 'fonts') -Destination $taskBaselineGame -Recurse
Copy-Item -LiteralPath (Join-Path $GameDirectory 'vanilla.win') -Destination (Join-Path $taskBaselineGame 'data.win')
Copy-Item -LiteralPath (Join-Path $GameDirectory 'vanilla.win') -Destination (Join-Path $taskBackup 'vanilla.win')
Copy-Item -LiteralPath (Join-Path $GameDirectory 'data.win') -Destination (Join-Path $taskBackup 'existing-mods-data.win')
Copy-Item -Path (Join-Path $taskBaselineGame '*') -Destination $taskWorkGame -Recurse
$taskMsl = Join-Path $GameDirectory 'msl'
foreach ($taskFile in (Get-ChildItem -LiteralPath $taskMsl -File | Where-Object { $_.Extension -in '.exe','.dll','.pdb','.txt' })) {
    Copy-Item -LiteralPath $taskFile.FullName -Destination $taskLauncher
}
foreach ($taskCulture in (Get-ChildItem -LiteralPath $taskMsl -Directory | Where-Object { $_.Name -match '^[a-z]{2}(-[A-Za-z]+)?$' })) {
    Copy-Item -LiteralPath $taskCulture.FullName -Destination $taskLauncher -Recurse
}
New-Item -ItemType Directory -Path (Join-Path $taskLauncher 'Mods'),(Join-Path $taskLauncher 'ModSources') | Out-Null
[IO.File]::WriteAllText((Join-Path $taskLauncher 'Settings.json'), '{"Language":"Chinese","EnableLogger":true,"EnabledMods":[]}', (New-Object System.Text.UTF8Encoding($false)))
$taskFingerprint = [ordered]@{ created=(Get-Date -Format o); baselineOrigin='User-confirmed original vanilla.win'; runtimeVerified=$false; launchAllowed=$false; formalGame=$GameDirectory; backup=$taskBackup; resources=@(); formalUserData=@() }
foreach ($taskName in 'vanilla.win','data.win','StoneShard.exe') {
    $taskFingerprint.resources += @{ name=$taskName; sha256=(Get-FileHash -LiteralPath (Join-Path $GameDirectory $taskName) -Algorithm SHA256).Hash }
}
foreach ($taskFile in (Get-ChildItem -LiteralPath $taskOriginalUserData -Recurse -File)) {
    $taskFingerprint.formalUserData += @{ relative=$taskFile.FullName.Substring($taskOriginalUserData.Length + 1); sha256=(Get-FileHash -LiteralPath $taskFile.FullName -Algorithm SHA256).Hash }
}
[IO.File]::WriteAllText((Join-Path $taskEnvRoot 'manifests\formal-before.json'), ($taskFingerprint | ConvertTo-Json -Depth 6), (New-Object System.Text.UTF8Encoding($false)))
Write-Output 'Prepared baseline, work copy, launcher and formal-data backup. Game launch remains blocked pending isolation verification.'
