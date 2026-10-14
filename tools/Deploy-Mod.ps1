param([Parameter(Mandatory)][string]$ValidatedInput, [switch]$PackageOnly)
$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskGame = 'D:\SteamLibrary\steamapps\common\Stoneshard'
$taskMsl = Join-Path $taskGame 'msl'
$taskMods = Join-Path $taskMsl 'Mods'
$taskData = Join-Path $taskGame 'data.win'
$taskSettings = Join-Path $taskMsl 'Settings.json'
$taskPackage = Join-Path $taskRoot 'artifacts\EmbersAndOaths.sml'
$taskCandidate = Join-Path $taskRoot 'artifacts\direct-data.win'
$taskDestination = Join-Path $taskMods 'EmbersAndOaths.sml'
$taskUserData = 'C:\Users\83912\AppData\Local\StoneShard'
$taskReport = Get-Content -LiteralPath (Join-Path $taskRoot 'artifacts\direct-validation.json') -Raw | ConvertFrom-Json
if ([version]$taskReport.modVersion -ge [version]'0.1.6') {
    $taskActions = Get-Content -LiteralPath (Join-Path $taskRoot 'artifacts\document-action-validation.json') -Raw | ConvertFrom-Json
    if ($taskActions.inputSha256 -ne $taskReport.outputSha256 -or @($taskActions.compiledCallbackScenarios).Count -lt 11) {
        throw 'Document transaction/read-state tests do not match this candidate; nothing deployed.'
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.2.0') {
    $taskRooms = Get-Content -LiteralPath (Join-Path $taskRoot 'artifacts\room-validation.json') -Raw | ConvertFrom-Json
    if ($taskRooms.inputSha256 -ne $taskReport.outputSha256 -or @($taskRooms.checks).Count -lt 7 -or @($taskActions.compiledCallbackScenarios).Count -lt 17) {
        throw 'MQ02 room/action checks do not match this candidate; nothing deployed.'
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.2.1') {
    $taskTeleport = Get-Content -LiteralPath (Join-Path $taskRoot 'artifacts\test-teleport-validation.json') -Raw | ConvertFrom-Json
    if ($taskTeleport.inputSha256 -ne $taskReport.outputSha256 -or @($taskTeleport.checks).Count -lt 5 -or @($taskActions.compiledCallbackScenarios).Count -lt 25) {
        throw 'Optional teleport checks do not match this candidate; nothing deployed.'
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.2.3' -and @($taskActions.compiledCallbackScenarios).Count -lt 30) {
    throw 'Native placeholder landing/recovery regression tests are missing; nothing deployed.'
}
if ([version]$taskReport.modVersion -ge [version]'0.2.4' -and (@($taskActions.compiledCallbackScenarios).Count -lt 33 -or @($taskRooms.checks).Count -lt 8)) {
    throw 'Visible Customs House entrance/native lock checks are missing; nothing deployed.'
}
if ([version]$taskReport.modVersion -ge [version]'0.3.0') {
    $taskStory = Get-Content -LiteralPath (Join-Path $taskRoot 'artifacts\story-validation.json') -Raw | ConvertFrom-Json
    $taskStoryMinimum = if ([version]$taskReport.modVersion -ge [version]'0.3.1') { 21 } else { 19 }
    if ($taskStory.inputSha256 -ne $taskReport.outputSha256 -or @($taskStory.checks).Count -lt $taskStoryMinimum -or @($taskActions.compiledCallbackScenarios | Where-Object { $_ -like 'night-*' }).Count -lt 10) {
        throw 'Story retirement/branch/scene checks do not match this candidate; nothing deployed.'
    }
}
if (Get-Process -Name ModShardLauncher -ErrorAction SilentlyContinue) { throw 'MSL is running; close it before updating. No process was stopped.' }
if ([version]$taskReport.modVersion -ge [version]'0.3.1') {
    $taskDev = Get-Content -LiteralPath (Join-Path $taskRoot 'artifacts/dev-validation.json') -Raw | ConvertFrom-Json
    if ($taskDev.inputSha256 -ne $taskReport.outputSha256 -or @($taskDev.checks).Count -lt 59) { throw 'Developer/art checks do not match this candidate.' }
    if ([version]$taskReport.modVersion -ge [version]'0.3.3') {
        foreach ($taskRequired in @('dev-six-scene-native-cycle-with-n2-arrival-tags','dev-n2-cycle-preserves-first-origin','r_eao_n2_camp-art-matches-serialized-native-collision-cells','r_eao_n2_winch-art-matches-serialized-native-collision-cells','r_eao_n2_side-art-matches-serialized-native-collision-cells')) {
            if ($taskRequired -notin $taskDev.checks) { throw ('Missing N2 scene/art check: ' + $taskRequired) }
        }
    }
}
if (!$PackageOnly -and (Get-Process -Name StoneShard -ErrorAction SilentlyContinue)) { throw 'Game is running; close it before updating data.win. No process was stopped.' }
function Test-TaskNoLink([string]$Path) {
    $taskAbsolute = [IO.Path]::GetFullPath($Path)
    for ($taskPart = $taskAbsolute; $taskPart; $taskPart = Split-Path $taskPart -Parent) {
        if ((Test-Path -LiteralPath $taskPart) -and ((Get-Item -LiteralPath $taskPart -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Deployment path is a reparse point.' }
    }
}
foreach ($taskPath in @($taskGame,$taskMods,$taskData,$taskSettings,$taskPackage,$taskCandidate,$taskDestination,$taskUserData,$ValidatedInput)) { Test-TaskNoLink $taskPath }
if ((Get-FileHash -LiteralPath $taskPackage -Algorithm SHA256).Hash -ne $taskReport.packageSha256 -or (Get-FileHash -LiteralPath $taskCandidate -Algorithm SHA256).Hash -ne $taskReport.outputSha256 -or (Get-FileHash -LiteralPath $ValidatedInput -Algorithm SHA256).Hash -ne $taskReport.inputSha256) { throw 'Validated input or artifact changed.' }
$taskConfiguration = Get-Content -LiteralPath $taskSettings -Raw | ConvertFrom-Json
if ($null -eq $taskConfiguration.EnableMods) { throw 'Unexpected local MSL settings schema; nothing deployed.' }
$taskOldHash = (Get-FileHash -LiteralPath $taskData -Algorithm SHA256).Hash
if ($PackageOnly) {
    $taskPackageBackup = Join-Path $taskRoot ('backups\package-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
    Test-TaskNoLink $taskPackageBackup
    New-Item -ItemType Directory -Path $taskPackageBackup | Out-Null
    Copy-Item -LiteralPath $taskSettings -Destination (Join-Path $taskPackageBackup 'Settings.json')
    if (Test-Path -LiteralPath $taskDestination) { Copy-Item -LiteralPath $taskDestination -Destination (Join-Path $taskPackageBackup 'EmbersAndOaths.sml') }
    Copy-Item -LiteralPath $taskPackage -Destination $taskDestination
    $taskConfiguration.EnableMods = @($taskConfiguration.EnableMods | Where-Object { $_ -ne 'EmbersAndOaths' }) + @('EmbersAndOaths')
    [IO.File]::WriteAllText($taskSettings, ($taskConfiguration | ConvertTo-Json -Depth 10), (New-Object System.Text.UTF8Encoding($false)))
    if ((Get-FileHash -LiteralPath $taskDestination -Algorithm SHA256).Hash -ne $taskReport.packageSha256 -or (Get-FileHash -LiteralPath $taskData -Algorithm SHA256).Hash -ne $taskOldHash) { throw 'Package deployment verification failed.' }
    $taskPackageResult = [ordered]@{ date=(Get-Date -Format o); mode='package only while game running'; package=$taskDestination; packageSha256=$taskReport.packageSha256; settingsBackup=$taskPackageBackup; mslEnabled=$true; gameResourceUpdated=$false; gameDataUnchanged=$true; runtimeVerified=$false }
    [IO.File]::WriteAllText((Join-Path $taskRoot 'artifacts\package-deployment.json'), ($taskPackageResult | ConvertTo-Json -Depth 5), (New-Object System.Text.UTF8Encoding($false)))
    $taskPackageResult | ConvertTo-Json -Depth 5
    return
}
$taskLastFile = Join-Path $taskRoot 'artifacts\direct-deployment.json'
if ($taskOldHash -ne $taskReport.inputSha256) {
    if (!(Test-Path -LiteralPath $taskLastFile)) { throw 'Current data does not match the validated input.' }
    $taskLast = Get-Content -LiteralPath $taskLastFile -Raw | ConvertFrom-Json
    if ($taskOldHash -ne $taskLast.deployedDataSha256 -or [IO.Path]::GetFullPath($ValidatedInput) -ne [IO.Path]::GetFullPath($taskLast.preEaoInput)) { throw 'Current data changed outside this deployment workflow.' }
}
$taskBackup = Join-Path $taskRoot ('backups\direct-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
Test-TaskNoLink $taskBackup
New-Item -ItemType Directory -Path $taskBackup | Out-Null
Copy-Item -LiteralPath $taskData -Destination (Join-Path $taskBackup 'data.win')
Copy-Item -LiteralPath $taskSettings -Destination (Join-Path $taskBackup 'Settings.json')
if (Test-Path -LiteralPath $taskDestination) { Copy-Item -LiteralPath $taskDestination -Destination (Join-Path $taskBackup 'EmbersAndOaths.sml') }
$taskUserLinks = @(Get-ChildItem -LiteralPath $taskUserData -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint })
if ($taskUserLinks.Count) { throw 'User data contains links; backup stopped.' }
Copy-Item -LiteralPath $taskUserData -Destination (Join-Path $taskBackup 'userdata') -Recurse
$taskUserSnapshot = @(Get-ChildItem -LiteralPath $taskUserData -File -Recurse | ForEach-Object {
    $taskRelative = $_.FullName.Substring($taskUserData.Length + 1)
    $taskHash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
    if ((Get-FileHash -LiteralPath (Join-Path (Join-Path $taskBackup 'userdata') $taskRelative) -Algorithm SHA256).Hash -ne $taskHash) { throw 'User-data backup mismatch.' }
    @{ relative=$taskRelative; sha256=$taskHash }
})
if ((Get-FileHash -LiteralPath (Join-Path $taskBackup 'data.win') -Algorithm SHA256).Hash -ne $taskOldHash) { throw 'Game-data backup mismatch.' }
$taskVanillaHash = (Get-FileHash -LiteralPath (Join-Path $taskGame 'vanilla.win') -Algorithm SHA256).Hash
$taskPreEaoInput = if ($taskReport.targetedRepair) { $null } elseif ($taskOldHash -eq $taskReport.inputSha256) { Join-Path $taskBackup 'data.win' } else { [IO.Path]::GetFullPath($ValidatedInput) }
$taskBeforeJson = @{ created=(Get-Date -Format o); game=$taskGame; beforeDataSha256=$taskOldHash; vanillaSha256=$taskVanillaHash; userFiles=$taskUserSnapshot } | ConvertTo-Json -Depth 5
[IO.File]::WriteAllText((Join-Path $taskBackup 'before.json'), $taskBeforeJson, (New-Object System.Text.UTF8Encoding($false)))
# Copy into the destination volume and hash before replacing the game resource.
$taskPending = Join-Path $taskGame 'data.win.eao-pending'
Test-TaskNoLink $taskPending
if (Test-Path -LiteralPath $taskPending) { throw 'Pending deployment file exists; inspect it before retrying.' }
Copy-Item -LiteralPath $taskCandidate -Destination $taskPending
if ((Get-FileHash -LiteralPath $taskPending -Algorithm SHA256).Hash -ne $taskReport.outputSha256 -or (Get-FileHash -LiteralPath $taskData -Algorithm SHA256).Hash -ne $taskOldHash) { throw 'Deployment race or staged file mismatch.' }
Copy-Item -LiteralPath $taskPackage -Destination $taskDestination
[IO.File]::Move($taskPending, $taskData, $true)
# Local MSL identifies its settings entries by package filename, not the display name.
$taskConfiguration.EnableMods = @($taskConfiguration.EnableMods | Where-Object { $_ -ne 'EmbersAndOaths' }) + @('EmbersAndOaths')
[IO.File]::WriteAllText($taskSettings, ($taskConfiguration | ConvertTo-Json -Depth 10), (New-Object System.Text.UTF8Encoding($false)))
if ((Get-FileHash -LiteralPath $taskData -Algorithm SHA256).Hash -ne $taskReport.outputSha256 -or (Get-FileHash -LiteralPath $taskDestination -Algorithm SHA256).Hash -ne $taskReport.packageSha256) { throw 'Deployment verification failed.' }
if ((Get-FileHash -LiteralPath (Join-Path $taskGame 'vanilla.win') -Algorithm SHA256).Hash -ne $taskVanillaHash) { throw 'Original vanilla changed externally.' }
foreach ($taskEntry in $taskUserSnapshot) {
    if ((Get-FileHash -LiteralPath (Join-Path $taskUserData $taskEntry.relative) -Algorithm SHA256).Hash -ne $taskEntry.sha256) { throw 'User file changed during deployment; investigate without restoring it.' }
}
if (@(Get-ChildItem -LiteralPath $taskUserData -Recurse -File).Count -ne $taskUserSnapshot.Count) { throw 'User file count changed during deployment.' }
$taskResult = [ordered]@{ date=(Get-Date -Format o); mode='current installation, no isolation'; game=$taskGame; package=$taskDestination; backup=$taskBackup; targetedRepair=[bool]$taskReport.targetedRepair; repairSourceData=if ($taskReport.targetedRepair) { Join-Path $taskBackup 'data.win' } else { $null }; preEaoInput=$taskPreEaoInput; preEaoInputSha256=if ($taskPreEaoInput) { $taskReport.inputSha256 } else { $null }; deployedDataSha256=$taskReport.outputSha256; packageSha256=$taskReport.packageSha256; vanillaUnchanged=$true; userFilesUnchanged=$true; userFilesChecked=$taskUserSnapshot.Count; runtimeVerified=$false }
[IO.File]::WriteAllText($taskLastFile, ($taskResult | ConvertTo-Json -Depth 5), (New-Object System.Text.UTF8Encoding($false)))
$taskResult | ConvertTo-Json -Depth 5
