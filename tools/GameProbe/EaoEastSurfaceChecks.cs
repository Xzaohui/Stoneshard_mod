using System.IO;
using System.Text.RegularExpressions;
using UndertaleModLib;
using UndertaleModLib.Decompiler;
using UndertaleModLib.Models;

// Serialized/native-interface contracts. These checks do not execute GameMaker
// generation, native collision or persistence; the actual walking/reload is separate.
internal static class EaoEastSurfaceChecks
{
    internal static string[] Validate(UndertaleData data)
    {
        var checks = new List<string>();
        void Require(bool condition, string name) { if (!condition) throw new InvalidDataException(name); checks.Add(name); }
        string Asm(string name) { var c = data.Code.Single(c => c.Name.Content == name); return c.Disassemble(data.Variables, data.CodeLocals.For(c)); }
        bool ObjectRef(string assembly, string name) => Regex.IsMatch(assembly, @"push(?:i\.e|\.i) " + data.GameObjects.IndexOf(data.GameObjects.Single(o => o.Name.Content == name)) + @"\b");
        var source = data.Rooms.Single(r => r.Name.Content == "r_steppe");
        var room = data.Rooms.Single(r => r.Name.Content == "r_eao_n2_world");
        var legacy = data.Rooms.Single(r => r.Name.Content == "r_eao_n2_sites");
        Require(room.Width == 2340 && room.Height == 2340 && source.Width == room.Width && source.Height == room.Height && !room.Persistent,
            "east-surface-native-ninety-by-ninety-geography");
        Require(legacy.Width == 1352 && legacy.Height == 988 && legacy.GameObjects.Any(i => i.ObjectDefinition.Name.Content == "o_eao_site_home"),
            "east-surface-legacy-exterior-and-exit-retained");
        Require(room.Flags == source.Flags && room.CreationCodeId == source.CreationCodeId && room.Views.Count == source.Views.Count && room.Layers.Count == source.Layers.Count && room.Tiles.Count == 0,
            "east-surface-native-outdoor-room-metadata");
        Require(room.GameObjects.Count == source.GameObjects.Count && room.GameObjects.Zip(source.GameObjects).All(p =>
            p.First.X == p.Second.X && p.First.Y == p.Second.Y && p.First.CreationCode == p.Second.CreationCode && p.First.PreCreateCode == p.Second.PreCreateCode &&
            (p.First.ObjectDefinition.Name.Content == "o_eao_east_steppe_generator" ? p.Second.ObjectDefinition.Name.Content == "o_prairieGenerationController" : p.First.ObjectDefinition == p.Second.ObjectDefinition)),
            "east-surface-only-generator-substituted-in-native-instance-order");
        Require(room.Layers.Zip(source.Layers).All(p => p.First.LayerName.Content == p.Second.LayerName.Content && p.First.LayerType == p.Second.LayerType && p.First.LayerDepth == p.Second.LayerDepth && p.First.XOffset == p.Second.XOffset && p.First.YOffset == p.Second.YOffset && p.First.IsVisible == p.Second.IsVisible),
            "east-surface-native-layer-order-and-depth");
        var generator = data.GameObjects.Single(o => o.Name.Content == "o_eao_east_steppe_generator");
        Require(generator.ParentId?.Name.Content == "o_prairieGenerationController" && generator.Events.SelectMany(e => e).Count() == 1 &&
            generator.Events[(int)EventType.Other].Single().EventSubtype == 18 && !generator.Persistent,
            "east-surface-native-generator-inheritance-only-preset-override");
        var preset = Asm("gml_Object_o_eao_east_steppe_generator_Other_18");
        Require(preset.IndexOf("event_inherited", StringComparison.Ordinal) >= 0 && preset.IndexOf("event_inherited", StringComparison.Ordinal) < preset.IndexOf("ds_grid_set_region", StringComparison.Ordinal) && preset.Contains("self.markerCollisionGrid"),
            "east-surface-preset-reserves-native-placement-grid");
        Require(new[] { "room_goto", "room_restart", "scr_atr_set_simple", "scr_gold", "EAO_resolve", "lock_movement" }.All(s => !preset.Contains(s)) && new[] { "o_player", "o_fastTurnController", "o_abstract_player" }.All(s => !ObjectRef(preset,s)),
            "east-surface-preset-never-relocates-player-or-writes-quest-state");
        Require(!preset.Contains("draw_rectangle") && !ObjectRef(preset,"o_eao_site_floor") && !ObjectRef(preset,"o_water_deep"),
            "east-surface-native-grass-without-legacy-water-or-floor-overlay");
        foreach (var id in new[] { "shed", "winch", "canal" }) {
            Require(ObjectRef(preset,"o_eao_site_building_" + id) && ObjectRef(preset,"o_eao_site_door_" + id) && ObjectRef(preset,"o_eao_site_start_" + id), "east-surface-building-and-native-return-marker-" + id);
            var enter = Asm("gml_Object_o_eao_site_door_" + id + "_Alarm_7");
            Require(enter.Contains("event_inherited") && enter.Contains("EAO_geo_sites_return") && enter.Contains("room_get_name") && !enter.Contains("scr_atr_set_simple"), "east-surface-native-door-persists-origin-" + id);
        }
        foreach (var id in new[] { "o_eao_n2_home", "o_eao_site_winch_back", "o_eao_site_canal_back" }) {
            var step = Asm("gml_Object_" + id + "_Step_0");
            Require(step.Contains("EAO_geo_sites_return") && step.Contains("r_eao_n2_world") && step.Contains("event_inherited") && !step.Contains("global.playerGrid") && !step.Contains("scr_atr_set_simple"), "east-surface-interior-return-keeps-native-grid-and-tag-" + id);
        }
        var arrival = Asm("gml_Object_o_eao_controller_Step_2");
        Require(!arrival.Contains("EAO_east_pilot") && !arrival.Contains("o_tile_transition"), "east-surface-removes-late-placeholder-rewrite-and-small-room-transitions");
        var cache = Asm("gml_GlobalScript_scr_globalmapCacheInit");
        Require(cache.Contains("r_eao_n2_world") && !cache.Contains("r_eao_n2_sites") && cache.Contains("ds_grid_width") && cache.Contains("ds_grid_resize"), "east-surface-cache-hook-updates-task-room-on-repair");
        // The resize guard must depend on the regenerated 42-column dimensions,
        // not on an allocator handle which can repeat after leaving to the title.
        Require(Regex.IsMatch(cache, @"call\.i ds_grid_width\(argc=1\)\s+pushi\.e 42\s+cmp\.i\.v EQ"), "east-surface-extension-guard-uses-dimensions-not-recycled-handle");
        foreach (var name in new[] { "Snow", "Steppe", "Sea", "Water", "Road", "Tree", "Encounter", "SingleTree", "Light", "Borders", "PaperSea", "PaperWater", "PaperRoad", "PaperTree", "PaperEncounter", "PaperSingleTree" })
            Require(cache.Contains("global.glmapBatchGrid" + name), "east-map-resizes-native-batch-" + name);
        Require(cache.Contains("ds_grid_set_region") && cache.Contains("scr_glmap_addSprite") && cache.IndexOf("global.glmapBatchGridSteppe", StringComparison.Ordinal) < cache.IndexOf("global.globalmapCacheMap", StringComparison.Ordinal),
            "east-map-native-batches-updated-before-cache-creation");
        Require(cache.Contains("scr_glmap_hasRoad") && cache.Contains("scr_glmap_findRoadTile") && cache.Contains("global.glmapBatchGridPaperRoad"),
            "east-map-road-uses-native-neighbor-frame-and-paper-pair");
        foreach (var name in new[] { "s_glmap_steppe_strip16", "s_glmap_sea_strip16", "s_glmap_sea_strip16_paper", "s_groad_steppe", "s_groad_steppe_paper", "s_groad", "s_groad_paper" }) {
            var sprite = data.Sprites.Single(s => s.Name.Content == name);
            Require(sprite.Width == 52 && sprite.Height == 52 && sprite.OriginX == 0 && sprite.OriginY == 0 && sprite.Textures.Count >= 15,
                "east-map-native-frame-geometry-" + name);
        }
        Require(!cache.Contains("call.i random") && !cache.Contains("call.i irandom") && !cache.Contains("random_set_seed") && !cache.Contains("scr_atr_set_simple") && !cache.Contains("room_goto"),
            "east-map-extension-does-not-reroll-or-write-character-position");
        var alarm = Asm("gml_Object_o_biome_generation_controller_Alarm_2");
        var presetCall = Regex.Match(alarm, @"pushi\.e 8\s+conv\.i\.v\s+call\.i event_user");
        var floraCall = Regex.Match(alarm, @"pushi\.e 9\s+conv\.i\.v\s+call\.i event_user");
        var presets = presetCall.Success ? presetCall.Index : -1;
        var flora = floraCall.Success ? floraCall.Index : -1;
        Require(presets >= 0 && flora > presets && alarm.Contains("scr_biome_connect_check"), "east-surface-preset-before-native-flora-and-connectivity-check");
        Require(ObjectRef(Asm("gml_Object_o_biome_generation_controller_Other_25"),"o_abstract_player"),
            "east-surface-player-still-created-by-native-generation-completion");
        // Independent footprint specification and native 26 / 2288-pixel arrivals.
        // Verify every possible edge row/column can enter and reach all three doors.
        var blocked = new HashSet<(int, int)>();
        foreach (var r in new[] { (25,37,33,41), (42,38,48,41), (57,37,65,41) })
            for (var x = r.Item1; x <= r.Item3; x++) for (var y = r.Item2; y <= r.Item4; y++) blocked.Add((x,y));
        var reached = new HashSet<(int,int)>(); var queue = new Queue<(int,int)>(); queue.Enqueue((1,42));
        while (queue.Count > 0) {
            var p = queue.Dequeue(); if (p.Item1 < 1 || p.Item1 > 88 || p.Item2 < 1 || p.Item2 > 88 || blocked.Contains(p) || !reached.Add(p)) continue;
            foreach (var d in new[] { (1,0), (-1,0), (0,1), (0,-1) }) queue.Enqueue((p.Item1+d.Item1, p.Item2+d.Item2));
        }
        Require(Enumerable.Range(1,88).All(n => new[] { (1,n), (88,n), (n,1), (n,88) }.All(reached.Contains)) && new[] { (29,42), (45,42), (61,42), (29,44), (45,44), (61,44) }.All(reached.Contains),
            "east-surface-all-native-edge-arrivals-and-building-returns-connected-in-authored-geometry");
        return checks.ToArray();
    }
}
