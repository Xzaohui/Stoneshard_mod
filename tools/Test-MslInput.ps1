param([string]$InputFile = 'D:\SteamLibrary\steamapps\common\Stoneshard\vanilla.win')
$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskProbe = Join-Path $taskRoot 'tools\GameProbe\bin\Release\net10.0-windows\GameProbe.dll'
if (!(Test-Path -LiteralPath $taskProbe)) { throw 'Build GameProbe first. This check does not update game files.' }
dotnet $taskProbe $InputFile --require-msl-clean
if ($LASTEXITCODE) { throw 'Do not use this file as native MSL packaging input. Load the original vanilla.win again.' }
