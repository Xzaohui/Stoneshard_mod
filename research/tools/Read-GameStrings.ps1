param(
    [string]$GameFile = 'D:\SteamLibrary\steamapps\common\Stoneshard\vanilla.win',
    [string]$Pattern = 'Gwynnel|Verren|0\.9\.4|格温|维伦',
    [int]$Limit = 50,
    [int]$MaxTextLength = 1000
)
$ErrorActionPreference = 'Stop'
if (-not ('StoryResearch.GameStrings' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
namespace StoryResearch {
    public sealed class Entry { public int Index; public uint Offset; public string Text; }
    public static class GameStrings {
        public static List<Entry> Read(string path) {
            var b = File.ReadAllBytes(path);
            if (Encoding.ASCII.GetString(b, 0, 4) != "FORM") throw new InvalidDataException("Not a FORM file");
            int p = 8;
            while (p + 8 <= b.Length) {
                string name = Encoding.ASCII.GetString(b, p, 4);
                uint size = BitConverter.ToUInt32(b, p + 4);
                long end = (long)p + 8 + size;
                if (end > b.Length) throw new InvalidDataException("Invalid chunk bounds");
                if (name == "STRG") {
                    int count = checked((int)BitConverter.ToUInt32(b, p + 8));
                    if ((long)p + 12 + 4L * count > end) throw new InvalidDataException("Invalid string table");
                    var result = new List<Entry>(count);
                    for (int i = 0; i < count; i++) {
                        uint offset = BitConverter.ToUInt32(b, p + 12 + 4 * i);
                        if ((long)offset + 4 > b.Length) throw new InvalidDataException("Invalid string pointer");
                        int len = checked((int)BitConverter.ToUInt32(b, (int)offset));
                        if ((long)offset + 4 + len > b.Length) throw new InvalidDataException("Invalid string length");
                        result.Add(new Entry { Index = i, Offset = offset, Text = Encoding.UTF8.GetString(b, (int)offset + 4, len) });
                    }
                    return result;
                }
                p = checked((int)end);
            }
            throw new InvalidDataException("STRG chunk not found");
        }
    }
}
'@
}
$entries = [StoryResearch.GameStrings]::Read($GameFile)
Write-Output "File: $GameFile; STRG count: $($entries.Count)"
$entries | Where-Object { $_.Text -match $Pattern } | Select-Object -First $Limit | ForEach-Object {
    $value = $_.Text
    if ($value.Length -gt $MaxTextLength) { $value = $value.Substring(0, $MaxTextLength) + ' [truncated]' }
    [pscustomobject]@{ Index = $_.Index; Offset = $_.Offset; Text = $value } | ConvertTo-Json -Compress
}
