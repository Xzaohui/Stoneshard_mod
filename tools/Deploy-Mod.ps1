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
if ([version]$taskReport.modVersion -ge [version]'0.3.5') {
    foreach ($taskRequired in @('scene-exterior-serialized-collision-matches-independent-footprints','scene-exterior-all-floor-cells-connected','scene-exterior-arrival-markers-before-native-player','scene-exterior-home-restores-native-world-return','scene-assembly-no-quest-reward-or-direct-room-writes')) {
        if ($taskRequired -notin $taskDev.checks) { throw ('Missing native scene assembly check: ' + $taskRequired) }
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.6') {
    foreach ($taskRequired in @('dev-panel-localized-chinese-and-english','scene-door-art-aligns-native-origin-and-retains-highlight','scene-quarry-arrival-clear-of-return-door-with-four-walkable-neighbors')) {
        if ($taskRequired -notin $taskDev.checks) { throw ('Missing 0.3.6 scene/observer check: ' + $taskRequired) }
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.7') {
    foreach ($taskRequired in @('scene-door-centred-interaction-anchor-reuses-native-pixels-o_eao_site_winch_back','scene-door-centred-interaction-anchor-reuses-native-pixels-o_eao_site_canal_back','scene-door-centred-interaction-anchor-reuses-native-pixels-o_eao_site_door_winch')) {
        if ($taskRequired -notin $taskDev.checks) { throw ('Missing 0.3.7 native door anchor check: ' + $taskRequired) }
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.8') {
    $taskArtCountCheck=if([version]$taskReport.modVersion -ge [version]'0.3.12'){'hd2d-fifty-one-native-sprites'}else{'hd2d-forty-eight-native-sprites'}
    foreach ($taskRequired in @($taskArtCountCheck,'n2-seven-doorway-stamps-below-characters','n2-doorway-native-interaction-and-contextual-label-o_eao_site_winch_back','n2-doorway-stamp-in-floor-pass-o_eao_site_canal_back')) {
        if ($taskRequired -notin $taskDev.checks) { throw ('Missing 0.3.8 interior style check: ' + $taskRequired) }
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.9') {
    foreach ($taskRequired in @('n2-architectural-stamps-use-background-depth','n2-winch-whole-basin-water-contract','n2-bedroll-floor-depth-and-sprite-camp_bedroll_a','n2-bedroll-floor-depth-and-sprite-side_bedroll')) {
        if ($taskRequired -notin $taskDev.checks) { throw ('Missing 0.3.9 basin/cloth check: ' + $taskRequired) }
    }
    $taskWater = Get-Content -LiteralPath (Join-Path $taskRoot 'artifacts/n2-water-style-validation.json') -Raw | ConvertFrom-Json
    $taskWaterManifest = (Get-FileHash -LiteralPath (Join-Path $taskRoot 'src/Art/native-n2-hd2d-v1/manifest.json') -Algorithm SHA256).Hash
    if (!$taskWater.passed -or $taskWater.manifestSha256 -ne $taskWaterManifest) { throw 'Basin pixels do not match the checked art manifest.' }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.10') {
    foreach ($taskRequired in @('n2-doorway-hit-rectangle-matches-opaque-art-bounds','n2-doorway-hit-shares-art-with-clickable-right-flap','n2-doorway-hit-keeps-native-grid-and-input-o_eao_site_winch_back','n2-doorway-hit-keeps-native-grid-and-input-o_eao_site_canal_back')) {
        if ($taskRequired -notin $taskDev.checks) { throw ('Missing 0.3.10 doorway hit check: ' + $taskRequired) }
    }
    if (@($taskDev.checks | Where-Object { $_ -like 'n2-doorway-hit-keeps-native-grid-and-input-*' }).Count -ne 7) { throw 'All seven N2 doorway masks must be checked.' }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.12') {
    if (@($taskDev.checks | Where-Object { $_ -like 'n1-doorway-keeps-native-grid-lock-and-input-*' }).Count -ne 5 -or
        @($taskDev.checks | Where-Object { $_ -like 'n1-doorway-hit-matches-embedded-opaque-bounds-*' }).Count -ne 3 -or
        'n1-doorway-art-below-player-floor-depth' -notin $taskDev.checks) { throw 'N1 doorway art/input checks do not match all five doors.' }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.13') {
    foreach ($taskN1Room in @('r_eao_n1_yard','r_eao_n1_bellhouse','r_eao_n1_underpass')) {
        foreach ($taskN1Layer in @('floor','structure','foreground')) {
            $taskRequired = 'n1-surface-embedded-' + $taskN1Layer + '-matches-native-collision-' + $taskN1Room
            if ($taskRequired -notin $taskDev.checks) { throw ('Missing N1 surface/collision check: ' + $taskRequired) }
        }
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.14') {
    foreach ($taskN1Room in @('r_eao_n1_yard','r_eao_n1_bellhouse','r_eao_n1_underpass')) {
        $taskRequired = 'n1-architecture-floor-preserved-' + $taskN1Room
        if ($taskRequired -notin $taskDev.checks) { throw ('Missing unchanged N1 floor check: ' + $taskRequired) }
    }
    foreach ($taskRequired in @('n1-architecture-two-tile-north-walls-r_eao_n1_bellhouse','n1-architecture-two-tile-north-walls-r_eao_n1_underpass','n1-architecture-drain-backing-flat-no-old-water-fragments')) {
        if ($taskRequired -notin $taskDev.checks) { throw ('Missing N1 architecture check: ' + $taskRequired) }
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.15') {
    $taskEast = Get-Content -LiteralPath (Join-Path $taskRoot 'artifacts/east-surface-validation.json') -Raw | ConvertFrom-Json
    if ($taskEast.inputSha256 -ne $taskReport.outputSha256) { throw 'East surface checks do not match this candidate.' }
    foreach ($taskRequired in @('east-surface-native-ninety-by-ninety-geography','east-surface-legacy-exterior-and-exit-retained','east-surface-cache-hook-updates-task-room-on-repair','east-surface-extension-guard-uses-dimensions-not-recycled-handle','east-surface-all-native-edge-arrivals-and-building-returns-connected-in-authored-geometry')) {
        if ($taskRequired -notin $taskEast.checks) { throw ('Missing east surface check: ' + $taskRequired) }
    }
    foreach ($taskRequired in @('east-building-return-persisted-source-r_eao_n2_world','east-building-return-persisted-source-missing','east-building-failed-or-pending-door-keeps-origin')) {
        if ($taskRequired -notin $taskActions.compiledCallbackScenarios) { throw ('Missing east building return scenario: ' + $taskRequired) }
    }
    if ([version]$taskReport.modVersion -ge [version]'0.3.16') {
        $taskMap = Get-Content -LiteralPath (Join-Path $taskRoot 'artifacts/east-map-preservation.json') -Raw | ConvertFrom-Json
        if (!$taskMap.result.passed -or $taskMap.inputSha256 -ne $taskReport.inputSha256 -or $taskMap.candidateSha256 -ne $taskReport.outputSha256) { throw 'Original map preservation does not match input/candidate.' }
        foreach ($taskRequired in @('east-map-native-batches-updated-before-cache-creation','east-map-road-uses-native-neighbor-frame-and-paper-pair','east-map-extension-does-not-reroll-or-write-character-position')) {
            if ($taskRequired -notin $taskEast.checks) { throw ('Missing east map rendering check: ' + $taskRequired) }
        }
    }
    if ([version]$taskReport.modVersion -ge [version]'0.3.17') {
        $taskRegion = Get-Content -LiteralPath (Join-Path $taskRoot 'artifacts/east-region-validation.json') -Raw | ConvertFrom-Json
        if ($taskRegion.inputSha256 -ne $taskReport.outputSha256) { throw 'East region checks do not match candidate.' }
        foreach ($taskRequired in @('east-region-compiled-nineteen-rows-match-approved-layout','east-region-all-planned-ground-connected-to-west-entry','east-region-rebuilds-native-buffers-and-retains-original-weights','east-region-native-fog-paper-and-path-weight-order-retained','east-region-no-rng-consumption-save-write-or-live-player-relocation')) {
            if ($taskRequired -notin $taskRegion.checks) { throw ('Missing east region check: ' + $taskRequired) }
        }
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.18') {
    foreach ($taskRequired in @('dev-warp-default-off-cancel-and-malformed-coordinate-noop','dev-warp-coordinate-combat-escape-preserves-source-until-saver','dev-warp-failed-transition-does-not-record-origin','dev-warp-shift-return-preserves-first-room-world-and-local-position','dev-warp-no-origin-lock-dungeon-and-disabled-return-gates')) {
        if ($taskRequired -notin $taskActions.compiledCallbackScenarios) { throw ('Missing developer teleport scenario: ' + $taskRequired) }
    }
    if ('dev-f8-validated-coordinate-modal-and-shift-return' -notin $taskDev.checks -or 'dev-f8-single-modifier-route-keeps-steam-f12-free' -notin $taskDev.checks) { throw 'Developer teleport binding/input checks are missing.' }
}
if (!$PackageOnly -and (Get-Process -Name StoneShard -ErrorAction SilentlyContinue)) { throw 'Game is running; close it before updating data.win. No process was stopped.' }
if ([version]$taskReport.modVersion -ge [version]'0.3.19') {
    foreach ($taskRequired in @('map-arrival-rejects-swimming-even-when-native-astar-is-open','map-all-water-target-returns-without-spawning-a-swimmer')) {
        if ($taskRequired -notin $taskActions.compiledCallbackScenarios) { throw ('Missing dry arrival scenario: ' + $taskRequired) }
    }
    if ('dev-warp-observer-survives-owned-new-player-and-resets-on-disable' -notin $taskDev.checks -or 'east-region-vertical-river-uses-east-west-walking-bridge' -notin $taskRegion.checks) { throw 'Developer warp continuity or bridge orientation checks are missing.' }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.20') {
    foreach ($taskRequired in @('map-arrival-waits-for-native-water-markers-abstract','map-arrival-waits-for-native-water-markers-rewind')) {
        if ($taskRequired -notin $taskActions.compiledCallbackScenarios) { throw ('Missing native water initialization scenario: ' + $taskRequired) }
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.21') {
    foreach ($taskRequired in @('east-region-unmatched-coast-reconstructs-four-corners','east-region-native-ground-details-in-normal-and-paper-batches','east-region-native-decal-stays-within-cell-s_globalmap_steppedecals','east-region-native-decal-stays-within-cell-s_globalmap_pinedecals01','east-region-deterministic-decal-variation-and-steppe-bridge-palette')) {
        if ($taskRequired -notin $taskRegion.checks) { throw ('Missing east map style check: ' + $taskRequired) }
    }
}
if ([version]$taskReport.modVersion -ge [version]'0.3.22') {
    foreach ($taskRequired in @('dev-map-focused-left-state-and-owned-user10-registered','dev-map-disable-restores-native-callback-and-only-owned-left-state')) {
        if ($taskRequired -notin $taskDev.checks) { throw ('Missing developer map registration check: ' + $taskRequired) }
    }
}
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
# PS 5.1 (.NET Framework) has no three-argument File.Move overwrite; Copy
# overwrites and the pending stage is verified again right after (S167 fix).
[IO.File]::Copy($taskPending, $taskData, $true)
Remove-Item -LiteralPath $taskPending
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
