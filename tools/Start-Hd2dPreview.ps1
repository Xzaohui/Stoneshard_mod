param([int]$Port = 6794)
$ErrorActionPreference = 'Stop'
if ($Port -lt 1024 -or $Port -gt 65535) { throw 'Invalid local preview port' }
$artProjectRoot = Split-Path -Parent $PSScriptRoot
$artPreviewRoot = Join-Path $artProjectRoot 'src/Art/hd2d_26x26_20261013'
$artPreviewUrl = "http://127.0.0.1:$Port/batches/R01-streets-v1/preview.html"
$artRecordPath = Join-Path $artProjectRoot "artifacts/hd2d-preview-$Port.json"
if (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue) {
    if (-not (Test-Path -LiteralPath $artRecordPath)) { throw 'Port already used by an unowned process' }
    $artPrior = Get-Content -Raw -LiteralPath $artRecordPath | ConvertFrom-Json
    $artExisting = Get-Process -Id $artPrior.pid -ErrorAction SilentlyContinue
    if (-not $artExisting) { throw 'Preview record does not identify a live process' }
    $artResult = $artPrior
} else {
    $artPython = 'C:/Users/83912/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
    $artProcess = Start-Process -FilePath $artPython -ArgumentList @('-m','http.server',"$Port",'--bind','127.0.0.1','--directory','.') -WorkingDirectory $artPreviewRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $artProjectRoot "artifacts/hd2d-preview-$Port.stdout.log") -RedirectStandardError (Join-Path $artProjectRoot "artifacts/hd2d-preview-$Port.stderr.log") -PassThru
    $artResult = [pscustomobject]@{pid=$artProcess.Id;root=$artPreviewRoot;url=$artPreviewUrl;bind='127.0.0.1';scope='generated project art only'}
    $artResult | ConvertTo-Json | Set-Content -LiteralPath $artRecordPath -Encoding utf8
}
$artResponse = Invoke-WebRequest -Uri $artPreviewUrl -TimeoutSec 5
[pscustomobject]@{server=$artResult;http=[int]$artResponse.StatusCode;length=$artResponse.RawContentLength} | ConvertTo-Json -Depth 4
