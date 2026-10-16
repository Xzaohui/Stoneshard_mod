using System.IO;
using UndertaleModLib;
using UndertaleModLib.Models;

// Compare actual input/readback rooms. The 119 original editor columns and all
// original metadata/layers/instances remain exact. EAO's appended columns and
// its named paper layer are checked separately by EaoEastRegionChecks.
internal static class EaoEastMapPreservation
{
    internal static object Validate(UndertaleData before, UndertaleData after)
    {
        var original = before.Rooms.Single(r => r.Name.Content == "r_GlobalMap");
        var candidate = after.Rooms.Single(r => r.Name.Content == "r_GlobalMap");
        if (candidate.Width != 127*52 || candidate.Height != original.Height) throw new InvalidDataException("Map dimensions.");
        string Prefix(UndertaleRoom room) {
            var width=room.Width;
            var owned=room.Layers.SingleOrDefault(l=>l.LayerName.Content=="map_eao_east");
            var ownedIndex=owned==null ? -1 : room.Layers.IndexOf(owned);
            var maps=room.Layers.Where(l=>l.TilesData!=null && l!=owned)
                .Select(l=>(Map:l.TilesData,Width:l.TilesData.TilesX,Rows:l.TilesData.TileData)).ToArray();
            if(width is not (119*52 or 127*52) || maps.Length!=42 || maps.Any(m=>m.Width!=width/52 || m.Rows.Any(row=>row.Length!=width/52)))
                throw new InvalidDataException("Unexpected original map layer shape.");
            try {
                if(owned!=null)room.Layers.Remove(owned);
                room.Width=119*52;
                foreach(var m in maps){m.Map.TilesX=119;m.Map.TileData=m.Rows.Select(row=>row.Take(119).ToArray()).ToArray();}
                return EaoRooms.Fingerprint(room);
            } finally {
                room.Width=width;
                foreach(var m in maps){m.Map.TilesX=m.Width;m.Map.TileData=m.Rows;}
                if(owned!=null)room.Layers.Insert(ownedIndex,owned);
            }
        }
        var fingerprint=Prefix(original);
        if(Prefix(candidate)!=fingerprint)throw new InvalidDataException("Original map layers, cells, instances or metadata changed.");
        return new { passed=true, readOnly=true, runtimeVerified=false, editorWidthBefore=original.Width/52, editorWidthAfter=127,
            checkedTileLayers=42, checkedOriginalCells=42*79*119, originalPrefixAndMetadataIntact=true, originalFingerprint=fingerprint,
            ownedAppendixScope="EAO columns 119..126 and map_eao_east validated separately" };
    }
}
