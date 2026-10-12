param(
    [string]$GameFile = 'D:\SteamLibrary\steamapps\common\Stoneshard\vanilla.win'
)
$ErrorActionPreference = 'Stop'
# Load the existing read-only STRG reader. Do not write to the game directory.
$null = & (Join-Path $PSScriptRoot 'Read-GameStrings.ps1') -GameFile $GameFile -Pattern '^__no_match__$' -Limit 1
$taskNames = [ordered]@{
    Aldwynn='奥尔德文'; Skonfert='斯孔弗特'; Yostwayne='约斯特文'; Kord='考德'
    Maen='曼恩'; Eeders='伊德斯'; Forholt='佛尔霍特'; Ratten='拉滕'
}
$taskEntries = [StoryResearch.GameStrings]::Read($GameFile)
$taskReferences = @($taskEntries | ForEach-Object {
    $taskEntry = $_
    $taskFields = $taskEntry.Text -split ';'
    if ($taskFields.Count -lt 4 -or $taskFields[0] -notmatch "^[A-Za-z0-9_ .'-]{0,100}$") { return }
    $taskChineseIndex = -1
    for ($taskFieldIndex=1; $taskFieldIndex -lt $taskFields.Count; $taskFieldIndex++) {
        if ($taskFields[$taskFieldIndex] -match '[\u4e00-\u9fff]') { $taskChineseIndex=$taskFieldIndex; break }
    }
    if ($taskChineseIndex -lt 2) { return }
    $taskEnglish = $taskFields[$taskChineseIndex-1]
    $taskChinese = $taskFields[$taskChineseIndex]
    $taskMatches = @($taskNames.Keys | Where-Object {
        $taskEnglish -match [regex]::Escape($_) -or
        $taskChinese -match [regex]::Escape($taskNames[$_]) -or
        $taskFields[0] -match [regex]::Escape($_)
    })
    if ($taskMatches.Count -eq 0) { return }
    [pscustomobject]@{
        strg_index=$taskEntry.Index; offset=$taskEntry.Offset; key=$taskFields[0]
        towns=$taskMatches; chinese_field_index=$taskChineseIndex
        english_length=$taskEnglish.Length; chinese_length=$taskChinese.Length
        status='candidate requiring contextual review; name similarity is not proof of relationship'
    }
})
$taskOutput = Join-Path (Split-Path $PSScriptRoot -Parent) 'settlement-reference-index.json'
[pscustomobject]@{
    checked_at='2026-10-11'; game_file=$GameFile; strg_count=$taskEntries.Count
    method='Localized fields and matching row keys; metadata only, no full dialogue retained'
    candidate_count=$taskReferences.Count; references=$taskReferences
    limitation='Candidate package purity, runtime accessibility, same-name people and historical claims require separate review'
} | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $taskOutput -Encoding UTF8
Write-Output "Indexed $($taskReferences.Count) candidates from $($taskEntries.Count) strings; output: $taskOutput"
