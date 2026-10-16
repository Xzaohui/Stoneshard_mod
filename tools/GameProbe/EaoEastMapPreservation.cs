using System.IO;
using UndertaleModLib;
using UndertaleModLib.Models;

// Compare actual input/readback rooms. Normalize only the sanctioned width and
// appended tile columns in memory, then fingerprint all original room fields.
internal static class EaoEastMapPreservation
{
    internal static object Validate(UndertaleData before, UndertaleData after)
    {
        var original = before.Rooms.Single(r => r.Name.Content == "r_GlobalMap");
        var candidate = after.Rooms.Single(r => r.Name.Content == "r_GlobalMap");
        var width = original.Width;
        var maps = candidate.Layers.Where(l => l.TilesData != null)
            .Select(l => (Map:l.TilesData, Width:l.TilesData.TilesX, Rows:l.TilesData.TileData)).ToArray();
        if (width is not (119*52 or 127*52) || candidate.Width != 127*52 || candidate.Height != original.Height ||
            maps.Any(m => m.Width != 127 || m.Rows.Any(row => row.Length != 127)))
            throw new InvalidDataException("Unexpected original/candidate map dimensions.");
        var columns = (int)(width/52);
        var fingerprint = EaoRooms.Fingerprint(original);
        try {
            candidate.Width = width;
            foreach (var m in maps) { m.Map.TilesX = (uint)columns; m.Map.TileData = m.Rows.Select(row => row.Take(columns).ToArray()).ToArray(); }
            if (EaoRooms.Fingerprint(candidate) != fingerprint)
                throw new InvalidDataException("Original map layers, cells, instances or metadata changed.");
        } finally {
            candidate.Width = 127*52;
            foreach (var m in maps) { m.Map.TilesX = m.Width; m.Map.TileData = m.Rows; }
        }
        return new { passed=true, readOnly=true, runtimeVerified=false, editorWidthBefore=columns, editorWidthAfter=127,
            checkedTileLayers=maps.Length, checkedOriginalCells=maps.Sum(m => m.Rows.Length*columns), originalPrefixAndMetadataIntact=true, originalFingerprint=fingerprint };
    }
}
