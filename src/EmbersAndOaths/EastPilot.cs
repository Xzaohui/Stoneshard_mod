using System;
using System.Linq;
using ModShardLauncher;
using UndertaleModLib.Models;

namespace EmbersAndOaths;

/// <summary>
/// GEO-02 east expansion pilot. Widens r_GlobalMap's editor layers from 119 to 127
/// cells and appends 8 local columns to the world grid AFTER vanilla generation and
/// random-sequence verification, so vanilla tiles, forests, roads and old saves keep
/// their exact random sequence. Only two cells open: (40,37) native steppe and
/// (41,37) temporarily hosting r_eao_n2_sites. Everything else stays blocked.
/// </summary>
internal static class EastPilot
{
    internal const int VanillaCells = 119, Added = 8;
    internal const string CacheInit = "gml_GlobalScript_scr_globalmapCacheInit";

    internal static void WidenRoom()
    {
        var room = Msl.GetRoom("r_GlobalMap");
        if (room.Width == (VanillaCells + Added) * 52) return;
        if (room.Width != VanillaCells * 52) throw new InvalidOperationException("r_GlobalMap width changed: " + room.Width);
        room.Width = (uint)((VanillaCells + Added) * 52);
        foreach (var layer in room.Layers.Where(l => l.TilesData != null)) {
            var t = layer.TilesData;
            if (t.TilesX != VanillaCells) throw new InvalidOperationException("Unexpected tile layer width: " + layer.LayerName.Content);
            var old = t.TileData;
            var name = layer.LayerName.Content;
            // Editor-only fill (generation still stops at o_border_down_right=118):
            // biome sea, full sea shore index; every other layer empty so paper
            // regions never claim the new columns.
            uint fill = name == "Biomes" ? 8u : name == "Sea" ? 15u : 0u;
            var rows = new uint[old.Length][];
            for (var y = 0; y < old.Length; y++) {
                rows[y] = new uint[VanillaCells + Added];
                Array.Copy(old[y], rows[y], VanillaCells);
                for (var x = VanillaCells; x < VanillaCells + Added; x++) rows[y][x] = fill;
            }
            t.TilesX = VanillaCells + Added;
            t.TileData = rows;
        }
    }

    internal static void Configure(Action<UndertaleGameObject, string, EventType, uint> set, ModFile files)
    {
        WidenRoom();
        var cache = Msl.GetStringGMLFromFile(CacheInit);
        if (!cache.Contains("EAO_east_grid")) {
            var head = cache.IndexOf("function scr_globalmapCacheInit", StringComparison.Ordinal);
            var brace = head < 0 ? -1 : cache.IndexOf('{', head);
            if (brace < 0 || !cache.Contains("o_globalmapCacheQueueController")) throw new InvalidOperationException("scr_globalmapCacheInit changed; refusing east pilot hook.");
            cache = cache.Insert(brace + 1, "\n" + files.GetCode("east_pilot_widen.gml") + "\n");
            Msl.SetStringGMLInFile(cache, CacheInit);
        }
    }
}
