param([switch]$Deploy, [switch]$RepairExistingEao, [string]$PackageCache)
$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskGame = 'D:\SteamLibrary\steamapps\common\Stoneshard'
Push-Location $taskRoot
try {
    $env:DOTNET_CLI_HOME = Join-Path $taskRoot 'tools\.dotnet-home'
    # Sparse code worktrees can reuse the main checkout's complete dependency
    # cache; tracked package metadata alone is not a restored NuGet package.
    $env:NUGET_PACKAGES = if ($PackageCache) { [IO.Path]::GetFullPath($PackageCache) } else { Join-Path $taskRoot 'tools\packages' }
    $env:MSBuildEnableWorkloadResolver = 'false'
    $env:DOTNET_SKIP_FIRST_TIME_EXPERIENCE = '1'
    $env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
    $taskMsl = Join-Path $taskGame 'msl'
    dotnet build src/EmbersAndOaths/EmbersAndOaths.csproj -c Release "-p:MslDir=$taskMsl" -p:NuGetAudit=false -v quiet
    if ($LASTEXITCODE) { throw 'Mod build failed.' }
    dotnet build tools/GameProbe/GameProbe.csproj -c Release "-p:MslDir=$taskMsl" -p:NuGetAudit=false -v quiet
    if ($LASTEXITCODE) { throw 'Probe build failed.' }
    $taskProbe = 'tools/GameProbe/bin/Release/net10.0-windows/GameProbe.dll'
    dotnet $taskProbe --pack src/EmbersAndOaths/bin/Release/net6.0-windows/EmbersAndOaths.dll src/EmbersAndOaths/Codes artifacts/EmbersAndOaths.sml
    if ($LASTEXITCODE) { throw 'SML packing/reader validation failed.' }
    $taskInput = Join-Path $taskGame 'data.win'
    $taskPatchCommand = if ($RepairExistingEao) { '--repair-eao' } else { '--patch' }
    $taskLastPath = Join-Path $taskRoot 'artifacts\direct-deployment.json'
    if (Test-Path -LiteralPath $taskLastPath) {
        $taskLast = Get-Content -LiteralPath $taskLastPath -Raw | ConvertFrom-Json
        if ((Get-FileHash -LiteralPath $taskInput -Algorithm SHA256).Hash -eq $taskLast.deployedDataSha256) {
            if ($taskLast.targetedRepair) { $taskPatchCommand = '--repair-eao' }
            else {
                $taskInput = $taskLast.preEaoInput
                if ((Get-FileHash -LiteralPath $taskInput -Algorithm SHA256).Hash -ne $taskLast.preEaoInputSha256) { throw 'Pre-EAO input backup changed.' }
            }
        }
        # If another tool changed data.win, use it as a new input. An existing EAO patch will be refused.
    }
    dotnet $taskProbe $taskInput $taskPatchCommand artifacts/EmbersAndOaths.sml artifacts/direct-data.win --direct
    if ($LASTEXITCODE) { throw 'Current combination patch verification failed; nothing deployed.' }
    dotnet $taskProbe artifacts/direct-data.win --test-eao-east
    if ($LASTEXITCODE) { throw 'East surface/native generation contracts failed; nothing deployed.' }
    dotnet $taskProbe artifacts/direct-data.win --test-eao-actions
    if ($LASTEXITCODE) { throw 'Compiled document handover/read-state tests failed; nothing deployed.' }
    dotnet $taskProbe artifacts/direct-data.win --test-eao-rooms
    if ($LASTEXITCODE) { throw 'Native annex room/transition checks failed; nothing deployed.' }
    dotnet $taskProbe artifacts/direct-data.win --test-eao-teleport
    if ($LASTEXITCODE) { throw 'Optional test teleport/native transition checks failed; nothing deployed.' }
    dotnet $taskProbe artifacts/direct-data.win --test-eao-story
    if ($LASTEXITCODE) { throw 'New story/retirement/scene checks failed; nothing deployed.' }
    dotnet $taskProbe artifacts/direct-data.win --test-eao-dev
    if ($LASTEXITCODE) { throw 'Developer mode and embedded HD2D checks failed; nothing deployed.' }
    Copy-Item -LiteralPath 'artifacts\offline-validation.json' -Destination 'artifacts\direct-validation.json'
    if ($Deploy) {
        & (Join-Path $PSScriptRoot 'Deploy-Mod.ps1') -ValidatedInput $taskInput
    } else { Write-Output 'Built and verified against the current combination. Run with -Deploy to update the current installation.' }
}
finally { Pop-Location }
