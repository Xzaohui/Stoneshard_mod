param([string]$ProjectRoot = (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent))
$ErrorActionPreference = 'Stop'
$vault = Join-Path $ProjectRoot 'design'
$model = Get-Content -LiteralPath (Join-Path $ProjectRoot 'research/design-model.json') -Raw | ConvertFrom-Json
$notes = @(Get-ChildItem -LiteralPath $vault -Filter '*.md' -Recurse | Where-Object { $_.Name -ne 'AGENTS.md' })
$errors = [System.Collections.Generic.List[string]]::new()
$byName = @{}
$ids = @{}
$texts = @{}
$incoming = @{}
$linkCount = 0
foreach ($note in $notes) {
    $body = Get-Content -LiteralPath $note.FullName -Raw
    $texts[$note.BaseName] = $body
    if ($byName.ContainsKey($note.BaseName)) { $errors.Add("Duplicate note name: $($note.BaseName)") }
    $byName[$note.BaseName] = $note.FullName
    $incoming[$note.BaseName] = 0
    if ($body -notmatch '(?s)^---\r?\n.*?\r?\n---') { $errors.Add("Missing frontmatter: $($note.Name)") }
    foreach ($field in @('title','id','type','status','canon','baseline','updated','tags','aliases')) {
        if ($body -notmatch "(?m)^${field}:") { $errors.Add("Missing ${field}: $($note.Name)") }
    }
    $idMatch = [regex]::Match($body, '(?m)^id:\s*(\S+)')
    if ($idMatch.Success) {
        $id = $idMatch.Groups[1].Value
        if ($ids.ContainsKey($id)) { $errors.Add("Duplicate ID: $id") }
        $ids[$id] = $note.FullName
    }
    if (([regex]::Matches($body, '(?m)^```')).Count % 2 -ne 0) { $errors.Add("Unbalanced code fences: $($note.Name)") }
}
foreach ($note in $notes) {
    foreach ($match in [regex]::Matches($texts[$note.BaseName], '\[\[([^\]]+)\]\]')) {
        $linkCount++
        $rawTarget = ($match.Groups[1].Value -split '\|', 2)[0]
        $parts = $rawTarget -split '#', 2
        $target = $parts[0]
        if (-not $target) { $target = $note.BaseName }
        if (-not $byName.ContainsKey($target)) { $errors.Add("Broken wikilink: $($note.Name) -> $rawTarget"); continue }
        $incoming[$target]++
        if ($parts.Count -gt 1 -and -not $parts[1].StartsWith('^')) {
            $heading = [regex]::Escape($parts[1])
            if ($texts[$target] -notmatch "(?m)^#{1,6}\s+${heading}\s*$") { $errors.Add("Missing heading: $($note.Name) -> $rawTarget") }
        }
    }
}
foreach ($name in $incoming.Keys) { if ($incoming[$name] -eq 0) { $errors.Add("No incoming link: $name") } }
foreach ($entity in @($model.main_quests) + @($model.regions) + @($model.side_chains) + @($model.daily_templates) + @($model.dungeons) + @($model.factions) + @($model.characters)) {
    if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot $entity.file))) { $errors.Add("Missing entity file: $($entity.file)") }
}
$expected = @{ main_quests=18; regions=6; side_chains=8; daily_templates=16; dungeons=10; factions=8; characters=12 }
foreach ($key in $expected.Keys) { if (@($model.$key).Count -ne $expected[$key]) { $errors.Add("Unexpected count: $key") } }
$nodeTotal = ($model.regions | Measure-Object -Property nodes -Sum).Sum
if ($nodeTotal -ne 54) { $errors.Add("Unexpected node budget: $nodeTotal") }
$stages = @($model.side_chains | ForEach-Object { $_.stages })
if ($stages.Count -ne 24 -or @($stages | Select-Object -Unique).Count -ne 24) { $errors.Add('Side stage count or uniqueness invalid') }
$qids = @($model.main_quests.id)
foreach ($q in $model.main_quests) {
    foreach ($req in @($q.requires) + @($q.at_least.of)) { if ($req -and $req -notin $qids) { $errors.Add("Unknown prerequisite: $($q.id) -> $req") } }
}
function Test-Prerequisites($Quest, $Done) {
    foreach ($req in $Quest.requires) { if (-not $Done.Contains($req)) { return $false } }
    if ($Quest.at_least) {
        $have = @($Quest.at_least.of | Where-Object { $Done.Contains($_) }).Count
        if ($have -lt $Quest.at_least.count) { return $false }
    }
    return $true
}
$paths = @()
foreach ($skip in @('MQ06','MQ07','MQ08','none')) {
    $done = [System.Collections.Generic.HashSet[string]]::new()
    $changed = $true
    while ($changed) {
        $changed = $false
        foreach ($q in $model.main_quests) {
            if ($q.id -eq $skip -or $done.Contains($q.id)) { continue }
            if (Test-Prerequisites $q $done) { [void]$done.Add($q.id); $changed = $true }
        }
    }
    if (-not $done.Contains('MQ18')) { $errors.Add("Main path blocked with skipped branch $skip") }
    $evidence = @()
    foreach ($p in $model.evidence_producers.PSObject.Properties) {
        if (@($p.Value | Where-Object { $done.Contains($_) }).Count -gt 0) { $evidence += $p.Name }
    }
    if ('E04' -notin $evidence -or 'E05' -notin $evidence) { $errors.Add("Missing fallback/containment evidence with skip $skip") }
    $paths += [pscustomobject]@{ skipped_branch=$skip; reachable_quests=$done.Count; reaches_MQ18=$done.Contains('MQ18'); evidence=$evidence }
}
# Independent document graph connectivity, treating travel edges as bidirectional.
if ($model.active_story) {
    $taskActiveIds = @($model.active_story.id)
    if (@($taskActiveIds | Select-Object -Unique).Count -ne $taskActiveIds.Count) { $errors.Add('Active story IDs duplicated') }
    foreach ($taskChapter in $model.active_story) {
        if (!(Test-Path -LiteralPath (Join-Path $ProjectRoot $taskChapter.file))) { $errors.Add("Active story note missing: $($taskChapter.id)") }
        foreach ($taskRequirement in @($taskChapter.requires) + @($taskChapter.at_least.of)) {
            if ($taskRequirement -and ($taskRequirement -notin $taskActiveIds -or $taskRequirement -in @('MQ01','MQ02'))) { $errors.Add("Active story requires missing or retired chapter: $taskRequirement") }
        }
    }
    $taskReached = [System.Collections.Generic.HashSet[string]]::new()
    do {
        $taskChanged = $false
        foreach ($taskChapter in $model.active_story) {
            if (!$taskReached.Contains($taskChapter.id) -and (Test-Prerequisites $taskChapter $taskReached)) { [void]$taskReached.Add($taskChapter.id); $taskChanged = $true }
        }
    } while ($taskChanged)
    if ($taskReached.Count -ne $taskActiveIds.Count) { $errors.Add('Active story graph cyclic or unreachable') }
    foreach ($taskRetired in @('MQ01_营火旁的迟信','MQ02_盐封的货单')) { if ($texts[$taskRetired] -notmatch '(?m)^status: retired$') { $errors.Add("Retired note still active: $taskRetired") } }
}
$reachable = [System.Collections.Generic.HashSet[string]]::new()
[void]$reachable.Add('BASE')
$changed = $true
while ($changed) {
    $changed = $false
    foreach ($edge in $model.region_edges) {
        if ($reachable.Contains($edge[0]) -and $reachable.Add($edge[1])) { $changed=$true }
        if ($reachable.Contains($edge[1]) -and $reachable.Add($edge[0])) { $changed=$true }
    }
}
foreach ($region in $model.regions) { if (-not $reachable.Contains($region.id)) { $errors.Add("Disconnected region: $($region.id)") } }
$report = [ordered]@{
    date='2026-10-12'; scope='Static documentation only; historical MQ graph kept separate from current N1-N18 screenplays; S62 narrative evaluation has separate report; no game runtime validation';
    legacy_graph_status=$model.legacy_graph_status; active_story_chapters=@($model.active_story).Count;
    notes=$notes.Count; wikilinks=$linkCount; unique_ids=$ids.Count; region_node_budget=$nodeTotal;
    side_stages=$stages.Count; dependency_paths=$paths; regions_connected=($reachable.Count -eq 7);
    errors=@($errors); passed=($errors.Count -eq 0)
}
$json = $report | ConvertTo-Json -Depth 12
[System.IO.File]::WriteAllText((Join-Path $ProjectRoot 'research/vault-validation.json'), $json + "`n", [System.Text.UTF8Encoding]::new($false))
Write-Output $json
if ($errors.Count -gt 0) { exit 1 }
