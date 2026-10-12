param([Parameter(Mandatory)][string]$BrokenData, [Parameter(Mandatory)][string]$FixedData)
$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskProbe = Join-Path $taskRoot 'tools/GameProbe/bin/Release/net10.0-windows/GameProbe.dll'
$taskBrokenOutput = @(& dotnet $taskProbe $BrokenData --assert-eao-struct-access 2>&1)
$taskBrokenExit = $LASTEXITCODE
if ($taskBrokenExit -eq 0 -or ($taskBrokenOutput -join "`n") -notmatch 'Courier Create coerces a struct receiver to an integer instance index') {
    throw 'The known broken bytecode was not rejected for the expected reason.'
}
$taskFixedOutput = @(& dotnet $taskProbe $FixedData --assert-eao-linkage 2>&1)
if ($LASTEXITCODE -ne 0) { throw ('Fixed resource validation failed: ' + ($taskFixedOutput -join "`n")) }
$taskResult = [ordered]@{
    date=(Get-Date -Format o)
    brokenDataSha256=(Get-FileHash -LiteralPath $BrokenData -Algorithm SHA256).Hash
    fixedDataSha256=(Get-FileHash -LiteralPath $FixedData -Algorithm SHA256).Hash
    brokenStructReceiverRejected=$true
    fixedSerializedResourcePassed=$true
    runtimeVerified=$false
}
$taskResult | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskRoot 'artifacts/struct-access-regression.json') -Encoding utf8NoBOM
$taskResult | ConvertTo-Json
